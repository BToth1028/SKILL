---
name: ontology-tutor
description: Use when designing or validating ontology-driven databases, TypeQL schemas, ER models, knowledge graphs, type hierarchies, folder taxonomies, vault structures, PARA/BASB layouts, or when the user asks "how should I model this", "what entities do I need", "should this be its own folder", or "is this an entity or attribute".
license: Internal use only
---

# ontology-tutor

Deterministic ontology engineering for databases and folder systems. The skill teaches and applies TypeDB-grounded modeling primitives: entities, relations, attributes, roles, type hierarchies, ownership, inference, closed-world classification, and traceable design decisions. In mode 2, the skill additionally produces SQL Server-compatible embodiment of TypeDB design decisions with governed field-value review and operator-approved removal workflow.

> **Before proceeding:** Read `CONTRACT.yaml` in this directory. It contains every definition, enum, gate, schema, error code, and invariant this skill references. This file contains only procedures, narratives, and rationale. If a §-pointer appears below, its target is defined in CONTRACT.yaml — see the `pointer_legend` there for the full index.

## Session Mission

Help the student design, validate, and learn ontology-driven systems where every classification, naming choice, hierarchy decision, and relationship is grounded in retrieved TypeDB evidence and recorded in an auditable `decision_trace`. In mode 2, additionally guide SQL Server embodiment of those design decisions using governed field-value review.

## Mandatory Activation

Run these steps when the operator explicitly invokes ontology-tutor or asks for ontology/schema/modeling guidance.

1. Read this `SKILL.md`.
2. **Read `CONTRACT.yaml`** — the deterministic definitions companion in the same directory. All enums, gates, schemas, error codes, and invariants are defined there. **No Source 1 / Source 2 / Source 3 evidence MCP call may run until this step completes.**
3. **Read canonical `ROUTER.yaml`** — the machine contract in the same directory as this `SKILL.md` (`ontology-tutor/ROUTER.yaml`). On success, set `router.router_status: present` and `router.router_version` from the file's top-level `router_version` (or `UNKNOWN` if key absent). If the file is missing or unreadable, set `router.router_status: missing` and `router.router_version: UNKNOWN`; then follow §Y — never emit `not_checked` for a session where this step was attempted.
4. **MCP pre-flight check:** Verify that the MCP tools required by §L are reachable before entering the evidence pipeline. Test each: `user-directive-mcp-search` (Source 1 / Qdrant), `user-typedb-snapshot-mcp` (Source 2 / snapshot filesystem). If a required MCP is unreachable, record `mcp_preflight: { <mcp_name>: unreachable }` and alert the operator — do not silently proceed into a pipeline that will fail at the first evidence call.
5. Confirm or default the active mode per §M. If the operator has not declared a mode, default to mode 1.
6. Select the routing command per §D:
   - `GENERAL` for broad modeling questions.
   - `/schema` for TypeQL or schema design.
   - `/folders` for folder hierarchy or file organization.
   - `/validate` for auditing existing designs (mode 1).
   - `/sql-embody` for SQL Server embodiment of a TypeDB design (mode 2).
   - `/sql-validate` for auditing an existing SQL embodiment against TypeDB intent (mode 2).
   - `/trace` for provenance questions.
   - `/lesson`, `/learn`, `/project`, `/explain` for teaching flows.
7. Capture the current time as ISO-8601; record it as `authority_probed_at` on every successful emission.
8. Classify `question_type` per §Q and run the Evidence Sufficiency Procedure (§E) in parallel with the evidence pipeline where applicable (counts, triggers, adversarial round, time-box).
9. Execute the evidence pipeline per the Source Authority Model procedure below (Source 1 → Source 2 → Source 3 → Source 9 gate → stop). If Source 2 finds paths not covered by the ROUTER, recommend a ROUTER promotion: add exact literals or tight globs, bump `router_version`, and rerun the loader.
10. Classify and design only after evidence is gathered.
11. Emit YAML with `decision_trace`, `evidence_sufficiency`, validation gates, and residual evidence gaps — per §N and §W.

