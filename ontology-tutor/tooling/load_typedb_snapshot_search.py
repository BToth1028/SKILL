#!/usr/bin/env python3
"""
load_typedb_snapshot_search.py — Chunk, embed, and upsert the ontology-tutor
ROUTER corpus into Qdrant collection `directive-mcp-search` (Cursor MCP
descriptor: user-directive-mcp-search).

ROUTER IS CANON. **`--ontology-router PATH`** is REQUIRED. The loader reads
ROUTER's **`vector_source_file_registry`** (snapshot-relative literals + globs)
and embeds **only** those paths under **`--root`** with ontology-tutor banners.
There are no other ingest scopes — full-tree rglob, manifest-only, custom
include/exclude flows have all been removed. If you need a different corpus
shape, edit ROUTER's registry and rerun.

**Default ingest mode:** **incremental hash dedup**. Each chunk's full SHA-256 over the
**raw post-chunk file body** (pre-banner) is stored as `metadata.content_hash`.
On every run the loader scrolls the existing collection, partitions candidate chunks into
`new` / `changed` / `unchanged` / `orphans` keyed by `(source_file, chunk_index)` + `content_hash`,
then **only embeds and upserts new+changed**, **deletes orphans** (keys present in collection but
absent from candidates), and **leaves unchanged points untouched**. The hash basis intentionally
EXCLUDES the loader-stamped banner (skill_id, router_version, routing_ids, lineage_source,
typedb version stamps), so governance edits to ROUTER metadata that don't change the
underlying snapshot bytes do NOT trigger a re-embed.

**Router metadata refresh (no rebuild required):** If you only need to refresh
ROUTER-derived payload fields (e.g. after a `router_version` bump or a routing-id rename
that does NOT change snapshot bytes), pass **`--refresh-router-metadata`**. The loader
verifies file/chunk/`content_hash` parity against Qdrant first; for every parity-matching
point it overwrites `metadata.{skill_id, router_version, routing_id,
routing_ids_utf8_lexicographic, lineage_source, typedb_authority_plane}` and the stored
`document` banner in place. No vectors are recomputed and no points are dropped. If parity
is broken (file/chunk drift, hash drift), the refresh aborts with a non-zero exit so the
caller falls back to a normal incremental ingest or `--rebuild` instead of silently masking
real source drift. **`--rebuild`** remains the right tool when you actually want to drop and
recreate the collection (e.g. embedding model change or schema reset).

**Optional chunk caps (default uncapped):** **`--max-chunks-per-file N`** keeps the first N chunks per file.
**`--max-total-chunks N`** keeps the first N chunks across all files. Both default to `0` (uncapped). When triggered
they print `CHUNK-CAP-TRUNCATE` / `CHUNK-CAP-TOTAL` on stderr — silent data loss is a hard no.

**Chunking progress (default visible):** **`--chunk-file-progress-every N`** prints a one-line
progress message every N files processed during the chunking phase (default 25). Pass `0` to silence.

Mirrors corpus/loader/load_dictionary.py conventions:
  - FastEmbed with nomic-ai/nomic-embed-text-v1.5
  - Named vector fast-nomic-embed-text-v1.5 (compatible with mcp-server-qdrant)
  - Cosine distance
  - Idempotent: deterministic point UUID v5 keyed on (collection, source_file, chunk_index)
  - After token/heading chunking, each piece is clamped to a UTF-8 byte ceiling (Vector-style safe splits)
    so embed payloads stay bounded without splitting multibyte code units.

Source root: set env var TYPEDB_SNAPSHOT_ROOT (or pass --root) to the TypeDB
snapshot capture root (manifest.yaml, _snapshot/*.typeql, …). No default path is
baked in, so this tool carries no machine-specific location.

Python 3.11+. Install deps for this script only:

	pip install -r requirements-directive-mcp-search.txt

Windows entry point (cwd + propagate errorlevel):

	load_typedb_snapshot_search.bat [same args]

Run (from this tooling dir, the ontology-tutor skill bundle under 43.01-custom-skills):

	python load_typedb_snapshot_search.py \\
	  --ontology-router C:/Users/rtoth/.cursor/skills-cursor/ontology-tutor/ROUTER.yaml
	python load_typedb_snapshot_search.py \\
	  --ontology-router C:/Users/rtoth/.cursor/skills-cursor/ontology-tutor/ROUTER.yaml \\
	  --dry-run
	python load_typedb_snapshot_search.py \\
	  --ontology-router C:/Users/rtoth/.cursor/skills-cursor/ontology-tutor/ROUTER.yaml \\
	  --rebuild
	python load_typedb_snapshot_search.py \\
	  --ontology-router .../ROUTER.yaml --verify-router-qdrant
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Iterable

try:
	import yaml
except ImportError:
	yaml = None  # type: ignore[misc,assignment]

from bs4 import BeautifulSoup  # type: ignore[import-not-found]
from fastembed import TextEmbedding  # type: ignore[import-not-found]
from qdrant_client import QdrantClient  # type: ignore[import-not-found]
from qdrant_client.models import Distance, PayloadSchemaType, PointIdsList, PointStruct, VectorParams  # type: ignore[import-not-found]


_ENV_SNAPSHOT_ROOT = os.environ.get("TYPEDB_SNAPSHOT_ROOT", "").strip()

DEFAULTS = {
	# No baked-in path (C:\dev external-path gate): the snapshot capture root is
	# resolved from the TYPEDB_SNAPSHOT_ROOT env var or the --root flag at runtime.
	"root": Path(_ENV_SNAPSHOT_ROOT) if _ENV_SNAPSHOT_ROOT else None,
	"qdrant_url": "http://127.0.0.1:6334",
	"collection": "directive-mcp-search",
	"embedding_model": "nomic-ai/nomic-embed-text-v1.5",
}

EMBED_EXTS = {
	".adoc", ".md", ".txt", ".html",
	".tql", ".tqls", ".typeql",
	".kt", ".py", ".sh",
	".yml", ".yaml",
	".json",
	".csv",
}

EXCLUDE_NAMES = {
	"LICENSE", ".gitignore", ".bazelrc", ".bazelversion",
	"WORKSPACE", "BUILD",
}

EXCLUDE_DIR_NAMES = {".git", ".factory", "dependencies", "_meta", "__pycache__"}

CSV_MAX_BYTES = 50_000
DEFAULT_MAX_BYTES = 1_500_000

MAX_CHUNK_TOKENS_APPROX = 450
MAX_CHUNK_UTF8_BYTES = 8000
HEADING_RE = re.compile(r"^(=+|#+)\s+")

CODE_EXTS = {".tql", ".tqls", ".typeql", ".kt", ".py", ".sh", ".yml", ".yaml", ".json", ".csv"}
PROSE_EXTS = {".adoc", ".md", ".txt", ".html"}


def strip_yaml_front_matter(raw: str) -> tuple[str | None, str]:
	if not raw.lstrip("\ufeff").startswith("---"):
		return None, raw
	s = raw.lstrip("\ufeff")
	parts = s.split("---", 2)
	if len(parts) < 3:
		return None, raw
	return parts[1].strip(), parts[2].lstrip("\n")


def load_router_yaml(path: Path) -> dict[str, Any]:
	if yaml is None:
		print("ERROR: pip install PyYAML", file=sys.stderr)
		sys.exit(2)
	doc = yaml.safe_load(path.read_text(encoding="utf-8"))
	if not isinstance(doc, dict):
		raise ValueError(f"ROUTER YAML root must be a mapping: {path}")
	return doc


def collect_all_row_routing_ids_utf8_lexicographic(data: dict[str, Any]) -> list[str]:
	out: list[str] = []
	for row in data.get("rows", []) or []:
		if not isinstance(row, dict):
			continue
		rid = row.get("routing_id")
		if isinstance(rid, str) and rid.strip():
			out.append(rid.strip())
	return sorted(out)


def expand_ontology_skill_snapshot_paths(root: Path, reg: dict[str, Any]) -> set[str]:
	paths: set[str] = set()
	lits = reg.get("ontology_skill_snapshot_corpus_literals_utf8_lexicographic")
	if isinstance(lits, list):
		for x in lits:
			if isinstance(x, str) and x.strip():
				paths.add(x.strip().replace("\\", "/"))
	globs = reg.get("ontology_skill_snapshot_corpus_globs_utf8_lexicographic")
	if isinstance(globs, list):
		for raw_pat in globs:
			if not isinstance(raw_pat, str) or not raw_pat.strip():
				continue
			pat_n = raw_pat.strip().replace("\\", "/")
			added_paths = expand_safe_glob_files_under_root(root, pat_n)
			if not added_paths:
				print(f"       REGISTRY-GLOB-ZERO_MATCHES pattern={pat_n!r} under root", file=sys.stderr)
			paths |= added_paths
	return paths


def expand_safe_glob_files_under_root(root: Path, raw_pat: str) -> set[str]:
	paths: set[str] = set()
	pat_n = raw_pat.strip().replace("\\", "/")
	if not pat_n:
		return paths
	if ".." in pat_n or pat_n.startswith("/"):
		print(f"       GLOB-SKIP unsafe pattern: {pat_n}", file=sys.stderr)
		return paths
	for fp in sorted(root.glob(pat_n)):
		if fp.is_file():
			paths.add(str(fp.relative_to(root)).replace("\\", "/"))
	return paths


def normalized_relative_path(raw: str) -> str | None:
	rel = raw.strip().replace("\\", "/")
	if (
		not rel
		or ".." in rel
		or rel.startswith("/")
		or re.match(r"^[A-Za-z]:", rel)
	):
		return None
	return rel


def collect_ontology_skill_registry_sources(
	snapshot_root: Path,
	reg: dict[str, Any],
) -> list[dict[str, Any]]:
	sources: dict[str, dict[str, Any]] = {}
	for rel in expand_ontology_skill_snapshot_paths(snapshot_root, reg):
		fp = snapshot_root.joinpath(*rel.split("/"))
		sources[rel] = {
			"path": fp,
			"root": snapshot_root,
			"source_file": rel,
			"typedb_authority_plane": "offline_snapshot",
		}

	bootstrap_root_raw = reg.get("ontology_skill_bootstrap_corpus_root")
	if isinstance(bootstrap_root_raw, str) and bootstrap_root_raw.strip():
		bootstrap_root = Path(bootstrap_root_raw.strip())
		prefix_raw = reg.get("ontology_skill_bootstrap_corpus_source_prefix")
		prefix = "bootstrap_yamls"
		if isinstance(prefix_raw, str) and prefix_raw.strip():
			prefix = prefix_raw.strip().replace("\\", "/").strip("/")
		literals = reg.get(
			"ontology_skill_bootstrap_corpus_literals_utf8_lexicographic"
		)
		if isinstance(literals, list):
			for item in literals:
				if not isinstance(item, str):
					continue
				rel = normalized_relative_path(item)
				if rel is None:
					print(
						f"       REGISTRY-BOOTSTRAP-SKIP unsafe literal: {item!r}",
						file=sys.stderr,
					)
					continue
				source_file = f"{prefix}/{rel}"
				sources[source_file] = {
					"path": bootstrap_root.joinpath(*rel.split("/")),
					"root": bootstrap_root,
					"source_file": source_file,
					"typedb_authority_plane": "bootstrap_memory",
				}
		globs = reg.get(
			"ontology_skill_bootstrap_corpus_globs_utf8_lexicographic"
		)
		if isinstance(globs, list):
			for item in globs:
				if not isinstance(item, str):
					continue
				pat = normalized_relative_path(item)
				if pat is None:
					print(
						f"       REGISTRY-BOOTSTRAP-SKIP unsafe glob: {item!r}",
						file=sys.stderr,
					)
					continue
				matched = False
				for fp in sorted(bootstrap_root.glob(pat)):
					if not fp.is_file():
						continue
					rel = str(fp.relative_to(bootstrap_root)).replace("\\", "/")
					source_file = f"{prefix}/{rel}"
					sources[source_file] = {
						"path": fp,
						"root": bootstrap_root,
						"source_file": source_file,
						"typedb_authority_plane": "bootstrap_memory",
					}
					matched = True
				if not matched:
					print(
						"       REGISTRY-BOOTSTRAP-GLOB-ZERO_MATCHES "
						f"pattern={pat!r}",
						file=sys.stderr,
					)

	return [sources[key] for key in sorted(sources)]


def verify_registry_for_ontology_ingest(
	snapshot_root: Path,
	router_data: dict[str, Any],
) -> None:
	reg = router_data.get("vector_source_file_registry")
	if not isinstance(reg, dict):
		return
	literals = reg.get("ontology_skill_snapshot_corpus_literals_utf8_lexicographic")
	if literals is None:
		print(
			"       REGISTRY-WARN missing ontology_skill_snapshot_corpus_literals_utf8_lexicographic",
			file=sys.stderr,
		)
		return
	if not isinstance(literals, list):
		return
	for x in literals:
		if not isinstance(x, str) or not x.strip():
			continue
		rel = x.strip().replace("\\", "/")
		fp = snapshot_root.joinpath(*rel.split("/"))
		if not fp.is_file():
			print(f"       REGISTRY-FAIL missing literal ontology corpus path on disk: {rel}", file=sys.stderr)
			sys.exit(2)
	raw_snap = reg.get("typedb_capture_snapshot_probe_b_utf8_lexicographic")
	if isinstance(raw_snap, list) and snapshot_root.is_dir():
		for item in raw_snap:
			if not isinstance(item, str):
				continue
			rel = item.strip().replace("\\", "/")
			fp = snapshot_root.joinpath(*rel.split("/"))
			if not fp.is_file():
				print(
					f"       REGISTRY-SNAPSHOT-MISS disk (typedb_capture_snapshot_probe_b): {rel}",
					file=sys.stderr,
				)
	bootstrap_root_raw = reg.get("ontology_skill_bootstrap_corpus_root")
	if isinstance(bootstrap_root_raw, str) and bootstrap_root_raw.strip():
		bootstrap_root = Path(bootstrap_root_raw.strip())
		literals_bootstrap = reg.get(
			"ontology_skill_bootstrap_corpus_literals_utf8_lexicographic"
		)
		if isinstance(literals_bootstrap, list):
			for item in literals_bootstrap:
				if not isinstance(item, str):
					continue
				rel = normalized_relative_path(item)
				if rel is None:
					print(
						f"       REGISTRY-FAIL unsafe bootstrap corpus path: {item!r}",
						file=sys.stderr,
					)
					sys.exit(2)
				fp = bootstrap_root.joinpath(*rel.split("/"))
				if not fp.is_file():
					print(
						"       REGISTRY-FAIL missing literal bootstrap corpus "
						f"path on disk: {rel}",
						file=sys.stderr,
					)
					sys.exit(2)


def validate_router_mcp_bindings(router_data: dict[str, Any], descriptor_root: Path) -> list[str]:
	errors: list[str] = []
	registration_to_tools: dict[str, set[str]] = {}

	for key, value in router_data.items():
		if not (isinstance(key, str) and key.endswith("_binding") and isinstance(value, dict)):
			continue
		descriptor_name = value.get("descriptor_folder_hint")
		if not isinstance(descriptor_name, str) or not descriptor_name.strip():
			continue
		descriptor_name = descriptor_name.strip()
		descriptor_dir = descriptor_root / descriptor_name
		tools_dir = descriptor_dir / "tools"
		if not descriptor_dir.is_dir():
			errors.append(f"{key}: descriptor folder missing: {descriptor_name}")
			continue
		if not tools_dir.is_dir():
			errors.append(f"{key}: tools folder missing for descriptor: {descriptor_name}")
			continue

		available_tools = {p.stem for p in tools_dir.glob("*.json") if p.is_file()}
		expected_tools = value.get("expected_tools_lexicographic")
		if isinstance(expected_tools, list):
			for tool in expected_tools:
				if isinstance(tool, str) and tool.strip() and tool.strip() not in available_tools:
					errors.append(f"{key}: expected tool missing: {descriptor_name}/tools/{tool.strip()}.json")

		registration_to_tools[descriptor_name] = available_tools
		cursor_server_name = value.get("cursor_server_name")
		if isinstance(cursor_server_name, str) and cursor_server_name.strip():
			registration_to_tools[cursor_server_name.strip()] = available_tools

	for row in router_data.get("rows", []) or []:
		if not isinstance(row, dict):
			continue
		routing_id = row.get("routing_id", "<unknown-routing-id>")
		for step in row.get("mandatory_sequence", []) or []:
			if not isinstance(step, dict) or step.get("kind") != "MCP":
				continue
			registration = step.get("registration")
			tool = step.get("tool")
			if not isinstance(registration, str) or not registration.strip():
				errors.append(f"{routing_id}: MCP step missing registration")
				continue
			registration = registration.strip()
			if registration not in registration_to_tools:
				errors.append(f"{routing_id}: unknown MCP registration: {registration}")
				continue
			if not isinstance(tool, str) or not tool.strip():
				errors.append(f"{routing_id}: MCP step missing tool for registration {registration}")
				continue
			tool = tool.strip()
			if tool not in registration_to_tools[registration]:
				errors.append(f"{routing_id}: unknown MCP tool for {registration}: {tool}")

	return errors


def ontology_tutor_registry_heading(rel_lineage: str, skill_id: str, rv: str, primary_rid: str, rids: list[str]) -> str:
	rs = ",".join(rids)
	return (
		"[ONTOLOGY-TUTOR SNAPSHOT_REGISTRY_VECTOR]\n"
		f"[skill_id: {skill_id} router_version: {rv} routing_id_primary: {primary_rid} "
		f"routing_ids_utf8_lexicographic: {rs} lineage_source: {rel_lineage}]\n\n"
	)


def build_ontology_skill_registry_chunks(
	snapshot_root: Path,
	router_data: dict[str, Any],
	max_chunks_per_file: int = 0,
	progress_every: int = 0,
	report_caps: bool = False,
) -> list[dict[str, Any]]:
	reg = router_data.get("vector_source_file_registry")
	if not isinstance(reg, dict):
		return []
	skid = router_data.get("skill_id")
	rv = router_data.get("router_version")
	if not isinstance(skid, str) or not isinstance(rv, str):
		raise ValueError("ROUTER must set skill_id and router_version strings")
	routing_ids_sorted = collect_all_row_routing_ids_utf8_lexicographic(router_data)
	if not routing_ids_sorted:
		raise ValueError("ROUTER rows must expose routing_id for ontology skill ingest")
	primary_rid = routing_ids_sorted[0]
	sources = collect_ontology_skill_registry_sources(snapshot_root, reg)
	total_files = len(sources)
	out: list[dict[str, Any]] = []
	files_processed = 0
	t_chunk_start = time.time()
	for source in sources:
		files_processed += 1
		fp = source["path"]
		source_root = source["root"]
		source_file = source["source_file"]
		authority_plane = source["typedb_authority_plane"]
		if not fp.is_file():
			print(f"       ONTOLOGY-REGISTRY-SKIP missing file: {source_file}")
			continue
		ok, reason = should_embed(fp, source_root)
		if not ok:
			print(f"       ONTOLOGY-REGISTRY-SKIP {source_file} ({reason})")
			continue
		try:
			raw = read_text(fp)
		except OSError as exc:
			print(f"       READ-FAIL {source_file}: {exc}")
			continue
		_fm, body = strip_yaml_front_matter(raw)
		text_body = body if _fm else raw
		chunks_txt = apply_chunk_cap_per_file(
			chunk_text(text_body),
			max_chunks_per_file,
			source_file,
			report=report_caps,
		)
		if not chunks_txt:
			continue
		lineage_src = source_file.replace("\\", "/")
		banner0 = ontology_tutor_registry_heading(lineage_src, skid, rv, primary_rid, routing_ids_sorted)
		cls = classify(source_file)
		extra_router = {
			"skill_id": skid,
			"router_version": rv,
			"routing_id": primary_rid,
			"routing_ids_utf8_lexicographic": routing_ids_sorted,
			"lineage_source": lineage_src,
			"typedb_authority_plane": authority_plane,
		}
		for i, c in enumerate(chunks_txt):
			out.append({
				"text": banner0 + version_banner(cls, source_file) + c,
				"body_text": c,
				"source_file": lineage_src,
				"chunk_index": i,
				"chunk_count": len(chunks_txt),
				"file_size": fp.stat().st_size,
				"typedb_version": cls["typedb_version"],
				"content_type": cls["content_type"],
				"syntax_safe_for_3x": cls["syntax_safe_for_3x"],
				"ontology_router_extra": extra_router,
			})
		if progress_every > 0 and (files_processed % progress_every == 0 or files_processed == total_files):
			elapsed = max(time.time() - t_chunk_start, 1e-9)
			print(
				f"       chunking progress: {files_processed}/{total_files} files, "
				f"{len(out)} chunks (~{files_processed / elapsed:.1f} files/s, {elapsed:.1f}s elapsed)",
				flush=True,
			)
	return out

def rel_posix_under_root(path: Path, root: Path) -> str:
	return str(path.relative_to(root)).replace("\\", "/")


def classify(rel_path: str) -> dict:
	"""Path-based classification: TypeDB version, content type, syntax safety."""
	p = rel_path.replace("\\", "/")
	pl = p.lower()

	if pl.startswith("ontology-tutor/"):
		return {
			"typedb_version": "version-agnostic",
			"content_type": "prose",
			"syntax_safe_for_3x": True,
		}

	ext = "." + pl.rsplit(".", 1)[-1] if "." in pl else ""

	if pl == "manifest.yaml" or pl.endswith("/manifest.yaml"):
		ver = "version-agnostic"
	elif "_snapshot/" in pl or pl.startswith("_snapshot/"):
		if ext in (".tql", ".tqls", ".typeql"):
			ver = "3.x"
		else:
			ver = "unknown"
	else:
		ver = "unknown"

	content_type = "code" if ext in CODE_EXTS else ("prose" if ext in PROSE_EXTS else "other")
	syntax_safe_for_3x = (ver == "3.x") or (content_type != "code")
	return {
		"typedb_version": ver,
		"content_type": content_type,
		"syntax_safe_for_3x": syntax_safe_for_3x,
	}


def version_banner(cls: dict, source_file: str) -> str:
	v = cls["typedb_version"]
	ct = cls["content_type"]
	if v == "3.x":
		tag = "[TYPEDB 3.x — current; TypeQL is safe to use]"
	elif v == "2.x" and ct == "code":
		tag = "[TYPEDB 2.x — ARCHIVED; DO NOT paste this TypeQL into a 3.x schema. Read for concept only.]"
	elif v == "2.x":
		tag = "[TYPEDB 2.x — ARCHIVED prose; concepts canonical, but any TypeQL shown will NOT run on 3.x without rewrite.]"
	elif v == "version-agnostic":
		tag = "[VERSION-AGNOSTIC — no TypeQL]"
	else:
		tag = "[VERSION UNKNOWN]"
	return f"{tag}\n[source: {source_file}]\n"


def mcp_vector_name(model: str) -> str:
	slug = model.split("/")[-1].lower()
	return f"fast-{slug}"


def compute_chunk_hash(text: str) -> str:
	"""Full 64-hex SHA-256 of the supplied bytes.

	Pure utility. Determinism is in the bytes you pass in. In this loader
	the basis is **the raw post-chunk file body (pre-banner)**, supplied via
	`chunk["body_text"]`. The loader-stamped banner (skill_id, router_version,
	routing_ids, lineage, typedb version stamp) is intentionally NOT part of
	the hash basis — governance edits to ROUTER metadata that don't change
	snapshot bytes must not invalidate the cache. To refresh banners or
	ROUTER-derived payload metadata without re-embedding, run with
	`--refresh-router-metadata` (no rebuild needed); use `--rebuild` only
	when you actually want to drop and recreate the collection.
	"""
	return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_point_uuid(collection: str, source_file: str, chunk_index: int) -> str:
	"""Deterministic UUID v5 keyed on (collection, source_file, chunk_index).

	Same key → same UUID across runs, so re-upserts overwrite cleanly and
	orphan deletion can recompute the exact point ID without scrolling.
	"""
	return str(uuid.uuid5(
		uuid.NAMESPACE_URL,
		f"{collection}/{source_file}/{chunk_index}",
	))


ROUTER_METADATA_REFRESH_FIELDS: tuple[str, ...] = (
	"skill_id",
	"router_version",
	"routing_id",
	"routing_ids_utf8_lexicographic",
	"lineage_source",
	"typedb_authority_plane",
)


def build_router_metadata_refresh_payload(
	existing_payload: Any,
	chunk: dict[str, Any],
) -> dict[str, Any] | None:
	"""Build a Qdrant payload that refreshes ROUTER-derived metadata in place.

	Pure function. Returns a new payload dict that:
	  - keeps existing identity + source-derived metadata (`source_file`,
	    `chunk_index`, `chunk_count`, `file_size`, `content_hash`,
	    `typedb_version`, `content_type`, `syntax_safe_for_3x`),
	  - replaces ROUTER-derived metadata fields listed in
	    `ROUTER_METADATA_REFRESH_FIELDS` from the chunk's `ontology_router_extra`,
	  - replaces top-level `document` with the chunk's banner-stamped `text`,
	  - recomputes `metadata.approx_tokens` for the new document text.

	Returns None when refresh is unsafe:
	  - existing payload is missing or malformed,
	  - existing metadata lacks `content_hash`,
	  - existing `content_hash` does not equal `compute_chunk_hash(chunk["body_text"])`
	    (means the underlying source bytes have actually drifted; a metadata-only
	    refresh would mask that and is rejected).
	"""
	if not isinstance(existing_payload, dict):
		return None
	existing_meta = existing_payload.get("metadata")
	if not isinstance(existing_meta, dict):
		return None
	existing_hash = existing_meta.get("content_hash")
	if not isinstance(existing_hash, str) or not existing_hash.strip():
		return None
	body_text = chunk.get("body_text")
	if not isinstance(body_text, str):
		return None
	if existing_hash != compute_chunk_hash(body_text):
		return None
	extra = chunk.get("ontology_router_extra")
	if not isinstance(extra, dict):
		return None
	new_meta: dict[str, Any] = dict(existing_meta)
	for k in ROUTER_METADATA_REFRESH_FIELDS:
		if k in extra:
			v = extra[k]
			if isinstance(v, list):
				new_meta[k] = list(v)
			else:
				new_meta[k] = v
	new_doc = chunk.get("text")
	if not isinstance(new_doc, str):
		return None
	new_meta["approx_tokens"] = approx_tokens(new_doc)
	return {
		"document": new_doc,
		"metadata": new_meta,
	}


def partition_chunks_for_incremental(
	existing: dict[tuple[str, int], str],
	candidates: list[dict[str, Any]],
) -> dict[str, list[Any]]:
	"""Partition candidate chunks against existing Qdrant payload state.

	Pure function. No I/O. Identity key is (source_file, chunk_index);
	freshness check is full SHA-256 of the chunk's body_text (pre-banner
	source bytes). Banner changes (router_version bumps, stamp template
	tweaks) do NOT route a chunk to `changed` — that's the whole point.

	Returns a dict with four buckets:
	  new       — list[chunk_dict]: key absent in existing → must embed + upsert
	  changed   — list[chunk_dict]: key present, body hash differs → must embed + upsert
	  unchanged — list[chunk_dict]: key present, body hash matches → skip both
	  orphans   — list[(source_file, chunk_index)]: in existing but not in
	              candidates → must delete by recomputed point UUID
	"""
	out: dict[str, list[Any]] = {"new": [], "changed": [], "unchanged": [], "orphans": []}
	candidate_keys: set[tuple[str, int]] = set()
	for c in candidates:
		sf = c["source_file"]
		ci = c["chunk_index"]
		key = (sf, ci)
		candidate_keys.add(key)
		h = compute_chunk_hash(c["body_text"])
		prev = existing.get(key)
		if prev is None:
			out["new"].append(c)
		elif prev == h:
			out["unchanged"].append(c)
		else:
			out["changed"].append(c)
	for key in existing.keys():
		if key not in candidate_keys:
			out["orphans"].append(key)
	out["orphans"].sort()
	return out


def apply_chunk_cap_per_file(
	chunks: list[str],
	max_per_file: int,
	source_file: str,
	report: bool = False,
) -> list[str]:
	"""Truncate per-file chunk list to first N. cap=0 means uncapped."""
	if max_per_file <= 0 or len(chunks) <= max_per_file:
		return chunks
	if report:
		print(
			f"       CHUNK-CAP-TRUNCATE rel={source_file} kept={max_per_file}/{len(chunks)}",
			file=sys.stderr,
		)
	return chunks[:max_per_file]


def apply_chunk_cap_total(
	chunks: list[dict[str, Any]],
	max_total: int,
	report: bool = False,
) -> list[dict[str, Any]]:
	"""Truncate combined chunk list to first N total. cap=0 means uncapped."""
	if max_total <= 0 or len(chunks) <= max_total:
		return chunks
	if report:
		print(
			f"       CHUNK-CAP-TOTAL kept={max_total}/{len(chunks)}",
			file=sys.stderr,
		)
	return chunks[:max_total]


def approx_tokens(text: str) -> int:
	return len(text.split())


def utf8_byte_len(s: str) -> int:
	return len(s.encode("utf-8"))


def split_oversized_utf8(segment: str, max_bytes: int) -> list[str]:
	encoded = segment.encode("utf-8")
	out: list[str] = []
	start = 0
	while start < len(encoded):
		end = min(start + max_bytes, len(encoded))
		if end < len(encoded):
			while end > start and (encoded[end] & 0xC0) == 0x80:
				end -= 1
			if end == start:
				end = min(start + max_bytes, len(encoded))
		out.append(encoded[start:end].decode("utf-8", errors="replace"))
		start = end
	return out


def clamp_chunks_utf8_bytes(chunks: list[str], max_bytes: int) -> list[str]:
	result: list[str] = []
	for c in chunks:
		if utf8_byte_len(c) <= max_bytes:
			result.append(c)
		else:
			result.extend(split_oversized_utf8(c, max_bytes))
	return [c for c in result if c.strip()]


def embed_chunks_reporting(
	embedder: TextEmbedding,
	texts: list[str],
	batch_size: int,
	progress_every: int,
) -> list[Any]:
	bs = max(1, batch_size)
	total = len(texts)
	batch_count = (total + bs - 1) // bs
	out: list[Any] = []
	t0 = time.time()
	for start in range(0, total, bs):
		end = min(start + bs, total)
		batch_idx = start // bs + 1
		if start == 0:
			print(
				f"       {batch_count} embedding batch(es), size {bs}; entering batch {batch_idx} "
				f"(chunks {start + 1}-{end}/{total}). First batch is often the slowest.",
				flush=True,
			)
		batch = texts[start:end]
		part = list(embedder.embed(batch, batch_size=len(batch)))
		out.extend(part)
		done = len(out)
		if progress_every <= 0:
			continue
		if batch_idx == 1 or done % progress_every == 0 or done == total:
			elapsed = max(time.time() - t0, 1e-9)
			print(
				f"       embedding progress: {done}/{total} chunks (~{done / elapsed:.1f} chunks/s, {elapsed:.1f}s elapsed)",
				flush=True,
			)
	return out


def html_to_text(raw: str) -> str:
	soup = BeautifulSoup(raw, "html.parser")
	for bad in soup(["script", "style", "nav", "footer", "header", "noscript"]):
		bad.decompose()
	return soup.get_text("\n", strip=True)


def read_text(path: Path) -> str:
	raw = path.read_bytes()
	try:
		text = raw.decode("utf-8")
	except UnicodeDecodeError:
		text = raw.decode("utf-8", errors="replace")
	if path.suffix.lower() == ".html":
		return html_to_text(text)
	return text


def split_by_headings(text: str) -> list[str]:
	lines = text.splitlines()
	sections: list[list[str]] = [[]]
	for line in lines:
		if HEADING_RE.match(line) and sections[-1]:
			sections.append([line])
		else:
			sections[-1].append(line)
	return ["\n".join(s).strip() for s in sections if any(l.strip() for l in s)]


def hard_split(text: str, max_tokens: int) -> Iterable[str]:
	words = text.split()
	if not words:
		return
	for i in range(0, len(words), max_tokens):
		yield " ".join(words[i:i + max_tokens])


def chunk_text(text: str) -> list[str]:
	chunks: list[str] = []
	for section in split_by_headings(text):
		if approx_tokens(section) <= MAX_CHUNK_TOKENS_APPROX:
			chunks.append(section)
			continue
		paragraphs = re.split(r"\n\s*\n", section)
		buf = ""
		for para in paragraphs:
			if approx_tokens(buf) + approx_tokens(para) <= MAX_CHUNK_TOKENS_APPROX:
				buf = (buf + "\n\n" + para).strip() if buf else para
			else:
				if buf:
					chunks.append(buf)
				if approx_tokens(para) <= MAX_CHUNK_TOKENS_APPROX:
					buf = para
				else:
					for piece in hard_split(para, MAX_CHUNK_TOKENS_APPROX):
						chunks.append(piece)
					buf = ""
		if buf:
			chunks.append(buf)
	return clamp_chunks_utf8_bytes([c for c in chunks if c.strip()], MAX_CHUNK_UTF8_BYTES)


def should_embed(path: Path, root: Path) -> tuple[bool, str]:
	if any(part in EXCLUDE_DIR_NAMES for part in path.relative_to(root).parts):
		return False, "excluded dir"
	if path.name in EXCLUDE_NAMES:
		return False, "excluded name"
	if path.suffix.lower() not in EMBED_EXTS:
		return False, f"ext {path.suffix} not in allowlist"
	size = path.stat().st_size
	if path.suffix.lower() == ".csv" and size > CSV_MAX_BYTES:
		return False, f"csv > {CSV_MAX_BYTES}B"
	if size > DEFAULT_MAX_BYTES:
		return False, f"file > {DEFAULT_MAX_BYTES}B"
	if size == 0:
		return False, "empty"
	return True, "ok"


def payload_source_file(payload: dict[str, Any] | None) -> str | None:
	if not payload or not isinstance(payload, dict):
		return None
	meta = payload.get("metadata")
	if isinstance(meta, dict):
		sf = meta.get("source_file")
		if isinstance(sf, str) and sf.strip():
			return sf.strip().replace("\\", "/")
	sf = payload.get("source_file")
	if isinstance(sf, str) and sf.strip():
		return sf.strip().replace("\\", "/")
	return None


def verify_router_qdrant_file_parity(
	snapshot_root: Path,
	router_data: dict[str, Any],
	qdrant_url: str,
	collection: str,
	max_chunks_per_file: int = 0,
) -> int:
	print("[verify] Expected = distinct (source_file, chunk_index, content_hash) triples emitted by build_ontology_skill_registry_chunks (ROUTER literals + globs, same skips and per-file caps as ingest).")
	try:
		chunks = build_ontology_skill_registry_chunks(
			snapshot_root,
			router_data,
			max_chunks_per_file,
			report_caps=True,
		)
	except Exception as exc:
		print(f"[verify] FAILED building expected chunk set: {exc}", file=sys.stderr)
		return 2
	expected_files: set[str] = {str(c["source_file"]).replace("\\", "/") for c in chunks}
	expected_keys: set[tuple[str, int]] = set()
	expected_hash_by_key: dict[tuple[str, int], str] = {}
	for c in chunks:
		key = (str(c["source_file"]).replace("\\", "/"), int(c["chunk_index"]))
		expected_keys.add(key)
		expected_hash_by_key[key] = compute_chunk_hash(c["body_text"])
	print(f"[verify] Expected: {len(expected_files)} files, {len(expected_keys)} chunks")

	reg = router_data.get("vector_source_file_registry")
	if isinstance(reg, dict):
		reg_resolved = {s["source_file"] for s in collect_ontology_skill_registry_sources(snapshot_root, reg)}
		zero_chunk = reg_resolved - expected_files
		if zero_chunk:
			print(f"[verify] NOTE: {len(zero_chunk)} registry-resolved paths yield no ontology chunks (missing, should_embed skip, read fail, or empty body after chunk).")

	client = QdrantClient(url=qdrant_url, check_compatibility=False)
	try:
		info = client.get_collection(collection)
	except Exception as exc:
		print(f"[verify] Qdrant get_collection failed: {exc}", file=sys.stderr)
		return 2
	print(f"[verify] Qdrant collection points_count: {info.points_count}")

	actual_files: set[str] = set()
	actual_keys: set[tuple[str, int]] = set()
	actual_hash_by_key: dict[tuple[str, int], str] = {}
	bad_payload = 0
	offset: Any = None
	while True:
		records, next_offset = client.scroll(
			collection_name=collection,
			limit=512,
			offset=offset,
			with_payload=True,
			with_vectors=False,
		)
		for rec in records:
			payload = rec.payload if isinstance(rec.payload, dict) else None
			meta = payload.get("metadata") if isinstance(payload, dict) else None
			if not isinstance(meta, dict):
				bad_payload += 1
				continue
			sf = meta.get("source_file")
			ci = meta.get("chunk_index")
			ch = meta.get("content_hash")
			if not (isinstance(sf, str) and isinstance(ci, int) and isinstance(ch, str)):
				bad_payload += 1
				continue
			sf_n = sf.replace("\\", "/")
			actual_files.add(sf_n)
			actual_keys.add((sf_n, ci))
			actual_hash_by_key[(sf_n, ci)] = ch
		if next_offset is None:
			break
		offset = next_offset

	print(f"[verify] Qdrant distinct metadata.source_file: {len(actual_files)}; chunks: {len(actual_keys)}")
	if bad_payload:
		print(f"[verify] WARN: points without usable metadata.(source_file, chunk_index, content_hash): {bad_payload}")

	file_missing = expected_files - actual_files
	file_extra = actual_files - expected_files
	chunk_missing = expected_keys - actual_keys
	chunk_extra = actual_keys - expected_keys
	hash_drift = sorted(
		k for k in (expected_keys & actual_keys)
		if expected_hash_by_key[k] != actual_hash_by_key[k]
	)

	if not file_missing and not file_extra and not chunk_missing and not chunk_extra and not hash_drift:
		print("[verify] PASS: file set, chunk set, and chunk hashes all match (nothing more, nothing less).")
		return 0

	print("[verify] FAIL: parity broken.", file=sys.stderr)
	if file_missing:
		print(f"[verify] Files in expected but not in Qdrant ({len(file_missing)}):", file=sys.stderr)
		for p in sorted(file_missing)[:80]:
			print(f"         - {p}", file=sys.stderr)
		if len(file_missing) > 80:
			print(f"         ... {len(file_missing) - 80} more", file=sys.stderr)
	if file_extra:
		print(f"[verify] Files in Qdrant but not in expected ({len(file_extra)}):", file=sys.stderr)
		for p in sorted(file_extra)[:80]:
			print(f"         + {p}", file=sys.stderr)
		if len(file_extra) > 80:
			print(f"         ... {len(file_extra) - 80} more", file=sys.stderr)
	if chunk_missing:
		print(f"[verify] Chunks in expected but not in Qdrant ({len(chunk_missing)}):", file=sys.stderr)
		for k in sorted(chunk_missing)[:80]:
			print(f"         - {k[0]}#{k[1]}", file=sys.stderr)
		if len(chunk_missing) > 80:
			print(f"         ... {len(chunk_missing) - 80} more", file=sys.stderr)
	if chunk_extra:
		print(f"[verify] Chunks in Qdrant but not in expected ({len(chunk_extra)}):", file=sys.stderr)
		for k in sorted(chunk_extra)[:80]:
			print(f"         + {k[0]}#{k[1]}", file=sys.stderr)
		if len(chunk_extra) > 80:
			print(f"         ... {len(chunk_extra) - 80} more", file=sys.stderr)
	if hash_drift:
		print(f"[verify] HASH-DRIFT (chunk present both sides, content_hash differs) ({len(hash_drift)}):", file=sys.stderr)
		for k in hash_drift[:80]:
			exp = expected_hash_by_key[k][:12]
			act = actual_hash_by_key[k][:12]
			print(f"         ~ {k[0]}#{k[1]}  expected={exp}... actual={act}...", file=sys.stderr)
		if len(hash_drift) > 80:
			print(f"         ... {len(hash_drift) - 80} more", file=sys.stderr)
		print("[verify] HINT: HASH-DRIFT means existing payloads carry a different (or shorter/legacy) content_hash than the current ROUTER chunk would compute. Run a normal incremental ingest (no flag) to re-embed those keys, or `--rebuild` to fully recreate. `--refresh-router-metadata` will refuse hash-drifted points by design.", file=sys.stderr)
	return 1


def refresh_router_metadata_in_qdrant(
	snapshot_root: Path,
	router_data: dict[str, Any],
	qdrant_url: str,
	collection: str,
	max_chunks_per_file: int = 0,
	progress_every: int = 100,
) -> int:
	"""Refresh ROUTER-derived payload metadata + document banner in place.

	Performs a strict parity check (file set, chunk set, content_hash) before
	any mutation. If parity is broken (file/chunk/hash drift), aborts with
	a non-zero exit code and does not touch Qdrant — hash drift is real
	source drift and must be repaired by `incremental` ingest or `--rebuild`,
	not silently masked by a metadata refresh.

	On parity PASS, calls `client.set_payload` per point with the payload
	produced by `build_router_metadata_refresh_payload`. Vectors are not
	touched. Point IDs are not changed.

	Returns 0 on success, 1 on parity failure, 2 on infrastructure failure.
	"""
	print("[refresh] Building expected chunk set from current ROUTER...")
	try:
		chunks = build_ontology_skill_registry_chunks(
			snapshot_root,
			router_data,
			max_chunks_per_file,
			report_caps=True,
		)
	except Exception as exc:
		print(f"[refresh] FAILED building expected chunk set: {exc}", file=sys.stderr)
		return 2
	expected_by_key: dict[tuple[str, int], dict[str, Any]] = {}
	for c in chunks:
		key = (str(c["source_file"]).replace("\\", "/"), int(c["chunk_index"]))
		expected_by_key[key] = c
	print(f"[refresh] Expected chunks from ROUTER: {len(expected_by_key)}")

	client = QdrantClient(url=qdrant_url, check_compatibility=False)
	try:
		info = client.get_collection(collection)
	except Exception as exc:
		print(f"[refresh] Qdrant get_collection failed: {exc}", file=sys.stderr)
		return 2
	print(f"[refresh] Qdrant collection points_count: {info.points_count}")

	actual_payloads: dict[tuple[str, int], tuple[Any, dict[str, Any]]] = {}
	bad_payload_n = 0
	offset: Any = None
	while True:
		records, next_offset = client.scroll(
			collection_name=collection,
			limit=512,
			offset=offset,
			with_payload=True,
			with_vectors=False,
		)
		for rec in records:
			payload = rec.payload if isinstance(rec.payload, dict) else None
			meta = payload.get("metadata") if isinstance(payload, dict) else None
			if not isinstance(meta, dict):
				bad_payload_n += 1
				continue
			sf = meta.get("source_file")
			ci = meta.get("chunk_index")
			if not (isinstance(sf, str) and isinstance(ci, int)):
				bad_payload_n += 1
				continue
			key = (sf.replace("\\", "/"), ci)
			actual_payloads[key] = (rec.id, payload)
		if next_offset is None:
			break
		offset = next_offset

	if bad_payload_n:
		print(f"[refresh] WARN: {bad_payload_n} Qdrant points lacked usable metadata.(source_file, chunk_index); refusing refresh.", file=sys.stderr)
		return 1

	expected_keys = set(expected_by_key.keys())
	actual_keys = set(actual_payloads.keys())
	missing_in_qdrant = expected_keys - actual_keys
	extra_in_qdrant = actual_keys - expected_keys
	common_keys = expected_keys & actual_keys

	hash_drift_keys: list[tuple[str, int]] = []
	refresh_plan: list[tuple[Any, dict[str, Any]]] = []
	for key in sorted(common_keys):
		existing_id, existing_payload = actual_payloads[key]
		chunk = expected_by_key[key]
		new_payload = build_router_metadata_refresh_payload(existing_payload, chunk)
		if new_payload is None:
			hash_drift_keys.append(key)
			continue
		refresh_plan.append((existing_id, new_payload))

	if missing_in_qdrant or extra_in_qdrant or hash_drift_keys:
		print("[refresh] FAIL: parity broken; refusing metadata refresh.", file=sys.stderr)
		if missing_in_qdrant:
			print(f"[refresh]   missing in Qdrant ({len(missing_in_qdrant)}):", file=sys.stderr)
			for k in sorted(missing_in_qdrant)[:40]:
				print(f"           - {k[0]}#{k[1]}", file=sys.stderr)
			if len(missing_in_qdrant) > 40:
				print(f"           ... {len(missing_in_qdrant) - 40} more", file=sys.stderr)
		if extra_in_qdrant:
			print(f"[refresh]   extra in Qdrant ({len(extra_in_qdrant)}):", file=sys.stderr)
			for k in sorted(extra_in_qdrant)[:40]:
				print(f"           + {k[0]}#{k[1]}", file=sys.stderr)
			if len(extra_in_qdrant) > 40:
				print(f"           ... {len(extra_in_qdrant) - 40} more", file=sys.stderr)
		if hash_drift_keys:
			print(f"[refresh]   content_hash drift ({len(hash_drift_keys)}):", file=sys.stderr)
			for k in hash_drift_keys[:40]:
				print(f"           ~ {k[0]}#{k[1]}", file=sys.stderr)
			if len(hash_drift_keys) > 40:
				print(f"           ... {len(hash_drift_keys) - 40} more", file=sys.stderr)
		print("[refresh] HINT: run a normal incremental ingest (no flag) to repair source drift, or `--rebuild` for a full reset. `--refresh-router-metadata` mutates only when parity is exact.", file=sys.stderr)
		return 1

	print(f"[refresh] PARITY PASS: refreshing payload metadata + document for {len(refresh_plan)} points...")
	refreshed = 0
	for point_id, new_payload in refresh_plan:
		client.set_payload(
			collection_name=collection,
			payload=new_payload,
			points=[point_id],
		)
		refreshed += 1
		if progress_every > 0 and (refreshed % progress_every == 0 or refreshed == len(refresh_plan)):
			print(f"[refresh] progress: {refreshed}/{len(refresh_plan)} points", flush=True)

	print(f"[refresh] DONE: refreshed {refreshed} points (no embeds, no deletes, no UUID changes)")
	return 0


def scroll_existing_chunk_hashes(
	client: QdrantClient,
	collection: str,
) -> dict[tuple[str, int], str]:
	"""Scroll a Qdrant collection and return {(source_file, chunk_index): content_hash}.

	Returns empty dict if collection does not exist. Bad/legacy payloads are
	counted and reported on stderr but do not abort the scroll.
	"""
	existing: dict[tuple[str, int], str] = {}
	coll_names = [c.name for c in client.get_collections().collections]
	if collection not in coll_names:
		return existing
	bad_payload = 0
	offset: Any = None
	while True:
		records, next_offset = client.scroll(
			collection_name=collection,
			limit=512,
			offset=offset,
			with_payload=True,
			with_vectors=False,
		)
		for rec in records:
			payload = rec.payload if isinstance(rec.payload, dict) else None
			meta = payload.get("metadata") if isinstance(payload, dict) else None
			if not isinstance(meta, dict):
				bad_payload += 1
				continue
			sf = meta.get("source_file")
			ci = meta.get("chunk_index")
			ch = meta.get("content_hash")
			if not (isinstance(sf, str) and isinstance(ci, int) and isinstance(ch, str)):
				bad_payload += 1
				continue
			existing[(sf.replace("\\", "/"), ci)] = ch
		if next_offset is None:
			break
		offset = next_offset
	if bad_payload:
		print(
			f"       INCREMENTAL-SCROLL: {bad_payload} points lacked usable "
			"(source_file, chunk_index, content_hash) payload",
			file=sys.stderr,
		)
	return existing


def delete_orphan_points(
	client: QdrantClient,
	collection: str,
	orphan_keys: list[tuple[str, int]],
) -> int:
	"""Delete points by recomputed UUID v5. Returns the number deleted."""
	if not orphan_keys:
		return 0
	point_ids = [compute_point_uuid(collection, sf, ci) for (sf, ci) in orphan_keys]
	BATCH = 256
	for i in range(0, len(point_ids), BATCH):
		client.delete(
			collection_name=collection,
			points_selector=PointIdsList(points=point_ids[i:i + BATCH]),
		)
	return len(point_ids)


def build_point_struct(
	collection: str,
	vec_name: str,
	chunk: dict[str, Any],
	vector: Any,
) -> PointStruct:
	pid = compute_point_uuid(collection, chunk["source_file"], chunk["chunk_index"])
	meta_blob: dict[str, Any] = {
		"source_file": chunk["source_file"],
		"chunk_index": chunk["chunk_index"],
		"chunk_count": chunk["chunk_count"],
		"file_size": chunk["file_size"],
		"content_hash": compute_chunk_hash(chunk["body_text"]),
		"approx_tokens": approx_tokens(chunk["text"]),
		"typedb_version": chunk["typedb_version"],
		"content_type": chunk["content_type"],
		"syntax_safe_for_3x": chunk["syntax_safe_for_3x"],
	}
	extra = chunk.get("ontology_router_extra")
	if extra:
		meta_blob.update(extra)
	return PointStruct(
		id=pid,
		vector={vec_name: vector.tolist()},
		payload={
			"document": chunk["text"],
			"metadata": meta_blob,
		},
	)


def main():
	ap = argparse.ArgumentParser(
		description=(
			"Load the ontology-tutor ROUTER corpus into Qdrant. "
			"--ontology-router is REQUIRED — ROUTER is the canonical corpus source."
		)
	)
	ap.add_argument("--root", type=Path, default=DEFAULTS["root"])
	ap.add_argument("--qdrant-url", default=DEFAULTS["qdrant_url"])
	ap.add_argument("--collection", default=DEFAULTS["collection"])
	ap.add_argument("--model", default=DEFAULTS["embedding_model"])
	ap.add_argument("--dry-run", action="store_true")
	ap.add_argument("--ontology-router", type=Path, required=True,
		help="REQUIRED. Ontology-tutor ROUTER.yaml. Its vector_source_file_registry "
		"(literals + globs) is the only source of truth for which snapshot paths get embedded.")
	ap.add_argument("--strict-mcp", action="store_true",
		help="Validate ROUTER MCP descriptor_folder_hint, expected_tools_lexicographic, and row mandatory_sequence registrations/tools before any vector work.")
	ap.add_argument("--mcp-descriptor-root", type=Path, default=Path("C:/Users/rtoth/.cursor/projects/c-dev/mcps"),
		help="Directory containing Cursor MCP descriptor folders used by --strict-mcp.")
	ap.add_argument("--embed-batch-size", type=int, default=4)
	ap.add_argument("--embed-progress-every", type=int, default=5,
		help="Print embedding progress every N chunks finished (0 = quiet until done line).")
	ap.add_argument("--chunk-file-progress-every", type=int, default=25,
		help="Print chunking progress every N files processed (0 = silent until total).")
	ap.add_argument("--upsert-progress-every", type=int, default=256,
		help="Print Qdrant upsert progress every N points (0 = quiet until final upsert summary).")
	ap.add_argument("--verify-router-qdrant", action="store_true",
		help="Compare (source_file, chunk_index, content_hash) triples in Qdrant to those produced by build_ontology_skill_registry_chunks; exit 0 iff equal. No embed.")
	ap.add_argument("--refresh-router-metadata", action="store_true",
		help="Refresh ROUTER-derived payload metadata (skill_id, router_version, routing_id, routing_ids_utf8_lexicographic, lineage_source, typedb_authority_plane) and the stored document banner in place. No embeds, no deletes, no UUID changes. Aborts non-zero if file/chunk/content_hash parity with Qdrant is broken; use a normal incremental ingest or --rebuild in that case. Mutually exclusive with --rebuild and --verify-router-qdrant.")
	ap.add_argument("--rebuild", action="store_true",
		help="Force full drop + recreate of the Qdrant collection (default is incremental hash dedup: scroll existing, embed only new+changed chunks, delete orphans). Use only when you actually need to recreate the collection (e.g. embedding model change). For ROUTER metadata refresh, use --refresh-router-metadata instead.")
	ap.add_argument("--max-chunks-per-file", type=int, default=0,
		help="Per-file chunk budget. 0 = uncapped (default). When >0, keeps first N chunks per file and prints CHUNK-CAP-TRUNCATE on stderr.")
	ap.add_argument("--max-total-chunks", type=int, default=0,
		help="Global chunk budget across all files. 0 = uncapped (default). When >0, keeps first N total chunks and prints CHUNK-CAP-TOTAL on stderr.")

	args = ap.parse_args()
	if args.max_chunks_per_file < 0:
		print("ERROR: --max-chunks-per-file must be >= 0", file=sys.stderr)
		sys.exit(2)
	if args.max_total_chunks < 0:
		print("ERROR: --max-total-chunks must be >= 0", file=sys.stderr)
		sys.exit(2)
	if args.chunk_file_progress_every < 0:
		print("ERROR: --chunk-file-progress-every must be >= 0", file=sys.stderr)
		sys.exit(2)
	mode_flags = [args.verify_router_qdrant, args.refresh_router_metadata, args.rebuild]
	if sum(1 for f in mode_flags if f) > 1:
		print("ERROR: --verify-router-qdrant, --refresh-router-metadata, and --rebuild are mutually exclusive.", file=sys.stderr)
		sys.exit(2)

	if args.root is None:
		print(
			"ERROR: snapshot root not set. Pass --root PATH or set the "
			"TYPEDB_SNAPSHOT_ROOT environment variable.",
			file=sys.stderr,
		)
		sys.exit(2)
	root = args.root.resolve()
	print("=" * 70)
	print("TYPEDB SNAPSHOT VECTOR LOADER (ROUTER-only)")
	print("=" * 70)
	print(f"  Root:       {root}")
	print(f"  Qdrant:     {args.qdrant_url}")
	print(f"  Collection: {args.collection}")
	print(f"  Model:      {args.model}")
	print(f"  Dry run:    {args.dry_run}")
	if args.refresh_router_metadata:
		mode_label = "refresh-router-metadata"
	elif args.verify_router_qdrant:
		mode_label = "verify-router-qdrant"
	elif args.rebuild:
		mode_label = "rebuild"
	else:
		mode_label = "incremental"
	print(f"  Mode:       {mode_label}")
	caps_label = (
		f"per-file={args.max_chunks_per_file or 'none'}; "
		f"total={args.max_total_chunks or 'none'}"
	)
	print(f"  Caps:       {caps_label}")
	print(
		f"  Progress:   chunk every {args.chunk_file_progress_every} files; "
		f"embed every {args.embed_progress_every} chunks; upsert every {args.upsert_progress_every} points"
	)
	print()

	or_path = args.ontology_router.resolve()
	print(f"  Ontology:   ROUTER {or_path}")
	try:
		router_doc = load_router_yaml(or_path)
		verify_registry_for_ontology_ingest(root, router_doc)
		if args.strict_mcp:
			mcp_root = args.mcp_descriptor_root.resolve()
			print(f"  Strict MCP: {mcp_root}")
			mcp_errors = validate_router_mcp_bindings(router_doc, mcp_root)
			if mcp_errors:
				print("  STRICT-MCP FAILED:", file=sys.stderr)
				for err in mcp_errors:
					print(f"       {err}", file=sys.stderr)
				sys.exit(2)
			print("  Strict MCP: PASS")
		reg_block = router_doc.get("vector_source_file_registry")
		ontology_skill_path_set: set[str] = set()
		if isinstance(reg_block, dict):
			ontology_skill_path_set = {
				s["source_file"]
				for s in collect_ontology_skill_registry_sources(root, reg_block)
			}
			print(f"  Ontology registry paths resolved: {len(ontology_skill_path_set)}")
	except Exception as exc:
		print(f"  ONTOLOGY-ROUTER INIT FAILED: {exc}", file=sys.stderr)
		sys.exit(1)

	if args.verify_router_qdrant:
		print()
		rc = verify_router_qdrant_file_parity(
			root, router_doc, args.qdrant_url, args.collection, args.max_chunks_per_file
		)
		sys.exit(rc)

	if args.refresh_router_metadata:
		print()
		rc = refresh_router_metadata_in_qdrant(
			root,
			router_doc,
			args.qdrant_url,
			args.collection,
			args.max_chunks_per_file,
		)
		sys.exit(rc)

	print(f"[1/5] Discovery: ROUTER vector_source_file_registry only (no full-tree rglob).")
	print(f"\n[2/5] Chunking...")
	try:
		all_chunks = build_ontology_skill_registry_chunks(
			root,
			router_doc,
			args.max_chunks_per_file,
			args.chunk_file_progress_every,
			report_caps=True,
		)
		onto_n = len(all_chunks)
		print(f"       {onto_n} ontology skill snapshot-registry chunks")
		if all_chunks:
			toks = [approx_tokens(c["text"]) for c in all_chunks]
			print(f"       avg ~{sum(toks)/len(toks):.0f} tokens, max ~{max(toks)}")
	except Exception as exc:
		print(f"       ONTOLOGY-ROUTER FAILED: {exc}", file=sys.stderr)
		sys.exit(1)

	pre_total = len(all_chunks)
	all_chunks = apply_chunk_cap_total(all_chunks, args.max_total_chunks, report=True)
	if len(all_chunks) != pre_total:
		print(f"       TOTAL chunks (post-cap): {len(all_chunks)} of {pre_total}")
	else:
		print(f"       TOTAL chunks: {len(all_chunks)}")
	if not all_chunks:
		print("ERROR: Nothing to embed — ROUTER vector_source_file_registry resolved zero chunks.")
		sys.exit(1)

	if args.dry_run:
		print(f"\nDry-run complete; skipping embed and Qdrant.")
		return

	print(f"\n[3/5] Mode decision...")
	client = QdrantClient(url=args.qdrant_url, check_compatibility=False)
	existing_collections = [c.name for c in client.get_collections().collections]
	collection_exists = args.collection in existing_collections
	full_rebuild_mode = args.rebuild or not collection_exists

	if args.rebuild and collection_exists:
		print(f"       --rebuild flag set + collection exists -> full drop + recreate ({len(all_chunks)} chunks to embed)")
	elif args.rebuild and not collection_exists:
		print(f"       --rebuild flag set + collection does not exist -> create + embed all ({len(all_chunks)} chunks)")
	elif not collection_exists:
		print(f"       collection {args.collection!r} does not exist -> first ingest, embed all ({len(all_chunks)} chunks)")
	else:
		print(f"       incremental: collection exists, scrolling for content hashes...")

	chunks_to_embed: list[dict[str, Any]] = all_chunks
	orphan_keys: list[tuple[str, int]] = []

	if not full_rebuild_mode:
		existing = scroll_existing_chunk_hashes(client, args.collection)
		print(f"       existing points indexed: {len(existing)}")
		short_hash_n = sum(1 for h in existing.values() if len(h) < 64)
		if short_hash_n > 0:
			print(
				f"       INCREMENTAL-WARN: {short_hash_n} existing points carry legacy <64-hex hashes;",
				file=sys.stderr,
			)
			print(
				"                         all such keys will re-embed as 'changed' until next --rebuild.",
				file=sys.stderr,
			)
		parts = partition_chunks_for_incremental(existing, all_chunks)
		chunks_to_embed = parts["new"] + parts["changed"]
		orphan_keys = parts["orphans"]
		print(
			f"       partition: new={len(parts['new'])} changed={len(parts['changed'])} "
			f"unchanged={len(parts['unchanged'])} orphans={len(orphan_keys)}"
		)

	vec_name = mcp_vector_name(args.model)
	embed_dim: int | None = None
	vectors: list[Any] = []

	if chunks_to_embed:
		print(f"\n[4/5] Embedding {len(chunks_to_embed)} chunks (batch={args.embed_batch_size})...")
		print(f"       Initializing embedding model ({args.model})...")
		t0 = time.time()
		embedder = TextEmbedding(model_name=args.model)
		print("       running warmup embed (model download / ONNX load can take several minutes on first run)", flush=True)
		probe = list(embedder.embed(["warmup"]))[0]
		embed_dim = len(probe)
		print(f"       {embed_dim} dimensions in {time.time() - t0:.1f}s")

		t0 = time.time()
		texts = [c["text"] for c in chunks_to_embed]
		bs = max(1, args.embed_batch_size)
		if args.embed_progress_every > 0:
			print(
				f"       batched embedding ({bs} texts/batch); logging every {args.embed_progress_every} chunks",
				flush=True,
			)
		vectors = embed_chunks_reporting(embedder, texts, bs, args.embed_progress_every)
		dt = time.time() - t0
		print(f"       done in {dt:.1f}s ({len(vectors)/max(dt,1e-9):.1f} chunks/s)")
	else:
		print(f"\n[4/5] No new or changed chunks -> embed step skipped.")

	print(f"\n[5/5] Updating Qdrant ({args.collection})...")
	if full_rebuild_mode:
		if collection_exists:
			print(f"       Dropping existing collection")
			client.delete_collection(args.collection)
		assert embed_dim is not None, "rebuild mode reached without embed_dim (chunks_to_embed should never be empty in rebuild)"
		client.create_collection(
			collection_name=args.collection,
			vectors_config={vec_name: VectorParams(size=embed_dim, distance=Distance.COSINE)},
		)
		print(f"       Created {args.collection} ({embed_dim}-dim, cosine, vector={vec_name})")

	points = [
		build_point_struct(args.collection, vec_name, chunk, vec)
		for chunk, vec in zip(chunks_to_embed, vectors)
	]
	BATCH = 64
	ups_every = args.upsert_progress_every
	for i in range(0, len(points), BATCH):
		client.upsert(collection_name=args.collection, points=points[i:i + BATCH])
		done_pts = min(i + BATCH, len(points))
		if ups_every > 0:
			if done_pts % ups_every == 0 or done_pts == len(points):
				print(f"       upsert progress: {done_pts}/{len(points)} points", flush=True)
		elif done_pts == len(points):
			print(f"       upsert progress: {done_pts}/{len(points)} points", flush=True)

	if full_rebuild_mode:
		for field in ("typedb_version", "content_type", "syntax_safe_for_3x"):
			client.create_payload_index(
				collection_name=args.collection,
				field_name=f"metadata.{field}",
				field_schema=PayloadSchemaType.KEYWORD if field != "syntax_safe_for_3x" else PayloadSchemaType.BOOL,
			)
		if onto_n > 0:
			for pname in ("routing_id", "skill_id"):
				try:
					client.create_payload_index(
						collection_name=args.collection,
						field_name=f"metadata.{pname}",
						field_schema=PayloadSchemaType.KEYWORD,
					)
				except Exception:
					pass

	deleted_n = 0
	if orphan_keys:
		print(f"       deleting {len(orphan_keys)} orphan points (keys absent from current corpus)...")
		deleted_n = delete_orphan_points(client, args.collection, orphan_keys)

	info = client.get_collection(args.collection)
	mode_label = "REBUILD" if full_rebuild_mode else "INCREMENTAL"
	print(
		f"       Upserted {len(points)} points; deleted {deleted_n} orphans; "
		f"collection now reports {info.points_count}"
	)
	ver_counts: dict[str, int] = {}
	for c in all_chunks:
		ver_counts[c["typedb_version"]] = ver_counts.get(c["typedb_version"], 0) + 1
	print(f"       Version breakdown (corpus): {ver_counts}")

	print("\n" + "=" * 70)
	print(f"LOAD COMPLETE ({mode_label})")
	print("=" * 70)
	print(f"  Collection: {args.collection}")
	print(f"  Points:     {info.points_count}")
	print(f"  Upserted this run: {len(points)}")
	print(f"  Deleted this run:  {deleted_n}")
	print(f"  Source: ROUTER vector_source_file_registry ({len(ontology_skill_path_set)} paths resolved)")


if __name__ == "__main__":
	main()
