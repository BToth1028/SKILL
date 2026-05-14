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

## Scope contract (routing + drift guard)

### In scope

- Produce one `kind: reusable_research_procedure` YAML file matching the §Required YAML skeleton and canon **AI / n8n** playbook morphology.
- Bind **tier_1_official**, **tier_2_curated_repos**, **tier_3_community_zeitgeist**, **`search_templates`**, **`decision_procedure`**, **`validation_gates`**, **`output_contract`** to operator **TOPIC** + facet enums.
- Run §Tier-1 URL integrity probes before locking `url:` literals (or degrade to **`manual_search:`** per rule).

### Out of scope (route, do not playbook)

| Request class | Mandatory surface |
|---|---|
| Binding legal adjudication beyond citing published instruments | **`NOT_IN_SCOPE_ROUTE_LEGAL_COUNSEL`** chat-only refusal |
| Certified accounting / audited financial assertions | **`NOT_IN_SCOPE_ROUTE_QUALIFIED_ACCOUNTANT`** chat-only refusal |
| Trade-secret / non-public tariff mapping without operator-supplied rows | **`OPERATOR_SPECIFIC_DATA_REQUIRED`** chat-only refusal |

### Never

- Emit **uncited** binding legal conclusions inside the YAML deliverable.
- Emit **fabricated** `https://` **tier_1** rows that failed §Tier-1 URL integrity without conversion to **`manual_search:`**.
- Execute filesystem **write** under `C:\dev` without satisfying **`§PLACEMENT`** (canonical: **§Preconditions** item **2** only).
- Split or rename the §Required YAML skeleton across undocumented files (single deliverable file per invocation unless operator opens a tracked follow-up task).

---

## Preconditions (fail-closed before authoring)

Perform **once per invocation**, in strict order:

1. **Canon templates readable** — Read BOTH paths relative to workspace root `C:\dev\` using the identical relative leaf trail expressed with **`/` segment separators** (tools accept the same logical path spelled with `\` on Windows shells):
   - `40-49-ai-agents-and-prompts/43-rules-skills-subagents/43.02-commands/research/ai/playbook/ai_research_playbook.yaml`
   - `40-49-ai-agents-and-prompts/43-rules-skills-subagents/43.02-commands/research/n8n/playbook/n8n_research_playbook.yaml`  
   On **I/O failure after exactly one duplicated read**: **HALT** (`halt_reason: CANON_REFERENCE_UNREADABLE`). Deliver only the verbatim error + missing path list. Emit **zero** playbook body.

2. **Placement verifier available or substituted (`§PLACEMENT`)** — **Normative copy lives only in this bullet;** all other sections **cite `§PLACEMENT`** (no paraphrase of tool names or outcomes). Before **first** filesystem write below `C:\dev\` **for this invocation’s current `output_path` string**, EITHER:
   - Run **`jd_validate_path(output_path)`** (jd-mcp / equivalent already permitted in session) **at most once per distinct `output_path` string** (if the operator supplies a **different** path string mid-run **or** explicitly requests revalidation, treat that as **new** **`output_path`** **→** permit **one** fresh call **for that string only**) **OR**
   - Operator pastes verbatim tool output approving that exact path **OR** types `PLACEMENT_APPROVED_LITERAL_PATH=<exact path copied>` matching `output_path`.  
   If **none** obtained: **HALT** (`halt_reason: PLACEMENT_UNVERIFIED`; **Code `E-PLACE`**). Output playbook **inside chat fences only** prefixed `UNSAVED_PLAYBOOK`; **do not** claim disk persistence.

---

## Tier-1 URL integrity (hard)

For every **`source_registry.tier_1_official`** descendant entry carrying a **`url:`** field valued as `http://` or `https://`:

1. Probe reachability using **HEAD**; **if HEAD unsupported by HTTP client**, use **GET**. Follow **one** redirect hop; no auth headers.
2. **If** terminal status ∉ **2xx** after **one** repeated probe → **strip** `url`; replace with **`manual_search:`** string `site:<hostname-from-failed-url> <TOPIC> <YEAR_HINT>` (hostname = registrable host extracted mechanically from the failed URL; no manual invention).

**Never** fabricate undocumented `url:` literals.

---

## When invoked

1. Execute §Preconditions successfully (else HALT table §Error protocol rows **E-CANON** / **E-PLACE**).
2. Confirm **TOPIC**, **primary facet slot** (`PRIMARY_PRODUCT` XOR `PRIMARY_SURFACE` XOR `PRIMARY_REGIME` XOR operator-supplied synonym recorded in `<PRIMARY_*>`), **SUBTOPIC** (empty string `""` allowed), **`YEAR_HINT`** (MUST equal operator session clock year from user_info when present; else ask for one **four-digit** year only), **`output_path`**, optional booleans **`NEGATIVE_EMBED_ALLOWED`**, **`NETWORK_FLAG_IN_YAML`**, **`SINGLE_LETTER_TOPIC_OK`** (default **false** when unstated).
3. If topic scope still ambiguous → execute **exactly one** clarification block **≤ 5 bullets** (pattern from canon AI playbook `acknowledgment_protocol`); unresolved → row **E-AMBIG** only.
4. Run **Passes A→D**, emit YAML, **then satisfy `§PLACEMENT` immediately before first disk write** (if already satisfied for the same `output_path`, **do not** call **`jd_validate_path`** again), then §Post-write validation.

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
  # boundary_saturated: true   # required only when §L4-CMP row CMP-8 predicate is true; omit key when false
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