## Source Authority Model — Procedures

All source definitions, evidence order, transition criteria, the refresh-only constraint, the `authority_source` enum (§A), tool permissions (§L), and the Source 9 hard gate prompt (§H) are defined in CONTRACT.yaml under §R, §T, and related sections. This section defines only the **procedural execution** of the evidence pipeline. Do not restate source rules here — defer to CONTRACT.yaml.

### Evidence Pipeline Execution

The evidence pipeline follows the fixed order defined in §R. Execute it as follows:

1. **Check Source 1:** Does the router-governed vector corpus contain the needed evidence (per the Source 1 criterion in §T)?
   - Yes → proceed with the session (step 3 below).
   - No → continue to step 2.
2. **Check Source 2:** Does snapshot-mcp contain the needed evidence (per the Source 2 criterion in §T)?
   - Yes → append the required source to `ROUTER.yaml`, run the vectorizer, wait until vectorization completes.
     - If vectorizer did not execute → emit `REFRESH_FAILED: VECTORIZER_UNAVAILABLE` (§X), halt, alert operator.
     - If vectorizer ran but Source 1 still does not contain the needed evidence after completion → emit `REFRESH_FAILED: SOURCE_NOT_INGESTED` (§X) (hard stop — alert operator), halt.
     - Otherwise → return to step 1.
   - No → check Source 3: does typedb.com contain the needed evidence (per the Source 3 criterion in §T)?
     - Yes → same refresh procedure as Source 2 above.
     - No → invoke the Source 9 hard gate (§H). If operator does not approve → emit `EVIDENCE_EXHAUSTED` (§X), halt.
3. **Proceed** with the session only after Source 1 contains the required evidence.

### Refresh-Phase Boundary

The mutations permitted during the evidence-refresh loop are defined in CONTRACT.yaml (`refresh_phase_mutations`). The phase boundary is explicit: refresh activates on evidence absence, completes when vectorization finishes, then restarts from Source 1. Outside of this phase, execution is read-only per §L.

### Evidence Sufficiency Execution (A-F)

This procedure controls how deep retrieval goes when Source 1 already returns citeable chunks. It is orthogonal to the evidence pipeline: the pipeline forces Source 2 → ingest → Source 1 when Source 1 lacks any citeable answer. A-F answers: given at least one citeable chunk, when must the agent still hit Source 2, Source 3, or extra Source 1 rounds?

All definitions — `question_type` enum (§Q), `minimum_evidence_units` table, evidence unit definition, saturation rules, contradiction handling, adversarial query requirements, time-box limits, and F-triggers — are in CONTRACT.yaml under §E. Maintain the following state tracker across all rounds to reduce working memory:

```
es_state: { question_type: null, min_units: null, units_achieved: 0,
             round_index: 0, saturated: false, contradiction: false,
             adversarial_run: false }
```

Update `es_state` after each step below. Execute in order:

**A** — Classify `question_type` per §Q. Record in `evidence_sufficiency.question_type` on every successful emission.

**B** — Look up `minimum_evidence_units` from the table in §E based on the question_type from A.

**C** — Maintain the `atomic_claim_hashes` set per the saturation rules in §E. After each retrieval round, apply the stop condition. If saturation occurs before `minimum_evidence_units`, do not stop — refine queries or escalate to Source 2 per F-triggers.

**D** — If two citeable chunks make incompatible definitional assertions about the same TypeDB primitive or keyword, retrieval has not converged. Log `decision_trace` entry `rule_applied: contradiction`. Run additional passes until reconciled with an explicit reconciliation note in `decision_trace`, or emit `CONTRADICTION_UNRESOLVED` (§X) with both citations.

**E** — Before final emission, run at least one `qdrant-find` whose query negates or challenges the draft conclusion (opposite keyword or "common misconception" pattern). If a citeable chunk supports counter-evidence, retrieval continues until reconciled in `decision_trace`. If no citeable counter-evidence → record `evidence_sufficiency.adversarial_query_run: true` and proceed.

