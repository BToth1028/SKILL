# create-envelope — NORTH_STAR

TIER_3 intent brief for the `create-envelope` skill. Required sections per master-router `north_star_md.required_sections` (verbatim machine keys: `context`, `principles`, `boundaries_with_rationale`, `key_concepts_glossary`, `failure_modes`, `upstream_inheritance`, `decision_log_pointer`).

## context

Every governed file under `C:\dev` must carry minimum PDKOS envelope frontmatter — including `relations.edges` for graph participation — per the operator's 2026-05-08 decision following authoring of the folder envelope spec (01.05) v1.1.0 and `dev-README.yaml`. The envelope schema authority's 15-key floor is non-negotiable. The Subtype Contracts Authority (`019dd5b8-5083-7c0b-9d0e-5b7c0a4ed060`, slot 6 of the umbrella charter, activated 2026-05-08) closes the closed-world loop on `subtype` values and per-subtype required payload keys.

`create-envelope` is the **single authoritative tool** for emitting the resulting `<basename>.envelope.yaml` sidecars. It is called by `create-capability` (and future `create-rule`, `create-subagent`, `create-hook` skills) for every file those skills produce. Without `create-envelope`, sidecar emission would either (a) duplicate per-skill or (b) drift between skills — both are determinism violations.

## principles

1. **Single source of truth for emission.** Envelope-emission logic lives in exactly one place. Every caller invokes the same primitive with the same inputs and gets the same output.
2. **Read-only on the registry.** The skill never authors or mutates the Subtype Contracts Authority. It reads the registry and applies it. Registry amendments are governance actions, not tooling actions.
3. **Closed-world inputs.** `doc_class` is a closed enum drawn from the registry. Unrecognised values fail closed.
4. **Caller passes intent.** `doc_class` and `parent_envelope_id` are caller-supplied. The skill never guesses.
5. **Atomic write.** Sidecar emission is one-shot — full envelope written or no file written. No partial writes.
6. **No retroactive overwrite.** Existing sidecars are not silently replaced. Overwrite requires explicit operator consent (mirrors `create-capability` overwrite_gate).
7. **Eat your own dog food.** Every file in this package has its own sidecar emitted by these same templates. The skill's own substructure is the first proof point for its emission rules.

## boundaries_with_rationale

| Boundary | Rationale |
|---|---|
| Does NOT author governed files | Separation of concerns; governed-file authoring belongs to domain skills (create-capability, etc.). One skill, one job. |
| Does NOT update existing sidecars | Mutation is a separate concern (`update-envelope` is a future skill). Conflating create + update collapses the overwrite_gate. |
| Does NOT validate the corpus | Corpus validation belongs to `02.10-pdkos-envelope-compliance`. This skill is producer-side; that script is auditor-side. |
| Does NOT register new subtypes | Registry mutation is a governance action requiring authority amendment. This skill is read-only on the registry. |
| Does NOT infer doc_class from filename | Filename heuristics fail silently (e.g., `notes.md` could be `reference` or `generic_doc`). Caller must declare intent. |
| Does NOT decide parent_envelope_id | Parent identity depends on package structure and registry constraints (`permitted_parent_subtypes`). Caller must resolve before invocation. |

## key_concepts_glossary

- **Sidecar** — A `<basename>.envelope.yaml` file sitting next to a governed file (`SKILL.md` → `SKILL.envelope.yaml`). The sidecar is the PDKOS envelope; the governed file is the data the envelope describes.
- **`doc_class`** — Closed enum drawn from `payload.subtype_registry.entries[].subtype` in the Subtype Contracts Authority. Identifies which per-subtype contract applies.
- **`parent_envelope_id`** — UUID of the envelope that should appear as the `source` of the new envelope's `contains` edge. Must resolve to an envelope whose `subtype` is in the registry's `permitted_parent_subtypes` for the chosen `doc_class`.
- **Closed-world** — A value space whose admitted values are enumerated in a single authoritative artifact. Subtype values are closed-world per the Subtype Contracts Authority; lifecycle states are closed-world per the envelope schema authority's `lifecycle_state_enum`; etc.
- **Dog-food principle** — Skill applies its own emission rules to its own files. If `create-envelope` cannot produce its own sidecars from its own templates, the skill is broken.

