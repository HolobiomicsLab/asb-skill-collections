---
name: metabolite-missing-value-imputation
description: Use when metabolite assay tables contain missing values (NAs) that exceed detection or instrument runtime limits, AND you have retained metabolites with ≥60% non-missing data (i.e., ≤40% missingness).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - MetaboDiff
  - R
  - MultiAssayExperiment
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_marr_cq
    doi: 10.1186/s12859-021-04336-9
    title: marr
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
---

# metabolite-missing-value-imputation

## Summary

Impute missing metabolite measurements using k-nearest neighbor (kNN) imputation to recover sparse data while minimizing distortion of variance and normality. This skill is essential after data quality assessment and before normalization to maximize the usable metabolite feature set for downstream differential and network analysis.

## When to use

Apply this skill when metabolite assay tables contain missing values (NAs) that exceed detection or instrument runtime limits, AND you have retained metabolites with ≥60% non-missing data (i.e., ≤40% missingness). Use it before variance-stabilizing normalization to fill gaps that would otherwise force metabolite exclusion, provided kNN imputation has been shown to minimize effects on data normality and variance within your missingness threshold.

## When NOT to use

- Input metabolite set has already been imputed or contains no missing values.
- Missingness is >50% for the majority of metabolites (kNN imputation reliability degrades; consider filtering first).
- Analysis goal requires conservative hypothesis testing and you prefer to exclude metabolites with missing data rather than recover them via imputation.

## Inputs

- MultiAssayExperiment object with assay (metabolite measurement matrix with NAs)
- rowData (metabolite annotations)
- colData (sample metadata)
- cutoff parameter (float, 0–1; recommended 0.4 for ≤40% missingness threshold)

## Outputs

- MultiAssayExperiment object with imputed assay (no NAs, kNN-filled values)
- Metabolite set reduced to those passing cutoff threshold

## How to apply

Load the MultiAssayExperiment object containing the imputation-candidate metabolite assay and call knn_impute(met, cutoff=0.4), which performs k-nearest neighbor imputation on metabolites meeting the cutoff threshold. The cutoff parameter (e.g., 0.4) specifies the maximum tolerable fraction of missing values per metabolite (here, 40%); metabolites exceeding this threshold are excluded before imputation. kNN finds the k nearest metabolites (by Euclidean distance in sample space) for each missing value and imputes using their observed values in that sample. After imputation, verify that the sample clustering and variance structure are stable (inspect via na_heatmap before and outlier_heatmap after) and that no artificial outliers are introduced. The rationale is that kNN is robust to outliers and preserves the correlation structure of the data better than simple mean/median imputation.

## Related tools

- **MetaboDiff** (R package providing knn_impute() function for k-nearest neighbor imputation of metabolite measurements in MultiAssayExperiment objects) — https://github.com/andreasmock/MetaboDiff
- **MultiAssayExperiment** (Data container class (BioConductor) that wraps assay, rowData, and colData for structured passage to knn_impute())

## Examples

```
met = knn_impute(met, cutoff=0.4)
```

## Evaluation signals

- Verify that no NA values remain in the imputed assay matrix after knn_impute() completes.
- Confirm that the set of metabolites retained equals the count of metabolites with missingness ≤ cutoff (e.g., ≤40% missing).
- Check that outlier_heatmap applied post-imputation identifies the same or fewer outlier samples than pre-imputation na_heatmap, indicating kNN did not introduce artificial structure.
- Inspect quality_plot(met, group_factor=...) output to verify that imputed metabolites do not show abnormal distribution shifts or bimodality compared to metabolites with no imputation.
- Confirm that subsequent variance-stabilizing normalization (normalize_met) converges without numerical instability, which would indicate kNN preserved reasonable variance structure.

## Limitations

- kNN imputation reliability depends on the number of missing values; performance degrades if missingness >50% because few non-missing reference metabolites are available.
- kNN assumes that metabolite correlation structure is preserved across samples; if true biological subgroups exhibit distinct metabolic signatures, kNN may homogenize imputed values and obscure group separation.
- The cutoff parameter (e.g., 0.4) is a hard threshold; metabolites with exactly cutoff-fraction missingness are retained while those slightly above are excluded, which can be arbitrary. Sensitivity analysis across cutoff values (e.g., 0.3–0.5) is recommended.
- kNN imputation introduces artificial correlations among imputed values that can inflate network edge weights in subsequent correlation network analysis; downstream analyses should consider this when interpreting module assignments.

## Evidence

- [methods] kNN imputation parameters and threshold: "met = knn_impute(met,cutoff=0.4)"
- [methods] kNN imputation rationale for variance preservation: "imputation is performed by k-nearest neighbor imputation, which could be shown to minimize the effects on the normality and variance of the data as long as the number of missing data does not exceed"
- [methods] Workflow step description: kNN imputation after missing-value assessment: "Perform k-nearest neighbor imputation using knn_impute(met, cutoff=0.4), retaining only metabolites with ≥60% non-missing data."
- [intro] MetaboDiff package role in differential metabolomic analysis: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
- [methods] MultiAssayExperiment container integration: "The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis."