**F** — Apply the time-box per §E. One round = one batch of retrieval work per the round definition in §E. If round index reaches `max_search_rounds` without satisfying B and unresolved D → emit `EVIDENCE_BUDGET_EXHAUSTED` (§X) with partial `decision_trace` and `actionable: false` for design claims still unsupported. Apply F-triggers per §E when any trigger fires.

## Evidence Sources — Operational Procedures

The rules governing when each source is used, transition criteria (§T), the refresh-only constraint, and the `authority_source` enum (§A) are defined in CONTRACT.yaml. This section defines only the operational query and retrieval procedures for each source.

### Source 1 — Vector Retrieval

Use `user-directive-mcp-search` / `qdrant-find` for substantive retrieval. Query text must include the task, the TypeDB primitive terms relevant to the active question (see the primitive term list in CONTRACT.yaml under `source_2_phases`), and when known:

- `skill: ontology-tutor`
- `routing_id_token: <routing id>`
- `corpus_roots: <read host_capture_root_hint from ROUTER typedb_snapshot_mcp_binding>`
- direct terms from the user's domain

Apply the Source 1 citeability criterion defined in CONTRACT.yaml (`source_1_citeability`). Query hints, ROUTER prose, and situational YAML are not facts.

### Source 2 — Snapshot Filesystem

Use `user-typedb-snapshot-mcp` when Source 1 is insufficient. Execute the phases defined in CONTRACT.yaml (`source_2_phases`) in order when Source 1 is insufficient; record each phase in `decision_trace` before declaring Source 2 exhausted:

1. Read `_snapshot/manifest.yaml` and `docs_snapshot/manifest.yaml` when available. (Paths are relative to the MCP server root `/typedb-snapshot`.)
2. Search exact user/domain terms with `search_files`.
3. Search TypeDB primitive terms from the active question per the primitive term list in CONTRACT.yaml.
4. Search command-specific terms per the command-specific term table in CONTRACT.yaml.
5. Read matched manifest, schema, and documentation files with `read_text_file` in the priority order defined in CONTRACT.yaml: exact filename matches, schema files, docs paths containing command-specific terms, then docs paths containing primitive terms.
6. Record `probe_b_search_terms`, `probe_b_matched_paths`, `probe_b_read_paths`, and `probe_b_failure_reason` on the `decision_trace` entry that documents this Source 2 pass (mirror this obligation in §W).
7. Advance to typedb.com only after phases 1-6 complete or the snapshot server/root is unavailable.

The criterion for "contains the needed evidence" for Source 2 is defined in §T. Search-result paths without read content are never sufficient.

### Source 3 — typedb.com

When Source 3 is reached per the transition rules in §T, log the fallback in `decision_trace` and distinguish external docs from local snapshot evidence. The criterion for "contains the needed evidence" for Source 3 and the transition to the Source 9 gate are defined in §T.

## Decision Procedure

### Mode 1 — Pure TypeDB

For commands listed under `mode_1` in §D, run this fixed pipeline.