## failure_modes

| Code | Trigger | Resolution |
|---|---|---|
| `DOC_CLASS_NOT_REGISTERED` | Caller passed a `doc_class` value not present in the registry | Halt; surface the registered enum to the caller; do not write |
| `PARENT_NOT_FOUND` | `parent_envelope_id` does not resolve to an existing envelope under `C:\dev` | Halt; do not write |
| `PARENT_SUBTYPE_NOT_PERMITTED` | Parent envelope's `subtype` is not in the registry's `permitted_parent_subtypes` for the chosen `doc_class` | Halt; surface the permitted set to the caller |
| `TARGET_EXISTS_NO_OVERWRITE` | `<basename>.envelope.yaml` already exists at the target path and overwrite consent was not given | Halt; do not write |
| `GOVERNED_FILE_NOT_FOUND` | `governed_file_path` does not exist on disk | Halt; do not write |
| `GOVERNED_FILE_OUTSIDE_DEV` | `governed_file_path` is not under `C:\dev` | Halt; do not write (per filesystem authority) |
| `REGISTRY_LOAD_FAILED` | Subtype Contracts Authority YAML cannot be parsed or has wrong `id` | Halt; emit registry-load diagnostic |
| `EMISSION_VALIDATION_FAILED` | Generated envelope fails self-validation against the 15-key shape or per-subtype contract | Halt; do not write; surface validation errors |

## upstream_inheritance

This skill inherits from and depends on (in load order):

1. **PDKOS Filesystem Authority** (`019dc031-df59-73f8-88dd-0d92eb9b9e59`) — for path law (sidecar location, governed-file location must be under `C:\dev`).
2. **PDKOS Envelope Schema Authority** (`cc2bb9ce-ab27-4a90-82d4-53e3051d696a`) — for the 15-key base envelope shape that emitted sidecars must satisfy.
3. **PDKOS Umbrella Charter** (`019dd4ef-a225-74df-a5f2-981b4a003889`) — for governance stack ordering and root authority.
4. **PDKOS Vocabulary Authority** (`019dd4ef-a239-7280-8177-0dd9b07db842`) — for canonical `lifecycle.state` and `labels.kot` values.
5. **PDKOS Relation Authority** (`019dd4d2-5850-7f9a-8b40-615704b7e6fc`) — for the closed set of `relations.edges[].type` values.
6. **PDKOS Subtype Contracts Authority** (`019dd5b8-5083-7c0b-9d0e-5b7c0a4ed060`) — for the closed registry of `subtype` values and per-subtype contracts. **Primary input data.**
7. **Folder Envelope Spec** (`53aff40b-6e04-4483-83c9-5cb516fe3528`) — for `area`, `category`, `id`, `workspace_root` subtype shapes (when emitting folder READMEs).
8. **Master-router `COMMAND.md`** (`C:/Users/rtoth/.cursor/commands/master-router/COMMAND.md`) — for TIER_3 capability requirements (NORTH_STAR.md required, intent_brief format, etc.).

## decision_log_pointer

Substantive decisions for this skill are recorded in:

- **2026-05-08 conversation transcript** establishing (a) the v1.1.0 amendment to 01.05 with the `approved_child_folders` allowlist, (b) the `dev-README.yaml` workspace-root envelope, (c) the operator decision that every governed file carries minimum PDKOS frontmatter including relations, (d) the choice of Path A (full schema floor) over a lighter tier, (e) the choice of `create-envelope` as a primitive separated from `create-capability`, and (f) activation of slot 6 of the umbrella charter via the new Subtype Contracts Authority.
- **`provenance.issue_ref`** in `SKILL.envelope.yaml` for the dated authoring record.
- **`payload.amendment_procedure`** in the Subtype Contracts Authority for the registry amendment process this skill depends on.

No standalone decision log file exists for this skill; the trail lives in the bootstrap session YAMLs under `46.01-bootstrap-yamls`.
