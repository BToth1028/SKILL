# PARA Ontology — Comprehensive Specification

**Purpose:** Single authoritative source for all PARA folder architecture rules, definitions, classification logic, placement decisions, lifecycle mechanics, and anti-patterns. Deterministic. No opinion. No ambiguity.

**Source sessions distilled:** 10 of 10 (all sessions complete)
**External research:** Tiago Forte primary sources (fortelabs.com, The PARA Method book, Building a Second Brain), Knowledge Organization Systems (KOS) literature (CLIR, ISKO, Zeng 2008, Gruber 1993), Johnny Decimal system (johnnydecimal.com), Nielsen Norman Group (information architecture taxonomy), IMERGE Consulting (enterprise taxonomy), practitioner implementations (Thomas Frank, Luca Pallotta, Matt Giaro, A Pragmatic Mind), community implementations (Claudesidian, Obsibrain, byarbrough, r/ObsidianMD, r/PKMS, Alex Bîtca), PM/engineering folder structures (PRINCE2/ITManagement101, J-PAL, WSDOT, construction PM), academic data management (UBC, Penn Libraries, Graduate Institute Geneva).

---

## 1. PARA — Core Definition

PARA is a **work-state classification model**, not a knowledge ontology. It was created by Tiago Forte as part of the Building a Second Brain (BASB) methodology.

PARA classifies information by **temporal relationship to current commitments**, not by semantic identity. It is a **production system**, not a filing system.

**PARA answers:** "What is this information for *right now*?"
**PARA does NOT answer:** "What *is* this thing?" / "How does it relate structurally to other knowledge?" / "What is its canonical or authoritative place?"

### 1.0 Irreducible Core

Across all sessions, PARA reduces to six invariants:

1. **Obligation test** — classification is driven by what obligation a file serves
2. **Single home** — every document lives in exactly one location
3. **Non-duplication** — use references instead of copies
4. **Lifecycle determinism** — transitions between states have explicit triggers
5. **Governance enforcement** — rules are formal, measurable, and enforceable
6. **Relational indexing** — cross-references handled via index layer, not folder nesting

The deepest invariant is **obligation-based classification**: "What fails if this disappears?"

### 1.0.1 Forte's Core Design Principles (From Primary Source)

- **Organize by actionability**, not by topic — PARA folders are ordered from most actionable (Projects) to least (Archive)
- **Organize by outcomes** — organization has no value in itself; it serves goal completion
- **Organize just-in-time** — make changes in small batches as you go, not in dedicated reorganization sessions
- **Organize opportunistically** — take advantage of work already being performed instead of requiring dedicated overhead time
- **Never create an empty folder** — only create structure when you have something to put in it (JIT folder creation, parallels JIT manufacturing)
- **If your organizational system is as complex as your life, the effort to maintain it will rob you of time to live it**

---

### 1.1 Letter Definitions

#### P — Projects
- **Definition:** A bounded initiative with an explicit outcome, defined success condition, and implied completion state. A series of tasks linked to a goal, with a deadline.
- **Properties:** Has a deadline or termination point. Exists to produce a specific result. Ends.
- **Diagnostic test:** "Will this folder be deleted or archived once the outcome is achieved?" -> If yes: Project.
- **Required metadata:** `status: active | paused | complete`, `owner`, `due_date`, `area_parent`
- **Capacity guideline:** Forte recommends 10-15 active projects. Enough that if stuck on one, you have alternatives. Few enough to see at a glance and review weekly.
- **Examples:** `FormBuilder_Access Refactor`, `2026 Rate Case Filing`, `Implement Layout Normalization`
- **Anti-patterns:** Ongoing responsibilities (-> Area). Tools (-> canonical asset). Concepts (-> Domain).

**False projects (must be excluded):**
- A project without a corresponding goal is a **hobby** (not a project)
- A goal without a corresponding project is a **dream** (not a project)
- A **megaproject** that is too large to complete as one unit must be broken into sub-projects

#### A — Areas
- **Definition:** A persistent domain of responsibility requiring ongoing maintenance. A sphere of activity with a standard to be maintained over time.
- **Properties:** No end date. Performance-based ("maintain", "manage", "ensure"). Represents accountability. Has standards, not deadlines.
- **Diagnostic test:** "If I stop paying attention to this, does something degrade?" -> If yes: Area.
- **Lifecycle rule:** Areas never auto-archive. Only manual demotion allowed.
- **Key distinction from Resources:** Areas are things you are **responsible for**. Resources are things you are merely **interested in**. Areas are private; Resources are shareable.
- **Examples:** `Health`, `Finances`, `Database Integrity`, `Governance Maintenance`, `Cost Estimating Governance`
- **Anti-patterns:** Anything with a finish line (-> Project). Reference material (-> Resource or Domain).
- **Psychological warning:** Viewing work only through Areas (never-ending responsibilities) kills motivation. Breaking Areas into Projects creates a cadence of regular victories.

#### R — Resources
- **Definition:** Reference material that is not actionable by itself but may support Projects or Areas. A topic or theme of ongoing interest. No obligation to act.
- **Properties:** Informational. Optional. Does not require maintenance. Not time-bound.
- **Diagnostic test:** "If I ignore this for 6 months, does anything break?" -> If no: Resource.
- **Key distinction from Areas:** Resources are topics of **interest**. Areas are domains of **responsibility**.
- **Migration rule:** If a Resource becomes operationally required -> migrate to Area. If referenced >= N times (suggest threshold of 5) -> evaluate for Area promotion.
- **Examples:** Articles, research notes, concept explanations, external documentation.
- **Critical nuance:** In rigorous systems, many items classified as "Resources" actually belong in a canonical domain taxonomy. PARA's R bucket is for convenience, not authority.