## Deterministic string measures (normative)

Use **one** executor-native definition consistently; **`python_here`** denotes Python **3.12+** semantics.

| Name | Definition |
|------|------------|
| **`utf8_byte_len(s)`** | **`len(s.encode('utf-8'))`** where **`s`** is the **delimiter-free** concatenation / substring **after** **`.strip()`** on each **`TOPIC` / `SUBTOPIC` / primary facet** fragment that the **CMP row** includes (`python_here`). |
| **`code_point_len(s)`** | **`len(s.strip())`** on a valid UTF-8–decoded Unicode string (`python_here`). **CMP rows** name the substring; **if** they name **`TOPIC`** or **`SUBTOPIC`**, **strip** **before** measure **unless** the row says otherwise. |

**Mandatory:** All **`CMP` rows**, **`E-NULL`**, **`E-TINY`**, **`E-BYTE`**, **`E-META`**, evaluation **§L4-CMP CMP-8** paragraph, **`TOPIC ∥ SUBTOPIC`**, and **`code_point_len`** / **`utf8_byte_len`** use **§Deterministic string measures** — **never** grapheme-cluster counts **unless** added as a **new numbered CMP row**.

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

**`halt_reason:` ↔ Code (biconditional equivalence for operator logs):**

| `halt_reason` | Code |
|---|---|
| **`CANON_REFERENCE_UNREADABLE`** | **E-CANON** |
| **`PLACEMENT_UNVERIFIED`** | **E-PLACE** |
| **`PRECEDENT_GATE`** | **E-PRECEDENT** |
| **`YAML_PARSE_FAIL`** | **E-YAML** |

### L4-CMP edge ↔ halt mapping (closed 8-tuple)

**Evaluation order (deterministic):** Test **CMP-1 → CMP-7** **preflight** in **numeric order**; **first** true row **latches** its mapped **Code** and **skips** remaining **CMP-1–7** tests. Separately (**post-compose**, immediately before disk write intent), evaluate **CMP-8** once **only when** **`utf8_byte_len(TOPIC ∥ SUBTOPIC) == 8192`** (see **§Deterministic string measures**); **`CMP-8` predicate true** iff that length equality holds **and** (`prompt_metadata.boundary_saturated` **absent** OR **not** YAML boolean **`true`**).  
**Independent channel:** §Tier-1 URL integrity transport faults invoke **`E-NET`** when the HTTP client surfaces **socket / DNS / TLS handshake** failure **before** a terminal status code — orthogonal to CMP latches except both may surface text in same operator turn **lex-sorted by Code**.

