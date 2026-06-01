---
name: deterministic-prompt-builder
description: >
  Deterministic prompt engineering system that creates, generates, and validates
  structured YAML agent prompts with closed-world semantics, fixed pipelines,
  validation gates, and drift prevention. Use this skill whenever the user mentions
  prompt engineering, writing a system prompt, building an agent prompt, creating a
  classifier prompt, making a deterministic prompt, YAML prompt, agent specification,
  "write me a prompt for", "build an agent that", "I need a prompt", structured prompt,
  prompt validation, prompt compliance, prompt audit, drift prevention in prompts,
  "make this deterministic", "turn this into a prompt", prompt skeleton, prompt template,
  or any request to produce instructions that an AI agent should follow. Also trigger
  when the user asks to distill knowledge, reverse-engineer documentation, or run
  ground-floor research — these are specialized templates available on request.
  When in doubt, trigger — a bad trigger is better than a missed one.
---

# Deterministic Prompt Builder

## What This Skill Does

This skill produces deterministic YAML agent prompts that obey 8 non-negotiable
principles. Every prompt it creates has: a fixed identity, a closed scope, an explicit
algorithm, a locked output schema, validation gates, drift prevention, and structured
error handling. No prose. No ambiguity. No invention.

## STEP 0 — Read References Before Generating

Before producing any prompt, read the reference files relevant to the current task:

| Task | Read These First |
|------|-----------------|
| Any prompt creation (interview or one-shot) | `references/skeleton.yaml` + `references/section-templates.md` |
| Selecting drift prevention mechanisms | `references/drift-catalog.md` |
| Checking for anti-patterns in a draft | `references/anti-patterns.md` |
| Validating an existing prompt | `references/quick-ref.md` + `references/anti-patterns.md` |
| User asks about the worked example | `references/example-prompt.yaml` |
| User asks about terminology | `references/glossary.md` |
| User asks to distill knowledge | `references/distillation-template.md` |
| User asks to reverse-engineer docs | `references/reverse-eng-template.md` |
| User asks for ground-floor research | `references/research-template.md` |

Do NOT generate from memory. Read the skeleton and templates every time.

---

## STEP 1 — Detect Mode

Determine which mode to operate in based on the user's input:

```
IF user provides an existing prompt/spec AND asks to check/validate/audit it:
  → MODE: VALIDATE
ELIF user provides a clear task description with enough detail to generate:
  → MODE: ONE-SHOT
ELSE:
  → MODE: INTERVIEW
```

Signals for each mode:
- **VALIDATE**: "check this prompt", "is this compliant", "audit", "validate", "review my prompt", user pastes a prompt and asks about quality
- **ONE-SHOT**: "write a prompt that classifies X", "build an agent for Y", "create a prompt to do Z", user gives a task with clear scope + domain
- **INTERVIEW**: "help me build a prompt", "I need a prompt", vague request, missing scope/domain/authority, user says "I don't know where to start"

---

## STEP 2A — Interview Mode

Walk the user through these 8 questions, one or two at a time. Do not dump all 8 at once.
Adapt phrasing to match the user's domain language. Skip questions the user has already
answered in their initial message.

```yaml
interview_questions:
  1_mission:
    ask: "What should this agent do? Give me one sentence."
    maps_to: "mission.objective"
    gate: "Must be one sentence. Must be specific. No jargon undefined elsewhere."

  2_scope:
    ask: "What will it NEVER do? What's out of bounds?"
    maps_to: "mission.scope.in_scope + mission.scope.out_of_scope"
    gate: "Both lists must be non-empty. out_of_scope must cover plausible misuses."

  3_authority:
    ask: "What is the single source of truth? What data is canonical vs. derived?"
    maps_to: "identity.authority_model"
    gate: "Exactly one canonical source named. Conflict resolution defined."

  4_inputs:
    ask: "What inputs will the agent receive? What should it ignore?"
    maps_to: "input_rules"
    gate: "accepted_sources and rejected_sources both non-empty."

  5_output:
    ask: "What exact fields should the output have? What format? What ordering?"
    maps_to: "output_contract"
    gate: "Every field has name, type, required. Ordering specified."

  6_algorithm:
    ask: "Walk me through the steps, in order. What does step 1 do? Step 2?"
    maps_to: "decision_procedure"
    gate: "Steps numbered. Each has action, input, output, validation, on_failure."

  7_validation:
    ask: "What checks must pass before output is emitted?"
    maps_to: "validation gates in decision_procedure + output_contract"
    gate: "At least one gate per step. Final gate checks schema compliance."

  8_errors:
    ask: "When something goes wrong, what should the error look like?"
    maps_to: "error_handling"
    gate: "Structured error format defined. Recovery options listed."
```

