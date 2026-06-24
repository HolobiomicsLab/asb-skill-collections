---
name: preprocessing-workflow-comparative-ranking
description: Use when you have multi-class or time-course metabolomic peak table data
  (raw or already peak-detected) with or without quality control samples and/or internal
  standards, and you need to evaluate which preprocessing workflow (normalization,
  imputation, scaling combination) will yield the most.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NOREVA
  - devtools
  - BiocManager
  - pcaMethods
  - multtest
  - limma
  - impute
  - statTarget
  - ProteoMM
  license_tier: open
derived_from:
- doi: 10.1038/s41596-021-00636-9
  title: NOREVA
evidence_spans:
- '[![R >3.5](https://img.shields.io/badge/R-%3E3.5-success.svg)](https://www.r-project.org/)'
- devtools::install_github("idrblab/NOREVA")
- '![installed with devtools](https://img.shields.io/badge/installed%20with-devtools-blueviolet.svg)'
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
- BiocManager::install("pcaMethods")
- BiocManager::install("multtest")
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

# preprocessing-workflow-comparative-ranking

## Summary

Rank multiple metabolomic preprocessing workflows against each other using five integrated assessment criteria—each grounded in distinct statistical theory—to identify the highest-performing workflow for a given dataset. This skill selects the most appropriate preprocessing method for biomarker discovery or differential profiling by scanning thousands of workflow combinations and scoring them across multiple dimensions.

## When to use

You have multi-class or time-course metabolomic peak table data (raw or already peak-detected) with or without quality control samples and/or internal standards, and you need to evaluate which preprocessing workflow (normalization, imputation, scaling combination) will yield the most reproducible, discriminative, or stable results for downstream biomarker discovery or differential profiling.

## When NOT to use

- Input is already a quality-controlled, normalized feature table from a validated preprocessing pipeline—ranking is intended for discovery and selection among candidate workflows, not validation of finalized pipelines.
- You lack sample class labels or time-point assignments—all ranking functions require categorical sample metadata to compute discrimination and stability metrics.
- Data are single-class or single time-point with no replication—ranking criteria depend on variance between groups or temporal trends, which require ≥2 sample classes or time-points.

## Inputs

- peak intensity table (rows: metabolites/ions, columns: samples) in standardized NOREVA format or one of 12 external metabolomic software formats (12 formats supported by PrepareInuputFiles)
- sample class labels or time-course time-point labels file
- optional: quality control sample identifiers (if applicable to study design)
- optional: internal standard metabolite column indices (if applicable to study design)

## Outputs

- OUTPUT-NOREVA-Overall.Ranking.Data.csv: ranked table of all tested preprocessing workflows with performance scores across four primary assessment dimensions and comparative rankings
- preprocessing workflow recommendations ranked by performance across multiple assessment criteria

## How to apply

First, prepare your peak table and sample labels using PrepareInuputFiles(), specifying the input format (standardized NOREVA format or one of 12 external software formats). Then invoke the appropriate NOREVA ranking function matching your data structure: normulticlassqcall() for multi-class data with QC samples, normulticlassnoall() for multi-class without QC/internal standards, normulticlassisall() for multi-class with internal standards, nortimecourseqcall() for time-course with QC, or nortimecoursenoall() for time-course without QC/internal standards. Declare which study assumptions your data satisfies (SAalpha, SAbeta, SAgamma representing equal metabolite importance, constant abundance levels, and unchanged intensities under study conditions, respectively). The function automatically scans thousands of preprocessing workflow combinations, applies five independent assessment criteria (each testing a different theoretical perspective on data quality), and outputs a ranked CSV table (OUTPUT-NOREVA-Overall.Ranking.Data.csv) scoring all workflows. Select the top-ranked workflow based on the assessment dimension most relevant to your downstream analysis goal.

## Related tools

