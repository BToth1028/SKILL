---
name: research-playbook-builder
description: >-
  Authors a new reusable_research_procedure YAML playbook (same structural
  vocabulary as ai_research_playbook.yaml / n8n_research_playbook.yaml):
  tiered source_registry, search_templates, decision_procedure, validation_gates,
  and output_contract. Use when the user asks to create, scaffold, extend, or
  refresh a topic research playbook, source map, or "paste into assistant"
  investigation procedure — including domain packs (utilities, regulators, OSS,
  vendor docs).
disable-model-invocation: true
---

# Research playbook builder

## Goal

Produce a **single complete YAML playbook file** (`*_research_playbook.yaml`) whose shape matches the **43.02 research commands**:

- Canonical references: `@40-49-ai-agents-and-prompts/43-rules-skills-subagents/43.02-commands/research/ai/playbook/ai_research_playbook.yaml` and `.../n8n/playbook/n8n_research_playbook.yaml`.

The playbook is **not** a prose article. It is a **reusable procedure** another agent or human executes: variables → authority model → tiers → searches → synthesized output shape.

## When invoked

1. Confirm **topic**, **primary jurisdiction or product facet** (if any), optional **SUBTOPIC**, **`YEAR_HINT`** (default from user environment date), and **output path** (see Placement).
2. If the topic is ambiguous, **one** clarifying question only (≤5 bullets), per the acknowledgment pattern in the reference playbooks.
3. Run the **internal authoring passes** below, then **emit YAML**.

## Internal authoring passes (Engines research-chain borrow)

Borrow structure from consolidated multi-step prompts (continuity locks, ontology-first), but **publish only YAML**:

**Pass A — Scope pin**

- State the **system boundary**: in-scope regimes, markets, geography, excluded adjacent topics.
- Choose the **primary facet variable** name to match domain shape:
  - Vendor/product stacks → `PRIMARY_PRODUCT` + `_enum`.
  - Platform surfaces → `PRIMARY_SURFACE` + `_enum`.
  - Regulatory or industry regimes → **`PRIMARY_REGIME`** (or domain-specific label) + closed `_enum`.

**Pass B — Authority topology**

- List **tier_1**: statutes, CFR/eCFR anchors, regulators’ own handbooks, standards bodies, forms that define accounting structure (not commentary).
- **Never invent URLs.** If unsure, emit `manual_search:` with precise query strings instead of fake links.
- **Pass C — Expansion**
  - `tier_2_curated_repos`: handbooks, form instructions, ISA/EPRI/EEI-class references only when they are durable public locations.
  - `tier_3_community_zeitgeist`: forums, Reddit, vendor blogs — clearly labeled.

**Pass D — Operations**

- `search_templates`: copy-paste literals using `{TOPIC}`, `{SUBTOPIC}`, `{YEAR_HINT}`, `{PRIMARY_*}` placeholders.
- `decision_procedure`: mirror steps 1–6 pattern from AI/n8n (fill_variables → open_tier_1 → search → triangulate tier_3 cap → conflicts → emit_output_contract).
- `validation_gates` + `failure_criteria` aligned with the domain.

## Required YAML top-level skeleton

Every playbook **must** include these keys (order flexible; omit only if genuinely inapplicable, and justify in `prompt_metadata.note`):

```yaml
prompt_metadata:
  id: <topic-kebab>-research-playbook-v1
  version: "1.0.0"
  kind: reusable_research_procedure
  intended_use: >-                   # Paste / @reference use; replace variables first
  modeled_on: >-                     # Optional pointer, e.g. ../../ai/playbook/ai_research_playbook.yaml
  yaml_indent: spaces_required_for_parsers
  note: This file uses 2-space indentation; YAML 1.2 parsers reject tab-indented files.

variables:
  TOPIC: ""
  <PRIMARY_*>: ""
  SUBTOPIC: ""
  YEAR_HINT: "2026"
  <PRIMARY_*>_enum: []              # Closed list tuned to topic

identity:
  role: research_synthesizer
  authority_model: >-               # Official > handbook > tertiary > zeitgeist
  non_goals:
    - invent_sources
    # ... domain specifics

mission:
  objective: >-
  success_criteria: []
  failure_criteria: []

url_redirect_notes: >-              # Mirrors, mergers, superseded CFR paths

source_registry:
  tier_1_official: {}               # Group by facet (see n8n playbook nesting)
  tier_2_curated_repos: []          # name, url, use_case per item where applicable
  tier_3_community_zeitgeist: {}    # Mirrors n8n: forums, Reddit, aggregator limits

determinism_note: >-               # Pin versions, filings, CFR snapshots, GAAP taxonomy versions

search_templates:
  web: []
  github_code: []                   # Omit entire key if pointless for topic

decision_procedure: []             # Ordered steps with action/input/output/rules

output_contract:
  format: markdown
  sections: []
  decision_trace_required: true
  forbidden: []

validation_gates:
  - gate: G1
    check: <domain-specific tier-1 obligation>

acknowledgment_protocol:
  if_topic_ambiguous: ask_one_clarifying_block_max_five_bullets
  if_sources_conflict: report_conflict_and_cite_both_with_dates  # cite both when regs disagree

examples:
  positive: []
  negative: []
```

Mirror **optional** extras from `n8n_research_playbook.yaml` **only when they fit**: additional `search_templates` channels (`npm`, `reddit`, agency portals), richer `tier_3` nesting, conflict-resolution rules inside `decision_procedure`.

## Hard rules

- **YAML**: 2-space indent, UTF-8, no tabs. Double-quote strings that embed quotes or colon-heavy prose.
- **Links**: Prefer `https://` government or vendor hosts; mark mirrors (`mirror:`) like `ai_research_playbook.yaml` when stable.
- **No invented specificity**: Unknown form numbers → `manual_search:` not a guessed URL path.
- **Zeitgeist cap**: Procedures that lean on bloggers or creators must cite `limit:` under tier_3 and forbid presenting them as authoritative for accounting/regulatory conclusions.

## Placement (JDex canonical)

Author new topical playbooks under:

`40-49-ai-agents-and-prompts/43-rules-skills-subagents/43.02-commands/research/<topic-slug>/playbook/<descriptive>_research_playbook.yaml`

Keep **mirror/junction discipline** documented in `@40-49-ai-agents-and-prompts/43-rules-skills-subagents/43.02-commands/README.md` (profile pickups are mirrors of this tree).

After writing under `C:\dev`, record any **novel subfolder class** precedence if your workspace gates that (normally `research/<topic-slug>/` beside `ai/` and `n8n/` is acceptable as command sub-structure).
