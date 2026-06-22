---
name: missing-value-detection-and-quantification
description: Use when you have a raw abundance matrix (e.g., metabolite or gene features × samples) and need to decide which features to retain before downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - R
  - MSPrep
  - Bioconductor
  - marr
derived_from:
- doi: 10.1186/s12859-021-04336-9
  title: marr
- doi: 10.1080/01621459.2017.1397521
  title: ''
evidence_spans:
- 'marr: An R/Bioconductor package for Maximum Rank Reproducibility'
- The R-package **marr** can be installed from GitHub using the R package [devtools]
- The **msprepCOPD** data in the **marr** package was pre-processed using the MSPrep software
- '`marr`: An R/Bioconductor package for Maximum Rank Reproducibility'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_marr_cq
    doi: 10.1186/s12859-021-04336-9
    title: marr
  dedup_kept_from: coll_marr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-021-04336-9
  all_source_dois:
  - 10.1186/s12859-021-04336-9
  - 10.1080/01621459.2017.1397521
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# missing-value-detection-and-quantification

## Summary

Systematically identify and quantify missing values (NA or zero) across features in high-dimensional replicate experiments to inform feature filtering decisions. This skill enables practitioners to characterize missingness patterns and apply data-driven retention thresholds.

## When to use

Apply this skill when you have a raw abundance matrix (e.g., metabolite or gene features × samples) and need to decide which features to retain before downstream analysis. Particularly critical in high-throughput MS-metabolomics or similar replicate experiments where technical or biological variability may produce sparse or incomplete feature detection across samples.

## When NOT to use

- Input is already a quality-controlled or pre-filtered feature table (e.g., post-MSPrep output) — skip this step to avoid redundant filtering.
- Missingness is structurally informative (e.g., missingness-at-random by design or indicates biological absence) — blanket removal may discard interpretable signal.
- Sample count is very small (< 5 replicates) — missingness thresholds become unstable and may remove most features; consider alternative imputation or relaxed thresholds.

## Inputs

- Raw abundance matrix (features × samples) as R data frame, matrix, or SummarizedExperiment assay object
- Sample count (number of replicates)
- Missingness representation convention (NA or zero)

## Outputs

- Per-feature missingness count (absolute number of missing values)
- Per-feature missingness proportion (percentage or fraction missing)
- Feature retention decision vector (logical or binary: retain vs. remove)
- Summary statistics: raw feature count, filtered feature count, count and percentage of features removed

## How to apply

Load the raw abundance matrix (e.g., as a SummarizedExperiment object or data frame with features as rows and samples as columns). For each feature, calculate the proportion of missing values (NA or zero, following the preprocessing convention of your data source) across all samples. Document the absolute count and percentage of missing values per feature. Use this quantification to apply a missingness threshold—commonly 80% in metabolomics workflows—to identify features for retention or removal. The rationale is that features with excessive missingness (present in fewer than the minimum viable sample count) lack sufficient signal for reliable statistical inference across replicates and contribute noise rather than information. Document the feature count before and after filtering as a transparency measure and sanity check.

## Related tools

- **MSPrep** (Pre-processing software that implements the 80% missingness filtering step on raw metabolite abundance matrices)
- **R** (Programming language for loading, calculating missingness statistics, and applying retention thresholds)
- **Bioconductor** (R ecosystem providing SummarizedExperiment container and downstream analysis infrastructure)
- **marr** (R/Bioconductor package that loads pre-filtered metabolomics data (msprepCOPD SummarizedExperiment) after missingness-based feature filtering has been applied) — https://github.com/Ghoshlab/marr

## Examples

```
# Load raw metabolite abundance matrix (662 features × 20 replicates) and calculate missingness per feature
missing_counts <- colSums(is.na(abundance_matrix))
missing_props <- missing_counts / nrow(abundance_matrix)
retained <- which(missing_props <= 0.80)
filtered_matrix <- abundance_matrix[, retained]
cat('Removed:', ncol(abundance_matrix) - length(retained), 'features;', 'Retained:', length(retained), '\n')
```

## Evaluation signals

- Missingness proportions for all features sum to valid ranges (0.0 to 1.0 per feature); no NaN or negative values.
- Feature counts before and after filtering are documented and the difference is non-negative (filtered ≤ raw).
- For a standard 80% missingness threshold on 20 replicates, expect features retained if present in ≥4 samples; verify a representative sample of removed features have >16 missing values.
- The filtering step reduces raw feature count from 662 to 645 (17 features removed, ~2.6%) in the msprepCOPD dataset; significant deviations suggest miscalculation or threshold mismatch.
- All retained features pass the missingness criterion uniformly; no features below the threshold remain in the output matrix.

## Limitations

- Threshold selection (e.g., 80%) is dataset- and domain-specific; no universal cutoff suits all experiments. Validation against biological or technical replicates is recommended.
- Zero-based missingness imputation may conflate true absences (biological or technical non-detection) with actual missing values (failed measurement); preprocessing convention must be documented.
- Extreme feature sparsity (e.g., >95% missingness across all features) may indicate inadequate sample depth, instrument failure, or poor experimental design; filtering alone cannot recover lost signal.
- Missingness patterns correlated with sample groups (e.g., all missing values in one treatment arm) may indicate batch effects or systematic technical bias; filtering removes features without addressing root cause.

## Evidence

- [other] Calculate the proportion of missing values (NA or zero, depending on MSPrep convention) for each metabolite across all samples.: "Calculate the proportion of missing values (NA or zero, depending on MSPrep convention) for each metabolite across all 20 samples."
- [other] Identify and retain only metabolites with ≤80% missingness (i.e., present in ≥20% of samples, or equivalently ≥4 of 20 samples).: "Identify and retain only metabolites with ≤80% missingness (i.e., present in ≥20% of samples, or equivalently ≥4 of 20 samples)."
- [other] The MSPrep filtering step removes metabolites exceeding 80% missingness, reducing the raw metabolite count from 662 to 645 (a loss of 17 metabolites or 2.6% of features).: "The MSPrep filtering step removes metabolites exceeding 80% missingness, reducing the raw metabolite count from 662 to 645 (a loss of 17 metabolites or 2.6% of features)."
- [intro] Filtering: Metabolites are removed if they are missing more than 80% of the samples: "Filtering: Metabolites are removed if they are missing more than 80% of the samples"
- [readme] The marr package contains a pre-processed data SummarizedExperiment assay object of 645 metabolites (features) measured in plasma and 20 biological replicates: "The **marr** package contains a pre-processed data `SummarizedExperiment` assay object of 645 metabolites (features) measured in plasma and 20 biological replicates"
