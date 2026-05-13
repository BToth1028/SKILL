---
name: jdex-ontology
description: "Deterministic Johnny.Decimal / JDex classification engine — universal JD spec (johnnydecimal.com v6.5.0) layered with Bobby's C:\\dev governance (AGENTS-01-dev.md). Use this skill whenever the user mentions JDex, Johnny.Decimal, JD, AC.ID, SYS.AC.ID, AC.ID+SUB, area/category/ID, standard zeros (AC.00-09), the Librarian, jdlint, jd-doctor, jd-mcp, scaffold.py, seed.py, validate.py, expand-an-area, extend-the-end, multiple systems, partially nested vs fully nested JDex, metadata above-the-line, MOC vs header IDs, system expansion, the 10x10 cap, the no-more-than-10 rule, index-spec, or any question about WHERE a file or folder belongs under C:\\dev. Also trigger for: 'where does this go', 'is this in the right folder', 'should this be 41 or 43', 'is this an area or a category', 'what's the AC.ID for X', 'JDex-conformant?', 'does this need a new ID', 'do I need to expand-an-area', 'should I use a new system', 'graduate this artifact', 'is this PARA or dev', 'reorganize C:\\dev', 'lint my JDex', 'what's in 00.00', 'AC.10 reserved?', 'inbox draining', 'partially nested or fully nested'. When in doubt, trigger — a missed JDex question is worse than a bad trigger. Does NOT apply to PARA classification (use para-ontology) and never operates on paths outside C:\\dev unless explicitly told the system identifier."
---

# JDEX Ontology — Deterministic Classification Engine

> **Two layers, one engine.**
> Layer 1: the universal Johnny.Decimal specification (johnnydecimal.com v6.5.0, JD spec 6.5.0, JDex schema 1.0.0, index-spec working draft, jdlint canonical rules).
> Layer 2: Bobby's `C:\dev` workspace governance (`AGENTS-01-dev.md` §§1–15, locked).
> Layer 2 OVERRIDES Layer 1 wherever they disagree; absent a Layer 2 rule, the universal spec applies. Both layers are closed-world. No improvisation.

---

## 0. Purpose

This skill deterministically answers:

> **"Where does this file / folder / artifact live, and is it where it belongs?"**

Same inputs → identical outputs. No opinion. No "where similar files happen to be." Every classification follows a fixed pipeline and emits a structured `decision_trace` plus pass/fail validation gates.

**Authority source for Bobby's workspace (read first if uncertain):**
`C:\dev\40-49-ai-agents-and-prompts\46-memory-and-bootstrap\46.02-working-memory\AGENTS-01-dev.md`

