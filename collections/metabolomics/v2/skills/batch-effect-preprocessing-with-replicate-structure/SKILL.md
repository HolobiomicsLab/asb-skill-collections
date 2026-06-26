---
name: batch-effect-preprocessing-with-replicate-structure
description: Use when you have metabolomics data from multiple experimental batches
  (≥2) with embedded replicate samples (identical samples run at different points
  within or across batches), log-transformed raw assays containing ≥50% missing values
  per batch, and a need to harmonise metabolite quantification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3365
  tools:
  - hRUV
  - R
  - dplyr
  - SummarizedExperiment
  - RUV-III
  - DMwR2
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data
  in a hierarchical strategy'
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

# batch-effect-preprocessing-with-replicate-structure

## Summary

A hierarchical preprocessing workflow for multi-batch metabolomics data that leverages intra-batch and inter-batch replicate samples to remove unwanted variation while preserving biological signal. This skill combines missing-value filtering, feature intersection across batches, k-nearest neighbour imputation, loess-based signal drift correction, and RUV-III normalisation to produce batch-corrected assays suitable for downstream analysis.

## When to use

Apply this skill when you have metabolomics data from multiple experimental batches (≥2) with embedded replicate samples (identical samples run at different points within or across batches), log-transformed raw assays containing ≥50% missing values per batch, and a need to harmonise metabolite quantification across batches while controlling for intra-batch drift and inter-batch systematic bias. This is particularly relevant for large-scale studies (e.g. >200 samples, >5 batches) where batch effects dominate biological variance.

## When NOT to use

- Input contains no replicate samples embedded within or across batches—RUV-III estimation requires replicate information to decompose unwanted variation.
- Metabolomics data are already normalised, batch-corrected, or merged into a single assay—applying this workflow would destroy prior normalisation and introduce redundant imputation.
- Single-batch data or data with <50% missing values per batch—the threshold filtering and intersection logic are tuned for multi-batch studies with substantial sparsity.

## Inputs

- List of SummarizedExperiment objects (one per batch)
- logRaw assay (log2-transformed raw metabolite counts)
- Metadata table defining intra-batch and inter-batch replicate sample assignments

## Outputs

- rawImpute assay (filtered, intersected, and imputed metabolite abundances)
- Intra-batch normalised assay (loess-smoothed, RUV-III corrected)
- Final inter-batch normalised assay (batch-effect corrected, ready for analysis)

## How to apply

Load each batch as a SummarizedExperiment object with a log2-transformed raw assay (logRaw = log2(raw + 1)). First, apply hRUV::clean() with threshold=0.5, method='intersect', and assay='logRaw' to filter metabolites with >50% missing values per batch, retain only metabolites quantified across all batches via the intersect method, and impute remaining missing values using k-nearest neighbour to produce a rawImpute assay. Next, perform intra-batch normalisation by applying loess smoothing on samples within each batch and RUV-III with k=5 using intra-batch replicate samples to estimate and remove unwanted variation within runs. Finally, execute inter-batch normalisation by concatenating the hierarchically structured batches and using inter-batch replicate samples to estimate and correct systematic batch-level drift. Verify that the final assay contains no missing values and metabolite counts are consistent across all samples.

## Related tools

- **hRUV** (Core normalisation package implementing the hierarchical RUV strategy, clean() function for filtering/imputation, loess smoothing, and RUV-III batch effect removal) — https://github.com/SydneyBioX/hRUV
- **SummarizedExperiment** (Data container for organising metabolite abundance matrices and metadata across batches)
- **RUV-III** (Statistical method for estimating and removing unwanted variation using replicate samples)
- **DMwR2** (Provides k-nearest neighbour imputation functionality used by hRUV::clean())
- **dplyr** (Data manipulation and tabulation of batch and replicate metadata)
- **R** (Runtime environment for executing hRUV and related statistical workflows)

## Examples

```
dat_list = hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute")
```

## Evaluation signals

- rawImpute assay contains exactly the intersection of metabolites quantified across all five batches (e.g. 61 metabolites), with no missing values and no NaN or Inf entries.
- Metabolite counts match expected post-intersect totals; verify by comparing dim(assay(dat_list[[i]], 'rawImpute')) across all batches returns identical row counts.
- Replicate samples (intra- and inter-batch) cluster together in PCA or hierarchical clustering of the normalised assay, indicating unwanted variation has been removed.
- Batch-level bias (e.g. mean or median metabolite abundance per batch) is harmonised post-normalisation, assessed via boxplots or median absolute deviation (MAD) per batch before and after inter-batch normalisation.
- Absence of NaN, Inf, or extreme outlier values in the final assay; check via summary(assay(dat_clean, 'finalAssay')) and confirm all values are finite and within biological range.

## Limitations

- Requires well-designed replicate embedding (intra-batch and inter-batch) to reliably estimate unwanted variation; sparse or imbalanced replicate designs may lead to unstable RUV-III estimates.
- The intersect method for feature selection is conservative—retains only metabolites quantified in all batches, potentially discarding batch-specific metabolites of biological interest.
- k-nearest neighbour imputation assumes missing values are missing at random (MAR); values missing due to detection limits or batch-specific failures may introduce bias.
- Threshold=0.5 is dataset-specific; applying it unchanged to metabolomics data with different sparsity patterns (e.g. very low-abundance datasets) may over-filter or under-filter metabolites.
- RUV-III parameter k=5 is tuned for the BioHEART-CT study; different replicate structures or batch sizes may require re-optimisation of k.

## Evidence

- [readme] hRUV is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy: "`hRUV` is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy with use of samples replicates in large-scale studies."
- [intro] The clean function filters metabolites with >50% missing values per batch using the intersect method, then performs k-nearest neighbour imputation: "The `clean` function filters metabolites with >50% missing values per batch using the intersect method, then performs k-nearest neighbour imputation to produce a rawImpute assay containing 61"
- [intro] Log transformation of raw assay: "assay(dat, "logRaw", withDimnames = FALSE) = log2(assay(dat, "raw") + 1)"
- [intro] Intra-batch normalisation with loess smoothing and RUV-III with k=5: "For intra batch normalisation, we perform loess smoothing on samples and RUV-III using short replicates with parameter k set to 5"
- [intro] Inter-batch normalisation with concatenating hierarchical structure: "For inter batch normalisation, we perform concatenating hierarchical structure using batch replicate samples"
- [readme] The tool utilises 2 types of replicates to estimate unwanted variation within and between batches: "The tool utilises 2 types of replicates: intra-batch and inter-batch replicates to estimate the unwatned variation within and between batches with RUV-III."
- [readme] Novel hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in experimental runs/batches: "Our novel tool is a novel hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the seequence of experimental runs/batches and applying"
