# Three-output metabarcoding cut fixture

This is a deterministic, public-safe structural cut for collector and corpus-join tests.

## Identity and sources

- Reduced fixture cut ID: `c631e4625159`. This is the first 12 hexadecimal characters of SHA-256 over the exact bytes of `corpus/skills/coverage_summary.json`.
- Parent provisional cut ID: `baa62d4e1c04`.
- Output source: `papers_view_provisional/metabarcoding/corpus/skills/`.
- Build source: `papers_view_provisional/metabarcoding/<run>/` for the three run directories retained under `builds/`.
- Tier source: `asb-corpus-omics/metabarcoding_tiered.json`.
- Corpus-row template: `rehearsal/candidates/metabarcoding/collections/metabarcoding/v1/corpus.yaml`.

## Why this fixture uses metabarcoding and three builds

The plan's multi-omics/two-build wording cannot exercise a merged output because that provisional cut contains no merged output. Metabarcoding has the required `semantic_auto` output with two members from two builds; a third build supplies the independent alignment output. The three-build cut therefore covers merged and single-output joins without changing the intended test surface.

## Fixture-only policy control

All three source rows are CC-BY with permissive reuse. To exercise the P3 path required by D1/D4, only `10.1002/ece3.6594` has `access.source_reuse: restricted` in fixture `corpus.yaml`. Its source-derived access type, access licence, licence tier, and licence subject remain unchanged. This synthetic field value is test control metadata, not a claim about the paper.

## Public-safety reductions

- The tier inventory keeps only the nine allowlisted identity, publication, access, and tier fields; descriptive prose and all other inventory fields are omitted.
- Build manifests keep source schema/build identity plus resolved DOI and repository flags; all other invocation and environment fields are omitted.
- Triage manifests keep only selected source slugs, omit per-row diagnostic narratives, and recompute aggregate counters over retained rows.
- Tool indexes keep only records named by selected variants. External enrichment keeps only Crossref and Unpaywall blocks.
- Markdown publication-summary evidence items and flagged embedded publication-summary passages are removed. Dependent validation claims and summary-provenance markers are removed with them.
- Structurally identified quoted evidence fields longer than 300 characters are shortened to the last sentence boundary at or below 300 characters. A span is removed when no complete sentence fits within the cap. No paper-specific phrase is used by the rule.

## Individual content cuts