### Gate Failure Handling

If a user's answer does not meet the gate criteria:
1. Explain what the gate requires and why.
2. Show what is missing or non-compliant.
3. Re-ask the question with a concrete example of a compliant answer.
4. Do NOT proceed to the next question until the gate passes.

After collecting answers that pass all gates, proceed to STEP 3.

---

## STEP 2B — One-Shot Mode

Parse the user's task description and extract answers to all 8 questions implicitly.
For any question that cannot be answered from the input, make a reasonable default
and flag it for the user to confirm:

```yaml
one_shot_procedure:
  step_1: "Extract mission objective from task description"
  step_2: "Infer scope (in/out) from domain and task type"
  step_3: "Identify canonical source (usually the prompt itself or user-specified data)"
  step_4: "Determine input types from task description"
  step_5: "Design output schema from task requirements"
  step_6: "Construct step-by-step algorithm"
  step_7: "Add validation gates to each step + final emission"
  step_8: "Define error format"
  step_9: "Present inferred answers to user with [INFERRED] tags on anything assumed"
  step_10: "On user confirmation, proceed to STEP 3"
  on_rejection: >
    If the user rejects or corrects any inference:
    1. Update the rejected values per user feedback.
    2. Re-check that the updated values still satisfy the gate for that question.
    3. Re-present the full inferred answer set with changes marked [REVISED].
    4. Wait for confirmation before proceeding.
```

Do NOT silently generate without showing the user what was inferred.
Every inferred value must be flagged and confirmed.

---

## STEP 2C — Validate Mode

Read `references/quick-ref.md` and `references/anti-patterns.md` first.

Apply the following compliance checks to the provided prompt:

```yaml
validation_pipeline:
  structural_checks:
    - "All 11 skeleton sections present (or explicitly n/a)"
    - "prompt_metadata complete (id, version, status, author)"
    - "identity section has role, role_constraints, authority_model"
    - "mission section has objective, in_scope, out_of_scope"
    - "decision_procedure has numbered steps with validation + on_failure"
    - "output_contract has schema with field definitions"
    - "error_handling has structured error format"
    - "drift_prevention has ≥5 mechanisms enabled"
    - "examples section has ≥3 positive, ≥2 negative, ≥2 edge cases"

  content_checks:
    - "No prose paragraphs (all content is YAML key-value or lists)"
    - "No vague verbs (consider, think, explore, try, attempt, look into)"
    - "No implicit enumerations (include, such as, for example, etc.)"
    - "Every definition has IS and IS-NOT"
    - "Every enum is closed (no 'other' unless explicitly defined)"
    - "decision_trace required in output schema"
    - "All output fields have type + constraints"
    - "Every step has on_failure defined"

  anti_pattern_scan:
    - "Check against all 12 anti-patterns from references/anti-patterns.md"
    - "Flag each violation with AP-ID, location, and fix"

  output:
    format: "structured compliance report"
    structural_and_content_check_fields:
      - section: "which section or check name"
      - status: "PASS | FAIL | WARN"
      - finding: "what was found"
      - fix: "how to fix it (REQUIRED for FAIL and WARN, 'n/a' for PASS)"
    anti_pattern_scan_fields:
      - ap_id: "anti-pattern ID (e.g., AP-01)"
      - name: "anti-pattern name"
      - status: "PASS | FAIL | WARN"
      - section: "where in the prompt the violation was found ('n/a' if PASS)"
      - finding: "description of the violation ('n/a' if PASS)"
      - fix: "how to fix it ('n/a' if PASS)"
    summary:
      - total_checks: integer
      - passed: integer
      - failed: integer
      - warnings: integer
      - compliance_score: "passed / total_checks as percentage"
      - critical_failures: "list of the most important failures to address first"
      - recommendation: "one-sentence next action"
```