**Authority source for the universal JD spec:**
[johnnydecimal.com](https://johnnydecimal.com/) (current version: 6.5.0). When this skill references "JD" or "the spec," it means that body of documentation.

---

## 1. The library analogy (the mental model that has to be right)

Credit to Moriarty on the JD Discord, paraphrased on johnnydecimal.com 22.00.0182:

> Your filesystem, notes folder, and physical filing cabinet are the **bookshelves** in a library. Your JDex is the **index card drawer**. The card index describes the shelves and what's on them; the shelves hold the content.

Three invariants follow from this analogy:

1. **The JDex is the system.** A library without a catalogue is not a library — it is a room full of books. A filesystem without a JDex is not a JD system — it is a tree of folders.
2. **Index cards represent the things, they are not the things.** A JDex entry can carry metadata about an ID even when no file with that ID exists yet (a "reserved" entry).
3. **Metadata lives with the entry, not separately.** "Above the line" on the index card. The file content itself ("below the line" / "on the shelves") is separate.

---

## 2. Session contract (locked)

| Field | Value |
|---|---|
| Mission | Classify any artifact against the JDex. Never invent placement. Emit a decision trace + validation gates. |
| Scope | `C:\dev` and any registered sibling system (per `system.multiple_systems` in `jdex.yaml`). PARA → handoff to `para-ontology`. |
| Authority model | Layer-2 (C:\dev AGENTS-01) overrides Layer-1 (universal JD). Within Layer-2: schema → jdex.yaml → filesystem. |
| Input rules | Filename, content hint (optional), user-stated purpose. Ignore convenience, recency, file-mtime, or "where similar files happen to be." |
| Output contract | A `classification:` YAML block (§16). No prose outside the block unless the user asked. |
| Determinism | Same inputs → identical AC.ID, identical path, identical trace. |
| Validation | Every classification passes G1–G10 (§15) before being emitted. |
| Error policy | Missing data → explicit `UNKNOWN`. Ambiguous placement → STOP and ask the user. Never default to a "convenient" location. |
| Anti-drift | Refuse out-of-scope requests in-schema. Follow precedence in §3. |

---

## 3. Authority chain (precedence — high to low)

### Layer 2 — Bobby's C:\dev (overrides Layer 1)

| Level | Source | Path |
|---|---|---|
| 1 | Schema | `00-09-system-administration\00-index\00.03-jdex-schema\jdex.schema.yaml` |
| 2 | JDex (machine-readable) | `00-09-system-administration\00-index\00.00-jdex\jdex.yaml` |
| 3 | Filesystem | `C:\dev\` |
| Aux (edit-time) | Cursor pointer | `.cursor\rules\workspace-rules.mdc` (`alwaysApply: true`) |
| Derived | Human-readable view | `00-09-system-administration\00-index\00.04-jdex-markdown\JDex.md` |
| Derived | Index README | `00-09-system-administration\00-index\00.01-readme\README.md` |
| Append-only | Changelog | `00-09-system-administration\00-index\00.02-changelog\CHANGELOG.md` |
| Norm spec | Folder README envelope | `00-09-system-administration\01-meta-and-policy\01.05-folder-envelope-spec\` |

If two disagree: higher level wins. Filesystem is corrected to match JDex; JDex is corrected to match schema.

### Layer 1 — Universal JD spec

| Source | Role |
|---|---|
| johnnydecimal.com 11.x | Core concepts (areas, categories, IDs, philosophy, JDex, files, notes, the Librarian) |
| 12.x | Advanced (email, alternative JDex methods, standard zeros, command line, AC.ID notation) |
| 13.x | System expansion (multiple systems, expand-an-area, extend-the-end, guidelines) |
| 14.x | Build, JD University, Workshop, task & project management |
| 15.x | Patterns (creative, Life Admin System, Small Business System) |
| `johnnydecimal/index-spec` | Formal spec (RFC 2119, TypeScript-typed) |
| `SiriusStarr/jdlint` | Canonical validation rule taxonomy |
| `johnnydecimal/awesome-johnnydecimal` | Community tooling index |

---

## 4. Hard structural invariants (never violate)

**Universal (from JD spec + index-spec):**

1. **Three levels, full stop.** Area → Category → ID. No sub-IDs inside an ID folder beyond owner discretion. JD-numbered subfolders inside an ID are forbidden (use Expand-an-area instead).
2. **10×10×100.** Max 10 areas; max 10 categories per area; max 100 IDs per category.
3. **AC.ID strict format:** `^\d{2}\.\d{2}$`.
4. **Area format:** `^([0-9])0-\1 9$` (e.g. `00-09`, `10-19`, … both digits equal).
5. **Category format:** `^[0-9]{2}$`; first digit of category MUST match the area's decade.
6. **ID format:** `^\d{2}\.\d{2}$`; category component MUST match parent category.
7. **Uniqueness:** every area, category, and ID is unique within the system.
8. **No files at area or category root.** Files live inside an ID folder only.
9. **`AC.10` is reserved/skipped** by long-standing convention to avoid `10` confusion. Real IDs start at `AC.11`. (Optional under the "standard zeros v2" symmetric variant; in Bobby's C:\dev this convention is followed.)
10. **Metadata attaches only to IDs.** To describe an area, attach metadata to ID `A0.00`. To describe a category, attach metadata to `AC.00`.
11. **JDex parity.** Every ID-folder on disk ↔ JDex entry. Names match exactly. Drift is a violation.

**Bobby C:\dev additions (locked, AGENTS-01 §2):**

12. **Bidirectional parity** enforced via `jd-doctor` (MISSING / ORPHAN / MALFORMED taxonomy — see §13).
13. **No unregistered folders** under `C:\dev`. Active session bootstrap is locked.
14. **Closed-world schema.** `additionalProperties: false` at every schema level. Schema-conformant entry is created BEFORE folder.
15. **Standard-zero.** Every category reserves `XX.00` for the index file. (Aligns with JD universal §11.05.)
16. **Dev-focused scope.** Non-software-development material does NOT belong in `C:\dev`. Personal/work material lives in sibling JD systems declared under `system.multiple_systems`.
17. **Governance depth limit.** JDex parity stops at the ID level. Substructure inside an ID is owner's domain — gated by `precedents.yaml` (§14).
18. **Folder README envelope.** Every JDex folder at area, category, and ID levels MUST have a PDKOS-conformant `<jdex-prefix>-README.yaml`. Spec: `01.05-folder-envelope-spec`.
19. **JDex overrides external tool conventions** for any work under `C:\dev`.

---

## 5. Closed-world enums

| Field | Allowed values | Source |
|---|---|---|
| `type` | `folder` \| `file` \| `repo` \| `crate` \| `mount` \| `reserved` | Bobby schema |
| `status` | `active` \| `planning` \| `dormant` \| `archived` \| `retired` \| `UNKNOWN` | Bobby schema |
| `lifecycle` | `permanent` \| `long-lived` \| `active` \| `cyclical` \| `frozen` \| `locked` \| `UNKNOWN` | Bobby schema |
| Reserved metadata keys | `description` (GFM), `relatesTo` (array of AC.ID), `url` (array of RFC 3986 URIs) | index-spec |
| User metadata keys | SHOULD be camelCase | index-spec |
| AC.ID format | `^\d{2}\.\d{2}$` | JD universal |
| SYS prefix | `^[A-Z][0-9]{2}$` (A00 … Z99 = 2,600 system identifiers) | JD 13.11 |
| AC.ID+SUB | `^\d{2}\.\d{2}\+[A-Za-z0-9]+$` | JD 13.31 |
| Tag format | `^[a-z][a-z0-9-]*$`, unique within entry | Bobby schema |
| Title length | 1–255 printable Unicode chars | index-spec |

Missing data → explicit `UNKNOWN`. Never empty string. Never invented values.

---

## 6. Naming (locked)

**Universal:** the displayed JDex name is the canonical name. `jdlint` strips trailing `area management`, `category management`, `index`, and `.md` for canonicalization — three forms (`10.00 Life Admin`, `10.00 Life Admin.md`, `10.00 Life Admin Area Management Index`) are equivalent.

**Bobby C:\dev (locked, AGENTS-01 §3):**

- **Folder pattern:** `<ac_id>-<kebab-name>` — `00-09-system-administration`, `02.06-jd-doctor`, `43.01-custom-skills`.
- **Transformation rule:** lowercase; drop parentheses; `&` → `and`; spaces/underscores → hyphen; collapse repeated hyphens; trim.
- **Filenames inside JDex folders:** kebab-case.
- **Single exception:** `system.name` in `jdex.yaml` stays as authored (it is a label, not a path).
- **Forbidden in folder names:** spaces, capital letters, `<>:"/\\|?*` (the last set is sanitized to `-`).

---

## 7. AC.ID notation glossary (JD 12.05)

`AC.ID` is *variable* notation — A, C, and ID are placeholders that resolve to concrete digits.

| Notation | Means |
|---|---|
| `AC.ID` | Any ID in the system |
| `1C.ID` | Any ID in area `10-19` |
| `11.ID` | Any ID in category `11` |
| `AC.11` | The `.11` ID in any category |
| `SYS.AC.ID` | Any ID across multiple-systems mode (e.g. `H01.11.11`, `W01.11.11`) |
| `AC.ID+SUB` | Extended-end variant (e.g. `11.24+JEM`) |

Notation extends in two scenarios only: `SYS.AC.ID` (multiple systems, §11) and `AC.ID+SUB` (extend-the-end, §11). They can compose: `SYS.AC.ID+SUB` is valid; expand-an-area + extend-the-end is NOT valid (§11).

---

## 8. Standard zeros (JD 12.03 + community v2)

### Classic standard zeros (default, JD 12.03)

Every category MAY reserve these IDs by convention. Bobby's `C:\dev` enforces `AC.00` for category index.

| ID | Purpose | Notes |
|---|---|---|
| `AC.00` | **Index** for the category | Required in C:\dev. Auto-generated from JDex. |
| `AC.01` | **Inbox** — unsorted incoming | SHOULD be drained; jdlint flags `NONEMPTY_INBOX`. |
| `AC.02` | **Work-in-progress** | Renamed from "Notes" — Johnny: "Notes felt like a place that notes went to die." |
| `AC.03` | **To-dos / checklists** | |
| `AC.04` | **Resources** | Reference material relevant to the category |
| `AC.05` | **Templates** | |
| `AC.08` | **Someday / maybe** | Backlog with no activation date |
| `AC.09` | **Archive within the category** | Distinct from system-level area `80-89` |
| `AC.10` | **RESERVED / skipped** | Convention to avoid confusion with `10`. Real IDs start at `AC.11`. |

### Standard zeros v2 (interrato proposal, Johnny-endorsed — forum 1558)

Moves area-management zeros into the system area `00-09`. `01` becomes management for area `10-19`, `02` for `20-29`, etc. Frees ~891 extra usable IDs (12.36% more space). Symmetric variant lets real IDs start at `AC.10`.

**Bobby C:\dev:** classic convention is in use. Track v2 as a possible future migration but do NOT switch silently.

---

## 9. The JDex data-storage continuum (JD 22.00.0182)

Two orthogonal axes that determine how a JD system stores its content:

```
                     JDex stored in filesystem
                              │
       Obsidian fully nested  │  Obsidian partially nested
                              │
─── Data IN JDex ─────────────┼────────────── Data EXTERNAL ───
                              │
       Bear / Notion          │  Excel / Google Sheets / Airtable
                              │
                     JDex stored elsewhere
```

| Axis | Options |
|---|---|
| **Where does the data live?** | (a) Below-the-line inside the JDex entry — single-file simplicity. (b) Externally in the filesystem — JDex entry references it via `Data:` metadata key. (c) Hybrid — most systems live on this continuum. |
| **Where does the JDex live?** | (a) Individual files in the filesystem (Obsidian-style — `.md` per ID). (b) Single text file / spreadsheet / database (Bear, Notion, Airtable, SQLite). |

### Nested vs flat patterns (Obsidian downloads from JDHQ)

| Pattern | Description | When |
|---|---|---|
| **Partially nested** | `.md` JDex entries live at `00.00/`; filesystem `10-19/11/11.12/…` for real files. Clean separation. **Default — recommended.** |
| **Fully nested** | Each ID is a folder; its `.md` JDex entry lives *inside* the folder beside the data files. **Universal consensus: this pattern doesn't work** (Obsidian slowdown, can't selectively sync — Johnny himself tried and abandoned). |
| **Flat** | `.md` JDex entries at `00.00/` with no area/category subtree. Some prefer this. |

