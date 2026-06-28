# untargeted-lcmsms-annotation-workflow — STAGING

**Status:** STAGING ONLY — not yet in `collections/metabolomics/v2/`. Promote via
`release_gate.py` after human review.

**Kind:** composite-workflow (P0 pilot, SPEC §10)

**Goal:** End-to-end untargeted LC-MS/MS annotation: raw mzML in, annotated master
feature table out. Six stages: preprocess, network, library_match, sirius,
taxonomy_propagate (optional), fusion.

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
/ground stage=preprocess kb=asb-paper-10-1021-acs-jnatprod-7b00737

# Without server — offline keyword search over skills_index.json
asb solve-workflow --ground-only workflow.yaml --stage preprocess
```

The `taxonomy_propagate` stage is **optional**: set `optional: true` in workflow.yaml
and skip it when no organism taxonomy metadata is available.

---

## Binding provenance

Stages were bound via **index** fallback (Perspicacité server unreachable at
authoring time). Re-bind with Perspicacité for semantic-quality improvements:

```bash
asb bind-workflow workflow.yaml --perspicacite http://localhost:8002 --rewrite
```
