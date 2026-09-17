# nmr-metabolomics-profiling-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **preprocess_nmr** — NMR spectral preprocessing (phase, baseline, referencing, binning)  →  `nmr-spectral-preprocessing-and-phasing`, `nmr-workflow-pipeline-execution`, `nmr-spectra-preprocessing`, `metabolite-dataset-preprocessing`
2. **identification** — identify metabolites by chemical shift matching  →  `metabolite-peak-assignment-from-nmr`, `nmr-metabolite-identity-confirmation`, `nmr-chemical-shift-interval-matching`, `hmdb-metabolite-query-and-retrieval`
3. **quantification** — quantify metabolites from NMR signals  →  `nmr-peak-deconvolution`, `compound-abundance-quantification-from-flow`, `nmr-peak-table-generation`
4. **statistics** — differential analysis of NMR profiles (univariate; multivariate where a leaf exists)  →  `multiple-testing-correction-metabolomics`, `confounder-adjustment-epidemiological-analysis`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
