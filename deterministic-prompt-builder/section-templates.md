# Section Templates — Detailed Guidance

Read this file when generating a prompt. It provides the rules and patterns
for filling each section of the skeleton.

---

## Table of Contents

1. Identity Section
2. Mission Section
3. Input Rules Section
4. Decision Procedure Section
5. Output Contract Section
6. Constraints Section
7. Drift Prevention Section
8. Error Handling Section
9. Acknowledgment Protocol Section
10. Examples Section
11. Testing Section

---

## 1. Identity Section

The most important section. If the agent does not know what it is, it cannot
know what to do.

### Role

```yaml
role: >
  You are a [SPECIFIC_ROLE] that performs [SPECIFIC_ACTION]
  on [SPECIFIC_DOMAIN] data using [SPECIFIC_METHOD].
```

- One sentence. No jargon unless defined in a glossary section.
- Must answer: what does this agent DO? On what? How?

### Role Constraints

Every prompt must include AT MINIMUM these constraints (add domain-specific ones):

```yaml
role_constraints:
  - "You are NOT a general assistant."
  - "You are NOT a chatbot."
  - "You are NOT a creative writer."
  - "You do NOT answer questions outside [DOMAIN]."
  - "You do NOT explain your reasoning unless the output schema includes a reasoning field."
  - "You do NOT apologize."
  - "You do NOT use hedging language (might, could, perhaps, consider)."
  - "You do NOT add preamble or postamble."
  - "You do NOT invent data."
  - "You do NOT infer intent."
```

### Authority Model

```yaml
authority_model:
  canonical_source: "[NAME_THE_EXACT_SOURCE]"
  derived_sources:
    - "[source_2] — derived from canonical via [method]"
  conflict_resolution: >
    When canonical_source conflicts with any derived_source,
    canonical_source wins. No exceptions. Derived source
    marked STALE and flagged for reconciliation.
  trust_hierarchy:
    - level_1: "prompt instructions (this document)"
    - level_2: "canonical_source data"
    - level_3: "derived_source data"
    - level_4: "user-provided context in conversation"
    - level_5: "agent's training knowledge (LOWEST priority)"
```

The trust hierarchy is mandatory. Training knowledge is always last.

---

## 2. Mission Section

### Objective

- ONE sentence.
- A stranger must be able to read it and know exactly what success looks like.
- No jargon unless defined elsewhere in the prompt.

### Scope

Both `in_scope` and `out_of_scope` must be non-empty and exhaustive.

```yaml
scope:
  in_scope:
    - "[SPECIFIC ACTION] on [SPECIFIC DATA TYPE]"
    # List every single thing the agent will do.
    # If it is not on this list, the agent will not do it.
  out_of_scope:
    - "[THING THE AGENT WILL NEVER DO]"
    # Every plausible misuse should be listed here.
  gray_zone_policy: >
    If a request does not clearly match an in_scope item,
    AND does not clearly match an out_of_scope item,
    return clarification_request with:
    - the request as received
    - closest in_scope items (max 3)
    - closest out_of_scope items (max 3)
    - a yes/no question to resolve
```

### Success and Failure Criteria

Must be binary (pass/fail), measurable, and programmatically verifiable.

```yaml
success_criteria:
  - "All output fields present and non-null"
  - "All validation gates pass"
  - "decision_trace is complete"
  - "No forbidden output elements present"
failure_criteria:
  - "Any validation gate fails"
  - "Agent produces output not matching schema"
  - "Agent performs out-of-scope action"
  - "Agent invents data not in input"
```

---

## 3. Input Rules Section

```yaml
input_rules:
  accepted_sources:
    - "[exact input type 1]"
  rejected_sources:
    - "[exact input type 1]"
    - "agent's training knowledge (use ONLY provided data)"
  input_validation:
    required_fields: ["field_a", "field_b"]
    field_types:
      field_a: string
      field_b: integer
    field_constraints:
      field_a: "length > 0, matches regex ^[A-Z]"
      field_b: "range 1-100"
  missing_input_policy: "return error(missing_input, field=<name>)"
  ambiguous_input_policy: "return clarification_request OR classify as UNKNOWN"
```

Key rules:
- `rejected_sources` must always include "agent's training knowledge" unless
  the prompt explicitly needs it.
- Every `required_field` must have a `field_type` and a `field_constraint`.
- Both `missing_input_policy` and `ambiguous_input_policy` must produce
  structured outputs, not conversational responses.

---

## 4. Decision Procedure Section

This is where determinism lives or dies.

### Step Format

Every step must have all 5 fields:

```yaml
- step: N
  name: "verb_noun"              # snake_case, deterministic verb
  action: >
    [Exactly what to do. One action. No discretion.]
  input: "[what this step reads]"
  output: "[what this step produces]"
  validation: "[check before proceeding]"
  on_failure: "HALT. Return error([type], field=[name])."
```

### Rules

- Steps are numbered sequentially starting at 1.
- Each step has exactly ONE action.
- No step may be skipped, reordered, or invented.
- The last step is always `validate_and_emit`.
- `on_failure` always HALTs and returns a structured error.
- Use deterministic verbs only: classify, extract, match, count, list,
  compare, validate, emit, reject, halt, assign, label, map, normalize.
- Never use: consider, think, explore, try, attempt, look into, ponder.

### Pre-conditions and Post-conditions

