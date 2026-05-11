# ontology-tutor — Complete Logic Tree

**Format:** ASCII decision tree, explanatory context  
**Source:** `ontology-tutor/SKILL.md` v1.3.7  
**Date:** 2026-05-08  

---

```
START ontology-tutor
│
│   Trigger: operator invokes skill or asks ontology/schema/modeling question.
│   Constraint: read-only execution. No mutations outside evidence-refresh phase.
│   Constraint: _ar/ folders are dead archives — never read, never reference.
│
└─► [ACTIVATE] — Mandatory Activation
    │
    ├─► step 1: Read SKILL.md
    │
    ├─► step 2: Read ROUTER.yaml
    │   │   Confirm router_version, vector_source_file_registry, MCP binding names.
    │   │   All deployment paths (snapshot root, Qdrant URL, collection, vectorizer,
    │   │   bootstrap corpus root) live in ROUTER.yaml — never hardcoded here.
    │   │
    │   ├─► IF ROUTER.yaml missing or unreadable
    │   │   │   Mark session ROUTER_MISSING.
    │   │   │
    │   │   ├─► IF Source 1 MCP still returns data
    │   │   │   │   Continue with Source 1; ROUTER_MISSING flag stays.
    │   │   │   └───────────────────────────────────────────────► fall through to step 3
    │   │   │
    │   │   └─► ELSE (Source 1 MCP returns nothing)
    │   │       │   Treat as AUTHORITY_DOWN for Source 1 plane.
    │   │       │   Proceed per evidence pipeline — Source 2, then 3, then 9 gate.
    │   │       └───────────────────────────────────────────────► fall through to step 3
    │   │
    │   └─► ELSE (ROUTER present and readable) ─────────────────► fall through to step 3
    │
    ├─► step 3: Set mode
    │   │   Operator declares mode 1 or mode 2 at session start.
    │   │   Every validator must honor the selected mode.
    │   │
    │   ├─► IF operator declares mode 1 ────────────────────────► fall through to step 4
    │   │
    │   ├─► IF operator declares mode 2 ────────────────────────► fall through to step 4
    │   │
    │   └─► ELSE (no mode declared)
    │       │   Default to mode 1.
    │       └───────────────────────────────────────────────────► fall through to step 4
    │
    ├─► step 4: Route command
    │   │   Match the operator's request to one command.
    │   │
    │   │   Mode 1 commands:
    │   │     /schema    — schema design, TypeQL
    │   │     /folders   — folder hierarchy as ontology
    │   │     /validate  — audit existing schema/ER/folder tree
    │   │     /trace     — re-emit decision trace + source paths
    │   │     /lesson, /learn, /project, /explain — teaching flows
    │   │     GENERAL    — modeling question, no slash command
    │   │
    │   │   Mode 2 commands:
    │   │     /sql-embody   — SQL Server embodiment of TypeDB design (one table)
    │   │     /sql-validate — audit SQL embodiment vs TypeDB intent (one table)
    │   │
    │   ├─► IF mode 2 command invoked but mode = 1 (default)
    │   │   └───────────────────────────────────────────────────► [ERROR: MODE_REQUIRED]
    │   │
    │   ├─► IF command requires operand and operand missing
    │   │   │   e.g., /schema needs <domain>, /sql-embody needs <table>
    │   │   └───────────────────────────────────────────────────► [ERROR: INSUFFICIENT_INPUT]
    │   │
    │   └─► ELSE (valid command + operand) ─────────────────────► fall through to step 5
    │
    ├─► step 5: Capture ISO-8601 timestamp
    │   │   Record as authority_probed_at on every successful emission.
    │   └───────────────────────────────────────────────────────► [MODE-DISPATCH]
    │
    └─► [MODE-DISPATCH]
        │
        ├─► IF mode = 1 ───────────────────────────────────────► [MODE-1-PIPELINE]
        │
        └─► IF mode = 2 ───────────────────────────────────────► [MODE-2-PIPELINE]
```

---

