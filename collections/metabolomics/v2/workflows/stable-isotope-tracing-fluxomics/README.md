# stable-isotope-tracing-fluxomics-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **preprocess** — raw labelled LC-MS -> aligned feature table (all isotopologues)  →  `peak-detection-and-mass-alignment`, `mass-spectral-feature-alignment`, `lcms-peak-detection-and-alignment`, `isotope-labeling-data-integration`, `mass-isotopologue-adduct-grouping`
2. **isotopologue_extract** — feature table -> per-metabolite isotopologue intensity distributions  →  `isotope-labelling-feature-interpretation`, `metabolite-feature-grouping-by-adduct-isotope`, `isotopologue-signature-detection`
3. **natural_abundance_correction** — correct isotopologue distributions for natural isotope abundance  →  `isotopic-impurity-accounting`, `tracer-impurity-correction-modeling`, `natural-isotope-abundance-propagation`, `naturally-occurring-isotope-contribution-accounting`, `isotopologue-distribution-matrix-construction`
4. **labelling_analysis** — corrected distributions -> mass-isotopomer distribution / fractional enrichment  →  `stable-isotope-labeling-quantification`, `fractional-abundance-transformation`, `metabolite-fold-change-statistical-testing`
5. **report** — consolidate labelling / enrichment results into a tracing report table  →  `metabolite-abundance-normalization-across-conditions`, `tab-delimited-export-formatting-for-metabolomics`, `stable-isotope-labelling-feature-detection`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
