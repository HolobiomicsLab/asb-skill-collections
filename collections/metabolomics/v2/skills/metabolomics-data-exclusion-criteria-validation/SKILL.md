---
name: metabolomics-data-exclusion-criteria-validation
description: Use when you have received or published a claim about the number of metabolites
  excluded by a missingness-based quality filter (e.g., 'cutoff=0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - R
  - MetaboDiff
  - MultiAssayExperiment
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty344
  all_source_dois:
  - 10.1093/bioinformatics/bty344
  - 10.1158/0008-5472.can-14-1490
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-exclusion-criteria-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate and reproduce the count of metabolites excluded from a metabolomics dataset by applying a missingness cutoff threshold during imputation preprocessing. This skill ensures that the imputation filter is applied correctly and reproducibly, and that the number of retained metabolites matches the stated exclusion count.

## When to use

Apply this skill when you have received or published a claim about the number of metabolites excluded by a missingness-based quality filter (e.g., 'cutoff=0.4 excludes 69 metabolites'), and you need to independently verify that claim by re-running the imputation step on the raw assay matrix and counting the excluded set. Use this before downstream analysis to confirm data preprocessing integrity.

## When NOT to use

- Input assay matrix is already imputed or post-QC; exclusion validation requires the raw, pre-imputation matrix with intact missing-value patterns.
- No published exclusion count is available; this skill is designed to validate a specific quantitative claim, not to discover optimal filtering thresholds.
- Cutoff parameter differs substantially from the published value (e.g., published cutoff=0.4 but you only have access to cutoff=0.3 results); the excluded count will not be comparable.

## Inputs

- Raw metabolomics assay matrix (metabolites × samples) with missing values
- Sample metadata indicating experimental groups (e.g., tumor vs. normal)
- Stated missingness cutoff threshold (e.g., 0.4)

## Outputs

- Count of metabolites excluded by the cutoff
- Count of metabolites retained after filtering
- List/set of excluded metabolite identifiers
- Comparison report confirming agreement with published exclusion count

## How to apply

Load the metabolomics dataset (raw assay matrix with samples as columns and metabolites as rows) into R and inspect the missing-value patterns. Apply the knn_impute function from MetaboDiff with the stated cutoff parameter (e.g., cutoff=0.4 to retain only metabolites missing in ≤40% of samples). Extract the metabolite identifiers from both the raw assay and the imputed assay slots. Count the metabolites in each and compute the difference to identify the excluded set. Verify that the excluded count matches the published claim and document the retained metabolite count and the identities of excluded metabolites for reproducibility.

## Related tools

- **MetaboDiff** (Provides knn_impute() function to apply missingness-based metabolite exclusion and inspect imputed assay slot) — https://github.com/andreasmock/MetaboDiff
- **R** (Host environment for MetaboDiff; used to load data, call knn_impute, and perform counting and comparison logic)
- **MultiAssayExperiment** (Data container accessed via create_mae() to organize metabolite assay matrix, rowData (metabolite annotations), and colData (sample metadata))

## Examples

```
library("MetaboDiff"); met <- knn_impute(met_example, cutoff=0.4); nrow_before <- nrow(assay(met_example)); nrow_after <- nrow(assay(met)); excluded_count <- nrow_before - nrow_after; print(paste("Excluded:", excluded_count, "metabolites"))
```

## Evaluation signals

- Excluded metabolite count from independent re-run exactly matches the published claim (e.g., 69 metabolites for cutoff=0.4 on met_example tumor-vs-normal dataset).
- Retained metabolite count = (raw metabolite count − excluded count); verify arithmetic consistency.
- Excluded metabolites are precisely those with missingness ≥ cutoff across all samples; inspect the missingness vector for each excluded metabolite to confirm it exceeds the threshold.
- The imputed assay contains no metabolites that should have been excluded by the cutoff criterion; verify that all retained metabolites have missingness ≤ cutoff.
- Downstream analyses (e.g., normalization, PCA, correlation network) use the same retained metabolite set as reported; confirm assay dimensions in downstream outputs match the validated retained count.

## Limitations

- knn_impute performance depends on input data quality and correlation structure; the exclusion count is deterministic given the cutoff, but the accuracy of imputed values is not directly validated by this skill.
- The skill only confirms that the stated cutoff produces the stated excluded count on the stated dataset; it does not assess whether the cutoff value itself is optimal or appropriate for the biological context.
- Missing-value patterns may vary across data acquisition batches or preprocessing pipelines; reproducibility of the excluded count requires identical raw input matrices.
- No built-in handling for edge cases such as metabolites with identical or near-identical missingness patterns; manual inspection may be needed if the excluded set is unusually large or small.

## Evidence

- [other] Application of knn_impute with cutoff=0.4 to the met_example tumor-vs-normal dataset results in exclusion of 69 metabolites that exceed the missingness threshold.: "finding: Application of knn_impute with cutoff=0.4 to the met_example tumor-vs-normal dataset results in exclusion of 69 metabolites that exceed the missingness threshold."
- [other] Call knn_impute(met_example, cutoff=0.4) to retain only metabolites with non-missing measurements in ≥60% of samples (i.e., missing in ≤40%). Extract and count the metabolites in the imputed assay slot and compare to the raw count to identify the number excluded.: "Call knn_impute(met_example, cutoff=0.4) to retain only metabolites with non-missing measurements in ≥60% of samples (i.e., missing in ≤40%). Extract and count the metabolites in the imputed assay"
- [methods] The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis.: "The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis."
- [methods] imputation is performed by k-nearest neighbor imputation, which could be shown to minimize the effects on the normality and variance of the data as long as the number of missing data does not exceed [cutoff]: "imputation is performed by k-nearest neighbor imputation, which could be shown to minimize the effects on the normality and variance of the data as long as the number of missing data does not exceed"
- [readme] The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements.: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