```
[MODE-1-PIPELINE]
│
│   Commands: /schema, /folders, /validate, /lesson, /learn,
│   /project, /explain, /trace, GENERAL.
│
├─► step 0: SCOPE CHECK
│   │   Classify request against §Scope in-scope / out-of-scope lists.
│   │
│   ├─► IF any out-of-scope bullet matches
│   │   └───────────────────────────────────────────────────────► [ERROR: OUT_OF_SCOPE]
│   │
│   └─► ELSE (in-scope) ───────────────────────────────────────► fall through to step 1
│
├─► step 1: EVIDENCE REFRESH ──────────────────────────────────► [EVIDENCE-REFRESH-LOOP]
│   │   Returns here once Source 1 confirmed or error emitted.
│   └───────────────────────────────────────────────────────────► fall through to step 2
│
├─► step 2: Identify closest TypeDB reference pattern
│   │   One of: entity, relation, role, attribute, ownership,
│   │   subtyping, inference, or query pattern.
│   └───────────────────────────────────────────────────────────► fall through to step 3
│
├─► step 3: Classify each candidate
│   │   Assign exactly ONE from closed enum:
│   │     entity | entity-subtype | attribute | relation | role |
│   │     abstract-type | view-or-query | operational-artifact | UNKNOWN
│   └───────────────────────────────────────────────────────────► fall through to step 4
│
├─► step 4: Subtype test
│   │   A subtype is justified ONLY when:
│   │     child owns ≥1 attribute parent does not
│   │     OR child plays ≥1 role parent does not
│   │   Evidence must come from Source 1 (may contain S2/S3 via refresh).
│   │
│   ├─► IF test passes → candidate keeps entity-subtype classification
│   │
│   └─► IF test fails → candidate cannot be entity-subtype
│   │
│   └───────────────────────────────────────────────────────────► fall through to step 5
│
├─► step 5: Relation test
│   │   A relation is justified ONLY when:
│   │     it names a verb-phrase the participants alone do not name
│   │     OR it is referenced as a role-player in another relation
│   │   Evidence must come from Source 1.
│   │
│   ├─► IF test passes → candidate keeps relation classification
│   │
│   └─► IF test fails → candidate cannot be relation
│   │
│   └───────────────────────────────────────────────────────────► fall through to step 6
│
├─► step 6: Attribute test
│   │   If the thing describes one owner AND has no independent
│   │   role structure → model as attribute.
│   └───────────────────────────────────────────────────────────► fall through to step 7
│
├─► step 7: Evidence-gap check
│   │   When NONE of subtype/relation/attribute tests apply
│   │   AND evidence is insufficient for a stronger classification:
│   │     classify as UNKNOWN
│   │     set rule_applied = evidence-gap in decision_trace
│   │   Never collapse UNKNOWN into a guess.
│   └───────────────────────────────────────────────────────────► fall through to step 8
│
├─► step 8: Generate decision_trace
│   │   One entry per emitted item, recorded in pipeline step order.
│   │   Each entry: item, classification, canonical_reference,
│   │   authority_source, rule_applied, probe_b fields.
│   └───────────────────────────────────────────────────────────► fall through to step 9
│
├─► step 9: Generate command-specific content body
│   │   Schema design, TypeQL, classification output, or explanation
│   │   based on evidence from steps 2–7.
│   │
│   ├─► [CORRECTION-GATE] — IF input contains malformed TypeQL
│   │   │   Hard-stop. Present correction table to operator:
│   │   │     Option A (Recommended): <fix> + <reasoning from evidence>
│   │   │     Option B: <alternative> + <why less correct>
│   │   │     Option C: <alternative> + <why less correct>
│   │   │
│   │   ├─► IF operator selects a correction
│   │   │   │   Apply selected correction, continue.
│   │   │   └───────────────────────────────────────────────────► fall through to step 10
│   │   │
│   │   └─► IF operator does not select (abandons)
│   │       └───────────────────────────────────────────────────► [STOP]
│   │
│   └─► ELSE (no malformed input) ─────────────────────────────► fall through to step 10
│
├─► step 10: VALIDATION GATES ─────────────────────────────────► [VALIDATION-GATES-MODE-1]
│   │   All gates must PASS or emit structured error.
│   └───────────────────────────────────────────────────────────► fall through to step 11
│
└─► step 11: EMIT output ─────────────────────────────────────► [EMIT-MODE-1]
```

---

