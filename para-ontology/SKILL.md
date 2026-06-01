---
name: para-ontology
description: "Deterministic PARA folder architecture classification engine. Use this skill whenever the user asks about PARA folder structure, file placement, folder organization, where a file should go, how to classify a document, project vs area vs resource distinction, archive rules, lifecycle transitions, vault structure, Obsidian vault organization, folder naming conventions, governance file placement, canonical vs PARA content, or anything related to the PARA method (Projects, Areas, Resources, Archives). Also trigger when the user mentions Tiago Forte, Building a Second Brain, BASB, folder ontology, knowledge organization, file taxonomy, or asks where does this go about any file or folder. Trigger even for casual mentions like should this be a project or area, how do I organize my files, is this a resource or an area, or where would X live in my system. When in doubt, trigger - a bad trigger is better than a missed classification question."
---

# PARA Ontology - Deterministic Classification Engine

## Purpose

This skill deterministically answers: **"Where does this file/folder/artifact go?"**

Same inputs MUST produce identical outputs. No opinion. No ambiguity. Every classification follows
a fixed-step algorithm and produces a decision trace.

Before answering ANY PARA question, read the full reference specification:
**`/mnt/skills/user/para-ontology/references/PARA_Ontology_Bible.md`**

That file is the single source of truth. This SKILL.md is the decision engine that operates on it.

___

## Core Invariants (Never Violate)

1. **Obligation test** - classify by what obligation a file serves ("What fails if this disappears?")
2. **Single home** - every document lives in exactly one location
3. **Non-duplication** - use references instead of copies
4. **Lifecycle determinism** - transitions have explicit triggers, not discretion
5. **Governance enforcement** - rules produce pass/fail, not advisory
6. **Relational indexing** - cross-references via index layer, not folder nesting

___

## Classification Algorithm (Execute Sequentially - Stop at First Match)

For ANY file/folder/artifact, run these steps IN ORDER:

### STEP 0 - Is this outside PARA entirely?

Ask: "Does this define how the system must behave across all projects?"
- YES → `/Governance/` - STOP

Ask: "Is this a reusable tool or library that outlives any project?"
- YES → `/Tools/` or `/Libraries/` - STOP

Ask: "Is this a domain-level canonical artifact that must be readable without project context?"
- YES → `/Domains/` - STOP

Ask: "Is this a historical session summary / process artifact?"
- YES → `/Sessions/` - STOP

If none → proceed to STEP 1.

### STEP 1 - Project?

Ask: "Does it have a defined outcome with a completion condition and deadline?"
- YES → **Project** (`/P/{project-slug}/`)
- NO → STEP 2

### STEP 2 - Area?

Ask: "Is it an ongoing responsibility with no defined end, where quality degrades if neglected?"
- YES → **Area** (`/A/{area-slug}/`)
- NO → STEP 3

### STEP 3 - Resource?

Ask: "Is it reference material not tied to current responsibility - a topic of interest, not obligation?"
- YES → **Resource** (`/R/{resource-domain}/`)
- NO → STEP 4

### STEP 4 - Archive?

Ask: "Is it inactive, completed, or obsolete but worth retaining?"
- YES → **Archive** (`/Archive/{origin-type}/`)
- NO → STEP 5

### STEP 5 - Unclassified

Item is INVALID. Return structured error:
```
CLASSIFICATION: FAILED
REASON: Item does not match any PARA category or canonical domain.
ACTION_REQUIRED: Resolve ambiguity. Provide: (a) what obligation it serves,
(b) whether it has a deadline, (c) whether neglecting it causes degradation.
```

___

## Supplementary Decision Tests (Use When Algorithm Alone Is Insufficient)

Run these ONLY if the sequential algorithm produces ambiguity:

| Question | If YES | If NO |
|----------|--------|-------|
| Will this still make sense in 3 years with no project context? | Canonical domain | PARA |
| Am I tempted to create subfolders to organize this? | Does NOT belong in PARA | May belong in PARA |
| Is this temporary / disposable? | PARA | Canonical |
| Is this primarily about execution, not definition? | PARA | Canonical |
| Does this still matter after this project ends? | Canonical | PARA |
| If I saw this file alone, would it make sense? | Canonical | PARA (needs project context) |

___

## Output Contract

Every classification response MUST include:

```yaml
classification:
  destination: <exact folder path>
  category: <Project | Area | Resource | Archive | Governance | Tool | Library | Domain | Session | INVALID>
  decision_trace:
    - step: <step number that matched>
    - question: <the diagnostic question asked>
    - answer: <YES or NO>
    - reason: <1-line justification>
  constraints_checked:
    - single_home: true
    - no_duplication: true
    - no_governance_in_para: true
    - nothing_irreplaceable_in_para: true
  warnings: <any edge cases or migration triggers detected>
```

___

## Boundary Rules (Hard Constraints)

### What MUST NOT live in PARA
- Governance rules, doctrine, axioms, standards
- Tools or libraries (reusable assets)
- Anything irreplaceable
- Canonical domain knowledge
- Anything AI must reason over long-term
- Finalized specs or stable definitions

### What MUST NOT live in Canonical
- Open questions ("maybe" files)
- Working notes tied to a specific project
- Unresolved decision workspaces
- Execution checklists, status trackers

### Archive Rules
- Write-locked except by formal transition
- No editing inside Archive
- If reactivated → restore to original category
- Archive is a treasure chest, not a graveyard

