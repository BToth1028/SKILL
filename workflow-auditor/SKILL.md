---
name: workflow-auditor
description: >
  Deterministic audit engine that stress-tests agent workflows before deployment.
  Evaluates any workflow document (YAML prompts, SKILL.md files, markdown runbooks,
  mixed-format instructions) across 8 layers: determinism, reference integrity,
  outcome achievability, completeness, internal consistency, scope coherence, agent
  executability, and structural quality. Produces scored reports with tier ratings
  (A–F) and prioritized findings. Triggers on: audit workflow, review prompt,
  stress-test, check workflow, "is this solid", "will this break", workflow
  validation, pre-flight check, "find the holes", "what did I miss", workflow
  scoring, post-mortem, "why did this fail", agent failure analysis, sanity check,
  dry run, compare workflow versions, or frustration about a workflow failing.
  Audits only — never modifies. When in doubt, trigger.
---

# Workflow Auditor

## Mission

Systematically evaluate any agent workflow document for structural soundness,
internal consistency, and real-world executability — surfacing every failure mode
BEFORE the user discovers it in production.

**This skill audits workflows. It does not build or modify them.**

Findings that require workflow reconstruction route to `deterministic-prompt-builder`
for YAML prompts or to the user for other formats. This skill's outputs are audit
reports and finding queues — not revised workflows.

### Before Your First Audit

Read `references/example-audit.yaml` before producing any Mode 1–4 audit report.
It contains a complete worked example with calibration notes for severity
assignment, finding granularity, and scoring. This is not optional —
uncalibrated audits produce inconsistent results.

For **Mode 5 (Iterative) audits**, also read `references/example-audit-mode5.yaml`.
It calibrates pass numbering, cross-pass deduplication, atomic-clause coverage at
Step M5-9, plan-item ordering with `locked` semantics, and `prompt_builder_substeps`
routing. Mode 5 audits without Mode 5 calibration produce inconsistent iteration
logs and plan reviews.

---

## Authority Model

**Canonical (ground truth):**
- The workflow document being audited (as provided by the user).
- The user's stated intent for the workflow (what it's supposed to accomplish).

**Derived (rebuildable from canonical):**
- Audit report, layer scores, tier rating, finding classifications, routing queues.

**Rule:** Never modify the workflow under audit. Never assume intent the user has
not stated. If the workflow's purpose is ambiguous, halt and ask before auditing —
an audit without a known target is meaningless.

---

## Scope / Non-Scope

**In scope:** Running the 8-layer audit framework. Scoring each layer. Producing
an overall tier rating. Classifying findings by severity. Routing findings to
appropriate remediation paths. Comparing two workflow versions. Post-mortem
analysis of a workflow that failed in production.

**Never:** Rewrite the workflow. Fix findings directly. Author new prompts or
skills. Make domain truth judgments about the workflow's subject matter. Skip
audit layers. Emit a passing score to avoid confrontation — if it's broken, say
so. Operate without a workflow document loaded.

---

## Session Modes

### Mode 1 — Full Audit
Run all 8 audit layers in order. All layers execute; none are optional. Emit a
complete audit report with per-layer scores and an overall tier rating.

**Trigger:** "audit this workflow", "full review", or any request without a
narrower scope specified.

### Mode 2 — Targeted Audit
Run a specific subset of layers (user-specified). All questions within selected
layers still execute — no partial layers. Emit a scoped audit report.

**Trigger:** "just check the references", "is this deterministic", or any request
that names specific audit dimensions.

### Mode 3 — Post-Mortem
The workflow has already failed in production. The user provides the workflow AND
a description of the failure. Run all 8 layers, but additionally trace the failure
back to specific audit findings. Emit a post-mortem report with root cause mapping.

**Trigger:** "why did this fail", "post-mortem", "what went wrong", or any request
that includes both a workflow and a failure description.

### Mode 4 — Diff Audit
Compare two versions of a workflow. Run all 8 layers against both. Emit a
comparative report showing which version scores higher on each dimension and
whether the changes introduced regressions.

**Trigger:** "compare these two versions", "is the new one better", or any
request that provides two workflow documents.

### Mode 5 — Iterative Audit
Wrap Mode 1 (FULL — default), Mode 3 (POST_MORTEM), or Mode 4 (DIFF) in a
multi-pass loop with explicit user gates. Each pass runs **all 8 audit layers**
against the workflow. Findings persist across passes. The loop exits **only
after two consecutive clean passes** (zero findings in two passes in a row),
guarding against a single false-clean.

Mode 5 produces the standard `audit_report` PLUS a `remediation_plan` section.
The plan is **proposal-only** — Mode 5 never executes it. A separate agent in a
separate session is the executor (see Anti-Drift Safeguards §7 and Companion
Skills `deterministic-prompt-builder` substep).

Modes 1, 2, 3, 4 remain unchanged and are still available single-pass.

**Trigger:** "audit iteratively", "iterative audit", "loop until clean", "loop
this audit", "exhaustive audit with plan", or any request that combines audit
work with a remediation plan handed off to a follow-up session.

---

## STEP 0 — Pre-Audit Setup

Before any audit work begins:

```
1. Confirm the workflow document is loaded and readable.
   - If not provided → HALT. Request workflow.
   - If provided as a file path → read the file.
   - If provided inline → capture it.

2. Generate audit_id using format WFA-YYYYMMDD-HHMMSS from current timestamp.

3. Identify the workflow format:
   - YAML_PROMPT: Structured YAML following deterministic-prompt-builder spec
   - SKILL_MD: Skill file with YAML frontmatter + markdown body
   - MARKDOWN_RUNBOOK: Markdown instructions without YAML structure
   - MIXED: Combination of formats
   - FREEFORM: Unstructured prose instructions
   → Record as `workflow_format` in the audit report.

4. Confirm the workflow's stated intent:
   - Extract the mission/objective/purpose statement if present.
   - If no mission statement exists → ask the user: "What is this workflow
     supposed to accomplish?" Do not proceed without this.
   → Record as `stated_intent`.

5. Confirm session mode (Full / Targeted / Post-Mortem / Diff).

6. If Post-Mortem → collect failure description from user.
   If Diff → confirm both versions are loaded.

7. Viability gate: IF the document contains no instructions, no steps, and no
   recognizable structure (no headings, no numbered items, no conditional logic)
   → HALT with finding NOT_A_WORKFLOW. Do not proceed to Layer 1.
```

---

## Audit Framework — 8 Layers

Layers execute in order 1 → 8. Each layer produces a score (0–100) and a list
of findings. A layer with zero findings scores 100. Scoring methodology is
defined per layer.

### Per-Check Error Protocol

Every check produces one of: PASS, FAIL, PARTIAL, or SKIPPED.

