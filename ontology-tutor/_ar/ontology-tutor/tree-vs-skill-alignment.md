# SKILL.md vs Logic Tree — Step Order Alignment Analysis

**Date:** 2026-05-08  
**Files compared:**  
- `SKILL.md` (see file, v1.3.7)  
- `ontology-tutor-logic-tree.md` (816 lines)

---

## Method

Every `##` and `###` section in SKILL.md was assigned a sequential position number (S-1 through S-26). Every major label or step group in the logic tree was assigned a sequential position number (T-1 through T-14). The table below maps each SKILL.md section to its tree counterpart, then flags whether the relative order is preserved or shifted.

---

## Full Mapping

| Pos | SKILL.md Section (line) | Tree Location | Aligned? | Notes |
|-----|------------------------|---------------|----------|-------|
| S-1 | Contract Metadata (11) | Not in tree | — | Static metadata (version string). No decision logic — correctly omitted. |
| S-2 | Mode Selector (16) | [ACTIVATE] step 3 (tree line 39) | ✅ | |
| S-3 | Sources (Pointer) (25) | Not in tree as standalone | — | Pointer-only section. Its target (S-5) is fully represented. Correctly omitted as a standalone node. |
| S-4 | Session Mission (29) | START context lines (tree line 10–14) | ✅ | Captured as the opening context/purpose statement. |
| S-5 | Source Authority Model (50) | [EVIDENCE-REFRESH-LOOP] (tree line 297) | ⚠️ SHIFTED | See Misalignment #1 below. |
| S-5a | └ Source Definitions (54) | [EVIDENCE-REFRESH-LOOP] steps 1–4 tool annotations | ✅ within parent | |
| S-5b | └ Fixed Evidence Order (64) | [EVIDENCE-REFRESH-LOOP] header context (line 303) | ✅ within parent | |
| S-5c | └ Transition Criteria (70) | [EVIDENCE-REFRESH-LOOP] step 1 citeability + step 2 criterion + step 3 criterion | ✅ within parent | |
| S-5d | └ Refresh-Only Constraint / Enum (84) | [EVIDENCE-REFRESH-LOOP] header context (line 300–301) + [VALIDATION-GATES] Authority gate | ✅ within parent | |
| S-5e | └ Evidence-Refresh Loop (95) | [EVIDENCE-REFRESH-LOOP] entire branch (lines 297–440) | ✅ within parent | |
| S-5f | └ Refresh-Phase Mutations (112) | [EVIDENCE-REFRESH-LOOP] → [REFRESH-SOURCE-1] sub-branch | ✅ within parent | |
| S-5g | └ Source 9 — Hard Gate (121) | [EVIDENCE-REFRESH-LOOP] step 4 (tree line 422) | ✅ within parent | |
| S-5h | └ Source X — Prohibition (131) | [VALIDATION-GATES-MODE-1] Source X gate (line 508) + [ANTI-DRIFT] rule 1 (line 761) | ✅ | Distributed across enforcement points — correct for a constraint. |
| S-5i | └ Read-Only Execution (135) | START context (line 12) + [VALIDATION-GATES-MODE-1] Read-only gate (line 501) | ✅ | Same distribution pattern as Source X. |
| S-6 | Evidence Sources — Operational Procedures (153) | [EVIDENCE-REFRESH-LOOP] steps 1–3 detailed procedures | ⚠️ SHIFTED | See Misalignment #2 below. |
| S-6a | └ Source 1 — Vector retrieval (157) | [EVIDENCE-REFRESH-LOOP] step 1 (tree line 305) | ✅ within parent | |
| S-6b | └ Source 2 — Snapshot filesystem (173) | [EVIDENCE-REFRESH-LOOP] step 2 (tree line 338) | ✅ within parent | |
| S-6c | └ Source 3 — typedb.com (194) | [EVIDENCE-REFRESH-LOOP] step 3 (tree line 394) | ✅ within parent | |
| S-7 | Evidence Refresh Loop (Pointer) (198) | Not in tree as standalone | — | Pointer-only section. Correctly omitted. |
| S-8 | Required Files And Bindings (202) | [ACTIVATE] step 2 context lines (tree line 20–23) | ⚠️ SHIFTED | See Misalignment #3 below. |
| S-9 | ROUTER And Corpus Law (217) | [ACTIVATE] step 2 context + [ANTI-DRIFT] rules 2, 5 | ⚠️ SHIFTED | See Misalignment #4 below. |
| S-10 | Mandatory Activation (229) | [ACTIVATE] (tree line 16) | ✅ | |
| S-11 | Decision Procedure (250) | [MODE-DISPATCH] (tree line 79) | ✅ | |
| S-11a | └ Mode 1 — Pure TypeDB (252) | [MODE-1-PIPELINE] (tree line 89) | ✅ | |
| S-11b | └ Mode 2 — TypeDB Embodiment using SQL (289) | [MODE-2-PIPELINE] (tree line 189) | ✅ | |
| S-12 | SQL Embodiment Mode — Field Value Governance (322) | [FIELD-VALUE-GOVERNANCE] (tree line 442) | ✅ | |
| S-13 | Validation Gates (351) | [VALIDATION-GATES-MODE-1] + [VALIDATION-GATES-MODE-2] (tree lines 491, 562) | ✅ | |
| S-14 | Output Contract (377) | [EMIT-MODE-1] + [EMIT-MODE-2] (tree lines 607, 633) | ✅ | |
| S-15 | Commands (475) | [ACTIVATE] step 4 command list (tree line 51–64) | ⚠️ SHIFTED | See Misalignment #5 below. |
| S-16 | Error Policy (491) | [ERROR-DISPATCH] (tree line 655) | ✅ | |
| S-17 | Corpus And Archive Policy (523) | START context line 14 (_ar/ rule) + [EVIDENCE-REFRESH-LOOP] header | ⚠️ SHIFTED | See Misalignment #6 below. |
| S-18 | Maintainer Workflow (529) | [MAINTAINER-WORKFLOW] (tree line 718) | ✅ | |
| S-19 | Anti-Drift Rules (551) | [ANTI-DRIFT RULES] (tree line 756) | ✅ | |

