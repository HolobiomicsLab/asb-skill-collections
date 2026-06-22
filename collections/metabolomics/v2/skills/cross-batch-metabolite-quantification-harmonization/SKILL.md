---
name: cross-batch-metabolite-quantification-harmonization
description: Use when you have multiple SummarizedExperiment objects representing separate metabolomics assay batches with different metabolite coverage and missing-value patterns, and you need to identify a common metabolite set quantified across all batches before applying hierarchical batch normalization or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - hRUV
  - R
  - dplyr
  - SummarizedExperiment
  - DMwR2
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy'
- Install the R package from GitHub using the `devtools` package
- we will load the hRUV package and other packages required for the demonstration... library(dplyr)
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
---

# cross-batch-metabolite-quantification-harmonization

## Summary

Filter and impute metabolites across multiple metabolomics batches to produce a unified feature set with complete quantification. This skill ensures only metabolites present across all batches are retained and missing values are resolved, enabling downstream batch-effect correction.

## When to use

You have multiple SummarizedExperiment objects representing separate metabolomics assay batches with different metabolite coverage and missing-value patterns, and you need to identify a common metabolite set quantified across all batches before applying hierarchical batch normalization or comparative analysis.

## When NOT to use

- Input is already a single unified feature table (not batch-separated SummarizedExperiment objects)
- You intend to retain batch-specific metabolites rather than enforce cross-batch consistency
- Missing-value mechanisms are informative and should not be imputed (e.g., absent metabolites indicate true biological absence rather than measurement failure)

## Inputs

- List of SummarizedExperiment objects, each with log2-transformed metabolite abundance assay (logRaw or equivalent)
- Multiple batches of metabolomics data with metabolite × sample matrix structure

## Outputs

- List of SummarizedExperiment objects with new assay (rawImpute) containing harmonized metabolites with imputed values
- Reduced metabolite set (e.g., 61 metabolites across 5 batches) quantified in all samples across all batches
- Assay matrix with no missing values

## How to apply

Load metabolomics data as a list of SummarizedExperiment objects with log2-transformed assay (e.g., logRaw). Apply hRUV::clean() with threshold=0.5 to filter metabolites with >50% missing values per batch, method='intersect' to retain only metabolites quantified in all batches, and k-nearest neighbour imputation to fill remaining missing values. Extract and verify the output assay (e.g., rawImpute) for metabolite count and absence of missing data. The intersect method ensures strict cross-batch comparability by excluding any metabolite absent from even one batch.

## Related tools

- **hRUV** (Primary tool: implements clean() function with threshold filtering, intersect method, and k-nearest neighbour imputation for cross-batch metabolite harmonization) — https://github.com/SydneyBioX/hRUV
- **SummarizedExperiment** (Data container: stores metabolite abundance matrices (assays) and metadata for batch-organized metabolomics data) — https://bioconductor.org/packages/SummarizedExperiment
- **dplyr** (Data manipulation and wrangling during workflow setup and verification)
- **DMwR2** (Supports k-nearest neighbour imputation used by hRUV::clean())
- **R** (Execution environment)

## Examples

```
dat_list = hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute")
```

## Evaluation signals

- Output assay contains no missing values (NA count = 0) after imputation
- Metabolite count is reduced and consistent across all batches (e.g., 61 metabolites × n_samples for each batch)
- All retained metabolites are present in every batch (intersect condition verified)
- Metadata and sample names are preserved; only metabolite dimension is filtered
- rawImpute assay is correctly nested in each SummarizedExperiment object with proper assay naming and dimnames

## Limitations

- Intersect method is stringent and may discard many batch-specific metabolites; not suitable when rare or batch-enriched metabolites carry biological significance
- k-nearest neighbour imputation assumes missing-at-random (MAR) mechanism; if missingness is informative (e.g., detection limits), imputation may bias downstream inference
- Threshold=0.5 (50% missing-value cutoff) is fixed in the demonstrated workflow; users must justify appropriateness for their data distribution
- Requires explicit batch structure in the SummarizedExperiment list; does not automatically detect or infer batch membership

## Evidence

- [intro] threshold and intersect method ensure cross-batch metabolite retention: "filters metabolites with >50% missing values per batch using the intersect method, then performs k-nearest neighbour imputation"
- [intro] intersect method definition and strict cross-batch requirement: "selected metabolites that are quantified across all batches (intersect) with `clean` function"
- [intro] concrete hRUV::clean() function call with parameters: "dat_list = hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute")"
- [intro] input data structure requirement: "The data is already formatted in to a `SummarizedExperiment` object"
- [intro] expected output: metabolite reduction and missing-value elimination: "produce a rawImpute assay containing 61 metabolites quantified across all five batches"
- [readme] installation and dependency context: "Install the R package from GitHub using the `devtools` package"