```
per_check_error_handling:
  PARTIAL:
    trigger: "Check cannot produce a definitive PASS or FAIL"
    action: >
      Record result as PARTIAL. Include both possible interpretations in
      the finding record. Weight as 0.5 in layer scoring (half credit).
    required_fields: "Both interpretations must appear in finding.evidence"

  SKIPPED:
    trigger: "Check is inapplicable to the workflow format"
    action: >
      Record result as SKIPPED. Exclude from layer score denominator
      (do not penalize for inapplicable checks). Note reason in
      finding.description.
    example: "YAML structure checks are SKIPPED for FREEFORM workflows"
```

### Layer-Failure Protocol

If a layer cannot complete (corrupted content, unreadable section, agent
uncertainty on all checks):

```
layer_failure:
  action:
    - Record layer score as INCOMPLETE (not 0, not estimated)
    - Continue to next layer — do not halt the full audit
    - Set audit_report.overall.tier_overrides to include:
        condition: "Layer [ID] could not complete"
        cap: "C"
        reason: "Incomplete layer — audit results are partial"
    - Record in decision_trace.auditor_notes: which layer failed and why
  rule: "An incomplete layer is better than a halted audit."
```

---

### Layer 1 — Determinism (L1-DET)
*Given identical inputs, will this workflow produce identical outputs every time?*

| ID | Check | What Fails It |
|----|-------|---------------|
| 1.1 | **Ambiguous verb scan** | Presence of: consider, try, attempt, explore, think about, look into, might, perhaps, maybe, could, should consider, various, some, several, a few, many, often |
| 1.2 | **Open enumeration scan** | Presence of: etc., such as, for example, including but not limited to, and more, among others, and similar, like (as a list opener), things like |
| 1.3 | **Ordering stability** | Any list or output sequence without an explicit sort key and direction |
| 1.4 | **Conditional completeness** | Any IF without an ELSE or explicit default. Any branching logic without exhaustive case coverage |
| 1.5 | **Implicit discretion** | Instructions that rely on agent judgment without defined criteria: "use your best judgment", "as appropriate", "when relevant", "if necessary" |
| 1.6 | **Reproducibility test** | Could two different agents reading this workflow independently arrive at different outputs for the same input? If yes → FAIL |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

---

### Layer 2 — Reference Integrity (L2-REF)
*Do all references in this workflow point to things that actually exist?*

| ID | Check | What Fails It |
|----|-------|---------------|
| 2.1 | **File path validation** | Any referenced file path that cannot be verified as existent or is not qualified (relative paths without a base) |
| 2.2 | **Cross-reference validation** | References to other skills, prompts, or documents that are not identified by a concrete locator (name, path, ID) |
| 2.3 | **Tool/capability references** | References to tools, APIs, or capabilities that the executing agent may not have access to |
| 2.4 | **Schema references** | References to data schemas, field names, or structures that are not defined within the workflow or a cited source |
| 2.5 | **Stale marker scan** | References that include version numbers, dates, or identifiers that may have changed since authoring |
| 2.6 | **Circular reference check** | Any reference chain that loops back to itself (A → B → C → A) |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

**Note on verification limits:** The auditor cannot always confirm that an external
file or tool exists — it flags references it *cannot verify* rather than asserting
they are broken. Findings in this layer use severity UNVERIFIABLE when existence
cannot be confirmed, and BROKEN when absence can be confirmed.

---

### Layer 3 — Outcome Achievability (L3-OUT)
*Can the stated mission actually be accomplished by following the defined steps?*

| ID | Check | What Fails It |
|----|-------|---------------|
| 3.1 | **Mission-to-steps coverage** | The stated intent requires actions that no step in the workflow addresses |
| 3.2 | **Step output chain** | A step requires input that no prior step produces (broken data flow) |
| 3.3 | **Terminal state reachability** | The workflow has no defined end state, or the end state cannot be reached via the defined steps |
| 3.4 | **Precondition satisfaction** | A step has preconditions that are never guaranteed by prior steps |
| 3.5 | **Output contract fulfillment** | The final output (if defined) requires fields or data that the workflow never generates |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 5) × 100.

---

### Layer 4 — Completeness (L4-CMP)
*Are all paths, errors, and edge cases handled?*

| ID | Check | What Fails It |
|----|-------|---------------|
| 4.1 | **Error handling coverage** | Any step that can fail but has no on_failure, fallback, or error path defined |
| 4.2 | **Edge case coverage** | Workflow does not address one or more of the following mandatory edge case categories: (1) empty/null input, (2) malformed/corrupt input, (3) boundary values (min/max/zero), (4) wrong-type input, (5) maximum-size input, (6) minimal-size input, (7) input with missing required fields, (8) input that exactly matches a boundary condition. Check each category; FAIL if ≥1 unaddressed. |
| 4.3 | **Branch exhaustiveness** | Decision points that do not cover all reachable cases |
| 4.4 | **Scope boundary handling** | No defined behavior for inputs or requests that fall outside the workflow's stated scope |
| 4.5 | **Graceful degradation** | No defined behavior for partial failures — one of several data sources unavailable, a referenced file missing, a tool returning an error instead of data |
| 4.6 | **Exit conditions** | No defined mechanism for the agent to halt, escalate, or abort when stuck |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

---

### Layer 5 — Internal Consistency (L5-CON)
*Does the workflow contradict itself?*

| ID | Check | What Fails It |
|----|-------|---------------|
| 5.1 | **Gate-state alignment** | A validation gate checks for a format or condition that a prior step has already transformed — validating lowercase after a step that uppercases, checking for nulls after a step that provides defaults |
| 5.2 | **Example compliance** | Provided examples (positive, negative, edge) that would fail the workflow's own validation rules |
| 5.3 | **Scope-algorithm alignment** | The algorithm contains steps that fall outside declared scope, or the scope declares capabilities the algorithm never exercises |
| 5.4 | **Definition consistency** | A term is defined differently in two places within the workflow |
| 5.5 | **Authority conflict** | Multiple canonical sources declared, or derived data treated as canonical |
| 5.6 | **Constraint contradiction** | Two rules that cannot both be satisfied simultaneously |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

---

### Layer 6 — Scope Coherence (L6-SCP)
*Does the workflow stay in its lane?*

| ID | Check | What Fails It |
|----|-------|---------------|
| 6.1 | **Scope declaration exists** | No explicit in-scope / out-of-scope / never lists |
| 6.2 | **Scope specificity** | Scope declarations so broad they impose no real constraint ("handles all user requests") |
| 6.3 | **Drift surface area** | Number of points where the agent could plausibly be prompted to leave scope, with no guardrails defined |
| 6.4 | **Anti-drift mechanisms** | No explicit drift prevention (identity anchors, refusal templates, scope-check steps) |
| 6.5 | **Companion routing** | Workflow does not define where out-of-scope requests should be routed |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 5) × 100.

---

### Layer 7 — Agent Executability (L7-EXE)
*Can the intended executor actually do what this workflow demands?*

