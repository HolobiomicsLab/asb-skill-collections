# masst-repository-scale-search-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **spectrum_prep** — prepare a query MS/MS spectrum / USI for search  →  `usi-spectrum-retrieval-and-loading`, `spectral-data-loading-from-repository`, `usi-namespace-parsing`, `usi-string-parsing-and-resolution`, `usi-spectrum-identifier-encoding`
2. **masst_search** — repository-scale spectral search (fastMASST)  →  `spectral-database-query-execution`, `spectral-match-result-consolidation`, `mass-spectrometry-database-search`, `mass-spectrometry-reference-database-integration`, `spectral-match-interpretation`
3. **specialized_masst** (optional) — (optional) ecological context via microbe/plant/food MASST  →  `domain-specific-spectrum-search-implementation`, `masst-output-visualization`, `multi-domain-search-result-aggregation`, `metadata-harmonization-across-sources`
4. **cooccurrence** — co-occurrence / reverse-metabolomics interpretation  →  `metabolite-metadata-integration`, `sample-centric-metabolite-annotation`, `tandem-mass-spectrometry-metadata-standardization`, `ms-ms-spectral-library-matching`, `compound-database-matching`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
