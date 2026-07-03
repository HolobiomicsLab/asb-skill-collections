# stable-isotope-tracing-fluxomics-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **preprocess** — raw labelled LC-MS -> aligned feature table (all isotopologues)  →  `peak-detection-and-mass-alignment`, `lcims-msms-data-preprocessing-peak-detection`, `mass-spectral-feature-alignment`, `lcms-peak-detection-and-alignment`, `isotope-labeling-data-integration`
2. **isotopologue_extract** — feature table -> per-metabolite isotopologue intensity distributions  →  `isotope-labelling-feature-interpretation`, `metabolite-feature-grouping-by-adduct-isotope`, `isotopologue-signature-detection`
3. **natural_abundance_correction** — correct isotopologue distributions for natural isotope abundance  →  `isotopic-impurity-accounting`, `tracer-impurity-correction-modeling`, `natural-isotope-abundance-propagation`, `naturally-occurring-isotope-contribution-accounting`, `isotopologue-distribution-matrix-construction`
4. **labelling_analysis** — corrected distributions -> mass-isotopomer distribution / fractional enrichment  →  `stable-isotope-labeling-quantification`, `fractional-abundance-transformation`, `stable-isotope-labelling-feature-detection`
5. **report** — consolidate labelling / enrichment results into a tracing report table  →  `metabolite-abundance-normalization-across-conditions`, `feature-consolidation-across-batches`, `retention-time-mass-tolerance-calibration`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
