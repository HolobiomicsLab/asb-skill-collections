---
name: log-transformation-and-scale-adjustment
description: Use when raw metabolomics peak intensity data exhibits right-skewed distributions
  with heteroscedastic variance across metabolites and samples, or when combining
  multiple normalization methods (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NormalizeMets
  - RStudio
  license_tier: restricted
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive
  Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
- The use of RStudio is also recommended. RStudio is an integrated development environment
  (IDE)
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

# log-transformation-and-scale-adjustment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply logarithmic transformation and scaling normalization to metabolomics feature data to stabilize variance, reduce the impact of outliers, and correct for systematic differences in peak intensity across samples. This is a foundational preprocessing step in the NormalizeMets workflow for handling unwanted variation due to batch effects and matrix effects.

## When to use

Raw metabolomics peak intensity data exhibits right-skewed distributions with heteroscedastic variance across metabolites and samples, or when combining multiple normalization methods (e.g., RLSC followed by median scaling) to correct for both technical drift and absolute signal magnitude differences.

## When NOT to use

- Data already contain zero or negative values and log transformation has not been preceded by a pseudocount or offset adjustment to avoid domain errors.
- The featuredata has already been log-transformed or normalized by an upstream preprocessing pipeline; re-transformation risks over-correction.
- Analysis goal requires absolute quantification or retention of original intensity ratios for external validation or method comparison.

## Inputs

- featuredata matrix (rows=unique sample names, columns=unique metabolite names, values=peak intensities or concentrations)
- optional: groupdata (sample grouping or class labels for stratified analysis)
- optional: refvec (reference vector for reference-based scaling)

## Outputs

- log-transformed and/or scaled featuredata matrix (same dimensions, values on normalized scale)
- optional: saved output files if saveoutput=TRUE

## How to apply

First, apply LogTransform() to the featuredata matrix, specifying a base (default: natural logarithm e) and deciding whether to save the output. Then apply NormScaling() to the log-transformed featuredata, selecting a scaling method ('median', 'mean', 'sum', or 'ref' with a reference vector) to standardize signal intensity across samples. Alternatively, chain both transformations via NormCombined() with methods=c('rlsc', 'median') or equivalent, which streamlines the workflow. The order matters: log transformation should precede scaling to ensure variance stabilization occurs before magnitude normalization. Set lg=TRUE in functions like NormQcsamples() to apply log transformation as part of a broader normalization pipeline.

## Related tools

- **NormalizeMets** (R package providing LogTransform, NormScaling, and NormCombined functions for integrated log transformation and scaling of metabolomics feature data) — github.com/metabolomicstats/NormalizeMets
- **R** (Statistical computing environment in which LogTransform and NormScaling functions are executed)
- **RStudio** (IDE for interactive execution and debugging of NormalizeMets transformations)

## Examples

```
data(Didata); featuredata_log <- LogTransform(Didata$featuredata, base=exp(1), saveoutput=FALSE); featuredata_normalized <- NormScaling(featuredata_log, method='median')
```

## Evaluation signals

- LogTransform output featuredata contains no negative or infinite values; all entries are finite real numbers on the log scale.
- NormScaling output exhibits expected central tendency: median of scaled values should equal the reference (median=1, mean=1 for mean scaling, or sum=constant for sum scaling).
- PCA or RLA plots post-transformation show reduced batch-driven clustering and more homogeneous variance across samples compared to raw data.
- Distribution of log-transformed metabolite intensities approximates normality (checked via Q-Q plots or Shapiro-Wilk test) more closely than untransformed data.
- Comparison of normalized vs. raw data confirms outliers are less influential and technical drift patterns are attenuated.

## Limitations

- Log transformation assumes all feature intensities are positive; zero or missing values require prior imputation or offset addition to avoid domain errors.
- Scaling method choice (median, mean, sum, ref) introduces a subjective decision point; the article does not provide explicit guidance on selection criteria for different study designs.
- Over-normalization can occur if log transformation is applied after other normalization steps; the order and combination of methods must be carefully planned.
- The NormalizeMets package vignette recommends assessing normalization method effectiveness before committing to a pipeline, but no automated selection criterion is provided in the article.

## Evidence

- [other] LogTransform function definition and purpose: "A metabolomics data matrix in the _featuredata_ format can be transformed using the following function. LogTransform <- function(featuredata, base=exp(1), saveoutput=FALSE,"
- [other] NormScaling function definition: "NormScaling<-function(featuredata, method = c("median", "mean", "sum", "ref"), refvec = NULL"
- [other] Combined normalization workflow including log transformation: "NormCombined<-function(featuredata, methods = c("rlsc", "median"), savefinaloutput = FALSE, finaloutputname = NULL"
- [other] Log transformation parameter in RLSC normalization: "NormQcsamples<- function(featuredata, sampledata, method = c("rlsc"), span = 0, deg = 2, lg = TRUE"
- [readme] Metabolomics data variability rationale: "Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation."
