# emit-envelope — Reference Recipe

L3 prose recipe for the single-route deterministic emission protocol. Mirrors `contracts/emit-envelope.yaml` (L4) in human-readable form. **If this prose disagrees with the L4 contract, the contract YAML wins.**

## When to invoke

You are emitting a PDKOS envelope sidecar (`<basename>.envelope.yaml`) for a governed file under `C:\dev`. The governed file already exists or is being written in the same operation. Caller (you, or a calling skill like `create-capability`) has determined:

- The absolute path of the governed file (`governed_file_path`).
- The doc class (`doc_class`) — one closed-world string drawn from the Subtype Contracts Authority registry (`019dd5b8-5083-7c0b-9d0e-5b7c0a4ed060`).
- The parent envelope id (`parent_envelope_id`) — UUID of the envelope whose `subtype` is in the registry's `permitted_parent_subtypes` for the chosen `doc_class`.

If any of these are unknown, **stop and resolve them first**. Do not invoke with placeholders.

## Step 1 — Load the registry

Open `C:\dev\40-49-ai-agents-and-prompts\41-prompts\41.03-deterministic-specs\pdkos-subtype-contracts-authority--5b7c0a4ed060.yaml`. Verify `id == "019dd5b8-5083-7c0b-9d0e-5b7c0a4ed060"`. Locate the entry in `payload.subtype_registry.entries[]` whose `subtype` equals your `doc_class`. Read its facets:

- `canonical_contract_name` (or `canonical_contract_name_pattern`)
- `role_constraint` (list)
- `domain_constraint` (list)
- `labels_kot` (string)
- `required_payload_keys` (list)
- `required_payload_subkeys` (mapping; may be empty)
- `permitted_parent_subtypes` (list)
- `sidecar_for` (string or null)

Cache these. They define what the constructed envelope must contain.

If the lookup fails, return failure code `DOC_CLASS_NOT_REGISTERED`. If the file load itself fails, return `REGISTRY_LOAD_FAILED`.

## Step 2 — Resolve and validate the parent

Locate the envelope identified by `parent_envelope_id`. Fastest path: grep all `*.yaml` files under `C:\dev` for `^id: "<parent_envelope_id>"` (top-level). Read its `subtype` field. Assert that value appears in the cached `permitted_parent_subtypes`. On failure, return `PARENT_NOT_FOUND` or `PARENT_SUBTYPE_NOT_PERMITTED`.

## Step 3 — Compute the target sidecar path

```
target_path = dirname(governed_file_path) + sep + basename(governed_file_path) + ".envelope.yaml"
```

Examples:

| governed_file_path | target_path |
|---|---|
| `C:\dev\...\create-envelope\SKILL.md` | `C:\dev\...\create-envelope\SKILL.envelope.yaml` |
| `C:\dev\...\contracts\emit-envelope.yaml` | `C:\dev\...\contracts\emit-envelope.envelope.yaml` |
| `C:\dev\...\references\fix-skill.md` | `C:\dev\...\references\fix-skill.envelope.yaml` |

Assert `target_path` is under `C:\dev`. On failure, `NAMING_GATE_FAILED`.

## Step 4 — Overwrite check

If `target_path` exists on disk:

- And `target_path` is in `overwrite_explicit_paths` → proceed (operator consented).
- Otherwise → halt with `TARGET_EXISTS_NO_OVERWRITE`.

This is the single overwrite gate; never default to overwrite, never accept blanket consent like `overwrite=True`.

## Step 5 — Construct the envelope (in memory)

Build the YAML structure with the 15 base keys plus per-subtype required keys.

### Static (constants)

