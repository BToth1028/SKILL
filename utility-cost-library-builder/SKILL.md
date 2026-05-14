---
name: utility-cost-library-builder
description: >-
  Deterministic builder for Electric and Gas Utility (T&D) cost libraries using a
  normalized matrix cost model. Delivers seventeen logical surfaces (ADR-19 split
  storage): thirteen `.xlsx` workbook tabs plus four YAML-canonical files under
  `references/` (`ferc_accounts.yaml`, `wbs_ferc_linkage.yaml`, `permits.yaml`,
  `permit_eligibility.yaml`) whose matching workbook tabs are derived views only.
  Five orthogonal cost dimensions: physical assets (WBS-A, FERC-tagged), labor pools
  (WBS-B), permit catalog, FERC USoA catalog
  (with ferc_part ∈ {PART_101, PART_201} affiliation), and state_overlay
  (NY_PSC canonical + 8 adjacent NE state PUCs) — joined via the Construction Unit
  (CU) layer. Every L6 row, every CU, every permit assignment traces to 18 CFR
  Part 101 (Electric USoA) or 18 CFR Part 201 (Gas USoA) for federal Form 1 / Form 2
  reporting accuracy, with NY 16 NYCRR state-overlay handling for NY PSC-regulated
  utilities. Use when authoring WBS rows, defining CUs, applying burden loading,
  building the permit catalog, mapping WBS to FERC, or assembling the audit-ready
  Master Cost Library workbook for Northeast US Electric and Gas T&D capital projects.

  Triggers on: "build a CU", "add WBS row", "what FERC account", "burden rate",
  "T&D unit cost", "substation construction unit", "line construction unit",
  "BGR vs UGD", "ACQ acquisitions", "PDL allocation", "permit catalog",
  "permit eligibility", "WBS FERC linkage", "labor pool", "matrix cost model",
  "AACE 96R-18", "ISO-NE PP-4", "MISO MTEP", "NYISO Manual 23", "Article VII",
  "CPCN siting", "Siting Council certificate", any utility cost-WBS authoring
  question.
version: 4.0.0
status: active
schema: 4.0
last_revised: 2026-05-14
revision_reason: "v4 architectural expansion: 18 CFR Part 201 (Gas) activation; Order No. 898 (effective 2025-01-01) account corrections (351, 363, 158, 359.1, 372); state_overlay 5th matrix dimension; three-view accounting (estimating + capitalization + SETTLEMENT) for NYISO / ISO-NE / PJM monthly reconciliation; NY PSC 16 NYCRR overlay; cross-references to ferc-accounting-* canonical research at 47.01-generated-docs and 47.04-ontology-decision-traces. ADR-19 (v4.1 data layer): FERC_Accounts, WBS_FERC_Linkage, Permits, and Permit_Eligibility are YAML-canonical; workbook_schema `sheets` holds 13 xlsx tabs; derived review workbook emitted via build_review_v2.py (or successor)."
related_skills:
  - wbs-cu-builder           # internal validator for electric utility WBS dictionary
  - deterministic-prompt-builder  # source of P1-P8 principles and DP-01..DP-10
  - context-bootstrap        # session continuity for multi-session WBS builds
authority:
  canonical:
    - references/enums.yaml
    - references/definitions.yaml
    - references/workbook_schema.yaml
    - references/source_catalog.yaml
    - references/examples.yaml
    - references/ferc_accounts.yaml       # YAML-canonical per ADR-19
    - references/wbs_ferc_linkage.yaml  # YAML-canonical per ADR-19
    - references/permits.yaml            # YAML-canonical per ADR-19
    - references/permit_eligibility.yaml # YAML-canonical per ADR-19
    - 18 CFR Part 101                  # FERC Uniform System of Accounts (Electric — Federal Power Act)
    - 18 CFR Part 201                  # FERC Uniform System of Accounts (Natural Gas — Natural Gas Act) — NEW v4 per ADR-16
    - 18 CFR §367.3030                 # Service Company USoA (Account 303 parallel)
    - 7 CFR §1767.16                   # RUS Electric Plant Instructions (mirrors FERC)
    - 23 CFR Part 645 Subpart A        # Utility Relocations on federal-aid highways
    - FERC Order No. 898 (RM21-11)     # Final rule effective 2025-01-01; renewables/storage/RECs/computer/comms — NEW v4
    - 16 NYCRR Chapter VI              # NY PSC Uniform System of Accounts — NEW v4 per ADR-17
    - 16 NYCRR Part 167                # NY electric revenue accounts incl. ESCO separation (167.5/167.6)
    - 16 NYCRR Part 312                # NY gas revenue accounts incl. ESCO separation (312.5/312.6)
    - NY PSC Case 14-M-0450            # 2015-11-24 NY USoA comprehensive revision (effective 2016-01-01) — NEW v4
    - ISO-NE PP-4 Attachment D         # Cost Estimating Guidelines (10-category template)
    - NYISO Manual 23 / OATT §30.8     # Class Year Interconnection Facilities Study
    - PJM Manual 14B / 14C / 14G       # Regional Transmission Planning / Interconnection
    - MISO MTEP25 Transmission Cost Estimation Guide
    - AACE RP 96R-18                   # Cost Estimate Classification — Power Transmission
    - RUS Bulletin 1724E-200           # HV Transmission Line Design Manual
    - NESC (IEEE C2)                   # National Electrical Safety Code
    - IEEE C57.13 / C37.30 / 738 / 605 # equipment standards (terminology lock)
  derived:
    - workbook content (.xlsx) — tabs mirroring `external_files` are regenerated views; not authoritative vs YAML
    - all citations and decision traces
  conflict_precedence:
    - user turn instruction
    - 18 CFR Part 101 (Electric) / 18 CFR Part 201 (Gas) — per ferc_part affiliation
    - FERC Order No. 898 effective-date amendments
    - 16 NYCRR Chapter VI (when state_overlay = NY_PSC)
    - references/workbook_schema.yaml
    - references/ferc_accounts.yaml
    - references/wbs_ferc_linkage.yaml
    - references/permits.yaml
    - references/permit_eligibility.yaml
    - references/enums.yaml
    - references/source_catalog.yaml
    - ISO-NE PP-4 Attachment D / NYISO Manual 23 / PJM / MISO MTEP / AACE 96R-18
    - source content cited inline
  cross_referenced_research:
    # NEW v4 — research-compiler outputs feeding this skill (UUIDv7 traceable)
    - "C:\\dev\\40-49-ai-agents-and-prompts\\47-outputs-and-artifacts\\47.01-generated-docs\\ferc-accounting-brief-019e25c1e2f2.md"
    - "C:\\dev\\40-49-ai-agents-and-prompts\\47-outputs-and-artifacts\\47.01-generated-docs\\ferc-accounting-electric-verification-019e25c1e3bb.md"
    - "C:\\dev\\40-49-ai-agents-and-prompts\\47-outputs-and-artifacts\\47.01-generated-docs\\ferc-accounting-gas-universe-019e25c1e483.md"
    - "C:\\dev\\40-49-ai-agents-and-prompts\\47-outputs-and-artifacts\\47.04-ontology-decision-traces\\ferc-accounting-decision-register-019e25c1e099.yaml"
    - "C:\\dev\\40-49-ai-agents-and-prompts\\47-outputs-and-artifacts\\47.04-ontology-decision-traces\\ferc-accounting-provenance-manifest-019e25c1e22a.yaml"
---

# Utility Cost Library Builder v4 — Electric and Gas T&D Matrix Cost Model

> Version 4.0.0 — Gas activation, state_overlay 5th dimension, three-view accounting, Order 898 currency, ADR-19 split storage (four YAML-canonical surfaces). Read §17 (Resolved Architectural Decisions, especially ADR-16 through ADR-19) and §18 (Changelog) to understand what changed from v3 and why.

---

## 1. Session Mission

Build an audit-ready Utility (Electric T&D + Gas T&D) cost library using a normalized matrix accounting model. Every cost dollar is stamped with **five orthogonal coordinates** — physical asset (WBS-A), labor pool (WBS-B), permit constraints, FERC USoA account (with `ferc_part` ∈ {PART_101, PART_201}), and **state_overlay** (NY_PSC canonical; 8 adjacent NE state commissions; FEDERAL_ONLY default) — joined through the Construction Unit (CU) layer. The output is **split storage** (per ADR-19): **13** `.xlsx` tabs in the workbook schema (interactive authoring, rate libraries, audit artifacts) + **4** YAML-canonical files (`references/ferc_accounts.yaml`, `references/wbs_ferc_linkage.yaml`, `references/permits.yaml`, `references/permit_eligibility.yaml`) declared under `workbook_schema.yaml :: external_files`, **17 logical surfaces** total. Workbook tabs that mirror those four YAMLs are **derived views**—regenerate on demand (e.g. `build_review_v2.py`); edit the YAML, not the derived cells. The output (regardless of storage) holds:

- Every WBS-A leaf row carries a single primary FERC account (via a normalized join table, not a direct column).
- Every labor pool row lives in a separate WBS-B structure and carries **no** FERC tag.
- Every permit type lives in a separate catalog with explicit eligibility constraints describing which WBS-A asset types it can apply to.
- Every CU joins these five dimensions and computes both direct cost and burden-loaded total cost, with the loaded cost flowing to the destination FERC account via the matrix join.
- Every row traces to a cited authoritative source under the T1–T5 tier model.

The system is designed for **federal Form 1 reporting accuracy first**, project-controls visibility second, and AACE Class 5→Class 1 estimating fidelity third — in that order of precedence.

## 2. The Matrix Cost Model (foundational concept)

**v4 update:** Matrix model expanded from four orthogonal dimensions to **five** (added state_overlay per ADR-17). All four prior dimensions remain unchanged; the fifth is a new optional tag that records jurisdictional overlay applicability.

### 2.1 Five orthogonal dimensions (v4)

```
  ┌──────────────────────────────────────────────────────────────────┐
  │                    Construction Unit (CU)                        │
  │                  the matrix-join point                           │
  │                                                                  │
  │   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
  │   │  WBS-A   │    │  WBS-B   │    │ Permits  │    │   FERC   │   │
  │   │  Asset   │    │  Labor   │    │ Catalog  │    │   USoA   │   │
  │   │   side   │    │   side   │    │          │    │ Accounts │   │
  │   └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘   │
  │        │               │               │               │         │
  │        │ ┌─────────────┘               │               │         │
  │        │ │      ┌──────────────────────┘               │         │
  │        │ │      │       ┌──────────────────────────────┘         │
  │        ▼ ▼      ▼       ▼                                        │
  │      CU links to one WBS-A leaf, consumes N labor types,         │
  │      attaches M permits (with eligibility check), inherits       │
  │      FERC from WBS-A → FERC linkage                              │
  └──────────────────────────────────────────────────────────────────┘
```

Each labor hour (direct or indirect), each material dollar, each permit fee, each equipment hour gets stamped with all four coordinates at CU consumption time. Two rollup totals are computed simultaneously:

- **Roll up by WBS-A → FERC** = Form 1 plant-account totals (federal reporting view).
- **Roll up by WBS-B = Labor-spend by labor pool** (project-controls view).

These are the **same dollars seen through two lenses**. Classic matrix accounting.

**v4 — Fifth dimension (state overlay):** Every WBS-A leaf row, every CU, every estimate row may optionally carry a `state_overlay` tag identifying which state PUC regulates its booking. Canonical = NY_PSC (16 NYCRR); adjacent = NJ_BPU / PA_PUC / CT_PURA / MA_DPU / ME_PUC / VT_PUC / NH_PUC / RI_PUC; FEDERAL_ONLY = no overlay applies (federal Form 1 / Form 2 only). The overlay does NOT change the FERC account routing — it captures whether state-specific accounting requirements (RDM / EAM / REV / ESCO separation / PGA / GSC) layer onto the booking.

### 2.2 The closed-world dimensions

| Dimension | Entity tab (catalog) | Join tab (M:N) | What it answers |
|---|---|---|---|
| Physical asset | `Registry` (WBS-A) | — | What was built / acquired |
| Labor pool | `Labor_Pools` (WBS-B) | `Labor_Eligibility` | Who did the work, by craft category |
| Permit | `Permits` | `Permit_Eligibility` | What regulatory obligations enabled the work |
| FERC account | `FERC_Accounts` | `WBS_FERC_Linkage` | Where the cost lands in the federal chart of accounts |
| Cost unit | `Master_Cost_Units` (joins all four) | — | The unit of consumable scope and the matrix join point |