0. **Scope check:** Classify the request against §S (if any out-of-scope bullet matches → out-of-scope). If out-of-scope → emit `OUT_OF_SCOPE` (§X) immediately. Do not proceed.
1. **Evidence refresh:** Run the evidence pipeline procedure above — confirm Source 1 contains the needed evidence before proceeding.
2. **Identify TypeDB pattern:** For each candidate in the request, match it to exactly one TypeDB reference pattern from this closed list: entity, relation, role, attribute, ownership, subtyping, inference, or query pattern. The match must be supported by at least one citeable Source 1 chunk that uses the candidate term in the context of that pattern. If no citeable chunk supports a match → assign `UNKNOWN` and proceed to step 7.
3. **Classify candidates:** Classify each candidate as exactly one value from §C.
4. **Subtype test:** A subtype is justified only when the child type **owns >=1 attribute the parent does not** OR **plays >=1 role the parent does not**, per cited TypeDB evidence in Source 1 (which may contain evidence originally from Source 2 or Source 3 via the evidence-refresh loop).
5. **Relation test:** A relation is justified only when it **names a verb-phrase the participants alone do not name** OR **is referenced as a role-player in another relation**, per cited TypeDB evidence in Source 1.
6. **Attribute test:** If the thing describes one owner and has no independent role structure, model it as an attribute.
7. **Evidence-gap:** When none of the subtype test, relation test, or attribute-test predicates applies to a candidate **and** evidence is insufficient to justify a stronger classification, classify that candidate as `UNKNOWN` with `rule_applied: evidence-gap` in `decision_trace`.
8. **Generate decision_trace** for every emitted item per §K (items recorded in pipeline step order).
9. **Generate content body** — the schema design, TypeQL, classification output, or explanation — based on the evidence gathered and classifications made in steps 2-7. Apply the correction gate (§Z) when input contains malformed TypeQL: hard-stop and present the operator with the correction table. No correction is applied without explicit operator approval.
10. **Run validation gates** per §G.
11. **Emit output** per §W and §N.

### Mode 2 — TypeDB Embodiment using SQL

For commands listed under `mode_2` in §D, run this fixed pipeline. **One table per invocation** (§1).

0. **Scope check and parse gate:** Classify the request against §S. If out-of-scope → emit `OUT_OF_SCOPE` (§X) immediately. Then inspect the provided DDL/SQL input for syntactic validity and structural completeness:
   - If input is syntactically invalid or structurally corrupt → emit `MALFORMED_INPUT` (§X), present the operator with a correction table per §Z, halt until operator selects a correction.
   - If input is syntactically valid but semantically ambiguous (missing constraints, incomplete key definitions, or other semantic ambiguity recorded by name in `decision_trace`) → log issues in `decision_trace`, continue with scope check and alert operator in the final output.
1. **Evidence refresh:** Run the evidence pipeline procedure above — confirm Source 1 contains the needed evidence before proceeding.
2. **Field value test:** For every source SQL field, run `field_value_test`:
   - Assign `source_nullability`, `source_type`, and at least one `value_categories` entry from §V.
   - Set `test_result` to a value from the `test_result` enum in CONTRACT.yaml.
   - Populate `evidence` with direct observation.
   - Populate `failure_reason` when `test_result = fail`; populate `uncertainty_reason` when `test_result = uncertain`.
3. **Cursory semantic review:** For every field, independently of the `field_value_test` result, apply the `cursory_semantic_review_criteria` predicates defined in §F. Evaluate `recommend_keep` first; if no condition is met, evaluate `recommend_remove`; if not all conditions are met, assign `uncertain`. Record the `agent_cursory_result` per field.
4. **Field review matrix:** Populate `field_review_matrix` for every field by comparing the cursory review result against the `field_value_test` result:
   - `agree_keep` → recommend keep; `operator_decision` required before finalizing.
   - `agree_remove` → add to `proposed_removals` with `operator_decision = pending_review`.
   - `disagree` → run detailed field review; add to `disagreements` with evidence and recommendation.
   - `both_uncertain` → run detailed field review; add to `disagreements`.
5. **Field removal governance:** No field may be excluded from mirroring (`removed_from_legacy`) unless `operator_decision = approved_remove`. Apply the canonical rules in §F.
6. **TypeDB intent mapping:** Produce TypeDB intent mapping for all retained fields: map each field to one TypeDB primitive consistent with Mode 1 steps 2-6 (entity, relation, role, attribute, ownership, subtyping, inference, query pattern) as embodied in SQL-relevant constructs. Apply the Mode 1 subtype, relation, and attribute tests where those constructs are asserted.
7. **Generate decision_trace** for every emitted item per §K (items recorded in pipeline step order).
8. **Generate SQL embodiment:** The SQL Server-compatible CREATE TABLE and supporting constraints embodying the TypeDB intent mapping from step 6.
9. **Alignment check:** For every field, compare the TypeDB construct from step 6 against the SQL construct from step 8. Produce an `alignment_report` per §W. If perfectly aligned → note that fact. If not perfectly aligned but intent can still be met via a documented workaround → provide a detailed summary. If not perfectly aligned and no workaround can meet the intent → emit `ALIGNMENT_IMPOSSIBLE` (§X), halt, alert operator.
10. **Run validation gates** per §G (including `alignment_gate`).
11. **Emit output** per §W and §N.

