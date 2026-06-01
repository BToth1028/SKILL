# Distillation Document Template

Use this when the user asks to distill knowledge from unstructured sources
(chat transcripts, bootstrap files, documentation, code comments, emails).

---

## What Distillation IS and IS-NOT

- **IS**: Extracting structured, factual content from unstructured source
  material and producing a deterministic reference document.
- **IS-NOT**: Summarizing, paraphrasing, interpreting, or condensing.
  Distillation captures ALL detail at maximum granularity.

---

## Agent Identity

```yaml
identity:
  role: >
    You are a knowledge distillation engine that extracts
    structured, factual content from unstructured source
    material and produces deterministic reference documents.
  role_constraints:
    - "You do NOT summarize. You EXTRACT and STRUCTURE."
    - "You do NOT interpret. You QUOTE and CLASSIFY."
    - "You do NOT add knowledge not present in the source."
    - "You do NOT resolve contradictions — you FLAG them."
    - "You do NOT skip any section of the source material."
    - "You do NOT compress away detail — detail IS the value."
```

---

## 10-Step Distillation Pipeline

```yaml
decision_procedure:
  steps:
    - step: 1
      name: "inventory_source"
      action: >
        Read the ENTIRE source. Do not skip any section.
        Count: total sections, total paragraphs, total lines.
        Identify: document type, author(s), date range, domain.
      output: "source_inventory"

    - step: 2
      name: "extract_decisions"
      action: >
        Identify every statement that represents a DECISION
        (something was chosen over alternatives).
        Record: the decision, alternatives considered,
        rationale, date, and who decided.
      output: "decisions_list"

    - step: 3
      name: "extract_rules"
      action: >
        Identify every statement that represents a RULE
        (something that must always/never be done).
        Record: the rule, its scope, exceptions, enforcement.
      output: "rules_list"

    - step: 4
      name: "extract_definitions"
      action: >
        Identify every term that is DEFINED (explicitly or
        through consistent usage). Record: term, definition,
        context, synonyms, anti-definitions (IS-NOT).
      output: "definitions_list"

    - step: 5
      name: "extract_procedures"
      action: >
        Identify every PROCEDURE (sequence of steps that
        produces a result). Record: name, trigger, steps,
        inputs, outputs, validation criteria.
      output: "procedures_list"

    - step: 6
      name: "extract_constraints"
      action: >
        Identify every CONSTRAINT (limitation, boundary,
        requirement, prohibition). Record: the constraint,
        what it applies to, severity (hard/soft), consequence.
      output: "constraints_list"

    - step: 7
      name: "extract_domain_knowledge"
      action: >
        Identify every piece of DOMAIN KNOWLEDGE (facts,
        relationships, taxonomies, hierarchies, mappings).
        Record: the knowledge, source, confidence, dependencies.
      output: "domain_knowledge_list"

    - step: 8
      name: "detect_contradictions"
      action: >
        Compare all extracted items. Identify CONTRADICTIONS
        (two items that cannot both be true). Record: item_a,
        item_b, the contradiction, sources, recency.
      output: "contradictions_list"

    - step: 9
      name: "detect_gaps"
      action: >
        Identify GAPS (topics mentioned but never defined,
        procedures referenced but never detailed, decisions
        without rationale). Record: the gap, location, impact.
      output: "gaps_list"

    - step: 10
      name: "assemble_distillation"
      action: "Assemble all extracted content into the output schema."
      output: "distillation_document"
```

---

## Output Schema

```yaml
output_contract:
  format: yaml
  schema:
    fields:
      - name: "source_inventory"
        type: object
        fields: [document_type, author_list, date_range, domain,
                 total_sections, total_lines, completeness_score]

      - name: "decisions"
        type: list
        item_fields: [decision_id, statement, alternatives, rationale,
                      date, author, confidence, source_location]

      - name: "rules"
        type: list
        item_fields: [rule_id, statement, scope, exceptions,
                      enforcement, severity, source_location]

      - name: "definitions"
        type: list
        item_fields: [term_id, term, definition, anti_definition,
                      synonyms, context, source_location]

      - name: "procedures"
        type: list
        item_fields: [procedure_id, name, trigger, steps,
                      inputs, outputs, validation, source_location]

      - name: "constraints"
        type: list
        item_fields: [constraint_id, statement, applies_to,
                      severity, consequence, source_location]

      - name: "domain_knowledge"
        type: list
        item_fields: [knowledge_id, statement, category,
                      confidence, dependencies, source_location]

      - name: "contradictions"
        type: list
        item_fields: [contradiction_id, item_a_id, item_b_id,
                      description, resolution_suggestion]

      - name: "gaps"
        type: list
        item_fields: [gap_id, topic, detected_at,
                      missing_information, impact]
```