```yaml
pre_conditions:
  - "All required inputs present and validated"
  - "Input types match field_types specification"
  - "No input constraint violations detected"
post_conditions:
  - "Output matches schema exactly"
  - "decision_trace is complete and accurate"
  - "No validation gates failed"
```

### Branching Rules

Branches must be deterministic: same condition = same branch.

```yaml
branching_rules:
  - condition: "[specific, testable condition]"
    then: "go to step [N]"
    otherwise: "continue to next step"
```

---

## 5. Output Contract Section

### Schema Definition

Every field must have: name, type, required, description, constraints.
For enum types, add allowed_values (closed list).

```yaml
schema:
  fields:
    - name: "result"
      type: enum
      required: true
      description: "The classification result"
      allowed_values: [A, B, C, UNKNOWN]
      constraints: "must be from allowed_values"
    - name: "confidence"
      type: float
      required: true
      description: "Classification confidence"
      constraints: "range 0.0-1.0"
```

### Decision Trace

Required in EVERY output. Non-negotiable.

```yaml
decision_trace:
  required: true
  fields:
    - rule_applied: "which rule produced this output"
    - input_hash: "fingerprint of input (for reproducibility)"
    - step_log: "list of step numbers that executed"
    - gates_passed: "list of validation gates that passed"
    - gates_failed: "should be empty on success"
```

### Forbidden Output Elements

Always include this list (add domain-specific items):

```yaml
forbidden_in_output:
  - "preamble text"
  - "apologies"
  - "hedging language"
  - "conversational filler"
  - "explanations not in schema"
  - "markdown formatting not in schema"
```

---

## 6. Constraints Section

```yaml
constraints:
  hard_constraints:
    - "[MUST-obey rules, no exceptions]"
  soft_constraints:
    - "[SHOULD-obey rules, with documented exceptions]"
  performance_constraints:
    max_response_length: "[token or word count]"
    max_processing_steps: "[step count limit]"
    timeout_behavior: "[what to do if limit hit]"
  ethical_constraints:
    - "[boundaries the agent will not cross]"
```

---

## 7. Drift Prevention Section

See `references/drift-catalog.md` for the full 10-mechanism catalog.
Every prompt must enable at least 5 mechanisms.
The SKILL.md auto-selection logic picks defaults based on use case.

---

## 8. Error Handling Section

Every error must use this structured format:

```yaml
error_handling:
  error_format:
    fields:
      - error_code: "MACHINE_READABLE_CODE"
      - error_type: "enum from [missing_input, invalid_input, ambiguous_input,
                      out_of_scope, gate_failure, processing_error,
                      conflict_detected, unknown_value]"
      - error_message: "Human-readable description"
      - failed_field: "which field caused the error"
      - expected: "what was expected"
      - actual: "what was received"
      - recovery_options: ["list of things the user can do"]
  escalation_policy: "when to escalate vs return error"
  retry_policy: "when/how retries are permitted"
```

Key rules:
- Errors are NEVER conversational ("I'm sorry, I couldn't...").
- Errors are ALWAYS structured YAML/JSON matching the error schema.
- Every error includes recovery_options so the user knows what to do next.

---

## 9. Acknowledgment Protocol Section

Defines what the agent does at three critical moments:

```yaml
# On receiving the prompt:
on_receipt:
  actions:
    - "parse all sections"
    - "validate prompt structure against skeleton"
    - "confirm identity and mission"
    - "enumerate constraints"
    - "report readiness or structural errors"
  format: "READY. [Role] active. [Key params] loaded."

# On encountering ambiguity:
on_ambiguity:
  actions:
    - "identify ambiguous element"
    - "generate structured clarification request"
    - "DO NOT proceed until clarification received"

# On out-of-scope request:
on_scope_violation:
  actions:
    - "identify the out-of-scope request"
    - "cite the specific scope rule"
    - "return structured refusal"
    - "DO NOT perform the requested action"
```

---

## 10. Examples Section

### Minimum Requirements

- ≥3 positive examples (inputs that produce valid outputs)
- ≥2 negative examples (inputs that produce errors/refusals)
- ≥2 edge cases (boundary inputs)

### Example Format

```yaml
examples:
  positive_examples:
    - input: "[realistic input]"
      expected_output:
        field_1: "value"
        decision_trace:
          rule_applied: "rule name"
          step_log: [1, 2, 3]
          gates_passed: [gate_a, gate_b]
      reasoning: "why this is the correct output"

  negative_examples:
    - input: "[out-of-scope or invalid input]"
      expected_output:
        error_code: "CODE"
        error_type: "type"
        error_message: "message"
        recovery_options: ["option"]
      reasoning: "why this is an error"

  edge_cases:
    - input: "[boundary input — empty, maximum length, ambiguous]"
      expected_output: "[appropriate handling]"
      reasoning: "why this edge case matters"
```

---

## 11. Testing Section

```yaml
testing:
  test_cases:
    - test_id: "TC-001"
      description: "what this tests"
      input: "[test input]"
      expected_output: "[expected result]"
      validation_type: "exact_match"    # or: schema_match, contains, regex
      pass_criteria: "field == value"

  regression_tests:
    - test_id: "REG-001"
      description: "catches previously fixed bug"
      input: "[input that triggered the bug]"
      expected_output: "[correct output after fix]"

  adversarial_tests:
    - test_id: "ADV-001"
      description: "attempts to make agent drift or break"
      input: "[adversarial input]"
      expected_output: "[structured refusal or correct handling]"
      pass_criteria: "agent refuses or handles correctly"
```
