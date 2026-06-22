---
name: batch-design-specification
description: Use when before applying any batch effect correction function in dbnorm (dbnormPcom, dbnormNPcom, dbnormBer, dbnormBagging, Visodbnorm, or hclustdbnorm), you must first prepare and validate a batch assignment vector that maps each sample to its analytical run or batch.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - dbnorm
  - sva
  - R
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- ComBat(parametric and non-parametric)-model [PMID:16632515] from sva package [PMID:22257669]
- dbnorm contains R functions which allow visualization and removal of technical heterogeneity
- '*dbnorm* contains R functions which allow visualization and removal of technical heterogeneity'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dbnorm_cq
    doi: 10.1038/s41598-021-84824-3
    title: Dbnorm
  dedup_kept_from: coll_dbnorm_cq
schema_version: 0.2.0
---

# batch-design-specification

## Summary

Specification and documentation of batch assignment vectors and experimental design metadata required to correctly apply batch effect correction models (ComBat, two-stage procedure) to metabolomics datasets. Proper batch design specification ensures that technical heterogeneity is correctly attributed and removed without confounding biological signal.

## When to use

Before applying any batch effect correction function in dbnorm (dbnormPcom, dbnormNPcom, dbnormBer, dbnormBagging, Visodbnorm, or hclustdbnorm), you must first prepare and validate a batch assignment vector that maps each sample to its analytical run or batch. Use this skill when metabolomics data spans multiple analytical runs, sample preparation batches, instrument sessions, or time-dependent drift periods, and you need to distinguish technical variation from biological variation.

## When NOT to use

- When samples are already batch-corrected or normalized by external tools; double-correction may remove biological signal.
- When batch information is unavailable or all samples were processed in a single analytical run (no technical heterogeneity across batches).
- When batch assignment is ambiguous or samples cannot be reliably mapped to a single batch (e.g., multiplexed or partially overlapping runs without clear demarcation).

## Inputs

- CSV file with samples (rows) × features (columns) matrix
- Batch assignment vector (first column of CSV, one label per sample)
- Preprocessed and log2-scaled metabolomics intensity matrix

## Outputs

- Validated batch design specification (R data.frame with batch column)
- Confirmed alignment of batch vector to sample count
- Input-ready data structure for dbnorm batch correction functions

## How to apply

Prepare a comma-separated CSV file with samples (independent experiments) in rows and features (metabolites) in columns. Place batch level identifiers in the first column, with each unique batch label (e.g., 'Batch_1', 'Batch_2', 'run_A', 'run_B') representing a distinct analytical run or preparation cohort. The batch vector must have one entry per sample and correctly align with the feature matrix columns. Load this structured data using `read.csv()` in R with `row.names=1` to preserve batch labels. The batch design specification directly feeds into the statistical models: ComBat (parametric and non-parametric) uses empirical Bayes methods to estimate batch effects conditional on the batch assignment, while the two-stage procedure uses batch labels to partition data for location and scale adjustment. Validate that batch labels are consistent, non-empty, and that no samples are unassigned.

## Related tools

- **dbnorm** (Batch normalization and visualization package that consumes batch design specification to apply ComBat and two-stage correction models) — https://github.com/NBDZ/dbnorm
- **sva** (Bioconductor package providing ComBat (parametric and non-parametric) empirical Bayes models used by dbnorm for batch effect correction) — https://bioconductor.org/packages/sva
- **R** (Statistical computing environment for loading, validating, and preparing batch design specifications and metabolomics matrices)

## Examples

```
data <- read.csv("path/to/metabolomics.csv", sep=",", header=TRUE, row.names=1); library(dbnorm); dbnormPcom(data)
```

## Evaluation signals

- Batch vector length equals number of samples (rows) in the feature matrix; no missing or NA values in batch column.
- All unique batch labels are non-empty strings and are consistent across the design (no typos or case mismatches).
- After loading with `read.csv(..., row.names=1)`, `table(data[,1])` or `unique(data[[1]])` shows all expected batch groups with non-zero sample counts.
- Batch design passes as input to dbnorm functions without type errors or dimension mismatches; functions execute without 'batch vector length mismatch' warnings.
- Downstream batch correction outputs (adjusted R² scores, PCA plots, corrected feature matrices) show reduced batch-level clustering and improved overlap of replicate samples across batches.

## Limitations

- Batch labels are categorical; temporal or continuous drift within a batch cannot be captured by discrete batch assignment alone.
- The two-stage procedure and ComBat assume that batch effects are additive or multiplicative on the log2-transformed scale; other systematic biases (e.g., instrument calibration drift, nonlinear detector response) may not be fully removed.
- Small or unbalanced batch sizes (e.g., a batch with only 1–2 samples) may lead to unstable empirical Bayes parameter estimates, reducing correction efficacy.
- The batch design specification does not account for covariates of interest (disease status, phenotype); care must be taken that batch adjustment does not remove biological signal correlated with batch.

## Evidence

- [other] Load the preprocessed metabolomics matrix and batch assignment vector into R: "Load the preprocessed metabolomics matrix and batch assignment vector into R."
- [readme] Input data must be in .csv format with independent experiments in rows and features in columns, with batch levels in first column: "The input data must be in **.csv** format with the independent experiments in the rows and the features (variables) in the columns, with the `batch` levels considered in the first column."
- [readme] ComBat and two-stage procedure use batch labels to correct for technical heterogeneity: "This function performs batch effect adjustment via three statistical models implemented in the *dbnorm*, namely two-stage procedure as described by Giordan (2013) and/or empirical Bayes methods in"
- [readme] dbnorm includes 11 functions for batch effect correction based on statistical models: "conventional functions for batch effect correction based on statistical models, as well as functions using advanced statistical tools to generate several diagnosis plots"
- [readme] Batch design enables removal of technical heterogeneity across analytical runs: "It allows users to efficiently correct drift across batch and to adjust large metabolomics datasets for technical variation"
