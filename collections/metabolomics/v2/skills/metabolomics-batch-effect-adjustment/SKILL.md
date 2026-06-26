---
name: metabolomics-batch-effect-adjustment
description: Use when you have a log-transformed metabolomics featuredata matrix with
  missing values handled (via knn or replacement) and you observe systematic variation
  across batches, quality control samples, or sample order that is NOT of biological
  interest.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NormalizeMets
  - NormQcmets
  - RlaPlots
  - PcaPlots
  - LogTransform
  - MissingValues
  - LinearModelFit
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive
  Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_normalizemets_cq
    doi: 10.1007/s11306-018-1347-7
    title: NormalizeMets
  dedup_kept_from: coll_normalizemets_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-018-1347-7
  all_source_dois:
  - 10.1007/s11306-018-1347-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-batch-effect-adjustment

## Summary

Apply statistical normalization methods to metabolomics feature matrices to remove unwanted variation from batch effects, matrix effects, and instrumental drift, enabling valid downstream biomarker discovery and classification. This skill selects and executes one or more normalization approaches (IS, NOMIS, CCMN, RUV2, RUVrand, RLSC) appropriate to the sources of variation in the dataset.

## When to use

Apply this skill when you have a log-transformed metabolomics featuredata matrix with missing values handled (via knn or replacement) and you observe systematic variation across batches, quality control samples, or sample order that is NOT of biological interest. Triggers include: (1) RLA plots showing within-group median relative log abundances far from zero, (2) PCA plots where technical factors (batch, run order) separate samples more strongly than biological factors of interest, (3) quality control metabolites showing drift or clustering by acquisition date, or (4) planning downstream biomarker identification where confounding batch structure could inflate false positives.

## When NOT to use

- Data are already normalized or do not show batch/technical structure detectable in RLA or PCA plots.
- Missing values have not been handled; call MissingValues() first to impute or remove NAs.
- Input is not log-transformed; call LogTransform() before normalization to stabilize variance.

## Inputs

- featuredata matrix (samples × metabolites, log-transformed, missing values imputed)
- sampledata dataframe (sample-level metadata: batch, run order, QC status, factors of interest)
- metabolitedata dataframe (metabolite-level annotations, optional: internal/external standard flags)
- groupdata vector or factor (sample grouping for diagnostic plots)

## Outputs

- normalized featuredata matrix (same dimensions, adjusted for batch/technical variation)
- normalization object containing model parameters and residuals
- diagnostic plots (RLA plots, PCA plots) showing pre- and post-adjustment structure

## How to apply

Load the log-transformed featuredata matrix (samples × metabolites) and construct a factors dataframe encoding batch, run order, or QC sample status. Choose a normalization method by assessing quality control metabolite behavior and between-batch variance using diagnostic plots (RLA, PCA). Call NormQcmets() with the selected method (e.g., 'rlsc' for run-order drift, 'ruv2' with empirical k for unwanted variation removal, 'ccmn' for cross-sample normalization) and optional parameters (span, deg for RLSC; k, qcmets for RUV2). Extract the normalized featuredata matrix from the output object. Validate normalization by re-plotting RLA and PCA on the adjusted data to confirm batch structure is attenuated and biological factors remain visible. Save the normalized matrix for downstream LinearModelFit biomarker identification.

## Related tools

- **NormQcmets** (Primary normalization function; applies selected method (IS, NOMIS, CCMN, RUV2, RUVrand, RLSC) to featuredata using batch/QC metadata) — https://github.com/metabolomicstats/NormalizeMets
- **RlaPlots** (Diagnostic visualization to assess normalization effectiveness; plots within-group median relative log abundances before and after adjustment) — https://github.com/metabolomicstats/NormalizeMets
- **PcaPlots** (Diagnostic visualization to verify batch structure is attenuated and biological factors remain separated after normalization) — https://github.com/metabolomicstats/NormalizeMets
- **LogTransform** (Prerequisite transformation to stabilize variance before normalization; required prior to calling NormQcmets) — https://github.com/metabolomicstats/NormalizeMets
- **MissingValues** (Prerequisite step to handle missing data in featuredata (knn or replacement) before normalization) — https://github.com/metabolomicstats/NormalizeMets
- **LinearModelFit** (Downstream use: apply to normalized featuredata to identify biomarkers free of batch confounding) — https://github.com/metabolomicstats/NormalizeMets
- **R** (Execution environment for all NormalizeMets functions)

## Examples

```
NormQcmets(featuredata = log_featuredata, factors = sampledata[, c('batch', 'run_order')], method = 'ruv2', k = 2, qcmets = qc_metabolite_names)
```

## Evaluation signals

- RLA plots show within-group median relative log abundances centered at or near zero post-normalization (compare pre- and post-adjustment plots).
- PCA plots show reduced clustering or separation by batch/technical factors (run order, batch ID) and maintained or improved separation by biological factors of interest.
- Quality control metabolite intensities show reduced drift across run order and reduced batch-level mean shifts after normalization.
- Normalized featuredata matrix dimensions are unchanged (samples × metabolites) and values are in expected range (log-scale, no new NAs introduced).
- Downstream LinearModelFit on normalized data produces coefficient and p-value tables with expected number of significant biomarkers (compare volcano plots or p-value histograms to unadjusted controls to detect batch-driven false positives have been removed).

## Limitations

- Normalization effectiveness depends on having sufficient and well-designed QC samples or replicates; sparse or non-random QC placement may lead to under-correction or over-correction.
- RUV2 and RUVrand methods require specification of k (number of unwanted factors); incorrect k selection can remove biological signal or leave residual batch structure; recommended to test k=1,2,3 and compare diagnostic plots.
- RLSC (run-order correction) assumes systematic drift; ineffective if batch structure is random or orthogonal to run order.
- Normalization does not account for missing data; MissingValues() must be called first; if >40% of data are missing per metabolite, that metabolite should be excluded before normalization.
- No changelog provided in repository; version compatibility and updates should be verified against R version (≥3.4.3 required) and active maintenance status.

## Evidence

- [readme] Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation.: "Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation."
- [readme] The NormalizeMets R package contains a collection of functions to aid in the statistical analysis of metabolomic data and can be used assess, select and implement statistical methods for normalizing metabolomics data.: "The NormalizeMets R package contains a collection of functions to aid in the statistical analysis of metabolomic data and can be used assess, select and implement statistical methods for normalizing"
- [other] Normalization methods presented in this package are divided into four categories: "Normalization methods presented in this package are divided into four categories"
- [other] NormQcmets <- function(featuredata, factors = NULL, method = c("is", "nomis", "ccmn", "ruv2", "ruvrand", "ruvrandclust")...: "NormQcmets <- function(featuredata, factors = NULL, method = c("is", "nomis", "ccmn", "ruv2", "ruvrand", "ruvrandclust")"
- [other] Log transforming, handling missing values, and visualization: "Log transforming, handling missing values, and visualization"
- [other] Call LinearModelFit() with featuredata, factormat, and optional parameters (ruv2=FALSE for unadjusted analysis, or ruv2=TRUE with k and qcmets for RUV2 method).: "Call LinearModelFit() with featuredata, factormat, and optional parameters (ruv2=FALSE for unadjusted analysis, or ruv2=TRUE with k and qcmets for RUV2 method)."
- [other] The criteria for assessing and choosing a normalization method implemented in this package: "The criteria for assessing and choosing a normalization method implemented in this package"