```
[MODE-2-PIPELINE]
│
│   Commands: /sql-embody, /sql-validate.
│   Constraint: ONE TABLE per invocation. Never process multiple tables.
│
├─► step 0: SCOPE CHECK + PARSE GATE
│   │   First: classify request against §Scope (same as Mode 1).
│   │
│   ├─► IF out-of-scope ───────────────────────────────────────► [ERROR: OUT_OF_SCOPE]
│   │
│   └─► ELSE (in-scope) → run parse gate on DDL/SQL input
│       │
│       ├─► IF syntactically invalid or structurally corrupt
│       │   │   Emit MALFORMED_INPUT.
│       │   │   Present correction table (up to 3 options,
│       │   │   same format as Mode 1 correction gate).
│       │   │   Halt until operator selects a correction.
│       │   │
│       │   ├─► IF operator selects correction ────────────────► fall through to step 1
│       │   │
│       │   └─► IF operator does not select ───────────────────► [STOP]
│       │
│       ├─► IF syntactically valid but semantically ambiguous
│       │   │   Missing constraints, incomplete keys, etc.
│       │   │   Log issues by name in decision_trace.
│       │   │   Continue — alert operator in final output.
│       │   └──────────────────────────────────────────────────► fall through to step 1
│       │
│       └─► ELSE (clean input) ────────────────────────────────► fall through to step 1
│
├─► step 1: EVIDENCE REFRESH ─────────────────────────────────► [EVIDENCE-REFRESH-LOOP]
│   │   Same loop as Mode 1. Returns here once Source 1 confirmed.
│   └───────────────────────────────────────────────────────────► fall through to step 2
│
├─► step 2: field_value_test — for EVERY source SQL field
│   │   Assign:
│   │     source_nullability (nullable | not_null)
│   │     source_type (string)
│   │     value_categories (≥1 from closed enum — see [FVG-ENUMS])
│   │     test_result (pass | fail | uncertain)
│   │     evidence (direct observation)
│   │     failure_reason (when fail) / uncertainty_reason (when uncertain)
│   └───────────────────────────────────────────────────────────► fall through to step 3
│
├─► step 3: Cursory semantic review — every field
│   │   Independent of field_value_test result.
│   │   Agent forms its own keep/remove/uncertain opinion.
│   └───────────────────────────────────────────────────────────► fall through to step 4
│
├─► step 4: field_review_matrix — compare cursory vs test
│   │   For each field, compute agreement_state:
│   │
│   ├─► agree_keep → recommend keep; operator_decision still required
│   │
│   ├─► agree_remove → add to proposed_removals (operator_decision = pending_review)
│   │
│   ├─► disagree → run detailed field review; add to disagreements
│   │
│   └─► both_uncertain → run detailed field review; add to disagreements
│   │
│   └───────────────────────────────────────────────────────────► fall through to step 5
│
├─► step 5: Field removal governance ─────────────────────────► [FIELD-VALUE-GOVERNANCE]
│   │   No field excluded from mirroring unless operator_decision = approved_remove.
│   └───────────────────────────────────────────────────────────► fall through to step 6
│
├─► step 6: TypeDB intent mapping — all retained fields
│   │   Map each field to one TypeDB primitive using Mode 1 tests:
│   │     entity, relation, role, attribute, ownership,
│   │     subtyping, inference, query pattern
│   │   Apply subtype/relation/attribute tests WHERE those
│   │   constructs are asserted. Evidence from Source 1 only.
│   └───────────────────────────────────────────────────────────► fall through to step 7
│
├─► step 7: Generate decision_trace
│   │   One entry per item, pipeline step order (same as Mode 1 step 8).
│   └───────────────────────────────────────────────────────────► fall through to step 8
│
├─► step 8: Generate SQL embodiment output
│   │   SQL Server-compatible CREATE TABLE + supporting constraints
│   │   that embody the TypeDB intent mapping from step 6.
│   └───────────────────────────────────────────────────────────► fall through to step 9
│
├─► step 9: ALIGNMENT CHECK
│   │   For every field: compare TypeDB construct (step 6) vs SQL construct (step 8).
│   │   Produce alignment_report table.
│   │
│   ├─► IF perfectly aligned
│   │   │   Note in report.
│   │   └──────────────────────────────────────────────────────► fall through to step 10
│   │
│   ├─► IF misaligned but workaround meets intent
│   │   │   Document misalignment + workaround in report.
│   │   └──────────────────────────────────────────────────────► fall through to step 10
│   │
│   └─► IF misaligned and NO workaround meets intent
│       └──────────────────────────────────────────────────────► [ERROR: ALIGNMENT_IMPOSSIBLE]
│
├─► step 10: VALIDATION GATES ────────────────────────────────► [VALIDATION-GATES-MODE-2]
│   │   All Mode 1 gates + Mode 2 additional gates.
│   └───────────────────────────────────────────────────────────► fall through to step 11
│
└─► step 11: EMIT output ────────────────────────────────────► [EMIT-MODE-2]
```

