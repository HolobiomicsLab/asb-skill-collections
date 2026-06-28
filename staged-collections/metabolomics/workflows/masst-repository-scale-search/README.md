# masst-repository-scale-search-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + deterministic selection).

## Stages

1. **spectrum_prep** — prepare a query MS/MS spectrum / USI for search  →  `spectral-data-loading-from-repository`, `usi-namespace-parsing`, `usi-spectrum-retrieval-and-loading`, `usi-string-parsing-and-resolution`, `usi-spectrum-identifier-encoding`
2. **masst_search** — repository-scale spectral search (fastMASST)  →  `spectral-match-result-consolidation`, `mass-spectrometry-database-search`, `mass-spectrometry-reference-database-integration`
3. **specialized_masst** (optional) — (optional) ecological context via microbe/plant/food MASST  →  `spectral-match-interpretation`, `domain-specific-spectrum-search-implementation`, `masst-output-visualization`, `multi-domain-search-result-aggregation`
4. **cooccurrence** — co-occurrence / reverse-metabolomics interpretation  →  `mass-spectrometry-metadata-interpretation`, `metabolite-metadata-integration`, `sample-centric-metabolite-annotation`, `tandem-mass-spectrometry-metadata-standardization`, `ms-ms-spectral-library-matching`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
