---
name: feature-table-subsetting-and-export
description: Use when you have a raw metabolite abundance matrix with substantial
  missing data (NAs or zero-valued entries) and need to remove poorly-measured features
  before downstream analysis. Apply this skill when the proportion of missing values
  per metabolite exceeds a predefined threshold (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - MSPrep
  - Bioconductor
  - marr (R/Bioconductor package)
  - R (base and SummarizedExperiment)
  license_tier: restricted
derived_from:
- doi: 10.1186/s12859-021-04336-9
  title: marr
- doi: 10.1080/01621459.2017.1397521
  title: ''
evidence_spans:
- 'marr: An R/Bioconductor package for Maximum Rank Reproducibility'
- The R-package **marr** can be installed from GitHub using the R package [devtools]
- The **msprepCOPD** data in the **marr** package was pre-processed using the MSPrep
  software
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-021-04336-9
  all_source_dois:
  - 10.1186/s12859-021-04336-9
  - 10.1080/01621459.2017.1397521
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-table-subsetting-and-export

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Remove metabolites exceeding a missingness threshold (e.g., >80% missing values) from a raw abundance matrix, then export the filtered feature table with sample annotations and metabolite identifiers preserved. This reduces noise and improves downstream reproducibility assessment by focusing on well-measured analytes.

## When to use

You have a raw metabolite abundance matrix with substantial missing data (NAs or zero-valued entries) and need to remove poorly-measured features before downstream analysis. Apply this skill when the proportion of missing values per metabolite exceeds a predefined threshold (e.g., 80% missingness = present in <20% of samples), indicating that feature is unreliable across replicates.

## When NOT to use

- Input is already a curated, pre-filtered feature table with known low missingness — subsetting again may over-filter.
- Missingness is not random but structured by sample group or batch — consider stratified filtering or imputation instead.
- The analysis goal requires all measured metabolites regardless of data quality (e.g., exploratory metabolite discovery) — apply this skill only if reproducibility or signal strength is the priority.

## Inputs

- Raw metabolite abundance matrix (SummarizedExperiment assay object or data frame: rows = metabolites, columns = samples)
- Missing value indicator convention (NA vs. zero)
- Missingness threshold parameter (e.g., 0.80 for 80% maximum allowed missing)

## Outputs

- Filtered metabolite abundance matrix (subset of input rows, all columns preserved)
- Filtered feature metadata (metabolite identifiers, annotation columns)
- Summary statistics: count of removed metabolites, percent feature loss

## How to apply

Load the raw abundance matrix (rows = metabolites/features, columns = samples) from a SummarizedExperiment object or data frame. Calculate the proportion of missing values (NA or zero, depending on data convention) for each metabolite across all samples. Identify metabolites where missingness ≤ threshold (e.g., ≤80%, equivalent to ≥20% of samples or ≥4 of 20 replicates in the marr/msprepCOPD case). Subset the abundance matrix to retain only those passing metabolites. Export the filtered matrix while preserving metabolite identifiers (rownames) and sample annotations (colnames and metadata). The rationale is that features present in very few samples contribute noise and unreliable signal for reproducibility and downstream statistical inference.

## Related tools

- **MSPrep** (Pre-processing and filtering software that removes metabolites exceeding 80% missingness threshold on raw abundance data)
- **marr (R/Bioconductor package)** (Provides msprepCOPD SummarizedExperiment object containing pre-filtered 645-metabolite matrix and reproducibility assessment on filtered features) — https://github.com/Ghoshlab/marr
- **R (base and SummarizedExperiment)** (Implements subsetting, row filtering, and export of abundance matrices with preserved annotations)

## Examples

```
# Load data and filter metabolites with >80% missingness
library(marr)
data(msprepCOPD)
filtered_data <- msprepCOPD[rowSums(is.na(assay(msprepCOPD))) <= 0.8 * ncol(assay(msprepCOPD)), ]
# Result: 645 metabolites retained from 662
```

## Evaluation signals

- Feature count reduced from raw to filtered set matches expected loss (e.g., 662 → 645 metabolites, ~2.6% loss for 80% threshold)
- All retained metabolites have ≤80% missingness (equivalently ≥20% sample presence or ≥4 samples in 20-replicate design)
- Metabolite identifiers and sample annotations preserved in output matrix (rownames and colnames intact)
- No missing value in retained features exceeds the threshold; spot-check several retained metabolites for compliance
- Output matrix dimensions and class match input (e.g., data.frame or SummarizedExperiment with same sample count but fewer rows)

## Limitations

- Threshold choice (e.g., 80%) is arbitrary; no guidance provided for threshold selection based on experiment design or biology.
- Zero-filling convention must match the data source; treating zeros as missing may be incorrect if zeros represent true biological absence.
- Filtering is applied uniformly across all samples; stratified filtering by sample type or batch may be needed if missingness is not random.
- Removed metabolites are discarded; if later analysis requires those features, re-processing from raw data is necessary.

## Evidence

- [results] The MSPrep filtering step removes metabolites exceeding 80% missingness, reducing the raw metabolite count from 662 to 645 (a loss of 17 metabolites or 2.6% of features).: "removing metabolites exceeding 80% missingness, reducing the raw metabolite count from 662 to 645 (a loss of 17 metabolites or 2.6% of features)"
- [methods] Identify and retain only metabolites with ≤80% missingness (i.e., present in ≥20% of samples, or equivalently ≥4 of 20 samples).: "retain only metabolites with ≤80% missingness (i.e., present in ≥20% of samples, or equivalently ≥4 of 20 samples)"
- [intro] Filtering: Metabolites are removed if they are missing more than 80% of the samples: "Filtering: Metabolites are removed if they are missing more than 80% of the samples"
- [methods] Load the raw msprepCOPD metabolite abundance matrix (662 features × 20 replicates) from the marr package SummarizedExperiment object.: "Load the raw msprepCOPD metabolite abundance matrix (662 features × 20 replicates) from the marr package SummarizedExperiment object"
- [methods] Output the filtered abundance matrix with metabolite identifiers and sample annotations preserved.: "Output the filtered abundance matrix with metabolite identifiers and sample annotations preserved"