## Field Value Governance — Workflow

The canonical governance rules, the `value_categories` enum (§V), the `operator_decision` enum (§O), removal state rules, and the nullability rule are defined in CONTRACT.yaml under §F. This section describes only the procedural workflow.

When reviewing a field for removal:

1. Run the `field_value_test` per Mode 2 step 2 above.
2. Check the field against §V — a field may stay only if it provides at least one closed-category value from that enum.
3. Nullability alone is not the removal criterion per §F. A nullable field that provides value stays. A nullable field that provides no value should fail `field_value_test`, but exclusion from mirroring still requires `operator_decision = approved_remove`.
4. Apply the removal state rules per §F: `approved_keep`, `approved_remove`, `rejected_remove`, `pending_review`.
5. The legacy SQL reference is read-only. `removed_from_legacy` means excluded from mirroring into the new schema — it does not modify the legacy reference in any way.

Gate names appear Title-Case-With-Hyphens in prose; in the Output Contract YAML they appear as snake_case per the convention noted in §F.

## Maintainer Workflow

When Source 2 finds useful guidance not covered by vectors:

1. Record the snapshot-relative path.
2. Classify the path as either an exact literal file path or a tight parent glob (per `ROUTER.yaml` schema for `vector_source_file_registry` entries).
3. Add it to `ROUTER.yaml` under `vector_source_file_registry` in UTF-8 lexicographic order.
4. Bump `router_version`.
5. Run the vectorizer loader per §J, passing `--ontology-router <ROUTER.yaml>`.
6. Use `--rebuild` only when metadata stamps must refresh or when incremental repair is insufficient.
7. Verify with `--strict-mcp --verify-router-qdrant`.

## Constraint Rationale

The anti-drift invariants (§I) are not sequential steps — they are assertions that must hold at all points during execution. If any invariant is violated, the pipeline must halt. All 14 invariant assertions are defined in CONTRACT.yaml. The following rationale explains why key constraints exist:

**Evidence authority chain:** Sources 2 and 3 are refresh inputs only (invariants 3, 4, 11). Their content must flow through Source 1 via the evidence-refresh loop before it can ground a design decision. This prevents the agent from short-circuiting the vector corpus and producing decisions that cannot be traced back to Source 1 citations.

**Read-only execution:** Normal execution must not mutate any state (invariant enforced by §L). The only mutations permitted are appending source literals to ROUTER.yaml and running the vectorizer, and only during the refresh phase. This keeps the evidence corpus stable within a session.

**Closed-world classification:** Every classification must come from §C; `UNKNOWN` must never be collapsed into a guess (invariant 7). This ensures the operator always sees when evidence was insufficient rather than receiving a fabricated classification.

**Determinism:** Same evidence and same input must produce the same classification and trace order (invariant 8). This makes the skill auditable and reproducible.

**Deployment isolation:** No deployment-specific paths, URLs, collection names, or project-specific filenames belong in this file or in CONTRACT.yaml (invariant 9). All deployment bindings live in ROUTER.yaml.

**Operator sovereignty over field removal:** No field may be excluded from mirroring without `operator_decision = approved_remove` (invariant 10, §F). The agent may recommend removal, but the operator always has final authority.

**Mode integrity:** Mode 1 behavior must not silently weaken during mode 2 operations (invariant 13). The subtype test, relation test, and attribute test retain their full rigor when applied to TypeDB intent mapping in mode 2.

**Evidence language precision:** The only permitted criterion for source sufficiency is "contains the needed evidence" as defined in §T (invariant 14). Softer synonyms like "sufficient," "adequate," or "directly supports" introduce ambiguity that weakens the gate.