#### Archive
- **Definition:** Inactive items from Projects, Areas, or Resources that are no longer current but retained for record.
- **Properties:** Frozen. Not actively maintained. Historical. **Write-locked except by transition.** No editing inside Archive.
- **Diagnostic test:** "Is this inactive but worth keeping?" -> If yes: Archive.
- **Reactivation rule:** If reactivated -> restore to original domain (Project, Area, or Resource).
- **Critical principle:** Archive is not a graveyard — it is a **treasure chest**. Always check Archive when starting new Projects for reusable material.
- **Reset mechanism (from Forte):** If the system becomes unwieldy, create "Archive [YYYY-MM-DD]" folder, move everything in, and start fresh. Nothing is lost.
- **Examples:** Completed projects, old area notes, obsolete resource collections.

#### Inbox (Unofficial 5th Folder)
- **Definition:** A temporary capture location for incoming items that have not yet been classified.
- **Properties:** Not a PARA category. A processing buffer. Must be emptied regularly.
- **Processing rule:** Items in Inbox must be retitled (descriptive names), placed into correct PARA folder, or deleted/archived. Forte suggests 5 minutes weekly.
- **Implementation:** Set up an Inbox folder on every major platform used.
- **Numbering:** 0 (before P=1, A=2, R=3, Archive=4) to remind you to process it first.

---

### 1.2 Structural Summary

| Letter  | Time-Bound | Requires Ongoing Attention | Canonical Truth? | Actionability |
|---------|------------|---------------------------|------------------|---------------|
| P       | Yes        | Yes (until done)          | No               | Highest       |
| A       | No         | Yes                       | No               | High          |
| R       | No         | No                        | Usually No       | Low           |
| Archive | No         | No                        | No               | None          |

**What is missing from PARA:** Governance, Tools, Libraries, Core domain taxonomy. These are NOT PARA categories.

---

## 2. PARA's Role in a System

### 2.1 What PARA Is

- A **work-state classifier** (not a knowledge ontology)
- A **cross-domain filter**
- A **lifecycle lens**
- A **retrieval heuristic**
- A **navigation layer** (not an operational model)
- An **execution overlay** (a view, not a foundation)
- A **production system** (not a filing system)
- **Traffic control**, not city planning
- A **launchpad**, not a warehouse
- An **obligation-classification and lifecycle-governance architecture** for knowledge work

### 2.2 What PARA Is NOT

- A full recursive ontology
- A universal schema for every folder
- A substitute for project architecture
- A replacement for WBS/CBS breakdown structures
- A replacement for estimating phase logic
- A replacement for cost engineering taxonomy
- A replacement for deterministic project codes
- A system of record
- The vault itself
- A knowledge connection system (it does not surface cross-category relationships)

### 2.3 Position in Knowledge Organization Systems (KOS) Spectrum

PARA sits low on the KOS complexity spectrum. KOS range from simple to complex:

```
Flat lists -> Authority files -> Taxonomies -> Thesauri -> Ontologies
```

PARA is closer to a **flat classification scheme** than a taxonomy. It has four fixed categories with no hierarchical depth, no controlled vocabulary, no semantic relationships, and no formal axioms. This is intentional — it optimizes for speed and low cognitive load at the expense of semantic richness.

For systems requiring deterministic naming, domain hierarchies, stable identifiers, schema evolution, or AI-readable structure, PARA must be supplemented with a proper domain taxonomy operating on an orthogonal axis.

### 2.4 Three Conceptual Layers

PARA can operate at three distinct abstraction levels:

**Layer A — Conceptual PARA (General PKM)**
Core definitions, cognitive science foundations, productivity theory, best practices, skill maturity. Tool-agnostic, research-grounded.

**Layer B — Deterministic Structural Architecture (Operational)**
Explicit data contracts, state models, naming invariants, validation gates, error handling, deterministic project boundary enforcement, cross-reference relational index layer, archive immutability constraints. Treats PARA as a **formal governance architecture**.

**Layer C — AI-Native Extension**
AI-augmented classification, prompt libraries, version tracking discipline, automation hooks, AI-driven review assistance, knowledge graph overlays. Moves PARA into an **orchestration system for AI development workflows**.

### 2.5 PARA Strengths

| Capability                       | Rating |
|----------------------------------|--------|
| Action-oriented retrieval        | High   |
| Reducing organizational friction | High   |
| Simple mental model              | High   |
| Onboarding new systems fast      | High   |
| Personal productivity            | High   |
| Cross-platform portability       | High   |

### 2.6 PARA Weaknesses

| Limitation                        | Reason                                   |
|-----------------------------------|------------------------------------------|
| Deep technical taxonomies         | No intrinsic hierarchy                   |
| Deterministic naming systems      | Too coarse                               |
| Multi-dimensional classification  | Single-axis only                         |
| Long-term knowledge modeling      | Not semantic                             |
| Large codebases                   | Poor fit                                 |
| AI reasoning                      | Weak without stable anchors              |
| Scales to large systems           | No                                       |
| Good for archives                 | No                                       |
| Cross-category connections        | No built-in mechanism                    |
| Template/file recycling           | No clear pattern for reusable artifacts  |
| Projects-Areas boundary           | Blurrier in practice than on paper       |
| Moving folders breaks links       | File paths change when files migrate     |

