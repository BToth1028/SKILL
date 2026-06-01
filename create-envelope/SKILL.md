---
name: create-envelope
description: Use when emitting a PDKOS envelope sidecar (<basename>.envelope.yaml) for any governed file under C:\dev. Reads the closed-world subtype registry from the Subtype Contracts Authority, looks up the file's doc class, populates the 15-key envelope shape per the registered per-subtype contract, and writes the sidecar next to the file. Single-purpose primitive called by create-capability and other create-* skills; never invoked to author the governed file itself.
disable-model-invocation: true
---

# create-envelope

Single-purpose primitive that emits PDKOS envelope **sidecars** for governed files under `C:\dev`. One input transformation: `(governed_file_path, doc_class, parent_envelope_id) -> <basename>.envelope.yaml` written next to the governed file.

## Contract Metadata

- `contract_version`: `1.0.0`
- `supported_router_version`: `1.0.0`
- **master-router `TIER_3`** — installed skill is request type `SKILL`, matching `tier_definitions.TIER_3` (`intent_anchor_required`, `intent_brief_required`, `intent_brief_format: standalone_north_star_md_file`, `north_star_md_required: true`); authoritative file: `C:/Users/rtoth/.cursor/commands/master-router/COMMAND.md`.
- **`north_star_md.required_sections`** (verbatim per master-router): `context`, `principles`, `boundaries_with_rationale`, `key_concepts_glossary`, `failure_modes`, `upstream_inheritance`, `decision_log_pointer` → implemented in [`NORTH_STAR.md`](NORTH_STAR.md).
- **`tier_locked`**: `TIER_3`. Sidecars this skill emits inherit no tier from the governed file; tier is a property of the package, not the sidecar.

## Mission

For every invocation: take a governed-file path, a `doc_class` value (closed-world enum from the Subtype Contracts Authority registry), and a parent envelope id; mint a fresh UUID; populate the 15 base envelope keys per the envelope schema authority and the per-subtype required keys per the Subtype Contracts Authority; write the result to `<basename(governed_file)>.envelope.yaml` in the same directory; return the new envelope id.

Never improvise the envelope shape. Never guess `doc_class` from filename heuristics — caller must pass it explicitly. Never overwrite an existing sidecar without explicit operator consent (per overwrite_gate, mirror create-capability's pattern).

## Closed-World Enums

`doc_class_enum` (mirrors `subtype` values from the Subtype Contracts Authority registry):

- `skill_root` — sidecar for `SKILL.md`
- `command_root` — sidecar for `COMMAND.md`
- `north_star` — sidecar for `NORTH_STAR.md`
- `router_data` — sidecar for `ROUTER.yaml`
- `reference` — sidecar for `references/*.md`
- `package_contract` — sidecar for `contracts/*.yaml`
- `generic_doc` — catch-all sidecar for any other governed file
- `area`, `category`, `id`, `workspace_root` — folder README envelopes (still emitted by this skill if the caller passes the doc_class explicitly; primary use case is folder-readme tooling)

`doc_class` values not in this enum → halt with `DOC_CLASS_NOT_REGISTERED`.

## Activation

Run these steps in order on every invocation.

1. **Read inputs.** Required: `governed_file_path` (absolute, must exist, must be under `C:\dev`), `doc_class` (closed enum above), `parent_envelope_id` (valid UUID, must resolve to an existing envelope under `C:\dev` whose `subtype` is in the registry's `permitted_parent_subtypes` for the chosen `doc_class`). Optional: `title_override`, `purpose_override`, `extra_payload_keys`.

2. **Load the Subtype Contracts Authority.** Resolve `019dd5b8-5083-7c0b-9d0e-5b7c0a4ed060` from `C:\dev\40-49-ai-agents-and-prompts\41-prompts\41.03-deterministic-specs\pdkos-subtype-contracts-authority--5b7c0a4ed060.yaml`. Look up the `doc_class` entry in `payload.subtype_registry.entries[]`. Read its `canonical_contract_name`, `role_constraint`, `domain_constraint`, `labels_kot`, `required_payload_keys`, `required_payload_subkeys`, `permitted_parent_subtypes`. If absent → halt with `DOC_CLASS_NOT_REGISTERED`.

3. **Run the gates** in [`contracts/emit-envelope.yaml`](contracts/emit-envelope.yaml): naming, overwrite, path, parent-subtype, registry-resolve. Each gate has a `failure_code` to return on failure.

4. **Emit the sidecar** following [`references/emit-envelope.md`](references/emit-envelope.md). Populate the 15 base keys + per-subtype required keys. Mint the UUID. Author the `contains` edge upward to `parent_envelope_id`.

5. **Write atomically** to `<basename(governed_file)>.envelope.yaml` in the same directory as `governed_file_path`. Return the new envelope's `id`.

## Out of Scope

- Authoring the governed file itself (that's `create-capability`, `create-rule`, `create-subagent`, etc.).
- Editing existing sidecars (separate `update-envelope` skill if/when needed; not in this scope).
- Validating the existing corpus (that's `02.10-pdkos-envelope-compliance`).
- Inferring `doc_class` from filename. Caller must pass it.
- Authoring the Subtype Contracts Authority itself or registering new subtypes (that's a governance action, not a tooling action).

## See also

- **Subtype Contracts Authority:** `40-49-ai-agents-and-prompts\41-prompts\41.03-deterministic-specs\pdkos-subtype-contracts-authority--5b7c0a4ed060.yaml`
- **Envelope schema authority:** `40-49-ai-agents-and-prompts\41-prompts\41.03-deterministic-specs\pdkos-envelope-schema-authority--53e3051d696a.yaml`
- **Folder envelope spec (01.05):** `00-09-system-administration\01-meta-and-policy\01.05-folder-envelope-spec\01.05-folder-envelope-spec.yaml`
- **Caller skill:** `40-49-ai-agents-and-prompts\43-rules-skills-subagents\43.01-custom-skills\create-capability\SKILL.md` (will integrate this skill in a follow-up)