---

## Summary Counts

| Status | Count |
|--------|-------|
| ✅ Aligned | 12 major sections (+ all subsections within Source Authority Model) |
| ⚠️ Shifted | 6 sections |
| — Correctly omitted | 3 sections (pointer-only or static metadata) |

---

## Misalignment Explanations

### Misalignment #1 — Source Authority Model (S-5 → tree line 297)

**SKILL.md position:** Lines 50–151. Appears 5th, immediately after Scope and before Evidence Sources Operational Procedures.  
**Tree position:** `[EVIDENCE-REFRESH-LOOP]` at tree line 297, which is the 5th major branch — but it appears AFTER both mode pipelines in the rendered tree.

**Why it shifted:** The SKILL.md organizes Source Authority Model as a *reference section* — a canonical block of definitions meant to be consulted from multiple points. The tree organizes by *execution flow* — you hit the evidence refresh loop only when a mode pipeline's step 1 calls it. Since the tree follows the runtime call graph (ACTIVATE → MODE-DISPATCH → MODE-1/2-PIPELINE step 1 → EVIDENCE-REFRESH-LOOP), the evidence refresh content naturally lands after the pipeline branches that invoke it, not before them.

**Is this a problem?** No. In the SKILL.md, the Source Authority Model is placed early because it's a *definition* that the later sections need to reference. In the tree, it's placed where it *executes*. Both orderings are correct for their medium — reference doc vs. execution trace.

---

### Misalignment #2 — Evidence Sources — Operational Procedures (S-6 → inside tree line 297)

**SKILL.md position:** Lines 153–196. A standalone `##` section after Source Authority Model.  
**Tree position:** Merged INTO `[EVIDENCE-REFRESH-LOOP]` steps 1–3 as the detailed query/retrieval procedures for each source.

**Why it shifted:** The SKILL.md separates *rules* (§Source Authority Model: when/why to use each source) from *procedures* (§Evidence Sources — Operational Procedures: how to query each source). The tree has no reason to maintain this separation because at runtime, the "when" and "how" execute together — you check Source 1 (when = Source 1 is first; how = qdrant-find with these query terms and citeability test) in a single step. Splitting them in the tree would force the reader to jump between two branches for what is one continuous action.

**Is this a problem?** No. The SKILL.md separation is a good authoring pattern (rules in one place, procedures in another, no duplication). The tree merging is a good reading pattern (everything you need for Source 1 is in one step). They serve different purposes.

---

### Misalignment #3 — Required Files And Bindings (S-8 → tree line 20)

**SKILL.md position:** Lines 202–215. Appears after Evidence Refresh Loop Pointer and before ROUTER Law.  
**Tree position:** Folded into `[ACTIVATE]` step 2 (tree line 20–23) as context about what ROUTER.yaml contains and the rule that deployment bindings live there.

**Why it shifted:** Required Files And Bindings is a *configuration prerequisite* — it tells you what files must exist and where bindings come from. In an execution tree, prerequisites are checked at startup, not in a standalone reference section. The tree puts this where the agent first touches ROUTER.yaml (step 2 of activation), which is where "does this file exist and what does it contain?" naturally occurs.