### 2.7 PARA vs Taxonomy — Direct Comparison

| Dimension              | PARA               | Domain Taxonomy       |
|------------------------|---------------------|-----------------------|
| Primary purpose        | Execution & action  | Truth & structure     |
| Classification axis    | Work state          | Semantic identity     |
| Primary question       | "What am I doing?"  | "What is this?"       |
| Stability over time    | Low-Medium          | High                  |
| Re-filing frequency    | High (by design)    | Low                   |
| Cognitive load         | Low in the moment   | Higher upfront        |
| AI friendliness        | Weak alone          | Strong                |
| Scales to large systems| No                  | Yes                   |
| Automation friendliness| Low                 | High                  |
| Knowledge longevity    | Medium              | Very High             |
| Identity model         | Temporal            | Structural            |
| Naming rigor           | Minimal             | Extreme               |

**Core distinction:** They solve different problems. They are not substitutes. Treating them as substitutes is a category error.

**Dimensional independence:** Domain (structural classification) and PARA (operational state/lifecycle) are **orthogonal dimensions**. Collapsing them into one axis destroys both.

### 2.8 PARA vs Competing Systems

| System | Strength | Weakness vs PARA |
|--------|----------|------------------|
| Johnny Decimal | Rigid numbering; great for teams/stable processes | Max 10 areas x 10 categories; archive renumbering painful; official stance: don't combine with PARA |
| Zettelkasten | Networked thinking; cross-idea connections | No lifecycle management; no action orientation |
| GTD (Getting Things Done) | Task/action management | No knowledge organization; PARA complements GTD |
| Topic-based folders | Intuitive for small systems | Scales poorly; no lifecycle; AI-unfriendly |

**Hybrid approaches:** PARA as top-level structure + Zettelkasten linking within notes is common and valid. PARA handles "where does this belong?"; Zettelkasten handles "how does this connect?"

### 2.9 What PARA Buys You (Exactly Three Things)

1. **Frictionless action** — Active work floats to the top.
2. **Automatic decay** — Finished work naturally drops into Archives.
3. **Psychological clarity** — Your vault mirrors your current commitments.

Anything beyond that is over-attribution.

### 2.10 What PARA Costs You (If Used For Everything)

1. **Loss of canonical structure** — Same concept appears in multiple places over time.
2. **Historical ambiguity** — Past decisions lose context once projects move.
3. **Weak composability** — Harder to reason across domains.
4. **AI degradation** — Models struggle without stable semantic anchors.
5. **Reclassification overhead** — You are constantly "gardening" files.

**PARA is anti-ontology by design.**

### 2.11 Why PARA Fails

**PARA fails behaviorally, not structurally.** Common decay vectors:
- Over-engineering the structure
- Resource hoarding (collecting without using)
- No review cadence
- Topic-based drift (classifying by subject instead of obligation)
- Governance neglect
- Confusing Projects with Areas (the most common structural error per Forte)
- Treating PARA as filing system rather than production system

---

## 3. The Two-Layer Architecture

### 3.1 The Correct Mental Model

Think in **layers**, not choices.

**Layer 1 — Canonical truth (taxonomy)**
- Stable domain folders. Deterministic naming. Long-lived references. AI-readable structure.
- Answers: "What is this?"

**Layer 2 — Execution view (PARA)**
- A projection over the canonical layer. Short-lived. Human-optimized. Disposable.
- Answers: "What am I doing with this right now?"

**PARA is a lens, not a foundation.**

In a fully mature system, PARA would not be folders at all — it would be **metadata-driven**. Root-level PARA is the closest folder approximation to that philosophy.

### 3.2 Vault Root Structure

PARA and the canonical taxonomy coexist as **parallel systems** at the vault root — not parent/child.

```
/(VAULT ROOT)
  /0_Inbox/             <- Capture buffer (process first)
  /1_Projects/          <- PARA: time-bound outcomes
  /2_Areas/             <- PARA: ongoing responsibilities
  /3_Resources/         <- PARA: optional, non-authoritative
  /4_Archive/           <- PARA: archived PARA material

  /Governance/          <- Canonical: rules, doctrine
  /Domains/             <- Canonical: subject taxonomy
  /Tools/               <- Canonical: reusable tools
  /Libraries/           <- Canonical: reusable building blocks
  /Sessions/            <- Historical: process artifacts
```

**Numbering rationale (from Forte):** Number 0-4 ensures correct sort order regardless of platform. Inbox at 0 reminds you to process it first. Order follows actionability gradient.

**Cross-platform mirroring (from Forte):** Maintain the same Project and Area names across all apps/platforms. Priorities and organization should be consistent regardless of tool. However, not every platform needs every folder.

### 3.3 Why PARA Must Be at Root (Not Under Each Domain)

Nesting PARA under domains causes dimension collapse (see 2.7). Root-level preserves lifecycle as independent axis; cross-domain project references; centralized archive; reusable resources; simpler portfolio layer.

---

## 4. Root-Level vs Nested PARA

### 4.1 Root-Level PARA (Recommended Default)

PARA at root. Inside projects, organize by **what the project needs**, not by PARA.

### 4.2 Nested PARA (Exception Only)

