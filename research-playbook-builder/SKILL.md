---
name: research-playbook-builder
description: >-
  Authors a new reusable_research_procedure YAML playbook (same structural
  vocabulary as ai_research_playbook.yaml / n8n_research_playbook.yaml):
  tiered source_registry, search_templates, decision_procedure, validation_gates,
  and output_contract. Use when the user asks to create, scaffold, extend, or
  refresh a topic research playbook, source map, or "paste into assistant"
  investigation procedure — including domain packs (utilities, regulators, OSS,
  vendor docs). Enforces precondition halts, URL verification-or-manual_search,
  mandatory YAML parse check after disk write, and JDex placement validation.
disable-model-invocation: true
---

# Research playbook builder

## Goal

Produce a **single complete YAML playbook file** (`*_research_playbook.yaml`) whose shape matches the **43.02 research commands**:

- Canonical references: `@40-49-ai-agents-and-prompts/43-rules-skills-subagents/43.02-commands/research/ai/playbook/ai_research_playbook.yaml` and `...@/n8n/playbook/n8n_research_playbook.yaml`.

The playbook is **not** prose. It is a **reusable procedure** another executor runs: variables → authority → tiers → searches → synthesized output shape.

---

## Preconditions (fail-closed before authoring)

Perform **once per invocation**, in strict order:

1. **Canon templates readable** — Read BOTH paths relative to workspace root `C:\dev\` using the identical relative leaf trail expressed with **`/` segment separators** (tools accept the same logical path spelled with `\` on Windows shells):
   - `40-49-ai-agents-and-prompts/43-rules-skills-subagents/43.02-commands/research/ai/playbook/ai_research_playbook.yaml`
   - `40-49-ai-agents-and-prompts/43-rules-skills-subagents/43.02-commands/research/n8n/playbook/n8n_research_playbook.yaml`  
   On **I/O failure after exactly one duplicated read**: **HALT** (`halt_reason: CANON_REFERENCE_UNREADABLE`). Deliver only the verbatim error + missing path list. Emit **zero** playbook body.

2. **Placement verifier available or substituted** — Before first filesystem write below `C:\dev\`, EITHER:
   - Run **`jd_validate_path(output_path)`** (jd-mcp / equivalent already permitted in session) **once** against the fully assembled path **OR**
   - Operator pastes verbatim tool output approving that exact path OR types `PLACEMENT_APPROVED_LITERAL_PATH=<exact path copied>` matching `output_path`.  
   If **none** obtained: **HALT** (`halt_reason: PLACEMENT_UNVERIFIED`) and output playbook **inside chat fences only** prefixed `UNSAVED_PLAYBOOK`; **do not** claim disk persistence.

---

## Tier-1 URL integrity (hard)

For every **`source_registry.tier_1_official`** descendant entry carrying a **`url:`** field valued as `http://` or `https://`:

1. Probe reachability using **HEAD**; **if HEAD unsupported by HTTP client**, use **GET**. Follow **one** redirect hop; no auth headers.
2. **If** terminal status ∉ **2xx** after **one** repeated probe → **strip** `url`; replace with **`manual_search:`** string `site:<hostname-from-failed-url> <TOPIC> <YEAR_HINT>` (hostname = registrable host extracted mechanically from the failed URL; no manual invention).

**Never** fabricate undocumented `url:` literals.

---

## When invoked

1. Execute §Preconditions successfully (else HALT table §Error protocol rows **E-CANON** / **E-PLACE**).
2. Confirm **TOPIC**, **primary facet slot** (`PRIMARY_PRODUCT` XOR `PRIMARY_SURFACE` XOR `PRIMARY_REGIME` XOR operator-supplied synonym recorded in `<PRIMARY_*>`), **SUBTOPIC** (empty string `""` allowed), **`YEAR_HINT`** (MUST equal operator session clock year from user_info when present; else ask for one **four-digit** year only), **`output_path`**.
3. If topic scope still ambiguous → execute **exactly one** clarification block **≤ 5 bullets** (pattern from canon AI playbook `acknowledgment_protocol`); unresolved → row **E-AMBIG** only.
4. Run **Passes A→D**, emit YAML, **`jd_validate_path` before write**, then §Post-write validation.