---

```
[EVIDENCE-REFRESH-LOOP]
│
│   Purpose: guarantee Source 1 contains the needed evidence before any
│   TypeDB decision proceeds. This loop runs every time evidence is needed.
│   Constraint: Sources 2 and 3 are REFRESH INPUTS ONLY — they seed
│   Source 1 via vectorization. Final decisions must cite Source 1.
│   Constraint: no source may be skipped; order is immutable.
│
├─► step 1: CHECK SOURCE 1 — vector retrieval
│   │   Tool: qdrant-find via user-directive-mcp-search.
│   │   Build query: task + TypeDB primitive terms + skill hints
│   │     (skill: ontology-tutor, routing_id_token, corpus_roots, domain terms).
│   │   ROUTER hints and situational YAML are NOT facts — never cite them.
│   │
│   ├─► IF chunks returned → apply CITEABILITY TEST
│   │   │
│   │   │   A chunk is citeable ONLY when BOTH hold:
│   │   │     (a) token count ≥ N, where N is justified in decision_trace
│   │   │         by citation to S1/S2/S3 stating a min chunk length threshold.
│   │   │         If no N can be justified → GATE_FAILED: source_1_chunk_threshold_unset
│   │   │     (b) chunk contains ≥1 TypeDB primitive term (entity, relation,
│   │   │         attribute, role, owns, plays, subtype, abstract, rule,
│   │   │         inference, TypeQL) OR a define/TypeQL keyword tied to
│   │   │         schema syntax in the same chunk.
│   │   │
│   │   ├─► IF ≥1 citeable chunk exists
│   │   │   │   Source 1 has the evidence. Record authority_source = source_1.
│   │   │   └──────────────────────────────────────────────────► [RETURN: Source 1 confirmed]
│   │   │
│   │   └─► ELSE (chunks returned but none citeable)
│   │       │   Source 1 insufficient.
│   │       └──────────────────────────────────────────────────► fall through to step 2
│   │
│   ├─► IF no chunks returned
│   │   │   Source 1 insufficient.
│   │   └──────────────────────────────────────────────────────► fall through to step 2
│   │
│   └─► IF citeability threshold N cannot be justified
│       └──────────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│           details: source_1_chunk_threshold_unset
│
├─► step 2: CHECK SOURCE 2 — snapshot filesystem
│   │   Tool: search_files, read_text_file via user-typedb-snapshot-mcp.
│   │   Execute phases 1–6 IN ORDER before declaring Source 2 exhausted.
│   │
│   │   Phase 1: Read _snapshot/manifest.yaml and docs_snapshot/manifest.yaml
│   │   Phase 2: Search exact user/domain terms (search_files)
│   │   Phase 3: Search TypeDB primitive terms:
│   │            entity, relation, attribute, role, owns, plays,
│   │            subtype, abstract, rule, inference, TypeQL
│   │   Phase 4: Search command-specific terms:
│   │            /schema:       define, owns, plays, relates, sub, value
│   │            /folders:      taxonomy, classification, hierarchy, folder, artifact
│   │            /validate:     schema, constraint, role player, attribute ownership
│   │            /lesson etc:   core concepts, example, guide, manual
│   │            /trace:        manifest, source_file, content_hash, provenance
│   │            /sql-*:        attribute, owns, relation, entity, cardinality, value
│   │            GENERAL:       matching primitives + user/domain terms
│   │   Phase 5: Read matched files (read_text_file) in priority order:
│   │            exact filename > schema files > docs with command terms > docs with primitives
│   │   Phase 6: Record in decision_trace:
│   │            probe_b_search_terms, probe_b_matched_paths,
│   │            probe_b_read_paths, probe_b_failure_reason
│   │
│   │   Source 2 criterion: read content names or defines the TypeDB
│   │   primitive/construct/constraint being classified, using ≥1 term
│   │   from the Phase 3 term list in the same passage.
│   │   Search-result paths without read content are NEVER sufficient.
│   │
│   ├─► IF snapshot server/root unavailable
│   │   │   Skip to Source 3 (phases incomplete is OK if server down).
│   │   └──────────────────────────────────────────────────────► fall through to step 3
│   │
│   ├─► IF phases 1–6 complete AND criterion met (evidence found)
│   │   │
│   │   └─► [REFRESH-SOURCE-1]
│   │       │   Append source path to ROUTER.yaml.
│   │       │   IF Source 2 found paths not in ROUTER → recommend ROUTER promotion:
│   │       │     add exact literals or tight globs, bump router_version, rerun loader.
│   │       │   Run vectorizer loader.
│   │       │
│   │       ├─► IF vectorizer did not execute
│   │       │   └──────────────────────────────────────────────► [ERROR: REFRESH_FAILED]
│   │       │       sub-code: VECTORIZER_UNAVAILABLE
│   │       │
│   │       ├─► IF vectorizer ran but Source 1 STILL lacks evidence
│   │       │   └──────────────────────────────────────────────► [ERROR: REFRESH_FAILED]
│   │       │       sub-code: SOURCE_NOT_INGESTED (hard stop)
│   │       │
│   │       └─► ELSE (vectorizer succeeded, Source 1 now has evidence)
│   │           │   authority_source = source_1+source_2
│   │           └──────────────────────────────────────────────► ↺ loop step 1 (recheck Source 1)
│   │
│   └─► ELSE (phases 1–6 complete, criterion NOT met — no evidence)
│       │   Source 2 exhausted.
│       └──────────────────────────────────────────────────────► fall through to step 3
│
├─► step 3: CHECK SOURCE 3 — typedb.com
│   │   Tool: read-only web search/fetch for typedb.com ONLY.
│   │   Log fallback in decision_trace.
│   │   Distinguish external docs from local snapshot evidence.
│   │
│   │   Source 3 criterion: page content names or defines the TypeDB
│   │   primitive/construct/constraint being classified.
│   │
│   ├─► IF typedb.com unavailable
│   │   │   Source 3 unavailable.
│   │   └──────────────────────────────────────────────────────► fall through to step 4
│   │
│   ├─► IF criterion met (evidence found)
│   │   │
│   │   └─► [REFRESH-SOURCE-1] (same procedure as Source 2 refresh)
│   │       │
│   │       ├─► IF vectorizer did not execute ─────────────────► [ERROR: REFRESH_FAILED]
│   │       │       sub-code: VECTORIZER_UNAVAILABLE
│   │       │
│   │       ├─► IF vectorizer ran but Source 1 STILL lacks ────► [ERROR: REFRESH_FAILED]
│   │       │       sub-code: SOURCE_NOT_INGESTED
│   │       │
│   │       └─► ELSE (success)
│   │           │   authority_source = source_1+source_3
│   │           └──────────────────────────────────────────────► ↺ loop step 1 (recheck Source 1)
│   │
│   └─► ELSE (no evidence found) ─────────────────────────────► fall through to step 4
│
└─► step 4: SOURCE 9 — HARD GATE
    │   All sources exhausted. Present this EXACT prompt to operator:
    │
    │   "No TypeDB evidence found from Sources 1–3. Source 9 (model-internal)
    │    knowledge is available for EXPLANATION ONLY — it is not actionable,
    │    not citable, and not authoritative for any classification, naming,
    │    hierarchy, or design decision. Proceed with explanation?"
    │
    ├─► IF operator approves
    │   │   Set authority_source = source_9, actionable = false.
    │   │   Source 9 output does NOT satisfy the evidence gate for design claims.
    │   └──────────────────────────────────────────────────────► [RETURN: Source 9 approved]
    │
    └─► IF operator declines
        └──────────────────────────────────────────────────────► [ERROR: EVIDENCE_EXHAUSTED]
```