| ID | Check | What Fails It |
|----|-------|---------------|
| 7.1 | **Context window feasibility** | Estimate total token count: workflow + all referenced files + expected average input. PASS if <80K tokens. PARTIAL if 80K–150K tokens. FAIL if >150K tokens. If token count cannot be estimated, record as PARTIAL with note. |
| 7.2 | **Tool availability assumptions** | The workflow assumes tools (web search, file I/O, code execution, MCP servers) without verifying availability |
| 7.3 | **Permission assumptions** | The workflow assumes permissions (file write, API access, network access) that may not be granted |
| 7.4 | **Multi-turn state assumptions** | The workflow assumes the agent retains state across turns or sessions without defining a persistence mechanism |
| 7.5 | **Cognitive load assessment** | Count concurrent state items the agent must track (open loops, pending conditions, deferred actions, active variables, unresolved branches). PASS if ≤5 concurrent state items. PARTIAL if 6–10. FAIL if >10. |
| 7.6 | **Instruction clarity for zero-context agent** | Could an agent with NO prior context on this project execute this workflow? If it requires implicit knowledge, it fails |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 6) × 100.

---

### Layer 8 — Structural Quality (L8-STR)
*Is the workflow well-organized, navigable, and maintainable?*

| ID | Check | What Fails It |
|----|-------|---------------|
| 8.1 | **Progressive disclosure** | All information frontloaded with no hierarchy; no clear "read this first, reference that later" structure |
| 8.2 | **Section organization** | Related instructions scattered across non-adjacent sections |
| 8.3 | **Redundancy** | Same instruction stated in multiple places (maintenance risk — they will diverge) |
| 8.4 | **Length proportionality** | Workflow length is disproportionate to task complexity (either bloated or underspecified) |
| 8.5 | **Naming clarity** | Section names, step names, or variable names that don't clearly communicate purpose |

**Scoring:** Each check is weighted equally. Score = (checks_passed / 5) × 100.

---

## Scoring and Tier Rating

### Layer Scores
Each layer produces a score from 0 to 100 as defined above.

### Overall Score
Weighted average of all 8 layer scores:

```
Layer weights:
  L1-DET (Determinism):          0.20    # Highest — foundational
  L2-REF (Reference Integrity):  0.15
  L3-OUT (Outcome Achievability): 0.15
  L4-CMP (Completeness):         0.15
  L5-CON (Internal Consistency):  0.15
  L6-SCP (Scope Coherence):       0.08
  L7-EXE (Agent Executability):   0.07
  L8-STR (Structural Quality):    0.05
                                 -----
                                  1.00
```

### Tier Rating
```
TIER_MAP:
  A:  90–100   # Production-ready. Minor advisory findings only.
  B:  75–89    # Deployable with known risks. No critical findings.
  C:  60–74    # Needs work. One or more layers have serious gaps.
  D:  40–59    # Significant rework required. Multiple critical findings.
  F:  0–39     # Not deployable. Fundamental structural problems.
```

### Automatic Tier Overrides
Regardless of overall score, the tier is capped:
```
overrides:
  - condition: "Layer 1 (Determinism) has ≥ 2 FAILed checks (i.e. ≥ 2 of the 6 L1 checks scored 0 individually)"
    cap: "D"
    reason: "Non-deterministic workflows are fundamentally unreliable. A single FAILed L1 check is a serious finding but may be local; two or more constitute systemic non-determinism."
    # NOTE: the threshold is at the *check* level (count of L1 checks with result=FAIL),
    # not at the layer aggregate level. PARTIAL counts as 0.5 and does NOT count toward
    # the FAIL count. SKIPPED is excluded entirely.

  - condition: "Layer 3 (Outcome Achievability) score < 40"
    cap: "D"
    reason: "Workflow cannot achieve its stated purpose"

  - condition: "Any CRITICAL severity finding exists"
    cap: "C"
    reason: "Critical findings must be resolved before deployment"

  - condition: "Layer 5 (Internal Consistency) has any contradiction finding"
    cap: "C"
    reason: "Self-contradicting workflows produce unpredictable behavior"
```

---

## Output Contract

### Audit Report

```yaml
audit_report:
  audit_id:           [string]        # Unique ID: WFA-YYYYMMDD-HHMMSS
  mode:               [enum]          # FULL | TARGETED | POST_MORTEM | DIFF
  workflow_format:    [enum]          # YAML_PROMPT | SKILL_MD | MARKDOWN_RUNBOOK | MIXED | FREEFORM
  stated_intent:      [string]        # User-confirmed mission statement
  executed_at:        [timestamp]     # ISO 8601

  overall:
    score:            [integer]       # 0–100 weighted average
    tier:             [enum]          # A | B | C | D | F
    tier_overrides:   [list<override> | null]  # Any overrides that capped the tier
    verdict:          [string]        # One-sentence summary

  layers:
    - layer_id:       [string]        # e.g., "L1-DET"
      layer_name:     [string]        # e.g., "Determinism"
      score:          [integer]       # 0–100
      weight:         [float]         # Weight used in overall calculation
      checks:
        - check_id:   [string]        # e.g., "1.1"
          check_name: [string]
          result:     [PASS | FAIL | PARTIAL | SKIPPED]
          findings:   [list<finding>]

  finding_summary:
    total:            [integer]
    by_severity:
      CRITICAL:       [integer]
      MAJOR:          [integer]
      MINOR:          [integer]
      ADVISORY:       [integer]
    by_layer:         [map<layer_id, integer>]

  finding_queue:      [list<finding>]   # All findings, sorted by severity then layer order

  routing:
    prompt_builder_queue:   [list<string>]  # Finding IDs routable to deterministic-prompt-builder
    user_action_queue:      [list<string>]  # Findings requiring user decisions
    informational:          [list<string>]  # Advisory findings, no action required

  # POST_MORTEM mode only:
  root_cause:
    failure_description:    [string | null]
    mapped_findings:        [list<string>]  # Finding IDs that explain the failure
    unmapped_factors:       [list<string>]  # Failure aspects not explained by audit findings
    confidence:             [enum]          # HIGH | MEDIUM | LOW

  decision_trace:
    mode_selected:          [string]        # Why this mode was chosen
    layers_executed:        [list<string>]
    overrides_applied:      [list<string>]
    auditor_notes:          [list<string>]  # Anything the auditor flagged for transparency
```

### Finding Record

```yaml
finding:
  finding_id:         [string]        # F-<layer_id>-<sequence>
  check_id:           [string]        # Which check surfaced this
  layer_id:           [string]
  severity:           [enum]          # CRITICAL | MAJOR | MINOR | ADVISORY
  category:           [enum]          # AMBIGUITY | BROKEN_REF | STALE_REF | UNREACHABLE |
                                      # UNHANDLED | CONTRADICTION | SCOPE_LEAK | ASSUMPTION |
                                      # REDUNDANCY | STRUCTURAL | UNVERIFIABLE
  location:           [string]        # Where in the workflow (section, line, step number)
  description:        [string]        # What the problem is
  evidence:           [string]        # The specific text or structure that triggered the finding
  impact:             [string]        # What goes wrong if this isn't fixed
  remediation:        [string]        # Concrete fix recommendation
  routing:            [enum]          # PROMPT_BUILDER | USER_ACTION | INFORMATIONAL
  pass_number:        [integer | null]   # Mode 5 only — pass on which finding first surfaced
```