Every dimension is a **closed-world enumeration**. No row can reference a value that does not exist in its entity catalog. Adding a new value requires explicit user approval and triggers an enum-expansion review.

### 2.3 Two-view accounting (estimating vs. capitalization)

The matrix model accommodates the canonical two-view pattern observed across every industry source (ISO-NE PP-4 Att. D, NYISO Manual 23, MISO MTEP25, AACE 96R-18, Versant Power capitalization guidelines, every commercial estimating tool):

- **Estimating view** — soft costs (ROW, permits, application fees, studies, interconnection fees, third-party reports) are **visible WBS-A line items** under the `ACQ` (Acquisitions) branch. AACE Class 5 → Class 1 estimates require this itemization for accuracy and project control.
- **Capitalization view** — at booking, each cost rolls into the **physical plant account it enabled** per Electric Plant Instructions 3, 7, 8, 9. Account 303 (Miscellaneous Intangible Plant) is reserved for genuinely intangible items (patents, long-term franchises, organizational costs) — NOT a catch-all for soft costs.

The matrix model gives you both views from the same data: the WBS-A row provides the estimating-view itemization; the WBS_FERC_Linkage tab provides the capitalization-view rollup destination.

## 3. Architectural Principles

These eight principles are load-bearing. Every other rule in this skill flows from them. Violations are caught by validation gates G1–G19.

| # | Principle | Enforcement |
|---|---|---|
| P1 | **Two parallel WBS structures** — WBS-A (physical assets, FERC-tagged) is structurally separate from WBS-B (labor pools, FERC-free). They join only at the CU layer. | A_RULE_11; G9; G16 |
| P2 | **Normalized relational design** — every many-to-many relationship lives in a dedicated join tab with explicit eligibility rows. No denormalized comma-lists in cells. | A_RULE_12, A_RULE_13, A_RULE_14; G11, G14, G16 |
| P3 | **Closed-world enumeration** — every controlled vocabulary (L1–L6 codes, FERC accounts, permit IDs, labor classifications) is enumerated in `enums.yaml`. No invention. | DP-04; G7 |
| P4 | **FERC USoA as sole financial authority** — 18 CFR Part 101 is canonical. The WBS_FERC_Linkage tab is the single authority for which FERC account applies to which WBS-A row. No FERC column on Registry. | DP-07; G12, G13, G14, G15 |
| P5 | **CU as matrix join point** — Construction Units are the only place where multiple cost dimensions are joined. WBS rows do not directly reference each other's dimensions. | A_RULE_15 |
| P6 | **Eligibility constraints as first-class data** — when an entity (permit, labor type) can only attach to a subset of WBS-A codes, that subset lives in an explicit eligibility join, not as a comma-string attribute. | A_RULE_14; G11, G16 |
| P7 | **Two-view accounting** — every cost has an estimating-view representation (WBS-A line item) and a capitalization-view representation (FERC account via linkage). The two views must agree by construction. | G3 (no CBS in WBS), G13 |
| P8 | **6-level WBS depth** — the WBS hierarchy is L1–L6. L7-style data (assumptions, inclusions, exclusions, notes) lives in metadata columns on the L6 row, never as a 7th hierarchical level. | A_RULE_03; G1 |

## 4. Authority Model

### 4.1 Canonical sources, in precedence order

1. **The current user turn** (highest)
2. **18 CFR Part 101** (FERC Uniform System of Accounts) — the federal regulatory authority for plant-account classification. Non-negotiable.
3. **`references/workbook_schema.yaml`** — the output contract defining tab schemas, column types, gate requirements.
4. **`references/enums.yaml`** — the closed-world vocabularies.
5. **`references/source_catalog.yaml`** — source-tier rules and prioritization.
6. **Tier-1 supplementary authorities** (ISO-NE PP-4 Att. D, NYISO Manual 23, MISO MTEP25, AACE 96R-18, FERC eLibrary filings, state PUC orders) — for items not directly addressed by 18 CFR Part 101.
7. **Tier-2 industry standards** (EPRI, IEEE, NESC, RUS Bulletins, NECA, IBEW CBAs, BLS).
8. **Tier-3–5 sources** with their tier ceilings on confidence (see source_catalog.yaml).
9. **User-supplied unstructured input** — treated as untrusted unless cited.

### 4.2 What is canonical vs. derived

- **Canonical**: this `SKILL.md`, the five reference YAML files, 18 CFR Part 101.
- **Derived**: every row in every output workbook. Each derived row must trace to canonical authority via its `decision_trace` and `source_refs` columns.

### 4.3 Authority delegation to workbook tabs

In v3, several authority-bearing concepts moved out of `SKILL.md` and into the workbook tabs themselves to make them queryable closed-world data:

| Authority concept | Pre-v3 location | v3 location |
|---|---|---|
| FERC account definitions | In-skill prose tables | `FERC_Accounts` tab (verbatim from 18 CFR Part 101) |
| WBS-A → FERC mapping | `ferc_account` column on Registry | `WBS_FERC_Linkage` tab |
| Permit definitions | Implied via PDL.* WBS rows | `Permits` tab |
| Permit → WBS-A applicability | Implied / undefined | `Permit_Eligibility` tab |
| Labor classifications | `enums.yaml` only | `Labor_Pools` tab (WBS-B) + CBS in `Labor_Rates` |

This makes the skill thinner (it owns procedures and gates) and the workbook richer (it owns the data).

## 5. Input Rules

### 5.1 Sources Claude MAY use (with confidence ceilings)

- **T1 (HIGH ceiling)** — Federal regulations (18 CFR Part 101, 23 CFR Part 645, 47 CFR), FERC eLibrary, state PUC orders / rate cases, ISO/RTO tariffs (PJM Manual 14B/14C/14G, ISO-NE PP-4, NYISO Manual 23), MISO MTEP guides, codified standards (NESC, IEEE C57/C37/738/605, RUS Bulletins 1724E series), state DOT specifications (PennDOT 408, NYSDOT, etc.).
- **T2 (HIGH ceiling)** — AACE RP 96R-18 (for transmission lines specifically; 56R-08 was the older general electric guidance), EPRI publications, NECA Manual of Labor Units, IBEW/NECA CBAs (Northeast Locals 102, 126, 269, 351, 358, 654, 1249), Davis-Bacon WDOL, BLS OES (NAICS 22/237/238), state prevailing-wage filings.
- **T3 (MEDIUM ceiling)** — RSMeans (Gordian), HeavyBid (HCSS), Sage Estimating, Primavera P6, ENR CCI/BCI indices, BLS PPI/CPI, LME/COMEX commodity indices.
- **T4 (MEDIUM ceiling)** — Northeast EPC contractor public capability docs (Quanta, MasTec, MYR, Pike, Henkels & McCoy, Asplundh, InfraSource, PAR Electrical), vendor scope language only (no pricing — Hubbell, S&C, ABB, Eaton, GE).
- **T5 (LOW ceiling)** — Reddit (r/lineman, r/utility, r/electricians), Mike Holt Forums, Contractor Talk, LinkedIn discussions, YouTube tutorials, GitHub utility cost-model repos (NREL/reV, catalyst-cooperative/PUDL, NREL/ReEDS, PyPSA), ToS-compliant scraped public pages.

### 5.2 Sources Claude MUST ignore

- Paywalled content without a verified license.
- Marketing pages (contractor SEO, vendor brochures with pricing).
- Aggregators (PrivCo-style, ZoomInfo, Crunchbase commercial-tier) without a primary citation.
- AI-generated content as a primary basis.
- ToS-violating scraped pages.

### 5.3 The No-Invention Rule

If a FERC account, WBS code, permit ID, or labor classification does not appear in the closed-world enums and the user has not explicitly approved its addition, the system MUST HOLD and ask **exactly one** clarifying question or emit a structured error. Inventing values silently is the most common drift failure mode for cost-WBS systems.

## 6. Output Contract — Split Storage (13 xlsx tabs + 4 YAML-canonical files)

### 6.1 Surface inventory (canonical order)

**xlsx tabs** — interactive authoring (Registry, Master_Cost_Units), per-run audit artifacts (Run_Manifest, Validation_Log), and reference / rate-library tabs that benefit from spreadsheet review:

| # | Tab | Type | Primary Key | Purpose |
|---|---|---|---|---|
| 1 | `Run_Manifest` | Audit envelope | run_id | One row per workbook emission; run metadata + gate summary |
| 2 | `Registry` | Entity (WBS-A) | wbs_id | Physical assets + tangible project costs (ACQ). **No FERC column.** |
| 3 | `Labor_Pools` | Entity (WBS-B) | labor_pool_id | Labor type catalog (Direct/Indirect by discipline) |
| 4 | `Labor_Eligibility` | Join (M:N) | linkage_id | Labor pool ↔ WBS-A asset eligibility (where labor types are constrained) |
| 5 | `Master_Cost_Units` | Join (matrix CU layer) | cu_id | The matrix join: CU → WBS-A leaf + labor consumption + permit attachment |
| 6 | `Burden_Factors` | Rate library | burden_id | Burden percentages (ENG/PMG/CMG/ENV/PER/SIT/IDC) per branch |
| 7 | `State_Overlay_Mapping` | Join (M:N) | overlay_link_id | (NEW v4 per ADR-17) FERC account ↔ state-overlay rules (NY PSC RDM/EAM/REV/ESCO and adjacent NE state PUCs) |
| 8 | `Labor_Rates` | Rate library | rate_id | CBS-level specific job classifications with wage rates |
| 9 | `Material_Indices` | Rate library | index_id | Commodity indices (ENR CCI, BLS PPI, LME, etc.) for normalization |
| 10 | `Productivity` | Reference | prod_id | Production rates per CU/crew/geography |
| 11 | `Source_Catalog` | Reference | source_id | Every cited source (T1–T5) with tier, vintage, license |
| 12 | `Model_Equations` | Reference | equation_id | Parametric models used for derivation |
| 13 | `Validation_Log` | Audit | row_ref | Every gate result (PASS/FAIL/WARN) with detail |

**External YAML files** (NEW v4.1 per ADR-19) — canonical storage for pure-reference catalog + join data that benefits from git-friendly diffs, scriptable parsing, and alignment with the skill's YAML-first authority chain. xlsx representations are derived views regenerated on demand from these YAMLs:

| File | Type | Primary Key | Path |
|---|---|---|---|
| `Permits` | Entity (catalog) | permit_id | `references/permits.yaml` |
| `Permit_Eligibility` | Join (M:N) | linkage_id | `references/permit_eligibility.yaml` |
| `FERC_Accounts` | Entity (catalog) | (ferc_part, account_number) | `references/ferc_accounts.yaml` |
| `WBS_FERC_Linkage` | Join (M:N) | linkage_id | `references/wbs_ferc_linkage.yaml` |

> **Note on count**: **13** `sheets:` tabs + **4** `external_files:` YAML authorities = **17** logical surfaces total. `FERC_Accounts`, `WBS_FERC_Linkage`, `Permits`, and `Permit_Eligibility` are YAML-canonical (per ADR-19); their xlsx mirror tabs are derived only. Future YAML migration **candidates** (not yet moved): `Labor_Pools`, `Labor_Eligibility`, `State_Overlay_Mapping`, and rate-library tabs (`Burden_Factors`, `Labor_Rates`, `Material_Indices`, `Productivity`). ADR-19 (§17) records rationale and the migration pattern.

### 6.2 Tab purposes — the three classes of tab

**Entity (catalog) tabs** — one row per concept in a closed-world domain. Examples: `Registry`, `Permits`, `FERC_Accounts`, `Labor_Pools`.

**Join (M:N) tabs** — one row per relationship between two entity tabs. Examples: `Permit_Eligibility`, `WBS_FERC_Linkage`, `Labor_Eligibility`.

**Reference / audit tabs** — supporting data and audit artifacts. Examples: `Source_Catalog`, `Validation_Log`, `Run_Manifest`, rate libraries.

### 6.3 Critical schema rules