---

```
[FIELD-VALUE-GOVERNANCE]
│
│   Purpose: control which fields are mirrored from legacy SQL into new schema.
│   Rule: the legacy SQL reference is READ-ONLY — never modified.
│   Rule: "removed_from_legacy" = excluded from mirroring, NOT deleted from legacy.
│
├─► For each field, check: does it provide ≥1 closed-category value?
│   │
│   │   Closed value_categories enum:
│   │     constraint_validated | code_validated | relationship_participant |
│   │     automation_driver | calculation_source | routing_or_status_driver |
│   │     reporting_or_filtering_value | operator_approved_descriptive_value |
│   │     migration_continuity
│   │
│   │   Nullability alone is NOT a removal criterion.
│   │   A nullable field that provides value stays.
│   │   A nullable field with no value should fail field_value_test,
│   │   but exclusion still requires operator approval.
│   │
│   ├─► IF field provides value → field stays (mirrors into new schema)
│   │
│   └─► IF field provides no value → field_value_test should = fail
│       │   Add to proposed_removals with operator_decision = pending_review.
│       │   Field is NOT excluded yet — pending operator decision.
│       │
│       └─► OPERATOR DECISION
│           │
│           ├─► approved_keep
│           │   │   Field remains. Receives tightest applicable SQL embodiment.
│           │   └──────────────────────────────────────────────► [FIELD STAYS]
│           │
│           ├─► approved_remove
│           │   │   Field may move to removed_from_legacy.
│           │   │   This is the ONLY path to exclusion.
│           │   └──────────────────────────────────────────────► [FIELD EXCLUDED]
│           │
│           ├─► rejected_remove
│           │   │   Field remains. Must receive keep rationale +
│           │   │   tightest applicable SQL embodiment.
│           │   └──────────────────────────────────────────────► [FIELD STAYS]
│           │
│           └─► pending_review
│               │   No removal may occur. Field remains outside removed_from_legacy.
│               └──────────────────────────────────────────────► [FIELD STAYS]
```

