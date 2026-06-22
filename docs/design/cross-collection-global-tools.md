# Design: cross-collection global tools ledger

**Status:** design draft (v1.1+).
**Author:** Holobiomics Lab.
**Last revised:** 2026-05-25.

## Problem

In v1, each collection's tool records live at `collections/<slug>/v<N>/tools/<tool-slug>.yaml`. When we ship a second collection (e.g. `chemistry/v1`) and reference shared tools (e.g. `matchms`, `rdkit`, `r`), each collection gets its own copy. The IRIs are content-hashed per-collection, so the same tool has multiple canonical identifiers across collections — and the YAMLs may drift (different `license_spdx`, different `evidence_spans`, different `related_skills`).

Concrete pain:
- A downstream user citing `matchms` needs to know which collection's record is authoritative.
- Audit checks ("is the license consistent across all collections?") have no single source of truth.
- HuggingFace / Zenodo mirrors see N versions of the same tool record.

## Approach

Introduce a repo-root `tools/` ledger that's the single canonical source. Per-collection `tools.lock.yaml` references entries in the global ledger by content-hash IRI.

```
asb-skill-collections/
├── tools/                              # NEW: global ledger
│   ├── matchms/
│   │   └── v1/
│   │       ├── tool.yaml               # canonical record, content-hashed
│   │       └── content_hash.txt
│   ├── rdkit/v1/tool.yaml
│   └── ...
├── collections/
│   ├── metabolomics/v1/
│   │   ├── tools.lock.yaml             # references entries in /tools/
│   │   └── (no /tools/ subdir anymore)
│   └── chemistry/v1/
│       ├── tools.lock.yaml             # may share entries
│       └── ...
```

## Schema

**`tools/<slug>/v<N>/tool.yaml`** (canonical record):

Same fields as today's per-collection `tools/<slug>.yaml`, plus:
- `iri: https://w3id.org/holobiomicslab/asb-tool/<slug>@sha256:<hash>`
- `iri_latest: https://w3id.org/holobiomicslab/asb-tool/<slug>`
- `used_in_collections: [<coll>/v<N>, ...]` — back-pointer, auto-populated by aggregator
- `version_history: [{version: 1, ...}, ...]` — for tool flavors / version bumps

**Per-collection `tools.lock.yaml`** (unchanged shape, new resolution):

```yaml
tools:
  - slug: matchms
    iri: https://w3id.org/holobiomicslab/asb-tool/matchms@sha256:<hash>
    path: ../../tools/matchms/v1/tool.yaml      # relative to collection
    used_in_skills: [feature-detection, ...]
```

## Aggregation script

`scripts/regen_global_tools.py` runs on every `asb collection promote`:

1. Walks all `collections/**/tools/<slug>.yaml` AND the new `tools/<slug>/v*/tool.yaml`.
2. For each unique slug, merges per-collection records into a single canonical entry using the same `_merge_tool_candidates` logic in `promote.py`.
3. Writes the merged YAML to `tools/<slug>/v<N>/tool.yaml` and computes the canonical IRI.
4. Updates each collection's `tools.lock.yaml` to point at the IRI.
5. Emits `tools/_GLOBAL_INDEX.json` mapping `slug → iri → used_in_collections`.

## Migration

| Phase | When | What ships |
|---|---|---|
| 1 (transition) | v1.1 | Aggregator runs; emits BOTH legacy per-collection `tools/` AND new repo-root `tools/`. `tools.lock.yaml` references both. |
| 2 | v1.2 | New collections only emit the new layout. Old `tools/` removed from new releases. |
| 3 | v2.0 | Legacy per-collection `tools/` directories deleted from older collections via a migration tool. IRIs in old `tools.lock.yaml` re-resolved to the global ledger. |

## Cross-collection consistency CI

New workflow `validate-tool-cross-coll.yml` runs on PRs touching `tools/` or any `tools.lock.yaml`:

- Walks all collections.
- For each tool slug appearing in 2+ collections, verifies `license_spdx`, `canonical_url`, `purl` (PURL identifier) are consistent.
- Flags inconsistency as a PR error with the conflicting fields listed.

## Open questions

1. **Tool flavors.** Does `matchms-0.26.4` get its own entry, or is it a `version_history` row inside `matchms`? Recommendation: same slug, version_history list. Different SLUGS only for genuinely different tools (e.g. `mzmine-2-x` vs `mzmine3` if APIs differ).
2. **Per-collection evidence overrides.** A collection may want to attach its own `evidence_spans` to a tool (paper-specific). Recommendation: collection-level lock entries CAN carry a `collection_specific_evidence_spans` array; global record holds the union.
3. **Versioned IRIs vs latest IRIs.** Both ship today; this design keeps both. Downstream consumers pin the versioned IRI for reproducibility; humans browse via `iri_latest`.

## Tracking issue

(Placeholder — file when starting phase 1.)

## See also

- `tools.lock.yaml` schema in spec §4.
- IDEAS-Q.md: the original backlog entry that motivated this design.
