---
name: context-bootstrap
description: >-
  Mandatory session continuity protocol via living YAML bootstrap documents.
  Use this skill at the START and END of every session in every project — no
  exceptions. Triggers on: session start, session end, "bootstrap", "context
  handoff", "session continuity", "pick up where we left off", "resume work",
  "what were we doing", "end of session", "wrap up", "finalize", any reference
  to carrying state between sessions, any mention of a bootstrap file or
  bootstrap YAML, any new project initialization, any session-zero scenario.
  Also trigger when the user asks about task persistence, decision logging,
  context file audits, or project state snapshots. When in doubt, trigger —
  skipping the bootstrap is always worse than running it unnecessarily.
---

# Context Bootstrap — Mandatory Session Continuity Protocol

## What This Skill Is

This is an agent directive — not human documentation. All prose exists solely
for agent comprehension. If a zero-context agent cannot understand a section,
it is underwritten. If a section could be halved without losing meaning, it
is overwritten.

## What a Context Bootstrap IS

A context bootstrap is a single YAML file that captures the complete working
state of a project at the end of each session. It is the SOLE mechanism for
transferring context between sessions. Every session produces exactly one
bootstrap. Every subsequent session consumes the most recent bootstrap as its
starting point.

## What a Context Bootstrap IS NOT

- NOT a changelog or journal (it is a living snapshot, not a history log)
- NOT a summary of the conversation (it captures state, not transcript)
- NOT optional (every session produces one, no exceptions)
- NOT a place for the agent to store thoughts (it stores facts, decisions, and state)

The bootstrap captures: current state, active tasks, settled decisions with
rationale, and enough environmental detail that an agent with zero prior context
can resume work without asking the user to re-explain anything.

---

## File Naming and Storage

### Location

Bootstraps are stored in the workspace at a predictable, per-project path:

```
{workspace_root}/_staging/{ProjectName}/bootstrap/
```

If the project does not have a `_staging` folder, use:

```
{workspace_root}/bootstrap/
```

The agent reads from and writes to this directory. No manual file attachment
is needed — the agent locates bootstrap files by reading the directory.

### Naming Convention

```
{ProjectName}_YYMMDD-HHMM.yaml
```

| Rule | Detail |
|------|--------|
| Timestamp | Reflects session END time (when bootstrap is finalized) |
| Revision suffixes | None. Each file is a unique point-in-time snapshot |
| Retention | All bootstraps are retained for the life of the project |
| Canonical | The most recent bootstrap by timestamp is always canonical |
| Immutability | Older bootstraps are historical record — never modify them |

### Examples

```
TransLineEstimator_260318-1430.yaml
PDKOS_260319-0900.yaml
FormBuilder_260402-2145.yaml
```

---

## Session Lifecycle — Mandatory Sequence

This is a strict pipeline. Steps MUST execute in this order. No work may begin
until steps 1–3 are complete.

### Phase 1: INGEST (before any project work begins)

#### Step 1 — Read Previous Bootstrap

**Trigger:** Session start.

**Action:**
Read the most recent bootstrap file from the project's bootstrap directory.
Parse every section. Internalize the project state, active tasks, settled
decisions, environment, and any flagged issues.

To find the most recent bootstrap:
1. List all `.yaml` files in the bootstrap directory
2. Sort by filename timestamp descending
3. Read the first (most recent) file

If no bootstrap directory or no `.yaml` files exist, this is session-zero.
Read [schema.yaml](schema.yaml) and emit a fresh bootstrap populated with
whatever the user provides. Mark all context as "session-zero — no prior
history." Inform the user that continuity with any prior work is unavailable.

**Output to user:**
Provide a concise summary confirming:
- Current project state understood
- Active task count and high-level theme
- Any BLOCKED or DEFERRED items that may need user input
- Any decisions from prior sessions that constrain current work

Do NOT regurgitate the bootstrap. Synthesize it.

#### Step 2 — Audit Workspace Context Files

**Trigger:** Immediately after step 1.

