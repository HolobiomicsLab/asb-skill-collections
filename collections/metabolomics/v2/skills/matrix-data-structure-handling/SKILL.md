---
name: matrix-data-structure-handling
description: Use when after feature filtering has removed low-abundance or highly sparse metabolites (e.g., >80% missingness), and before applying missing value imputation or normalization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - R
  - Bioconductor
  - SummarizedExperiment
  - marr
derived_from:
- doi: 10.1186/s12859-021-04336-9
  title: marr
- doi: 10.1080/01621459.2017.1397521
  title: ''
evidence_spans:
- 'marr: An R/Bioconductor package for Maximum Rank Reproducibility'
- The R-package **marr** can be installed from GitHub using the R package [devtools]
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

# matrix-data-structure-handling

## Summary

Converting filtered metabolite abundance data into structured matrix or SummarizedExperiment formats suitable for downstream imputation, normalization, and reproducibility analysis. This skill ensures data integrity and compatibility with statistical packages like marr and Bioconductor.

## When to use

After feature filtering has removed low-abundance or highly sparse metabolites (e.g., >80% missingness), and before applying missing value imputation or normalization. Triggered when raw metabolite quantification data needs to be reorganized from tabular form into a matrix with explicit row (metabolite/feature) and column (sample) structure for vectorized operations.

## When NOT to use

- Data is already in a validated SummarizedExperiment or matrix format — skip restructuring.
- Filtering step has not yet been completed — defer matrix construction until after feature selection.
- Input contains non-numeric or mixed data types that cannot be coerced to a single numeric matrix.

## Inputs

- Filtered metabolite abundance table (CSV or data frame with >80% missingness already removed)
- Sample metadata or colData (optional, for SummarizedExperiment construction)

## Outputs

- Numeric matrix: metabolites (rows) × samples (columns)
- SummarizedExperiment object with metabolite matrix in assay slot and sample metadata in colData (optional)

## How to apply

Load the filtered metabolite abundance table into R and restructure it as a numeric matrix with metabolites as rows and samples as columns, or encapsulate it within a SummarizedExperiment object with one assay slot. Verify matrix dimensions match the expected feature count (post-filtering) and sample count. This structured format enables row-wise operations (Bayesian PCA imputation across samples per metabolite) and column-wise operations (median normalization across metabolites per sample). The marr package and Bioconductor workflows expect this SummarizedExperiment or matrix input format to ensure correct application of reproducibility metrics and preprocessing steps.

## Related tools

- **R** (Language for loading, restructuring, and validating metabolite matrices; base functions (as.matrix, data.frame) and S4 class construction.) — https://www.r-project.org/
- **SummarizedExperiment** (Bioconductor class for encapsulating metabolite abundance matrix with assay slot and associated sample metadata (colData).) — https://bioconductor.org/packages/SummarizedExperiment
- **marr** (R/Bioconductor package that accepts SummarizedExperiment or matrix input for reproducibility and imputation workflows.) — https://github.com/Ghoshlab/marr

## Examples

```
# Load filtered metabolite data and restructure as SummarizedExperiment
library(SummarizedExperiment)
metab_data <- read.csv('filtered_metabolites.csv', row.names=1)
se <- SummarizedExperiment(assays=list(abundance=as.matrix(metab_data)))
MarrOutput <- marr::Marr(object=se, pSamplepairs=0.75, pFeatures=0.75, alpha=0.05)
```

## Evaluation signals

- Matrix dimensions are correct: rows = filtered metabolite count, columns = sample count.
- All matrix entries are numeric (no NA, NaN, or character values outside of row/column names).
- Row names correspond to metabolite identifiers; column names correspond to sample identifiers.
- For SummarizedExperiment: assay slot contains the numeric matrix, colData contains sample metadata with row count matching matrix column count.
- Matrix can be successfully passed to Bayesian PCA imputation (marr or marr-compatible function) without dimension or type errors.

## Limitations

- Matrix restructuring does not impute missing values; BPCA or other imputation must follow.
- SummarizedExperiment construction requires consistent metadata — missing or mismatched colData will cause indexing failures.
- Row and column names must be unique and non-empty; duplicates or NAs in names will cause ambiguity in downstream operations.
- Large metabolite matrices (>10,000 features × >1,000 samples) may require memory optimization or chunked processing in R.

## Evidence

- [other] Load the filtered metabolite matrix (metabolites with >80% missingness already removed) into R.: "Load the filtered metabolite matrix (metabolites with >80% missingness already removed) into R."
- [readme] SummarizedExperiment with one assay object with observations (e.g., metabolites or genes) on the rows and samples as the columns: "a data frame or a matrix or a Summarized Experiment with one assay object with observations (e.g., metabolites or genes) on the rows and samples as the columns"
- [other] The marr package contains a pre-processed data SummarizedExperiment assay object of 645 metabolites (features) measured in plasma and 20 biological replicates: "The **marr** package contains a pre-processed data `SummarizedExperiment` assay object of 645 metabolites (features) measured in plasma and 20 biological replicates"
- [other] Export the complete imputed metabolite abundance matrix as a numeric table (CSV or RDS format) ready for downstream median normalization.: "Export the complete imputed metabolite abundance matrix as a numeric table (CSV or RDS format) ready for downstream median normalization."