---

```
[VALIDATION-GATES-MODE-1]
│
│   All gates must PASS. Any FAIL → halt with structured error.
│   Gate names: Title-Case-With-Hyphens in prose, snake_case in YAML.
│
├─► Authority gate
│   │   authority_source must be from closed enum:
│   │   source_1 | source_1+source_2 | source_1+source_3 | source_9
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Read-only gate
│   │   Only approved read-only tools were used during normal execution.
│   │   Refresh-phase mutations confined to refresh phase only.
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Source X gate
│   │   No live typedb-mcp evidence used (database_list, database_schema, query)
│   │   unless operator explicitly overrode the skill.
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Closed-world gate
│   │   Every classification is in the allowed enum set.
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Evidence gate
│   │   Every non-UNKNOWN design claim has citation to Source 1
│   │   (may contain S2/S3 evidence via refresh).
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Hierarchy gate
│   │   Every subtype passes the subtype test (step 4).
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Relation gate
│   │   Every relation passes the relation test (step 5).
│   │   Also applies to relations asserted in Mode 2 TypeDB intent mapping.
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Naming gate
│   │   TypeQL identifiers use kebab-case unless cited source uses different literal.
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Trace completeness gate
│   │   Every emitted item appears in decision_trace.
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Source-gap gate
│   │   If Source 1 was insufficient: Source 2 phases 1–6 were
│   │   completed OR snapshot server/root was unavailable.
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
└─► Mode gate
    │   Active mode (1 or 2) recorded in output contract.
    │   If a validator required by the mode is unavailable → halt.
    ├─► PASS ──────────────────────────────────────────────────► [ALL GATES PASSED]
    └─► FAIL ──────────────────────────────────────────────────► [ERROR: VALIDATOR_INCOMPATIBLE]
```

---

```
[VALIDATION-GATES-MODE-2]
│
│   Runs ALL Mode 1 gates above PLUS these additional gates.
│
├─► (all Mode 1 gates — see [VALIDATION-GATES-MODE-1])
│   └───────────────────────────────────────────────────────────► fall through to Mode 2 gates
│
├─► Field coverage gate
│   │   Every source SQL field has a field_value_test entry
│   │   AND a field_review_matrix entry.
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Operator decision gate
│   │   Every field in field_review_matrix has non-null operator_decision.
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Removal approval gate
│   │   removed_from_legacy contains ONLY fields where
│   │   operator_decision = approved_remove.
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► No auto-removal gate
│   │   No field moved to removed_from_legacy without explicit
│   │   operator_decision = approved_remove in proposed_removals.
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
├─► Source 1 authority gate
│   │   TypeDB intent mapping cites Source 1 evidence ONLY.
│   │   (Refresh-only constraint — S2/S3 not cited directly.)
│   ├─► PASS ──────────────────────────────────────────────────► next gate
│   └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
│
└─► Alignment gate
    │   FAIL if alignment_report contains any ALIGNMENT_IMPOSSIBLE row.
    ├─► PASS ──────────────────────────────────────────────────► [ALL GATES PASSED]
    └─► FAIL ──────────────────────────────────────────────────► [ERROR: GATE_FAILED]
```

---

