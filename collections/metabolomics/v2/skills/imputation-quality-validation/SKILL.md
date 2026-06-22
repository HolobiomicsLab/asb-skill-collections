---
name: imputation-quality-validation
description: Use when after applying BPCA imputation to a filtered metabolite matrix (with metabolites having >80% missingness already removed) and before proceeding to median normalization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
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

# imputation-quality-validation

## Summary

Verification that Bayesian Principal Component Analysis (BPCA) missing-value imputation has successfully eliminated all missing values from a filtered metabolite abundance matrix prior to downstream normalization. This quality-control step ensures the imputed matrix is complete and ready for median normalization in the MSPrep preprocessing pipeline.

## When to use

After applying BPCA imputation to a filtered metabolite matrix (with metabolites having >80% missingness already removed) and before proceeding to median normalization. Use this skill when you need to confirm that the imputation algorithm has produced a matrix with no remaining NA, NaN, or missing value codes that would disrupt downstream statistical analyses.

## When NOT to use

- Input matrix already contains no missing values (filtering was sufficient) — skip directly to normalization.
- Imputation has not yet been applied — use the BPCA imputation skill first.
- Data are at a different preprocessing stage (e.g., post-normalization, post-QC filtering) — validation targets the imputation step specifically.

## Inputs

- BPCA-imputed metabolite abundance matrix (numeric table, R object or CSV/RDS format)
- Original filtered metabolite matrix metadata (feature and sample counts)

## Outputs

- Validation report (missing value count per feature, per sample, total)
- Complete imputed metabolite abundance matrix (CSV or RDS, verified NA-free)
- Boolean confirmation flag (all missing values successfully imputed: TRUE/FALSE)

## How to apply

Load the BPCA-imputed metabolite matrix into R and systematically verify that no missing values remain using functions like `sum(is.na(imputed_matrix))` or `anyNA(imputed_matrix)`. Check both feature (row) and sample (column) dimensions to ensure complete coverage. Confirm the imputed matrix maintains the expected dimensions and data type (numeric). Document the count of imputed values per feature and per sample to assess the severity of the original missingness pattern. Only export the matrix for downstream normalization once these checks confirm zero missing values across all features and samples.

## Related tools

- **marr** (R/Bioconductor package containing BPCA imputation implementation and msprepCOPD reference dataset; used to apply the imputation prior to validation) — https://github.com/Ghoshlab/marr
- **R** (Statistical computing environment for loading, inspecting, and validating the imputed matrix; hosts marr package and NA-detection functions)
- **Bioconductor** (Repository and framework for marr installation and SummarizedExperiment object handling)

## Examples

```
# In R after BPCA imputation:
library(marr)
imputed_check <- sum(is.na(imputed_matrix))
if(imputed_check == 0) { write.csv(imputed_matrix, 'imputed_metabolites_verified.csv'); cat('Validation passed: 0 missing values\n') } else { stop('Imputation incomplete: ', imputed_check, ' NAs remain') }
```

## Evaluation signals

- Output of `sum(is.na(imputed_matrix))` equals 0 for all features and samples combined.
- Output of `anyNA(imputed_matrix)` returns FALSE; no NA, NaN, or Inf values present.
- Imputed matrix dimensions (n_metabolites × n_samples) match the original filtered matrix dimensions.
- All values in the imputed matrix are numeric (no character, factor, or logical coercion required).
- Feature-wise and sample-wise missingness distributions show that previously sparse features (near 80% missing) now have complete coverage across all samples.

## Limitations

- BPCA imputation quality depends on the rank and structure of the underlying metabolite correlation matrix; low-rank or highly sparse data may produce less reliable imputed values despite absence of NAs.
- Validation confirms completeness but does not assess biological plausibility or accuracy of imputed values relative to true unmeasured metabolite abundances.
- The skill assumes the prior filtering step (removal of metabolites with >80% missingness) has already been performed; it does not validate the filtering threshold itself.

## Evidence

- [intro] filtering_and_imputation_workflow: "Filtering: Metabolites are removed if they are missing more than 80% of the samples; Missing value imputation technique: We apply Bayesian Principal Component Analysis (BPCA) to impute missing values"
- [methods] task_definition_verification_step: "Verify that no missing values remain in the imputed matrix"
- [methods] output_readiness_for_normalization: "Export the complete imputed metabolite abundance matrix as a numeric table (CSV or RDS format) ready for downstream median normalization"
- [intro] bpca_application_context: "BPCA is used as the missing value imputation technique applied to the metabolite dataset after filtering step and before median normalization"
