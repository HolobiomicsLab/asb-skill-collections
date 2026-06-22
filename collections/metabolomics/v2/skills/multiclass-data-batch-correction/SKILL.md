---
name: multiclass-data-batch-correction
description: Use when your input is a raw or prepared multi-class metabolomic peak table (in ExpressionSet format or CSV) where samples belong to distinct biological classes, and you have either QC samples (quality control replicates) or internal standards (IS) to anchor batch correction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-021-00636-9
  all_source_dois:
  - 10.1038/s41596-021-00636-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Multiclass Metabolomic Data Batch Correction

## Summary

Apply integrated quality control and batch correction workflows to multi-class metabolomic peak tables to remove systematic variation from QC samples or internal standards. This skill normalizes signal drift and technical bias across sample classes before downstream biomarker discovery or differential profiling.

## When to use

Your input is a raw or prepared multi-class metabolomic peak table (in ExpressionSet format or CSV) where samples belong to distinct biological classes, and you have either QC samples (quality control replicates) or internal standards (IS) to anchor batch correction. Apply this skill before performing differential abundance or biomarker discovery when technical batch effects may confound biological signals across classes.

## When NOT to use

- Input is already a fully processed feature table from another preprocessing pipeline—re-normalizing risks over-correction and loss of biological signal.
- Dataset lacks QC samples or internal standards AND you cannot justify study assumptions (alpha, beta, gamma)—batch correction will be unreliable without anchors or valid assumptions.
- Samples belong to a single biological class without multi-class structure—use univariate QC normalization instead of multi-class batch correction.

## Inputs

- Multi-class metabolomic peak table (raw or prepared; CSV or ExpressionSet format)
- Metadata/label file indicating class membership for each sample
- QC sample replicates (if datatype=2) or internal standard column indices (if datatype=3)

## Outputs

- Processed peak table (CSV) with batch correction, imputation, and normalization applied
- NOREVA output object containing workflow performance metrics and corrected ExpressionSet

## How to apply

First, prepare your multi-class peak matrix and metadata using PrepareInuputFiles(), specifying the dataformat (1 for NOREVA standardized format, 2 for software-generated formats) and input label file. Load the prepared result into R as a Biobase ExpressionSet object. Call normulticlassmatrix() with: (1) datatype parameter matching your QC/IS availability (1=no QCS/IS, 2=with QCS, 3=with IS), (2) the prepared fileName, (3) optional IS column identifiers if using internal standards, and (4) preprocessing method codes for imputation (1–4), QC correction (1–3), transformation (1–3), and normalization (1–20, where codes specify metabolite-based, sample-based, or combined approaches). The function applies the selected workflow sequence in order—imputation, then QC signal normalization (if QC samples or IS present), then transformation, then normalization—and outputs a processed peak table. Extract and write the result to CSV. Rationale: NOREVA's normulticlassmatrix integrates multiple independent correction criteria and supports thousands of workflow combinations; the ordered pipeline ensures batch effects are removed before applying transformation and statistical scaling, preserving biological signal.

## Related tools

- **NOREVA** (Executes normulticlassmatrix() function to apply integrated QC correction, imputation, transformation, and normalization workflows on multi-class metabolomic peak tables) — https://github.com/idrblab/NOREVA
- **Biobase** (Loads and structures multi-class peak matrix and metadata as ExpressionSet objects for input to NOREVA)
- **statTarget** (Provides QC sample-based signal correction and normalization methods integrated into NOREVA workflow)
- **limma** (Supplies batch effect modeling and correction algorithms used by NOREVA normalization methods)
- **impute** (Handles missing value imputation in preprocessing step of NOREVA normulticlassmatrix workflow)
- **pcaMethods** (Provides principal component analysis options for normalization and quality assessment within NOREVA)

## Examples

```
library(NOREVA); prepared <- PrepareInuputFiles(dataformat=1, rawdata='peak_table.csv', label='sample_labels.txt'); result <- normulticlassmatrix(prepared, datatype=2, IS=NULL, imputation=1, qcCorrection=1, transformation=1, normalization=8); write.csv(result$peak_table, 'corrected_peaks.csv')
```

## Evaluation signals

- Verify the output peak table dimensions match input (same metabolites × corrected samples) and contains no negative abundances after transformation/normalization.
- Confirm QC sample correlation and reproducibility improved: PCA or heatmap of QC replicates should cluster tightly post-correction; RSD (relative standard deviation) of QC metabolites should decrease.
- Check that biological class separation is preserved or improved: samples within each class should remain coherent or show stronger separation from other classes than before correction.
- Validate workflow code was applied correctly by inspecting NOREVA output metadata; compare performance metrics (alpha, beta, gamma criteria) across candidate workflows to confirm the selected method ranked in top tier.
- Perform sensitivity analysis: re-run with alternative preprocessing codes (different imputation, transformation, normalization) and verify that corrected peak table is stable and that top biomarker candidates remain consistent.

## Limitations

- Requires preparation via PrepareInuputFiles() first; NOREVA does not accept raw instrument files directly.
- QC correction (datatype=2) is most effective when QC samples are evenly distributed across the analysis; sparse or end-heavy QC sampling may not capture all batch drift.
- Internal standard (IS) correction (datatype=3) assumes IS metabolites are truly stable across all conditions; if biological treatment affects IS abundance, correction will bias results.
- Study assumptions (alpha, beta, gamma) are user-specified and cannot be validated a priori; incorrect assumption selection may lead to suboptimal workflow ranking and selection.
- NOREVA version 2.1.1 optimizes memory and I/O but still requires sufficient RAM for scanning thousands of preprocessing workflows; very large datasets (>10k metabolites × >1k samples) may encounter performance bottlenecks.

## Evidence

- [other] The normulticlassmatrix function accepts a datatype parameter (1, 2, or 3 for datasets without QCSs/ISs, with QCSs, or with ISs respectively), a prepared fileName, optional IS column identifiers, and processing method codes for imputation (1–4), QC sample correction (1–3), transformation (1–3), and normalization (1–20...), then outputs a single processed peak table.: "The normulticlassmatrix function accepts a datatype parameter (1, 2, or 3 for datasets without QCSs/ISs, with QCSs, or with ISs respectively), a prepared fileName, optional IS column identifiers, and"
- [other] Load the multi-class peak matrix and metadata into R using Biobase ExpressionSet format. 2. Select and apply the chosen preprocessing workflow sequence (impute missing values if specified, apply QC signal normalization if specified, apply transformation if specified, apply normalization if specified) using NOREVA's normulticlassmatrix function with the corresponding workflow code.: "Load the multi-class peak matrix and metadata into R using Biobase ExpressionSet format. 2. Select and apply the chosen preprocessing workflow sequence (impute missing values if specified, apply QC"
- [intro] The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing: "The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing"
- [readme] This function enables the performance assessment of metabolomic data processing for multi-class dataset (with quality control sample but without internal standard) using four criteria, and can scan thousands of processing workflows and rank them based on their performances.: "This function enables the performance assessment of metabolomic data processing for multi-class dataset (with quality control sample but without internal standard) using four criteria, and can scan"
- [readme] NOREVA version 2.1.1 realizes (1) the parallel computing together with memory management and (2) the optimization of I/O efficiency.: "NOREVA version 2.1.1 realizes (1) the parallel computing together with memory management and (2) the optimization of I/O efficiency."
