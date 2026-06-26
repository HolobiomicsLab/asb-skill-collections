---
name: qc-signal-normalization
description: Use when your metabolomic dataset contains dedicated QC samples (pooled
  or standard reference material injected at intervals throughout the analytical sequence)
  and you observe intensity drift, batch effects, or systematic signal variation correlated
  with run order or acquisition time rather than.
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
  provenance_tier: literature
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

# QC-Signal Normalization

## Summary

Corrects systematic signal drift and batch effects in metabolomic peak tables using quality control (QC) samples acquired during the analytical run. This skill is essential when QC samples are available and metabolite intensities show run-order or instrumental variation that could confound biological signal.

## When to use

Your metabolomic dataset contains dedicated QC samples (pooled or standard reference material injected at intervals throughout the analytical sequence) and you observe intensity drift, batch effects, or systematic signal variation correlated with run order or acquisition time rather than biological condition. Apply this skill before downstream differential profiling or biomarker discovery.

## When NOT to use

- No QC samples are available in the dataset (use quality-independent normalization instead)
- QC samples show greater biological variability than technical replicates (indicates confounding QC design)
- Peak table is already QC-corrected or has had instrumental drift removed by the analytical platform

## Inputs

- Multi-class peak matrix (Biobase ExpressionSet) with QC sample annotations
- Metadata file indicating which samples are QC replicates
- Raw peak intensities (numeric matrix, samples × metabolites)

## Outputs

- QC-corrected peak table (CSV or ExpressionSet)
- Quality control report documenting signal drift reduction
- Corrected peak matrix suitable for downstream normalization or statistical analysis

## How to apply

Load the multi-class peak matrix (with QC sample annotations) into R using Biobase ExpressionSet format. Select a QC correction method code (1–3, corresponding to different QC signal normalization algorithms implemented in NOREVA or statTarget) and pass it to the normulticlassmatrix function with datatype=2 (indicating the dataset contains QC samples). The function applies the chosen QC correction algorithm to normalize metabolite intensities across all samples relative to QC signal consistency, removing run-order and instrument drift artifacts while preserving biological variation. Extract the corrected peak table and validate by plotting QC sample intensities pre- and post-correction to confirm signal stabilization and reduced variance across the run.

## Related tools

- **NOREVA** (Orchestrates QC correction workflow via normulticlassmatrix function; wraps statTarget and other QC normalization algorithms) — https://github.com/idrblab/NOREVA
- **statTarget** (Core QC signal normalization engine; implements QC-robust loess and QC-based signal correction) — https://bioconductor.org/packages/statTarget
- **Biobase** (Data container (ExpressionSet) for multi-class peak matrix and sample/QC metadata) — https://bioconductor.org/packages/Biobase
- **limma** (Optional; supports batch effect visualization and diagnosis post-QC correction) — https://bioconductor.org/packages/limma
- **R** (Runtime environment for NOREVA and statistical validation of QC correction efficacy) — https://www.r-project.org/

## Examples

```
library(NOREVA); result <- normulticlassmatrix(datatype=2, fileName='prepared_peak_matrix', method_imputation=1, method_QC=2, method_transformation=1, method_normalization=1)
```

## Evaluation signals

- QC sample intensities show reduced inter-replicate coefficient of variation (CV) post-correction; typically CV < 10–15% for well-corrected QC replicates
- Principal component analysis (PCA) plot shows QC samples clustered tightly together, indicating removal of run-order artifact
- Signal intensity drift across run order (visualized by loess smoothing or LOWESS) is flattened to near-zero residual slope post-correction
- Biological sample grouping (by treatment or class label) is preserved or improved in post-correction PCA; no artificial separation by injection order
- Metabolite-wise comparison: fold-change between biological groups is stable before and after QC correction; spurious fold-changes due to drift are eliminated

## Limitations

- QC correction efficacy depends on QC sample representativeness and sufficient replication (typically ≥ 3–5 QC replicates per batch); sparse QC sampling may fail to capture instrumental drift
- Assumes QC samples contain no biological signal and only technical variation; confounded QC design (e.g., QC samples spiked with only a subset of metabolites) can introduce bias
- Different QC correction algorithms (codes 1–3) may perform differently depending on peak table characteristics (e.g., missing-value frequency, metabolite abundance range); algorithm selection should be validated using NOREVA's assessment criteria (SAalpha, SAbeta, SAgamma)
- QC correction may not fully remove very large batch effects if batches differ fundamentally (e.g., different instruments, reagent lots); instrument cross-validation recommended for multi-site studies

## Evidence

- [other] The normulticlassmatrix function accepts a datatype parameter (1, 2, or 3 for datasets without QCSs/ISs, with QCSs, or with ISs respectively), a prepared fileName, optional IS column identifiers, and processing method codes for imputation (1–4), QC sample correction (1–3), transformation (1–3), and normalization (1–20 for metabolite-based, sample-based, or combined approaches), then outputs a single processed peak table.: "datatype parameter (1, 2, or 3 for datasets without QCSs/ISs, with QCSs, or with ISs respectively) ... processing method codes for imputation (1–4), QC sample correction (1–3), transformation (1–3),"
- [other] Select and apply the chosen preprocessing workflow sequence (impute missing values if specified, apply QC signal normalization if specified, apply transformation if specified, apply normalization if specified) using NOREVA's normulticlassmatrix function with the corresponding workflow code.: "apply QC signal normalization if specified ... using NOREVA's normulticlassmatrix function with the corresponding workflow code"
- [readme] This function enables the performance assessment of metabolomic data processing for multi-class dataset (with quality control sample but without internal standard) using four criteria, and can scan thousands of processing workflows and rank them based on their performances.: "performance assessment of metabolomic data processing for multi-class dataset (with quality control sample but without internal standard) using four criteria"
- [readme] The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing workflows.: "enables the pre-processing and assessment of multi-class/time-series metabolomic data ... discovery of the well-performing pre-processing workflows"
- [readme] five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion: "five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation"
