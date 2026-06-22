---
name: ms2-spectral-library-matching-post-denoising
description: 'Use when after frequency-based denoising of MS/MS spectra, when you need to validate that denoising improves metabolite identifications and quantify the trade-off between signal retention and annotation confidence. Specifically: (1) you have denoised MS/MS spectra from replicate measurements;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - rPref
  - DEoptim
  - dplyr
  - ggplot2
  - pbapply
  - magrittr
  - stats
  - data.table
  - Spectra
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra", "BiocManager", "knitr", "markdown"),
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dures_cq
    doi: 10.1021/acs.analchem.5c01726
    title: DuReS
  dedup_kept_from: coll_dures_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01726
  all_source_dois:
  - 10.1021/acs.analchem.5c01726
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS/MS Spectral Library Matching Post-Denoising

## Summary

Match experimental denoised MS/MS spectra against a curated reference library using modified dot product and fragment matching metrics to assign metabolite annotations with confidence filtering. This skill applies after denoising to evaluate whether noise removal improves spectral similarity and annotation quality.

## When to use

After frequency-based denoising of MS/MS spectra, when you need to validate that denoising improves metabolite identifications and quantify the trade-off between signal retention and annotation confidence. Specifically: (1) you have denoised MS/MS spectra from replicate measurements; (2) you want to compare matching scores before and after denoising; (3) you need to filter low-confidence matches using fragment count and dot product thresholds; and (4) you require annotation reproducibility across replicates (≥30% occurrence).

## When NOT to use

- Input spectra are already heavily denoised by vendor software or external tools — library matching cannot validate further gains.
- Reference library is not pre-processed consistently with experimental spectra (e.g., different fragmentation protocols, mass calibration, or precursor ion filtering).
- Sample has <2 replicates — the ≥30% replicate occurrence filter cannot be reliably applied.

## Inputs

- Denoised MS/MS spectra (mzML format) with labeled fragment frequencies
- Best-matching reference spectra from pre-denoising matching (for before/after comparison)
- Curated reference spectral library (positive and negative ionization modes, 1,259,372 unique spectra across 356,330 compounds)
- Feature metadata (precursor m/z, RT, number of replicates)

## Outputs

- CSV files of all evaluated matches per feature (matching scores, dot products, fragment counts, before/after metrics)
- Filtered dataframe containing: optimal frequency threshold, similarity scores pre/post-denoising, signal/noise reduction metrics, fragment match rates, matched compound identifiers
- Pareto front plots per feature (signal retention vs. noise reduction trade-offs)
- Summary table with annotated features meeting confidence criteria (≥2 fragments, dot product ≥0.25, ≥30% replicate occurrence)

## How to apply

For each denoised spectrum, compute a modified dot product against all reference library spectra, then apply the matching score formula: 5 × [Modified Dot Product × 100 + 20 × log₂(max(NMF, 1))], where NMF is the number of matching fragments. Filter matches requiring: (a) ≥2 matching fragments, (b) dot product ≥0.25, and (c) occurrence in ≥30% of replicate spectra for a feature. Compare similarity scores, fragment match rates, and matching counts before and after denoising; retain features with improved scores and positive signal retention. Calculate percentage improvement in matching score and generate results tables and Pareto front analysis plots to visualize trade-offs between denoising stringency and annotation quality.

## Related tools

- **rPref** (Identifies Pareto front of optimal trade-offs between signal retention and noise reduction across frequency thresholds and features)
- **DEoptim** (Backup differential evolution optimization method when Pareto front analysis alone is insufficient to identify optimal threshold)
- **dplyr** (Data wrangling and filtering of matched spectra, merging results tables, and extracting features meeting confidence criteria) — https://github.com/tidyverse/dplyr
- **ggplot2** (Visualization of Pareto front plots per feature and matching score distributions before/after denoising) — https://github.com/tidyverse/ggplot2
- **data.table** (Fast aggregation and subsetting of large matching result sets during threshold evaluation) — https://github.com/Rdatatable/data.table
- **pbapply** (Parallel iteration over matched features to apply matching score calculation and filtering in batches)
- **Spectra** (Representation and manipulation of experimental and reference MS/MS spectra objects) — https://bioconductor.org/packages/Spectra

## Examples

```
# Pseudo-R: After generating l5 denoised spectra, match against library and evaluate improvement
l6_matches <- match_and_score_library(
  denoised_spectra = l5,
  reference_library = library_positive.rds,
  min_fragments = 2,
  min_dot_product = 0.25,
  replicate_occurrence_threshold = 0.30,
  output_dir = "pareto_results/"
)
```

## Evaluation signals

- Matching score improvement (percentage gain) is positive for features passing filtering; at least some denoised spectra show higher similarity to reference library than raw spectra.
- Fragment match rate increases or remains stable post-denoising (signal not disproportionately lost); unmatched fragment count decreases.
- At least 30% of replicate spectra for each annotated feature pass the matching confidence thresholds (≥2 fragments, dot product ≥0.25).
- Pareto front plots show a clear trade-off surface; selected threshold lies on the front, not dominated by other thresholds in both signal retention and noise reduction dimensions.
- Filtered output dataframe contains consistent columns with no missing values in signal/noise metrics; all matched compound identifiers are resolvable to the reference library.

## Limitations

- Matching quality depends critically on reference library completeness and consistency; compounds absent from or poorly represented in the library will not be identified regardless of denoising quality.
- The ≥30% replicate occurrence threshold may exclude genuine low-abundance metabolites that appear sporadically across replicates.
- Modified dot product metric assumes similar fragmentation patterns across instruments and ionization conditions; transferability to different MS platforms may be limited.
- Pareto front analysis assumes that signal retention and noise reduction are the only two competing objectives; other quality dimensions (e.g., spectral entropy, isotope pattern fidelity) are not explicitly optimized.

## Evidence

- [methods] Match all thresholded spectra against the best-matching reference spectrum (identified before denoising in l6) using dot product-based metrics and fragment match rates: "Match all thresholded spectra against the best-matching reference spectrum (identified before denoising in l6) using dot product-based metrics and fragment match rates"
- [readme] Matching Score = 5 × [Modified Dot Product × 100 + 20 × log₂(max(NMF, 1))]: "Matching Score = 5 × [Modified Dot Product × 100 + 20 × log₂(max(NMF, 1))]"
- [readme] Matches with fewer than 2 fragments or dot products < 0.25 are filtered out; Annotations must occur in ≥30% of replicate spectra: "Matches with fewer than 2 fragments or dot products < 0.25 are filtered out; Annotations must occur in ≥30% of replicate spectra"
- [methods] Filter features showing improved similarity scores post-denoising with positive signal retention and compute percentage improvement: "Filter features showing improved similarity scores post-denoising with positive signal retention and compute percentage improvement"
- [readme] The curated reference spectral libraries comprise 1,259,372 unique spectra across 356,330 unique compounds with coverage in both positive and negative ionization modes: "1,259,372 unique spectra and 356,330 unique compounds with Coverage across both positive and negative ionization modes"
- [methods] Generate CSV files of all evaluated matches in pareto_results/csv/ and Pareto front plots per feature in pareto_results/pdf/: "Generate CSV files of all evaluated matches in pareto_results/csv/ and Pareto front plots per feature in pareto_results/pdf/"
- [methods] Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each threshold: "Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each threshold"