### Enforcement Constraints
1. No nested PARA inside PARA
2. Projects cannot contain Areas
3. Areas cannot contain Projects
4. Resources cannot contain active deliverables
5. A file can only exist in ONE location
6. Never create empty folders (JIT creation only)
7. Never duplicate items (use references)
8. Domain and lifecycle are orthogonal dimensions - never collapse them

___

## Transition Triggers (Lifecycle State Machine)

| From | To | Trigger |
|------|----|---------|
| Project | Archive | status == complete AND no open tasks AND deliverables accepted |
| Project | Area | Project becomes long-term ongoing responsibility |
| Resource | Area | Becomes required standard OR referenced >= 5 times |
| Area | Project | Temporary initiative created within area scope (never automatic) |
| Area | Archive | Area ceases to be active responsibility (manual only) |
| Archive | Original | Reactivation needed - restore to original category |
| PARA file | Canonical | Content stabilizes into definition/rule/spec → Promote |

___

## Vault Root Structure

```
/(VAULT ROOT)
  /0_Inbox/         ← Capture buffer (process weekly)
  /1_Projects/      ← PARA: time-bound outcomes
  /2_Areas/         ← PARA: ongoing responsibilities
  /3_Resources/     ← PARA: optional, non-authoritative
  /4_Archive/       ← PARA: inactive items

  /Governance/      ← Canonical: rules, doctrine
  /Domains/         ← Canonical: subject taxonomy
  /Tools/           ← Canonical: reusable tools
  /Libraries/       ← Canonical: reusable building blocks
  /Sessions/        ← Historical: process artifacts
```

PARA and canonical taxonomy are PARALLEL systems at root - not parent/child.
PARA is NOT the vault. It is one folder scheme inside the vault.

___

## Naming Conventions

- **Files:** `{YYYYMMDD}_{descriptor}_{type}.{ext}`
- **Folder slugs:** lowercase, hyphen-separated, no spaces - regex: `^[a-z0-9-]+$`
- **PARA filenames are generic:** index.md, working-notes.md, decisions.md, open-questions.md
- **If you need the domain in the filename → it belongs in canonical, not PARA**

___

## Common Classification Scenarios

### "Where does governance go?"
NEVER in PARA. Always `/Governance/`. Only *changes to governance* create a temporary PARA project.

### "Where do tools/libraries go?"
NEVER in PARA. Always `/Tools/` or `/Libraries/`. "Under construction" is a project STATE, not a storage location - the tool files live canonically even while being built.

### "Where do AI prompts go?"
`/R/prompts/` with prefix `prm.` and tier: sys (infrastructure), lib (reusable), exp (experimental).

### "Where do session summaries go?"
`/Sessions/` with naming: `YYYY-MM-DD_<subject-slug>_session-summary.md`. If content stabilizes into doctrine → promote to `/Governance/` or `/Domains/`.

### "Should I nest PARA inside a project?"
Almost certainly NO. Only if project behaves like a department with independent sub-initiatives. Default: flat within project.

### "What goes in 00_meta / 01_inputs / 02_working / 03_outputs / 04_archive?" (Formal variant only)
This applies to the File System / Formal project subfolder template. See Bible §5.2.1 for full content manifests.

**Quick decision test for any file inside a formal project:**

1. "Does this define the project's identity, state, or governance links?" → `00_meta/`
2. "Was this given to or gathered for the project before work began?" → `01_inputs/`
3. "Is this in-progress, messy, or not yet accepted?" → `02_working/`
4. "Has this been accepted as a final deliverable?" → `03_outputs/`
5. "Is this superseded, abandoned, or no longer active within this project?" → `04_archive/`

**Critical distinctions:**
- `working-notes.md` maps to `02_working/`, NOT `00_meta/` — it is execution material, not project identity
- `04_archive/` is project-level (within an active project). `/4_Archive/` is vault-level (completed projects). They are different.
- A file moves `02_working/` → `03_outputs/` only on **acceptance as deliverable**
- Content that stabilizes into reusable/authoritative knowledge promotes OUT of the project entirely (→ `/Governance/`, `/Domains/`, `/Libraries/`)

### "Is this a Project or an Area?"
Does it have a deadline AND a defined outcome? → Project. Is it an ongoing standard with no end? → Area. If unsure: "Will this end?" YES → Project. NO → Area.

___

## Anti-Patterns (Refuse These)

If the user proposes any of these, flag as anti-pattern with explanation:

1. Using PARA as the entire vault structure (must have canonical taxonomy alongside)
2. Nesting PARA under each domain (dimension collapse)
3. Putting governance, tools, or libraries in PARA
4. Encoding domain taxonomy in PARA filenames
5. Treating PARA as system of record
6. Putting irreplaceable content in PARA
7. Editing files inside Archive
8. Organizing by topic instead of by actionability
9. Creating empty folder structures in advance

___

## Reference

For the complete specification including:
- Full letter definitions with metadata schemas
- Enterprise governance variables and failure modes
- Information flow between PARA categories (all 12 transitions)
- Subfolder templates (Obsidian and filesystem variants)
- **Project subfolder content manifests (§5.2.1) — what goes in meta/inputs/working/outputs/archive**
- **Obsidian-to-Formal variant mapping (§5.3.1)**
- **Construction estimating subfolder mapping (§10.1)**
- Promotion mechanics and project closeout procedures
- Competing system analysis (Johnny Decimal, Zettelkasten, GTD)
- KOS spectrum positioning
- Utility estimator application example
- Frontmatter schemas
- Complete source bibliography

**Read:** `/mnt/skills/user/para-ontology/references/PARA_Ontology_Bible.md`