**Action:**
Review relevant workspace files — rules, skills, reference documents, config
files, and any other context files the agent has been working with. For each,
determine:
- Is it still relevant to the current project state?
- Has it been superseded by a newer version?
- Is there duplication (two files covering the same content)?
- Does any file need to be updated based on work done in prior sessions
  (as recorded in the bootstrap)?

**Output to user:**
Report findings as a brief context audit:
- List any files that are STALE (outdated, superseded)
- List any files that are DUPLICATE (redundant with another)
- List any files that NEED UPDATE (content no longer matches current project state)
- If all context files are current, say so in one line.

The user decides what to do with flagged files. Do not delete or modify
context files without explicit instruction.

#### Step 3 — Initialize New Bootstrap

**Trigger:** Immediately after step 2.

**Action:**
Create the new session's bootstrap in memory. Populate by carrying forward
from the previous bootstrap:

**CARRY FORWARD (always):**
- Project identity and summary (update if scope has shifted)
- ALL tasks with status ACTIVE or BLOCKED (these persist)
- ALL tasks with status DEFERRED (these persist with rationale)
- Settled decisions (carry forward — these are permanent record)
- Environment snapshot (carry forward, will be updated at session end)

**DO NOT CARRY FORWARD:**
- Tasks with status DONE or CANCELLED from prior sessions (they served
  their purpose in that bootstrap; they are not copied into the new one)

The new bootstrap is now live. From this point forward, every qualifying
event updates it in-place.

### Phase 2: WORK (normal session activity)

#### Step 4 — Maintain Bootstrap During Session

**Trigger:** Hybrid — event-driven + periodic checkpoint (see Update Policy below).

As work progresses, the bootstrap is updated continuously. This is not optional.
The bootstrap must reflect reality at all times, not just at session end.

### Phase 3: FINALIZE (session ending)

#### Step 5 — Finalize Bootstrap

**Trigger:** Session end (user signals done, or natural completion).

