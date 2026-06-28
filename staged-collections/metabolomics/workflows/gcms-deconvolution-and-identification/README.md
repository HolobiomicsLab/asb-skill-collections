# gcms-deconvolution-identification-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + deterministic selection).

## Stages

1. **deconvolution** — GC-MS EI spectral deconvolution + peak detection  →  `gc-ms-spectral-deconvolution`, `gcms-spectrum-deconvolution`, `pure-component-spectrum-extraction`, `mass-spectral-component-extraction`, `deconvolved-spectrum-comparison`
2. **ei_library_match** — identify compounds by EI spectral library matching  →  `electron-ionization-spectral-comparison`, `spectral-similarity-scoring-ei-simple`, `gc-ms-spectral-library-matching`, `mass-spectrometry-network-construction`
3. **retention_index** — retention index calibration + RI-filtered identifications  →  `retention-index-calibration-application`, `retention-index-assignment-and-filtering`, `low-resolution-compound-identification`, `gc-column-polarity-specific-ri-filtering`, `kovats-retention-index-extraction-and-assignment`
4. **statistics** — differential GC-MS feature analysis between groups  →  `group-comparison-statistics`, `gc-ms-data-preprocessing-and-normalization`, `gcxgc-ms-multivariate-analysis`, `univariate-statistical-testing-for-metabolomics`, `permanova-statistical-testing-multivariate-groups`
5. **fusion** — consolidate GC-MS identifications + stats into a master table  →  `feature-consolidation-across-samples`, `mass-spectrometry-feature-grouping`, `feature-table-matrix-assembly`, `feature-alignment-metabolomics`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
