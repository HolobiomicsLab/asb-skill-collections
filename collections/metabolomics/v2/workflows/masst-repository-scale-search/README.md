# masst-repository-scale-search-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **spectrum_prep** — prepare a query MS/MS spectrum / USI for search  →  `usi-spectrum-retrieval-and-loading`, `spectral-data-loading-from-repository`, `usi-namespace-parsing`, `usi-string-parsing-and-resolution`, `usi-spectrum-identifier-encoding`
2. **masst_search** — repository-scale spectral search (fastMASST)  →  `spectral-database-query-execution`, `spectral-match-result-consolidation`, `mass-spectrometry-database-search`, `mass-spectrometry-reference-database-integration`, `spectral-match-interpretation`
3. **specialized_masst** (optional) — (optional) ecological context via microbe/plant/food MASST  →  `domain-specific-spectrum-search-implementation`, `masst-output-visualization`, `multi-domain-search-result-aggregation`, `metadata-harmonization-across-sources`
4. **cooccurrence** — co-occurrence / reverse-metabolomics interpretation  →  `metabolite-metadata-integration`, `sample-centric-metabolite-annotation`, `tandem-mass-spectrometry-metadata-standardization`, `ms-ms-spectral-library-matching`, `compound-database-matching`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