Only when project runs long-term, contains independent sub-projects, has heavy research/reference needs, or resembles a portfolio.

### 4.3 Nesting Decision Rule

| Condition | Action |
|-----------|--------|
| Project has single outcome | No inner PARA |
| Project has < 4 structural domains | No inner PARA |
| Project behaves like a department | Consider inner |
| Project contains multiple independent initiatives | Consider inner |
| You're unsure | Do NOT nest |

**Default bias: flat within project.**

---

## 5. What Lives Inside PARA

### 5.1 Cardinal Rule

> **Nothing in PARA should be irreplaceable.**

If deleting a PARA folder would destroy knowledge -> the system is wrong.

### 5.2 PARA Subfolder Templates

#### Project Subfolders (Obsidian / Notes)
```
P/<project-name>/
    index.md, status.md, working-notes.md, decisions.md, open-questions.md
```

#### Project Subfolders (File System / Formal)
```
P/{project-slug}/
    00_meta/ 01_inputs/ 02_working/ 03_outputs/ 04_archive/
```

#### 5.2.1 Project Subfolder Content Manifests (File System / Formal)

The formal variant intentionally extends Forte's flat-folder guidance for project work involving high file volume, binary/non-Markdown files, or lifecycle states that must be visible in the filesystem rather than in metadata. This extension is acknowledged as **not part of Forte's canonical PARA** — it is a governed formalization layered onto PARA for structured, file-system-based project execution.

**Lifecycle flow:** Inputs are given → Working is created → Outputs are accepted → Archive captures superseded material.

##### `00_meta/` — Project Identity & Governance

Purpose: Everything needed to understand what this project IS, who owns it, what rules govern it, and what state it's in. The "label on the box." Read-mostly after project initialization.

| File | Mandatory | Purpose |
|------|-----------|---------|
| `index.md` | **YES** | Project identity: domain links, phase, governing rules, canonical system references. Replaces "knowing the folder structure." |
| `status.md` | No | Current state: In Progress / Blocked / Paused / Next. Becomes meaningless after project ends. |
| `decisions.md` | No | While forming: options, tradeoffs, leanings. Once final: rule promotes to canonical governance; history stays or archives. |
| `open-questions.md` | No | Unresolved items. Prevents half-truths from leaking into canonical files. |
| `scope.md` | No | Project scope definition, success criteria, constraints. Equivalent to PID/charter in project management. |

**Prohibited:** Working notes (→ `02_working/`), source material (→ `01_inputs/`), deliverables (→ `03_outputs/`), active task lists (→ `02_working/` or external task manager).

##### `01_inputs/` — Source Material & Seed Data

Purpose: Everything given to the project or gathered for it. Material that existed before project work began. Read-mostly after initial population.

| Category | Examples |
|----------|----------|
| Requirements & briefs | Client RFP, scope statement, SOW, design brief |
| Reference documents | Standards, codes, specs referenced by this project |
| External data | Rate tables, survey data, GIS files, raw datasets |
| Correspondence | Key emails, meeting notes, directives that initiated work |
| Baseline/seed files | Templates, starting-point models, inherited artifacts |
| Governing documents | Contracts, permits, regulatory approvals (copies, not originals) |

**Prohibited:** Anything created by the project team during execution (→ `02_working/` or `03_outputs/`), project identity files (→ `00_meta/`), superseded versions of inputs (→ `04_archive/`).

##### `02_working/` — Active Execution Space

Purpose: Where in-progress work happens. Drafts, calculations, analysis, scratch thinking. Nothing here is authoritative or final.

| Category | Examples |
|----------|----------|
| Working notes | Messy thinking, scratch calculations, exploratory analysis |
| Drafts | In-progress deliverables not yet accepted |
| Analysis-in-progress | Spreadsheets being built, models being calibrated |
| Task tracking | Active checklists, WIP kanban states, daily logs |
| AI conversation logs | Session transcripts, agent outputs under review |
| Intermediate products | Processed data, intermediate calculations, staging files |

**Prohibited:** Accepted/final deliverables (→ `03_outputs/`), source material (→ `01_inputs/`), project identity (→ `00_meta/`), superseded drafts no longer in play (→ `04_archive/`).

**Key principle:** "Messy, unsafe thinking. None of this belongs in canonical files yet."

**Obsidian variant mapping:** `working-notes.md` maps here, NOT to `00_meta/`.

##### `03_outputs/` — Accepted Deliverables

Purpose: Final, accepted products of the project. Things that have crossed the acceptance threshold.

| Category | Examples |
|----------|----------|
| Final deliverables | Submitted bid, final report, accepted design, published artifact |
| Accepted artifacts | Agent-produced files accepted as deliverables |
| Final datasets | Cleaned, validated, publication-ready data |
| Presentation materials | Final slide decks, client-facing documents |
| Exported/published content | PDFs for distribution, signed documents |

**Prohibited:** Drafts still in progress (→ `02_working/`), source material (→ `01_inputs/`), superseded final versions (→ `04_archive/`), working calculations that produced the outputs (→ `02_working/`).

**Promotion trigger:** A file moves from `02_working/` to `03_outputs/` when it is **accepted as a deliverable** — by the client, by the owner, or by the project's acceptance criteria.

##### `04_archive/` — Project-Level Archive

Purpose: Inactive material from THIS project. Superseded versions, completed task records, abandoned approaches. Still retrievable but out of the way.

