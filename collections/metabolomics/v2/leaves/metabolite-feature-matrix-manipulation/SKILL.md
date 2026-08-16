---
name: metabolite-feature-matrix-manipulation
description: Use when you have raw metabolomics peak intensity or concentration data
  in matrix form (samples as rows, metabolites as columns) and need to prepare it
  for normalization or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - NormalizeMets
  - LogTransform
  - MissingValues
  license_tier: open
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

# metabolite-feature-matrix-manipulation

## Summary

Prepare and transform raw metabolomics intensity matrices into analysis-ready featuredata objects through log transformation and missing-value handling. This skill enables downstream normalization, biomarker identification, and statistical modeling by standardizing the input data format and distribution.

## When to use

Apply this skill when you have raw metabolomics peak intensity or concentration data in matrix form (samples as rows, metabolites as columns) and need to prepare it for normalization or statistical analysis. Specifically, use it when the data exhibits non-normal (right-skewed) intensity distributions, contains missing values from incomplete analyses or below-detection-limit measurements, or requires standardization before batch-effect correction or biomarker discovery workflows.

## When NOT to use

- Input data is already normalized, batch-corrected, or log-transformed by upstream processing.
- Missing values represent true biological zeros (e.g., metabolites absent in certain samples) — replacement or imputation may introduce bias; consider filtering instead.
- Data is already in a reduced-dimension or summary format (e.g., PCA scores, averaged across replicates) rather than raw feature-level intensities.

## Inputs

- raw featuredata matrix (samples × metabolites, numeric intensities or concentrations)
- sample row names (unique sample identifiers)
- metabolite column names (unique metabolite identifiers)

## Outputs

- log-transformed featuredata matrix
- imputed featuredata matrix (missing values replaced)
- processed featuredata object ready for normalization or statistical analysis

## How to apply

Load the raw featuredata matrix (sample names as row names, metabolite names as column names) into R. Apply LogTransform() with base=exp(1) to convert intensity values to log scale, addressing the non-normal distribution typical of metabolomics measurements. Then apply MissingValues() to handle missing data using either k-nearest-neighbor (knn) imputation for data missing at random, or replacement methods (e.g., half minimum detection limit) for values below detection threshold. The choice between methods depends on the missing-data mechanism: use knn for sparse, random missingness; use replacement for systematic missingness associated with detection limits. Validate that the resulting featuredata matrix contains no missing values and has appropriate numeric range for downstream normalization (typically log-transformed intensities with mean near zero and sd near 1 before normalization). Store the processed featuredata as an R object for input to NormQcmets(), NormScaling(), or LinearModelFit().

## Related tools

- **LogTransform** (Applies log transformation (base e by default) to featuredata matrix to normalize intensity distributions) — github.com/metabolomicstats/NormalizeMets
- **MissingValues** (Replaces or imputes missing values in featuredata depending on missingness mechanism (knn or replacement methods)) — github.com/metabolomicstats/NormalizeMets
- **R** (Execution environment for loading, manipulating, and validating metabolomics matrices)
- **NormalizeMets** (R package containing LogTransform and MissingValues functions and dependent workflow functions) — github.com/metabolomicstats/NormalizeMets

## Examples

```
LogTransform(featuredata, base=exp(1), saveoutput=FALSE); featuredata_imputed <- MissingValues(featuredata_log, method=c('knn'))
```

## Evaluation signals

- Log-transformed featuredata has numeric values with plausible range (typically mean ~0–1 log scale) suitable for normalization; no negative values if base-e log of positive intensities.
- Imputed featuredata contains zero missing values (100% completeness) across all samples and metabolites; missingness summary shows all replaced values documented.
- Row and column names are preserved, unique, and match the original featuredata dimensions; sample and metabolite identities are traceable.
- Distribution of log-transformed intensities is approximately normal or unimodal (inspect via histogram or Q-Q plot); skewness reduced compared to raw intensity distribution.
- Imputation choice is justified by missing-data pattern: knn applied to sparse random missingness; replacement applied to systematic below-detection-limit missingness.

## Limitations

- Log transformation assumes all intensity values are positive; zero or negative values will produce NaN or -Inf, requiring filtering or pseudocount addition before transformation.
- Missing-value imputation introduces uncertainty; knn imputation accuracy depends on number of observed neighbors and data dimensionality; replacement at LOD threshold is conservative but may underestimate true biological signals.
- This skill does not address batch effects, matrix effects, or other sources of unwanted variation; normalized data should be processed through NormQcmets() or NormCombined() for batch correction.
- The choice of imputation method (knn vs. replacement) is not automated; analyst must inspect missing-data patterns and justify method selection per study design.

## Evidence

- [other] Log transforming, handling missing values, and visualization: "Log transforming, handling missing values, and visualization"
- [other] A metabolomics data matrix in the _featuredata_ format can be transformed using the following function. LogTransform <- function(featuredata, base=exp(1), saveoutput=FALSE,: "A metabolomics data matrix in the _featuredata_ format can be transformed using the following function. LogTransform <- function(featuredata, base=exp(1)"
- [other] The following `MissingValues()` function can be used to replace missing values, depending on the nature of missing data.: "The following `MissingValues()` function can be used to replace missing values, depending on the nature of missing data."
- [other] Load the imputed featuredata matrix (log-transformed, missing values handled via knn or replacement) and a design matrix (factormat) encoding factors of interest: "Load the imputed featuredata matrix (log-transformed, missing values handled via knn or replacement) and a design matrix"
- [readme] The input data format consists of three parts: (i) "featuredata" which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be provided as row names and unique metabolite names as column names: "featuredata" which is the metabolomics data matrix containing all metabolite peak intensities. Unique sample names must be provided as row names and unique metabolite names as column names"
