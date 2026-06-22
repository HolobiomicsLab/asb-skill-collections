---
name: multi-criteria-performance-evaluation
description: Use when you have preprocessed multi-class or time-course metabolomic peak tables (with or without quality control samples and/or internal standards) and need to compare multiple preprocessing workflows to identify which performs for biomarker discovery or differential profiling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
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

# multi-criteria-performance-evaluation

## Summary

Systematically rank metabolomic preprocessing workflows by applying five independent assessment criteria (each grounded in distinct statistical theory) to generate a comprehensive comparative performance table. This skill enables discovery of optimal preprocessing pipelines across multiple evaluation perspectives rather than relying on a single criterion.

## When to use

You have preprocessed multi-class or time-course metabolomic peak tables (with or without quality control samples and/or internal standards) and need to compare multiple preprocessing workflows to identify which performs best for biomarker discovery or differential profiling. Apply this skill when you want rankings across four or five distinct assessment dimensions simultaneously rather than optimizing for a single metric.

## When NOT to use

- Input peak table is already normalized or feature-selected; this skill evaluates raw preprocessing workflows, not post-hoc feature engineering.
- Single-class or case-control designs without time-course or multi-class structure; NOREVA requires multi-group comparison.
- Untargeted metabolomics data requiring molecular identification or spectral matching; this skill ranks preprocessing only, not annotation workflows.

## Inputs

- Standardized peak table (rows=metabolites, columns=samples; or format from 12 supported preprocessing software tools)
- Sample label file (for time-course or multi-class group assignments)
- Quality control sample designations (optional, for QC-aware functions)
- Internal standard column indices (optional, for IS-aware functions)

## Outputs

- OUTPUT-NOREVA-Overall.Ranking.Data.csv (ranking table with all workflows, scores across five assessment criteria, and comparative rankings)
- Individual workflow performance metrics across four primary assessment dimensions

## How to apply

First, prepare your raw peak table and sample labels using PrepareInuputFiles() to standardize format. Then, select the appropriate NOREVA function based on your experimental design: use normulticlassqcall() for multi-class data with QC samples, normulticlassnoall() for multi-class without QC, normulticlassisall() for multi-class with internal standards, or corresponding time-course variants. Specify study assumptions (SAalpha, SAbeta, SAgamma) that reflect whether all metabolites should be weighted equally, metabolite abundance is constant across samples, and whether most metabolite intensities remain unchanged under study conditions. The function applies five integrated criteria—each with distinct underlying statistical theory—to scan and rank all available preprocessing workflows. Validation involves confirming that the output ranking table (OUTPUT-NOREVA-Overall.Ranking.Data.csv) contains all workflows with assigned scores and comparative rankings across the four primary assessment dimensions.

## Related tools

- **NOREVA** (Core R package that implements multi-criteria ranking via normulticlassqcall, normulticlassnoall, normulticlassisall, and time-course variants; integrates five assessment criteria for comprehensive workflow evaluation) — https://github.com/idrblab/NOREVA
- **Biobase** (Provides ExpressionSet data structures used by NOREVA for standardized metabolomic data representation)
- **pcaMethods** (Enables PCA-based assessment criterion within NOREVA's multi-criteria framework)
- **limma** (Supports differential abundance testing as part of NOREVA's performance assessment criteria)
- **statTarget** (Provides QC-based preprocessing and batch correction options evaluated by NOREVA's ranking system)

## Examples

```
library(NOREVA); normulticlassqcall(fileName="Multiclass_with_QCS", SAalpha="Y", SAbeta="Y", SAgamma="Y")
```

## Evaluation signals

- Output file OUTPUT-NOREVA-Overall.Ranking.Data.csv exists and contains all available preprocessing workflows with non-null scores
- Ranking table includes scores for all five integrated assessment criteria (or four for non-QC variants); values are numeric and within expected ranges
- Each workflow appears exactly once in the ranking with a comparative rank position across all assessment dimensions
- Study assumption parameters (SAalpha, SAbeta, SAgamma) are correctly reflected in the assessment logic applied to the dataset
- Workflow rankings differ across assessment criteria, demonstrating that multi-dimensional evaluation identified trade-offs rather than uniform ranking

## Limitations

- Requires adequate sample size and metabolite coverage; sparse or highly filtered peak tables may yield unstable criterion estimates.
- Assumes that metabolite intensities and quality control samples (when used) are suitable for the selected assessment criteria; misaligned study assumptions (e.g., setting SAalpha='Y' when metabolites have heterogeneous importance) will bias rankings.
- Computational cost scales with number of workflows and sample count; NOREVA v2.1.1 optimizes parallel computing and I/O, but very large datasets may require memory management.
- Ranking depends on choice of study assumptions; different SAalpha/SAbeta/SAgamma combinations may yield substantially different performance orders for the same workflows.

## Evidence

- [other] The normulticlassqcall function generates OUTPUT-NOREVA-Overall.Ranking.Data.csv, which ranks all processing workflows under multiple assessment criteria for multi-class metabolomic data with quality control samples.: "The normulticlassqcall function generates OUTPUT-NOREVA-Overall.Ranking.Data.csv, which ranks all processing workflows under multiple assessment criteria for multi-class metabolomic data with quality"
- [intro] Five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion.: "five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion"
- [other] This skill applies five integrated assessment criteria to evaluate all preprocessing workflows.: "Apply the five integrated assessment criteria (each with distinct underlying theory) to evaluate all preprocessing workflows."
- [intro] The NOREVA package enables pre-processing and assessment of multi-class/time-series metabolomic data and high-throughput discovery of well-performing preprocessing methods.: "The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing"
- [readme] This function enables the performance assessment of metabolomic data processing for multi-class dataset (with quality control sample but without internal standard) using four criteria, and can scan thousands of processing workflows and rank them based on their performances.: "This function enables the performance assessment of metabolomic data processing for multi-class dataset (with quality control sample but without internal standard) using four criteria, and can scan"