| Category | Examples |
|----------|----------|
| Superseded drafts | V1, V2 of deliverables replaced by final version |
| Completed task records | Closed-out checklists, resolved issue threads |
| Baseline snapshots | Original budget, original schedule before changes |
| Abandoned approaches | Explored alternatives that were discarded |
| Old correspondence | Historical emails/notes no longer actively referenced |
| Change control history | Approved/rejected change requests |

**Prohibited:** Material from other projects (→ vault-level `/4_Archive/`), content that should be promoted to canonical (→ `/Governance/`, `/Domains/`, `/Libraries/`), content still actively referenced (stays in `01_inputs/` or `02_working/`).

##### Project-Level vs Vault-Level Archive Distinction

| Level | Location | Contains | Trigger |
|-------|----------|----------|---------|
| Project-level | `P/{slug}/04_archive/` | Superseded versions, old drafts within an **active** project | Draft superseded, approach abandoned |
| Vault-level | `/4_Archive/projects/` | Entire **completed** project folders | Project complete, all deliverables accepted |

When a project completes, the ENTIRE project folder (including its `04_archive/`) moves to `/4_Archive/projects/`.

#### Area Subfolders
```
A/{area-slug}/
    00_meta/ 01_standards/ 02_operational/ 03_records/
```

#### Resource Subfolders
```
R/{resource-domain}/
    01_reference/ 02_templates/ 03_research/ 04_snippets/
```

#### Archive Subfolders
```
Archive/
    projects/ areas/ resources/
```

### 5.3 File Role Definitions (Obsidian Project Files)

**index.md (mandatory, non-negotiable)**
- What domain(s) this touches
- What canonical systems it links to
- What phase the work is in
- Links to governing rules
- This file REPLACES "knowing the folder structure"

**status.md** — In progress / Blocked / Next. Becomes meaningless after project ends (that is correct).

**working-notes.md** — Messy, unsafe thinking. None of this belongs in canonical files yet.

**decisions.md** — While decisions forming: options, tradeoffs, leanings. Once final: rule moves to canonical governance; history stays or is archived.

**open-questions.md** — Prevents half-truths leaking into the system. Canonical systems should never contain open questions.

#### 5.3.1 Obsidian-to-Formal Variant Mapping

The Obsidian/Notes files map to formal subfolders as follows:

| Obsidian File | Formal Subfolder | Rationale |
|---------------|------------------|-----------|
| `index.md` | `00_meta/index.md` | Project identity |
| `status.md` | `00_meta/status.md` | Project state |
| `decisions.md` | `00_meta/decisions.md` | Decision governance |
| `open-questions.md` | `00_meta/open-questions.md` | Unresolved items |
| `working-notes.md` | `02_working/` | Execution material, NOT identity — does not belong in `00_meta/` |

### 5.4 Allowed vs Prohibited PARA Content

**Allowed:** Links to canonical files, working notes, scratch synthesis, task-specific views, short-lived drafts, decision workspaces, project coordination material, open questions.

**Prohibited:** Authoritative specs, finalized doctrine, stable definitions, long-term references, anything AI must reason over, tools, libraries, governance rules.

### 5.5 PARA Filenames Are Intentionally Generic

If you need the domain in the filename, that file belongs in the canonical system.

### 5.6 Do NOT Duplicate Domain Structure Inside PARA

PARA folders must NEVER mirror the canonical taxonomy. If you duplicate your domain structure inside PARA: you reintroduce classification friction, create two sources of truth, force decisions PARA is meant to postpone, and guarantee drift.

---

## 6. Information Flow Between PARA Categories

PARA is a **dynamic system**. Information flows bidirectionally between all four categories:

| From | To | Trigger |
|------|----|---------|
| Project | Area | Project becomes long-term ongoing responsibility |
| Project | Resource | Intermediate work (brainstorms, research, diagrams) may be useful for future projects |
| Project | Archive | Project completed or put on hold |
| Area | Project | New time-bound initiative spawned from area responsibility |
| Area | Resource | Note relevant to others beyond personal responsibility |
| Area | Archive | Area ceases to be active responsibility |
| Resource | Project | Interest becomes full project |
| Resource | Area | Realize resource applies to area of responsibility |
| Resource | Archive | Topic no longer of interest |
| Archive | Any | Reactivation needed; restore to original category |

---

## 7. How PARA Interacts With Canonical Structure

### 7.1 Navigation Mechanics

PARA **never owns truth**. PARA **links to truth**. Truth lives in: /Governance, /Domains, /Tools, /Libraries.

### 7.2 Single-Home + Index Duality

Every document lives in exactly ONE location. Cross-references handled via relational index layer, never by duplicating files.

### 7.3 Retrieval Flow

1. "What am I working on?" -> PARA
2. "What is this concept/system?" -> Canonical domain
3. "Where did this decision come from?" -> Backlink to PARA index

---

## 8. Lifecycle Rules

### 8.1 PARA-Only File Futures

Every PARA-only file must satisfy exactly ONE: Deleted, Archived verbatim, Collapsed into canonical artifact, Replaced by link to promoted result.

### 8.2 Transition Conditions (Formal Triggers)

- **Project -> Archive:** status == complete AND no open tasks AND deliverables accepted
- **Resource -> Area:** becomes required standard OR referenced >= N threshold
- **Area -> Project:** Never automatic. Only when temporary initiative created.
- **Archive -> Original:** Reactivation needed; restore to original domain.

