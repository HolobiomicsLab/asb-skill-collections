# gcms-deconvolution-identification-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **deconvolution** — GC-MS EI spectral deconvolution + peak detection  →  `gcms-spectrum-deconvolution`, `gc-ms-spectral-deconvolution`, `pure-component-spectrum-extraction`, `mass-spectral-component-extraction`, `deconvolved-spectrum-comparison`
2. **ei_library_match** — identify compounds by EI spectral library matching  →  `gc-ms-spectral-library-matching`, `low-resolution-compound-identification`, `electron-ionization-spectral-comparison`, `spectral-similarity-scoring-ei-simple`, `spectral-library-molecular-networking`
3. **retention_index** — retention index calibration + RI-filtered identifications  →  `mass-spectrometry-column-polarity-filtering`, `retention-index-calibration-application`, `retention-index-assignment-and-filtering`, `gc-column-polarity-specific-ri-filtering`, `kovats-retention-index-extraction-and-assignment`
4. **statistics** — differential GC-MS feature analysis between groups  →  `group-comparison-statistics`, `gc-ms-data-preprocessing-and-normalization`, `univariate-statistical-testing-for-metabolomics`, `permanova-statistical-testing-multivariate-groups`
5. **fusion** — consolidate GC-MS identifications + stats into a master table  →  `compound-area-aggregation-across-samples`, `mass-spectrometry-feature-grouping`, `feature-alignment-metabolomics`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
