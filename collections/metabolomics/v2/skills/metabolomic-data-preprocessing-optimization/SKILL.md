---
name: metabolomic-data-preprocessing-optimization
description: Use when you have multi-class or time-course metabolomic peak tables (with or without quality control samples and/or internal standards) and need to select the preprocessing workflow from hundreds of candidate combinations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
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
  - Biobase
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
---

# metabolomic-data-preprocessing-optimization

## Summary

Systematic evaluation and ranking of metabolomic data preprocessing workflows for multi-class or time-course studies using five integrated assessment criteria, each grounded in distinct theoretical frameworks. This skill enables discovery of optimal preprocessing methods that maximize biomarker signal recovery and minimize artifactual variation.

## When to use

You have multi-class or time-course metabolomic peak tables (with or without quality control samples and/or internal standards) and need to select the best preprocessing workflow from hundreds of candidate combinations. Trigger this skill when: (1) you are performing biomarker discovery or differential profiling requiring validated preprocessing, (2) your peak table is in standardized or software-generated format (e.g., from 12 available software tools), and (3) you want rankings across four to five distinct assessment perspectives rather than a single metric.

## When NOT to use

- Your metabolomic data is already fully preprocessed or normalized; this skill requires raw or minimally processed peak tables with batch and technical variation.
- You have only a single or two samples per group; NOREVA's assessment criteria are calibrated for studies with sufficient replication to estimate reproducibility and statistical power.
- Your data type is not multi-class or time-course (e.g., case-control binary comparison without time dimension) — single-class or binary designs may require alternative NOREVA functions not described here.

## Inputs

- peak table in standardized NOREVA format or customized format from 12 supported software tools
- label file defining multi-class or time-course sample groupings (optional but required for class/time-point assignment)
- quality control sample annotations (if present in dataset)
- internal standard column indices (if applicable)

## Outputs

- OUTPUT-NOREVA-Overall.Ranking.Data.csv containing all preprocessing workflows ranked by composite performance scores
- individual assessment criterion outputs corresponding to the five integrated criteria
- processed peak table for the top-ranked workflow

## How to apply

First, prepare your peak table and optional label file using PrepareInuputFiles(), specifying the data format (standardized format '1' or customized format '2' from supported software). Choose the NOREVA function matching your dataset structure: normulticlassqcall() for multi-class data with QC samples, normulticlassnoall() for multi-class without QC/internal standards, normulticlassisall() for multi-class with internal standards, or the corresponding nortimecourse variants for time-course studies. Specify study assumptions (SAalpha, SAbeta, SAgamma) reflecting whether metabolites are equally important, have constant abundance, and whether intensities are stable across conditions. The function scans thousands of preprocessing workflows and applies five well-established criteria—each with distinct underlying theory—to rank all workflows comprehensively. Extract and validate the OUTPUT-NOREVA-Overall.Ranking.Data.csv file, which provides ranked workflows with scores across the four primary assessment dimensions.

## Related tools

- **NOREVA** (Primary R package executing preprocessing workflows, applying integrated assessment criteria (alpha, beta, gamma study assumptions), and generating ranked workflow output) — https://github.com/idrblab/NOREVA
- **R** (Runtime environment (≥3.5) required to load and execute NOREVA functions) — https://www.r-project.org/
- **Biobase** (Bioconductor dependency for expression set data structures and metabolomic data representation)
- **pcaMethods** (Bioconductor dependency providing principal component analysis for feature reduction and assessment criteria computation)
- **limma** (Bioconductor dependency for differential abundance testing and fold-change estimation within assessment workflows)
- **statTarget** (Bioconductor dependency for batch correction and quality control sample normalization)
- **multtest** (Bioconductor dependency for multiple testing correction in statistical assessment criteria)
- **impute** (Bioconductor dependency for handling missing values in metabolomic peak tables)
- **ProteoMM** (Bioconductor dependency for metabolomic data normalization methods)

## Examples

```
library(NOREVA); PrepareInuputFiles(dataformat='1', rawdata='peak_table.csv', label='sample_labels.txt'); normulticlassqcall(fileName='prepared_data', SAalpha='Y', SAbeta='Y', SAgamma='Y')
```

## Evaluation signals

- OUTPUT-NOREVA-Overall.Ranking.Data.csv is generated and contains all expected preprocessing workflows with non-missing scores across all four primary assessment dimensions.
- Ranking table includes at least one workflow in top 10% across all five assessment criteria, indicating stable overall performance.
- Study assumption parameters (SAalpha, SAbeta, SAgamma) match your data characteristics; inconsistent assumptions produce invalid rankings.
- Reproducibility criterion scores (typically derived from QC sample clustering or within-group variance) show >0.7 for top-ranked workflows if QC samples are present.
- Top-ranked workflow's differential abundance signal (measured by fold-change recovery or statistical power criterion) aligns with known or expected metabolite intensity changes in your experimental conditions.

## Limitations

- Computation time scales with workflow count and sample/feature size; NOREVA v2.1.1+ implements parallel computing and memory management but may require high-performance resources for very large datasets.
- Assessment criteria assume adequate replication within each multi-class group or time-point; sparse or unbalanced designs may yield unreliable rankings.
- The five integrated assessment criteria reflect consensus best practices but may not capture domain-specific priorities (e.g., preservation of specific metabolite classes or isotopologue ratios); users should validate top-ranked workflows against their own biological knowledge.
- Quality control sample assessment assumes QC samples are metabolically representative of study samples; non-representative QC design compromises QC-based criteria.
- The function generates rankings for all workflows independently; no a priori selection of workflow subset is performed—users must interpret and select from the full ranked list.

## Evidence

- [readme] The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing workflows.: "The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing"
- [readme] five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion.: "five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation"
- [intro] This study provides guidelines for researchers who will engage in biomarker discovery or other differential profiling omics studies with respect selecting the most appropriate preprocessing method: "provides guidelines for researchers who will engage in biomarker discovery or other differential profiling omics studies with respect selecting the most appropriate preprocessing method"
- [other] normulticlassqcall function generates OUTPUT-NOREVA-Overall.Ranking.Data.csv, which ranks all processing workflows under multiple assessment criteria for multi-class metabolomic data with quality control samples.: "normulticlassqcall function generates OUTPUT-NOREVA-Overall.Ranking.Data.csv, which ranks all processing workflows under multiple assessment criteria for multi-class metabolomic data"
- [other] Apply the five integrated assessment criteria (each with distinct underlying theory) to evaluate all preprocessing workflows.: "Apply the five integrated assessment criteria (each with distinct underlying theory) to evaluate all preprocessing workflows."
