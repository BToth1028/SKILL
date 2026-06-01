#!/usr/bin/env python3
"""
test_load_typedb_snapshot_search.py — pure-function tests for incremental
hash dedup, chunk-budget caps, and deterministic point UUIDs in
load_typedb_snapshot_search.py.

No live Qdrant or FastEmbed required.

Run (from this tooling dir):
	python test_load_typedb_snapshot_search.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import load_typedb_snapshot_search as loader


BOOTSTRAP_HANDOFF_FILE = "c-dev_260505-1808_ontology-tutor-audit-handoff.yaml"
BOOTSTRAP_HANDOFF_SOURCE = f"bootstrap_yamls/{BOOTSTRAP_HANDOFF_FILE}"


def make_chunk(source_file: str, chunk_index: int, body: str, banner: str = "[BANNER]\n") -> dict:
	"""Build a chunk dict mirroring the loader's structure.

	`body` is the raw post-chunk file content (cache-key basis).
	`banner` defaults to a constant marker so tests can assert that banner
	bytes do NOT influence the hash routing.
	"""
	return {
		"text": banner + body,
		"body_text": body,
		"source_file": source_file,
		"chunk_index": chunk_index,
	}


def test_hash_determinism() -> bool:
	h1 = loader.compute_chunk_hash("hello world")
	h2 = loader.compute_chunk_hash("hello world")
	if h1 != h2:
		print(f"FAIL hash_determinism: same input produced {h1[:12]} != {h2[:12]}")
		return False
	if len(h1) != 64:
		print(f"FAIL hash_determinism: expected 64 hex chars, got {len(h1)}")
		return False
	if any(c not in "0123456789abcdef" for c in h1):
		print(f"FAIL hash_determinism: non-hex chars in {h1}")
		return False
	print("PASS hash_determinism: deterministic 64-hex SHA-256")
	return True


def test_hash_byte_sensitivity() -> bool:
	h_lower = loader.compute_chunk_hash("entity")
	h_upper = loader.compute_chunk_hash("Entity")
	h_trail = loader.compute_chunk_hash("Entity ")
	h_lead = loader.compute_chunk_hash(" Entity")
	h_multibyte = loader.compute_chunk_hash("Entityé")
	if len({h_lower, h_upper, h_trail, h_lead, h_multibyte}) != 5:
		print("FAIL hash_byte_sensitivity: case/whitespace/multibyte collisions detected")
		return False
	print("PASS hash_byte_sensitivity: case + whitespace + multibyte all distinct")
	return True


def test_uuid_determinism() -> bool:
	u1 = loader.compute_point_uuid("col-x", "docs/foo.html", 3)
	u2 = loader.compute_point_uuid("col-x", "docs/foo.html", 3)
	u3 = loader.compute_point_uuid("col-x", "docs/foo.html", 4)
	u4 = loader.compute_point_uuid("col-y", "docs/foo.html", 3)
	u5 = loader.compute_point_uuid("col-x", "docs/bar.html", 3)
	if u1 != u2:
		print(f"FAIL uuid_determinism: same key produced {u1} != {u2}")
		return False
	if len({u1, u3, u4, u5}) != 4:
		print("FAIL uuid_determinism: distinct keys collided to same UUID")
		return False
	if len(u1) != 36 or u1.count("-") != 4:
		print(f"FAIL uuid_determinism: not a UUID-shaped string: {u1}")
		return False
	print("PASS uuid_determinism: deterministic per (collection, source_file, chunk_index)")
	return True


def test_partition_empty_existing() -> bool:
	candidates = [
		make_chunk("a.html", 0, "hello"),
		make_chunk("a.html", 1, "world"),
	]
	parts = loader.partition_chunks_for_incremental({}, candidates)
	if len(parts["new"]) != 2:
		print(f"FAIL partition_empty_existing: expected 2 new, got {len(parts['new'])}")
		return False
	if parts["changed"] or parts["unchanged"] or parts["orphans"]:
		print(f"FAIL partition_empty_existing: non-new buckets non-empty: {parts}")
		return False
	print("PASS partition_empty_existing: empty existing -> all candidates new")
	return True


def test_partition_all_unchanged() -> bool:
	candidates = [
		make_chunk("a.html", 0, "hello"),
		make_chunk("a.html", 1, "world"),
	]
	existing = {
		("a.html", 0): loader.compute_chunk_hash("hello"),
		("a.html", 1): loader.compute_chunk_hash("world"),
	}
	parts = loader.partition_chunks_for_incremental(existing, candidates)
	if parts["new"] or parts["changed"] or parts["orphans"]:
		print(f"FAIL partition_all_unchanged: non-unchanged buckets non-empty: {parts}")
		return False
	if len(parts["unchanged"]) != 2:
		print(f"FAIL partition_all_unchanged: expected 2 unchanged, got {len(parts['unchanged'])}")
		return False
	print("PASS partition_all_unchanged: matching hashes -> all skipped")
	return True


def test_partition_changed_hash() -> bool:
	candidates = [make_chunk("a.html", 0, "hello world")]
	existing = {("a.html", 0): loader.compute_chunk_hash("hello")}
	parts = loader.partition_chunks_for_incremental(existing, candidates)
	if len(parts["changed"]) != 1:
		print(f"FAIL partition_changed_hash: expected 1 changed, got {len(parts['changed'])}")
		return False
	if parts["new"] or parts["unchanged"] or parts["orphans"]:
		print(f"FAIL partition_changed_hash: other buckets non-empty: {parts}")
		return False
	print("PASS partition_changed_hash: hash mismatch routes to changed")
	return True


def test_partition_legacy_short_hash_routes_to_changed() -> bool:
	candidates = [make_chunk("a.html", 0, "stable text")]
	existing = {("a.html", 0): loader.compute_chunk_hash("stable text")[:16]}
	parts = loader.partition_chunks_for_incremental(existing, candidates)
	if len(parts["changed"]) != 1:
		print(f"FAIL legacy_short_hash: expected 1 changed (16-hex != 64-hex), got {parts}")
		return False
	print("PASS legacy_short_hash: 16-hex legacy hash treated as mismatch -> changed")
	return True


def test_partition_orphan() -> bool:
	candidates: list[dict] = []
	existing = {("a.html", 0): "deadbeef" * 8}
	parts = loader.partition_chunks_for_incremental(existing, candidates)
	if len(parts["orphans"]) != 1:
		print(f"FAIL partition_orphan: expected 1 orphan, got {len(parts['orphans'])}")
		return False
	if parts["orphans"][0] != ("a.html", 0):
		print(f"FAIL partition_orphan: wrong key {parts['orphans'][0]}")
		return False
	print("PASS partition_orphan: existing-but-absent key routes to orphans")
	return True


def test_partition_mixed_all_four_buckets() -> bool:
	candidates = [
		make_chunk("a.html", 0, "new chunk text"),
		make_chunk("a.html", 1, "unchanged chunk"),
		make_chunk("b.html", 0, "changed text now"),
	]
	existing = {
		("a.html", 1): loader.compute_chunk_hash("unchanged chunk"),
		("b.html", 0): loader.compute_chunk_hash("OLD changed text"),
		("c.html", 0): "stale_hash_value_a",
		("c.html", 1): "stale_hash_value_b",
	}
	parts = loader.partition_chunks_for_incremental(existing, candidates)
	new_keys = {(c["source_file"], c["chunk_index"]) for c in parts["new"]}
	changed_keys = {(c["source_file"], c["chunk_index"]) for c in parts["changed"]}
	unchanged_keys = {(c["source_file"], c["chunk_index"]) for c in parts["unchanged"]}
	orphan_keys = set(parts["orphans"])
	if new_keys != {("a.html", 0)}:
		print(f"FAIL partition_mixed: new keys = {new_keys}")
		return False
	if changed_keys != {("b.html", 0)}:
		print(f"FAIL partition_mixed: changed keys = {changed_keys}")
		return False
	if unchanged_keys != {("a.html", 1)}:
		print(f"FAIL partition_mixed: unchanged keys = {unchanged_keys}")
		return False
	if orphan_keys != {("c.html", 0), ("c.html", 1)}:
		print(f"FAIL partition_mixed: orphan keys = {orphan_keys}")
		return False
	print("PASS partition_mixed: all four buckets populated correctly")
	return True


def test_partition_empty_candidates_all_orphan() -> bool:
	candidates: list[dict] = []
	existing = {("a.html", 0): "h0", ("b.html", 1): "h1"}
	parts = loader.partition_chunks_for_incremental(existing, candidates)
	if (
		len(parts["orphans"]) != 2
		or parts["new"]
		or parts["changed"]
		or parts["unchanged"]
	):
		print(f"FAIL partition_empty_candidates: {parts}")
		return False
	print("PASS partition_empty_candidates: all existing become orphans")
	return True


def test_uuid_round_trip_with_orphan_keys() -> bool:
	collection = "test-col"
	keys = [("docs/a.html", 0), ("docs/a.html", 1), ("docs/b.html", 0)]
	upsert_uuids = {k: loader.compute_point_uuid(collection, k[0], k[1]) for k in keys}
	delete_uuids = {k: loader.compute_point_uuid(collection, k[0], k[1]) for k in keys}
	if upsert_uuids != delete_uuids:
		print("FAIL uuid_round_trip: upsert UUIDs != delete UUIDs for same keys")
		return False
	if len(set(upsert_uuids.values())) != len(keys):
		print("FAIL uuid_round_trip: distinct keys produced colliding UUIDs")
		return False
	print("PASS uuid_round_trip: orphan deletion can recompute upsert UUID exactly")
	return True


def test_apply_chunk_cap_per_file_no_cap() -> bool:
	chunks = ["a", "b", "c", "d", "e"]
	out = loader.apply_chunk_cap_per_file(chunks, 0, "x.html")
	if out != chunks:
		print(f"FAIL chunk_cap_per_file_no_cap: cap=0 should pass through, got {out}")
		return False
	print("PASS chunk_cap_per_file_no_cap: cap=0 = uncapped")
	return True


def test_apply_chunk_cap_per_file_under_cap() -> bool:
	chunks = ["a", "b", "c"]
	out = loader.apply_chunk_cap_per_file(chunks, 10, "x.html")
	if out != chunks:
		print(f"FAIL chunk_cap_per_file_under_cap: under cap should pass through, got {out}")
		return False
	print("PASS chunk_cap_per_file_under_cap: under cap -> unchanged")
	return True


def test_apply_chunk_cap_per_file_truncates() -> bool:
	chunks = ["a", "b", "c", "d", "e"]
	out = loader.apply_chunk_cap_per_file(chunks, 3, "x.html")
	if out != ["a", "b", "c"]:
		print(f"FAIL chunk_cap_per_file_truncates: expected first 3, got {out}")
		return False
	print("PASS chunk_cap_per_file_truncates: keeps first N chunks deterministically")
	return True


def test_apply_chunk_cap_total_no_cap() -> bool:
	chunks = [{"i": i} for i in range(5)]
	out = loader.apply_chunk_cap_total(chunks, 0)
	if out != chunks:
		print(f"FAIL chunk_cap_total_no_cap: cap=0 should pass through")
		return False
	print("PASS chunk_cap_total_no_cap: cap=0 = uncapped")
	return True


def test_apply_chunk_cap_total_truncates() -> bool:
	chunks = [{"i": i} for i in range(10)]
	out = loader.apply_chunk_cap_total(chunks, 4)
	if len(out) != 4 or [c["i"] for c in out] != [0, 1, 2, 3]:
		print(f"FAIL chunk_cap_total_truncates: expected first 4, got {out}")
		return False
	print("PASS chunk_cap_total_truncates: keeps first N total chunks")
	return True


def test_partition_banner_change_does_not_reroute() -> bool:
	"""Critical: banner changes (router_version bumps, stamp tweaks) must NOT
	move a chunk to 'changed'. Hash basis is body_text only.
	"""
	body = "stable source body bytes from snapshot"
	candidates = [make_chunk("a.html", 0, body, banner="[BANNER router_version: 1.1.6]\n")]
	existing = {("a.html", 0): loader.compute_chunk_hash(body)}
	parts = loader.partition_chunks_for_incremental(existing, candidates)
	if len(parts["unchanged"]) != 1:
		print(
			f"FAIL banner_change_does_not_reroute: expected unchanged=1, got "
			f"new={len(parts['new'])} changed={len(parts['changed'])} "
			f"unchanged={len(parts['unchanged'])} orphans={len(parts['orphans'])}"
		)
		return False
	if parts["new"] or parts["changed"] or parts["orphans"]:
		print(f"FAIL banner_change_does_not_reroute: other buckets non-empty: {parts}")
		return False
	print("PASS banner_change_does_not_reroute: banner-only change keeps chunk in 'unchanged'")
	return True


def test_partition_body_change_routes_to_changed() -> bool:
	"""Mirror of the above: when the BODY changes (banner identical), chunk
	must route to 'changed'. Confirms the hash basis is sensitive to source bytes.
	"""
	old_body = "version 1 of the source body"
	new_body = "version 2 of the source body"
	banner = "[BANNER identical across runs]\n"
	candidates = [make_chunk("a.html", 0, new_body, banner=banner)]
	existing = {("a.html", 0): loader.compute_chunk_hash(old_body)}
	parts = loader.partition_chunks_for_incremental(existing, candidates)
	if len(parts["changed"]) != 1:
		print(f"FAIL body_change_routes_to_changed: expected changed=1, got {parts}")
		return False
	print("PASS body_change_routes_to_changed: body diff routes to 'changed' even with identical banner")
	return True


def test_partition_does_not_mutate_inputs() -> bool:
	candidates = [make_chunk("a.html", 0, "hello")]
	existing = {("a.html", 0): loader.compute_chunk_hash("hello")}
	candidates_snapshot = [dict(c) for c in candidates]
	existing_snapshot = dict(existing)
	loader.partition_chunks_for_incremental(existing, candidates)
	if candidates != candidates_snapshot:
		print("FAIL partition_no_mutation: candidates list mutated")
		return False
	if existing != existing_snapshot:
		print("FAIL partition_no_mutation: existing dict mutated")
		return False
	print("PASS partition_no_mutation: inputs unchanged")
	return True


def make_router_chunk(
	source_file: str,
	chunk_index: int,
	body: str,
	router_version: str = "1.1.8",
	routing_ids: list[str] | None = None,
	skill_id: str = "ontology-tutor",
) -> dict:
	"""Build a chunk dict shaped like build_ontology_skill_registry_chunks output.

	Includes ontology_router_extra and a banner-bearing `text` string so the
	refresh helper can read both the new metadata fields and the new document.
	"""
	if routing_ids is None:
		routing_ids = ["R-F010_FOLDERS", "R-G010_GENERAL", "R-V010_VALIDATE"]
	primary = routing_ids[0]
	rs = ",".join(routing_ids)
	banner = (
		"[ONTOLOGY-TUTOR SNAPSHOT_REGISTRY_VECTOR]\n"
		f"[skill_id: {skill_id} router_version: {router_version} routing_id_primary: {primary} "
		f"routing_ids_utf8_lexicographic: {rs} lineage_source: {source_file}]\n\n"
	)
	return {
		"text": banner + body,
		"body_text": body,
		"source_file": source_file,
		"chunk_index": chunk_index,
		"chunk_count": 1,
		"file_size": len(body),
		"typedb_version": "unknown",
		"content_type": "prose",
		"syntax_safe_for_3x": True,
		"ontology_router_extra": {
			"skill_id": skill_id,
			"router_version": router_version,
			"routing_id": primary,
			"routing_ids_utf8_lexicographic": list(routing_ids),
			"lineage_source": source_file,
			"typedb_authority_plane": "offline_snapshot",
		},
	}


def make_existing_payload(
	source_file: str,
	chunk_index: int,
	body: str,
	router_version: str = "1.1.6",
	routing_ids: list[str] | None = None,
) -> dict:
	"""Build an existing Qdrant-shaped payload with stale ROUTER metadata."""
	if routing_ids is None:
		routing_ids = ["R-G010_GENERAL", "R-S011_FOLDERS", "R-V010_VALIDATE_UTILIX"]
	return {
		"document": "[OLD BANNER]\n" + body,
		"metadata": {
			"source_file": source_file,
			"chunk_index": chunk_index,
			"chunk_count": 1,
			"file_size": len(body),
			"content_hash": loader.compute_chunk_hash(body),
			"approx_tokens": loader.approx_tokens(body),
			"typedb_version": "unknown",
			"content_type": "prose",
			"syntax_safe_for_3x": True,
			"skill_id": "ontology-tutor",
			"router_version": router_version,
			"routing_id": routing_ids[0],
			"routing_ids_utf8_lexicographic": list(routing_ids),
			"lineage_source": source_file,
			"typedb_authority_plane": "offline_snapshot",
		},
	}


def test_refresh_payload_preserves_content_hash_and_keys() -> bool:
	body = "stable snapshot body bytes"
	existing = make_existing_payload("docs/a.html", 0, body, router_version="1.1.6")
	chunk = make_router_chunk("docs/a.html", 0, body, router_version="1.1.8")

	refreshed = loader.build_router_metadata_refresh_payload(existing, chunk)
	if refreshed is None:
		print("FAIL refresh_payload_preserves: helper returned None for matching hashes")
		return False
	meta = refreshed.get("metadata")
	if not isinstance(meta, dict):
		print("FAIL refresh_payload_preserves: metadata missing in refreshed payload")
		return False
	expected_hash = loader.compute_chunk_hash(body)
	if meta.get("content_hash") != expected_hash:
		print(f"FAIL refresh_payload_preserves: content_hash changed; expected={expected_hash[:12]}... got={meta.get('content_hash')}")
		return False
	if meta.get("source_file") != "docs/a.html" or meta.get("chunk_index") != 0:
		print(f"FAIL refresh_payload_preserves: identity keys changed; got source_file={meta.get('source_file')} chunk_index={meta.get('chunk_index')}")
		return False
	if meta.get("router_version") != "1.1.8":
		print(f"FAIL refresh_payload_preserves: router_version not bumped; got {meta.get('router_version')}")
		return False
	rids = meta.get("routing_ids_utf8_lexicographic")
	if rids != ["R-F010_FOLDERS", "R-G010_GENERAL", "R-V010_VALIDATE"]:
		print(f"FAIL refresh_payload_preserves: routing IDs not refreshed; got {rids}")
		return False
	for stale_id in ("R-S011_FOLDERS", "R-V010_VALIDATE_UTILIX", "R-V020_VALIDATE_STANDARD"):
		if stale_id in (rids or []):
			print(f"FAIL refresh_payload_preserves: stale routing id {stale_id} still present in {rids}")
			return False
	for preserved_key in ("typedb_version", "content_type", "syntax_safe_for_3x", "chunk_count", "file_size"):
		if meta.get(preserved_key) != existing["metadata"][preserved_key]:
			print(f"FAIL refresh_payload_preserves: {preserved_key} changed unexpectedly")
			return False
	print("PASS refresh_payload_preserves: hash + identity + source-derived metadata preserved; router fields refreshed")
	return True


def test_refresh_payload_replaces_document_banner() -> bool:
	body = "stable body"
	existing = make_existing_payload("docs/a.html", 0, body, router_version="1.1.6")
	chunk = make_router_chunk(
		"docs/a.html",
		0,
		body,
		router_version="1.1.8",
		routing_ids=["R-F010_FOLDERS", "R-G010_GENERAL", "R-V010_VALIDATE"],
	)

	refreshed = loader.build_router_metadata_refresh_payload(existing, chunk)
	if refreshed is None:
		print("FAIL refresh_payload_document: helper returned None")
		return False
	doc = refreshed.get("document")
	if not isinstance(doc, str) or not doc:
		print("FAIL refresh_payload_document: document missing from refreshed payload")
		return False
	if "router_version: 1.1.8" not in doc:
		print(f"FAIL refresh_payload_document: refreshed document missing current router_version banner")
		return False
	if "router_version: 1.1.6" in doc:
		print("FAIL refresh_payload_document: refreshed document still shows stale router_version 1.1.6")
		return False
	for current_id in ("R-F010_FOLDERS", "R-V010_VALIDATE"):
		if current_id not in doc:
			print(f"FAIL refresh_payload_document: missing current routing id {current_id} in document")
			return False
	for stale_id in ("R-S011_FOLDERS", "R-V010_VALIDATE_UTILIX"):
		if stale_id in doc:
			print(f"FAIL refresh_payload_document: stale routing id {stale_id} still present in document")
			return False
	if doc.endswith(body) is False or body not in doc:
		print("FAIL refresh_payload_document: source body bytes missing from refreshed document")
		return False
	print("PASS refresh_payload_document: document banner refreshed without touching source body")
	return True


def test_refresh_payload_rejects_hash_mismatch() -> bool:
	body_old = "first version body"
	body_new = "second version body bytes (different)"
	existing = make_existing_payload("docs/a.html", 0, body_old)
	chunk = make_router_chunk("docs/a.html", 0, body_new)

	refreshed = loader.build_router_metadata_refresh_payload(existing, chunk)
	if refreshed is not None:
		print(f"FAIL refresh_payload_rejects_mismatch: expected None for hash mismatch, got {refreshed}")
		return False
	print("PASS refresh_payload_rejects_mismatch: hash mismatch refused (cannot mask source drift as metadata refresh)")
	return True


def test_refresh_payload_rejects_missing_existing_metadata() -> bool:
	body = "body"
	chunk = make_router_chunk("docs/a.html", 0, body)
	for bad in (
		None,
		{},
		{"document": "x"},
		{"metadata": "not a dict"},
		{"metadata": {"source_file": "docs/a.html"}},
	):
		refreshed = loader.build_router_metadata_refresh_payload(bad, chunk)
		if refreshed is not None:
			print(f"FAIL refresh_payload_rejects_bad_existing: bad input accepted: {bad}")
			return False
	print("PASS refresh_payload_rejects_bad_existing: missing/invalid existing metadata refused")
	return True


def test_refresh_payload_does_not_mutate_inputs() -> bool:
	body = "stable body bytes"
	existing = make_existing_payload("docs/a.html", 0, body, router_version="1.1.6")
	chunk = make_router_chunk("docs/a.html", 0, body, router_version="1.1.8")
	import copy
	existing_snapshot = copy.deepcopy(existing)
	chunk_snapshot = copy.deepcopy(chunk)

	loader.build_router_metadata_refresh_payload(existing, chunk)

	if existing != existing_snapshot:
		print("FAIL refresh_payload_no_mutation: existing payload mutated in place")
		return False
	if chunk != chunk_snapshot:
		print("FAIL refresh_payload_no_mutation: chunk dict mutated in place")
		return False
	print("PASS refresh_payload_no_mutation: inputs unchanged")
	return True


def test_validate_router_mcp_bindings_accepts_known_descriptors() -> bool:
	with tempfile.TemporaryDirectory() as td:
		root = Path(td)
		(root / "user-directive-mcp-search" / "tools").mkdir(parents=True)
		(root / "user-typedb-snapshot-mcp" / "tools").mkdir(parents=True)
		(root / "user-directive-mcp-search" / "tools" / "qdrant-find.json").write_text("{}", encoding="utf-8")
		(root / "user-typedb-snapshot-mcp" / "tools" / "search_files.json").write_text("{}", encoding="utf-8")
		(root / "user-typedb-snapshot-mcp" / "tools" / "read_text_file.json").write_text("{}", encoding="utf-8")

		router = {
			"typedb_directive_search_binding": {
				"descriptor_folder_hint": "user-directive-mcp-search",
				"expected_tools_lexicographic": ["qdrant-find"],
			},
			"typedb_snapshot_mcp_binding": {
				"descriptor_folder_hint": "user-typedb-snapshot-mcp",
				"expected_tools_lexicographic": ["read_text_file", "search_files"],
			},
			"rows": [
				{"mandatory_sequence": [
					{"kind": "MCP", "registration": "user-directive-mcp-search", "tool": "qdrant-find"},
					{"kind": "MCP", "registration": "user-typedb-snapshot-mcp", "tool": "search_files"},
				]}
			],
		}

		errors = loader.validate_router_mcp_bindings(router, root)
		if errors:
			print(f"FAIL validate_router_mcp_known: expected no errors, got {errors}")
			return False
	print("PASS validate_router_mcp_known: known descriptor folders/tools accepted")
	return True


def test_validate_router_mcp_bindings_rejects_unknown_registration() -> bool:
	with tempfile.TemporaryDirectory() as td:
		root = Path(td)
		(root / "user-directive-mcp-search" / "tools").mkdir(parents=True)
		(root / "user-directive-mcp-search" / "tools" / "qdrant-find.json").write_text("{}", encoding="utf-8")

		router = {
			"typedb_directive_search_binding": {
				"descriptor_folder_hint": "user-directive-mcp-search",
				"expected_tools_lexicographic": ["qdrant-find"],
			},
			"rows": [
				{"mandatory_sequence": [
					{"kind": "MCP", "registration": "unknown-mcp", "tool": "qdrant-find"},
				]}
			],
		}

		errors = loader.validate_router_mcp_bindings(router, root)
		if not any("unknown MCP registration" in e for e in errors):
			print(f"FAIL validate_router_mcp_unknown: expected unknown registration error, got {errors}")
			return False
	print("PASS validate_router_mcp_unknown: unknown row registration rejected")
	return True


def test_bootstrap_registry_paths_resolve_with_stable_source_prefix() -> bool:
	with tempfile.TemporaryDirectory() as td:
		tmp = Path(td)
		snapshot_root = tmp / "typedb"
		bootstrap_root = tmp / "bootstrap-yamls"
		(snapshot_root / "_snapshot").mkdir(parents=True)
		bootstrap_root.mkdir(parents=True)
		(snapshot_root / "_snapshot" / "iam.schema.typeql").write_text(
			"define entity person;",
			encoding="utf-8",
		)
		(bootstrap_root / BOOTSTRAP_HANDOFF_FILE).write_text(
			"probe_b_search_terms: []",
			encoding="utf-8",
		)

		reg = {
			"ontology_skill_snapshot_corpus_literals_utf8_lexicographic": [
				"_snapshot/iam.schema.typeql",
			],
			"ontology_skill_bootstrap_corpus_root": str(bootstrap_root),
			"ontology_skill_bootstrap_corpus_source_prefix": "bootstrap_yamls",
			"ontology_skill_bootstrap_corpus_literals_utf8_lexicographic": [
				BOOTSTRAP_HANDOFF_FILE,
			],
		}

		sources = loader.collect_ontology_skill_registry_sources(snapshot_root, reg)
		source_files = [s["source_file"] for s in sources]
		if source_files != [
			"_snapshot/iam.schema.typeql",
			BOOTSTRAP_HANDOFF_SOURCE,
		]:
			print(f"FAIL bootstrap_registry_sources: unexpected source files {source_files}")
			return False
		if any(str(tmp).replace("\\", "/") in sf for sf in source_files):
			print("FAIL bootstrap_registry_sources: source_file leaked absolute temp path")
			return False
	print("PASS bootstrap_registry_sources: stable source prefix")
	return True


def test_build_chunks_includes_bootstrap_corpus() -> bool:
	with tempfile.TemporaryDirectory() as td:
		tmp = Path(td)
		snapshot_root = tmp / "typedb"
		bootstrap_root = tmp / "bootstrap-yamls"
		(snapshot_root / "_snapshot").mkdir(parents=True)
		bootstrap_root.mkdir(parents=True)
		(snapshot_root / "_snapshot" / "iam.schema.typeql").write_text(
			"define entity person;",
			encoding="utf-8",
		)
		(bootstrap_root / BOOTSTRAP_HANDOFF_FILE).write_text(
			"F-INT-4: Probe B fields obligated by workflow\n"
			"probe_b_search_terms\n"
			"probe_b_matched_paths\n"
			"probe_b_read_paths\n"
			"probe_b_failure_reason\n",
			encoding="utf-8",
		)

		router = {
			"skill_id": "ontology-tutor",
			"router_version": "1.1.11",
			"vector_source_file_registry": {
				"ontology_skill_snapshot_corpus_literals_utf8_lexicographic": [
					"_snapshot/iam.schema.typeql",
				],
				"ontology_skill_bootstrap_corpus_root": str(bootstrap_root),
				"ontology_skill_bootstrap_corpus_source_prefix": "bootstrap_yamls",
				"ontology_skill_bootstrap_corpus_literals_utf8_lexicographic": [
					BOOTSTRAP_HANDOFF_FILE,
				],
			},
			"rows": [
				{"routing_id": "R-G010_GENERAL"},
				{"routing_id": "R-T010_TRACE"},
			],
		}

		chunks = loader.build_ontology_skill_registry_chunks(snapshot_root, router)
		bootstrap_chunks = [
			c for c in chunks
			if c["source_file"] == BOOTSTRAP_HANDOFF_SOURCE
		]
		if not bootstrap_chunks:
			print("FAIL bootstrap_chunks: bootstrap source produced no chunks")
			return False
		if "F-INT-4" not in bootstrap_chunks[0]["body_text"]:
			print("FAIL bootstrap_chunks: expected audit handoff content absent")
			return False
		extra = bootstrap_chunks[0].get("ontology_router_extra") or {}
		if extra.get("typedb_authority_plane") != "bootstrap_memory":
			print(f"FAIL bootstrap_chunks: expected bootstrap_memory plane, got {extra}")
			return False
	print("PASS bootstrap_chunks: bootstrap corpus chunked with metadata")
	return True


def main() -> int:
	print("=" * 70)
	print("Tests: load_typedb_snapshot_search.py incremental hash dedup + caps")
	print("=" * 70)
	print()

	tests = [
		test_hash_determinism,
		test_hash_byte_sensitivity,
		test_uuid_determinism,
		test_partition_empty_existing,
		test_partition_all_unchanged,
		test_partition_changed_hash,
		test_partition_legacy_short_hash_routes_to_changed,
		test_partition_orphan,
		test_partition_mixed_all_four_buckets,
		test_partition_empty_candidates_all_orphan,
		test_uuid_round_trip_with_orphan_keys,
		test_apply_chunk_cap_per_file_no_cap,
		test_apply_chunk_cap_per_file_under_cap,
		test_apply_chunk_cap_per_file_truncates,
		test_apply_chunk_cap_total_no_cap,
		test_apply_chunk_cap_total_truncates,
		test_partition_banner_change_does_not_reroute,
		test_partition_body_change_routes_to_changed,
		test_partition_does_not_mutate_inputs,
		test_refresh_payload_preserves_content_hash_and_keys,
		test_refresh_payload_replaces_document_banner,
		test_refresh_payload_rejects_hash_mismatch,
		test_refresh_payload_rejects_missing_existing_metadata,
		test_refresh_payload_does_not_mutate_inputs,
		test_validate_router_mcp_bindings_accepts_known_descriptors,
		test_validate_router_mcp_bindings_rejects_unknown_registration,
		test_bootstrap_registry_paths_resolve_with_stable_source_prefix,
		test_build_chunks_includes_bootstrap_corpus,
	]

	results = []
	for t in tests:
		try:
			results.append(t())
		except Exception as exc:
			print(f"FAIL {t.__name__}: raised {type(exc).__name__}: {exc}")
			results.append(False)

	print()
	print("=" * 70)
	passed = sum(results)
	total = len(results)
	if passed == total:
		print(f"ALL {total} TESTS PASSED")
		return 0
	print(f"{passed}/{total} passed; {total - passed} FAILED")
	return 1


if __name__ == "__main__":
	sys.exit(main())
