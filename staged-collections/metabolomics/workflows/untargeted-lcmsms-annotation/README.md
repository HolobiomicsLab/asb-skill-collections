# untargeted-lcmsms-annotation-workflow — STAGING (v2)

**Status:** STAGING ONLY — not yet in `collections/metabolomics/v2/`. Promote via
`release_gate.py` after human review.

**Kind:** composite-workflow (P0 pilot, SPEC §10)

**Version:** v2 — semantic binding via Perspicacité embedding model
(text-embedding-3-large) + LLM judge. v1 (index binding) archived at
`../_archive/untargeted-lcmsms-annotation.v1-index` for A/B comparison.

**Goal:** End-to-end untargeted LC-MS/MS annotation: raw mzML in, annotated master
feature table out. Six stages: preprocess, network, library_match, sirius,
taxonomy_propagate (optional), fusion.

---

## What changed from v1 to v2

| Stage | v1 primary (index-bound) | v2 primary (semantic-bound) | Fix |
|-------|--------------------------|------------------------------|-----|
| preprocess | `peak-detection-and-mass-alignment` | `peak-detection-and-mass-alignment` | Kept; now adds 4 LC-MS-specific support skills (NeatMS, pyOpenMS, XCMS, ISFrag) |
| network | `spectral-similarity-scoring-cosine` | `spectral-similarity-network-generation` | Fixed: v1 primary was a scoring primitive shared with library_match; v2 uses a dedicated GRAPH-building skill |
| library_match | `spectral-similarity-scoring-cosine` | `spectral-library-matching` | Fixed: v1 shared the same primary as network; v2 uses a distinct REFERENCE LIBRARY search skill covering GNPS/MASSBANK/MASST |
| sirius | `sirius-spectral-request-construction` | `sirius-spectral-request-construction` | Kept; now adds MSNovelist de-novo, Zodiac filter, fingerprint query |
| taxonomy_propagate | `metabolite-annotation-scoring` | `metabolite-annotation-taxonomic-integration` | Reordered: taxonomic-integration is the entry point; scoring is a downstream step |
| fusion | `inchikey-normalization-and-deduplication` | `mass-spectrometry-feature-deduplication` | Fixed: v1 primary was not in the semantic pool; v2 uses MolNotator-based deduplication |

Key fixes:
- **Cross-stage collision removed:** `spectral-similarity-scoring-cosine` no longer
  appears in two stages simultaneously.
- **GC-MS leaves dropped from network:** v1 included `gc-ms-spectral-similarity-clustering`
  and `spectral-batch-submission-to-networking-server` (both GC-MS primary); v2 uses
  only LC-MS-technique leaves.
- **Script filenames removed from tools:** `jobs.py`, `smiles.py`, `sanitizing.py`,
  `prepare_wikidata_lotus_prefect.py`, `drugbank_extraction.py` dropped from
  `member_tools`.
- **Near-duplicate tools consolidated:** SIRIUS/SIRIUS v5/v6/SIRIUS (v5/v6) → SIRIUS;
  LOTUS/(Natural Products Database) → LOTUS; tima variants → canonical form.

---

## Derived from workflows (eval-ablation list)

The following benchmark builds contributed structure to this super-skill. The eval
harness ablates these items when scoring agents that have this super-skill installed
(SPEC §8 benchmark integrity):

`coll_ms2deepscore`, `coll_ramclust_cq`, `coll_xcms_cq`, `coll_inventa_cq`,
`coll_nmr2struct`, `spec2vec_grounded`, `spec2vec_pkg_oalarge`,
`coll_bioactivity_based_molecular_networking_cq`, `coll_concise_cq`, `coll_redu_cq`,
`coll_deepmsprofiler_cq`, `coll_cardinal_cq`, `coll_dures_cq`, `coll_fbmn_stats_cq`,
`coll_idsl_ipa_cq`, `coll_metabodirect`, `coll_multiomicsintegrator_cq`,
`coll_peakqc_cq`, `coll_tardis`, `coll_vimms`, `coll_lipidin_cq`,
`coll_molnetenhancer`, `coll_ms2rescore_immunopeptidome_rescoring_cq`,
`coll_npclassscore_cq`, `coll_rapidmass_cq`, `coll_tardis_cq`, `coll_esp_cq`,
`coll_graphormer_rt_cq`, `coll_lipidmatch_cq`, `coll_corems`

---

## How to ground a stage

Stages carry `grounding.kb_slugs` and `grounding.dois` pointing to their source
papers in the ASB metabolomics v2 KB. To ground a stage against its source paper:

```bash
# With Perspicacité server running on :8002
/ground stage=preprocess     kb=asb-paper-10-1021-acs-jnatprod-7b00737
/ground stage=network        kb=asb-paper-10-1038-s41596-024-01046-3
/ground stage=library_match  kb=asb-paper-10-1038-s41538-022-00137-3
/ground stage=sirius         kb=asb-paper-10-1038-s41587-021-01045-9
/ground stage=taxonomy_propagate kb=asb-paper-10-3389-fpls-2019-01329
/ground stage=fusion         kb=asb-paper-10-1021-acs-analchem-2c05810

# Without server — offline keyword search over skills_index.json
asb solve-workflow --ground-only workflow.yaml --stage preprocess
```

The `taxonomy_propagate` stage is **optional**: set `optional: true` in workflow.yaml
and skip it when no organism taxonomy metadata is available.

---

## Binding provenance

Stages were bound in v2 via **semantic retrieval** (Perspicacité
text-embedding-3-large + LLM judge) using the top-12 candidates per stage from
`.semantic_pools.json`. Selection criteria applied:

1. **Platform filter**: prefer LC-MS technique leaves; drop pure GC-MS / CE-MS /
   NMR / direct-infusion-only unless platform-agnostic.
2. **Task distinctness**: `network` and `library_match` must not share primary
   leaves; no slug appears in more than one stage.
3. **Quality**: prefer higher semantic scores; avoid near-duplicate leaves within
   a stage.

To re-bind with updated Perspicacité pools:

```bash
asb bind-workflow workflow.yaml --perspicacite http://localhost:8002 --rewrite
```
