---
name: missing-value-imputation-with-k-nearest-neighbour
description: Use when you have log-transformed metabolomics data in SummarizedExperiment
  format organized as multiple batches, have already filtered metabolites with >50%
  missing values per batch and retained only those quantified across all batches via
  intersect method, and now need to impute remaining missing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - hRUV
  - R
  - dplyr
  - SummarizedExperiment
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

# missing-value-imputation-with-k-nearest-neighbour

## Summary

Apply k-nearest neighbour imputation to fill missing values in metabolomics assays after threshold-based filtering and batch intersection. This skill restores metabolite quantification across multi-batch studies by leveraging local similarity structure in the feature space.

## When to use

You have log-transformed metabolomics data in SummarizedExperiment format organized as multiple batches, have already filtered metabolites with >50% missing values per batch and retained only those quantified across all batches via intersect method, and now need to impute remaining missing values before downstream normalisation or statistical analysis.

## When NOT to use

- Input metabolomics data is already complete (no missing values) — imputation adds computational overhead without benefit.
- Missing values are >50% per batch in most metabolites — threshold filtering would eliminate too many features, leaving insufficient data for k-nearest neighbour to work reliably.
- Data is not yet log-transformed or organized as SummarizedExperiment objects — the skill expects logRaw assay as input.

## Inputs

- List of SummarizedExperiment objects, each with a logRaw assay containing log2-transformed metabolite raw counts and sample-level missing-value patterns
- Metabolomics data organized as multiple experimental batches with samples and metabolite features

## Outputs

- List of SummarizedExperiment objects with a new rawImpute assay containing imputed metabolite quantification with no missing values
- Reduced feature set: metabolites quantified across all batches with k-nearest neighbour-imputed values

## How to apply

Apply hRUV::clean() with threshold=0.5, method='intersect', assay='logRaw', and newAssay='rawImpute' to a list of SummarizedExperiment objects. The function first filters metabolites with >50% missing values per batch, retains only metabolites present in all batches using the intersect method, then performs k-nearest neighbour imputation on the filtered feature set. The resulting rawImpute assay contains complete metabolite quantification with no missing values across all samples and batches. Verify success by confirming the rawImpute assay has reduced metabolite count (relative to input) and zero missing values.

## Related tools

- **hRUV** (Primary tool: implements clean() function for threshold filtering, batch intersection, and k-nearest neighbour imputation on metabolomics batches) — https://github.com/SydneyBioX/hRUV
- **SummarizedExperiment** (Data structure: stores assays (logRaw, rawImpute), sample metadata, and feature annotations for multi-batch metabolomics objects)
- **DMwR2** (Dependency of hRUV: provides k-nearest neighbour imputation algorithm implementation)
- **dplyr** (Utility: data manipulation and pipeline composition in hRUV workflows)

## Examples

```
dat_list = hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute")
```

## Evaluation signals

- The rawImpute assay has reduced metabolite count compared to logRaw (e.g., 61 metabolites retained from larger initial set), reflecting successful threshold and intersect filtering.
- Zero missing values are present in the rawImpute assay across all samples and batches.
- Metabolites retained are exactly those quantified in all five batches (intersection rule respected).
- Imputed values are numeric and within the realistic range of log2-transformed metabolite abundance (no extreme outliers or NaN/Inf).
- Assay dimensions match: metabolites × samples are consistent between logRaw (pre-filtered) and rawImpute (post-filtered and imputed).

## Limitations

- k-nearest neighbour imputation relies on local similarity structure; sparse or highly imbalanced feature spaces may yield unreliable imputations.
- The intersect method removes all metabolites not quantified in every batch, which can be overly stringent for studies with batch-specific biological signals.
- Missing-not-at-random (MNAR) mechanisms — e.g., values below instrument detection limits — may violate the missing-completely-at-random (MCAR) assumption implicit in k-nearest neighbour imputation.
- No guidance provided in the article on choosing k or on validation of imputation quality; practitioners should cross-validate against held-out complete cases if possible.

## Evidence

- [intro] The `clean` function filters metabolites with >50% missing values per batch using the intersect method, then performs k-nearest neighbour imputation to produce a rawImpute assay containing 61 metabolites quantified across all five batches.: "The `clean` function filters metabolites with >50% missing values per batch using the intersect method, then performs k-nearest neighbour imputation to produce a rawImpute assay containing 61"
- [intro] Apply hRUV::clean() with threshold=0.5, method='intersect', assay='logRaw', and newAssay='rawImpute' parameters on a list of SummarizedExperiment objects.: "dat_list = hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute")"
- [intro] We have filtered metabolites with more than 50% of missing values per batch and selected metabolites that are quantified across all batches (intersect): "We have filtered metabolites with more than 50% of missing values per batch and selected metabolites that are quantified across all batches (intersect)"