### 8.3 Weekly Maintenance (From Forte)

5-minute weekly process:
1. Retitle items in Inbox (make names descriptive)
2. Place items into correct PARA folders
3. Update active project statuses

Monthly/quarterly: elevated review of Areas and long-term goals.

---

## 9. Classification of Non-PARA Items

### 9.1 Projects vs Tools vs Libraries

| Item | Ends? | Reused? | Lives Where |
|------|-------|---------|-------------|
| Project | Yes | No | PARA |
| Tool | No | Yes | Canonical |
| Library | No | Yes | Canonical |
| Working notes | Yes | No | PARA |
| Specs / doctrine | No | Yes | Canonical |

### 9.2 Governance

Governance rules are: Authoritative, Cross-project, Long-lived, Normative ("must / must not"), Referenced repeatedly, AI-consumed.

**Classification:** Governance is **doctrine**, not execution. It belongs exclusively in the canonical taxonomy. PARA must never be the system of record for governance.

**Why governance is NOT a PARA Area:** Areas are ongoing responsibilities. Governance is not a responsibility — it is **authority**.
**Why governance is NOT a PARA Resource:** Resources are optional reference material. Governance is mandatory and normative.
**Why governance is NOT a PARA Project:** Projects end. Governance persists. Only *changes to governance* are projects.

**Canonical location:**
```
/Governance/
    /Filesystem/    (folder-structure.md, file-naming.md, lifecycle-rules.md, enforcement.md)
    /Obsidian/      (vault-structure.md, para-overlay-rules.md, promotion-criteria.md)
```

**PARA's only relationship to governance:**
1. Link to governance files from project indexes
2. Temporarily draft/revise governance (as proposals, not rules) in a PARA project
3. Capture governance impact on a project in working notes

**Governance lifecycle:** Drafted (PARA, temporary) -> Ratified (canonical) -> Referenced (linked from PARA) -> Enforced (applied everywhere) -> Never moved again. PARA participates only in drafting and referencing.

### 9.3 Session Summaries

Historical process artifacts -> /Sessions/ with naming: `YYYY-MM-DD_<subject-slug>_session-summary.md`

**Type A (Working):** Historical records. Not active execution. Not normative truth. -> /Sessions/
**Type B (Distilled):** When a summary becomes doctrine, it is a promoted canonical artifact -> /Governance/, /Domains/, /Tools/ depending on what it became.

### 9.4 AI Prompts

AI prompts are **governed knowledge artifacts**. Canonical location: `/R/prompts/`. Domain: `prompts`. Prefix: `prm.`

| Tier | Prefix | Definition | Stability | Scope | Decision Test |
|------|--------|------------|-----------|-------|---------------|
| System | prm.sys. | Governs workflows or enforces structure. Infrastructure. | Very high | Cross-workflow | "If this disappeared, would multiple workflows degrade?" |
| Library | prm.lib. | Stable, reusable prompts for recurring tasks. | High | Task-specific | "Is this reusable but not depended on by other prompts?" |
| Experimental | prm.exp. | Unproven, volatile, exploratory. Sandboxes. | Low | Unknown | "Am I still tuning this?" |

**Default when unsure:** lib. **Lifecycle:** exp -> lib -> sys (rare). If too many are sys, you're over-classifying.

### 9.5 Multi-Project Files

Place in /R/{shared-domain}/, reference from projects. Never duplicate.

---

## 10. Utility Estimator PARA Application

Standard root structure with Projects (active bids), Areas (cost models, standards), Resources (RSMeans, FERC, templates), Archive (closed bids). Inside projects: 01-Scope through 06-Final-Submission. Obsidian vault as Area (institutional memory engine).

### 10.1 Construction Estimating Project Subfolder Mapping

For the formal variant (`00_meta / 01_inputs / 02_working / 03_outputs / 04_archive`), construction estimating content maps as follows:

| Content Type | Subfolder | Rationale |
|--------------|-----------|-----------|
| Client RFP / bid package | `01_inputs/` | Given to project, not created by it |
| Quantity takeoffs in progress | `02_working/` | Active execution |
| Rate table references | `01_inputs/` | Source data (or linked from `/3_Resources/`) |
| Draft estimate spreadsheet | `02_working/` | Not yet accepted |
| Final submitted bid | `03_outputs/` | Accepted deliverable |
| Superseded estimate v1 | `04_archive/` | Replaced by final |
| Project scope definition | `00_meta/scope.md` | Project identity |
| WBS for this project | `02_working/` while developing; `03_outputs/` when accepted |
| Subcontractor quotes | `01_inputs/` | External data given to project |
| Labor crew composition sheets | `02_working/` while developing; `03_outputs/` when final |
| Project-specific CU definitions | `02_working/` while developing; promote to `/Libraries/cost-models/` or `/Domains/` when stabilized |

---

## 11. Decision Rules (Deterministic)

### 11.1 Formal Classification Algorithm (Sequential)

**Step 1:** Does it have a defined outcome with a completion condition? -> YES = Project
**Step 2:** Is it an ongoing responsibility with no defined end? -> YES = Area
**Step 3:** Is it reference material not tied to current responsibility? -> YES = Resource
**Step 4:** Is it inactive, completed, or obsolete? -> YES = Archive
**Step 5:** None of above -> INVALID (resolve ambiguity before proceeding)

### 11.2 Forte's Quick Decision Flowchart