### Output Contract additions (Mode 5 — Iterative Audit)

In Mode 5, two additional blocks are populated on the existing `audit_report`.
In Modes 1–4 these blocks MUST be `null`.

```yaml
audit_report:
  # ... all existing fields unchanged ...

  iteration:                              # Mode 5 only; null otherwise
    enabled:                [bool]
    base_mode:              [enum]        # FULL | POST_MORTEM | DIFF — the mode the loop wraps
    pass_count:             [integer]     # Total passes executed (including incomplete)
    pass_budget:            [integer]     # Max passes allowed; default 10. Enforced by ITERATION_BUDGET_EXHAUSTED
    clean_passes:           [integer]     # Consecutive clean passes at exit (must be 2 for normal exit)
    intent_approved_at_pass: [integer]    # Pass on which user approved the Workflow Intent
    bootstrap_scratchpad_id: [string]     # Stable ID of the scratchpad section in
                                          # context-bootstrap holding externalized Mode 5
                                          # state across passes. See "Mode 5 state externalization"
                                          # in the procedure section.
    halt_reason:            [enum | null] # null on normal exit; otherwise:
                                          # INTENT_NOT_APPROVED | INTENT_DRIFT |
                                          # PLAN_REVISION_EXHAUSTED | USER_HALT |
                                          # GRANULAR_PASS_FAILURE | USER_TIMEOUT |
                                          # DEDUP_FAILURE | ITERATION_BUDGET_EXHAUSTED
    iteration_log:                        # Per-pass record
      - pass_number:        [integer]
        started_at:         [timestamp]
        ended_at:           [timestamp]
        findings_count:     [integer]
        new_findings_count: [integer]     # Excludes deduped duplicates of prior findings
        pass_status:        [enum]        # COMPLETE | INCOMPLETE
        notes:              [string | null]

  remediation_plan:                       # Mode 5 only; null otherwise
    intent_anchor:          [string]      # The user-approved Workflow Intent (immutable within run)
    items:
      - plan_id:            [string]      # P-<sequence>
        finding_ids:        [list<string>]   # Findings this item resolves
        action:             [enum]        # ADD | REMOVE | UPDATE | REPLACE | SPLIT | MERGE
        target:             [string]      # Section / step / line range in workflow
        change:             [string]      # Concrete change description (proposal text).
                                          # MUST be ≤ 60 words AND describe action+target only.
                                          # MUST NOT contain a full re-authored section, full
                                          # replacement YAML/markdown body, or complete prose
                                          # paragraphs intended for verbatim insertion.
                                          # Long-form rewrites: route via routing=PROMPT_BUILDER
                                          # and reference under prompt_builder_substeps;
                                          # the executor session generates the new text.
        severity:           [enum]        # Inherited from highest-severity finding it resolves
        routing:             [enum]        # PROMPT_BUILDER | USER_ACTION | INFORMATIONAL
        depends_on:         [list<string>]   # Other plan_ids that must precede this one
        locked:             [bool]        # PARTIAL-approval persistence flag.
                                          # false on plan creation; flipped to
                                          # true at Step M5-10 when the user
                                          # accepts this specific plan item
                                          # under user_approval.status = PARTIAL.
                                          # When a re-audit runs after PARTIAL,
                                          # findings already resolved by a
                                          # locked item are excluded from
                                          # subsequent passes (see Step M5-10).
    ordering_rule:          "Severity-first (CRITICAL → ADVISORY), then layer order, then dependency topological order."
    prompt_builder_substeps:              # Items routable to deterministic-prompt-builder
      - plan_id:            [string]
        rationale:          [string]
    plan_review:
      satisfies_intent:     [bool]        # Computed in Step M5-9 by atomic-clause coverage
      revision_rounds:      [integer]     # 0–3
      gaps_if_unsatisfied:  [list<string>]   # Verbatim clauses with zero coverage; empty iff satisfies_intent == true
      intent_clauses:       [list<string>]   # Step M5-9.1 output: atomic clauses split from intent_anchor (1–5 items)
      clause_coverage:                       # Step M5-9.2 output: map<clause, coverage>
        - clause:                  [string]
          plan_item_ids:           [list<string>]      # remediation_plan.items[].plan_id values that cover this clause
          existing_step_locations: [list<string>]      # workflow-under-audit locations that already satisfy this clause
    user_approval:
      status:               [enum]        # PENDING | APPROVED | REJECTED | PARTIAL
      rationale:            [string | null]
      decided_at:           [timestamp | null]
```

---

## Finding Severity Definitions

```yaml
severity_definitions:
  CRITICAL:
    IS: >
      The workflow will produce wrong results, crash, or enter an unrecoverable
      state. Deployment at this level risks wasted hours or corrupted outputs.
    IS_NOT: "A style preference. A theoretical concern. An optimization opportunity."
    examples:
      - "Step 3 requires output from Step 5 (impossible ordering)"
      - "The only error handler routes to a nonexistent skill"
      - "Two rules contradict: one says HALT, the other says CONTINUE for the same condition"

  MAJOR:
    IS: >
      The workflow will produce unreliable, inconsistent, or incomplete results
      under plausible real-world conditions. Not every run will fail, but enough
      will to erode trust.
    IS_NOT: "A guaranteed failure. A minor style issue."
    examples:
      - "No error handling for the most likely failure mode"
      - "Agent judgment relied on without criteria in a high-frequency path"
      - "Reference to a tool that may or may not be available"

  MINOR:
    IS: >
      The workflow will usually work, but has rough edges that increase fragility,
      reduce maintainability, or cause occasional unexpected behavior.
    IS_NOT: "A deployment blocker. A cosmetic issue."
    examples:
      - "An open enumeration ('such as X, Y, Z') in a low-stakes context"
      - "Redundant instructions in two sections (will diverge over time)"
      - "Scope defined but no anti-drift mechanisms present"

  ADVISORY:
    IS: >
      A recommendation for improvement. The workflow functions correctly without
      this change, but would be better with it.
    IS_NOT: "A problem. A finding that requires action."
    examples:
      - "Section headings could be more descriptive"
      - "Workflow is longer than necessary for its complexity"
      - "Could benefit from more examples"
```

---

## Edge Cases

