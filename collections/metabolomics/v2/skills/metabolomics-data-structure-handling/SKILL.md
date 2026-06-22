---
name: metabolomics-data-structure-handling
description: Use when you have metabolomics data already formatted as a SummarizedExperiment object containing multiple assays (raw counts, log-transformed, imputed, or normalized versions) and need to access specific assay layers alongside batch annotation metadata to perform comparisons (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - hRUV
  - R
  - dplyr
  - SummarizedExperiment
  - MsFeatures
  - xcms
  - MsExperiment
  - Spectra
  - MSnbase
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
- doi: 10.1021/ac051437y
  title: ''
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy'
- Install the R package from GitHub using the `devtools` package
- we will load the hRUV package and other packages required for the demonstration... library(dplyr)
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hruv_cq
    doi: 10.1101/2020.12.21.423723
    title: hRUV
  - build: coll_xcms
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_hruv_cq
schema_version: 0.2.0
---

# metabolomics-data-structure-handling

## Summary

Load, organize, and access metabolomics assays within a SummarizedExperiment object to enable coordinated analysis across raw, imputed, and normalized data matrices. This skill ensures correct indexing of multiple assay layers (e.g., rawImpute, loessShort_concatenate) and their associated batch metadata for downstream visualization and batch-effect assessment.

## When to use

You have metabolomics data already formatted as a SummarizedExperiment object containing multiple assays (raw counts, log-transformed, imputed, or normalized versions) and need to access specific assay layers alongside batch annotation metadata to perform comparisons (e.g., before/after normalization PCA plots, batch-effect diagnostics). Use this skill when transitioning between preprocessing stages that produce new assays stored in the same object.

## When NOT to use

- Data is stored as separate CSV/TSV files or feature tables without integrated sample metadata—use file I/O and data frame merging instead.
- You only need a single assay snapshot and do not need to compare multiple normalization or processing states.
- The SummarizedExperiment object has not been formally constructed (e.g., rows and columns are not properly labeled, or colData lacks batch identifiers).

## Inputs

- SummarizedExperiment object containing multiple metabolomics assays
- assay names as strings (e.g., 'rawImpute', 'loessShort_concatenate')
- batch metadata column name (e.g., 'batch_info')

## Outputs

- Extracted assay matrix (rows = metabolites, columns = samples)
- Associated batch_info vector or colData subset
- Verified SummarizedExperiment object ready for downstream analysis

## How to apply

Load the SummarizedExperiment object into R using the SummarizedExperiment library. Access individual assays by name using assay(object, 'assayName') or assays(object) to inspect all available layers. Verify the structure: rows = metabolites, columns = samples, with consistent metadata columns (e.g., batch_info) in colData(). Extract the appropriate assay (e.g., rawImpute for pre-normalization, loessShort_concatenate for post-normalization) along with its corresponding batch_info column from colData(). Use these paired objects as inputs to downstream functions like hRUV::plotPCA, ensuring the assay matrix dimensions and sample order align with metadata annotations.

## Related tools

- **SummarizedExperiment** (Container class for organizing metabolomics assays (raw, imputed, normalized) alongside sample metadata and batch annotations; enables coordinated subsetting and cross-assay comparisons) — https://bioconductor.org/packages/SummarizedExperiment
- **hRUV** (Consumes SummarizedExperiment objects and accesses specific named assays (e.g., rawImpute, loessShort_concatenate) for normalization workflows and batch-effect visualization via plotPCA) — https://github.com/SydneyBioX/hRUV
- **dplyr** (Data manipulation utility for filtering, selecting, and reshaping assay matrices and metadata after extraction from SummarizedExperiment) — https://dplyr.tidyverse.org

## Examples

```
library(SummarizedExperiment); dat <- readRDS('hruv_summarized_experiment.rds'); raw_assay <- assay(dat, 'rawImpute'); batch_info <- colData(dat)$batch_info; normalized_assay <- assay(dat, 'loessShort_concatenate')
```

## Evaluation signals

- assay(object, 'assayName') returns a numeric matrix with metabolite rows and sample columns (no NA row/column names).
- colData(object) contains batch_info column with correct batch labels matching the number of samples in all assays.
- Assay dimensions are consistent across all named assays (same number of columns; row counts may differ if metabolites were filtered).
- Subsetting by batch_info (e.g., colData(object)$batch_info == 'batch_1') correctly indexes corresponding columns in the assay matrix.
- Downstream functions (e.g., hRUV::plotPCA) execute without dimension-mismatch errors and produce outputs colored/faceted by batch metadata as intended.

## Limitations

- SummarizedExperiment assumes rectangular structure; metabolites missing in specific batches must be handled via imputation or explicit filtering before object construction.
- Assay names and metadata column names are case-sensitive; typos in assay('object', 'wrongName') will return NULL without warning.
- The object does not enforce data type consistency across assays (e.g., log-transformed vs. raw counts); users must track transformations manually or document them in metadata.
- Large metabolomics datasets (10,000+ metabolites, 1,000+ samples) may cause memory overhead if all assays are loaded simultaneously; consider subsetting by metabolite or batch before analysis.

## Evidence

- [readme] The data is already formatted in to a `SummarizedExperiment` object: "The data is already formatted in to a `SummarizedExperiment` object"
- [full_text] Load the cleaned and imputed metabolomics data (rawImpute assay) from the SummarizedExperiment object: "Load the cleaned and imputed metabolomics data (rawImpute assay) from the SummarizedExperiment object"
- [full_text] Load the normalized metabolomics data (loessShort_concatenate assay) from the same SummarizedExperiment object: "Load the normalized metabolomics data (loessShort_concatenate assay) from the same SummarizedExperiment object"
- [full_text] Generate a PCA plot using hRUV::plotPCA with rawImpute assay colored by batch_info to visualize the pre-normalization batch effect: "Generate a PCA plot using hRUV::plotPCA with rawImpute assay colored by batch_info to visualize the pre-normalization batch effect"
- [readme] library(SummarizedExperiment)... The data is deposited at https://github.com/SydneyBioX/BioHEART_metabolomics: "library(SummarizedExperiment); The data is deposited at https://github.com/SydneyBioX/BioHEART_metabolomics"