Deliver the compliance report, then offer to fix the issues.

---

## STEP 3 — Auto-Select Drift Prevention

Read `references/drift-catalog.md` for the full mechanism catalog.

Select mechanisms based on the prompt's use case.
Categories are additive — if the agent matches multiple categories
(e.g., classification + long-session), apply ALL matching mechanisms.

```yaml
drift_prevention_auto_select:
  # Always included (baseline for every prompt):
  always:
    - "DP-03: Scope Fence"           # zero cost unless triggered
    - "DP-05: Schema Lock"           # zero cost unless triggered
    - "DP-06: Decision Trace"        # ~100-200 tokens, essential for auditability
    - "DP-07: Precedence Hierarchy"  # zero cost, prevents authority confusion
    - "DP-09: Negative Examples"     # zero runtime cost, prevents common errors

  # Add based on use case:
  long_session_agents:
    add: ["DP-01: Identity Anchor", "DP-02: SCAN Protocol", "DP-04: Vocabulary Lock", "DP-08: Scope Creep Detection"]
    trigger: "agent is designed for multi-turn conversations (>5 turns expected)"

  stateful_agents:
    add: ["DP-01: Identity Anchor", "DP-02: SCAN Protocol", "DP-10: Output Fingerprinting"]
    trigger: "agent modifies state or produces cumulative outputs"

  classification_agents:
    add: ["DP-04: Vocabulary Lock"]
    trigger: "agent classifies inputs against a fixed enum"

  high_stakes_agents:
    add: ["DP-01", "DP-02", "DP-04", "DP-08", "DP-10"]
    trigger: "errors have significant consequences (financial, legal, safety)"
```

State the selected mechanisms and rationale in the generated prompt's
`drift_prevention` section. Do not ask the user to choose — select and explain.

---

## STEP 4 — Generate the Prompt

1. Read `references/skeleton.yaml` for the exact template structure.
2. Read `references/section-templates.md` for section-level guidance.
3. Fill every section using the collected/inferred answers.
4. Apply the selected drift prevention mechanisms.
5. Generate ≥3 positive examples, ≥2 negative examples, ≥2 edge cases.
6. Include the decision_trace in the output schema.

### Generation Rules

```yaml
generation_rules:
  format: "YAML only. No prose paragraphs anywhere in the prompt."
  verbs: "Use only deterministic verbs. Read references/quick-ref.md for the allowed list."
  enums: "Every list of allowed values is closed. No 'etc.', 'such as', 'including'."
  definitions: "Every term defined must have IS and IS-NOT."
  steps: "Every step has: action, input, output, validation, on_failure."
  step_ordering: >
    Validation gates within a step must be consistent with the state of data
    AT THAT STEP. If step N normalizes data and step N-1 validates format,
    the validation regex/constraint at step N-1 must match pre-normalization
    format, not post-normalization format. Alternatively, combine normalization
    and validation into the same step.
  errors: "Every error is structured (error_code, error_type, error_message, recovery_options)."
  output_schema: "Every field has: name, type, required, description, constraints."
  scope: "in_scope and out_of_scope are both exhaustive."
  authority: "Exactly one canonical_source. Trust hierarchy defined."
  no_invention: "Never fill gaps with assumed content. Flag unknowns."
  example_gate_consistency: >
    Every example (positive, negative, edge case) must be consistent with
    the validation gates and regex patterns defined in decision_procedure.
    If a positive example's expected output would fail a defined gate,
    the example is defective. If an edge case shows a passing result but
    the input would fail a validation regex, the edge case is defective.
    Verify each example against each relevant gate before including it.
```

---

## STEP 5 — Validate Before Emission

Run the Part 10 checklist (from `references/quick-ref.md`) against the generated prompt
BEFORE delivering it. This is a self-check — the prompt must pass its own spec.