```yaml
edge_cases:
  empty_document:
    condition: "Workflow has frontmatter but no body, or body has no instructions"
    action: "HALT at Step 0 viability gate. Emit finding NOT_A_WORKFLOW."

  oversized_document:
    condition: "Workflow exceeds 3,000 lines or estimated 100K tokens"
    action: >
      Proceed with audit but add ADVISORY finding in L8-STR noting size.
      If token count risks context window overflow during audit, split into
      two passes: Layers 1–4 first, then Layers 5–8 with findings summary
      from the first pass carried forward.

  non_english_workflow:
    condition: "Workflow is written in a language other than English"
    action: >
      Proceed with audit. Checks 1.1 (ambiguous verb scan) and 1.2 (open
      enumeration scan) use English-language markers only — SKIP these
      checks and note language limitation. All structural checks (Layers
      2–8) apply regardless of language.

  self_referential_workflow:
    condition: "Workflow references itself (an auditor skill auditing itself)"
    action: >
      Proceed normally. The audit evaluates structural quality, not domain
      recursion. Note in decision_trace.auditor_notes that the workflow is
      self-referential.

  minimal_prose_only:
    condition: "Workflow is a single paragraph or short block of prose"
    action: >
      Record format as FREEFORM. Many checks will produce PARTIAL or FAIL
      due to lack of structure. This is expected — the score reflects the
      workflow's actual quality, not a format penalty.

  syntax_errors:
    condition: "YAML frontmatter has syntax errors, or markdown is malformed"
    action: >
      Record a CRITICAL finding in L2-REF. If the workflow is still
      readable despite syntax errors, proceed with audit on the readable
      portions. If unreadable, invoke layer-failure protocol.

  workflow_with_no_stated_purpose:
    condition: "No mission/objective found AND user declines to provide one"
    action: >
      HALT. An audit without a target cannot evaluate outcome achievability
      (Layer 3). Record in decision_trace and exit cleanly.
```

---

## Error Policy

| Condition | Action |
|-----------|--------|
| No workflow document provided | HALT. Request workflow. Do not audit nothing. |
| Workflow purpose ambiguous | HALT. Ask user to state intent. Do not audit without a target. |
| Cannot verify an external reference | Record as UNVERIFIABLE finding (not BROKEN). Note verification limits. |
| Workflow format unrecognizable | Record format as FREEFORM. Proceed with audit. Note that format-specific checks (YAML structure, frontmatter) will be SKIPPED. |
| Layer produces ambiguous result | Record as PARTIAL. Include both interpretations in the finding. Never round up. |
| User asks to skip a layer in Full Audit mode | Refuse. Offer Targeted mode instead. A Full Audit with skipped layers is a lie. |
| Out-of-scope request ("fix this for me", "rewrite this section", "improve the wording") | Emit structured refusal. Route to appropriate skill or user action. |

---

## Anti-Drift Safeguards

1. **No modification**: Never edit, rewrite, or "improve" the workflow under audit.
   Findings describe problems. Remediation fields suggest fixes. The auditor does
   not apply them.
2. **No skipping**: All checks within an executed layer run. A skipped check is an
   unverified claim.
3. **No grade inflation**: If a check fails, it fails. Do not soften findings to
   avoid difficult conversations. The whole point is to catch problems early.
4. **No domain judgment**: The auditor does not evaluate whether the workflow's
   subject matter is correct — only whether the workflow is structurally sound,
   internally consistent, and executable.
5. **Findings before routing**: Always present the full audit report to the user
   before routing any findings. The user confirms remediation paths.
6. **Separation of concerns**: Do not mix audit and construction work in the same
   session. If the user wants to fix findings, route them to the appropriate skill
   or start a new session.
7. **Mode 5 clarification — plan, do not apply** (see also Iterative Audit Procedure below): Safeguard #1 ("No modification")
   applies to **the workflow under audit** at all times. Mode 5 IS permitted to
   **author** a `remediation_plan`. Mode 5 is **NOT** permitted to **apply** any
   plan item, even after the user approves the plan. Plan execution belongs to a
   separate agent in a separate session. The Mode 5 deliverable is the merged
   `audit_report` + `remediation_plan` artifact and an explicit handoff.
8. **Mode 5 Intent immutability**: After the Workflow Intent is approved at Step
   M5-2, it is the anti-drift anchor for the rest of the run and is immutable
   within that run. If the auditor concludes the Intent itself is misstated,
   HALT (`halt_reason: INTENT_DRIFT`) and notify the user. Do not silently revise.
9. **Mode 5 two-pass exit only**: A single clean pass is a candidate, never a
   confirmation. Exit requires **two consecutive clean passes**.

---

## Iterative Audit Procedure (Mode 5)

Mode 5 wraps the full 8-layer framework in the 10-step loop below. **STEP 0
still runs first** (mode selection, format detection, viability gate). The
loop begins after STEP 0 completes.

**Determinism rule:** During every granular pass, traverse the workflow under
audit in **document order, depth-first**. Same input → same traversal → same
finding order across runs. This is non-negotiable; it makes Mode 5 reproducible.

### Step M5-1 — High-level review

Read the entire workflow at speed. Capture purpose, scope, tone, structure,
declared mode (if any). No per-step depth yet.

This step uses STEP 0's viability gate; it does not replace it.

### Step M5-2 — Summarize Workflow Intent → user approval gate

Author a concise statement of the workflow's overall intent (≤ 3 sentences,
not granular). It MUST encapsulate purpose without prescribing implementation.

Write the summary into `audit_report.stated_intent`. Mode 5 OVERWRITES the
bare STEP-0 intent with this richer, user-approved summary.

Present to the user:

- **2.1 Not approved**
  - 2.1.1 Solicit feedback. Refine the summary. Re-present.
  - **Hard cap: 3 refinement rounds.** If still not approved on the third
    round → HALT (`halt_reason: INTENT_NOT_APPROVED`). Notify the user with
    the three candidate summaries and stop.

- **2.2 Approved**
  - 2.2.1 The approved Intent becomes the **anti-drift anchor** for the rest
    of the run. It is immutable within the run (Anti-Drift §8). It is
    restated at the top of every granular pass (Step M5-3) and at every
    plan-review checkpoint (Step M5-9).
  - 2.2.2 Begin (or continue) the iterative loop at Step M5-3.

### Step M5-3 — Granular per-step review (Pass N)

1. Initialize `pass_number = 1` on first entry; otherwise increment.
2. **Restate the approved Intent** at the top of the pass (record in
   `iteration_log[N].notes`).