```
[EMIT-MODE-1]
│
│   Output format: YAML (default) or concise bullets/prose if operator requests.
│   Internal evidence order preserved regardless of output format.
│
│   Emit:
│     skill_id: ontology-tutor
│     command: <routed command>
│     mode: 1
│     authority_source: <from closed enum>
│     authority_probed_at: <ISO-8601 from step 5>
│     authority_plane: <which plane was probed — diagnostic, not decision>
│     router: { router_status, router_version }
│     content: <command-specific body>
│     decision_trace: [ { item, classification, canonical_reference,
│                         authority_source, rule_applied, probe_b_* } ]
│     validation: { all gate results = PASS }
│     menu: /learn /lesson /project /explain /schema /folders /validate
│           /trace /sql-embody /sql-validate
│
└───────────────────────────────────────────────────────────────► [DONE]
```

---

```
[EMIT-MODE-2]
│
│   Emits everything from [EMIT-MODE-1] PLUS these additional blocks:
│
│   sql_embodiment:
│     field_value_test:       [ per-field test results ]
│     field_review_matrix:    [ per-field agreement + operator_decision ]
│     proposed_removals:      [ fields proposed for exclusion ]
│     disagreements:          [ fields where cursory vs test disagree ]
│     removed_from_legacy:    [ ] — only approved_remove fields
│     alignment_report:       [ per-field TypeDB vs SQL alignment ]
│     sql_embodiment_validation:
│       field_coverage_gate, operator_decision_gate,
│       removal_approval_gate, no_auto_removal_gate,
│       source_1_authority_gate, alignment_gate = PASS
│
└───────────────────────────────────────────────────────────────► [DONE]
```

---

```
[ERROR-DISPATCH]
│
│   When the pipeline cannot complete, emit structured error YAML:
│     skill_id, command, mode, authority_source = NONE,
│     error: { code, message, details, recommended_action }, menu
│
├─► AUTHORITY_DOWN
│   │   Source 1, Source 2, and Source 3 are all unavailable.
│   └──────────────────────────────────────────────────────────► [HALT]
│
├─► EVIDENCE_EXHAUSTED
│   │   S1, S2, S3 attempted in order, none had evidence,
│   │   and Source 9 gate was declined by operator.
│   └──────────────────────────────────────────────────────────► [HALT]
│
├─► ROUTER_MISSING
│   │   ROUTER.yaml missing or unreadable.
│   │   (May still proceed if Source 1 MCP returns data.)
│   └──────────────────────────────────────────────────────────► [HALT or CONTINUE flagged]
│
├─► GATE_FAILED
│   │   A validation gate rejected the draft.
│   │   Includes source_1_chunk_threshold_unset when N not justified.
│   └──────────────────────────────────────────────────────────► [HALT]
│
├─► INSUFFICIENT_INPUT
│   │   Prompt omits required operand (domain/table/schema body).
│   └──────────────────────────────────────────────────────────► [HALT]
│
├─► OUT_OF_SCOPE
│   │   Request outside this skill.
│   │   recommended_action → alternative skill name or operator-alert.
│   └──────────────────────────────────────────────────────────► [HALT]
│
├─► VALIDATOR_INCOMPATIBLE
│   │   Active mode requires a validator that can't accept that mode.
│   └──────────────────────────────────────────────────────────► [HALT]
│
├─► MODE_REQUIRED
│   │   Mode 2 command invoked but mode = 1 (default).
│   │   Prompt operator to declare mode = 2.
│   └──────────────────────────────────────────────────────────► [HALT]
│
├─► REFRESH_FAILED
│   │   Sub-codes:
│   │     VECTORIZER_UNAVAILABLE — vectorizer did not execute.
│   │     SOURCE_NOT_INGESTED — vectorizer ran but Source 1 still empty.
│   └──────────────────────────────────────────────────────────► [HALT]
│
├─► ALIGNMENT_IMPOSSIBLE
│   │   Mode 2 field can't align to SQL and no workaround exists.
│   │   Alert operator to discuss alternative.
│   └──────────────────────────────────────────────────────────► [HALT]
│
└─► MALFORMED_INPUT
    │   DDL/SQL (Mode 2) or TypeQL (Mode 1) is syntactically invalid.
    │   Present correction table (up to 3 options), halt until selected.
    └──────────────────────────────────────────────────────────► [HALT until correction selected]
```

---