---

## Internal authoring passes A–D (Engines-derived; YAML-only emission)

Apply multi-pass discipline (ontology first); **published artifact = YAML playbook only**:

### Pass A — Scope pin

- Write **explicit system boundary**: regimes/geography/markets in scope vs excluded adjacencies.
- **Bind facet variable naming** (`PRIMARY_PRODUCT` \| `PRIMARY_SURFACE` \| `PRIMARY_REGIME` bespoke label) plus **closed** `<that>_enum` list keyed in variables.

### Pass B — Authority topology

- Enumerate authoritative **tier_1** anchors per §Tier-1 URL integrity before locking rows.
- **Never invent URLs** — unresolved authority → **`manual_search:`** stubs with site-scoping.

### Pass C — Expansion

- Produce `tier_2_curated_repos` with durable **`https`** rows only after §Tier-1 URL integrity (same HEAD/GET rule) **or** `manual_search`.
- Produce `tier_3_community_zeitgeist` with explicit **`limit:`** echoing canon playbooks labeling zeitgeist non-canon.

### Pass D — Operations

- Compose `search_templates` literal strings parameterized `{TOPIC}`, `{SUBTOPIC}`, `{YEAR_HINT}`, `{PRIMARY_*}`.
- Compose `decision_procedure` duplicated from AI/n8n ordering: fill_variables → tier_1 open → templated searches → tier_3 cap → conflict rules → emit_output_contract.
- Align `failure_criteria`/`validation_gates` to domain predicates.

---

## Required YAML top-level skeleton (keys mandatory shape)

Produce **every** top-level structural key listed here. Replace placeholder angle-bracket identifiers with literal operator choices. Populate empty collections **`[]`** / `{}` instead of omission where an array/map is stipulated.

Duplicate extra `search_templates` channel maps (`npm`, `reddit`, …) cloned from **`n8n_research_playbook.yaml` ONLY IF** the chosen facet identifier string literal (from variables) matches **regexp** `[Nn]odes|[Rr]epos|[Tt]emplate|[Mm][Cc][Pp]|[Gg]ithub` OR **TOPIC+SUBTOPIC concatenation** matches same regexp **case-insensitive**. Otherwise emit only `web` (+ `gov_document_portals` when Pass B enumerated government portals) sans vacuous clones.

```yaml
prompt_metadata:
  id: <topic-kebab>-research-playbook-v1
  version: "1.0.0"
  kind: reusable_research_procedure
  intended_use: >-
  modeled_on: "../../ai/playbook/ai_research_playbook.yaml"
  yaml_indent: spaces_required_for_parsers
  note: This file uses 2-space indentation; YAML 1.2 parsers reject tab-indented files.

variables:
  TOPIC: ""
  <PRIMARY_*>: ""
  SUBTOPIC: ""
  YEAR_HINT: "2026"
  <PRIMARY_*>_enum: []

identity:
  role: research_synthesizer
  authority_model: >-
  non_goals:
    - invent_sources

mission:
  objective: >-
  success_criteria: []
  failure_criteria: []

url_redirect_notes: >-

source_registry:
  tier_1_official: {}
  tier_2_curated_repos: []
  tier_3_community_zeitgeist: {}

determinism_note: >-

search_templates:
  web: []
  github_code: []

decision_procedure: []

output_contract:
  format: markdown
  sections: []
  decision_trace_required: true
  forbidden: []

validation_gates:
  - gate: G1
    check: <domain predicate>

acknowledgment_protocol:
  if_topic_ambiguous: ask_one_clarifying_block_max_five_bullets
  if_sources_conflict: report_conflict_and_cite_both_with_dates

examples:
  positive: []
  negative: []
```

