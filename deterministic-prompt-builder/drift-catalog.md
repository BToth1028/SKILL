# Drift Prevention Catalog — 10 Mechanisms

Every prompt must implement at least 5 of these 10 mechanisms.
The SKILL.md auto-selection logic picks defaults based on use case.

---

## DP-01: Identity Anchor

```yaml
id: "DP-01"
name: "Identity Anchor"
cost: "~50 tokens per restatement"
when_to_use: "long-session agents, stateful agents, high-stakes agents"

implementation:
  frequency: "every_3_turns"       # or: every_turn, every_n_turns, on_scope_change
  method: "active_generation"       # agent generates, not passively re-reads
  format: |
    IDENTITY_CHECK:
      role: [restate role in ≤15 words]
      constraints_active: [list top 3 constraints]
      scope_status: [in_scope | approaching_boundary | out_of_scope]

purpose: >
  Forces the agent to actively regenerate its identity in output tokens.
  Output token generation restores attention weights to the original
  instructions, counteracting attention decay over long conversations.
```

---

## DP-02: SCAN Protocol

```yaml
id: "DP-02"
name: "SCAN Protocol (Behavioral Scan)"
cost: "~20-300 tokens depending on level"
when_to_use: "long-session agents, stateful agents, high-stakes agents"

implementation:
  trigger: "before every task that modifies state or produces output"
  levels:
    - level: "FULL"
      token_cost: "~300 tokens"
      when: "critical tasks, state changes, complex operations"
      markers:
        - "SCAN_1: Does this task affect session state? Y/N + risk."
        - "SCAN_2: Am I about to violate any scope constraint? Y/N + which."
        - "SCAN_3: Does my output match the required schema? Y/N + diff."
        - "SCAN_4: Am I inventing any data? Y/N + what."

    - level: "MINI"
      token_cost: "~120 tokens"
      when: "medium tasks, lookups, classifications"
      markers:
        - "SCAN_1: Scope check. Y/N."
        - "SCAN_2: Schema check. Y/N."

    - level: "ANCHOR"
      token_cost: "~20 tokens"
      when: "between subtasks, trivial operations"
      markers:
        - "ROLE: [role in 5 words]. SCOPE: [in/out]."

    - level: "SKIP"
      when: "read-only, no-output operations"

  output_requirement: >
    SCAN answers MUST be in the agent's output text, NOT in internal
    reasoning/thinking. Token generation in output is what restores
    attention weights.

purpose: >
  Based on the DEV Community SCAN protocol. Agent answers behavioral
  markers BEFORE each task, which restores attention to instructions
  and forces explicit compliance checking.
```

---

## DP-03: Scope Fence

```yaml
id: "DP-03"
name: "Scope Fence"
cost: "0 tokens unless triggered"
when_to_use: "ALWAYS — baseline mechanism for every prompt"

implementation:
  on_out_of_scope_request:
    action: "REFUSE"
    format: |
      SCOPE_VIOLATION:
        request_received: "[the request]"
        violated_rule: "[specific out_of_scope item]"
        suggestion: "[closest in_scope alternative, if any]"
        status: REFUSED

  on_scope_creep:
    definition: >
      A series of in-scope requests that gradually moves the agent
      toward out-of-scope territory. Each individual request seems
      reasonable, but the cumulative effect is a scope violation.
    detection: >
      After every 5 turns, review the trajectory of requests and
      check whether the cumulative direction is moving toward
      out_of_scope items.
    action: "flag and warn, continue only if user confirms in-scope intent"

purpose: >
  Explicit in-scope and out-of-scope lists with structured refusal.
  The scope creep detection catches gradual drift that no individual
  request would trigger.
```

---

## DP-04: Vocabulary Lock

```yaml
id: "DP-04"
name: "Vocabulary Lock"
cost: "0 tokens unless triggered"
when_to_use: "classification agents, domain-specific agents, any prompt with defined terms"

implementation:
  definition: >
    Key terms defined in the prompt cannot be redefined by the user
    during the conversation. If the user uses a term differently
    than the prompt defines it, the agent uses the prompt definition.
  enforcement: |
    If user redefines a locked term:
      VOCABULARY_CONFLICT:
        term: "[the term]"
        prompt_definition: "[definition from prompt]"
        user_definition: "[how user used it]"
        resolution: "Using prompt definition per vocabulary_lock."

purpose: >
  Prevents semantic drift where the user gradually shifts the meaning
  of key terms, causing the agent to operate on redefined concepts
  without realizing the definitions have changed.
```

---

## DP-05: Schema Lock

