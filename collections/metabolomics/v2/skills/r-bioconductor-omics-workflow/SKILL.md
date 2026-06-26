---
name: r-bioconductor-omics-workflow
description: Use when you have a raw or partially processed multi-class or time-series
  metabolomic peak table (in standardized or software-specific format) and need to
  determine which combination of imputation, QC sample normalization, transformation,
  and metabolite/sample-based normalization methods will.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
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

# R Bioconductor omics workflow

## Summary

A systematic approach to preprocessing and assessing multi-class or time-series metabolomic datasets using NOREVA, integrating imputation, QC correction, transformation, and normalization steps to identify optimal processing workflows. This skill enables high-throughput evaluation of thousands of preprocessing combinations against multiple criteria to guide biomarker discovery and differential profiling studies.

## When to use

Apply this skill when you have a raw or partially processed multi-class or time-series metabolomic peak table (in standardized or software-specific format) and need to determine which combination of imputation, QC sample normalization, transformation, and metabolite/sample-based normalization methods will best preserve biological signal while minimizing technical variation. Use it especially when your study involves quality control samples, internal standards, or time-course data and you must evaluate hundreds of preprocessing workflows systematically rather than applying a single fixed pipeline.

## When NOT to use

- Your input is already a finalized feature table or has been preprocessed by a single fixed pipeline that you are confident about — use this skill only when you need to optimize and evaluate multiple preprocessing strategies
- Your dataset is not metabolomic or does not fit the multi-class/time-series structure that NOREVA assumes
- Your analysis goal is downstream statistical modeling or machine learning (e.g., biomarker classification) rather than preprocessing optimization — apply this skill before those downstream steps

## Inputs

- Raw or partially processed peak table (standardized NOREVA format or software tool output format)
- Metadata/label file (for multi-class or time-course annotation)
- Quality control sample identifiers (optional, if present in dataset)
- Internal standard column identifiers (optional, if present in dataset)

## Outputs

- Processed peak table (ExpressionSet object, exportable to CSV)
- Ranked workflow performance metrics across five evaluation criteria
- Assessment scores for all scanned preprocessing combinations

## How to apply

First, prepare your input peak table and metadata using PrepareInputFiles(), specifying dataformat (1 for standardized NOREVA format, 2 for software tool output), rawdata filename, and label file for multi-class or time-course annotation. Then select the appropriate assessment function based on your dataset structure: normulticlassqcall() for multi-class with QC samples, normulticlassnoall() for multi-class without QC/IS, normulticlassisall() for multi-class with internal standards, or nortimecourse variants for time-course data. Configure study assumptions (SAalpha, SAbeta, SAgamma) reflecting whether all metabolites are equally important, abundance is constant across samples, and whether most metabolite intensities should remain unchanged. The function will iterate through preprocessing workflows combining: imputation methods (codes 1–4), QC correction techniques (codes 1–3), transformation approaches (codes 1–3), and normalization strategies (codes 1–20 spanning metabolite-based, sample-based, or combined methods). Extract the processed peak table from the output ExpressionSet object and evaluate ranking of workflows using NOREVA's five integrated criteria (each with distinct underlying theory) to select the best-performing preprocessing method for your specific dataset and study assumptions.

## Related tools

- **NOREVA** (Primary package for preprocessing, assessment, and workflow optimization of multi-class/time-series metabolomic data) — https://github.com/idrblab/NOREVA
- **Biobase** (Provides ExpressionSet data structure for storing and manipulating multi-class metabolomic matrices with metadata)
- **impute** (Implements missing value imputation methods (part of imputation workflow codes 1–4))
- **statTarget** (Provides QC sample-based signal normalization and correction methods)
- **limma** (Supports variance stabilization and normalization transformations)
- **pcaMethods** (Provides dimensionality reduction and transformation methods for preprocessing evaluation)
- **R** (Runtime environment (≥3.5 required) for executing NOREVA workflow) — https://www.r-project.org/

## Examples

```
library(NOREVA); prepared <- PrepareInuputFiles(dataformat=1, rawdata='peak_table.csv', label='sample_labels.csv'); result <- normulticlassqcall(fileName=prepared, SAalpha='Y', SAbeta='Y', SAgamma='Y'); write.csv(exprs(result), 'processed_peak_table.csv')
```

## Evaluation signals

- Processed peak table has no missing values (imputation verified) and row/column counts match input dimensions
- QC sample intensities show reduced inter-sample variance and improved batch alignment if QC correction was applied
- Transformation applied (if selected) results in data closer to normal distribution or homoscedasticity (verifiable via log/sqrt/Box-Cox plots)
- Ranked workflow outputs from assessment function are sorted by composite score across five criteria; top-ranked workflow should be reproducible and interpretable
- Output ExpressionSet object metadata (phenoData, featureData, assayData) correctly reflect the input annotation and processed intensity values

## Limitations

- NOREVA assumes metabolomic data structure (peak intensity matrix); not applicable to other omics types without modification
- Study assumptions (SAalpha, SAbeta, SAgamma) must be set by the user based on biological knowledge; incorrect assumptions may rank inappropriate workflows as optimal
- Computational time and memory scale with dataset size and number of workflows to evaluate; version 2.1.1+ addresses this with parallel computing and memory management, but very large datasets may still be slow
- The five integrated evaluation criteria may disagree on optimal workflow ranking; users must prioritize criteria according to their downstream analysis goals (e.g., biomarker discovery vs. differential profiling)
- Quality control samples or internal standards must be clearly annotated in the input metadata; misannotation will cause QC-based or IS-based correction to fail or mislead rankings

## Evidence

- [other] The normulticlassmatrix function accepts a datatype parameter (1, 2, or 3 for datasets without QCSs/ISs, with QCSs, or with ISs respectively): "The normulticlassmatrix function accepts a datatype parameter (1, 2, or 3 for datasets without QCSs/ISs, with QCSs, or with ISs respectively), a prepared fileName, optional IS column identifiers, and"
- [readme] Five well-established criteria, each with a distinct underlying theory, are integrated to ensure comprehensive evaluation: "Particularly, five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion."
- [other] Load the multi-class peak matrix and metadata into R using Biobase ExpressionSet format: "Load the multi-class peak matrix and metadata into R using Biobase ExpressionSet format. 2. Select and apply the chosen preprocessing workflow sequence"
- [readme] NOREVA enables pre-processing and assessment of multi-class/time-series metabolomic data but also realize high-throughput discovery of the well-performing pre-processing: "The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing"
- [readme] NOREVA version 2.1.1 realizes the parallel computing together with memory management and the optimization of I/O efficiency: "NOREVA version 2.1.1 realizes (1) the parallel computing together with memory management and (2) the optimization of I/O efficiency."
- [readme] This study provides guidelines for researchers who will engage in biomarker discovery or other differential profiling omics studies with respect selecting the most appropriate preprocessing method: "This study provides guidelines for researchers who will engage in biomarker discovery or other differential profiling "omics" studies with respect selecting the most appropriate preprocessing method"
