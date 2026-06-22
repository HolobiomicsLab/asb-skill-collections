---
name: bayesian-dimensionality-reduction-application
description: Use when your input is a filtered metabolite abundance matrix with remaining sporadic missingness (after removing features with >80% missingness) and you need to produce a complete feature table for subsequent normalization and statistical analysis without data loss or listwise deletion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3365
  - http://edamontology.org/topic_3172
  tools:
  - R
  - Bioconductor
  - marr
  - devtools
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-021-04336-9
  all_source_dois:
  - 10.1186/s12859-021-04336-9
  - 10.1080/01621459.2017.1397521
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bayesian-dimensionality-reduction-application

## Summary

Apply Bayesian Principal Component Analysis (BPCA) to impute missing values in high-dimensional metabolomic feature matrices after initial feature filtering and before downstream normalization. BPCA estimates and fills missing metabolite abundances using probabilistic dimensionality reduction, preserving the covariance structure of the data.

## When to use

Your input is a filtered metabolite abundance matrix with remaining sporadic missingness (after removing features with >80% missingness) and you need to produce a complete feature table for subsequent normalization and statistical analysis without data loss or listwise deletion.

## When NOT to use

- Input matrix is already complete (no missing values); imputation is unnecessary and adds computational overhead.
- More than 80% of values per feature are missing; BPCA cannot reliably estimate from extremely sparse data.
- The goal is feature selection or filtering rather than missing value recovery; consider alternative filtering strategies instead.

## Inputs

- Filtered metabolite abundance matrix (numeric data frame or matrix, rows = metabolites, columns = samples)
- Matrix with ≤80% missingness per feature after initial filtering

## Outputs

- Complete imputed metabolite abundance matrix (no missing values)
- Numeric table (CSV, RDS, or SummarizedExperiment format) ready for normalization

## How to apply

Load the filtered metabolite matrix (rows = metabolites, columns = samples) into R as a numeric data frame or matrix. Apply BPCA via the marr package (or compatible Bioconductor imputation function) to estimate missing values by iteratively computing the Bayesian posterior distribution of principal components conditioned on observed values. BPCA leverages the correlation structure across metabolites to infer plausible values for missing entries. Verify completion by checking that the output matrix contains no remaining NA or NaN values. Export the imputed matrix in a portable format (CSV, RDS, or SummarizedExperiment object) for input to median normalization or other downstream steps.

## Related tools

- **marr** (R/Bioconductor package providing BPCA imputation via compatible functions for high-dimensional metabolomic data) — https://github.com/Ghoshlab/marr
- **R** (Programming environment for loading, processing, and exporting the metabolite matrix)
- **Bioconductor** (Repository and ecosystem providing SummarizedExperiment class and compatible imputation packages)
- **devtools** (R package for installing marr from GitHub) — https://github.com/r-lib/devtools

## Examples

```
library(marr); filtered_metabolites <- read.csv('filtered_metabolites.csv', row.names=1); imputed_metabolites <- apply(filtered_metabolites, 2, function(x) bpca_impute(x)); write.csv(imputed_metabolites, 'imputed_metabolites.csv')
```

## Evaluation signals

- Output matrix has identical dimensions to input (same rows and columns) and contains only numeric values with no NA, NaN, or NULL entries.
- Mean and standard deviation of imputed values are reasonable relative to observed metabolite abundances (no extreme outliers introduced).
- Covariance structure among metabolites is preserved; imputed values respect observed correlations across the feature matrix.
- Downstream median normalization step completes without error and produces expected quantitative distributions.
- Reproducibility assessment (marr procedure) on imputed data yields consistent rank-order reproducibility metrics across replicate sample pairs.

## Limitations

- BPCA assumes multivariate normality; severe departure from normality in metabolite distributions may reduce accuracy.
- Performance degrades with very high dimensionality and extreme sparsity (>80% missing per feature); pre-filtering is critical.
- Imputation introduces artificial correlations if missingness is not random (MCAR); non-random missingness patterns may bias downstream inference.
- Computational cost increases with matrix size; very large datasets (>10,000 features × >1000 samples) may require memory-efficient implementations.
- Method assumes missing values are missing completely at random (MCAR); if missingness is related to unobserved metabolite abundance (MNAR), imputation may not be valid.

## Evidence

- [intro] BPCA imputation application: "Missing value imputation technique: We apply Bayesian Principal Component Analysis (BPCA) to impute missing values"
- [intro] Filtering step preceding imputation: "Filtering: Metabolites are removed if they are missing more than 80% of the samples"
- [intro] Sequential preprocessing pipeline: "Missing value imputation technique: Bayesian Principal Component Analysis (BPCA) is applied to impute missing values in the filtered metabolite matrix prior to normalization"
- [intro] marr package BPCA implementation: "marr: An R/Bioconductor package for Maximum Rank Reproducibility"
- [readme] Installation from GitHub: "Use to install the latest version of **marr** from GitHub: devtools::install_github("Ghoshlab/marr")"
- [intro] msprepCOPD dataset preprocessing: "The **msprepCOPD** data in the **marr** package was pre-processed using the MSPrep software"
