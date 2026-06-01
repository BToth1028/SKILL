# Anti-Patterns — 12 Things That Make Prompts Fail

Use this reference during validation (STEP 2C) and as a self-check
before emitting any generated prompt (STEP 5).

---

## AP-01: Prose Instructions

```yaml
id: "AP-01"
name: "Prose Instructions"
symptom: "Instructions written as paragraphs instead of structured YAML."
why_it_fails: >
  Prose is ambiguous, skippable, and subject to interpretation.
  The model can skip over a sentence; it cannot skip a YAML field.
fix: "Convert all prose to YAML key-value pairs and lists."
detection: "Any instruction block that is a paragraph rather than YAML."
```

## AP-02: Vague Verbs

```yaml
id: "AP-02"
name: "Vague Verbs"
symptom: "Using verbs like consider, think about, explore, look into, try to."
why_it_fails: "These give the agent discretion. Discretion is the enemy of determinism."
fix: >
  Replace with deterministic verbs: classify, extract, match, count,
  list, compare, validate, emit, reject, halt, assign, label, map,
  normalize, parse, identify, isolate, select, convert, transform,
  merge, combine, deduplicate, sort, filter, diff, rank.
detection: "Scan for forbidden verbs (see quick-ref.md for the full list)."
```

## AP-03: Missing Negatives

```yaml
id: "AP-03"
name: "Missing Negatives"
symptom: "Defining what the agent SHOULD do without what it SHOULD NOT do."
why_it_fails: >
  Leaves the door open for unwanted behavior. The agent will fill
  undefined space with its training defaults.
fix: >
  For every in_scope item, add a corresponding out_of_scope item.
  For every definition, add an anti-definition (IS-NOT).
  For every positive example, add a negative example.
detection: >
  Check: is out_of_scope empty or shorter than in_scope?
  Does every definition have an is_not field?
```

## AP-04: Implicit Enumerations

```yaml
id: "AP-04"
name: "Implicit Enumerations"
symptom: "Using 'types include X, Y, Z' instead of 'types are: [X, Y, Z]'."
why_it_fails: >
  'include' implies there are more values. The agent may invent values
  beyond the listed ones.
fix: >
  Replace 'include', 'such as', 'for example', 'etc.', 'and more',
  'among others' with exhaustive closed lists. If the list is truly
  open-ended, state that explicitly and define the process for
  handling unknown values.
detection: "Scan for: include, such as, for example, e.g., etc., and more, among others."
```

## AP-05: No Output Schema

```yaml
id: "AP-05"
name: "No Output Schema"
symptom: "Telling the agent what to do without specifying exact output format."
why_it_fails: "Leads to inconsistent, unparseable responses."
fix: "Define exact schema with field names, types, ordering, and constraints."
detection: "Check: does output_contract.schema have field definitions?"
```

## AP-06: No Error Handling

```yaml
id: "AP-06"
name: "No Error Handling"
symptom: "Not specifying what the agent does when things go wrong."
why_it_fails: >
  Agent falls back to its training defaults, which are usually
  chatbot-style apologies: "I'm sorry, I couldn't..."
fix: "Define error schema and error policy for every failure mode."
detection: "Check: is error_handling section populated?"
```

## AP-07: No Validation Gates

```yaml
id: "AP-07"
name: "No Validation Gates"
symptom: "Emitting output without checking it against constraints."
why_it_fails: "The agent cannot self-correct if it does not self-check."
fix: "Add validation gates between processing and output emission."
detection: "Check: does every step have a validation field? Is there a final emit gate?"
```

## AP-08: Asking the Agent to 'Be Creative'

```yaml
id: "AP-08"
name: "Asking the Agent to Be Creative"
symptom: "Instructions containing 'be creative', 'use your judgment', 'feel free to'."
why_it_fails: "Determinism and creativity are opposites."
fix: >
  Replace 'be creative' with 'select from [option_list] based on
  [selection_criteria]'. Define the exact dimensions along which
  variation is permitted and the bounds of that variation.
detection: "Scan for: creative, judgment, feel free, up to you, as you see fit."
```

## AP-09: No Few-Shot Examples

```yaml
id: "AP-09"
name: "No Few-Shot Examples"
symptom: "Not providing concrete input → output examples."
why_it_fails: >
  The agent has to guess what you want instead of seeing what you want.
  Examples are the most powerful constraint mechanism after the schema.
fix: >
  Include minimum 3 positive examples, 2 negative examples,
  and 2 edge cases.
detection: "Check: does the examples section meet minimum counts?"
```

## AP-10: Mid-Level Granularity

```yaml
id: "AP-10"
name: "Mid-Level Granularity"
symptom: "Providing surface-level or summary information instead of exhaustive detail."
why_it_fails: >
  The agent fills gaps with training knowledge, which may be wrong,
  stale, or inconsistent with your domain.
fix: >
  For every concept, drill down until you hit atomic primitives
  that cannot be decomposed further. Provide ALL required knowledge
  in the prompt or context.
detection: "Check: are there any terms used but never defined?"
```

## AP-11: No IS-NOT Definitions

```yaml
id: "AP-11"
name: "No IS-NOT Definitions"
symptom: "Defining terms only by what they ARE, not what they ARE NOT."
why_it_fails: >
  Without negative definitions, the agent cannot distinguish the
  concept from similar concepts. It will conflate adjacent ideas.
fix: >
  For every definition, add an is_not field listing at least 2 things
  the term is commonly confused with, and why they are different.
detection: "Check: does every definition in the prompt have an is_not?"
```

## AP-12: Trusting Training Knowledge

```yaml
id: "AP-12"
name: "Trusting the Agent's Training Knowledge"
symptom: "Relying on the agent to 'know' things from its training."
why_it_fails: >
  Training knowledge is stale, incomplete, and may be wrong.
  It is the LOWEST priority source in the trust hierarchy.
fix: >
  Provide ALL required knowledge in the prompt or context.
  Set trust_hierarchy with training knowledge at level_5 (last).
detection: >
  Check: does the prompt provide all domain knowledge needed,
  or does it assume the agent already knows things?
```