**Bobby C:\dev:** uses neither — Bobby's JDex is `jdex.yaml` (YAML database, schema-validated). Folder content lives at each AC.ID's canonical folder. This is the SQLite/database row of the continuum.

### Metadata above-the-line / Data below-the-line discipline

- **Metadata:** structured key/value pairs in the JDex entry, "above the line." Standardize keys (`Location:`, `Last updated:`, `Data:`). If the user uses `Where is it?` once and `Location` elsewhere, querying breaks.
- **Data:** unstructured content "below the line" OR external files referenced from above-the-line `Data:`.
- A spreadsheet column IS a metadata key. Adding `Where is it?` as a new column when `Location` already exists is the same mistake.

---

## 10. AC.ID notation hierarchy and reserved 00 conventions

`00.00` is **the system's own JDex entry** — recursive but trivial. It declares the system itself.

`00.AC` IDs (system-administration area) hold infrastructure that governs the rest of the system:
- `00.00` — system index
- `00.01` — README / orientation
- `00.02` — CHANGELOG (append-only)
- `00.03` — schema (Bobby-specific)
- `00.04` — human-readable JDex view (Bobby-specific)

**Universal rule:** the area `00-09` is reserved for system administration. Do not assign work content there.

---

## 11. System expansion — when to use what (JD 13.x)

Three orthogonal expansion mechanisms. Choose the smallest that fits.

