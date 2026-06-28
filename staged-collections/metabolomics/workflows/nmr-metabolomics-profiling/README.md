# nmr-metabolomics-profiling-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + deterministic selection).

## Stages

1. **preprocess_nmr** — NMR spectral preprocessing (phase, baseline, referencing, binning)  →  `nmr-spectral-preprocessing-and-phasing`, `nmr-workflow-pipeline-execution`, `nmr-spectra-preprocessing`, `metabolite-dataset-preprocessing`
2. **identification** — identify metabolites by chemical shift matching  →  `metabolite-peak-assignment-from-nmr`, `nmr-metabolite-identity-confirmation`, `nmr-chemical-shift-interval-matching`, `hmdb-metabolite-query-and-retrieval`
3. **quantification** — quantify metabolites from NMR signals  →  `nmr-peak-deconvolution`, `compound-abundance-quantification-from-flow`, `nmr-peak-table-generation`
4. **statistics** — multivariate + differential analysis of NMR profiles  →  `univariate-statistical-testing-for-metabolomics`, `multiple-testing-correction-metabolomics`, `group-comparison-statistics`, `multicontrast-statistical-testing-lipidomics`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