**Action:**
Perform a final pass on the bootstrap:
- Ensure all tasks have accurate statuses
- Ensure all decisions made this session are recorded
- Capture a fresh environment snapshot
- Capture the context file audit (flag stale/outdated files for the NEXT
  session's agent to surface in step 2)
- Write a `session_summary`: 2–4 sentences covering what was accomplished,
  what remains, and any open questions

**Output to user:**
Write the finalized bootstrap YAML to the project's bootstrap directory using
the naming convention `{ProjectName}_YYMMDD-HHMM.yaml` with the current
timestamp. Confirm the file path to the user.

---

## Update Policy (Hybrid: Event-Driven + Periodic Checkpoint)

The bootstrap updates on two independent triggers. Both are active
simultaneously. Whichever fires first wins.

### Event Triggers

These cause an IMMEDIATE in-memory update to the bootstrap:

| Event | Action |
|-------|--------|
| `task-completed` | Set task status to DONE. Record completion note if non-obvious. |
| `new-task-discovered` | Add task with status ACTIVE. Include origin (user request, dependency, defect found, etc.). |
| `task-blocked` | Set task status to BLOCKED. Record blocker with enough detail to resolve without re-diagnosis. |
| `task-deferred` | Set task status to DEFERRED. Record reason and any conditions for reactivation. |
| `task-cancelled` | Set task status to CANCELLED. Record reason — cancellation is a decision and needs rationale. |
| `decision-made` | Add to decisions section. Include outcome AND rationale per Decision Logging Rules below. |
| `scope-change` | Update project summary and affected tasks. Note what changed and why. |
| `error-or-conflict-encountered` | Log in issues section. Include what was tried, what failed, and current resolution state. |

### Periodic Checkpoint

**Interval:** Every significant block of work — roughly every 3–5 substantive
exchanges, or whenever the agent recognizes that accumulated small changes have
not yet been captured by event triggers.

**Self-check question:** "If this session ended RIGHT NOW, would the bootstrap
accurately reflect where we are?" If the answer is no, checkpoint immediately.

**Action:** Review the bootstrap against current session state. Fill any gaps.
This is a catch-all for incremental progress that doesn't neatly map to a
single event trigger.

---

## Bootstrap Schema

This is the exact structure of every bootstrap file. All fields are mandatory
unless marked `[optional]`. For a copy-paste template, see [schema.yaml](schema.yaml).
For a filled-out example, see [example-bootstrap.yaml](example-bootstrap.yaml).

### `project`

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Project name — must match file naming convention |
| `summary` | string | 2–5 sentences. Current state of the project as a whole. Written for a zero-context agent. Covers: what the project IS, what phase it is in, and what the immediate trajectory looks like. |
| `scope` | string | What this project covers — its boundaries. |
| `non_scope` | string | What this project explicitly does NOT cover. |

### `session`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Timestamp matching the file name: `YYMMDD-HHMM` |
| `started` | string | ISO 8601 datetime |
| `ended` | string | ISO 8601 datetime — populated at finalization only |
| `session_summary` | string | 2–4 sentences written at finalization. What was accomplished, what remains, any open questions or risks heading into next session. |

### `tasks`

Flat list. Every task that EXISTS in the current session appears here. Tasks
carried forward from prior sessions retain their original `session_origin`.
New tasks created this session are tagged accordingly.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Short unique identifier, e.g., `T-001`, `T-002` |
| `title` | string | Imperative verb phrase, e.g., "Implement FK creation via DAO CreateRelation" |
| `status` | enum | `ACTIVE` \| `DONE` \| `BLOCKED` \| `DEFERRED` \| `CANCELLED` |
| `session_origin` | string | Session ID where this task was first created |
| `session_completed` | string \| null | Session ID where status became DONE or CANCELLED |
| `priority` | enum | `HIGH` \| `MEDIUM` \| `LOW` — `[optional]` but recommended for ACTIVE tasks |
| `description` | string | Enough detail that a zero-context agent can execute or continue this task without asking clarifying questions. If the task requires specific technical context (a particular API pattern, a known gotcha), include it here. |
| `blockers` | string \| null | For BLOCKED tasks: what is preventing progress |
| `deferred_reason` | string \| null | For DEFERRED tasks: why, and conditions to reactivate |
| `cancelled_reason` | string \| null | For CANCELLED tasks: why it was dropped |
| `notes` | string \| null | `[optional]` Any additional context accumulated during work |

### `decisions`

Every design choice, architectural call, or directional decision made during
ANY session. These accumulate across the project lifetime and are NEVER removed
from the bootstrap (they carry forward forever).

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | `D-001`, `D-002`, etc. |
| `session_origin` | string | Session ID where decision was made |
| `domain` | string | What area this decision affects (e.g., "database", "UI", "architecture", "naming") |
| `outcome` | string | What was decided — the concrete result |
| `rationale` | string | WHY this was decided. Write so a zero-context agent understands not just WHAT was chosen but WHY the alternatives were rejected. Include specific technical or practical reasoning. If the decision resolved a tradeoff, name both sides and explain why this side won. Apply the Zero-Context Test (see Decision Logging Rules). |
| `supersedes` | string \| null | ID of prior decision this replaces, if any |

### `environment`

Snapshot of the working environment. Updated at session finalization. Captures
anything an incoming agent needs to know to operate.

| Field | Type | Description |
|-------|------|-------------|
| `tools` | list of strings | Software, frameworks, languages in active use |
| `key_paths` | list of strings | File paths, database locations, output directories that matter for ongoing work. Not every file — just the ones relevant to current tasks. |
| `schema_state` | string \| null | `[optional]` Current state of any database schemas, APIs, or data models |
| `dependencies` | string \| null | `[optional]` External dependencies, services, accounts |
| `notes` | string \| null | `[optional]` Anything else environment-related |

### `context_file_audit`

Populated at session finalization. Lists workspace context files and their
current relevance status. The NEXT session's agent uses this as a pre-check
in step 2, then performs its own fresh audit.

| Field | Type | Description |
|-------|------|-------------|
| `filename` | string | File path relative to workspace root |
| `status` | enum | `CURRENT` \| `STALE` \| `NEEDS_UPDATE` \| `DUPLICATE` |
| `note` | string \| null | Why it's flagged, or what needs updating |

### `issues`

`[optional section]` Open problems, unresolved errors, technical debt, or
risks. Anything that isn't a task but needs to be tracked.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | `I-001`, `I-002` |
| `summary` | string | What the issue is |
| `severity` | enum | `HIGH` \| `MEDIUM` \| `LOW` |
| `session_origin` | string | When it was first identified |
| `resolution` | string \| null | How it was resolved, if resolved |

---

## Decision Logging Rules

### When to Log

Any time a choice is made that could reasonably go a different way. If the
user or agent selects between alternatives — even if the choice seems obvious
— log it. "Obvious" to a current-context agent is not obvious to a
zero-context agent in a future session.

### The Zero-Context Test

After writing the outcome and rationale, re-read them as if you know NOTHING
about this project. Ask:

1. Do I understand what was decided?
2. Do I understand why?
3. Would I be tempted to revisit or reverse this decision?

If the answer to (3) is yes, the rationale needs more detail.
If the answer to (1) or (2) is no, rewrite.

### What NOT to Log

Do not log trivial operational choices (e.g., "used a for-loop instead of a
while-loop"). Only log decisions that affect project direction, architecture,
naming, scope, tooling, or approach.

---

## Task Persistence Rules

The task list is the project's living TODO. It persists across sessions with
the following carry-forward rules:

### Carry-Forward Matrix

| Status | Carry Forward? | Detail |
|--------|---------------|--------|
| `ACTIVE` | Always | This is incomplete work. |
| `BLOCKED` | Always | Include blocker detail so next session can attempt resolution. |
| `DEFERRED` | Always | Include reactivation conditions. |
| `DONE` | Never | Exists only in the bootstrap of the session where it was completed. |
| `CANCELLED` | Never | Exists only in the bootstrap of the session where it was cancelled. |

### ID Stability

Task IDs are permanent. `T-001` is always `T-001` across all bootstraps.
New tasks get the next available ID. Never reuse a completed or cancelled
task's ID.

### Ordering

Tasks are ordered by:
1. Status: ACTIVE first, then BLOCKED, then DEFERRED
2. Priority: HIGH > MEDIUM > LOW
3. ID: ascending

This ordering is deterministic and must be consistent across bootstraps.

---

## Anti-Drift Rules

1. Never skip the session lifecycle steps. Ever. No exceptions.
2. Never begin project work before completing steps 1–3.
3. Never finalize a session without completing step 5.
4. If the user asks to skip the bootstrap process, remind them that this
   directive governs all sessions. Offer to make the process faster, but
   do not skip it.
5. If the previous bootstrap is missing or not provided, inform the user
   immediately. Do not attempt to reconstruct context from memory or
   assumptions. Start a fresh bootstrap and note that continuity with
   prior sessions may be incomplete.
6. If a task's status is ambiguous, set it to ACTIVE and flag it with a
   note requesting clarification. Do not guess.
7. The bootstrap is the canonical source of truth for session state. If
   your memory and the bootstrap conflict, the bootstrap wins.

---

## Error Handling

| Error | Policy |
|-------|--------|
| **Missing bootstrap** | Alert user. Cannot proceed with continuity. Initialize a fresh bootstrap. Mark all context as "session-zero" — no prior history. |
| **Ambiguous task status** | Default to ACTIVE. Add note: "Status unclear — carried as ACTIVE pending user clarification." |
| **Conflicting information** | Flag the conflict explicitly in the issues section. Do not silently resolve it. Present both versions to the user and ask for canonical answer. |
| **Missing fields** | If a required schema field cannot be populated, use the string `UNKNOWN — [reason]`. Never leave a required field blank. Never invent a value. |
| **Bootstrap directory missing** | Create it. Log in session notes that this is a first-session bootstrap for this project. |

---

## Reference Files

| File | Contents |
|------|----------|
| [schema.yaml](schema.yaml) | Copy-paste bootstrap template with all fields |
| [example-bootstrap.yaml](example-bootstrap.yaml) | Realistic filled-out example showing what a real bootstrap looks like |
