---
name: summarizedexperiment-assay-manipulation
description: Use when when working with multi-batch metabolomics studies where you
  need to create intermediate normalized assays (e.
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
  - SummarizedExperiment
  - dplyr
  license_tier: open
  provenance_tier: literature
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
- library(SummarizedExperiment)... The data is already formatted in to a `SummarizedExperiment`
  object
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

# SummarizedExperiment Assay Manipulation

## Summary

Create, transform, and extract assays within SummarizedExperiment objects to support multi-stage metabolomics data processing pipelines. This skill enables chaining of normalization, imputation, and batch-correction workflows while preserving sample and feature metadata.

## When to use

When working with multi-batch metabolomics studies where you need to create intermediate normalized assays (e.g., logRaw, rawImpute, loessShort_concatenate) at each processing stage, and downstream analysis tools expect data in SummarizedExperiment format with assay names tracked as formal object attributes rather than loose matrices.

## When NOT to use

- Input is a simple matrix or data.frame without sample/feature metadata—use SummarizedExperiment construction first.
- Assay dimensions are inconsistent (metabolite or sample count differs across assays)—fix dimension mismatches before assignment.
- You need to store non-numeric metadata or per-assay parameters—use metadata() or altExp() slots instead of assay slots for those.

## Inputs

- SummarizedExperiment object with one or more named assays (e.g., 'raw', 'logRaw')
- Numeric matrix of metabolite abundances (metabolites × samples)
- colData with batch and replicate metadata
- rowData with metabolite identifiers

## Outputs

- SummarizedExperiment object with new named assay(s) appended (e.g., 'rawImpute', 'loessShort_concatenate')
- Extracted assay matrix for external tool input
- Updated colData and rowData preserved alongside new assays

## How to apply

Load or construct a SummarizedExperiment object containing raw metabolite abundance data in a named assay (e.g., 'raw'). Apply transformations by computing new assay matrices—such as log2(raw + 1) for loess-compatible scaling, k-nearest neighbor imputation for missing values, or RUV-III batch correction—and attach each result to the same SummarizedExperiment using assay(object, 'newAssayName') <- result_matrix. Verify that row and column dimensions match the original object (metabolites × samples) and that metadata in colData (batch, replicate flags) and rowData remain aligned. Extract final assays using assay(object, 'assayName') for downstream tools.

## Related tools

- **SummarizedExperiment** (Container class for storing metabolite abundance matrices with aligned sample and feature metadata across multiple normalization stages) — https://bioconductor.org/packages/SummarizedExperiment
- **hRUV** (Batch normalization pipeline that accepts SummarizedExperiment inputs and returns updated objects with new assays (rawImpute, loessShort_concatenate, etc.)) — https://github.com/SydneyBioX/hRUV
- **dplyr** (Data transformation and metadata manipulation for colData and rowData annotations)

## Examples

```
assay(dat, "logRaw", withDimnames = FALSE) <- log2(assay(dat, "raw") + 1); dat_list <- hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute")
```

## Evaluation signals

- Verify assay name is registered: names(assays(object)) includes the new assay string.
- Check matrix dimensions are consistent: nrow(assay(object, 'newAssay')) == nrow(object) and ncol(...) == ncol(object).
- Confirm colData and rowData match object dimensions: nrow(colData(object)) == ncol(object), nrow(rowData(object)) == nrow(object).
- Validate no NA introduction: sum(is.na(assay(object, 'newAssay'))) is acceptable given imputation method (e.g., 0 if kNN imputed).
- Trace metadata preservation: batch and replicate annotations in colData should be unchanged across assay operations.

## Limitations

- SummarizedExperiment does not enforce assay name uniqueness; overwriting an existing assay name silently replaces prior data.
- Memory usage scales with matrix size and number of assays stored; large metabolomics studies (>10k metabolites × >1k samples) may require memory-aware assay subsetting.
- Row and column dimension mismatches will cause runtime errors during assay assignment; no automatic reconciliation is performed.
- Cross-assay operations (e.g., comparing values across 'raw' and 'logRaw') require manual extraction and alignment; the object itself provides no join semantics.

## Evidence

- [intro] Log transformation via assay assignment: "assay(dat, "logRaw", withDimnames = FALSE) = log2(assay(dat, "raw") + 1)"
- [intro] Multi-assay workflow in hRUV pipeline: "dat_list = hRUV::clean(dat_list, threshold = 0.5, method = "intersect", assay = "logRaw", newAssay = "rawImpute")"
- [intro] SummarizedExperiment as standard container: "The data is already formatted in to a `SummarizedExperiment` object"
- [methods] Assay extraction from normalized output: "Extract the resulting normalised loessShort_concatenate assay from the returned SummarizedExperiment object"
- [other] Multiple assay names in single object: "Extract and verify the rawImpute assay from the cleaned output, confirming metabolite count reduction and absence of missing values"
