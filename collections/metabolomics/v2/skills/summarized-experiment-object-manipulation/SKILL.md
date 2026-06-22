---
name: summarized-experiment-object-manipulation
description: Use when when working with metabolomics, proteomics, or other high-throughput replicate experiments stored in Bioconductor SummarizedExperiment format (rows = features/metabolites, columns = samples/replicates), and you need to inspect raw feature dimensions, assess data completeness, or apply.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - R
  - MSPrep
  - Bioconductor
  - marr
derived_from:
- doi: 10.1186/s12859-021-04336-9
  title: marr
- doi: 10.1080/01621459.2017.1397521
  title: ''
evidence_spans:
- 'marr: An R/Bioconductor package for Maximum Rank Reproducibility'
- The R-package **marr** can be installed from GitHub using the R package [devtools]
- The **msprepCOPD** data in the **marr** package was pre-processed using the MSPrep software
- '`marr`: An R/Bioconductor package for Maximum Rank Reproducibility'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_marr_cq
    doi: 10.1186/s12859-021-04336-9
    title: marr
  dedup_kept_from: coll_marr_cq
schema_version: 0.2.0
---

# SummarizedExperiment object manipulation

## Summary

Load, inspect, and manipulate Bioconductor SummarizedExperiment objects containing high-dimensional assay data (e.g., metabolite abundance matrices) with associated sample and feature metadata. This skill enables extraction of raw feature counts, calculation of missingness statistics per feature, and preservation of annotations during filtering workflows.

## When to use

When working with metabolomics, proteomics, or other high-throughput replicate experiments stored in Bioconductor SummarizedExperiment format (rows = features/metabolites, columns = samples/replicates), and you need to inspect raw feature dimensions, assess data completeness, or apply row-wise filtering while retaining sample and feature annotations.

## When NOT to use

- Input is already a pre-filtered feature table with unknown provenance or missingness criteria.
- Analysis requires retention of all raw features regardless of data completeness (e.g., for benchmarking purposes).
- Metadata structure is non-standard or does not conform to SummarizedExperiment slot conventions.

## Inputs

- SummarizedExperiment object with assay slot containing feature abundance matrix (features × samples)
- Feature metadata (rowData) with metabolite identifiers
- Sample metadata (colData) with sample/replicate annotations

## Outputs

- Filtered SummarizedExperiment or abundance matrix with reduced feature count
- Summary statistics (original vs. filtered feature counts, missingness proportions per feature)
- Feature-level metadata preserved (row names, identifiers)

## How to apply

Load the SummarizedExperiment object from a Bioconductor package (e.g., marr::msprepCOPD). Extract the assay matrix and inspect its dimensions (e.g., 662 features × 20 replicates). For each row (metabolite), calculate the proportion of missing values (NA or structural zeros per the preprocessing convention used by MSPrep). Identify rows meeting a retention criterion (e.g., ≤80% missingness, equivalent to ≥20% sample coverage or ≥4 of 20 samples present). Subset the assay matrix to retain only qualifying rows, preserving row names (metabolite identifiers) and column names (sample identifiers) along with any associated metadata stored in rowData() and colData() slots. Output the filtered SummarizedExperiment or derived abundance matrix with consistent dimensions and annotations for downstream analysis.

## Related tools

- **marr** (R/Bioconductor package providing SummarizedExperiment assay objects (msprepCOPD) and reproducibility assessment for high-dimensional replicate experiments) — https://github.com/Ghoshlab/marr
- **Bioconductor** (Infrastructure providing SummarizedExperiment class and assay/metadata slot manipulation methods) — https://www.bioconductor.org
- **R** (Statistical language for loading, subsetting, and manipulating SummarizedExperiment objects)

## Examples

```
library(marr); data(msprepCOPD); se <- msprepCOPD; dim(assay(se)); missing_prop <- rowMeans(is.na(assay(se))); se_filtered <- se[missing_prop <= 0.8, ]; dim(assay(se_filtered))
```

## Evaluation signals

- Output feature count is correctly reduced (e.g., 662 → 645 metabolites = 2.6% loss) and matches the stated threshold (80% missingness).
- All retained metabolites meet the retention criterion: ≤80% missing values across the sample dimension.
- Feature identifiers and sample identifiers are preserved in output; no identifiers are duplicated or corrupted.
- Output assay matrix dimensions are consistent with filtered feature count and original sample count (e.g., 645 × 20).
- Missing value counts per feature can be recalculated from the output to verify the filtering boundary.

## Limitations

- Missingness detection depends on preprocessing convention (NA vs. structural zero); MSPrep may use zero-based convention requiring clarification before filtering.
- Threshold choice (80% in the article) is context-dependent; different studies or omics platforms may require different cutoffs.
- SummarizedExperiment assumes standard slot structure (assay, rowData, colData); non-standard objects may require adaptation.
- Filtering is deterministic but statistically uninformed; no uncertainty quantification or multiple testing correction is applied within this step alone.

## Evidence

- [other] Load the raw msprepCOPD metabolite abundance matrix (662 features × 20 replicates) from the marr package SummarizedExperiment object.: "Load the raw msprepCOPD metabolite abundance matrix (662 features × 20 replicates) from the marr package SummarizedExperiment object."
- [other] The marr package contains a pre-processed data SummarizedExperiment assay object of 645 metabolites (features) measured in plasma and 20 biological replicates: "The **marr** package contains a pre-processed data `SummarizedExperiment` assay object of 645 metabolites (features) measured in plasma and 20 biological replicates"
- [intro] Metabolites are removed if they are missing more than 80% of the samples: "Filtering: Metabolites are removed if they are missing more than 80% of the samples"
- [other] Identify and retain only metabolites with ≤80% missingness (i.e., present in ≥20% of samples, or equivalently ≥4 of 20 samples).: "Identify and retain only metabolites with ≤80% missingness (i.e., present in ≥20% of samples, or equivalently ≥4 of 20 samples)."
- [other] The MSPrep filtering step removes metabolites exceeding 80% missingness, reducing the raw metabolite count from 662 to 645 (a loss of 17 metabolites or 2.6% of features).: "The MSPrep filtering step removes metabolites exceeding 80% missingness, reducing the raw metabolite count from 662 to 645 (a loss of 17 metabolites or 2.6% of features)."