```
New information arrives
    -> Does it have a deadline? 
        YES -> Is it multi-step? 
            YES -> PROJECT
            NO -> Add to active project tasks
        NO -> Is it an ongoing responsibility?
            YES -> AREA
            NO -> Is it useful reference?
                YES -> RESOURCE
                NO -> ARCHIVE (or delete)
```

### 11.3 Supplementary Classification Questions

Q1-Q8 series testing for: project/responsibility origin, 3-year persistence, subfolder temptation, temporality, disposability, execution vs definition, cross-project governance, post-project relevance.

---

## 12. Naming Conventions

- **Files:** `{YYYYMMDD}_{descriptor}_{type}.{ext}`
- **Slugs:** lowercase, hyphen-separated, no spaces, regex: `^[a-z0-9-]+$`
- **Sessions:** `YYYY-MM-DD_<subject-slug>_session-summary.md`
- **Forte's convention:** Emoji prefix for Projects, CAPITALS for Areas, lowercase for Resources

---

## 13. Enforcement Constraints

1. No nested PARA inside PARA
2. Projects cannot contain Areas
3. Areas cannot contain Projects
4. Resources cannot contain active deliverables
5. Archive is write-locked except by formal transition
6. A file can only exist in ONE domain
7. No editing inside Archive
8. If reactivated from Archive -> restore to original domain
9. Governance must not live inside PARA
10. Never duplicate items across categories (use references)
11. Never create empty folders (JIT creation only)

---

## 14. Anti-Patterns (Explicit Prohibitions)

1. Using PARA as the entire vault structure
2. Nesting PARA inside every project or under each domain
3. Duplicating domain structure inside PARA
4. Putting governance rules, tools, libraries, or irreplaceable content in PARA
5. Encoding taxonomy in PARA filenames
6. Treating PARA as a system of record
7. Creating deep domain trees inside PARA folders
8. Using PARA for anything AI must reason over long-term
9. Putting open questions or "maybe" files in canonical systems
10. Archiving the Obsidian vault
11. Editing files inside Archive
12. Collapsing domain and lifecycle dimensions into one axis
13. Confusing Projects (deadlines) with Areas (standards)
14. Over-engineering the structure (complexity kills adoption)
15. Organizing by topic instead of by actionability

---

## 15. Enterprise Governance Layer

### 15.1 Principles

- **Quantification:** Structural integrity expressed through measurable variables
- **Enforceability:** Rules produce observable pass/fail states
- **System Boundary Integrity:** All repositories share invariant governance definitions

### 15.2 Governing Variables

| Variable | Abbr | Definition | Risk Direction |
|----------|------|------------|----------------|
| Active Project Count | APC | Number of concurrent deliverable-bound projects | Up increases entropy risk non-linearly beyond threshold |
| Entropy Index | EI | Composite indicator from APC, AGR, GDR | Threshold breach predicts retrieval degradation |
| Archive Growth Rate | AGR | Rate of archival accumulation | Up without review introduces stagnation risk |
| Governance Drift Rate | GDR | % items violating review cycle or classification rules | Up predicts structural decay |
| Synchronization Divergence Rate | SDR | % mismatch across repositories under shared governance | Up predicts audit inconsistency |
| Recovery Exposure Window | REW | Time between last recoverable state and current | Up increases disaster recovery risk |
| Complexity Cost Factor | CCF | Review time + migration time + synchronization effort | Up reduces system sustainability |

### 15.3 Canonical Models

- **Entropy Model:** EI = f(APC, AGR, GDR). Threshold breach triggers governance intervention.
- **Lifecycle Risk Model:** Risk = AGR x GDR x Review Latency. Archive stagnation increases systemic opacity.
- **Complexity Cost Model:** CCF = structural layers x repositories x review cycles.
- **Benchmarking Model:** Performance evaluated via retrieval latency, APC stability, GDR, CCF relative to baseline.
- **Audit Traceability Framework:** Every artifact must have traceable lineage (origin -> modification -> archive). Binary: traceable or non-traceable.
- **Synchronization Invariant Model:** All repositories must maintain identical classification and lifecycle states. Divergence beyond SDR threshold triggers reconciliation.
- **Disaster Recovery Model:** Define RTO and RPO. REW must not exceed defined RPO.

### 15.4 Enterprise Tradeoffs

- Measurement Rigor vs Operational Overhead (higher precision increases CCF)
- Archive Retention vs Stagnation Risk (higher retention increases AGR)
- Synchronization Strictness vs Flexibility (lower SDR tolerance increases coordination cost)
- Metric Granularity vs Enforcement Fatigue (excess measurement increases GDR)

### 15.5 Enterprise Failure Modes

- **Entropy Saturation:** APC exceeds threshold -> retrieval degradation, stalled migration
- **Archive Stagnation:** AGR high + review inactivity -> loss of institutional memory clarity
- **Governance Drift:** GDR exceeds threshold -> classification inconsistency, audit vulnerability
- **Synchronization Divergence:** SDR beyond tolerance -> repository inconsistency, audit failure
- **Recovery Failure:** REW exceeds RPO -> unrecoverable artifact loss
- **Traceability Breakdown:** Artifact lacks modification lineage -> non-auditable state

### 15.6 Open Enterprise Questions (Empirical Calibration Needed)