```yaml
ontology_version: "1.0.0"
vocab_authority_id: "019dd4ef-a239-7280-8177-0dd9b07db842"
contract:
  name: <canonical_contract_name>          # from registry entry
  version: "1.0.0"
lifecycle:
  state: active
  version: 1
  since: <ISO 8601 now>
labels:
  kot: <labels_kot>                         # from registry entry
provenance:
  issued_by: human_operator                 # or caller-supplied id
  issued_at: <ISO 8601 now>
  issue_ref: <purpose_override or default>
  authority: human_operator
  signature: null
created_at: <ISO 8601 now>
updated_at: <ISO 8601 now>
```

### Computed per-doc

```yaml
id: <freshly minted UUID>                   # v4 or v7
domain: <domain_constraint[0]>              # or caller override
role: <role_constraint[0]>                  # or caller override
subtype: <doc_class>
title: "<basename(governed_file_path)> — PDKOS sidecar"   # or caller override
relations:
  edges:
    - type: contains
      source: <parent_envelope_id>
      target: <minted id>
      note: <derived note>
```

### Payload

```yaml
payload:
  pdkos_authority_ref: "cc2bb9ce-ab27-4a90-82d4-53e3051d696a"
  governs_file: <basename(governed_file_path)>
  purpose: <purpose_override or default phrase>
  # plus every other key listed in required_payload_keys for this doc_class
  # plus every required_payload_subkeys structure
```

If the per-subtype contract requires payload keys beyond `pdkos_authority_ref`, `purpose`, and `governs_file`, the **caller must supply them via `extra_payload_keys`**. The recipe does not invent values for `capability_package`, `tier_brief_for_package`, `applies_to_routes`, etc. — those are caller knowledge.

## Step 6 — Self-validate

Before writing, verify the constructed envelope:

1. All 15 top-level keys present.
2. All `required_payload_keys` present in `payload`.
3. All `required_payload_subkeys` present where applicable.
4. `id` matches the UUID pattern `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`.
5. `subtype` equals input `doc_class`.
6. `role` is in registry's `role_constraint` for this `doc_class`.
7. `domain` is in registry's `domain_constraint` for this `doc_class`.
8. `labels.kot` equals registry's `labels_kot`.
9. Exactly one `contains` edge present with `source == parent_envelope_id` and `target == minted id`.

Any failure → `EMISSION_VALIDATION_FAILED`. Do not write.

## Step 7 — Atomic write

Serialize to YAML (UTF-8, no BOM, LF or CRLF per workspace convention) and write to `target_path` in a single operation. Return `(envelope_id, target_path)` to the caller.

## Common doc_class examples

| doc_class | Typical governed_file | Typical parent_envelope_id |
|---|---|---|
| `skill_root` | `SKILL.md` | ID-level README (e.g., `43.01-README.yaml`) or umbrella charter (transitional) |
| `north_star` | `NORTH_STAR.md` | Sibling `SKILL.envelope.yaml` (the package's `skill_root`) |
| `router_data` | `ROUTER.yaml` | Sibling `SKILL.envelope.yaml` |
| `package_contract` | `contracts/<name>.yaml` | Sibling `SKILL.envelope.yaml` or `ROUTER.envelope.yaml` |
| `reference` | `references/<name>.md` | Sibling `SKILL.envelope.yaml` |
| `generic_doc` | any other governed file | Containing folder's README envelope, or skill_root, or category README |

## Anti-patterns (do NOT do these)

- **Filename heuristics.** Do not infer `doc_class` from the filename. `notes.md` could be `reference` or `generic_doc`; you don't know without caller intent.
- **Default to umbrella charter.** Picking the umbrella charter as parent because no closer parent exists is only acceptable when the registry explicitly permits it as a transitional parent (currently true for `skill_root`, `command_root`, `area`, `category`, `id`).
- **Silent overwrite.** Never replace an existing sidecar without the explicit per-path consent in `overwrite_explicit_paths`.
- **Inventing payload keys.** If `required_payload_keys` lists a key the caller did not supply, halt with `EMISSION_VALIDATION_FAILED`. Do not invent a placeholder.
- **Skipping self-validation.** The 9 checks in Step 6 are non-negotiable. Skipping any of them breaks the determinism guarantee.