Extra nested blocks inside `tier_3` / multi-channel mirrors follow **`n8n_research_playbook.yaml`** morphology only where Pass C enumerated matching surfaces.

---

## Hard rules

- **YAML**: 2-space indent, UTF-8, ASCII tab forbidden in file body.
- **Links**: Mirrors carry `mirror:` alias like AI playbook precedent.
- **No invented specificity** — unknown deterministic targets → **`manual_search:`** pseudo-field.
- **Zeitgeist**: third tier lists carry `limit:` echoing authoritative separation.

---

## Placement (deterministic subtree)

Compose path skeleton:

```
C:\dev\40-49-ai-agents-and-prompts\43-rules-skills-subagents\43.02-commands\research\<topic-slug>\playbook\<descriptive>_research_playbook.yaml
```

**`<topic-slug>` transform:** lowercase ASCII, trim; characters outside `[a-z0-9-]` rewritten to hyphen; collapse repeats; strip edge hyphens.

**Sibling anchor:** resultant directory **MUST** sit parallel to **`research\ai\playbook`** and **`research\n8n\playbook`** prefixes above.

Mirror/junction pickups per `@40-49-ai-agents-and-prompts/43-rules-skills-subagents/43.02-commands/README.md`.

**First-time `research\<topic-slug>\` subtree creation** under JDex-monitored workspace: operator explicit chat approval line `CREATE_TOPIC_SLUG=<topic-slug>` REQUIRED before mkdir / write beyond existing siblings; else **HALT** (`halt_reason: PRECEDENT_GATE`) quoting `AGENTS-01-dev.md §5` placement + precedent expectation.

---

## Post-write validation (mandatory)

After successful bytes-on-disk (`output_path`):

```text
python -c "import pathlib,yaml; p=pathlib.Path(r'<ABS_OUTPUT_PATH>'); yaml.safe_load(p.read_text(encoding='utf-8'))"
```

- Substitute **`<ABS_OUTPUT_PATH>`** with the concrete Windows absolute path string (escape embedded backslashes once for Python).
- Exit code **0** required → else **HALT** (`halt_reason: YAML_PARSE_FAIL`) printing **verbatim** Python traceback + line/column markers. **Do not** claim success while parse fails.

---

## Error protocol (enumerated deterministic halts)

Stable presentation **order:** Emit table rows **sorted ascending lexicographically** by the **`Code`** column string.

| Code | Predicate | Emitter action |
|------|-----------|------------------|
| **E-AMBIG** | Topic ambiguous after clarification | Single sentence HALT cite insufficient scope |
| **E-CANON** | Template read fails | Preconditions row 1 path list only |
| **E-PLACE** | Placement verifier missing + literal approval absent | Fence `UNSAVED_PLAYBOOK`; assert no disk commit |
| **E-PRECEDENT** | New slug folder sans `CREATE_TOPIC_SLUG` ACK | Quote AGENTS precedent gate; zero write |
| **E-YAML** | Post-parse failure | Stderr verbatim; forbid SUCCESS narrative |

Abort entire run upon first triggering row (**no partially written corrupt file retries without operator fresh approval**).

---

## Never_route (explicit refusal surfaces)

Produce **finding-style refusal** (**not disguised playbook content**) redirecting externally when:

| Class | Boundary |
|------|-----------|
| **Binding legal adjudication** beyond statute/registry citation assembly | Respond `NOT_IN_SCOPE_ROUTE_LEGAL_COUNSEL` verbatim |
| **Certified accountant / audit assertion** wording | Respond `NOT_IN_SCOPE_ROUTE_QUALIFIED_ACCOUNTANT` |
| **Privileged trade-secret / unpublished tariff line item** extrapolation | Respond `OPERATOR_SPECIFIC_DATA_REQUIRED` blocking inference |

Forbidden: invent factual account numbers absent CFR anchor rows.

Keep refusals **outside** playbook YAML emitted as deliverable (**chat-only**) **unless** `examples.negative[]` illustrative stub demands encoded refusal pattern verbatim.