```
[MAINTAINER-WORKFLOW]
│
│   Trigger: Source 2 finds useful guidance not already in vectors.
│   This is a maintenance-time procedure, not part of the runtime pipeline.
│
├─► step 1: Record snapshot-relative path of the useful content
│
├─► step 2: Classify path as exact literal OR tight parent glob
│   │   Per ROUTER.yaml schema for vector_source_file_registry entries.
│
├─► step 3: Add to ROUTER.yaml under vector_source_file_registry
│   │   UTF-8 lexicographic order.
│
├─► step 4: Bump router_version
│
├─► step 5: Run vectorizer loader
│   │   Path from ROUTER.yaml vector_ingest bindings.
│   │   Pass --ontology-router <ROUTER.yaml>.
│   │   Default: incremental hash dedup (SHA-256 of pre-banner body bytes).
│   │   Cache key: body_text, NOT bannered text.
│   │   Banners embedded for search context but not hashed.
│   │
│   ├─► IF metadata stamps need refresh or incremental repair insufficient
│   │   │   Use --rebuild (opt-in).
│   │   └──────────────────────────────────────────────────────► fall through to step 6
│   │
│   └─► ELSE (default incremental) ───────────────────────────► fall through to step 6
│
├─► step 6: Verify with --strict-mcp --verify-router-qdrant
│   │   Qdrant verify compares (source_file, chunk_index, content_hash).
│
└─► step 7: (optional) Chunk caps: --max-chunks-per-file, --max-total-chunks
    └──────────────────────────────────────────────────────────► [DONE]
```

---

```
[ANTI-DRIFT RULES] — constraints that apply across the entire tree
│
│   These are NOT sequential steps. They are invariants.
│   If any rule is violated at any point, the pipeline must halt.
│
│    1. No live typedb-mcp (Source X) as tutor authority.
│    2. ROUTER hints and archived references are NOT evidence.
│    3. Never stop after weak vector search — follow full evidence pipeline.
│    4. Never stop Source 2 until phases 1–6 complete or server unavailable.
│    5. No non-router ingest scopes in tutor vector corpus.
│    6. Banner/metadata changes must not become source-content cache keys.
│    7. Never collapse UNKNOWN into a guess.
│    8. Same evidence + same input = same classification + same trace order.
│    9. No hardcoded deployment paths/URLs/collections in SKILL.md — ROUTER.yaml only.
│   10. No field excluded from mirroring without operator approval.
│   11. S2 and S3 are refresh inputs only — never cite directly for design decisions.
│   12. Wrong validator for active mode → halt VALIDATOR_INCOMPATIBLE.
│   13. Mode 2 execution must not silently weaken Mode 1 behavior.
│   14. No synonym for "sufficient/adequate/enough/directly supports" as evidence
│       criteria. Only "contains the needed evidence" per §Transition Criteria.
│
└──────────────────────────────────────────────────────────────► [INVARIANT — always enforced]
```

---

## Topology Summary

```
[START]
  └─► [ACTIVATE]
        ├─► steps 1–5 (read, ROUTER, mode, command, timestamp)
        └─► [MODE-DISPATCH]
              ├─► [MODE-1-PIPELINE]
              │     ├─► step 0: scope check
              │     ├─► step 1 → [EVIDENCE-REFRESH-LOOP]
              │     │               ├─► Source 1 (qdrant-find + citeability)
              │     │               ├─► Source 2 (snapshot phases 1–6 → refresh S1)
              │     │               ├─► Source 3 (typedb.com → refresh S1)
              │     │               └─► Source 9 (hard gate → operator approve/decline)
              │     ├─► steps 2–7: classify (subtype/relation/attribute/evidence-gap)
              │     ├─► step 8: decision_trace
              │     ├─► step 9: content body (+ correction gate if malformed)
              │     ├─► step 10 → [VALIDATION-GATES-MODE-1] (11 gates)
              │     └─► step 11 → [EMIT-MODE-1]
              │
              └─► [MODE-2-PIPELINE]
                    ├─► step 0: scope check + parse gate
                    ├─► step 1 → [EVIDENCE-REFRESH-LOOP] (same as Mode 1)
                    ├─► steps 2–4: field_value_test → cursory review → field_review_matrix
                    ├─► step 5 → [FIELD-VALUE-GOVERNANCE] (operator_decision workflow)
                    ├─► step 6: TypeDB intent mapping (uses Mode 1 tests)
                    ├─► step 7: decision_trace
                    ├─► step 8: SQL embodiment output
                    ├─► step 9: alignment check
                    ├─► step 10 → [VALIDATION-GATES-MODE-2] (11 + 6 gates)
                    └─► step 11 → [EMIT-MODE-2]

Any branch → [ERROR-DISPATCH] when halting conditions are met.
[MAINTAINER-WORKFLOW] runs offline when Source 2 finds unvectorized content.
[ANTI-DRIFT RULES] enforced as invariants across all branches.
```