```yaml
id: "DP-05"
name: "Schema Lock"
cost: "0 tokens unless triggered"
when_to_use: "ALWAYS — baseline mechanism for every prompt"

implementation:
  definition: >
    The output schema defined in the prompt cannot change during the
    conversation. The agent will not add fields, remove fields,
    rename fields, or change field types regardless of user requests.
  on_schema_change_request: |
    SCHEMA_LOCK_VIOLATION:
      requested_change: "[what user asked to change]"
      current_schema: "[field list]"
      status: REFUSED
      reason: "Output schema is locked per prompt specification."

purpose: >
  Prevents the output format from drifting as the conversation
  continues. Without schema lock, agents tend to add explanatory
  fields, drop "unimportant" fields, or reformulate outputs.
```

---

## DP-06: Decision Trace

```yaml
id: "DP-06"
name: "Decision Trace"
cost: "~100-200 tokens per output"
when_to_use: "ALWAYS — baseline mechanism for every prompt"

implementation:
  required: true
  in_every_output: true
  fields:
    - rules_applied: "list of rule IDs that produced this output"
    - steps_executed: "list of step numbers in order"
    - gates_passed: "list of gate names that passed"
    - inputs_used: "list of input fields consumed"
    - confidence: "enum: [deterministic, high, medium, low, insufficient]"

purpose: >
  Makes drift detectable after the fact. If the trace shows rules
  or steps that don't exist in the prompt, or if it omits rules
  that should have applied, drift has occurred. Also enables
  reproducibility — given the same input and the same trace,
  the output should be reconstructible.
```

---

## DP-07: Precedence Hierarchy

```yaml
id: "DP-07"
name: "Precedence Hierarchy"
cost: "0 tokens"
when_to_use: "ALWAYS — baseline mechanism for every prompt"

implementation:
  trust_hierarchy:
    - level_1: "prompt instructions (this document)"
    - level_2: "canonical_source data"
    - level_3: "derived_source data"
    - level_4: "user-provided context in conversation"
    - level_5: "agent's training knowledge (LOWEST priority)"

purpose: >
  Explicit ranking of instruction authority prevents the agent from
  treating all inputs as equally trustworthy. Without this, agents
  tend to elevate user requests above prompt instructions over time,
  especially when the user is persistent.
```

---

## DP-08: Scope Creep Detection

```yaml
id: "DP-08"
name: "Scope Creep Detection"
cost: "~100 tokens per check"
when_to_use: "long-session agents, agents with broad scope boundaries"

implementation:
  trigger: "every 5 turns"
  action: >
    Review the trajectory of the last 5 requests. Check whether
    the cumulative direction is moving toward out_of_scope items.
    If drift detected:
      SCOPE_CREEP_WARNING:
        trajectory: "[summary of last 5 requests]"
        direction: "[toward which out_of_scope item]"
        action: "Confirm in-scope intent to continue."

purpose: >
  Catches gradual drift that individual scope checks miss.
  A series of individually valid requests can cumulatively
  move the agent outside its scope. This mechanism watches
  the trajectory, not just individual requests.
```

---

## DP-09: Negative Examples

```yaml
id: "DP-09"
name: "Negative Examples"
cost: "0 tokens at runtime (cost is in prompt length)"
when_to_use: "ALWAYS — baseline mechanism for every prompt"

implementation:
  minimum_count: 2
  format: >
    Include examples of INCORRECT behavior in the examples section.
    Show the agent what drift looks like so it can recognize it.
  types:
    - "out-of-scope request → structured refusal"
    - "invalid input → structured error"
    - "ambiguous input → clarification request"
    - "request to change schema → schema lock refusal"

purpose: >
  Shows the agent what NOT to do. Without negative examples,
  the agent only knows what correct behavior looks like and
  may not recognize when it is drifting toward incorrect behavior.
```

---

## DP-10: Output Fingerprinting

```yaml
id: "DP-10"
name: "Output Fingerprinting"
cost: "~20 tokens per output"
when_to_use: "stateful agents, high-stakes agents, audit-required agents"

implementation:
  fields:
    - input_hash: "hash of the input that produced this output"
    - prompt_version: "version of the prompt spec"
    - timestamp: "ISO 8601 timestamp"
  purpose_in_trace: >
    Include input_hash in the decision_trace. This makes it
    possible to verify that the same prompt + input produces
    the same output. If the hash matches but the output differs,
    drift has occurred.

purpose: >
  Enables post-hoc reproducibility verification. By recording
  a fingerprint of the input alongside the output, auditors
  can verify that the agent's behavior was deterministic.
```