- What APC threshold defines entropy saturation at different scales?
- What SDR percentage constitutes unacceptable repository divergence?
- What AGR level predicts stagnation risk onset?
- What CCF value marks unsustainable governance overhead?
- What retrieval latency baselines define acceptable enterprise performance?

---

## 16. Mental Models

- **Taxonomy holds truth. PARA holds attention.**
- **Canonical files = published papers. PARA files = lab notebooks.**
- **Projects are verbs. Tools and libraries are nouns.**
- **Governance = Constitution. PARA projects = Court cases.**
- **Projects without goals = hobbies. Goals without projects = dreams.**

---

## 17. Definitions

**PARA:** Work-state classification model (P/A/R/Archive) classifying by temporal relationship to commitments.
**Canonical:** Authoritative, stable, long-lived location for knowledge. Project-independent.
**Promotion:** Extracting stabilized knowledge from PARA into canonical domain structure.
**Frontmatter:** Structured metadata block (YAML) defining file identity, classification, and relationships.
**Obligation-Based Classification:** Deepest PARA invariant — classify by what obligation is served and what fails if removed.
**Dimensional Independence:** Domain and PARA are orthogonal axes that must not be collapsed.
**False Project:** An item masquerading as a project that is actually a hobby (no goal) or dream (no project) or megaproject (needs decomposition).
**JIT Organization:** Just-in-time folder/structure creation; never pre-build empty structures.

---

## 18. Session Summary Frontmatter Schema

```yaml
---
type: session-summary
date: YYYY-MM-DD
session_id: YYYY-MM-DD_<subject-slug>
subject: <Human-readable label>
status: archived        # active | archived | promoted
related_projects:
  - <project-slug>
related_domains:
  - <domain/path>
canonical_outputs:
  - <domain/path/to/promoted-artifact>
supersedes: null
superseded_by: null
---
```

---

## 19. Sources and References

### Primary Sources
- Forte, Tiago. *The PARA Method: Simplify, Organize, and Master Your Digital Life.* Atria Books, 2023.
- Forte, Tiago. *Building a Second Brain.* Atria Books, 2022.
- Forte, Tiago. "The PARA Method: The Simple System for Organizing Your Digital Life in Seconds." fortelabs.com/blog/para/
- Forte, Tiago. "P.A.R.A. II: Operations Manual." Medium/Praxis, 2017.

### Knowledge Organization Systems
- Hodge, Gail. "Systems of Knowledge Organization for Digital Libraries." CLIR/DLF, 2000.
- Zeng, Marcia Lei. "Knowledge Organization Systems (KOS)." Knowledge Organization, 35(3/2), 160-182, 2008.
- Gruber, Thomas R. "A translation approach to portable ontologies." Knowledge Acquisition, 5/2, pp. 199-220, 1993.
- ISKO Encyclopedia of Knowledge Organization: "Ontologies as KOS" (isko.org/cyclo/ontologies)
- Nielsen Norman Group. "Taxonomy 101: Definition, Best Practices." nngroup.com, 2024.

### Competing/Complementary Systems
- Noble, Johnny. Johnny Decimal System. johnnydecimal.com
- Luhmann, Niklas. Zettelkasten method (atomic notes, bidirectional linking)
- Allen, David. Getting Things Done (GTD). Task/action management complement to PARA.

### Practitioner Analysis
- Thomas J. Frank. "The PARA Method by Tiago Forte — Summary and Book Notes." thomasjfrank.com, 2023.
- Luca Pallotta. "The PARA Method: How I Organize my Digital Information." lucapallotta.com, 2024.
- A Pragmatic Mind. "The PARA Method: A Pragmatic Guide." apragmaticmind.com, 2026.
- IMERGE Consulting. "Introduction to Classification, Taxonomy and File Plans." imergeconsulting.com, 2022.

### Community Implementations (Project Subfolder Research, 2026-04-15)
- Bîtca, Alex. "Enhancing the PARA Method: Adding Structure & Clarity to Projects." Medium, 2023.
- Claudesidian (heyitsnoah). PARA vault organization with project subfolders. deepwiki.com/heyitsnoah/claudesidian, 2024.
- byarbrough. obsidian-para template (flat project structure). github.com/byarbrough/obsidian-para.
- Obsibrain. P.A.R.A. Folder Structure documentation. docs.obsibrain.com, 2026.
- r/ObsidianMD. "Anyone using PARA?" community discussion. reddit.com/r/ObsidianMD, 2025.

### Project Management Folder Structures (Cross-Discipline)
- ITManagement101. "Template folder structure for Project Management." itmanagement101.co.uk, 2023. (PRINCE2-based)
- J-PAL North America. "Template Folder Structure." povertyactionlab.org. (Academic research)
- WSDOT. "Electronic Engineering Data Standards Manual M 3028." wsdot.wa.gov. (Civil engineering)
- All Things Construction PM. "Construction Project Management Folder Template." allthingsconstructionpm.com, 2023.
- UBC Library Research Commons. "Directory Structures." ubc-library-rc.github.io. (Academic research data management)
- Forte, Tiago. "Why PARA Is the Key to the AI Era." fortelabs.com, 2026.

---

*Specification complete. All 10 source sessions distilled. External research incorporated. §5.2.1 amended 2026-04-15 with project subfolder content manifests based on exhaustive cross-source research (30+ sources: Forte primary, GitHub, Reddit, Obsidian forums, PM/PRINCE2, construction engineering, academic research). Document is authoritative for deterministic PARA classification decisions.*
