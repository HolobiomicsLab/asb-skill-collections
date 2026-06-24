---
name: internal-standard-normalization
description: Use when your metabolomics dataset includes internal standard metabolites
  (marked in the metabolitedata IS column), log-transformed featuredata are available,
  and you need to remove systematic variation attributable to instrument drift, sample
  matrix effects, or batch differences while preserving.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - NormalizeMets
  - RStudio
  - NormQcmets
  - LogTransform
  - MissingValues
  - RlaPlots
  - PcaPlots
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
  - build: coll_eclipse_cq
    doi: 10.1093/bioinformatics/btaf290/8128335
    title: Eclipse
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

# internal-standard-normalization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Normalize metabolomics featuredata matrices using internal standard (IS) metabolites as reference anchors to correct for unwanted variation (batch effects, matrix effects) across samples. This skill applies the 'is' method within the NormQcmets function, which requires identification of internal standard metabolites and uses their relative intensities to scale all features within each sample.

## When to use

Your metabolomics dataset includes internal standard metabolites (marked in the metabolitedata IS column), log-transformed featuredata are available, and you need to remove systematic variation attributable to instrument drift, sample matrix effects, or batch differences while preserving biological signal. Use this skill when internal standards span your analytical run and you want a reference-based normalization approach.

## When NOT to use

- Input featuredata has not been log-transformed; raw or untransformed peak intensities will violate the assumption of multiplicative error.
- No internal standards are available or marked in the metabolitedata; use NormQcsamples (RLSC) or NormScaling (median/mean/sum) instead.
- Internal standards show biological variation correlated with the exposure or outcome of interest; they would remove signal rather than unwanted variation.

## Inputs

- featuredata matrix (metabolite intensities or concentrations, samples × metabolites, log-transformed)
- metabolitedata dataframe (metabolite-specific metadata with IS column marking internal standards)
- sampledata dataframe (sample identifiers and metadata)
- indices or boolean vector identifying internal standard metabolites

## Outputs

- normalized featuredata matrix (same dimensions as input, corrected for IS-based variation)

## How to apply

First, load your metabolomics dataset (featuredata, sampledata, metabolitedata) and log-transform the featuredata using LogTransform with base=exp(1) and zerotona=TRUE to handle zero values. Identify the column indices of internal standard metabolites from the metabolitedata IS column. Then call NormQcmets with the log-transformed featuredata, specify method='is', pass the IS metabolite indices via the qcmets parameter, and optionally supply an isvec parameter if using a specific internal standard vector. The function normalizes each sample by scaling feature intensities relative to the geometric mean (or specified reference) of the internal standards, thereby correcting for sample-to-sample variation in ionization efficiency and instrument response. Extract and validate the normalized featuredata matrix from the returned object.

## Related tools

- **NormQcmets** (Primary function that implements internal standard (is) normalization method along with alternative methods (nomis, ccmn, ruv2, ruvrand, ruvrandclust)) — github.com/metabolomicstats/NormalizeMets
- **LogTransform** (Prerequisite function to log-transform featuredata before normalization, handling zeros via zerotona parameter) — github.com/metabolomicstats/NormalizeMets
- **MissingValues** (Optional preprocessing step to impute missing values in featuredata using knn or replacement methods before normalization) — github.com/metabolomicstats/NormalizeMets
- **RlaPlots** (Visualization tool to assess normalization quality by comparing relative log abundance before and after IS normalization) — github.com/metabolomicstats/NormalizeMets
- **PcaPlots** (Post-normalization quality check to visualize whether IS normalization reduces unwanted batch or run-order variation in principal component space) — github.com/metabolomicstats/NormalizeMets
- **R** (Statistical computing environment required to execute NormQcmets and associated NormalizeMets functions)
- **RStudio** (Recommended integrated development environment for interactive execution and debugging of normalization workflow)

## Examples

```
NormQcmets(featuredata=log_featuredata, factors=NULL, method='is', qcmets=is_indices, isvec=NULL)
```

## Evaluation signals

- Verify that the returned normalized featuredata matrix has the same dimensions (samples × metabolites) as input and contains no NaN or Inf values outside expected ranges.
- Check that relative intensities of internal standard metabolites across samples are more homogeneous (lower coefficient of variation) after normalization compared to log-transformed input.
- Generate RlaPlots before and after normalization; IS normalization should visually reduce systematic trends in relative log abundance across sample order or batch.
- Confirm that biological signal of interest (e.g., metabolite associations with exposure) is preserved or strengthened post-normalization via correlation or linear model analysis.
- Compare PCA plots before and after normalization; IS normalization should reduce clustering by batch/run order while maintaining biological grouping if present.

## Limitations

- Internal standard metabolites must be stably measured across all samples and not subject to biological variation linked to the outcome; failure violates the assumption of true 'unwanted variation only'.
- If internal standards show high technical variation themselves, they will propagate error rather than correct it; assess IS CV before applying.
- Method assumes multiplicative error structure (i.e., log-scale); if additive errors dominate or data include negative values, results may be unreliable.
- No explicit guidance provided for selecting which IS metabolites to use when multiple are available; the article recommends assessing normalization method choice empirically (e.g., via RlaPlots, PcaPlots, linear model fit).

## Evidence

- [other] The NormQcmets function accepts a featuredata matrix as input along with optional factors and a normalization method parameter supporting 'is', 'nomis', 'ccmn', 'ruv2', 'ruvrand', and 'ruvrandclust' methods: "The NormQcmets function accepts a featuredata matrix as input along with optional factors and a normalization method parameter supporting 'is', 'nomis', 'ccmn', 'ruv2', 'ruvrand', and 'ruvrandclust'"
- [other] Identify quality control metabolites (internal standards) from the metabolitedata using the IS column: "Identify quality control metabolites (internal standards) from the metabolitedata using the IS column."
- [other] Call NormQcmets with the log-transformed featuredata, specifying the chosen method (is, nomis, ccmn, ruv2, ruvrand, or ruvrandclust), pass the indices of QC metabolites via qcmets parameter, and provide additional parameters as required (e.g., isvec for 'is' method: "Call NormQcmets with the log-transformed featuredata, specifying the chosen method (is, nomis, ccmn, ruv2, ruvrand, or ruvrandclust), pass the indices of QC metabolites via qcmets parameter, and"
- [other] Log-transform the featuredata using LogTransform with base=exp(1) and zerotona=TRUE to handle zeros: "Log-transform the featuredata using LogTransform with base=exp(1) and zerotona=TRUE to handle zeros."
- [readme] Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation.: "Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation."
- [readme] metabolitedata contains metabolite-specific information in a separate dataframe. These information can include, but is not limited to, designation of metabolites as internal/external standards: "metabolitedata contains metabolite-specific information in a separate dataframe. These information can include, but is not limited to, designation of metabolites as internal/external standards"
