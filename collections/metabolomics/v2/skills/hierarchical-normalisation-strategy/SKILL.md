---
name: hierarchical-normalisation-strategy
description: Use when when you have multiple batches of metabolomics data with embedded
  intra-batch (short) and inter-batch (batch) replicate samples, visible run-order
  signal drift in individual metabolites within batches, and batch effects visible
  in PCA or run plots.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - hRUV
  - RUV-III
  - R
  - dplyr
  - SummarizedExperiment
  license_tier: open
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data
  in a hierarchical strategy'
- 'utilises 2 types of replicates: intra-batch and inter-batch replicates to estimate
  the unwanted variation within and between batches with RUV-III'
- Install the R package from GitHub using the `devtools` package
- we will load the hRUV package and other packages required for the demonstration...
  library(dplyr)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hierarchical-normalisation-strategy

## Summary

A batch-aware normalisation approach for multi-batch metabolomics data that applies intra-batch signal drift correction via loess smoothing and RUV-III, followed by inter-batch unwanted variation removal using hierarchical sample replicate information. This skill targets metabolomics studies where sample replicates are embedded across experimental runs and batches.

## When to use

When you have multiple batches of metabolomics data with embedded intra-batch (short) and inter-batch (batch) replicate samples, visible run-order signal drift in individual metabolites within batches, and batch effects visible in PCA or run plots. Use this skill to eliminate both drift and batch effects before downstream statistical analysis or biomarker discovery.

## When NOT to use

- Input data does not contain embedded intra-batch and inter-batch replicate samples; hierarchical RUV-III requires these structured replicates.
- Single-batch metabolomics data without inter-batch variation; intra-batch loess smoothing alone may suffice.
- Metabolomics assay already pre-normalised or batch-corrected by another method; applying hRUV may introduce redundant or conflicting corrections.

## Inputs

- SummarizedExperiment object with 'raw' assay containing metabolite signal intensities across multiple experimental batches
- Sample metadata columns specifying batch assignment and replicate type (intra-batch/inter-batch)

## Outputs

- SummarizedExperiment object with new normalised assay (e.g. 'loessShort_concatenate') containing drift-corrected and batch-corrected metabolite signals
- Diagnostic run plots (hRUV::plotRun output) showing signal intensity vs. run order for specified metabolites

## How to apply

First, log-transform the raw assay using log2(raw + 1), then apply hRUV::clean with threshold=0.5 and method='intersect' to filter metabolites with >50% missing values per batch and retain only those quantified across all batches. Next, call the hRUV function with intra='loessShort' (non-linear loess smoothing + RUV-III with k=5 on short replicates for intra-batch correction) and inter='concatenate' (hierarchical structure using batch replicate samples with k=5 for inter-batch RUV-III). Extract the resulting normalised assay (e.g. loessShort_concatenate) and verify correction by comparing hRUV::plotRun diagnostic plots before (rawImpute) and after normalisation to confirm elimination of run-order drift and batch clustering artifacts.

## Related tools

- **hRUV** (Main normalisation package implementing hierarchical RUV-III with loess smoothing for intra- and inter-batch correction) — https://github.com/SydneyBioX/hRUV
- **RUV-III** (Unwanted variation estimation and removal using replicate sample information within and between batches)
- **SummarizedExperiment** (Container class for storing raw and normalised assays with associated sample and feature metadata)
- **dplyr** (Data manipulation and metadata handling during workflow)

## Examples

```
dat_list = hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute"); dat_norm = hRUV::hruv(dat_list, intra='loessShort', inter='concatenate', intra_k=5, inter_k=5)
```

## Evaluation signals

- Run plots (hRUV::plotRun) show elimination of monotonic signal drift and run-order trends visible in rawImpute assay; normalised assay should display flat, horizontal signal patterns across run order.
- PCA plots of loessShort_concatenate assay show batch clustering eliminated compared to rawImpute; samples should cluster by biological phenotype rather than batch identity.
- Metabolites previously exhibiting strong batch effects (e.g. GlucosePos2) and signal drift (e.g. 1-methylhistamine) display stable, batch-independent intensity distributions in normalised assay.
- No introduction of artificial structure or within-batch compression; replicate samples should remain co-located in normalised space and biological sample variance should be preserved.
- Successful extraction of normalised assay from returned SummarizedExperiment object with correct dimensions (same features × samples as input) and no missing values where input had valid measurements after cleaning.

## Limitations

- Requires well-designed replicate embedding scheme; suboptimal placement of intra-batch and inter-batch replicates may reduce effectiveness of unwanted variation estimation.
- Method assumes linear or smooth non-linear (loess) relationship between signal and run order; abrupt instrumental failures or calibration jumps may not be fully corrected.
- Removes variation associated with batch/run; if biological signal is confounded with batch structure, normalisation may inadvertently remove true biological effects.
- Performance depends on k parameter choice (k=5 used in examples); different study designs or replicate densities may require parameter tuning.

## Evidence

- [readme] hRUV hierarchical approach and RUV-III mechanism: "hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the seequence of experimental runs/batches and applying signal drift correction with"
- [intro] Log transformation step: "assay(dat, "logRaw", withDimnames = FALSE) = log2(assay(dat, "raw") + 1)"
- [intro] Data cleaning parameters and filtering rationale: "dat_list = hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute")"
- [intro] Intra-batch normalisation specification: "For intra batch normalisation, we perform loess smoothing on samples and RUV-III using short replicates with parameter k set to 5"
- [intro] Inter-batch normalisation specification: "For inter batch normalisation, we perform concatenating hierarchical structure using batch replicate samples"
- [full_text] Expected outcome: drift and batch effect elimination: "hRUV normalisation eliminates signal drift in 1-methylhistamine and strong batch effects in GlucosePos2 that were present in the rawImpute assay"