| CMP | Stress |
|:-:|---|
| **1** empty / null-like | **`TOPIC` AND `SUBTOPIC` BOTH** zero-length **after ASCII trim AND collapse of internal ASCII whitespace runs** → **cannot** distill scope (**else** skip row). |
| **2** malformed / corrupt payload | **Path character grammar (string-only; no `resolve()`, no disk touch):** let **`p_norm = output_path.strip().replace('/', '\\')`**. Predicate **true** if **any**: (i) **`p_norm`** empty; (ii) **`U+0000` ∈ `output_path`**; (iii) **any forbidden filename character** ∈ **`output_path`**, forbidden set **`{ U+003C, U+003E, U+0022, U+007C, U+003F, U+002A }`** (ASCII **less-than, greater-than, quotation mark, vertical bar, question mark, asterisk**); (iv) **`local-drive colon discipline`:** iff **`not p_norm.startswith('\\\\')`** **and** **`p_norm`** matches **`(?i)^[a-z]:[\\/]`** (drive letter + colon + path separator), then **`output_path`** **must contain exactly one** **`U+003A` (colon)** — otherwise predicate **true** (reject **`C:stream`**, multi-colon quirks). Paths starting **`\\\\`** (**UNC**, **`\\?\`**, etc.) **skip clause (iv)**. **JDex / `C:\dev` conformance** is **solely `§PLACEMENT` / `jd_validate_path`** — **CMP‑2 does not replicate it.** |
| **3** boundary | **`YEAR_HINT` parses to integer ∉ closed range `1900..2099`**. |
| **4** wrong-type | `user_info` **omits** clock year **and** operator-supplied `YEAR_HINT` is **not** **exactly** `/^[0-9]{4}$/` ASCII. |
| **5** maximum-size | Let **`s5 = TOPIC.strip() ∥ SUBTOPIC.strip() ∥ v₁ ∥ v₂ ∥ v₃`** where **`v₁,v₂,v₃`** are **`PRIMARY_PRODUCT.strip()`**, **`PRIMARY_SURFACE.strip()`**, **`PRIMARY_REGIME.strip()`** in **that order**, each **omitted if empty** after strip. **`utf8_byte_len(s5) > 8192`**. |
| **6** minimal-size | **`code_point_len(TOPIC)==1`** **and** **`SUBTOPIC.strip()` empty** **and** Pass A **would** emit **zero** in-scope regime nouns **but** operator has **not** confirmed intent `SINGLE_LETTER_TOPIC_OK=true`. |
| **7** missing required fields | **>1** of (`PRIMARY_PRODUCT`,`PRIMARY_SURFACE`,`PRIMARY_REGIME`) carrying **non-empty** symbolic bindings after trim (facet XOR violation). |
| **8** exact boundary coincidence | **Post-compose only:** **`utf8_byte_len(TOPIC ∥ SUBTOPIC) == 8192`** **and** (`prompt_metadata.boundary_saturated` **absent** OR **not** YAML boolean **`true`**) → latch **`E-META`**. |

| Code | Predicate | Emitter action |
|------|-----------|------------------|
| **E-AMBIG** | Topic ambiguous after clarification | Single sentence HALT cite insufficient scope |
| **E-BOUND** | Rows **CMP-3** or **CMP-4** latch | Deliver **exactly one** corrective prompt repeating failing predicate + permissible closed response shape |
| **E-BYTE** | Row **CMP-5** latch | Demand operator partition strings so reconstructed **`utf8_byte_len(s5)`** (CMP‑5 formulation) **`≤ 8192`** across the merge plan (stable merge ID in chat header) |
| **E-CANON** | Template read fails | Preconditions row 1 path list only |
| **E-MALPATH** | Row **CMP-2** latch | HALT verbatim illegal path excerpt + forbids disk write |
| **E-META** | **CMP-8** latch | Insert `prompt_metadata.boundary_saturated: true` + re-run §Post-write validation (**no** `REWRITE_ACK` if zero prior successful bytes) |
| **E-NET** | Transport failure during §Tier-1 URL integrity | Freeze new `url:` locks; downgrade **all** pending unproven URLs this pass to **`manual_search:`** stubs per §Tier-1 URL integrity; **do not HALT** if ≥1 playbook section still producible (**degraded fidelity flag** boolean `NETWORK_DEGRADED=true` in operator chat header only, **not** inside YAML unless operator sets `NETWORK_FLAG_IN_YAML=true`) |
| **E-NULL** | Row **CMP-1** latch | Prompt once for replacement string **`s`** (**prefer** non-empty **`TOPIC`**; else materially distinct **`SUBTOPIC`**) such that **`code_point_len(s) ≥ 8`** |
| **E-PLACE** | Placement verifier missing + literal approval absent | Fence `UNSAVED_PLAYBOOK`; assert no disk commit |
| **E-PRECEDENT** | New slug folder sans `CREATE_TOPIC_SLUG` ACK | Quote AGENTS precedent gate; zero write |
| **E-TINY** | Row **CMP-6** latch | One prompt: supply `SINGLE_LETTER_TOPIC_OK=true` **or** expand **TOPIC** / **SUBTOPIC** to **`code_point_len ≥ 2`** **or** enumerate Pass A regime noun |
| **E-XOR** | Row **CMP-7** latch | Listing conflicting primaries verbatim; forbid emission until XOR repaired |
| **E-YAML** | Post-parse failure | Stderr verbatim; forbid SUCCESS narrative |

Abort / **HALT** (no playbook file bytes **except** `UNSAVED_PLAYBOOK` fence where listed) on first truth of: **E-AMBIG**, **E-BYTE**, **E-CANON**, **E-MALPATH**, **E-PLACE**, **E-PRECEDENT**, **E-YAML**.

**Recoverable (one corrective cycle then re-enter §When invoked step 2 sans partial disk artifact):** **E-NULL**, **E-BOUND**, **E-TINY**, **E-XOR**, **E-META**.

**Degrade without abort:** **E-NET** — complete YAML with `manual_search:` substitutions per rule.

**No destructive on-disk rewrite retries** without **`REWRITE_ACK=<path>`** operator line.

---

## Never_route (explicit refusal surfaces)

Produce **finding-style refusal** (**not disguised playbook content**) redirecting externally when:

| Class | Boundary |
|------|-----------|
| **Binding legal adjudication** beyond statute/registry citation assembly | Respond `NOT_IN_SCOPE_ROUTE_LEGAL_COUNSEL` verbatim |
| **Certified accountant / audit assertion** wording | Respond `NOT_IN_SCOPE_ROUTE_QUALIFIED_ACCOUNTANT` |
| **Privileged trade-secret / unpublished tariff line item** extrapolation | Respond `OPERATOR_SPECIFIC_DATA_REQUIRED` blocking inference |

Forbidden: invent factual account numbers absent CFR anchor rows.

**Refusal transport rule:** Structured refusals from §Scope contract **Out of scope** routes **never** occupy `identity`, `mission`, or **`source_registry`** except as **opaque quoted string blobs** inside `examples.negative[]` **only when** operator predeclares `NEGATIVE_EMBED_ALLOWED=true` in chat **before** write. Default → refusals stay **chat-only**; YAML bytes contain **no** refusal tokens.
