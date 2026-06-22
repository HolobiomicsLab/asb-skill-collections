---
name: ruv-iii-implementation-in-metabolomics
description: Use when you have metabolomics data distributed across multiple experimental batches, each batch contains sample replicates (the same sample measured multiple times within and across batches), PCA or visual inspection reveals systematic batch effects, and you need to distinguish unwanted variation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - hRUV
  - RUV-III
  - R
  - SummarizedExperiment
  - DMwR2
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy'
- 'utilises 2 types of replicates: intra-batch and inter-batch replicates to estimate the unwanted variation within and between batches with RUV-III'
- Install the R package from GitHub using the `devtools` package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hruv_cq
    doi: 10.1101/2020.12.21.423723
    title: hRUV
  dedup_kept_from: coll_hruv_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.12.21.423723
  all_source_dois:
  - 10.1101/2020.12.21.423723
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# RUV-III implementation in metabolomics

## Summary

Apply RUV-III (Removal of Unwanted Variation III) within the hRUV hierarchical framework to remove batch effects from metabolomics data by leveraging intra-batch and inter-batch sample replicates. This skill corrects signal drift across experimental runs while preserving biological signal.

## When to use

Use this skill when you have metabolomics data distributed across multiple experimental batches, each batch contains sample replicates (the same sample measured multiple times within and across batches), PCA or visual inspection reveals systematic batch effects, and you need to distinguish unwanted variation from true biological signal while preserving metabolite abundance patterns.

## When NOT to use

- Input data lacks replicate samples embedded within or across batches (RUV-III requires replicates to estimate unwanted variation factors)
- Data is already normalised or batch-corrected by an orthogonal method (e.g. ComBat, SVA) and re-normalisation may over-correct
- Metabolomics assay is not on a comparable scale (e.g. already heavily filtered or feature-selected to a small subset)

## Inputs

- SummarizedExperiment object with 'raw' assay
- Batch assignment metadata (experimental run/batch identifiers)
- Replicate metadata (intra-batch and inter-batch replicate sample identifiers)

## Outputs

- SummarizedExperiment object with 'loessShort_concatenate' normalised assay
- Batch-corrected metabolite abundance matrix (log2-scale)
- Unwanted variation estimates (RUV-III factors W per batch)

## How to apply

First, load your metabolomics data as a SummarizedExperiment object with batch and replicate metadata annotations. Apply log transformation (log2(raw + 1)) to the raw assay and perform data cleaning (threshold filtering >50% missing values per batch, k-nearest neighbour imputation) to create a rawImpute assay. Then call the hRUV function with two stages: (1) intra-batch normalisation using RUV-III with k=5 short replicates and loessShort non-linear smoothing to correct signal drift within each batch, and (2) inter-batch normalisation using RUV-III with k=5 batch replicates and concatenate hierarchical structure to align replicates across batches. Extract the resulting normalised assay and verify batch effect removal by PCA plot inspection—batch clusters should dissolve while replicate samples should cluster together.

## Related tools

- **hRUV** (Main R package implementing hierarchical RUV-III workflow with intra-batch and inter-batch normalisation stages) — https://github.com/SydneyBioX/hRUV
- **RUV-III** (Statistical method for estimating and removing unwanted variation using replicate sample information)
- **SummarizedExperiment** (Bioconductor container class for storing metabolomics abundance matrix with batch and replicate annotations)
- **DMwR2** (R package providing k-nearest neighbour imputation for missing metabolite values during data cleaning)

## Examples

```
library(hRUV); library(SummarizedExperiment); dat <- hRUV::hRUV(dat, intra='loessShort', inter='concatenate', intra_k=5, inter_k=5); loessShort_concatenate_assay <- assay(dat, 'loessShort_concatenate')
```

## Evaluation signals

- PCA plots before and after normalisation: batch clusters should be eliminated or substantially reduced while replicate samples remain clustered together
- Replicate correlation: intra-batch and inter-batch replicate pairs should exhibit high correlation (Pearson r > 0.9) in the normalised assay
- No systematic trend in metabolite abundance vs. batch order (inspect loess smoothing residuals to confirm signal drift correction)
- Metabolite quantification consistency: metabolites with >50% missing values per batch should have been filtered; remaining metabolites should be quantified across all batches (intersect method)
- RUV-III factor W convergence: unwanted variation estimates should stabilise across iterations, indicating successful factor estimation from replicates

## Limitations

- Requires careful embedding of replicate samples within and between batches; arbitrary replicate placement may degrade unwanted variation estimation
- Performance depends on replicate quality—if replicate samples are contaminated or not genuinely identical, RUV-III will estimate inflated unwanted variation factors
- Intra-batch loessShort smoothing is a non-linear approximation; may oversmoothes sharp metabolite intensity changes if replicate spacing is uneven
- No changelog available in repository; version compatibility and bug fixes may not be transparently documented
- Tested only on macOS Big Sur 11.1 and Linux Debian 10; behaviour on other systems not validated

## Evidence

- [readme] RUV-III method definition: "utilises 2 types of replicates: intra-batch and inter-batch replicates to estimate the unwanted variation within and between batches with RUV-III"
- [readme] Hierarchical normalisation rationale: "hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the sequence of experimental runs/batches and applying signal drift correction"
- [intro] Intra-batch normalisation workflow: "For intra batch normalisation, we perform loess smoothing on samples and RUV-III using short replicates with parameter k set to 5"
- [intro] Inter-batch normalisation workflow: "For inter batch normalisation, we perform concatenating hierarchical structure using batch replicate samples"
- [intro] Data cleaning prerequisite: "We have filtered metabolites with more than 50% of missing values per batch and selected metabolites that are quantified across all batches (intersect)"
- [other] Success metric (batch effect removal): "the resulting loessShort_concatenate assay eliminates batch effects visible in PCA plots and corrects signal drift across experimental runs"
- [intro] Input data format: "The data is already formatted in to a `SummarizedExperiment` object"
- [intro] Log transformation step: "Log transformation of raw assay: assay(dat, "logRaw", withDimnames = FALSE) = log2(assay(dat, "raw") + 1)"