| Mechanism | When to use | What it gains | Allowed combinations |
|---|---|---|---|
| **Multiple systems** (JD 13.11) | Two domains with nothing in common (work vs personal). | Up to 2,600 separate systems via `[A-Z][0-9][0-9]` prefix. | ✓ with Expand-an-area. ✓ with Extend-the-end. |
| **Expand-an-area** (JD 13.21) | One area legitimately needs >10 categories or >3 levels (freelance jobs, university semesters, creative portfolios). | Abandons constraint inside ONE area only. The rest of the system stays standard. | ✓ with Multiple systems. ✗ with Extend-the-end (incompatible — the area is no longer standard). |
| **Extend-the-end** (JD 13.31) | One ID legitimately needs sub-instances (multiple kids' dental records, repeating events). | `AC.ID+SUB` notation, e.g. `11.24+JEM`. | ✓ with Multiple systems. ✗ with Expand-an-area. |

**Anti-pattern:** if you find yourself extending-the-end frequently, your system design is wrong — split to multiple systems or expand-an-area instead.

### Expand-an-area principles (when used)

When expanding, all expanded IDs MUST still start with the area's first digit. Permitted tactics, in priority order:
1. Use **natural hierarchies** (client → product → job).
2. Use the **alphabet** for long sortable lists (organizations, courses).
3. Use the **date** in ISO 8601 `yyyy-mm-dd` for chronological data.
4. **Stop using numbers** where alphabet or date is better.
5. **Look for patterns** — repeated structures become templates numbered in tens (10, 20, 30) for spacing.
6. **Use existing codes** (university course codes, agency job numbers) rather than inventing new ones.
7. **Invent your own scheme** only as a last resort, and document it in the area's `A0.00` entry.

**Overarching principle:** consistency is critical. Document the scheme.

### `AC.ID+SUB` vs numeric extension

Community convention (forum 2637):
- `+SUB` = subordinate parts of one thing (dies with parent)
- `.91 / .92 / …` = new distinct things at the same level

---

## 12. The Librarian role (JD 11.08)

When this skill is active, Claude **takes the Librarian role** for the affected system. Responsibilities (universal, locked):

1. **Own the index.** Keep the JDex up to date. Every change to the filesystem produces a JDex change.
2. **Annotate.** Add description, tags, and process notes that document "what goes where, and why."
3. **Monitor and enforce.** Surface drift (MISSING / ORPHAN / MALFORMED). Help when rules aren't being followed.
4. **Arbitrate.** Final word on category boundaries when categories overlap or compete.
5. **Drain the inbox** (`AC.01`). Inboxes are staging; they MUST be processed.
6. **Maintain hygiene.** Detect duplicates, name drift, broken `relatesTo`, orphaned ID folders.
7. **Proposal-first mandate** (community pattern from `johnny-decimal-zettelkasten`, recommended for AI agents): **analyze and suggest, do not mutate without approval.** Every move/rename/delete is a *proposal* until the user explicitly approves it — even when within authority.

For Bobby's C:\dev, the Librarian role is governed by AGENTS-01 §5 (precedent gate), §5A (destructive-op gate), and §5B (auto-commit and push).

---

## 13. Placement gate layers (Bobby C:\dev) + universal validators

| Layer | Gate | Source | Purpose | Status |
|---|---|---|---|---|
| L1 | `jd-mcp` (live, six tools) | `02.03-jd-mcp\jd_mcp.py` | Edit-time prevention | active |
| L1.5 | git pre-commit hook | `02.04-git-pre-commit-hook\` | Commit-time guard | planning |
| L2 | `validate.py` | `02.01-jd-validate\validate.py` | Schema validation (read-only) | active |
| L3 | `jd-doctor` | `02.06-jd-doctor\jd_doctor.py` | Filesystem-vs-JDex parity (read-only) | active |
| L4 (univ) | `jdlint` | community tool | Universal JD lint rules | available |

### `jd-doctor` taxonomy (Bobby canonical vocabulary)

- **MISSING** — in JDex but not on disk
- **ORPHAN** — on disk but not in JDex
- **MALFORMED** — folder name doesn't match the AC pattern at its level

### `jdlint` rule taxonomy (universal, treat as additional validators)

- **File-tree:** `INVALID_AREA_NAME`, `INVALID_CATEGORY_NAME`, `INVALID_ID_NAME`, `CATEGORY_IN_WRONG_AREA`, `ID_IN_WRONG_CATEGORY`, `DUPLICATE_AREA`/`CATEGORY`/`ID`, `FILE_OUTSIDE_ID` (file at area/category root), `NONEMPTY_INBOX` (`AC.01` not drained).
- **JDex sync:** `*_NOT_IN_JDEX`, `*_DIFFERENT_FROM_JDEX` (name drift), `JDEX_FILE_OUTSIDE_CATEGORY`.
- **Canonicalization strips:** trailing ` area management`, ` category management`, ` index`, `.md`.

### jd-mcp tool surface (Bobby's live L1)

| Tool | Purpose |
|---|---|
| `jd_get_system()` | System metadata + counts (authoritative ID count) |
| `jd_propose(filename, hint)` | Ranked AC.ID candidates with reasons (**the L1 gate**) |
| `jd_resolve(ac_id)` | Canonical folder + metadata |
| `jd_validate_path(path)` | Conformance check |
| `jd_search(query)` | Free-text lookup |
| `jd_list_area(area)` | Area or category listing |

---

## 14. Classification pipeline (deterministic — execute in order; STOP at first match or first failure)

### STEP 0 — In-scope check

Ask sequentially:
- "Is the proposed path outside `C:\dev`?" → out of scope. If PARA, handoff to `para-ontology`. STOP.
- "Is this a new governance / rule file?" → AGENTS-01 §10 forbids new rule files anywhere under `C:\dev` or `C:\PARA`. Refuse and route to `AGENTS-01-dev.md` / `AGENTS-02-para.md`.
- "Is this a `SKILL.md` / `COMMAND.md` for a Cursor capability?" → canonical home is `43.01-custom-skills\<name>\` / `43.02-commands\<name>\` (precedent `cursor-agent-skill-bundle`). Use that. STOP.
- "Is this the workspace-root auto-load shim (`C:\dev\AGENTS.md`) or a dot-prefixed tool folder?" → exempt per §17. No new placement decision required.

### STEP 1 — Identify the system

Run `jd_get_system()`. If the artifact belongs to a sibling system listed under `system.multiple_systems`, prefix all subsequent references with the appropriate `SYS` (e.g. `H01`, `W01`). Bobby's primary system is **the C:\dev system** (no SYS prefix in addressing within-system).

### STEP 2 — Resolve the AC.ID via jd-mcp

1. `jd_propose(filename, content_hint)` → ranked candidates with reasons.
2. If top score ≥ 10 → take it.
3. If top two scores tie within 1 point → STOP and ask the user.
4. `jd_resolve(top_ac_id)` → confirm canonical folder + metadata.
5. `jd_validate_path(<proposed full path>)` → conformance check (see §13 known drift caveats in AGENTS-01).

Fallback if `jd-mcp` is unavailable: read `jdex.yaml` directly.

### STEP 3 — Substructure / precedent gate (AGENTS-01 §5 step 5)

After the AC.ID resolves, **before placing the file**:

1. Read `<resolved-id-folder>\precedents.yaml`.
2. **Pattern matches?** Follow it exactly. No improvisation. Continue.
3. **No matching pattern, OR `precedents.yaml` doesn't exist?** **STOP** and present to the user:
   - The file to place
   - The resolved AC.ID and folder
   - A proposed precedent entry (`pattern_id`, `description`, `path_rule`, `extensions_allowed`, `first_established`, `examples`)
4. If `precedents.yaml` defines a `novel_content_resolution_protocol` → execute it first.
5. On approval: write the precedent, append CHANGELOG, then place the file.

**Forbidden:** silently improvising a placement and writing a precedent for it. First-of-class placements require explicit user approval; subsequent placements of the same class are automatic.

### STEP 4 — System-expansion check

Ask: does this placement *need* multiple-systems, expand-an-area, or extend-the-end? Use §11 to decide. If the answer is yes:
- Multiple systems → user must declare the SYS identifier and register it.
- Expand-an-area → STOP. This is a structural change requiring user authorship.
- Extend-the-end → propose `AC.ID+SUB`; check that the AC is not in an expanded area.

Default answer: **no** — the existing AC.ID accommodates the file.

### STEP 5 — Cross-area lifecycle check (Bobby AGENTS-01 §10)

- **Graduation:** `47 outputs-and-artifacts` and `64 llm-experiments` are staging. Keepers move to permanent homes (typically 41–46 for AI work).
- **Archive integrity:** `80-89 archive` takes whole project folders **intact** — never splinter. Never split across IDs. Never split across PARA and JDex.
- **Reserved:** `90-99` is locked; JD 13.31 "Extend the end" only.
- **Permanent:** `00-09` is permanent. Touch with care.
- **Area-scoped rules:** consult each area's `description` field. Do not over-generalize.

### STEP 6 — External path reference gate (AGENTS-01 §14)

Scan content for filesystem paths outside `C:\dev`:
- `C:\code`, `C:\PARA`, `C:\staging`, `C:\vault`, `C:\projects`, `C:\work`
- `%USERPROFILE%`, `%APPDATA%`, `%LOCALAPPDATA%` expansions outside `C:\dev`
- Relative paths (`../`, `_staging/`) resolving outside `C:\dev`
- UNC paths unless explicitly approved

**Allowed:** `https://` / `http://` URLs, `C:\dev` paths, profile paths (`C:\Users\rtoth\.cursor\`) where intentional and documented.

On violation: STOP, report exact line(s), remediate (update / remove / annotate-and-quarantine with user approval).

### STEP 7 — Destructive-op gate (AGENTS-01 §5A)

If the placement involves anything destructive — overwrite, move that removes the original, delete, retarget a symlink, force/recursive flags on existing paths — **STOP** and request explicit user approval for the exact path(s) and exact operation(s). Approval is not implied by a broad task request. Prefer additive repair.

### STEP 8 — Auto-commit and push (AGENTS-01 §5B)

After write, if §5 and §6 cleared:
1. `git status` — identify only paths from this task.
2. Stage only those paths.
3. Commit with a concise message.
4. Push to the tracked remote branch.
5. On failure, report the exact error and leave the work staged/committed as far as the failed command reached.

Skip ONLY if: user explicitly opted out, or a tool/auth/test failure blocks completion. Never silently include unrelated dirty-tree changes, secrets, IDE state, or transcript dumps.

---

## 15. Validation gates (G1–G10, must all pass before emitting)

| Gate | Check | On fail |
|---|---|---|
| G1 | AC.ID matches `^\d{2}\.\d{2}$` | `INVALID_ID_NAME` — structured error |
| G2 | Area matches `^[0-9]0-[0-9]9$` (both digits equal) | `INVALID_AREA_NAME` |
| G3 | Category matches `^\d{2}$` and starts with parent-area decade | `CATEGORY_IN_WRONG_AREA` |
| G4 | ID's category-prefix matches parent category | `ID_IN_WRONG_CATEGORY` |
| G5 | AC.ID exists in jdex.yaml | `*_NOT_IN_JDEX` |
| G6 | Folder name matches `<ac_id>-<kebab-name>` (Bobby §6) | `MALFORMED` |
| G7 | Status ∈ enum (§5); not `archived`/`retired` for active placement | structured error |
| G8 | Precedent matched OR user-approved new precedent recorded | structured error |
| G9 | No external-path violations (§Step 6) | STOP, report, remediate |
| G10 | No destructive op without per-path approval (§Step 7) | STOP, request approval |

**Soft-warn gates (do not block, but flag):**

- W1: `AC.01` inbox non-empty (`NONEMPTY_INBOX`).
- W2: `AC.10` assigned (universally reserved).
- W3: File would land at area or category root (move to `AC.00` or appropriate ID).
- W4: Title drift between JDex entry name and folder name post-canonicalization.
- W5: `relatesTo` reference points at a non-existent AC.ID.
- W6: Auto-generated file is about to be hand-edited (`00.01 README.md`, `00.04 JDex.md`).

---

## 16. `jd_propose` deterministic scoring (Bobby C:\dev)

| Score | Trigger |
|---|---|
| **+15** | Filename in ID's `contains` whitelist (always wins; explicit pinning) |
| +10 | Extension in `contains` whitelist |
| +5 | Keyword match in tags |
| +4 | Keyword in ID name |
| +3 | Keyword in description |
| +2 | Keyword in category name |
| +1 | Keyword in area name |
| −1 | Status `planning` |
| −3 | Status `archived` or `retired` |

`contains` is enforced (not advisory). Empty list = unrestricted; `*` = unrestricted; non-empty = whitelist. Filename match wins over extension, which wins over keyword.

---

## 17. Output contract

```yaml
classification:
  system: <C:\dev | SYS prefix>
  proposed_path: <absolute path>
  ac_id: <NN.NN | UNKNOWN>
  area: <area name from jdex.yaml>
  category: <category name from jdex.yaml>
  id_name: <id name from jdex.yaml>
  destination_folder: <C:\dev\AA-BB-<area>\NN-<category>\NN.NN-<id>\>
  expansion_mode: standard | multiple-systems | expand-an-area | extend-the-end
  precedent_status: matched | new-pending-approval | not-applicable
  metadata_proposed:
    description: <…>
    relatesTo: [<AC.ID>, …]
    tags: [<…>]
  decision_trace:
    - step: 1
      action: identify-system
      result: <system identity>
    - step: 2
      tool: jd_propose
      input: { filename: <…>, hint: <…> }
      top_candidate: { ac_id: <…>, score: <…>, reasons: [<…>] }
    - step: 3
      tool: jd_resolve
      ac_id: <…>
      folder: <…>
    - step: 4
      tool: jd_validate_path
      path: <…>
      result: conformant | non-conformant
    - step: 5
      precedent_check: matched | none | new-proposed
      pattern_id: <…>
    - step: 6
      expansion_needed: yes | no
      reason: <…>
    - step: 7
      lifecycle: graduation | archive | reserved | permanent | active
    - step: 8
      external_paths: clean | flagged
    - step: 9
      destructive: none | requires-approval
  validation_gates:
    G1_ac_id_format: pass | fail
    G2_area_format: pass | fail
    G3_category_in_area: pass | fail
    G4_id_in_category: pass | fail
    G5_jdex_registered: pass | fail
    G6_folder_naming: pass | fail
    G7_status_enum: pass | fail
    G8_precedent: pass | fail
    G9_external_paths: pass | fail
    G10_destructive_ops: pass | fail
  soft_warnings: [<W1, W2, … with descriptions>]
  next_actions:
    - <e.g., "Append CHANGELOG entry under 2026-MM-DD">
    - <e.g., "git add / commit / push per AGENTS-01 §5B">
```

**Structured error:**

```yaml
classification: FAILED
error_code: <PROPOSE_NO_MATCH | AC_ID_NOT_IN_JDEX | PRECEDENT_REQUIRES_APPROVAL | EXTERNAL_PATH_VIOLATION | DESTRUCTIVE_OP_UNAPPROVED | SCHEMA_VIOLATION | INVALID_ID_NAME | CATEGORY_IN_WRONG_AREA | ID_IN_WRONG_CATEGORY | DUPLICATE_AREA | DUPLICATE_CATEGORY | DUPLICATE_ID | FILE_OUTSIDE_ID | NONEMPTY_INBOX | EXPANSION_REQUIRED>
reason: <one line>
blocking_gate: <G1 | G2 | … | G10>
action_required: <what the user must clarify or approve>
```

---

## 18. Exemptions from parity

`jd-doctor` and `jdlint` ignore:
- **Dot-prefixed directories** at any level (`.cursor`, `.git`, `.specstory`, `.vscode`)
- **Windows system folders** (`$RECYCLE.BIN`, `System Volume Information`, `Thumbs.db`)
- **Anything inside an ID folder** (substructure is owner's domain, gated by precedents)
- **Files at the workspace root** (root-level files are not iterated)

**Documented root-level exception:** `C:\dev\AGENTS.md` (symlink → `46.02-working-memory\AGENTS.md`).

**Tool pointer files (exempt):**
- `C:\dev\.cursor\rules\workspace-rules.mdc`
- `C:\dev\.claude\rules\CLAUDE.md` (symlink → `46.02-working-memory\CLAUDE.md`)

---

## 19. Universal NO-NEW-RULE-FILES constraint (Bobby AGENTS-01 §10)

No new file anywhere under `C:\dev` or `C:\PARA` whose purpose is to define / restate / extend / enforce workspace governance rules. No new `.mdc` rules. No new `.md` under `.claude\rules\` or `.cursor\rules\` beyond existing thin pointers. No new `RULES.md` / `GOVERNANCE.md` / `POLICY.md`. No substantive rule content in `workspace-rules.mdc` or `CLAUDE.md`.

If a rule is needed → add it to `AGENTS-01-dev.md` or `AGENTS-02-para.md` and follow the index-split procedure in the governance decision record.

---

## 20. Area reference table — Bobby C:\dev

| Area | Name | Typical content | Lifecycle |
|---|---|---|---|
| `00-09` | system-administration | JDex, schema, validators, scaffold, doctor, seed, MCP, bootstrap, registries, backup/sync | permanent |
| `10-19` | active-code-projects | One ID per repo; the ID folder IS the working tree | active |
| `20-29` | libraries-and-configuration | Personal libs, snippets, dotfiles, editor configs, peripherals | long-lived |
| `30-39` | data-and-databases | SQL Server / SSMS, datasets, notebooks, ML models, reference data | active |
| `40-49` | ai-agents-and-prompts | Prompts, agent sessions, rules/skills/subagents, MCP servers, RO-crates, memory/bootstrap, outputs | active |
| `50-59` | infrastructure-and-devops | Terraform, Bicep, Kubernetes, CI/CD, containers, scripts | long-lived |
| `60-69` | sandbox-and-experiments | Algorithm practice, language tryouts, quick spikes, LLM experiments | cyclical |
| `70-79` | documentation-and-learning | Books/notes, courses, tutorials, cheatsheets, reference clips | long-lived |
| `80-89` | archive | Year-partitioned frozen completed work — **whole project folders intact** | frozen |
| `90-99` | reserved | Locked. JD 13.31 "Extend the end" only | locked |

This table is intuition, not authority. **Always run `jd_propose` for the actual placement.** Confirm against `jd_get_system()` for ID counts.

---

## 21. Adding a new ID (AGENTS-01 §9 procedure)

1. Choose AC.ID; verify uniqueness via `jd_resolve(ac_id)` or grep of `jdex.yaml`.
2. Add schema-conformant entry to `jdex.yaml` (required: `name`, `type`, `status`).
3. Run `validate.py` → schema conformance.
4. Run `scaffold.py --apply` → create the folder.
5. Append CHANGELOG entry under today's heading:
   ```
   ## YYYY-MM-DD

   - {action description}
   ```
6. Run `jd_doctor.py` → confirm parity (no MISSING / ORPHAN / MALFORMED).
7. Optional: `seed.py --apply` → regenerate README and JDex.md.

The written procedure's right home: `01.02-lifecycle-rules\` (currently empty per AGENTS-01 §13).

---

## 22. Maintenance loop

| Step | Tool | Default | `--apply` effect |
|---|---|---|---|
| 1 | `02.01-jd-validate\validate.py` | read-only | n/a |
| 2 | `02.05-scaffold\scaffold.py` | dry-run | Materialize folder tree |
| 3 | `02.06-jd-doctor\jd_doctor.py` | read-only | n/a |
| 4 | `02.07-seed\seed.py` | dry-run | Re-seed canonical files + regenerate README + JDex.md |
| 5 (optional, universal) | `jdlint` | read-only | n/a |
| 6 (optional, universal) | `jd-folders-tool` | dry-run | Normalize folder naming |

**Auto-generated (NEVER hand-edit):** `00.01 README.md`, `00.04 JDex.md`. Clobbered every `seed.py --apply`.

---

## 23. Common JDEX scenarios (deterministic shortcuts)

| Scenario | Answer |
|---|---|
| "Where does this SKILL.md go?" | `43.01-custom-skills\<skill-kebab-name>\SKILL.md` — precedent `cursor-agent-skill-bundle`. |
| "Where does this slash-command go?" | `43.02-commands\<command-kebab-name>\COMMAND.md`. |
| "Where does a new prompt go?" | `41-prompts\…` — run `jd_propose` to choose the category. |
| "Where does a bootstrap YAML go?" | `46.01-bootstrap-yamls\` — filename `<system-name>_<YYMMDD>-<HHMM>.yaml`. |
| "Where does working memory go?" | `46.02-working-memory\` (AGENTS.md, AGENTS-01-dev.md, AGENTS-02-para.md, CLAUDE.md). |
| "Where do MCP server configs go?" | `44-mcp-servers\…`. |
| "Where does a SQL Server saved query go?" | `30-39 data-and-databases` — run `jd_propose`. |
| "Where do session output artifacts go?" | `47-outputs-and-artifacts\` — staging; graduate keepers to permanent homes. |
| "Is governance content allowed here?" | NO if it's a new rule file (§19). Edit `AGENTS-01-dev.md`. |
| "Is this an Area or a Category?" | Areas are `NN-NN` ranges (10 of them). Categories are `NN` (max 10/area). IDs are `NN.NN` (max 100/category). |
| "Does this need a new ID?" | Only if no existing ID's `contains`/scope reasonably covers it AND a precedent doesn't already route it inside an existing ID's substructure. Default: extend substructure under an existing ID. |
| "Is the path conformant?" | `jd_validate_path(path)` — kebab name, AC prefix, registered in JDex. |
| "When should I split to a new system?" | When you have two domains with nothing in common, or you have run out of room in the primary system and compression doesn't work. Use `SYS.AC.ID` with `[A-Z][0-9][0-9]` prefix. |
| "When should I expand-an-area?" | Only when ONE area legitimately needs >10 categories or natural hierarchies deeper than three levels. Other areas stay standard. |
| "When should I extend-the-end?" | Only when ONE ID needs sub-instances (multiple kids, repeating events). Format: `AC.ID+SUB`. |
| "Two valid AC.IDs scored equally — which?" | STOP. Ask the user. Never coin-flip. |
| "Inbox `AC.01` has 47 files." | Soft-warn (W1) and propose draining each to a real ID. |
| "Multi-home: file fits two IDs." | Pick one canonical home; add `relatesTo: [<other AC.ID>]` metadata. Never duplicate. |
| "JDex within a JDex?" | The `00.00` entry IS the system's own JDex entry — recursive but trivial. Not duplication; not infinite recursion. |
| "Should I use header-IDs (`AC.41-AC.49`) or MOCs?" | Header-IDs for stable addressable structure (max 9 children); MOCs (frontmatter `parent:`/`children:`) for flexible composition. |
| "PARA project — does it map to a JD area?" | NO. A PARA project maps roughly to a single JD ID, not an area. |

---

## 24. Anti-patterns (refuse these — universal + Bobby)

**Universal:**

1. **Files at the area or category root.** Files MUST live inside an ID folder. (`FILE_OUTSIDE_ID`.)
2. **JD-numbered subfolders inside an ID.** Use Expand-an-area instead.
3. **Assigning `AC.10`.** Reserved by convention.
4. **Inbox `AC.01` accumulating.** Drain it.
5. **Inconsistent metadata keys.** `Where is it?` vs `Location:` breaks querying.
6. **Fully-nested Obsidian pattern.** Universal consensus: doesn't work.
7. **PARA project → JD area mapping.** A project is an ID, not an area.
8. **Extending-the-end frequently.** Symptom of bad system design — split to multiple systems or expand-an-area.
9. **Combining expand-an-area with extend-the-end.** Forbidden.
10. **Hex / multi-letter SYS prefixes.** SYS is strict `[A-Z][0-9][0-9]`.
11. **Duplicate IDs.** Globally unique.
12. **Splintering an archived project across multiple `80-89` IDs.** Archive integrity: whole folders intact.

**Bobby-specific (AGENTS-01):**

13. **Folder-first creation.** Schema entry first.
14. **Saving to a "convenient temp location."** Forbidden.
15. **Splintering a project across PARA and JDex.**
16. **Creating new `RULES.md` / `GOVERNANCE.md` / `POLICY.md`.** Forbidden.
17. **Authoring SKILL.md / COMMAND.md outside `43.01-custom-skills\<name>\` / `43.02-commands\<name>\`.**
18. **"Second source of truth" under `%USERPROFILE%\.cursor\skills-cursor\`.** Junctions/shortcuts only.
19. **Hand-editing `00.01 README.md` or `00.04 JDex.md`.** Auto-generated.
20. **Improvising a placement and silently writing a precedent.** First-of-class requires user approval.
21. **External path references** to `C:\code\…`, `C:\PARA\…`, `_staging\…` inside files written into `C:\dev`.
22. **Force/recursive destructive operations** without explicit per-path approval.
23. **Skipping auto-commit/push** after agent-made changes (unless user opted out).
24. **Treating one area's `description` as a general rule** for other areas.
25. **Saving non-software-development material** under `C:\dev`. Belongs in sibling systems.

---

## 25. PARA boundary + hybrid considerations

**Official JD stance:** do NOT combine PARA and JD — "fundamentally different structures" (forum 1005). PARA moves things between Projects / Areas / Resources / Archives based on current state. JD assigns static permanent IDs based on identity.

**Bobby's stance (AGENTS-02-para.md):** `C:\dev` is canon (JDex-governed). `C:\PARA` is execution (PARA-method-governed). They are siblings, not parent/child. Cross-references in prose are fine; functional path references across the boundary are forbidden.

**Hybrid mappings (Luca-Decimal, etc.) are forks, not JD.** Do not invent hybrid schemes inside `C:\dev`.

**The triage question:** "Will another project, agent, or session need to depend on or find this?" Yes → `C:\dev`. Only relevant to this in-flight project → `C:\PARA`.

---

## 26. Multi-home references

When a file legitimately relates to multiple AC.IDs:

1. Pick the canonical home using the obligation test: "What is this file for, primarily?" — that ID gets the file.
2. Add `relatesTo: [<other AC.ID>, …]` metadata to the JDex entry (index-spec reserved key).
3. NEVER duplicate the file across IDs. Use one-way refs only.
4. If multi-homing happens repeatedly between the same two IDs, the IDs may be miscarved — propose a category boundary review.

---

## 27. MOC (Map of Content) vs header IDs

| Approach | When | Trade-offs |
|---|---|---|
| **Header IDs** (e.g. `AC.41` parents `AC.42`–`AC.49` as children) | Structure is stable and addressable; max 9 children. | Rigid; fixed in number-space. Stable URLs. |
| **MOC pattern** (frontmatter `parent:` / `children:` on JDex entries) | Structure is flexible or many-children. | Requires link discipline. No artificial child cap. |

**Default rule of thumb (forum 2921):** IDs for stable addresses, MOCs for flexible composition.

---

## 28. When to escalate (STOP and ask the user)

Always escalate — never improvise — when:
- `jd_propose` returns no candidate with score ≥ 5.
- Top two candidates tie within 1 point.
- The resolved ID has no `precedents.yaml`, OR no pattern matches.
- The placement would create a new ID (requires §21 procedure with user-authored schema entry).
- The placement would require multiple-systems / expand-an-area / extend-the-end (structural change).
- File content trips the external-path gate (§Step 6).
- A destructive operation is required (§Step 7).
- Authority sources disagree (filesystem ≠ jdex.yaml ≠ schema). Report the disagreement.
- Soft-warns W2 (AC.10 assigned) or W3 (file would land at area/category root) fire.
- The artifact looks like it belongs in PARA, not dev — hand off to `para-ontology`.
- The user mentions a sibling system identifier you don't have evidence for in `jdex.yaml`.

---

## 29. Spec metadata

| Field | Value |
|---|---|
| Johnny.Decimal spec | 6.5.0 |
| JDex schema (Bobby) | 1.0.0 |
| JDex content (Bobby) | 0.1.0 |
| Librarian (Bobby) | Bobby |
| Authoritative ID count | query `jd_get_system()` (never embed) |
| Universal spec | <https://johnnydecimal.com/> |
| Formal index-spec | <https://github.com/johnnydecimal/index-spec> |
| Awesome list | <https://github.com/johnnydecimal/awesome-johnnydecimal> |
| Lint reference | <https://github.com/SiriusStarr/jdlint> |
| Multi-vault Librarian pattern | <https://github.com/jabez007/johnny-decimal-zettelkasten> |

Spec citations used in Bobby's `jdex.yaml`:
- **JD 13.11** — Multiple systems (basis for `system.multiple_systems`)
- **JD 13.31** — Extend the end (basis for `90-99` reserved area)

---

## 30. Reference

For full normative text:

**Bobby C:\dev:**
- `C:\dev\40-49-ai-agents-and-prompts\46-memory-and-bootstrap\46.02-working-memory\AGENTS-01-dev.md`
- `C:\dev\40-49-ai-agents-and-prompts\46-memory-and-bootstrap\46.02-working-memory\AGENTS-02-para.md`
- `C:\dev\40-49-ai-agents-and-prompts\43-rules-skills-subagents\43.05-governance-decisions\agent-rules-single-source-of-truth.md`

**Universal JD spec (read-as-needed, not in full unless requested):**
- 11.01 Introduction · 11.02 Areas & categories · 11.03 IDs · 11.04 Philosophy · 11.05 The JDex · 11.06 Saving files · 11.07 Keeping notes · 11.08 The Librarian
- 12.01 Email · 12.02 Other JDex methods · 12.03 Standard zeros · 12.04 CLI · 12.05 AC.ID notation
- 13.01 System expansion intro · 13.11 Multiple systems · 13.12 Guidelines · 13.21 Expand-an-area · 13.31 Extend-the-end · 13.32 Guidelines
- 14.01 Build · 14.02 JD University · 14.03 Workshop · 14.04 Task & project management
- 15.01–15.04 Patterns and templates
- 22.00.0182 JDex deep-dive (data and storage)

This SKILL.md MUST be kept in sync with `AGENTS-01-dev.md`. When `AGENTS-01-dev.md` changes, regenerate this file rather than hand-patching. When the universal JD spec at johnnydecimal.com advances (currently v6.5.0), check Layer-1 sections against the new version.

---

*Layer 1 sourced from johnnydecimal.com 6.5.0 and the ecosystem repos under the johnnydecimal GitHub organization. Layer 2 sourced from `AGENTS-01-dev.md` (locked). Cross-cutting community insights from the JD forum, HN, and practitioner blogs.*
