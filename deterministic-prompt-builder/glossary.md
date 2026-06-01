# Glossary — Key Terms (IS / IS-NOT Format)

Reference this file when the user asks about terminology, or when
generating a prompt that needs a glossary section.

---

```yaml
glossary:

  - term: "prompt"
    is: "text you give to an AI model to control its output"
    is_not: "a question you ask a person; a search query; a command in a terminal"

  - term: "system prompt"
    is: "background instructions that define the agent's identity and rules; set once per session"
    is_not: "the user's message; a one-time setup that can be ignored later"

  - term: "context window"
    is: "the total amount of text the model can see at once (prompt + conversation)"
    is_not: "the model's memory; permanent storage; something that grows without limit"

  - term: "token"
    is: "a piece of a word (roughly 3/4 of a word in English)"
    is_not: "a character; a word; a sentence"

  - term: "deterministic"
    is: "producing the same output for the same input, every time"
    is_not: "rigid or inflexible (structure enables precision, not limitation)"

  - term: "drift"
    is: "gradual deviation from intended behavior over the course of a conversation"
    is_not: "a sudden error; a crash; a bug in the code"

  - term: "hallucination"
    is: "when the model states something as fact that is not true"
    is_not: "a lie (the model has no concept of truth); a bug (it is working as designed)"

  - term: "few-shot examples"
    is: "concrete input→output pairs included in the prompt to show desired behavior"
    is_not: "training data; the model does not learn from them permanently"

  - term: "closed world assumption"
    is: "the rule that only explicitly stated things exist; anything not stated does not exist"
    is_not: "a limitation on reality; it is a limitation on what the SYSTEM considers real"

  - term: "canonical source"
    is: "the single, authoritative source of truth that wins all conflicts"
    is_not: "the most recent source; the most detailed source; the user's preference"

  - term: "validation gate"
    is: "a check that must pass before output is emitted"
    is_not: "a suggestion; a warning; something that can be overridden"

  - term: "YAML"
    is: "a data format that uses indentation to show hierarchy (key: value pairs)"
    is_not: "a programming language; code that executes; something only developers can use"

  - term: "enum (enumeration)"
    is: "a fixed, exhaustive list of all allowed values"
    is_not: "a list of examples; a suggestion of common values"

  - term: "schema"
    is: "the exact structure, field names, and types of an output"
    is_not: "a template; a suggestion; a rough outline"

  - term: "decision trace"
    is: "a log embedded in the output showing which rules and steps produced it"
    is_not: "an explanation for the user; reasoning; commentary"

  - term: "scope"
    is: "the defined boundary of what the agent will and will not do"
    is_not: "a guideline; a preference; something the user can override"

  - term: "anti-pattern"
    is: "a practice that seems helpful but actually causes problems"
    is_not: "a bug; an error; something that fails immediately (it fails slowly)"

  - term: "distillation document"
    is: "structured knowledge extracted from unstructured source material"
    is_not: "a summary; a paraphrase; a condensed version that loses detail"

  - term: "reverse engineering (documentation)"
    is: "extracting documentation from existing project artifacts"
    is_not: "hacking; decompiling; anything illegal or unethical"

  - term: "ground-floor research"
    is: "research that starts at absolute fundamentals and builds up layer by layer"
    is_not: "an overview; a summary; a quick introduction"

  - term: "attention (in transformers)"
    is: "how much weight the model gives to each token when generating output"
    is_not: "the model 'paying attention' like a person; it is a mathematical weight"
```