- **Stop at L6.** L7 is NOT a column. Any L7-like data (assumptions, inclusions, exclusions) lives in metadata columns on the L6 row.
- **No FERC column on Registry.** FERC mapping lives in `WBS_FERC_Linkage`. To find the FERC account for a Registry row, query the linkage. This makes `WBS_FERC_Linkage` the sole authority and prevents the denormalization drift that plagued v1/v2.
- **Strip display artifacts.** Element names emit without `└─` Unicode prefix; WBS IDs have no trailing dots.
- **L5_WILDCARD + L6_SPECIFIC override pattern.** Eligibility and FERC linkage rows can target a whole L5 (wildcard) with explicit L6 overrides for exceptions. See §9 for the lookup procedure.
- **Project-level entities use IMPLICIT scope.** Federal/state/local project-wide permits (A1/A2/A3 buckets) get NO entries in `Permit_Eligibility` because they apply to all assets by definition. Only A4 (per-asset) and A5 (per-activity) permits get explicit eligibility rows. (Closed-world rule per §10.)
- **FERC inheritance is derived, not stored.** Permits that inherit FERC from the enabled asset do NOT store the inherited FERC on `Permit_Eligibility` rows; the inheritance is derived at query time via the join Permit_Eligibility → WBS_FERC_Linkage → FERC_Accounts.

### 6.4 Filename and output location

- Filename pattern: `utility-cost-library_<mode>_electric_<YYMMDD-HHMM>.xlsx`
- Modes: `wbs`, `units`, `permits`, `ferc`, `full`
- Output directory: session outputs folder

## 7. Decision Procedure — Five Modes

Mode is resolved at session start. If ambiguous, ask **exactly one** clarifying question and HOLD.

```
IF user discusses WBS rows, hierarchy, scope decomposition, "what work belongs in X"
  → MODE A (WBS Development — covers both WBS-A and WBS-B authoring)
ELSE IF user discusses cost, crew, productivity, rate, CU buildup
  → MODE B (CU Development — the matrix join)
ELSE IF user discusses permits, regulatory, fees, applications
  → MODE C (Permit Catalog Building)
ELSE IF user discusses FERC account assignment, plant-account mapping
  → MODE D (FERC Linkage Building)
ELSE IF user requests audit, validation, gate check, dry run
  → MODE E (Validation & Audit)
ELSE
  → HOLD; ask one disambiguating question
```

### 7.1 Mode A — WBS Development

Used for authoring both WBS-A (physical assets) and WBS-B (labor pools). Sub-mode is detected from the L1 prefix of the target rows: `E.T.*` or `E.D.*` → WBS-A (Electric, Part 101); `G.T.*` or `G.D.*` → WBS-A (Gas, Part 201); `LBR.*` → WBS-B (domain-agnostic).

**Algorithm A1–A6:**
- A1. Resolve domain (Electric T&D and Gas T&D supported in v4; refuse water, telecom, and electric generation with `OUT_OF_SCOPE`).
- A2. Load canonical: enums.yaml, definitions.yaml, FERC USoA reference.
- A3. Research pass (T1 → T5 corroboration; ≥1 T2+ source for HIGH confidence).
- A4. Structure pass — for each row emit: `wbs_id` (dot-path), L1–L6 codes, element_name, canonical_phrase, definition, scope_inclusions, scope_exclusions, assumptions, utility_domain, is_overhead, source_refs, confidence, license, status, vintage_iso, vintage_window, decision_trace. **No FERC column.**
- A5. Validation gates G1–G10 (gate set varies by WBS-A vs WBS-B; G9 FERC validity applies only to WBS-A).
- A6. Emit workbook.

### 7.2 Mode B — CU Development (the matrix join)

This is the heaviest mode. CUs are where every cost dimension converges.

**Algorithm B1–B8:**
- B1. Resolve scope: which WBS-A leaf does this CU produce? (`wbs_a_link`). HOLD if ambiguous.
- B2. Load canonical (enums, FERC linkage, permit eligibility, labor pools).
- B3. Research pass T1 → T5.
- B4. Extraction: cu_id, wbs_a_link, canonical_phrase, uom, crew composition (CBS labor classes), labor_hours_per_uom, equipment_list, material_list, production_rate, vintage, citations.
- B5. **Break-point pre-flight** (Mode B-specific): does primary equipment change? Does crew size/composition change? Does specialized tools/techniques change? ≥1 YES → BREAK; all NO → GROUP. Material cost alone is NEVER a break driver.
- B6. **Normalization** — convert UOM via enums.uom_conversions; normalize geography; reconcile vintage.
- B7. **Burden loading** — compute `loaded_cost_per_uom = direct_cost × (1 + Σ burden_pct)`. Burdens applied per Burden_Factors: ENG, PMG, CMG, ENV, PER, SIT, IDC. Burdens INHERIT the CU's FERC via wbs_a_link → WBS_FERC_Linkage.
- B8. **Validation gates G1–G19** (full gate set; G18 fires on CUs carrying a state_overlay tag; G19 fires on CUs with accounting_view = SETTLEMENT). Emit.

