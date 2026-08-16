---
name: metabolomic-peak-matrix-preprocessing
description: Use when you have a raw or minimally processed metabolomic peak matrix
  (in standardized or tool-generated format) from multi-class samples with optional
  quality control (QC) samples and/or internal standards (IS), and you need to generate
  a single normalized peak table suitable for statistical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
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
  license_tier: open
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-021-00636-9
  all_source_dois:
  - 10.1038/s41596-021-00636-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-peak-matrix-preprocessing

## Summary

Transform a prepared multi-class or time-course metabolomic peak matrix into a processed feature table by sequentially applying imputation, QC signal correction, log/other transformation, and metabolite- or sample-based normalization workflows using NOREVA. This skill selects and executes the optimal preprocessing sequence for downstream biomarker discovery or differential profiling.

## When to use

Apply this skill when you have a raw or minimally processed metabolomic peak matrix (in standardized or tool-generated format) from multi-class samples with optional quality control (QC) samples and/or internal standards (IS), and you need to generate a single normalized peak table suitable for statistical testing or biomarker identification. Use it after data import and sample/metabolite annotation, before statistical modeling or feature selection.

## When NOT to use

- Input is already a fully processed, normalized feature table from another preprocessing pipeline—applying NOREVA preprocessing would introduce redundant or conflicting transformations.
- Dataset contains only univariate samples (no class labels or biological grouping); NOREVA is designed for multi-class or time-course comparisons and evaluation criteria assume class structure.
- Peak matrix contains fewer than ~10–20 metabolites or samples; NOREVA's workflow scanning and evaluation criteria are optimized for larger-scale metabolomic datasets and may overfit or produce unstable rankings on sparse data.

## Inputs

- raw or minimally processed peak matrix (CSV, standardized NOREVA format, or output from vendor software: mzXML, netCDF, raw MS data formats)
- sample metadata file with class labels and (optionally) QC sample identifiers or internal standard column indices
- Biobase ExpressionSet object (after calling PrepareInuputFiles)

## Outputs

- processed peak table (CSV, single matrix with metabolites as rows and samples as columns)
- imputed and normalized feature intensities ready for statistical testing or biomarker discovery

## How to apply

First, load the peak matrix and sample metadata into R using Biobase ExpressionSet format and call PrepareInuputFiles() to standardize the input format. Next, select the appropriate NOREVA function based on your dataset structure: use normulticlassqcall() for multi-class data with QC samples, normulticlassnoall() for multi-class without QC/IS, or normulticlassisall() for datasets with internal standards. For each function, specify your study assumptions (SAalpha, SAbeta, SAgamma) reflecting whether metabolites are equally important, if abundance is constant across samples, and if most metabolites are unchanged under the studied conditions. Within the chosen function, select method codes for imputation (1–4; e.g., KNN, mean, or median), QC correction (1–3; e.g., signal correction via QC samples), transformation (1–3; e.g., log2 or pareto), and normalization (1–20 for metabolite-centric, sample-centric, or hybrid approaches). The function will execute the full preprocessing workflow and output a processed peak table; extract this table and write to CSV. The rationale is that no single preprocessing choice works optimally for all datasets—NOREVA integrates five distinct evaluation criteria (each with different theoretical foundations) to comprehensively assess thousands of workflow combinations and rank them, guiding selection of the best-performing workflow for your specific assumptions and biological context.

## Related tools

