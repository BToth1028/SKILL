#!/usr/bin/env python3
"""
Runtime contract tests for ontology-tutor.

These tests verify the live skill/ROUTER pair behaves like an executable
runtime contract: route selection is deterministic, MCP registrations/tools
exist, row args satisfy descriptor schemas, and stale live-typedb authority
text has not returned.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml


SKILL_DIR = Path("C:/Users/rtoth/.cursor/skills-cursor/ontology-tutor")
MCP_DIR = Path("C:/Users/rtoth/.cursor/projects/c-dev/mcps")
SKILL_PATH = SKILL_DIR / "SKILL.md"
ROUTER_PATH = SKILL_DIR / "ROUTER.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
	doc = yaml.safe_load(path.read_text(encoding="utf-8"))
	if not isinstance(doc, dict):
		raise AssertionError(f"{path} root is not a mapping")
	return doc


def load_skill_frontmatter() -> dict[str, Any]:
	text = SKILL_PATH.read_text(encoding="utf-8")
	match = re.match(r"^---\n(.*?)\n---", text, re.S)
	if not match:
		raise AssertionError("SKILL.md missing YAML frontmatter")
	doc = yaml.safe_load(match.group(1))
	if not isinstance(doc, dict):
		raise AssertionError("SKILL.md frontmatter is not a mapping")
	return doc


def load_tool_schema(registration: str, tool: str) -> dict[str, Any]:
	path = MCP_DIR / registration / "tools" / f"{tool}.json"
	if not path.is_file():
		raise AssertionError(f"missing MCP descriptor: {path}")
	return load_yaml(path)


def command_primary(prompt: str) -> tuple[str, str | None]:
	text = prompt.strip()
	if not text.startswith("/"):
		return "GENERAL", None
	cmd = text.split(maxsplit=1)[0]
	return "SLASH", cmd


def row_matches(row: dict[str, Any], prompt: str) -> bool:
	primary, slash = command_primary(prompt)
	match = row.get("match")
	if not isinstance(match, dict):
		return False
	if match.get("command_primary") != primary:
		return False
	if primary == "SLASH":
		allowed = match.get("slash_command_any_of") or []
		if slash not in allowed:
			return False
	keywords_any = match.get("keyword_any_of") or []
	keywords_all = match.get("keyword_all_of") or []
	prompt_l = prompt.lower()
	if keywords_any and not any(str(k).lower() in prompt_l for k in keywords_any):
		return False
	if keywords_all and not all(str(k).lower() in prompt_l for k in keywords_all):
		return False
	return True


def select_route(router: dict[str, Any], prompt: str) -> str:
	rows = [r for r in router.get("rows", []) if isinstance(r, dict)]
	matches = [r for r in rows if row_matches(r, prompt)]
	if not matches:
		raise AssertionError(f"no route matched prompt: {prompt}")
	matches.sort(key=lambda r: (-int(r.get("match_priority", 0)), str(r.get("routing_id", ""))))
	routing_id = matches[0].get("routing_id")
	if not isinstance(routing_id, str):
		raise AssertionError("selected row has no routing_id")
	return routing_id


def validate_args_against_descriptor(registration: str, tool: str, args: dict[str, Any]) -> None:
	schema = load_tool_schema(registration, tool)
	arg_schema = schema.get("arguments")
	if not isinstance(arg_schema, dict):
		raise AssertionError(f"{registration}/{tool} has no arguments schema")
	required = arg_schema.get("required") or []
	for key in required:
		if key not in args:
			raise AssertionError(f"{registration}/{tool} missing required arg {key!r}")
	if arg_schema.get("additionalProperties") is False:
		properties = set((arg_schema.get("properties") or {}).keys())
		extra = set(args) - properties
		if extra:
			raise AssertionError(f"{registration}/{tool} has extra args: {sorted(extra)}")


def mcp_steps(row: dict[str, Any]) -> list[dict[str, Any]]:
	return [
		step for step in row.get("mandatory_sequence", []) or []
		if isinstance(step, dict) and step.get("kind") == "MCP"
	]


def test_skill_folder_has_no_stale_runtime_references() -> bool:
	files = sorted(p.relative_to(SKILL_DIR).as_posix() for p in SKILL_DIR.rglob("*") if p.is_file())
	required = {"ROUTER.yaml", "SKILL.md"}
	missing = sorted(required - set(files))
	if missing:
		print(f"FAIL skill_folder_runtime_surface: missing active files {missing}")
		return False
	stale_runtime_refs = [
		path for path in files
		if path.startswith("references/") and path.endswith(".md")
	]
	if stale_runtime_refs:
		print(f"FAIL skill_folder_runtime_surface: stale reference files present {stale_runtime_refs}")
		return False
	print("PASS skill_folder_runtime_surface: active files present and stale references absent")
	return True


# Two-version compatibility handshake (CONTRACT.yaml is authority):
#   CONTRACT.yaml: contract_version 1.3.7, supported_router_version 1.2.1
#   ROUTER.yaml:   router_version 1.2.1,   supported_contract_version 1.3.7
ROUTER_VERSION = "1.2.1"
CONTRACT_VERSION = "1.3.7"


def test_contract_versions_match() -> bool:
	router = load_yaml(ROUTER_PATH)
	skill = SKILL_PATH.read_text(encoding="utf-8")
	frontmatter = load_skill_frontmatter()
	if frontmatter.get("name") != "ontology-tutor":
		print(f"FAIL contract_versions: wrong skill name {frontmatter.get('name')!r}")
		return False
	rv = router.get("router_version")
	scv = router.get("supported_contract_version")
	if rv != ROUTER_VERSION:
		print(f"FAIL contract_versions: router_version {rv!r} != {ROUTER_VERSION!r}")
		return False
	if scv != CONTRACT_VERSION:
		print(f"FAIL contract_versions: supported_contract_version {scv!r} != {CONTRACT_VERSION!r}")
		return False
	if f"**`contract_version`:** `{CONTRACT_VERSION}`" not in skill:
		print(f"FAIL contract_versions: SKILL.md missing contract_version {CONTRACT_VERSION}")
		return False
	if f"**`supported_router_version`:** `{ROUTER_VERSION}`" not in skill:
		print(f"FAIL contract_versions: SKILL.md missing supported_router_version {ROUTER_VERSION}")
		return False
	print(f"PASS contract_versions: SKILL.md/ROUTER.yaml handshake aligned (contract {CONTRACT_VERSION}, router {ROUTER_VERSION})")
	return True


def test_stale_live_authority_is_absent() -> bool:
	skill = SKILL_PATH.read_text(encoding="utf-8")
	forbidden = [
		"mcp__typedb",
		"typedb_mcp",
		"must be consulted before every decision",
		"canonical authority is online",
		"references/tutorai_prompt.md",
		"references/database_patterns.md",
		"references/folder_hierarchy.md",
	]
	found = [term for term in forbidden if term in skill]
	if found:
		print(f"FAIL stale_live_authority_absent: found stale terms {found}")
		return False
	print("PASS stale_live_authority_absent: stale live-MCP/reference authority text absent")
	return True


def test_route_selection_examples() -> bool:
	router = load_yaml(ROUTER_PATH)
	cases = {
		"/schema utility pole attachments": "R-S010_SCHEMA",
		"/folders PARA ontology vault": "R-F010_FOLDERS",
		"/validate this TypeQL schema": "R-V010_VALIDATE",
		"/trace why is customer an entity": "R-T010_TRACE",
		"/lesson teach entity relation attribute": "R-L010_LESSON",
		"How should I model a service order relation?": "R-G010_GENERAL",
		"/sql-embody SQL Server customer table field review": "R-SE010_SQL_EMBODY",
		"/sql-validate operator_decision field governance": "R-SV010_SQL_VALIDATE",
	}
	for prompt, expected in cases.items():
		actual = select_route(router, prompt)
		if actual != expected:
			print(f"FAIL route_selection: {prompt!r} -> {actual}, expected {expected}")
			return False
	print("PASS route_selection: slash and GENERAL prompts select expected rows")
	return True


def test_mcp_steps_are_descriptor_valid() -> bool:
	router = load_yaml(ROUTER_PATH)
	for row in router.get("rows", []) or []:
		if not isinstance(row, dict):
			continue
		for step in mcp_steps(row):
			registration = step.get("registration")
			tool = step.get("tool")
			args = step.get("args") or {}
			if not isinstance(registration, str) or not isinstance(tool, str):
				print(f"FAIL mcp_descriptor_valid: malformed MCP step in {row.get('routing_id')}")
				return False
			if not isinstance(args, dict):
				print(f"FAIL mcp_descriptor_valid: args not mapping in {row.get('routing_id')}")
				return False
			try:
				validate_args_against_descriptor(registration, tool, args)
			except AssertionError as exc:
				print(f"FAIL mcp_descriptor_valid: {exc}")
				return False
	print("PASS mcp_descriptor_valid: all row MCP steps match live descriptor schemas")
	return True


def test_probe_order_is_deterministic() -> bool:
	router = load_yaml(ROUTER_PATH)
	for row in router.get("rows", []) or []:
		if not isinstance(row, dict):
			continue
		steps = mcp_steps(row)
		if not steps:
			print(f"FAIL probe_order: {row.get('routing_id')} has no MCP steps")
			return False
		first = steps[0]
		if first.get("registration") != "user-directive-mcp-search" or first.get("tool") != "qdrant-find":
			print(f"FAIL probe_order: {row.get('routing_id')} does not start with Probe A")
			return False
		if len(steps) > 1:
			second = steps[1]
			if second.get("registration") != "user-typedb-snapshot-mcp" or second.get("tool") != "search_files":
				print(f"FAIL probe_order: {row.get('routing_id')} second MCP step is not Probe B search")
				return False
	print("PASS probe_order: mandatory MCP sequences start with Probe A then Probe B when present")
	return True


def test_snapshot_read_tool_is_available_for_probe_b() -> bool:
	router = load_yaml(ROUTER_PATH)
	binding = router.get("typedb_snapshot_mcp_binding")
	if not isinstance(binding, dict):
		print("FAIL snapshot_read_tool: missing typedb_snapshot_mcp_binding")
		return False
	expected = binding.get("expected_tools_lexicographic") or []
	if "read_text_file" not in expected or "search_files" not in expected:
		print(f"FAIL snapshot_read_tool: expected tools incomplete: {expected}")
		return False
	for tool in ["search_files", "read_text_file"]:
		load_tool_schema("user-typedb-snapshot-mcp", tool)
	print("PASS snapshot_read_tool: Probe B search and read tools are available")
	return True


def test_sql_routes_are_present() -> bool:
	router = load_yaml(ROUTER_PATH)
	rows = {r["routing_id"]: r for r in router.get("rows", []) if isinstance(r, dict) and "routing_id" in r}
	required = {
		"R-SE010_SQL_EMBODY": 95,
		"R-SV010_SQL_VALIDATE": 92,
	}
	for rid, expected_priority in required.items():
		if rid not in rows:
			print(f"FAIL sql_routes_present: missing row {rid}")
			return False
		row = rows[rid]
		if row.get("match_priority") != expected_priority:
			print(f"FAIL sql_routes_present: {rid} priority {row.get('match_priority')!r} != {expected_priority}")
			return False
		steps = mcp_steps(row)
		if not steps or steps[0].get("registration") != "user-directive-mcp-search":
			print(f"FAIL sql_routes_present: {rid} first step is not Probe A")
			return False
		if len(steps) < 2 or steps[1].get("registration") != "user-typedb-snapshot-mcp":
			print(f"FAIL sql_routes_present: {rid} second step is not Probe B")
			return False
	print("PASS sql_routes_present: R-SE010_SQL_EMBODY and R-SV010_SQL_VALIDATE present with correct priorities and Probe A/B sequences")
	return True


def test_mode_selector_is_present_in_skill() -> bool:
	skill = SKILL_PATH.read_text(encoding="utf-8")
	required = [
		"mode = 1",
		"mode = 2",
		"Pure TypeDB",
		"TypeDB Embodiment using SQL",
		"VALIDATOR_INCOMPATIBLE",
		"MODE_REQUIRED",
	]
	missing = [term for term in required if term not in skill]
	if missing:
		print(f"FAIL mode_selector_present: missing terms {missing}")
		return False
	print("PASS mode_selector_present: mode 1 and mode 2 definitions and error codes present in SKILL.md")
	return True


def test_sql_field_governance_is_present() -> bool:
	skill = SKILL_PATH.read_text(encoding="utf-8")
	required = [
		"field_value_test",
		"field_review_matrix",
		"proposed_removals",
		"disagreements",
		"operator_decision",
		"approved_keep",
		"approved_remove",
		"rejected_remove",
		"pending_review",
		"removed_from_legacy",
	]
	missing = [term for term in required if term not in skill]
	if missing:
		print(f"FAIL sql_field_governance_present: missing terms {missing}")
		return False
	print("PASS sql_field_governance_present: all field governance terms present in SKILL.md")
	return True


def test_no_auto_removal_language() -> bool:
	skill = SKILL_PATH.read_text(encoding="utf-8")
	required_phrases = [
		"operator_decision = approved_remove",
		"No field may move to",
	]
	missing = [p for p in required_phrases if p not in skill]
	if missing:
		print(f"FAIL no_auto_removal: required anti-auto-removal phrases missing {missing}")
		return False
	forbidden_phrases = [
		"automatically removed",
		"auto-remove",
		"removed without approval",
	]
	found = [p for p in forbidden_phrases if p in skill]
	if found:
		print(f"FAIL no_auto_removal: forbidden auto-removal phrases found {found}")
		return False
	print("PASS no_auto_removal: anti-auto-removal language present and no forbidden auto-removal phrases")
	return True


def test_evidence_refresh_loop_is_present() -> bool:
	skill = SKILL_PATH.read_text(encoding="utf-8")
	router = load_yaml(ROUTER_PATH)
	skill_required = [
		"Evidence Refresh Loop",
		"Source 2 and Source 3 are refresh inputs only",
		"source_1",
	]
	skill_missing = [t for t in skill_required if t not in skill]
	if skill_missing:
		print(f"FAIL evidence_refresh_loop: SKILL.md missing terms {skill_missing}")
		return False
	if "evidence_refresh_loop_binding" not in router:
		print("FAIL evidence_refresh_loop: ROUTER.yaml missing evidence_refresh_loop_binding")
		return False
	binding = router["evidence_refresh_loop_binding"]
	for key in ("source_1", "source_2", "source_3", "append_target", "decision_restart_after_refresh"):
		if key not in binding:
			print(f"FAIL evidence_refresh_loop: evidence_refresh_loop_binding missing key {key!r}")
			return False
	if binding.get("decision_restart_after_refresh") != "source_1":
		print("FAIL evidence_refresh_loop: decision_restart_after_refresh is not source_1")
		return False
	print("PASS evidence_refresh_loop: refresh loop present in SKILL.md and ROUTER.yaml with correct restart target")
	return True


def test_skill_md_is_deployment_agnostic() -> bool:
	import re
	skill = SKILL_PATH.read_text(encoding="utf-8")
	failures: list[str] = []

	# Absolute paths not inside the skills-cursor tree
	skills_cursor_prefix = "C:/Users/rtoth/.cursor/skills-cursor/"
	for match in re.finditer(r"C:/[^\s`'\"\n]+", skill):
		path = match.group(0).rstrip(".,)")
		if not path.startswith(skills_cursor_prefix):
			failures.append(f"forbidden absolute path: {path!r}")

	# Hardcoded HTTP URLs (deployment values such as Qdrant instance URL)
	for match in re.finditer(r"http://[^\s`'\"\n]+", skill):
		failures.append(f"forbidden http:// URL: {match.group(0)!r}")

	# Project-specific bootstrap filenames
	for match in re.finditer(r"c-dev_[^\s`'\"\n]+", skill):
		failures.append(f"project-specific bootstrap filename: {match.group(0)!r}")

	# Project-specific schema filenames
	for name in ("iam.schema.typeql", "utilix.schema.typeql"):
		if name in skill:
			failures.append(f"project-specific schema filename: {name!r}")

	# Qdrant collection name as a standalone value (not preceded by 'user-')
	for match in re.finditer(r"(?<!user-)directive-mcp-search", skill):
		failures.append(f"hardcoded collection name at offset {match.start()}: {skill[max(0,match.start()-20):match.end()+20]!r}")

	if failures:
		for f in failures:
			print(f"FAIL skill_md_deployment_agnostic: {f}")
		return False
	print("PASS skill_md_deployment_agnostic: SKILL.md contains no forbidden deployment-specific references")
	return True


def main() -> int:
	print("=" * 70)
	print("Tests: ontology-tutor runtime contract")
	print("=" * 70)
	print()
	tests = [
		test_skill_folder_has_no_stale_runtime_references,
		test_contract_versions_match,
		test_stale_live_authority_is_absent,
		test_route_selection_examples,
		test_mcp_steps_are_descriptor_valid,
		test_probe_order_is_deterministic,
		test_snapshot_read_tool_is_available_for_probe_b,
		test_sql_routes_are_present,
		test_mode_selector_is_present_in_skill,
		test_sql_field_governance_is_present,
		test_no_auto_removal_language,
		test_evidence_refresh_loop_is_present,
		test_skill_md_is_deployment_agnostic,
	]
	results: list[bool] = []
	for test in tests:
		try:
			results.append(test())
		except Exception as exc:
			print(f"FAIL {test.__name__}: raised {type(exc).__name__}: {exc}")
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