**Mode B Novelty Validation (5 gates, one FAIL = REJECT):**
- G_NOV_1: scope (real scope gap, not duplicate of existing CU)
- G_NOV_2: non-derivative (not a math variant of an existing CU)
- G_NOV_3: granularity (matches break-point test)
- G_NOV_4: unit integrity (UOM consistent; no mixing LF and EA in one CU)
- G_NOV_5: anti-drift (cu_id doesn't recycle a retired ID; no inventing labor classes)

### 7.3 Mode C — Permit Catalog Building

Used to populate or extend the `Permits` and `Permit_Eligibility` tabs.

**Algorithm C1–C6:**
- C1. Identify permit candidate: name, issuing authority, scope, fee basis.
- C2. Classify into bucket: A1 (Federal), A2 (State), A3 (Local/Municipal), A4 (Asset/Crossing/Site), A5 (Activity). Apply 4-test from §10.
- C3. For A1/A2/A3 (project-level): emit one row in `Permits`; emit ZERO rows in `Permit_Eligibility` (implicit scope rule, P6 / closed-world convention).
- C4. For A4/A5 (per-instance): emit one row in `Permits`; emit explicit eligibility rows in `Permit_Eligibility` for every WBS-A code the permit can apply to. Use L5_WILDCARD with L6_SPECIFIC overrides where applicable.
- C5. Set `ferc_account_basis`: SPECIFIC_ACCOUNT (with account_number) | INHERITS_FROM_ENABLED_ASSET | ACCOUNT_183_TRANSFERS | FERC_303_INTANGIBLE.
- C6. Validation gates G1, G2, G7, G8, G11, G14, G15. Emit.

### 7.4 Mode D — FERC Linkage Building

Used to populate or extend the `FERC_Accounts` and `WBS_FERC_Linkage` tabs.

**Algorithm D1–D6:**
- D1. Ensure FERC USoA reference is loaded (the 28-row canonical account catalog from 18 CFR Part 101).
- D2. For each WBS-A code (L5 wildcard or L6 specific) needing linkage: identify the PRIMARY FERC account per Electric Plant Instruction 3/7/8/9. Cite the EPI section.
- D3. Identify any CONDITIONAL alternatives (e.g., a foundation could be 352 if building-related or 353 if equipment-specific).
- D4. Emit linkage rows: one PRIMARY entry per (wbs_a_code, branch_context); zero or more CONDITIONAL entries.
- D5. For L5 wildcards: emit a single row covering the wildcard plus explicit L6 override rows for exceptions.
- D6. Validation gates G7, G8, G12, G13, G14, G15, G18 (if emitting State_Overlay_Mapping rows). Emit.

### 7.5 Mode E — Validation & Audit

Pure read-only mode: run the full validation pipeline on an existing workbook and emit `Validation_Log` with PASS/FAIL/WARN per row per gate.

**Algorithm E1–E4:**
- E1. Load workbook; verify schema conformance per workbook_schema.yaml.
- E2. Run gates G1–G19 + V1–V9 across every tab.
- E3. Run referential-integrity checks across all join tabs.
- E4. Emit Validation_Log with one row per (sheet, row, gate, result) tuple.

## 8. Universal Rules (A_RULE_01 through A_RULE_15)

Hard rules. Violation triggers a structured error and a gate failure. The set was 10 in v2; v3 adds 5 to enforce the matrix model.

| # | Rule | Enforcement |
|---|---|---|
| A_RULE_01 | **WBS and CBS are separate.** No CBS-level specificity in WBS labels (no vendor names, model numbers, sizes, voltage classes, kVA ratings). CBS attributes live in `Master_Cost_Units` and `Labor_Rates`. | G3 |
| A_RULE_02 (REVISED) | **L6 is the leaf scope node.** CUs attach at L6 by default; L5 family-level CUs only when no break-point distinguishes children (rare). | G1, B5 |
| A_RULE_03 (REPLACED) | **L7 is not a WBS column.** Scope assumptions/inclusions/exclusions live in `scope_inclusions`, `scope_exclusions`, `assumptions` metadata columns on the L6 row. | G1, P8 |
| A_RULE_04 | **No "Replace" at unit level.** Decompose to Remove + Install. | B-mode novelty |
| A_RULE_05 | **No mob/demob inside individual CUs.** Mob/demob is project-level WBS at `E.{T,D}.{SUB,LIN}.CON.GCO.MOB`. | G3 |
| A_RULE_06 | **IEEE/ANSI terminology lock.** Use "Surge Arrester" (not Arrestor); "Disconnect Switch" / "Air Switch" per IEEE C37.30; "Voltage Transformer (VT)" not "PT" per IEEE C57.13; "Shield Wire / OHSW" not "OHGW". See `enums.canonical_terminology`. | G4 |
| A_RULE_07 | **Canonical phrase pattern.** `[verb] [object] [material/type] [context/method]`. Base verb form; no `-ing`. | G6 |
| A_RULE_08 | **Adders are separate WBS L6 nodes** under their parent L5, with `uom = Per_Location` or `Per_Job`. Climb, Energized, Night Work, Confined Space, Weather Standby. | A4 |
| A_RULE_09 | **No duplicate L1..L6 paths.** Path uniqueness enforced at G5. | G5 |
| A_RULE_10 | **No product names at any WBS level.** None. | G3, A_RULE_01 |
| A_RULE_11 (NEW) | **WBS-A and WBS-B are separate structures.** WBS-A rows are FERC-tagged (via WBS_FERC_Linkage); WBS-B rows are NEVER FERC-tagged. They join only via CU layer. | G9, G16, P1 |
| A_RULE_12 (NEW) | **Permits live in a catalog, not as WBS-A rows.** No row in `Registry` represents a permit. Permits are entities in the `Permits` tab; their applicability to WBS-A is recorded in `Permit_Eligibility`. | G11, P2 |
| A_RULE_13 (NEW) | **FERC mapping lives in a linkage tab, not on Registry.** Registry has no `ferc_account` column. FERC for any WBS-A row is derived from `WBS_FERC_Linkage`. | G12, G13, P2, P4 |
| A_RULE_14 (NEW) | **Eligibility constraints are explicit, not implied.** When an entity (permit, labor type) can only apply to a subset of WBS-A codes, that subset is enumerated in the corresponding eligibility tab. No comma-string lists in cells; no "applies to all" implicit. | G11, G16, P2, P6 |
| A_RULE_15 (NEW) | **CU is the only cross-dimensional join point.** WBS-A rows do not reference WBS-B rows. Permits do not reference labor pools. FERC accounts do not reference permits. All cross-dimension references happen at the CU layer via `wbs_a_link`, `labor_consumption`, `permits_attached`, and the derived ferc_account_inherited. | G17 (NEW), P5 |

## 9. FERC USoA Routing Procedure

Given a `wbs_id` like `E.T.SUB.CON.BGR.FDN` (electric) or `G.D.MAIN.CON.PIP.STL` (gas), determine the FERC account deterministically. This is **the** authoritative routing procedure and replaces all in-skill FERC-mapping prose tables from v2.

**v4 update:** Routing now returns a tuple `(ferc_part, account_number)` instead of bare `account_number`. The `ferc_part` ∈ {PART_101, PART_201} is dispositive — Account 365 in Part 101 (electric overhead conductors) is NOT the same as Account 365 in Part 201 (gas transmission land).

### 9.1 Lookup procedure (closed-world, deterministic)

```
INPUT: wbs_id (full dot-path)
1. Parse wbs_id:
   - L1_root        = parts[0]   (E for electric; G for gas — v4)
   - branch_context = L2 + L3   (electric: T_SUB, T_LIN, D_SUB, D_LIN;
                                  gas:      G_TPIPE, G_TCS, G_TSTG, G_DMAIN, G_DSVC, G_DSTN)
   - L5_code        = parts[4] if depth >= 5 else None
   - L6_code        = parts[5] if depth >= 6 else None
   - leaf_code      = parts[-1]
2. Determine ferc_part from L1_root: E -> PART_101; G -> PART_201; UNKNOWN -> hold.
3. Load the WBS_FERC_Linkage data (canonical YAML at references/wbs_ferc_linkage.yaml
   per ADR-19; OR the derived xlsx tab if working against an emitted workbook).
   Search in order (filtered by ferc_part):
   (a) L6_SPECIFIC + branch_context + applicability=PRIMARY + ferc_part match
   (b) L5_WILDCARD + branch_context + applicability=PRIMARY + ferc_part match
   (c) L5_WILDCARD + branch_context=ALL + applicability=PRIMARY + ferc_part match
4. If a match: RETURN (ferc_part, account_number). Optionally verify the account
   exists in references/ferc_accounts.yaml as a composite-FK integrity check (G13).
5. If no match: emit G12 (FERC routing missing) error; HOLD pending user input.
6. CONDITIONAL entries are surfaced as alternatives but do NOT become the PRIMARY return value.
7. If row has non-null state_overlay and ferc_account_basis = INHERITS_FROM_STATE_OVERLAY,
   apply state-overlay routing modifier (see §9.4 — NEW v4).
```

### 9.4 State-overlay routing modifier (NEW v4)

When a WBS-A row, CU, or estimate row carries `state_overlay = NY_PSC` (or any other state PUC):

- The federal FERC account from §9.1 remains the PRIMARY routing target.
- The state overlay adds DERIVED bookings: NY RDM reconciles to FERC 440 / 480 series; NY EAM credits / debits to regulatory asset / liability deferral accounts; NY REV-program costs to deferred regulatory asset (16 NYCRR-specified); ESCO delivery-revenue split per 16 NYCRR 167.5/167.6 (electric) or 312.5/312.6 (gas).
- Derived bookings live in the `State_Overlay_Mapping` workbook tab (NEW v4) and are surfaced at capitalization-view AND settlement-view consumption (see ADR-18).

### 9.2 Inheritance for permits and other non-asset rows

When a row's `ferc_account_basis = INHERITS_FROM_ENABLED_ASSET` (e.g., a railroad crossing permit attaches to a specific WBS-A asset at CU consumption time), the inherited FERC is derived at query time:

```
INPUT: permit_id, attached_wbs_id (the WBS-A leaf the permit is attached to at the CU)
1. Run §9.1 routing procedure on attached_wbs_id → returns FERC account X.
2. Verify (permit_id, attached_wbs_id leaf_code or L5 wildcard) exists in Permit_Eligibility → G11.
3. Return X as the inherited FERC for this permit consumption event.
```

This means the same permit (e.g., `PRM-XNG-RR` Railroad crossing fee) gets a different FERC depending on which asset it attaches to:
- Attached to OVH.TWR → inherits 354
- Attached to OVH.POL → inherits 355
- Attached to UGD.CDT → inherits 357
- Attached to UGD.CBL → inherits 358

Same permit, four different inherited FERCs, all derived from a single point of truth (`WBS_FERC_Linkage`).

### 9.3 Cross-branch FERC validity (G15)

A `T_*` branch_context can only link to FERC accounts with `branch_applicability ∈ {T_ONLY, BOTH, INTANGIBLE_ONLY}`. Same rule mirrored for `D_*`. This prevents a T-LIN row from being tagged with FERC 364 (a Distribution-only account). Enforced at write-time on `WBS_FERC_Linkage`.

## 10. Permit Taxonomy & Routing

### 10.1 Five-bucket permit taxonomy

Every permit type belongs to exactly one of these five buckets. The bucket determines whether the permit gets explicit eligibility rows.

| Bucket | Scope | Typical count per project | Eligibility rows? |
|---|---|---|---|
| **A1 — Federal** | Project-wide | 3–8 per project | NO (implicit) |
| **A2 — State (project)** | Project-wide per state crossed | 2–5 per state | NO (implicit) |
| **A3 — Local / Municipal** | Project-wide per affected jurisdiction | 1–N per municipality | NO (implicit) |
| **A4 — Asset / Crossing / Site** | Per individual instance | Scales with crossing count | YES (explicit per WBS-A code) |
| **A5 — Activity-specific** | Per construction event/method | Scales with method use | YES (explicit per WBS-A code or method) |

### 10.2 The 4-test for project-level vs. asset-level classification

Apply in order; first YES wins:

1. **Single-application test** — Does the entire scope flow through one regulatory application, one docket, one fee, one final order? → **PROJECT-LEVEL** (A1/A2/A3).
2. **Per-instance issuance test** — Does the issuing authority require a separate application/permit ID for each crossing, pole, site, or event? → **ASSET/ACTIVITY-LEVEL** (A4/A5).
3. **Counts-with-quantity test** — Does total cost scale linearly with the number of crossings/sites/events (e.g., 12 RR crossings = 12 fees)? → **ASSET-LEVEL** (A4).
4. **Triggers-with-activity test** — Does the permit only exist when a specific construction method is used (blasting, HDD, helicopter)? → **ACTIVITY-LEVEL** (A5).

### 10.3 Eligibility-set examples (A4 / A5 only)

Asset-specific permits apply to only a SUBSET of WBS-A codes, not all assets. Each A4/A5 permit has explicit eligibility rows enumerating that subset:

- **Railroad crossing occupancy** (`PRM-XNG-RR`) → eligible: `OVH.POL`, `OVH.TWR`, `UGD.CDT`, `UGD.CBL`, `UGD.MNH`, `FIB.OPG`, `FIB.ADS`.
- **FAA Form 7460-1 obstruction** (`PRM-XNG-FAA-7460`) → eligible: `OVH.TWR` only (>200 ft AGL or within FAA Part 77 surfaces).
- **Blasting permit** (`PRM-ACT-BLAST`) → eligible: `BGR.FDN`, `BGR.MAT`, `UGD.CDT`, `SWK.EXC` (anywhere rock excavation occurs).
- **Oversize-overweight hauling** (`PRM-ACT-OVERSIZE`) → eligible: `MEQ.TRF` only (transformer transport).

This eligibility data lives in `Permit_Eligibility` as explicit rows. No comma-string lists in `Permits` cells.

### 10.4 Permit FERC inheritance

The `Permits` catalog records `ferc_account_basis` for each permit:

| ferc_account_basis | Meaning | Example permits |
|---|---|---|
| SPECIFIC_ACCOUNT | Permit always routes to one specific FERC account; `ferc_account_specific` populated. | `PRM-STA-NY-ART7` (Article VII) → 350; `PRM-LND-FEE` (Land) → 350/360 |
| INHERITS_FROM_ENABLED_ASSET | Permit's FERC is derived from the WBS-A asset it attaches to at the CU layer (§9.2). | Most A4/A5 permits |
| ACCOUNT_183_TRANSFERS | Pre-commitment in Account 183; transfers to plant account on commitment. | Pre-project environmental studies (per EPI 3(20)) |
| FERC_303_INTANGIBLE | Only used for genuinely separable intangible rights (patents, long-term franchises, organizational costs). NOT a catch-all. | Software licenses tied to operations, not projects |

## 11. Labor Architecture (WBS-B + CBS)

### 11.1 WBS-B structure

WBS-B is a separate WBS hierarchy from WBS-A. It captures labor categories (the "who did the work" dimension) and is **never** FERC-tagged.

```
LBR                       (L1 — Labor root, no T/D distinction)
├── DIR                   (L2 — Direct Labor)
│   ├── CIV               (L3 — Civil)
│   ├── ELE               (L3 — Electrical)
│   ├── MEC               (L3 — Mechanical)
│   ├── SVY               (L3 — Survey)
│   └── OPE               (L3 — Equipment Operations)
└── IND                   (L2 — Indirect Labor)
    ├── ENG               (L3 — Engineering)
    ├── PMG               (L3 — Project Management)
    ├── CMG               (L3 — Construction Management)
    ├── ENV               (L3 — Environmental)
    ├── PER               (L3 — Permitting)
    ├── SIT               (L3 — Siting)
    ├── COM               (L3 — Commissioning)
    ├── QAQ               (L3 — QA / QC)
    ├── SAF               (L3 — Safety)
    └── LRA               (L3 — Land / ROW Administration)
```

WBS-B stops at L3 (discipline). Job-title granularity lives in CBS, not WBS-B.

### 11.2 CBS — specific job classifications

CBS holds the wage-rate-bearing labor classes (Lineman_Journeyman, Senior_Civil_Engineer, Substation_Electrician_Apprentice, etc.). Each CBS class has a **single rollup** to a WBS-B leaf:

| CBS class (example) | Rolls up to WBS-B leaf |
|---|---|
| Lineman_Journeyman | LBR.DIR.ELE |
| Substation_Electrician_Journeyman | LBR.DIR.ELE |
| Concrete_Finisher | LBR.DIR.CIV |
| Ironworker | LBR.DIR.MEC |
| Surveyor | LBR.DIR.SVY |
| Equipment_Operator_Crane | LBR.DIR.OPE |
| Senior_Civil_Engineer | LBR.IND.ENG |
| Senior_Electrical_Engineer | LBR.IND.ENG |
| Project_Manager_III | LBR.IND.PMG |
| Construction_Manager | LBR.IND.CMG |
| Environmental_Specialist | LBR.IND.ENV |

The CBS-to-WBS-B mapping lives in `Labor_Rates` (one column per CBS row pointing to its WBS-B leaf).

### 11.3 Labor consumption at CU

A CU specifies which CBS labor classes it consumes (via `labor_consumption` list). At rollup time:
- **WBS-A rollup**: every labor hour goes to the CU's `wbs_a_link` for FERC reporting via §9.1.
- **WBS-B rollup**: every labor hour goes to the labor class's `wbs_b_link` (via `Labor_Rates`) for labor-spend tracking.

Same dollars, two coordinates. No need for "burden percentages" for the labor categories that are tracked at WBS-B level — they're real labor consumption, not allocation. Burden percentages remain useful for the small subset of indirect labor that genuinely can't be allocated per-CU (project-level PM supervising hundreds of CUs).

### 11.4 Labor eligibility (optional constraint layer)

Some labor types only apply to certain asset categories — e.g., a Cable_Splicer is only consumed by UGD.CBL or UGD.TRM CUs, not by OVH.POL CUs. When this constraint matters, `Labor_Eligibility` records the valid asset-labor pairings. For unconstrained labor (Foreman, Laborer_General), no eligibility rows are needed (implicit "applies to all" similar to project-level permits in §10).

## 12. PDL → ACQ Refactor

### 12.1 What was wrong with PDL

The old `PDL` (Project Delivery) L4 branch in v1/v2 mixed three different cost categories:

1. **Labor pools** (`PDL.ENG.LOE`, `PDL.PMG.LOE`, `PDL.CMG.LOE`, etc.) — these were labor categories trying to live in WBS-A but lacked a single destination FERC because labor spans many assets.
2. **Tangible third-party costs** (`PDL.LND.FEE`, `PDL.PER.PRM`, `PDL.ENV.APP`, `PDL.COM.ICN`) — these were real cost line items with definable FERC destinations.
3. **Design milestones** (`PDL.ENG.D10`, `D30`, `D60`, `D90`, `IFC`) — these were schedule milestones masquerading as cost categories.

The result was incoherent: a single PDL row couldn't be FERC-tagged because the same row contained costs that should go to many different FERC accounts.

### 12.2 The v3 resolution

v3 splits PDL into three destinations:

| Old PDL item | v3 destination |
|---|---|
| `PDL.ENG.LOE`, `PDL.PMG.LOE`, `PDL.CMG.LOE`, `PDL.ENV.LOE`, `PDL.PER.LOE`, `PDL.SIT.LOE`, `PDL.COM.LOE`, `PDL.LND.LOE`, `PDL.ROW.LOE` (all labor LOE rows) | **WBS-B** as `LBR.IND.{ENG,PMG,CMG,ENV,PER,SIT,COM,LRA}` |
| `PDL.LND.FEE`, `PDL.ROW.FEE` (tangible land/ROW costs) | **ACQ** branch as `ACQ.LND` / `ACQ.ROW` |
| `PDL.PER.PRM`, `PDL.ENV.APP`, `PDL.SIT.APP`, `PDL.COM.ICN`, `PDL.ENV.RPT`, `PDL.SIT.RPT`, `PDL.CMG.TST` (tangible fees/reports) | **Permits catalog** + **ACQ** branch (depending on whether they're permits or paid deliverables) |
| `PDL.ENG.D10..D90`, `PDL.ENG.IFC` (design milestones) | **Schedule milestones**, NOT WBS rows — phase tracking is a schedule concern |

### 12.3 The new ACQ branch (Acquisitions / Project Soft Costs)

`ACQ` is an L4 peer of `CON` under each L3:

```
E.T.SUB.CON  ┐                          E.T.SUB.ACQ  ┐
E.T.SUB.ACQ  ┘  (peers under E.T.SUB)    ├── LND     │  (Acquisitions)
E.T.LIN.CON  ┐                           ├── PER     │
E.T.LIN.ACQ  ┘  (peers under E.T.LIN)    │   ├── PRM │  (permit fees by type)
                                         │   └── APP │  (application fees)
                                         ├── ENV     │
                                         │   ├── APP │
                                         │   └── RPT │
                                         ├── SIT     │
                                         │   ├── APP │
                                         │   └── RPT │
                                         ├── ICN     │  (interconnection fees)
                                         └── TST     │  (3rd-party testing)
                                                     ┘
E.T.LIN.ACQ adds:
  ├── ROW     (Right-of-Way easements; LIN-only, not SUB)
```

Each ACQ row has its FERC mapping in `WBS_FERC_Linkage`. Permits and similar are linked via `Permit_Eligibility` to specific assets.

### 12.4 Why this is correct per FERC USoA

FERC 18 CFR Part 101, Electric Plant Instructions 3, 7, 8, and 9, do NOT create separate plant accounts for permits / studies / interconnection / commissioning. Instead, EPI 3 (21 "Components of Construction Cost") itemizes these as components that get directed INTO the physical plant account they enable. Account 303 (Miscellaneous Intangible Plant) is reserved for genuinely separable intangible property (patents, licenses, long-term franchises) — NOT a catch-all for soft costs.

This was a research finding from §17 ADR-07. The user's pre-v3 hypothesis ("if no FERC bucket exists, fold into 303") was inverted relative to actual FERC practice. Industry-standard frameworks (ISO-NE PP-4 Att. D, MISO MTEP25, AACE 96R-18, Versant Power's capitalization guidelines) all maintain itemized estimating-view rows that roll into physical plant accounts at booking — exactly the "two-view accounting" pattern in P7.

## 13. Validation Gates (G1–G19)

Gates run at workbook emission. Each gate produces a row in `Validation_Log` per affected workbook row.

| Gate | Scope | Description |
|---|---|---|
| G1 | All WBS rows | L1..L6 path populated; no trailing dot; no `└─` prefix in element_name |
| G2 | All rows | ≥1 source citation; ≥1 T2+ source for HIGH confidence |
| G3 | WBS-A rows | No CBS specificity in WBS labels (no vendor/model/size/voltage class/kVA) |
| G4 | All rows | IEEE/ANSI terminology check against `enums.canonical_terminology` |
| G5 | WBS-A and WBS-B rows | Path uniqueness (no duplicate L1..L6 paths) |
| G6 | All rows | Canonical phrase pattern (verb-object-type-context) |
| G7 | All rows | Every enum value is in `enums.yaml` (no inventing values) |
| G8 | All rows | `decision_trace` populated |
| G9 | WBS-A rows + CUs | FERC validity — must resolve via WBS_FERC_Linkage to a valid `FERC_Accounts.account_number` |
| G10 | Mode B (CUs) | Burden coherence — `loaded_cost_per_uom = direct × (1 + total_burden_pct)`; each burden line cites a Burden_Factors row |
| G11 (NEW v3) | CUs that attach permits | Every (permit_id, wbs_a_code) pair has an explicit row in `Permit_Eligibility` (for A4/A5 buckets) |
| G12 (NEW v3) | WBS-A rows | FERC routing exists — every WBS-A row has at least one PRIMARY entry in `WBS_FERC_Linkage` (catches missing mappings) |
| G13 (NEW v3) | WBS_FERC_Linkage rows | FERC USoA referential integrity — every `(ferc_part, ferc_account_number)` composite FK exists in `FERC_Accounts` |
| G14 (NEW v3) | All catalog cross-refs | Permit_Eligibility.permit_id → Permits.permit_id; Labor_Eligibility.labor_pool_id → Labor_Pools.labor_pool_id; etc. |
| G15 (NEW v3) | WBS_FERC_Linkage rows | Branch-FERC consistency — `T_*` branch_context can only link to FERC accounts where `branch_applicability ∈ {T_ONLY, BOTH, INTANGIBLE_ONLY}`; same rule mirrored for `D_*`. v4 extends to gas: `G_T*`/`G_D*` mirror against Part 201 accounts. |
| G16 (NEW v3) | WBS-B rows | WBS-B never has a FERC tag (catches accidental denormalization) |
| G17 (NEW v3) | All cross-dimension references | The only cross-dimension reference column is on `Master_Cost_Units` (CU layer). WBS-A → WBS-B, Permits → Labor, FERC → Permits direct references are forbidden. |
| G18 (NEW v4) | State_Overlay_Mapping rows + WBS_FERC_Linkage rows with INHERITS_FROM_STATE_OVERLAY | State-overlay eligibility check per ADR-17 — every State_Overlay_Mapping row's `(ferc_part, federal_account_number)` pair MUST resolve to an existing FERC_Accounts row; `state_overlay` MUST be in `enums.state_overlay`; `overlay_effect` MUST be in the four allowed values. Catches state-overlay rows pointing at non-existent FERC accounts or using invalid overlay effects. |
| G19 (NEW v4) | Settlement-view rows (CUs / line items with `accounting_view = SETTLEMENT`) | Settlement-view routing check per ADR-18 — settlement-view bookings MUST route to FERC 456 (credits) / 557 (charges) / 565 (transmission by others) with a non-null `rto_iso` value ∈ {NYISO, ISO_NE, PJM, NONE, UNKNOWN}. Catches settlement bookings using capital-account FERCs (which would corrupt monthly close). |

### 13.1 Universal validation gates V1–V9

Apply across the whole workbook on every emit. Unchanged from v2.

- V1: Schema conformance (every required column populated or `UNKNOWN`)
- V2: Enum integrity (no values outside enums.yaml)
- V3: Citation integrity (every cited source exists in Source_Catalog)
- V4: UOM integrity (`uom_conversions` applied; no implicit conversions)
- V5: Confidence consistency (tier ceilings respected — T5 alone never HIGH)
- V6: Vintage hygiene (CURRENT ≤24mo; STALE >60mo → confidence ≤ LOW)
- V7: License hygiene (RESTRICTED never embedded; PUBLIC_WITH_ATTRIBUTION attributed)
- V8: Decision trace (every emit row has a non-empty `decision_trace`)
- V9: Determinism (re-running same inputs produces byte-identical workbook except `run_id` / `timestamp`)

## 14. Error Policy

Structured YAML errors only. Schema:

```yaml
error_code: <unique_id>
error_type: <enum: missing_input | invalid_input | ambiguous_input |
             out_of_scope | gate_failure | processing_error | conflict_detected |
             unknown_value | license_restricted | vintage_stale |
             cross_dimension_violation>
error_message: <human-readable>
failed_field: <jsonpath>
failed_gate: <G1..G19 | V1..V9>
expected: <expected value/pattern>
actual: <observed>
recovery_options: [<option_id_1>, <option_id_2>]
decision_trace: <free text>
```

### 14.1 Specific policies

- **Missing data** → emit row with `UNKNOWN` for the missing field; never invent.
- **Ambiguous input** → HOLD; ask exactly ONE clarifying question.
- **Out-of-scope request** (e.g., user asks about gas/water/telecom) → refuse in-schema with `OUT_OF_SCOPE`; do not silently attempt.
- **Enum expansion request** → HOLD; require explicit user approval before adding to enums.yaml.
- **Source conflicts** → emit BOTH rows with decision_trace; do not silently choose.
- **Stale vintage** (>60 mo) with no fresher source → force confidence ≤ LOW per V6; do not infer.
- **Cross-dimension violation** (e.g., WBS-A row referencing a WBS-B leaf directly without going through CU) → emit `cross_dimension_violation`; HOLD pending architectural review.

## 15. Anti-Drift Guardrails (DP-01 through DP-12)

Drift-prevention mechanisms. ≥5 must be active on every Mode A–E run. Numbers DP-01..DP-10 carried from v2; DP-11 and DP-12 added in v3 to enforce the matrix model.

| # | Mechanism | What it prevents |
|---|---|---|
| DP-01 | identity_anchor | Mode and current scope reasserted at every reply opener |
| DP-02 | scan_protocol | Canonical enums scanned before any emit |
| DP-03 | scope_fence | Refuses expansions outside Electric T&D and Gas T&D in v4 (water and telecom remain OUT_OF_SCOPE; electric generation FERC 310–347 remains OUT_OF_SCOPE) |
| DP-04 | vocabulary_lock | WBS/FERC/permit/labor vocabularies are closed-world |
| DP-05 | schema_lock | workbook_schema.yaml is the only allowed output shape |
| DP-06 | decision_trace | Every gate fires its decision trace |
| DP-07 | precedence_hierarchy | `conflict_precedence` is followed strictly |
| DP-08 | scope_creep_detection | Side-trips to gas/water/telecom refused, not deferred silently |
| DP-09 | negative_examples | examples.yaml ships both positive and forbidden patterns |
| DP-10 | output_fingerprinting | Filename + run_id form an audit handle |
| DP-11 (NEW) | matrix_coherence | Cross-dimension references must go through CU layer (G17). No direct WBS-A → WBS-B links, no direct Permits → FERC links. |
| DP-12 (NEW) | catalog_vs_join_discipline | Entity tabs hold one row per concept; join tabs hold M:N relationships. No denormalized lists in entity cells. |

## 16. Determinism Contract

Same inputs produce byte-identical workbook except for:
- `run_id` (ULID/UUIDv7 — one per emission)
- `timestamp_utc_iso` / `timestamp_local`

### 16.1 Row ordering rules

- `Registry`: ASC by `wbs_id`
- `Permits`: ASC by `permit_id` (bucket prefix sorts lexically: A1_FEDERAL < A2_STATE < A3_LOCAL < A4_ASSET_CROSSING < A5_ACTIVITY)
- `Permit_Eligibility`: ASC by (`permit_id`, `wbs_a_code`)
- `FERC_Accounts`: ASC by `account_number` (string sort: "183" < "301" < "302" < "303" < "350" < ...)
- `WBS_FERC_Linkage`: ASC by (`branch_context`, `wbs_a_code`, `applicability` where PRIMARY < SECONDARY < CONDITIONAL)
- `Labor_Pools`: ASC by (`L1`, `L2`, `L3`)
- `Master_Cost_Units`: ASC by `cu_id`
- All others: ASC by primary key

### 16.2 Empty cell convention

Empty cells use literal `UNKNOWN`. Blank cells are forbidden (V1 gate failure).

### 16.3 Filename convention

`utility-cost-library_<mode>_electric_<YYMMDD-HHMM>.xlsx`

## 17. Resolved Architectural Decisions (ADR log)

Every architectural decision made during the v2→v3 transition is logged here with rationale and source.

### ADR-01: Stop at L6; L7 is metadata, not hierarchy

- **Decision**: WBS hierarchy is exactly 6 levels (L1–L6). L7-style data (assumptions, inclusions, exclusions) lives in metadata columns on the L6 row.
- **Rationale**: The prior `A_RULE_03` ("L7 is the assumptions/inclusions column") was identified as smuggling CBS factor lists into WBS labels — the exact failure mode `A_RULE_01` was meant to prevent. Demoting L7 to row metadata preserves the scope information without polluting the hierarchy.
- **Source**: User direction; consistent with AACE 56R/96R L5-as-unit-level convention.
- **Enforcement**: A_RULE_03 (replaced), P8, G1.

### ADR-02: Two parallel WBS structures (WBS-A + WBS-B)

- **Decision**: Physical assets live in WBS-A (FERC-tagged via linkage); labor pools live in WBS-B (no FERC). They join only at the CU layer.
- **Rationale**: A single WBS hierarchy cannot represent both "what was built" and "who did the work" coherently — they're orthogonal dimensions. Direct labor (crews) and indirect labor (engineering, PM, CM) are both labor, both need consistent treatment. Putting indirect labor in WBS-A as PDL rows forced single-FERC-per-row stamping that doesn't match how labor actually flows.
- **Source**: User direction; matches Primavera P6 / Oracle Unifier "WBS for work + Cost Codes for FERC accounts" orthogonal pattern.
- **Enforcement**: A_RULE_11, G9, G16, P1.

### ADR-03: Normalized relational design (catalogs + joins)

- **Decision**: Every many-to-many relationship lives in a dedicated join tab. Entity tabs hold one row per concept; join tabs hold M:N relationships. No denormalized comma-string lists in entity cells.
- **Rationale**: The eligibility constraints between permits and assets, between labor types and assets, between WBS-A rows and FERC accounts are all M:N relationships. Denormalizing them as lists in cells breaks queryability and validation. The closed-world skill design demands a closed-world data structure.
- **Source**: User direction; standard relational database normalization.
- **Enforcement**: A_RULE_12, A_RULE_13, A_RULE_14, P2, DP-12.

### ADR-04: FERC mapping moved off Registry to WBS_FERC_Linkage

- **Decision**: The `ferc_account` column is removed from the `Registry` tab. FERC mapping for any WBS-A row is derived from `WBS_FERC_Linkage` exclusively.
- **Rationale**: A single FERC column on Registry forces a single primary FERC per row, which doesn't accommodate (a) the PRIMARY/CONDITIONAL alternatives observed for ambiguous assets (e.g., a foundation that could be 352 or 353), (b) the inheritance semantics for permit attachments, or (c) the audit trail of why a particular FERC was assigned.
- **Source**: User direction.
- **Enforcement**: A_RULE_13, P4, G12, G13.

### ADR-05: Permits as separate catalog + eligibility join

- **Decision**: Permits live in a `Permits` entity tab. Their applicability to WBS-A is recorded in `Permit_Eligibility` as M:N join.
- **Rationale**: Treating permits as WBS-A rows was incoherent because (a) they're not physical assets, (b) most permits apply to many asset types (RR crossing → 7+ asset types), (c) project-level permits apply to all assets (NEPA, CGP). Catalog + join cleanly handles all three cases.
- **Source**: User direction.
- **Enforcement**: A_RULE_12, P2, G11.

### ADR-06: Project-level permits use implicit eligibility (D1c)

- **Decision**: Federal/state/local project-wide permits (A1/A2/A3 buckets) get NO entries in `Permit_Eligibility`. Eligibility table only used for A4 (per-asset) and A5 (per-activity) permits.
- **Rationale**: Enumerating every WBS-A code for a project-wide permit (e.g., NEPA → 30+ rows) bloats the eligibility table without adding information. The implicit "covers everything" semantics is documented as a closed-world rule per §10.
- **Source**: User direction (decision D1c from session of 2026-05-14).
- **Enforcement**: §6.3, §10.1, Mode C algorithm step C3.

### ADR-07: FERC USoA routing — destination plant account, NOT 303

- **Decision**: Non-physical project items (permits, application fees, third-party studies, interconnection fees) route to the **physical plant account they enable**, not to FERC 303.
- **Rationale**: 18 CFR Part 101 Electric Plant Instructions 3, 7, 8, 9 itemize these as components of construction cost, NOT as separate plant accounts. Account 303 is reserved for genuinely separable intangible property (patents, licenses, long-term franchises). The user's pre-v3 hypothesis ("if no FERC bucket exists, fold into 303") was inverted relative to actual FERC practice.
- **Source**: 18 CFR §101 EPI 3 ("Components of Construction Cost"), EPI 7 (24-item Land list), EPI 8 (66-item Structures list), EPI 9 (Equipment testing). Cross-confirmed by Versant Power Capitalization Guidelines (18 components), ISO-NE PP-4 Att. D (10 estimating categories), NYISO Manual 23, MISO MTEP25, AACE RP 96R-18.
- **Enforcement**: §10.4, §12.4, G9.

### ADR-08: Three-view accounting (estimating + capitalization + SETTLEMENT) — expanded v4

- **Decision**: The workbook supports THREE views over the same template data:
  1. **Estimating view** — soft costs visible as WBS-A line items in the ACQ branch (Class 5→1 estimates).
  2. **Capitalization view** — soft costs roll into physical plant accounts via WBS_FERC_Linkage at in-service booking.
  3. **Settlement view (NEW v4 per ADR-18)** — monthly RTO/ISO settlement charges/credits booked to FERC 456 (Other Electric Revenues, credits), 557 (Other Expenses, charges), 565 (Transmission of Electricity by Others) — reconciled against NYISO / ISO-NE / PJM invoice line items.
- **Rationale (estimating + capitalization)**: Canonical pattern across every industry framework (ISO-NE PP-4 Att. D mandates 10 estimating categories; NYISO Manual 23 similar; MISO MTEP25 uses 8; AACE RP 96R-18 organizes Class 5→1 estimates with this structure).
- **Rationale (settlement, v4)**: Monthly close at Northeast IOUs reconciles RTO/ISO settlement to specific FERC accounts; this is a distinct workflow from project estimating (long horizon, project-scoped) and from in-service capitalization (one-time event per project). The settlement view operates monthly, scoped to operating period, and consumes the same WBS_FERC_Linkage + state_overlay rows.
- **Source**: ISO-NE PP-4 Attachment D, NYISO OATT §30.8, MISO MTEP25 §3, AACE 96R-18 §5, FERC AI01-1-000 Office of Enforcement guidance on settlement booking, NY PSC tariff rules on monthly reconciliation.
- **Enforcement**: P7, ACQ branch design (§12.3), new `accounting_view` enum, settlement-view tab additions in workbook_schema.

### ADR-09: RCL = Reclamation (SUB); CLR = Clearing (LIN)

- **Decision**: The same 3-letter code `RCL` cannot mean different things in SUB vs. LIN contexts. SUB.GCO retains `RCL` for "Reclamation" (post-construction site restoration); LIN.GCO uses `CLR` for "Clearing" (vegetation/tree removal pre-construction).
- **Rationale**: Pre-v3 used `RCL` in both SUB and LIN with different meanings — a closed-world violation.
- **Source**: User direction.
- **Enforcement**: `enums.wbs_l6_electric`; A_RULE_09 (no code-meaning collisions).

### ADR-10: SEC = "Security" everywhere

- **Decision**: The `SEC` code's element name is "Security" in all contexts (no "Temp Construction Security" / "Permanent Security Infrastructure" variants).
- **Rationale**: The temp-vs-permanent distinction was carried by the parent L5 (`GCO.SEC` is temporary by definition because it's under General Conditions; `SUB.CON.SEC` L5 is permanent infrastructure). The element-name variants added noise without information.
- **Source**: User direction.
- **Enforcement**: `enums.wbs_l6_electric` element_name field.

### ADR-11: STC (Site Conditions) added to T-LIN

- **Decision**: T-LIN.CON gets an `STC` L5 mirroring D-LIN.CON.STC (children: GRD, PAV, SRF, UTC). SUB sections (T and D) do not get STC.
- **Rationale**: User direction: "Sub should be different than Line." T-Line restoration costs (grading, pavement, surface restoration after UG work) are real cost categories that previously had no home.
- **Source**: User direction.
- **Enforcement**: `enums.wbs_l5_electric` × `branch_context.LIN`; Registry rows 188–192.

### ADR-12: BGR / UGD split

- **Decision**: The single "Below Grade" L5 splits into BGR (structural foundations / grounding) and UGD (underground utility infrastructure).
- **Rationale**: The combined L5 mixed two FERC routing destinations: foundations route to 352/353/354/355/361/362/364, underground utility routes to 357/358/366/367. Splitting them gives clean FERC mapping at L5.
- **Source**: User direction; FERC USoA EPI 9 (Equipment) vs. FERC 357/358/366/367 (Underground).
- **Enforcement**: `enums.wbs_l5_electric`.

### ADR-13: D1c / D2a / D3b — eligibility design choices

- **Decision**:
  - D1c: Project-level permits use implicit eligibility (no rows).
  - D2a: L5_WILDCARD + L6_SPECIFIC override pattern.
  - D3b: FERC inheritance derived at query time, not stored on `Permit_Eligibility` rows.
- **Rationale**: With `WBS_FERC_Linkage` as a separate tab, the inherited FERC is derivable via join, removing the need to store it redundantly on eligibility rows. D3a fallback was offered in case the join couldn't be done — but it can, so D3b applies.
- **Source**: User direction.
- **Enforcement**: Mode C algorithm steps C3, C4; §6.3.

### ADR-14: Permit FERC inheritance from enabled asset

- **Decision**: Most A4/A5 permits have `ferc_account_basis = INHERITS_FROM_ENABLED_ASSET`. The same permit gets different FERCs depending on which asset it attaches to at CU consumption.
- **Rationale**: A RR crossing permit attached to a pole inherits FERC 355; attached to a tower inherits 354; attached to UG conduit inherits 357; attached to UG cable inherits 358. Same permit, four different inherited FERCs, all derived from a single point of truth.
- **Source**: §9.2 derivation procedure.
- **Enforcement**: G9, G11, §9.2.

### ADR-15: Eligibility constraints are explicit, not implied

- **Decision**: When a permit or labor type can only apply to a subset of WBS-A codes, that subset is enumerated in the corresponding eligibility tab. No comma-string lists in cells; no "applies to all" implicit (except for project-level permits per ADR-06).
- **Rationale**: Closed-world principle. Implicit subsets are not queryable and not validatable.
- **Source**: User direction.
- **Enforcement**: A_RULE_14, P6, G11.

### ADR-16: Activate 18 CFR Part 201 (Natural Gas) — NEW v4

- **Decision**: Activate Gas as a first-class utility_domain. Add `ferc_account_part_201` enum with 87 accounts covering Intangibles (301-303), Production/Gathering (304-320), Products Extraction (340-347), Underground Storage (350-356), Other Storage / LNG Peak-Shaving (360-363.5), Base Load LNG Terminaling (364.1-364.8), Transmission (365-371), Distribution (374-387), and General Plant (389-399). Rename v3's `ferc_account_electric` to `ferc_account_part_101`. Add `ferc_part` ∈ {PART_101, PART_201} affiliation tag to every WBS_FERC_Linkage row.
- **Rationale**: v3 hard-coded gas as out-of-scope (`# v4 candidates (NOT active in v3; refuse with OUT_OF_SCOPE)`). The research-compiler outputs at `47.01-generated-docs/ferc-accounting-gas-universe-019e25c1e483.md` enumerated the full Part 201 universe ready to consume. Activating Part 201 unlocks NE LDC scope (Con Ed Gas, National Grid Gas, NYSEG Gas, RG&E, NFG Distribution) without forcing a parallel skill.
- **Why disjoint by ferc_part affiliation**: Account 365 means different things in Part 101 (Overhead Conductors and Devices) vs Part 201 (Land and Land Rights — gas transmission). Code-Part affiliation is dispositive; numerical overlap is not a bug.
- **Source**: 18 CFR Part 201 eCFR; `ferc-accounting-gas-universe-019e25c1e483.md`; user direction 2026-05-14.
- **Enforcement**: New `ferc_part` enum in `enums.yaml`; new column on `WBS_FERC_Linkage` tab; updated §9.1 routing procedure returns `(ferc_part, account_number)` tuple.

### ADR-17: Add `state_overlay` as 5th matrix dimension — NEW v4

- **Decision**: Add a fifth orthogonal dimension `state_overlay` to the matrix cost model. Values from `enums.yaml :: state_overlay` (NY_PSC canonical; NJ_BPU/PA_PUC/CT_PURA/MA_DPU/ME_PUC/VT_PUC/NH_PUC/RI_PUC adjacent; FEDERAL_ONLY default). New optional column on Registry + WBS_FERC_Linkage + State_Overlay_Mapping (NEW tab). Overlay does NOT change federal FERC routing — it captures whether state-specific accounting requirements (RDM / EAM / REV / ESCO separation / PGA / GSC) layer onto the booking.
- **Rationale**: v3 named "Northeast US Electric T&D" in its description but had zero coverage of NY PSC 16 NYCRR or the 8 adjacent NE state commissions. NY canonical scope requires modeling RDM reconciliation (to FERC 440/480 series), ESCO separation per 16 NYCRR 167.5/167.6 (electric) and 312.5/312.6 (gas), REV deferred-asset accounting, and EAM credits / debits. Adjacent states require similar overlay handling.
- **Why a 5th orthogonal dimension rather than embedded in WBS-A**: Same physical asset (pole, transformer, main) gets identical federal FERC routing regardless of jurisdiction; the state overlay is orthogonal context that affects revenue-side bookings, not capital-account routing. Matrix-model orthogonality is preserved.
- **Source**: NY PSC Case 14-M-0450 (2015-11-24); 16 NYCRR Chapter VI + Parts 167/312; `ferc-accounting-brief-019e25c1e2f2.md` §8.
- **Enforcement**: New `state_overlay` enum; new `State_Overlay_Mapping` workbook tab (M:N between FERC accounts and state-overlay rules); validation gate **G18** (NEW v4 — `state_overlay_eligibility_check`). Note: G16 in §13 remains the v3 "WBS-B never has FERC tag" gate; G18 is the v4-added state-overlay gate. Renumbered from an earlier draft that collided with G16.

### ADR-18: Three-view accounting — add SETTLEMENT view per ADR-08 expansion — NEW v4

- **Decision**: Expand ADR-08 two-view (estimating + capitalization) to THREE views by adding a SETTLEMENT view scoped to monthly RTO/ISO + state-overlay reconciliation. New `accounting_view` enum with values {ESTIMATING, CAPITALIZATION, SETTLEMENT}. New `rto_iso` enum {NYISO, ISO_NE, PJM, NONE, UNKNOWN}.
- **Rationale**: v3 cited NYISO Manual 23 and ISO-NE PP-4 Attachment D extensively but only for cost-estimating templates (estimating view). It did not handle the distinct downstream workflow of monthly close where NYISO/ISO-NE/PJM settlement charges and credits map to FERC 456 (credits), 557 (charges), 565 (transmission of electricity by others). The two-view model didn't accommodate this without forcing settlement into the capitalization view (which it is not — settlement is operating-period, not capital).
- **Source**: FERC AI01-1-000 Office of Enforcement; `ferc-accounting-brief-019e25c1e2f2.md` §10; `ferc-accounting-decision-register-019e25c1e099.yaml` DR-F06 (low-corroboration flag carried forward — exact FERC 456/557/565 routing is single-source and should be verified against current FERC Office of Enforcement guidance before relying on it in production close).
- **Enforcement**: New `accounting_view` + `rto_iso` enums; new validation gate **G19** (NEW v4 — `settlement_view_routing_check`); settlement-view-specific column additions in `workbook_schema.yaml` for `external_files.FERC_Accounts` and `external_files.WBS_FERC_Linkage` (YAML-canonical per ADR-19). Note: G17 in §13 remains the v3 "cross-dimension via CU only" gate; G19 is the v4-added settlement-routing gate. Renumbered from an earlier draft that collided with G17.

### ADR-19: Split storage — YAML-canonical for reference data; xlsx as derived view — NEW v4.1

- **Decision**: `FERC_Accounts`, `WBS_FERC_Linkage`, `Permits`, and `Permit_Eligibility` are **canonical YAML** under `references/` (`ferc_accounts.yaml`, `wbs_ferc_linkage.yaml`, `permits.yaml`, `permit_eligibility.yaml`). Matching workbook tabs are **derived views** regenerated on demand (e.g. `build_review_v2.py`). `workbook_schema.yaml :: sheets:` retains **13** xlsx surfaces; the four datasets are declared under `external_files:`. Future migration candidates (not yet YAML-canonical): `Labor_Pools`, `Labor_Eligibility`, `State_Overlay_Mapping`, and rate-library tabs (`Burden_Factors`, `Labor_Rates`, `Material_Indices`, `Productivity`) when appropriate.
- **Rationale**: Pure-reference catalog and join data — derived from FERC USoA + Registry structure, not interactively authored by humans — is poorly served by binary xlsx storage. YAML wins on four axes: (1) git-friendly diffs and PR review (linkage changes show up as one-line text diffs vs opaque binary blobs); (2) scriptable parsing without openpyxl, aligning with the rest of the skill's YAML-first authority chain (enums, definitions, workbook_schema, source_catalog, examples); (3) deterministic byte-stability (xlsx embeds zip metadata, app version, timestamps that are hard to suppress); (4) presentation-ready architectural artifacts — a YAML linkage file reads as "BGR family in T_SUB routes to 352 (Structures), with conditional alternate 353 (Station Equipment) where the foundation directly supports equipment," which surfaces intent more clearly than 442 Excel rows. xlsx remains the right home for interactive authoring (Registry, Master_Cost_Units), per-run audit artifacts (Run_Manifest, Validation_Log), and rate-library tabs where spreadsheet review is genuinely useful.
- **Source**: User direction 2026-05-14 (T-019/T-020/T-021; session 260514-1400).
- **Enforcement**: `workbook_schema.yaml` `external_files:` block declares YAML storage and ordering; `sheets:` retains **13** xlsx surfaces. Validation gates (G7, G12, G13, G14, G15) operate on data shape and are storage-agnostic. ADR-04 wording ("WBS_FERC_Linkage is sole FERC authority") remains substantively true — only the storage format changes. §9.1 routing reads from YAML (or the derived xlsx tab when working against an emitted workbook). `examples.yaml` NUL-byte hygiene preserved.
- **Migration pattern**: For **future** surfaces migrating to YAML — (1) port data to `references/<name>.yaml` with header comment naming `workbook_schema.yaml :: external_files.<Surface>`; (2) move the entry from `sheets:` to `external_files:`; (3) renumber xlsx tab comments; (4) update §6.1; (5) extend the review build script to regenerate derived xlsx columns; (6) validate FK integrity across split surfaces.

## 18. Version Changelog

### v4.0.0 (2026-05-14) — Part 201 activation + state overlay + settlement view

**Architectural expansion** integrating FERC research-compiler outputs from session 2026-05-14:

**FERC Part 201 (Gas) activation (ADR-16):**
- New `ferc_account_part_201` enum with 87 accounts (Intangibles, Production/Gathering, Products Extraction, Underground Storage, Other Storage / LNG Peak-Shaving, Base Load LNG Terminaling, Transmission, Distribution, General Plant)
- New `ferc_part` ∈ {PART_101, PART_201, UNKNOWN} affiliation tag on every WBS_FERC_Linkage row
- Renamed v3 `ferc_account_electric` → `ferc_account_part_101` (alias retained, will remove in v5)
- New gas branches in `branch_context`: G_TPIPE, G_TCS, G_TSTG, G_DMAIN, G_DSVC, G_DSTN, ALL_G_T, ALL_G_D
- `utility_domain` enum activates GAS_TRANSMISSION + GAS_DISTRIBUTION (previously OUT_OF_SCOPE v4 candidates)
- §9.1 routing procedure now returns `(ferc_part, account_number)` tuple

**Order No. 898 currency (effective 2025-01-01) updates to §19.3:**
- Account 351 "[Reserved]" → "Energy Storage Equipment — Transmission" (NEW per Order 898)
- Account 363 "Storage Battery Equipment" → "Energy Storage Equipment — Distribution" (relabeled per Order 898)
- Account 359.1 "Asset Retirement Costs for Transmission Plant" (ADDED — missing in v3 scope)
- Account 372 "Leased Property on Customer Premises" (ADDED — missing in v3 scope)
- New account series 158.1-158.4 Environmental Credits (NEW per Order 898; formerly REC accounting)
- New ferc_account_class values: ENVIRONMENTAL_CREDITS plus 6 gas-specific classes
- New ferc_branch_applicability values: PRODUCTION_ONLY, STORAGE_ONLY, GENERAL_ONLY, ENVIRONMENTAL_ONLY

**State overlay 5th matrix dimension (ADR-17):**
- New `state_overlay` enum: NY_PSC canonical; NJ_BPU/PA_PUC/CT_PURA/MA_DPU/ME_PUC/VT_PUC/NH_PUC/RI_PUC adjacent; FEDERAL_ONLY default
- New `INHERITS_FROM_STATE_OVERLAY` value in `ferc_account_basis`
- §2.1 expanded from 4 to 5 orthogonal dimensions
- §9 routing procedure adds §9.4 state-overlay modifier
- New `State_Overlay_Mapping` workbook tab (in the 13-tab `sheets:` contract; ADR-19 later moved four other surfaces to YAML)
- 16 NYCRR Chapter VI + Parts 167/312 + NY PSC Case 14-M-0450 added to canonical authority

**Three-view accounting (ADR-18 expanding ADR-08):**
- New `accounting_view` enum: ESTIMATING + CAPITALIZATION + SETTLEMENT
- New `rto_iso` enum: NYISO + ISO_NE + PJM + NONE + UNKNOWN
- SETTLEMENT view scoped to monthly RTO/ISO + state-overlay reconciliation
- FERC 456 / 557 / 565 explicit routing for settlement charges/credits (flagged low-corroboration per DR-F06 — verify against current FERC Office of Enforcement guidance)

**Validation gate additions (G18, G19) — renumbered:**
- **G18** `state_overlay_eligibility_check` (per ADR-17) — was drafted as G16 in earlier ADR-17 text; renumbered to avoid collision with v3 G16 (`wbs_b_no_ferc`).
- **G19** `settlement_view_routing_check` (per ADR-18) — was drafted as G17 in earlier ADR-18 text; renumbered to avoid collision with v3 G17 (`cross_dimension_via_cu_only`).
- §13 validation-gate table now covers G1–G19; `workbook_schema.gates_active` enumerates all 19; error_policy `failed_gate` range extended to `G1..G19`; `gate_type` enum adds `state_overlay_eligibility_check` and `settlement_view_routing_check`.

**Cross-references to canonical research:**
- `47.01-generated-docs/ferc-accounting-brief-019e25c1e2f2.md` — primary research brief
- `47.01-generated-docs/ferc-accounting-electric-verification-019e25c1e3bb.md` — verifies all 14 v3 electric accounts
- `47.01-generated-docs/ferc-accounting-gas-universe-019e25c1e483.md` — source of Part 201 enumeration
- `47.04-ontology-decision-traces/ferc-accounting-decision-register-019e25c1e099.yaml` — DR-F01 through DR-F08 decisions
- `47.04-ontology-decision-traces/ferc-accounting-provenance-manifest-019e25c1e22a.yaml` — authority model

**Split storage — YAML-canonical data (ADR-19, session 260514-1400):**
- Four authoritative files under `references/`: `ferc_accounts.yaml`, `wbs_ferc_linkage.yaml`, `permits.yaml`, `permit_eligibility.yaml` (row counts as built that session: 126 / 476 / 66 / 71). Matching workbook columns are **derived** — edit YAML, regenerate review workbook (e.g. `build_review_v2.py`).
- `workbook_schema.yaml` gained `external_files:`; `sheets:` holds **13** xlsx surfaces — **17** logical surfaces total.
- `examples.yaml` pre-existing NUL bytes removed; `SKILL.md` authority frontmatter lists all nine `references/*.yaml` files.

**Decisions logged:** ADR-16, ADR-17, ADR-18, ADR-19.

**Skill author note:** All 14 of v3's electric FERC accounts (303, 350, 352-358, 364-368) verified against current 18 CFR Part 101 as 100% correct — no name changes required for the v3 scope, only additions and Order-898 currency fixes.

### v3.0.0 (2026-05-14) — Architectural restructure

**Major changes:**
- Introduced normalized matrix cost model with four orthogonal cost dimensions (WBS-A asset, WBS-B labor, Permits, FERC Accounts) joined at the CU layer.
- Replaced the in-skill FERC mapping prose tables with the `FERC_Accounts` catalog tab + `WBS_FERC_Linkage` join tab.
- Removed the `ferc_account` column from the `Registry` tab. WBS_FERC_Linkage is now sole authority.
- Deprecated the `PDL` L4 branch: labor LOE rows moved to WBS-B; tangible items moved to new `ACQ` branch; design milestones moved out of cost WBS into schedule.
- Added `Permits` and `Permit_Eligibility` tabs with five-bucket taxonomy (A1/A2/A3/A4/A5) and 4-test classification procedure.
- Added `Labor_Pools` (WBS-B) and `Labor_Eligibility` tabs; CBS-to-WBS-B mapping in `Labor_Rates`.
- Added Modes C (Permit Catalog Building), D (FERC Linkage Building), E (Validation & Audit).
- Added rules A_RULE_11 through A_RULE_15 enforcing the matrix model.
- Added gates G11 through G17 enforcing relational integrity and cross-dimension discipline.
- Added drift-prevention mechanisms DP-11 (matrix_coherence) and DP-12 (catalog_vs_join_discipline).
- Added ADR log (§17) documenting every architectural decision with rationale and source.
- Updated authority list to include 23 CFR Part 645, ISO-NE PP-4 Att. D, NYISO Manual 23 / OATT §30.8, PJM Manual 14B/14C/14G, MISO MTEP25, AACE RP 96R-18, RUS Bulletin 1724E-200, NESC.

**Breaking changes from v2:**
- v2 `A_RULE_03` "L7 is the assumptions/inclusions column" is REPLACED — L7 is no longer a column. Scope assumptions live in metadata fields on L6 rows.
- v2 `WBS_L7` sheet name → renamed to `Registry`; structure restricted to L1–L6 only.
- v2 PDL.* rows → migrated to WBS-B and ACQ per ADR-12.
- v2 wbs_id format `WBS-edx-NNNNNN` surrogate → replaced by dot-path composite key `E.T.SUB.CON.BGR.FDN`.
- v2 `utility_domain` flat enum (`ELECTRIC_TRANSMISSION` / `ELECTRIC_DISTRIBUTION` / `ELECTRIC_SUBSTATION`) → replaced by hierarchical L1 (E) / L2 (T, D) / L3 (SUB, LIN) structure.

### v2.0.0 (2026-05-14, earlier session)

- Switched from utility-agnostic to Electric T&D only.
- Introduced controlled 3-letter UPPERCASE L1–L6 vocabulary.
- Added FERC USoA scaffolding (in-skill tables, later superseded by v3 catalog tabs).
- Added BGR/UGD split (carried forward to v3).
- Added burden-loading model for CUs.

### v1.1.0 (pre-2026-05-14)

- Utility-agnostic (electric, gas, water, telecom).
- Surrogate-key `wbs_id` format.
- L1–L7 hierarchy with L7 as assumptions column.
- Single utility_domain enum.

## 19. Quick References

### 19.1 L5 codes (CON sub-branches)

| Code | Element name | Where used |
|---|---|---|
| BGR | Below Grade (structural foundations / grounding) | All CON branches |
| UGD | Underground (utility infrastructure) | All CON branches |
| OVH | Overhead | LIN.CON only |
| WIR | Wire (overhead conductors) | LIN.CON only |
| SCT | Sectionalizing | LIN.CON only |
| FIB | Fiber / Comms | SUB.CON, LIN.CON |
| GCO | General Conditions | All CON branches |
| MEQ | Major Equipment | SUB.CON; D-LIN.CON only |
| STC | Site Conditions | LIN.CON only (T and D) |
| BUS | Buswork | SUB.CON only |
| CAB | Control / LV Cable | SUB.CON only |
| CHS | Control House | SUB.CON only |
| PRO | Protection & Control | SUB.CON only |
| SEC | Security (permanent) | SUB.CON only |
| SSV | Station Service | SUB.CON only |
| STR | Above-Grade Structures | SUB.CON only |
| SWK | Sitework / Yard Prep | SUB.CON only |

### 19.2 L5 codes (ACQ sub-branches)

| Code | Element name | Where used |
|---|---|---|
| LND | Land | SUB.ACQ only |
| ROW | Right of Way | LIN.ACQ only |
| PER | Permitting | All ACQ branches |
| ENV | Environmental | All ACQ branches |
| SIT | Siting | All ACQ branches |
| ICN | Interconnection Fees | All ACQ branches |
| TST | Testing (3rd-party) | All ACQ branches |

### 19.3 FERC USoA accounts in scope

**v4 update:** Account list now spans 18 CFR Part 101 (Electric) + 18 CFR Part 201 (Gas). Every row carries a `ferc_part` tag. Account names verified against current eCFR as of 2026-02-19 and against `ferc-accounting-electric-verification-019e25c1e3bb.md` for Part 101; Part 201 sourced from `ferc-accounting-gas-universe-019e25c1e483.md`.

#### 19.3.A Part 101 — Electric (40 accounts)

| Account | Title | Branch | Order 898 effect |
|---|---|---|---|
| 158.1 | Allowance Inventory | ENVIRONMENTAL | NEW per Order 898 |
| 158.2 | Allowances Withheld | ENVIRONMENTAL | NEW per Order 898 |
| 158.3 | Environmental Credits — Renewable Energy | ENVIRONMENTAL | NEW per Order 898 (formerly REC accounting) |
| 158.4 | Environmental Credits — Carbon / Emissions | ENVIRONMENTAL | NEW per Order 898 |
| 183 | Preliminary Survey and Investigation Charges | BOTH | unchanged |
| 301 | Organization | INTANGIBLE | unchanged |
| 302 | Franchises and Consents | INTANGIBLE | unchanged |
| 303 | Miscellaneous Intangible Plant | INTANGIBLE | unchanged |
| 350 | Land and Land Rights (Transmission) | T | unchanged |
| **351** | **Energy Storage Equipment — Transmission** | T | **NEW per Order 898 (was "[Reserved]" pre-v4)** |
| 352 | Structures and Improvements (Transmission) | T | unchanged |
| 353 | Station Equipment (Transmission) | T | unchanged |
| 354 | Towers and Fixtures (Transmission) | T | unchanged |
| 355 | Poles and Fixtures (Transmission) | T | unchanged |
| 356 | Overhead Conductors and Devices (Transmission) | T | unchanged |
| 357 | Underground Conduit (Transmission) | T | unchanged |
| 358 | Underground Conductors and Devices (Transmission) | T | unchanged |
| 359 | Roads and Trails (Transmission) | T | unchanged |
| **359.1** | **Asset Retirement Costs for Transmission Plant** | T | **ADDED v4 (missing in v3 scope)** |
| 360 | Land and Land Rights (Distribution) | D | unchanged |
| 361 | Structures and Improvements (Distribution) | D | unchanged |
| 362 | Station Equipment (Distribution) | D | unchanged |
| **363** | **Energy Storage Equipment — Distribution** | D | **Relabeled per Order 898 (was "Storage Battery Equipment" pre-v4)** |
| 364 | Poles, Towers and Fixtures (Distribution) | D | unchanged |
| 365 | Overhead Conductors and Devices (Distribution) | D | unchanged |
| 366 | Underground Conduit (Distribution) | D | unchanged |
| 367 | Underground Conductors and Devices (Distribution) | D | unchanged |
| 368 | Line Transformers (Distribution) | D | unchanged |
| 369 | Services (Distribution) | D | unchanged |
| 370 | Meters (Distribution) | D | unchanged |
| 371 | Installations on Customer Premises | D | unchanged |
| **372** | **Leased Property on Customer Premises** | D | **ADDED v4 (missing in v3 scope)** |
| 373 | Street Lighting and Signal Systems | D | unchanged |
| 374 | Asset Retirement Costs for Distribution Plant | D | unchanged |

#### 19.3.B Part 201 — Natural Gas (NEW v4; 87 accounts)

See `references/enums.yaml :: ferc_account_part_201` and `ferc-accounting-gas-universe-019e25c1e483.md` for the full enumeration. Working-subset for typical NE LDC:

| Account | Title | Branch | Notes |
|---|---|---|---|
| 301-303 | Intangibles (same numbers as Part 101) | INTANGIBLE | shared structure |
| 350.x | Underground Storage Plant | STORAGE | NE LDC relevant if owns storage |
| 363.1-363.5 | LNG Peak-Shaving Equipment | STORAGE | NE LDC relevant (Con Ed Astoria, NG Greenpoint, etc.) |
| 365-371 | Transmission Plant (gas) | T | 367 Mains is the primary T capital account |
| **374-387** | **Distribution Plant (gas)** | **D** | **Primary NE LDC scope; 376 Mains carries 90%+ of LDC capital** |
| 376 | Mains (gas D) | D | primary distribution capital account |
| 378 | M&R Station Equipment — General | D | district regulators |
| 379 | M&R Station Equipment — City Gate | D | city-gate take stations |
| 380 | Services (gas D) | D | service drops main → customer |
| 381 | Meters (gas D) | D | customer meters |
| 383 | House Regulators | D | premise pressure regulators |
| 385 | Industrial M&R Station Equipment | D | industrial-class M&R |
| 389-399 | General Plant | GENERAL | shared with Part 101 same numbers |

Full Part 201 universe (production, gathering, products extraction, all storage variants) is in `enums.yaml` and the gas-universe research file.

### 19.4 Permit bucket taxonomy

| Bucket | Scope | Eligibility rows? |
|---|---|---|
| A1 — Federal | Project-wide | NO (implicit) |
| A2 — State (project) | Project-wide per state | NO (implicit) |
| A3 — Local / Municipal | Project-wide per jurisdiction | NO (implicit) |
| A4 — Asset / Crossing / Site | Per individual instance | YES (explicit) |
| A5 — Activity-specific | Per construction event | YES (explicit) |

### 19.5 Validation gates summary

| Gate | What it catches | Where defined |
|---|---|---|
| G1 | Path malformed, `└─` prefix, trailing dot | §13 |
| G2 | Missing citation | §13 |
| G3 | CBS specificity in WBS labels | §13 |
| G4 | Non-IEEE/ANSI terminology | §13 |
| G5 | Duplicate L1..L6 path | §13 |
| G6 | Bad canonical phrase | §13 |
| G7 | Enum violation | §13 |
| G8 | Missing decision_trace | §13 |
| G9 | FERC validity (WBS-A and CUs) | §13 |
| G10 | Burden coherence (CUs) | §13 |
| G11 | Permit eligibility missing | §13 (NEW v3) |
| G12 | FERC routing missing on WBS-A | §13 (NEW v3) |
| G13 | FERC USoA referential integrity | §13 (NEW v3) |
| G14 | Catalog cross-reference broken | §13 (NEW v3) |
| G15 | Branch-FERC consistency | §13 (NEW v3) |
| G16 | WBS-B has FERC (forbidden) | §13 (NEW v3) |
| G17 | Cross-dimension reference outside CU | §13 (NEW v3) |
| G18 | State-overlay eligibility (ADR-17) — State_Overlay_Mapping rows resolve to valid FERC_Accounts; overlay_effect valid | §13 (NEW v4) |
| G19 | Settlement-view routing (ADR-18) — settlement-view rows route to 456/557/565 with non-null rto_iso | §13 (NEW v4) |
| V1–V9 | Universal: schema, enum, citation, UOM, confidence, vintage, license, decision trace, determinism | §13.1 |

### 19.6 Reference file locations

```
SKILL.md
references/enums.yaml                 — closed-world vocabularies
references/definitions.yaml           — IS / IS-NOT glossary
references/workbook_schema.yaml       — output contract (13 xlsx `sheets` + 4 YAML `external_files`)
references/source_catalog.yaml        — T1–T5 source tiers
references/examples.yaml              — positive / negative examples
references/ferc_accounts.yaml         — YAML-canonical FERC USoA catalog (ADR-19)
references/wbs_ferc_linkage.yaml      — YAML-canonical WBS-A → FERC join (ADR-19)
references/permits.yaml               — YAML-canonical permit catalog (ADR-19)
references/permit_eligibility.yaml    — YAML-canonical permit ↔ WBS-A eligibility (ADR-19)
```

For controlled vocabularies see `references/enums.yaml`.
For IS / IS-NOT term definitions see `references/definitions.yaml`.
For workbook output contract see `references/workbook_schema.yaml`.
For source tiering rules see `references/source_catalog.yaml`.
For positive / negative usage examples see `references/examples.yaml`.
For ADR-19 authoritative data see the four `references/*.yaml` files above (not the derived xlsx tabs).

## End of SKILL.md v4.0.0