| Fixture file | Structural locator | Reason | Original chars | Retained chars | Boundary |
|---|---|---:|---:|---:|---|
| builds/asbb_wave250_2026-09-01__coll_10_1002_ece3_6594_cq/skills/_triage_manifest.json | rows[slug=amplicon-sequence-denoising]/diagnostic-narrative | triage diagnostic narrative | 481 | 0 | removed |
| builds/asbb_wave250_2026-09-01__coll_10_1002_ece3_6594_cq/skills/_triage_manifest.json | rows[slug=amplicon-sequence-denoising]/diagnostic-narrative | triage diagnostic narrative | 650 | 0 | removed |
| builds/asbb_wave250_2026-09-01__coll_10_1002_ece3_6594_cq/skills/_triage_manifest.json | rows[slug=kruskal-wallis-group-comparison]/diagnostic-narrative | triage diagnostic narrative | 411 | 0 | removed |
| builds/asbb_wave250_2026-09-01__coll_10_1002_ece3_6594_cq/skills/_triage_manifest.json | rows[slug=kruskal-wallis-group-comparison]/diagnostic-narrative | triage diagnostic narrative | 1468 | 0 | removed |
| builds/asbb_wave250_2026-09-01__coll_10_1038_s41467_019_13036_1_cq/skills/_triage_manifest.json | rows[slug=16s-amplicon-alignment-to-reference]/diagnostic-narrative | triage diagnostic narrative | 732 | 0 | removed |
| builds/asbb_wave250_2026-09-01__coll_10_1038_s41467_019_13036_1_cq/skills/_triage_manifest.json | rows[slug=16s-amplicon-alignment-to-reference]/diagnostic-narrative | triage diagnostic narrative | 1064 | 0 | removed |
| builds/asbb_wave250_2026-09-01__coll_10_1038_s41598_023_30764_z_cq/skills/_triage_manifest.json | rows[slug=16s-amplicon-sequence-denoising]/diagnostic-narrative | triage diagnostic narrative | 714 | 0 | removed |
| builds/asbb_wave250_2026-09-01__coll_10_1038_s41598_023_30764_z_cq/skills/_triage_manifest.json | rows[slug=16s-amplicon-sequence-denoising]/diagnostic-narrative | triage diagnostic narrative | 1437 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/skill.md | body evidence item at source line 84 | publication-summary evidence | 187 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/claims_checked/0/evidence_quote | quoted evidence span | 408 | 209 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/claims_checked/0/note | publication-summary reference | 246 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/claims_checked/6/evidence_quote | quoted evidence span | 329 | 113 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/claims_checked[7] | summary-dependent validation claim | 587 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/diagnostic-narrative | diagnostic narrative | 1048 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/0/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/0/text | quoted evidence span | 344 | 291 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/1/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/1/text | quoted evidence span | 6013 | 277 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/10/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/10/text | quoted evidence span | 6013 | 91 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/11/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/11/text | quoted evidence span | 6013 | 0 | dropped-no-sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/12/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/12/text | quoted evidence span | 4382 | 10 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/13/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/13/text | quoted evidence span | 5783 | 0 | dropped-no-sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/14/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/14/text | quoted evidence span | 3379 | 173 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/15/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/15/text | quoted evidence span | 3184 | 0 | dropped-no-sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/16/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/16/text | quoted evidence span | 6013 | 0 | dropped-no-sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/17/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/17/text | quoted evidence span | 6013 | 0 | dropped-no-sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/18/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/18/text | quoted evidence span | 6013 | 29 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/19/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/19/text | quoted evidence span | 6013 | 53 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/2/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/2/text | quoted evidence span | 6013 | 159 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/20/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/20/text | quoted evidence span | 6013 | 240 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/21/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/21/text | quoted evidence span | 6013 | 266 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/22/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/22/text | quoted evidence span | 6013 | 33 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/23/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/23/text | quoted evidence span | 6013 | 141 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/24/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/24/text | quoted evidence span | 6013 | 117 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/25/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/25/text | quoted evidence span | 6013 | 186 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/26/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/26/text | quoted evidence span | 6013 | 94 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/27/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/27/text | quoted evidence span | 6013 | 237 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/28/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/28/text | quoted evidence span | 3370 | 261 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/29/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/29/text | quoted evidence span | 869 | 258 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/3/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/3/text | quoted evidence span | 6013 | 199 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/30/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/30/text | quoted evidence span | 1202 | 258 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/31/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/31/text | quoted evidence span | 1202 | 235 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/32/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/32/text | quoted evidence span | 1202 | 116 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/4/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/4/text | quoted evidence span | 6013 | 191 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/5/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/5/text | quoted evidence span | 6013 | 245 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/6/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/6/text | quoted evidence span | 6013 | 280 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/7/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/7/text | quoted evidence span | 6013 | 251 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/8/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/8/text | quoted evidence span | 6013 | 248 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/9/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used/9/text | quoted evidence span | 6013 | 209 | sentence |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json | sidecars/validation.json/passages_used[idx=2] | publication-summary passage | 1098 | 0 | removed |
| corpus/skills/16s-amplicon-alignment-to-reference/variants/16s-amplicon-alignment-to-reference--18725dbbed09898c.json#body | body evidence item at source line 84 | publication-summary evidence | 187 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/skill.md | body evidence item at source line 103 | publication-summary evidence | 177 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/diagnostic-narrative | diagnostic narrative | 1036 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/0/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/0/text | quoted evidence span | 339 | 0 | dropped-no-sentence |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/1/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/1/text | quoted evidence span | 6013 | 177 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/2/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/2/text | quoted evidence span | 6013 | 156 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/3/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/3/text | quoted evidence span | 6013 | 244 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/4/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/4/text | quoted evidence span | 6013 | 297 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/5/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/5/text | quoted evidence span | 3449 | 276 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/6/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/6/text | quoted evidence span | 1202 | 272 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/7/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/7/text | quoted evidence span | 1202 | 172 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/8/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used/8/text | quoted evidence span | 1202 | 258 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json | sidecars/validation.json/passages_used[idx=2] | publication-summary passage | 1881 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/16s-amplicon-sequence-denoising--c91683cbe415cba2.json#body | body evidence item at source line 91 | publication-summary evidence | 103 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/claims_checked/3/evidence_quote | quoted evidence span | 389 | 0 | dropped-no-sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/claims_checked[0] | summary-dependent validation claim | 709 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/diagnostic-narrative | diagnostic narrative | 688 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/0/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/1/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/1/text | quoted evidence span | 6013 | 279 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/10/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/10/text | quoted evidence span | 6013 | 44 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/11/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/11/text | quoted evidence span | 6013 | 176 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/12/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/12/text | quoted evidence span | 6013 | 198 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/13/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/13/text | quoted evidence span | 5422 | 234 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/14/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/14/text | quoted evidence span | 1202 | 264 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/15/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/15/text | quoted evidence span | 1202 | 226 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/16/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/16/text | quoted evidence span | 1202 | 200 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/17/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/17/text | quoted evidence span | 1202 | 187 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/2/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/2/text | quoted evidence span | 6013 | 202 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/3/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/3/text | quoted evidence span | 6013 | 227 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/4/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/4/text | quoted evidence span | 6013 | 217 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/5/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/5/text | quoted evidence span | 6013 | 177 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/6/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/6/text | quoted evidence span | 6013 | 14 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/7/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/7/text | quoted evidence span | 6013 | 230 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/8/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/8/text | quoted evidence span | 6013 | 47 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/9/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used/9/text | quoted evidence span | 6013 | 166 | sentence |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json | sidecars/validation.json/passages_used[idx=2] | publication-summary passage | 1788 | 0 | removed |
| corpus/skills/amplicon-sequence-denoising/variants/amplicon-sequence-denoising--b4da862147ad46d2.json#body | body evidence item at source line 103 | publication-summary evidence | 177 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/skill.md | body evidence item at source line 98 | publication-summary evidence | 177 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/claims_checked/0/evidence_quote | quoted evidence span | 545 | 254 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/claims_checked/1/evidence_quote | quoted evidence span | 363 | 278 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/claims_checked/4/evidence_quote | quoted evidence span | 427 | 291 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/claims_checked/8/evidence_quote | quoted evidence span | 434 | 296 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/diagnostic-narrative | diagnostic narrative | 411 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/0/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/1/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/1/text | quoted evidence span | 6013 | 279 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/10/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/10/text | quoted evidence span | 6013 | 44 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/11/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/11/text | quoted evidence span | 6013 | 176 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/12/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/12/text | quoted evidence span | 6013 | 198 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/13/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/13/text | quoted evidence span | 5422 | 234 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/14/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/14/text | quoted evidence span | 1202 | 226 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/15/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/15/text | quoted evidence span | 634 | 133 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/16/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/16/text | quoted evidence span | 1202 | 200 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/17/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/17/text | quoted evidence span | 1202 | 187 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/2/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/2/text | quoted evidence span | 6013 | 202 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/3/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/3/text | quoted evidence span | 6013 | 227 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/4/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/4/text | quoted evidence span | 6013 | 217 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/5/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/5/text | quoted evidence span | 6013 | 177 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/6/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/6/text | quoted evidence span | 6013 | 14 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/7/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/7/text | quoted evidence span | 6013 | 230 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/8/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/8/text | quoted evidence span | 6013 | 47 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/9/publication-summary-marker | publication-summary marker | 1 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used/9/text | quoted evidence span | 6013 | 166 | sentence |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json | sidecars/validation.json/passages_used[idx=2] | publication-summary passage | 1788 | 0 | removed |
| corpus/skills/kruskal-wallis-group-comparison--4f3b5102cc625c23/variants/kruskal-wallis-group-comparison--865f6b27b9caecbd.json#body | body evidence item at source line 98 | publication-summary evidence | 177 | 0 | removed |

## Selected outputs

- `16s-amplicon-alignment-to-reference`: `single`, 1 source member(s).
- `amplicon-sequence-denoising`: `semantic_auto`, 2 source member(s).
- `kruskal-wallis-group-comparison--4f3b5102cc625c23`: `single`, 1 source member(s).
