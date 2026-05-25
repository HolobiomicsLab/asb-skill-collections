# Changelog — Metabolomics v1

## v1.0 — 2026-05-25

- Initial release.
- 105 deduplicated skills derived from 5 ASB source runs (4 included + 1 excluded; see corpus.yaml rationale for `10.1073/pnas`).
- 38 deduplicated tool records with content-hashed IRIs.
- Benchmark: per-paper tasks + claim-retrieval test sets with silver/gold tiering.

### Known issues (v1.0)

- **`## Examples` section fill rate: 38/106 skills (36%).** Upstream ASB Agent 5 (example-invocation generator) returns empty for the majority of skills when no defensible invocation could be honestly synthesized. Tracked for v1.1 upstream prompt-tuning. The 38 skills with examples are flagged in `_index.md`.
- **Tool license resolution: 16/38 tools resolved (42%).** Remaining 22 tools have `license_source: unresolved` in their YAML; curator fill-in expected before v1.1. See `sbom.cdx.json` for the full inventory.
- **CC-BY attribution per-quote:** quotes within tool `evidence_spans` carry the source paper DOI at the tool level (via `source_paper_doi`), but per-quote DOI attribution is a v1.1+ schema improvement.
- **w3id IRIs not resolving:** `w3id.org/holobiomicslab/asb-*` IRIs appear in artifact `@id` fields but the redirection PR at perma-id/w3id.org is still pending. See README "w3id IRIs" section for the temporary GitHub-raw fallback.