3. Walk the workflow under audit **step-by-step in document order, depth-first**.
4. For each step, run **all 8 audit layers** per the existing per-check
   protocol (PASS / FAIL / PARTIAL / SKIPPED). The **step boundary** is the
   smallest enclosing element from this fixed hierarchy (use the first
   matching level — never blend levels):
   1. **Numbered or lettered list item** — any line whose leading
      non-whitespace prefix matches the regex
      `^\s*(\d+|[A-Za-z]|[ivxIVX]+)[\.\)]\s+` (Arabic, single Latin letter, or
      Roman numeral followed by `.` or `)` and at least one whitespace).
      Plain bullet items (`-`, `*`, `+`) do NOT count as steps; they are
      sub-content of the enclosing step.
   2. **Markdown heading section** (`#` … `######`) at the deepest applicable level.
   3. **Fenced code block** (```` ``` ````), treated as a single atomic step.
   4. **Prose paragraph** (text separated by blank lines), only when none of
      levels 1–3 apply.
   Sub-bullets, inline code, and tables are evaluated as part of the enclosing
   step at one of the four levels above; they are not standalone steps.
5. Findings use the existing `finding` schema and SET `pass_number = N`.
   `finding.location` MUST cite the step boundary level used (e.g.
   "Step M5-3 item 4 (numbered list item)").

### Step M5-4 — Classify findings (MISSING / INCORRECT / AMBIGUOUS / OUT_OF_SCOPE)

In addition to the standard `category` enum, Mode 5 emphasizes a four-way
classification when summarizing per-pass results:

- **MISSING** — required step absent for Intent (typically L3-OUT, L4-CMP).
- **INCORRECT** — step present but wrong; maps to exactly these `category`
  enum values: `UNHANDLED`, `CONTRADICTION`, `BROKEN_REF`, `UNREACHABLE`,
  `STALE_REF`, `UNVERIFIABLE`, `STRUCTURAL`, `REDUNDANCY`, `ASSUMPTION`. Any
  category not on this list is NOT classified as INCORRECT — see the other
  three labels below or consult the canonical `category` enum in the
  `finding` schema.
- **AMBIGUOUS** — step unclear or non-deterministic; maps to `AMBIGUITY`.
- **OUT_OF_SCOPE** — step exceeds Intent; maps to `SCOPE_LEAK`.

Each finding still records the standard `category` plus this surface label in
`finding.description` for the per-pass summary.

### Step M5-5 — Compile and deduplicate

1. Aggregate findings discovered in this pass.
2. Deduplicate against findings already on file from prior passes. Two
   findings are duplicates **iff ALL THREE** of these fields are identical
   (string-exact comparison):
   - `finding.check_id`  (e.g. `"1.5"`)
   - `finding.category`  (canonical enum value, e.g. `"AMBIGUITY"`)
   - `finding.location`  (must match the step-boundary citation rule defined
     in Step M5-3 item 5)

   `evidence` similarity is **not** a dedup criterion. Two findings with the
   same `check_id` + `category` + `location` but different `evidence` are
   treated as **the same finding with additional evidence** (apply rule 3,
   below). Two findings with different `check_id` or `category` or `location`
   are **never deduped**, even if their text reads similarly.
3. When a new finding is detected as a duplicate (per rule 2), do NOT create
   a new finding record. Instead, append the new finding's `evidence` text to
   the existing finding's `evidence` field as a new line, prefixed with
   `[pass N]:` followed by a single space (where N is the current
   `pass_number`). Do not modify any other field on the existing finding.
4. Update `iteration_log[N].new_findings_count` to count only findings that
   were NOT dedup-matched in this pass.

### Step M5-6 — Pass complete: branch on findings

- **6.1 Findings exist this pass**
  - 6.1.1 Restate the approved Intent.
  - 6.1.2 → return to Step M5-3 for Pass N+1.
- **6.2 Zero findings this pass AND prior pass had findings (first clean pass)**
  - 6.2.1 Note in `iteration_log`: "First clean pass at N=…"
  - 6.2.2 → return to Step M5-3 for Pass N+1 (confirmation pass).
- **6.3 Zero findings this pass AND prior pass also clean (second consecutive clean pass)**
  - 6.3.1 Loop exits. Continue to Step M5-7.

#### Intent-drift halt (any time during M5-3 → M5-6)

HALT the loop with `halt_reason: INTENT_DRIFT` and notify the user **iff any
one** of these three explicit triggers fires in a single pass:

1. **OUT_OF_SCOPE saturation** — the pass produces ≥ **3** findings whose
   four-way classification (Step M5-4) is `OUT_OF_SCOPE`. (Threshold is fixed
   at 3 to distinguish a few in-scope outliers from a systemic mismatch.)
2. **Intent vs declared scope contradiction** — at least one finding in this
   pass reports a `CONTRADICTION` between the approved Intent statement and
   the workflow's own declared scope (any of: in-scope list, out-of-scope
   list, "never" list, or mission/objective statement). Source contradiction
   must be cited verbatim in the finding's `evidence`.
3. **MISSING-step density** — the pass produces ≥ **5** findings classified
   `MISSING` (Step M5-4) that all cite the same Intent clause as the gap.
   (Same Intent clause = identical substring of the approved Intent in the
   finding's `description` or `remediation` field.)

Trigger evaluation is per-pass (not cumulative across passes). Do NOT silently
revise the Intent — that is forbidden by Anti-Drift §8. The user must decide
whether to restart Mode 5 with a corrected Intent. If none of the three
triggers fires, the loop continues normally even when individual findings
hint at Intent issues.

#### Mode 5 state externalization

To keep concurrent in-memory state low, Mode 5 externalizes loop state to a
**bootstrap scratchpad** (a dedicated section in `context-bootstrap`).
The scratchpad is the source of truth for cross-pass state; the in-memory
copy is a working buffer.

**Scratchpad contract.** At Step M5-2 approval, allocate a scratchpad
section (record its ID in `audit_report.iteration.bootstrap_scratchpad_id`).
The scratchpad MUST contain exactly these top-level keys, written as a
YAML block:

- `intent_anchor` — the approved Workflow Intent string.
- `intent_clauses` — atomic clauses (computed at first M5-9 entry).
- `pass_number` — current pass counter.
- `findings` — cumulative findings list (full schema).
- `plan_items` — current `remediation_plan.items[]` (filled at M5-8).
- `iteration_log` — per-pass entries.
- `halt_flag` — null while running; set to a `halt_reason` enum on halt.

**Read/write rule.** At the start of every pass (Step M5-3 item 1), read
the scratchpad and load `pass_number`, `findings`, and `intent_anchor`
into working memory. At the end of every pass (after Step M5-5), write
back the updated `findings`, `iteration_log`, and `pass_number`. At
Step M5-8, write `plan_items`. At Step M5-9, write `intent_clauses` and
`clause_coverage`. At Step M5-10, write `halt_flag` if applicable.

**Effect on cognitive load.** With externalization, the agent holds only
the **current pass's findings buffer** and the **scratchpad ID** in
working memory. Other state items are read/write fields, not in-head
state. This keeps Mode 5 below the L7-EXE 7.5 PARTIAL band.

**Granular-pass-failure interaction.** If a granular pass fails before
write-back, the scratchpad still reflects the prior pass's state; the
auditor restarts from there on Pass N+1.

#### Granular-pass-failure protocol

If a per-step pass cannot complete (file segment unreadable, mid-pass error,
unrecoverable layer failure on every step):

- Set `iteration_log[N].pass_status = INCOMPLETE`.
- Do NOT count the pass toward the clean-pass quota.
- Notify the user.
- Proceed to Pass N+1 (do not silently retry the same pass).
- If two consecutive INCOMPLETE passes → HALT
  (`halt_reason: GRANULAR_PASS_FAILURE`).

#### User-timeout protocol

User prompts at Step M5-2 (Intent approval) and Step M5-10 (plan approval)
have a fixed response window of **30 minutes** (configurable per session if
the user states a different limit at start). On window expiry:

- Save `audit_report` and `remediation_plan` (current state) to the session
  bootstrap.
- HALT (`halt_reason: USER_TIMEOUT`).
- Note in `iteration_log` which prompt timed out (M5-2 vs M5-10) and the
  pass number at the time.

The user may resume in a new session; a resumed run treats the saved state
as authoritative and re-presents the same prompt.

#### Dedup-failure protocol

If Step M5-5 deduplication cannot complete (e.g. malformed `finding`
records prevent the string-exact triple-key comparison, or a finding lacks
one of the three required fields `check_id` / `category` / `location`):

- Mark the offending finding(s) with `finding.dedup_status = "MALFORMED"`
  (a transient status; not stored in the final report).
- Skip dedup for those specific findings; ALL other findings dedup
  normally per Step M5-5 rule 2.
- If ≥ 1 malformed finding remains after the pass → HALT
  (`halt_reason: DEDUP_FAILURE`). The auditor cannot guarantee the
  two-clean-pass exit invariant when dedup is partial.
- If all malformed findings can be repaired by the auditor before the next
  pass (e.g. by filling in a missing `category` from `check_id`), the
  pass continues normally.

#### Iteration-budget protocol

To prevent runaway loops, Mode 5 caps total passes at a fixed budget.

- **Default budget: `pass_budget = 10`.** The user MAY override at Step
  M5-1 (acceptance) by stating an integer between 4 and 30 inclusive.
  Outside that range or non-integer → reject and use 10.
- The budget includes ALL passes — passes that surface findings AND clean
  passes. (Two clean passes still count toward the budget.)
- **Trigger:** at the END of any pass (after Step M5-5 write-back), if
  `pass_count >= pass_budget` AND `clean_passes < 2` → HALT
  (`halt_reason: ITERATION_BUDGET_EXHAUSTED`).
- **On halt:** Skip Step M5-7 consolidation? **No** — still consolidate
  findings discovered through `pass_count`, still build the remediation
  plan at Step M5-8, still run plan ↔ Intent review at Step M5-9. The
  user receives a partial-but-actionable report with `halt_reason` set.
- **Rationale:** A workflow that cannot reach two clean passes within 10
  iterations is structurally unstable; further passes are unlikely to
  converge. Surface the report, let a follow-up session restructure.
- **No retries.** The auditor MUST NOT increase the budget mid-run, even
  if findings are still being discovered. The user can request a new
  Mode 5 audit with a higher budget after reviewing the partial result.

### Step M5-7 — Final consolidated findings summary

- Emit the consolidated set of all findings discovered across all passes,
  deduped, with `pass_number` retained on each so the user sees when each one
  surfaced.
- Each finding retains the FULL existing schema. No compression. No softening.
- Severity, routing, evidence, impact, and remediation fields are preserved
  verbatim from the underlying audit.

### Step M5-8 — Build remediation plan (proposal-only)

For every consolidated finding, emit a concrete plan item:

- `action`: ADD | REMOVE | UPDATE | REPLACE | SPLIT | MERGE
- `target`: section / step / line range in workflow under audit
- `change`: concrete change text (proposal — not applied). **Hard limit:
  ≤ 60 words. MUST describe the action and the target only.** It MAY include
  a short example phrase ≤ 10 words inside quotes when needed for clarity.
  It MUST NOT contain a full re-authored section, full replacement
  YAML/markdown body, or complete prose paragraphs intended for verbatim
  insertion. If a finding requires long-form rewriting, set
  `routing = PROMPT_BUILDER`, write a short directive in `change`, and add
  the item to `prompt_builder_substeps` with rationale; the executor
  session authors the long-form text.
- `severity`: inherited from the highest-severity finding the item resolves
- `routing`: inherited from the finding(s)
- `depends_on`: other plan_ids that must land first
- `locked`: bool, defaults to `false` at plan creation (see Step M5-10
  PARTIAL branch).

Ordering: **severity-first (CRITICAL → ADVISORY), then layer order, then
dependency topological order**.

Items with `routing == PROMPT_BUILDER` are also listed under
`remediation_plan.prompt_builder_substeps` with rationale. Mode 5 does NOT
invoke `deterministic-prompt-builder`. The executor session does.

The plan is **proposal-only**. Mode 5 NEVER applies plan items.

### Step M5-9 — Plan ↔ Intent review

Verify plan-Intent satisfaction by **atomic-clause coverage**, NOT by free
judgment.

**Procedure:**

1. **Decompose the approved Intent** (`intent_anchor`) into atomic clauses.
   Each clause is one independent declarative claim. Split rules:
   - Sentence boundaries (`.`, `?`, `!`) are clause boundaries.
   - Within a sentence, a coordinating conjunction (`and`, `or`, `;`) that
     joins two complete claims (each with its own subject + verb) is a
     clause boundary; the conjunction is dropped.
   - Subordinate clauses introduced by `because`, `so that`, `in order to`,
     `while`, `unless` stay with their parent clause (not split).
   - The total clause count MUST be ≥ 1 and SHOULD be ≤ 5; > 5 indicates
     the Intent is too granular and should have been refined at Step M5-2.
   Record the resulting list in `plan_review.intent_clauses`
     (new field — see Output Contract addition below).

2. **Map each clause to coverage**. For every clause C, set
   `plan_review.clause_coverage[C]` to the union of:
   - `plan_item_ids`: list of `remediation_plan.items[].plan_id` whose
     `change` text references the same subject/object as C, AND
   - `existing_step_locations`: list of `finding.location`-style citations
     pointing to steps in the workflow under audit that already satisfy C
     without modification.

3. **Compute satisfaction**:
   - `satisfies_intent = true` IFF every clause C has
     `len(plan_item_ids) + len(existing_step_locations) ≥ 1`.
   - `gaps_if_unsatisfied` = the list of clauses C for which both lists
     are empty (verbatim clause text).

4. **Branch**:
   - `satisfies_intent == true` → continue to M5-10.
   - `satisfies_intent == false` → **back-edge to Step M5-8** (revise plan
     to add items covering each gap clause); increment
     `plan_review.revision_rounds`.
   - **Hard cap: 3 revision rounds.** If still unsatisfied on the third
     round → HALT (`halt_reason: PLAN_REVISION_EXHAUSTED`). Deliver the
     partial plan plus the verbatim gap clauses to the user.

This procedure is fully deterministic: two auditors with the same
`audit_report` and same `remediation_plan.items[]` MUST produce the same
clause set, the same coverage map, and the same `satisfies_intent` value.

### Step M5-10 — Present plan to user

Deliver the merged artifact: `audit_report` + `iteration` + `remediation_plan`.

User options:

- **Approve** → set `user_approval.status = APPROVED`. Mode 5 ends. Hand off
  to the executor session via `context-bootstrap`. Record bootstrap entry.
- **Reject** → set `user_approval.status = REJECTED`. Capture rationale in
  `user_approval.rationale`. **Return to Step M5-3** for a fresh pass with
  the rejection rationale carried into `iteration_log`.
- **Partial** → set `user_approval.status = PARTIAL`. Capture rationale in
  `user_approval.rationale`. The user MUST identify each accepted plan item
  by `plan_id`; for every accepted item, set
  `remediation_plan.items[<plan_id>].locked = true`. All other items remain
  `locked = false`. Then return to Step M5-3 with the following constraint:
  any finding whose `finding_id` appears in `items[<plan_id>].finding_ids`
  for a `locked = true` item is **excluded** from subsequent passes (it is
  considered resolved). The two-clean-pass exit rule applies to the
  remaining (non-locked) finding surface.

If the user halts the run at any prompt → set
`halt_reason: USER_HALT` and exit cleanly.

### Mode 5 — Halt summary

| Halt reason | Trigger |
| --- | --- |
| `INTENT_NOT_APPROVED` | 3 refinement rounds at Step M5-2 without approval. |
| `INTENT_DRIFT` | Any of the three explicit triggers in §Intent-drift halt fires in a single pass. |
| `GRANULAR_PASS_FAILURE` | Two consecutive INCOMPLETE granular passes. |
| `PLAN_REVISION_EXHAUSTED` | 3 revision rounds at Step M5-9 without satisfaction. |
| `USER_HALT` | User halts at any prompt. |
| `USER_TIMEOUT` | User does not respond at M5-2 or M5-10 within the response window (default 30 min). |
| `DEDUP_FAILURE` | ≥ 1 malformed finding prevents Step M5-5 dedup from completing for that finding. |
| `ITERATION_BUDGET_EXHAUSTED` | `pass_count >= pass_budget` (default 10) reached without two consecutive clean passes. |

---

## Companion Skills

- **`deterministic-prompt-builder`** — Construction skill for YAML prompts.
  Route YAML-specific structural findings here when the workflow is a YAML prompt
  that needs to be rebuilt or brought into compliance with the 8-principle spec.
  **In Mode 5**, plan items whose `routing == PROMPT_BUILDER` are listed under
  `remediation_plan.prompt_builder_substeps` with rationale. The Mode 5 auditor
  does NOT invoke `deterministic-prompt-builder`; the executor session does.
- **`ontology-axiom-compliance`** — Audit skill for ontology systems. IF the
  workflow under audit governs an ontology system (schema definitions, entity
  relationships, constraint enforcement) → recommend axiom-level compliance
  audit in a separate session. ELSE → skip.
- **`context-bootstrap`** — Session continuity. Audit findings and routing queues
  should be captured in the session bootstrap if the remediation work will span
  multiple sessions. **Mode 5 always crosses sessions** (audit here, executor
  next), so a bootstrap entry is required at handoff.

---

## Procedure Summary

```
STEP 0: Pre-Audit Setup
  → Load workflow → Generate audit_id → Identify format → Confirm intent
  → Select mode → Run viability gate

STEP 1: Execute Audit Layers 1–4 (foundational checks)
  → For each layer (L1-DET, L2-REF, L3-OUT, L4-CMP):
    → Run all checks (per-check error protocol applies)
    → Record findings
    → Calculate layer score
    → If layer cannot complete → invoke layer-failure protocol

CHECKPOINT: Summarize Layers 1–4 findings before continuing.
  → This prevents attention decay on later layers.

STEP 2: Execute Audit Layers 5–8 (structural checks)
  → For each layer (L5-CON, L6-SCP, L7-EXE, L8-STR):
    → Run all checks
    → Record findings
    → Calculate layer score

STEP 3: Calculate Overall Score and Tier
  → Weighted average of layer scores
  → Apply tier map
  → Apply tier overrides (if any)

STEP 4: Classify and Route Findings
  → Assign severity to each finding
  → Sort by severity, then layer order
  → Assign routing (PROMPT_BUILDER | USER_ACTION | INFORMATIONAL)

STEP 5: Assemble Report
  → Populate all fields of audit_report schema
  → Include decision_trace

STEP 6: Present to User
  → Deliver the audit report
  → Offer: "Want me to drill into any specific layer or finding?"
  → If Post-Mortem: present root cause mapping
  → If Diff: present comparative table

STEP 7: Route on User Confirmation
  → User confirms routing queues
  → Findings routed to companion skills or user action
```

### Procedure Summary — Mode 5 (Iterative)

```
STEP 0:    Pre-Audit Setup (unchanged) — base_mode = FULL | POST_MORTEM | DIFF

STEP M5-1: High-level review of the entire workflow (Summarize)

STEP M5-2: Summarize Workflow Intent → user approval gate
           NOT_APPROVED → refine (≤3 rounds) → else HALT (INTENT_NOT_APPROVED)
           APPROVED   → Intent becomes anti-drift anchor (immutable in run)

LOOP {
  STEP M5-3: Granular per-step review (Pass N)
             - Restate Intent
             - Document-order DFS over workflow
             - Run all 8 layers per step (per-check protocol applies)
             - Tag findings with pass_number = N

  STEP M5-4: Classify findings (MISSING / INCORRECT / AMBIGUOUS / OUT_OF_SCOPE)

  STEP M5-5: Compile + deduplicate against prior-pass findings

  STEP M5-6: Branch
             6.1 Findings exist        → goto M5-3 (Pass N+1)
             6.2 Clean pass #1         → goto M5-3 (Pass N+1, confirmation)
             6.3 Clean pass #2         → exit loop

  HALTS (any time): INTENT_DRIFT | GRANULAR_PASS_FAILURE | USER_HALT
}

STEP M5-7: Final consolidated findings summary (full schema, pass_number kept)

STEP M5-8: Build remediation plan (proposal-only)
           - Items ordered: severity → layer → dependency topology
           - PROMPT_BUILDER items also listed under prompt_builder_substeps

STEP M5-9: Plan ↔ Intent review
           Unsatisfied → goto M5-8 (≤3 revision rounds) → else HALT (PLAN_REVISION_EXHAUSTED)
           Satisfied   → continue

STEP M5-10: Present audit_report + iteration + remediation_plan to user
            APPROVE → handoff via context-bootstrap; END
            REJECT  → goto M5-3 (re-audit, rationale logged)
            PARTIAL → treat as REJECT; rationale logged
```