```yaml
pre_emission_checklist:
  before_writing:
    - "Objective is ONE sentence"
    - "Canonical source is named"
    - "All in-scope actions listed"
    - "All out-of-scope actions listed"
    - "Every enum is closed"

  while_writing:
    - "Every step has exactly one action"
    - "Every step has validation and on_failure"
    - "Output schema is complete with types and constraints"
    - "≥3 positive examples"
    - "≥2 negative examples"
    - "≥2 edge cases"
    - "decision_trace required in every output"
    - "≥5 drift prevention mechanisms enabled"

  after_writing:
    - "0 prose paragraphs in the prompt"
    - "0 vague verbs"
    - "0 implicit enumerations"
    - "Every output field can be validated programmatically"
    - "Same input would produce same output on re-run"
    - "Error format is structured, not conversational"
    - "Every definition includes IS-NOT"
    - "All examples (positive, negative, edge) produce outputs consistent with defined validation gates and regex patterns"
    - "Step ordering is consistent: no step validates a format that a later step would change (e.g., validating case before a normalization step changes case)"
```

If any check fails, fix it before delivering. Do not deliver a non-compliant prompt.

---

## STEP 6 — Deliver

1. Save the generated prompt as a `.yaml` file.
2. File path: `/mnt/user-data/outputs/<prompt-id>.yaml`
3. Use the `prompt_metadata.id` field as the filename.
4. Present the file to the user.
5. Offer: "Want me to validate this against the full spec, or adjust any section?"

---

## The 8 Principles (Operational Summary)

These are non-negotiable. Every prompt produced by this skill must obey all 8.

```yaml
principles:
  P1_determinism:
    rule: "Same inputs → identical outputs. Stable ordering. No ambiguity."
    forbidden: "consider, might, perhaps, various, some, try, attempt"
    required: "explicit enumerations, exact counts, named items, sort key + direction"

  P2_authority:
    rule: "Exactly ONE canonical truth source. Everything else is derived."
    on_conflict: "Canonical wins. Always. Derived marked STALE."
    on_missing: "Return UNKNOWN. Never infer."

  P3_closed_world:
    rule: "Only enumerated values exist. No implicit 'other' category."
    on_new_value: "REFUSE. Return structured error."
    on_missing: "Return UNKNOWN. Never invent."

  P4_no_invention:
    rule: "Never guess, infer, assume, interpolate, extrapolate, or add."
    on_gap: "Return structured error with field name."
    on_unclear_intent: "Return clarification_request with options."

  P5_algorithm:
    rule: "Numbered steps. Sequential. Mandatory. One action per step."
    forbidden: "skip, reorder, invent steps"
    on_failure: "HALT at failed step. Return error."

  P6_output_contract:
    rule: "Exact schema. Fixed field names, types, ordering."
    forbidden: "extra text, commentary, preamble, postamble"
    on_missing_field: "Include with value UNKNOWN or null."

  P7_validation_gates:
    rule: "Checks run BEFORE output emission. All must pass."
    on_failure: "Do not emit. Return structured error."
    gate_types: [enum_check, regex_check, path_check, conflict_check,
                 completeness_check, range_check, referential_check]

  P8_anti_drift:
    rule: "≥5 drift prevention mechanisms per prompt."
    mechanisms: "See references/drift-catalog.md for the full 10."
    refusal_format: "Structured, not conversational."
```

---

## Edge Cases

```yaml
edge_cases:
  user_wants_creative_prompt:
    response: >
      This skill produces deterministic prompts. If you need variation,
      define the exact dimensions and bounds of permitted variation.
      Read anti-pattern AP-08 for guidance.

  user_wants_prose_prompt:
    response: >
      This spec requires YAML-only prompts. Prose is ambiguous and
      subject to attention decay. Convert prose to YAML key-value pairs.
      Read anti-pattern AP-01 for the rationale.

  user_asks_for_distillation:
    action: "Read references/distillation-template.md and follow its procedure."

  user_asks_for_reverse_engineering:
    action: "Read references/reverse-eng-template.md and follow its procedure."

  user_asks_for_ground_floor_research:
    action: "Read references/research-template.md and follow its procedure."

  user_prompt_has_no_clear_domain:
    action: "Enter INTERVIEW mode. Start with question 1 (mission)."

  user_provides_partial_spec:
    action: >
      Enter ONE-SHOT mode. Extract what's provided, flag gaps as
      [INFERRED] or [MISSING], confirm with user before generating.
```
