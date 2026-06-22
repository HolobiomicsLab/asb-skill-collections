---
name: missing-value-imputation-for-omics
description: Use when your metabolomic peak table contains missing values (e.g., undetected metabolites below instrument sensitivity or sparse measurements) and you are preparing multi-class or time-course data for statistical analysis, differential profiling, or biomarker discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NOREVA
  - impute
  - statTarget
  - limma
  - pcaMethods
  - Biobase
derived_from:
- doi: 10.1038/s41596-021-00636-9
  title: NOREVA
evidence_spans:
- '[![R >3.5](https://img.shields.io/badge/R-%3E3.5-success.svg)](https://www.r-project.org/)'
- devtools::install_github("idrblab/NOREVA")
- BiocManager::install("impute")
- BiocManager::install("statTarget")
- BiocManager::install("limma")
- BiocManager::install("pcaMethods")
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_noreva_cq
    doi: 10.1038/s41596-021-00636-9
    title: NOREVA
  dedup_kept_from: coll_noreva_cq
schema_version: 0.2.0
---

# missing-value-imputation-for-omics

## Summary

Apply missing-value imputation to metabolomic peak tables as a preprocessing step before QC correction, transformation, and normalization. This skill selects and executes one of four imputation methods (coded 1–4) within the NOREVA framework to handle missing intensity values while preserving metabolite and sample relationships.

## When to use

Your metabolomic peak table contains missing values (e.g., undetected metabolites below instrument sensitivity or sparse measurements) and you are preparing multi-class or time-course data for statistical analysis, differential profiling, or biomarker discovery. Use this skill when missing values are present but you do not yet know whether simple deletion, mean imputation, k-nearest-neighbor imputation, or model-based imputation will best preserve downstream discovery power.

## When NOT to use

- Your peak table already has no missing values or missing values are structurally meaningful (e.g., zero-inflated data from a sparse metabolite in most samples).
- You require imputation of missing values in sample metadata (phenotype labels, covariates) rather than metabolite intensities.
- The majority (>50%) of values are missing in specific metabolites or samples, indicating systematic data quality problems rather than random missingness.

## Inputs

- Prepared multi-class metabolomic peak matrix (ExpressionSet format in Biobase, or CSV/text file)
- Sample metadata and class labels (for multi-class stratification)
- Imputation method code (integer 1–4)
- Dataset type code (1 = no QC/IS; 2 = with QC; 3 = with internal standards)

## Outputs

- Imputed peak table (numeric matrix with missing values replaced)
- ExpressionSet object with imputed expression matrix and preserved phenotype data
- CSV file of processed peak table (rows = metabolites, columns = samples)

## How to apply

Load the prepared peak matrix into R using Biobase ExpressionSet format, then call the normulticlassmatrix function with your chosen imputation method code (1–4) as the first preprocessing step in the workflow sequence. The function accepts a datatype parameter (1, 2, or 3) specifying whether your dataset has no QC samples/internal standards, QC samples, or internal standards respectively. Run the imputation step alone or as the initial phase of a full preprocessing pipeline (imputation → QC correction → transformation → normalization). Extract the imputed peak table from the NOREVA output object and validate that missing values have been replaced with numeric intensities and that the matrix dimensions remain unchanged.

## Related tools

- **NOREVA** (Orchestrates imputation workflow via normulticlassmatrix function; accepts method code and applies selected imputation to multi-class/time-course metabolomic data) — https://github.com/idrblab/NOREVA
- **impute** (Provides underlying imputation algorithms (k-nearest-neighbor and model-based methods) called by NOREVA)
- **pcaMethods** (Supplies principal component analysis-based imputation methods used by NOREVA)
- **Biobase** (Defines ExpressionSet data structure for storing and manipulating imputed peak matrices with sample metadata)
- **R** (Execution environment (≥3.5) for NOREVA package and imputation workflow) — https://www.r-project.org/

## Examples

```
library(NOREVA); result <- normulticlassmatrix(fileName='prepared_data', datatype=2, imputation_method=1, QC_method=1, transformation_method=1, normalization_method=1)
```

## Evaluation signals

- No NA, NaN, or missing numeric values remain in the imputed peak matrix.
- Imputed matrix dimensions (rows = metabolites, columns = samples) match the input; no features or samples were dropped.
- Imputed values fall within a plausible intensity range consistent with the measured metabolites (e.g., positive values for MS intensities, no extreme outliers).
- Sample grouping (multi-class labels) and metabolite identities are preserved in the ExpressionSet object after imputation.
- Comparison of PCA scores or clustering before/after imputation shows reasonable stability (no collapse of class separation or introduction of artifacts).

## Limitations

- NOREVA imputation method codes (1–4) are not explicitly enumerated in the provided README; users must consult NOREVA documentation (??NOREVA in R) or the Nature Protocols publication to determine which algorithm each code represents.
- Imputation performance depends on the missing-data mechanism (MCAR, MAR, or MNAR); NOREVA's built-in methods may not handle non-random missingness optimally without external guidance on study assumptions.
- High proportions of missing values (>30–40% per metabolite) can lead to inflated false discovery in downstream differential analysis, regardless of imputation method.
- NOREVA version 2.1.1 optimizes I/O efficiency and parallel computing but may require tuning of memory parameters for very large peak matrices (>100K metabolites or >10K samples).

## Evidence

- [other] imputation (1–4): "processing method codes for imputation (1–4), QC sample correction (1–3), transformation (1–3), and normalization"
- [other] accept prepared multi-class metabolomic dataset: "The normulticlassmatrix function accepts a datatype parameter (1, 2, or 3 for datasets without QCSs/ISs, with QCSs, or with ISs respectively), a prepared fileName"
- [other] preprocessing workflow sequence: "Select and apply the chosen preprocessing workflow sequence (impute missing values if specified, apply QC signal normalization if specified, apply transformation if specified, apply normalization if"
- [other] ExpressionSet format: "Load the multi-class peak matrix and metadata into R using Biobase ExpressionSet format."
- [readme] impute package capability: "BiocManager::install("impute")"
- [readme] pcaMethods for analysis: "BiocManager::install("pcaMethods")"