- **NOREVA** (Core R package providing normulticlassmatrix, normulticlassqcall, normulticlassnoall, normulticlassisall functions to execute multi-step preprocessing workflows and rank them by five integrated evaluation criteria) — https://github.com/idrblab/NOREVA
- **Biobase** (Provides ExpressionSet class for storing and manipulating peak matrix, metadata, and feature annotations in standardized format required by NOREVA) — https://bioconductor.org/packages/Biobase
- **impute** (Implements KNN and other imputation methods (method code 1–4) for handling missing values in peak intensity matrix) — https://bioconductor.org/packages/impute
- **statTarget** (Provides QC sample-based signal correction methods (method code 1–3) to normalize systematic variation and instrumental drift) — https://bioconductor.org/packages/statTarget
- **limma** (Supplies transformation and normalization approaches integrated into NOREVA's preprocessing workflows) — https://bioconductor.org/packages/limma
- **pcaMethods** (Provides PCA-based imputation and transformation methods available within NOREVA normalization options) — https://bioconductor.org/packages/pcaMethods

## Examples

```
library(NOREVA); PrepareInuputFiles(dataformat=1, rawdata='peak_matrix.csv', label='sample_labels.csv'); result <- normulticlassqcall(fileName='prepared_data', SAalpha='Y', SAbeta='Y', SAgamma='Y'); write.csv(result$processed_peak_table, 'normalized_peaks.csv')
```

## Evaluation signals

- Output peak table has same number of samples as input, with no unexpected row or column loss; all metabolite and sample identifiers are preserved.
- Processed intensities are strictly positive (after log transformation) or in expected numerical range; no NaN, Inf, or negative values remain.
- QC sample intensities (if present in input) are more similar to each other than to biological samples post-preprocessing, indicating successful QC correction.
- Distribution of normalized intensities across samples shows expected centering and scaling relative to input (e.g., post-log-transformation mean ≈ 0, SD ≈ 1 for z-score normalization); verify via boxplot or density plot.
- Rank ordering of preprocessing workflows reported by NOREVA reflects consistency across the five evaluation criteria; high concordance suggests robust optimal workflow selection.

## Limitations

- NOREVA's evaluation criteria assume multi-class or time-course structure; datasets with weak or absent class structure may yield unreliable or non-interpretable workflow rankings.
- Preprocessing method codes (1–4 for imputation, 1–3 for QC correction, 1–3 for transformation, 1–20 for normalization) are fixed and cannot be easily extended; custom imputation or normalization schemes require wrapper code external to NOREVA.
- Study assumption parameters (SAalpha, SAbeta, SAgamma) must be specified a priori; misspecification of assumptions can lead to selection of a suboptimal workflow that violates the true data structure.
- NOREVA's five evaluation criteria each rest on distinct theoretical assumptions (e.g., QC-based stability, PCA-based variance structure); no single criterion is universally superior, and criterion weights are unspecified in the selection logic.
- Internal standards (IS) are required to use normulticlassisall(); datasets lacking IS but containing other forms of calibration or reference compounds may not benefit from IS-based correction.

## Evidence

- [other] The normulticlassmatrix function accepts a datatype parameter (1, 2, or 3 for datasets without QCSs/ISs, with QCSs, or with ISs respectively), a prepared fileName, optional IS column identifiers, and processing method codes for imputation (1–4), QC sample correction (1–3), transformation (1–3), and normalization (1–20 for metabolite-based, sample-based, or combined approaches), then outputs a single processed peak table.: "The normulticlassmatrix function accepts a datatype parameter (1, 2, or 3 for datasets without QCSs/ISs, with QCSs, or with ISs respectively), a prepared fileName, optional IS column identifiers, and"
- [readme] The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing workflows.: "The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing"
- [readme] Particularly, five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion.: "five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion."
- [readme] This study provides guidelines for researchers who will engage in biomarker discovery or other differential profiling omics studies with respect selecting the most appropriate preprocessing method: "provides guidelines for researchers who will engage in biomarker discovery or other differential profiling omics studies with respect selecting the most appropriate preprocessing method"
- [other] Load the multi-class peak matrix and metadata into R using Biobase ExpressionSet format. 2. Select and apply the chosen preprocessing workflow sequence (impute missing values if specified, apply QC signal normalization if specified, apply transformation if specified, apply normalization if specified) using NOREVA's normulticlassmatrix function: "Load the multi-class peak matrix and metadata into R using Biobase ExpressionSet format. Select and apply the chosen preprocessing workflow sequence (impute missing values if specified, apply QC"