- **NOREVA** (Core package executing preprocessing workflow scanning and comparative ranking via five integrated assessment criteria) — https://github.com/idrblab/NOREVA
- **R** (Execution environment (≥3.5 required)) — https://www.r-project.org/
- **devtools** (Package installation and dependency management)
- **BiocManager** (Installation of Bioconductor dependencies (Biobase, pcaMethods, multtest, limma, impute, statTarget, ProteoMM, timecourse, ropls, vsn, affy))
- **statTarget** (Quality control sample-based batch correction and normalization workflows evaluated in ranking)
- **ProteoMM** (Proteomics-oriented normalization and preprocessing methods evaluated in ranking)
- **limma** (Linear regression and differential abundance testing integrated into assessment criteria)
- **pcaMethods** (Principal component analysis and imputation methods for preprocessing evaluation)

## Examples

```
library(NOREVA); data <- PrepareInuputFiles(dataformat='1', rawdata='peak_table.csv', label='sample_labels.txt'); normulticlassqcall(fileName=data, SAalpha='Y', SAbeta='Y', SAgamma='Y')
```

## Evaluation signals

- OUTPUT-NOREVA-Overall.Ranking.Data.csv contains rows for all evaluated preprocessing workflows (typically hundreds to thousands) with no missing entries.
- Each workflow is assigned numeric performance scores across all five assessment criteria with rankings (e.g., 1=best, N=worst) without ties or NaN values in ranking columns.
- Top-ranked workflows show consistent or complementary rankings across the four or five primary assessment dimensions, indicating robust preprocessing performance.
- Study assumption declarations (SAalpha, SAbeta, SAgamma) correctly match the input data characteristics (e.g., SAalpha='Y' if all metabolites weighted equally; SAalpha='N' if some metabolites are known biomarkers with higher importance).
- Output file contains columns for workflow identifiers, performance scores (numerical), and ranking positions; schema aligns with NOREVA version 2.1.1+ expected format.

## Limitations

- Ranking requires sufficient sample replication within each class or time-point to compute robust variance and discrimination metrics; heavily imbalanced or single-replicate designs may produce unreliable rankings.
- Study assumptions (SAalpha, SAbeta, SAgamma) must reflect true biological properties of the dataset; misspecification can bias ranking toward inappropriate workflows.
- NOREVA scans a fixed set of preprocessing workflows (normalization, imputation, scaling combinations) built into the package; novel or custom preprocessing methods not in the library cannot be ranked.
- Computational cost scales with number of workflows and samples; version 2.1.1+ includes parallel computing and memory optimization, but very large datasets (>10,000 metabolites, >1,000 samples) may require high-performance computing resources.
- Rankings are comparative and relative to the chosen assessment criteria; a 'best' workflow for one criterion may rank poorly on another, requiring selection based on downstream analysis goals (e.g., biomarker discovery vs. reproducibility).

## Evidence

- [other] The normulticlassqcall function generates OUTPUT-NOREVA-Overall.Ranking.Data.csv, which ranks all processing workflows under multiple assessment criteria for multi-class metabolomic data with quality control samples.: "The normulticlassqcall function generates OUTPUT-NOREVA-Overall.Ranking.Data.csv, which ranks all processing workflows under multiple assessment criteria for multi-class metabolomic data with quality"
- [intro] Five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion.: "five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion"
- [intro] The NOREVA package enables high-throughput discovery of well-performing pre-processing workflows and provides guidelines for selecting appropriate preprocessing methods.: "The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing"
- [readme] This function enables the performance assessment of metabolomic data processing for multi-class dataset (with quality control sample but without internal standard) using four criteria, and can scan thousands of processing workflows and rank them based on their performances.: "This function enables the performance assessment of metabolomic data processing for multi-class dataset (with quality control sample but without internal standard) using four criteria, and can scan"
- [readme] NOREVA version 2.1.1 realizes (1) the parallel computing together with memory management and (2) the optimization of I/O efficiency.: "NOREVA version 2.1.1 realizes (1) the parallel computing together with memory management and (2) the optimization of I/O efficiency"