**Is this a problem?** No. The SKILL.md placement is mid-document because it's a reference section that other sections point to. The tree placement is early because at runtime you need to know this before doing anything else.

---

### Misalignment #4 — ROUTER And Corpus Law (S-9 → tree line 20 + 756)

**SKILL.md position:** Lines 217–227. A standalone section after Required Files And Bindings.  
**Tree position:** Split across two locations:  
1. `[ACTIVATE]` step 2 context (tree line 20–23) — the operational facts (ROUTER is source of truth, binding keys, registry structure).  
2. `[ANTI-DRIFT RULES]` rules 2 and 5 (tree lines 762, 765) — the prohibitions (don't treat hints as evidence, no non-router ingest scopes).

**Why it shifted:** ROUTER And Corpus Law is a *mixed section* — part operational fact ("here's how the corpus is structured"), part constraint ("don't do X"). The tree splits mixed content by execution role: operational facts go where they're consumed (ACTIVATE, when reading ROUTER.yaml), and constraints go where they're enforced (ANTI-DRIFT, as invariants). A tree branch for "ROUTER corpus law" with no decision point would be dead weight.

**Is this a problem?** No, but it's the one misalignment worth watching. If someone reads only the tree and needs to understand the *full* ROUTER contract (what `vector_source_file_registry` contains, what `situational_retrieval_hints_only_not_evidence` means, what `ontology_skill_bootstrap_corpus_*` entries do), they'd need more detail than the tree provides. The tree gives enough to *execute* correctly but not enough to *understand the design* of the corpus architecture.

---

### Misalignment #5 — Commands (S-15 → tree line 51)

**SKILL.md position:** Lines 475–489. Near the end, after Output Contract.  
**Tree position:** Folded into `[ACTIVATE]` step 4 (tree line 51–64) as the command-routing table.

**Why it shifted:** In the SKILL.md, §Commands is a *reference section* — it lists each command with a summary of what it does, including behavioral constraints like "one table per invocation" and "no field excluded without operator approval." It sits late in the document because it's a summary that references concepts defined earlier.

In the tree, command routing happens *early* — it's step 4 of activation, before any pipeline runs. The tree places the command list where the routing decision is made, because that's where the agent needs to know which commands exist for which mode.

**Is this a problem?** Partially. The tree captures the command-to-mode mapping and the routing decision, but the SKILL.md §Commands section also restates behavioral constraints from the pipeline (D-1 and D-2 from the duplication audit — field-removal rule and one-table constraint). Those restatements are *not* in the tree's ACTIVATE step 4 because the tree handles them in the pipeline steps where they execute. So the tree is cleaner here, but a reader comparing the two will notice that the SKILL.md §Commands section contains information that the tree distributes across [ACTIVATE] step 4 + [MODE-2-PIPELINE] steps 0 and 5 + [FIELD-VALUE-GOVERNANCE].

---

### Misalignment #6 — Corpus And Archive Policy (S-17 → tree lines 14 + 297)

**SKILL.md position:** Lines 523–527. Near the end, after Error Policy.  
**Tree position:** Split across:  
1. START context line 14 — the `_ar/` dead archive rule.  
2. `[EVIDENCE-REFRESH-LOOP]` header — the fact that runtime evidence follows the Source Authority Model pipeline.

**Why it shifted:** Corpus And Archive Policy contains two unrelated rules stapled together: (a) runtime evidence follows the evidence pipeline (which is just a pointer to §Source Authority Model), and (b) `_ar/` folders are forbidden. The tree puts (a) where evidence is gathered (the refresh loop) and (b) at the very top as a global constraint, because the archive prohibition applies to every file-read operation, not just one pipeline step.

**Is this a problem?** No. The SKILL.md groups them because they're both about "what sources are valid." The tree splits them by scope — global constraint vs. pipeline-specific rule. Both are correct for their format.

---

## Root Cause Pattern

All 6 misalignments share the same root cause: **the SKILL.md is organized by *topic* (reference sections grouped by subject) while the tree is organized by *execution order* (steps grouped by when they run).**

This means:

- **Definition sections that are consulted from multiple places** (Source Authority Model, Required Files, ROUTER Law, Commands) get pulled *earlier* in the tree (to where they're first consumed) or *merged into the calling step*.
- **Mixed sections that contain both facts and constraints** (ROUTER Law, Corpus Policy) get *split* in the tree — facts go to the consuming step, constraints go to the invariant block.
- **Pointer-only sections** (Sources Pointer, Evidence Refresh Loop Pointer) are *correctly absent* from the tree because they have no execution step.

No misalignment represents missing content. Every rule, constraint, step, and decision point in the SKILL.md has a corresponding location in the tree. The differences are purely structural — topic-grouped reference document vs. execution-ordered decision tree.
