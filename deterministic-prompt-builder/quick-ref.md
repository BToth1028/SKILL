# Quick Reference Card

Use this for STEP 5 (pre-emission self-check) and STEP 2C (validation mode).

---

## Pre-Emission Checklist

### Before Writing

- [ ] Is the objective ONE sentence?
- [ ] Is the canonical source named?
- [ ] Are ALL in-scope actions listed?
- [ ] Are ALL out-of-scope actions listed?
- [ ] Is every enum closed (no 'etc.' or 'such as')?

### While Writing

- [ ] Does every step have exactly one action?
- [ ] Does every step have validation and on_failure?
- [ ] Is the output schema complete with types and constraints?
- [ ] Are there ≥3 positive examples?
- [ ] Are there ≥2 negative examples?
- [ ] Are there ≥2 edge cases?
- [ ] Is decision_trace required in every output?
- [ ] Are ≥5 drift prevention mechanisms enabled?

### After Writing

- [ ] Does the prompt contain ANY prose paragraphs? (must be 0)
- [ ] Does the prompt use ANY vague verbs? (must be 0)
- [ ] Does the prompt have ANY implicit enumerations? (must be 0)
- [ ] Can every output field be validated programmatically?
- [ ] Would the same input produce the same output on re-run?
- [ ] Is the error format structured (not conversational)?
- [ ] Does every definition include IS-NOT?
- [ ] Do all examples (positive, negative, edge) produce outputs consistent with defined validation gates and regex patterns?
- [ ] Is step ordering consistent? (no step validates a format that a later step would change)

---

## Structural Completeness Check

All 11 sections must be present (or explicitly `n/a`):

1. `prompt_metadata` — id, version, status, author, changelog
2. `identity` — role, role_constraints, persona, authority_model
3. `mission` — objective, scope (in/out), gray_zone_policy, success/failure criteria
4. `input_rules` — accepted_sources, rejected_sources, validation, policies
5. `decision_procedure` — steps (numbered), branching, termination, pre/post conditions
6. `output_contract` — format, schema (fields with types), decision_trace, forbidden
7. `constraints` — hard, soft, performance, ethical
8. `drift_prevention` — ≥5 mechanisms from the catalog
9. `error_handling` — error_format, escalation_policy, retry_policy
10. `acknowledgment_protocol` — on_receipt, on_ambiguity, on_scope_violation
11. `examples` — positive (≥3), negative (≥2), edge_cases (≥2)

Optional but recommended:
- `testing` — test_cases, regression_tests, adversarial_tests

---

## Deterministic Verb Reference

### Allowed Verbs

```yaml
classification: [classify, categorize, match, assign, label]
extraction:     [extract, parse, identify, isolate, select]
validation:     [validate, verify, check, confirm, assert]
transformation: [convert, transform, map, translate, normalize]
aggregation:    [count, sum, average, merge, combine, deduplicate]
control_flow:   [halt, continue, skip_to, retry, emit, reject, return]
comparison:     [compare, diff, rank, sort, filter]
```

### Forbidden Verbs

```
consider
think about
explore
try
attempt
look into
ponder
brainstorm
feel free to
you might want to
```

### Forbidden Phrases (Implicit Enumerations)

```
include          → replace with exhaustive list
such as          → replace with exhaustive list
for example      → replace with exhaustive list
e.g.             → replace with exhaustive list
etc.             → replace with exhaustive list
and more         → replace with exhaustive list
among others     → replace with exhaustive list
various          → replace with specific count + list
some             → replace with specific count + list
several          → replace with specific count + list
many             → replace with specific count + list
```

### Forbidden Hedging Words

```
might
could
perhaps
maybe
possibly
probably
generally
typically
usually
often
sometimes
```

---

## Error Type Enum

The `error_type` field must use one of these values:

```yaml
error_types:
  - missing_input      # required field was absent
  - invalid_input      # field present but wrong type/format
  - ambiguous_input    # field present but meaning unclear
  - out_of_scope       # request is outside agent's scope
  - gate_failure       # validation gate did not pass
  - processing_error   # step failed during execution
  - conflict_detected  # contradictory data found
  - unknown_value      # value not in any known enum
```

---

## Validation Gate Types

```yaml
gate_types:
  - enum_check:         "value is in allowed set"
  - regex_check:        "value matches pattern"
  - path_check:         "hierarchical path is valid"
  - conflict_check:     "no contradictions in output"
  - completeness_check: "all required fields present"
  - range_check:        "numeric values within bounds"
  - referential_check:  "referenced IDs exist"
```
