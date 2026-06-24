---
name: feature-detection-rate-filtering
description: Use when after constructing a MetaboSet object with LC-MS peak abundances,
  sample metadata (pData with QC labels), and feature metadata (fData), and after
  marking missing values as NA.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - notame
  - R
  - Biobase
  - ExpressionSet
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package
  by Bioconductor'
- '```MetaboSet``` objects are the primary data structure of this package. ```MetaboSet```
  is built upon the ```ExpressionSet``` class'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_notame_cq
    doi: 10.3390/metabo10040135
    title: notame
  dedup_kept_from: coll_notame_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo10040135
  all_source_dois:
  - 10.3390/metabo10040135
  - 10.1093/bioinformatics/btr597
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-detection-rate-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identifies and flags LC-MS metabolomic features that fail to meet a minimum detection-rate threshold (e.g., 70% of QC samples) to exclude low-quality or sporadic features from downstream multivariate analysis. This filtering step operates on a MetaboSet object after data import and missing-value markup, removing features with insufficient QC reproducibility before imputation and statistical modeling.

## When to use

Apply this skill after constructing a MetaboSet object with LC-MS peak abundances, sample metadata (pData with QC labels), and feature metadata (fData), and after marking missing values as NA. Use it when your workflow requires quality-control filtering based on detection reproducibility—specifically, when you need to exclude features observed in fewer than a user-defined proportion (typically 70%) of QC replicates to reduce noise and improve signal-to-noise in subsequent multivariate models.

## When NOT to use

- Input data lacks QC sample replicates or does not include QC labeling in pData (flag_detection requires the QC column to identify replicates).
- Features have already been pre-filtered by the peak-picking software (e.g., MS-DIAL) and you do not need additional QC-based reproducibility filtering.
- Your analysis goal is to retain all detected features regardless of QC reproducibility (e.g., exploratory discovery in rare or low-abundance metabolites).

## Inputs

- MetaboSet object (ExpressionSet subclass) containing exprs matrix, pData sample metadata with QC column, fData feature metadata with Flag column

## Outputs

- Updated MetaboSet object with Flag column in fData annotated with non-NA values for features below detection-rate threshold

## How to apply

Load the MetaboSet object and apply the `flag_detection` function with a `qc_limit` parameter set to your acceptance threshold (e.g., 0.7 for 70%). The function calculates the proportion of QC samples in which each feature is detected (non-NA abundances) and updates the Flag column in the fData slot of the MetaboSet object with non-NA values for features that fall below the threshold. Features marked in the Flag column are then automatically excluded from downstream multivariate analyses when `all_features=FALSE` is set. This filtering operates as an early QC step, before imputation and batch correction, to remove features with inconsistent QC reproducibility that would otherwise propagate noise into statistical models.

## Related tools

- **notame** (Provides flag_detection function and MetaboSet data structure for QC-based feature filtering in non-targeted LC-MS metabolomics workflows) — https://github.com/hanhineva-lab/notame
- **Biobase** (Supplies ExpressionSet class upon which MetaboSet is built, enabling storage and manipulation of feature detection flags in fData)
- **R** (Execution environment for flag_detection function and MetaboSet object operations)

## Examples

```
flag_detection(metaboset_object, qc_limit=0.7)
```

## Evaluation signals

- Flag column in fData contains non-NA values only for features with detection rate below the qc_limit threshold (e.g., detected in <70% of QC samples); unflagged features have NA in the Flag column.
- When all_features=FALSE in downstream multivariate analyses, flagged features are excluded and do not appear in results, reducing feature count from the pre-filtered set.
- The detection rate for each flagged feature, calculated as the proportion of QC samples with non-NA abundances, is verifiable to be strictly less than the qc_limit parameter.
- Comparison of feature counts before and after flagging shows a reduction in total features proportional to the proportion of features with low QC reproducibility.
- Flagged features typically show high proportions of missing values across the entire dataset, confirming that QC-based filtering removes features with sparse detection patterns.

## Limitations

- Filtering depends entirely on the QC labeling scheme in pData—mislabeled or inconsistent QC annotations will produce unreliable flags.
- The threshold (qc_limit) is user-defined and requires prior knowledge or validation to set appropriately; too high a threshold may remove true metabolites with low QC signal, while too low a threshold may retain noise.
- Detection-rate filtering is agnostic to the magnitude or signal-to-noise ratio of abundances; a feature detected in 70% of QCs but with very low or noisy signal may still pass but contribute little to downstream analyses.
- The notame package API is described as 'still quite experimental, and breaking changes are possible,' which may affect reproducibility and compatibility across versions.

## Evidence

- [other] flag_detection function and its role in QC filtering: "The flag_detection function flags features based on their detection rate, operating as a filter step in the notame workflow to identify features failing quality acceptance criteria by updating the"
- [other] Concrete workflow: apply flag_detection with qc_limit=0.7: "Apply flag_detection with qc_limit=0.7 to identify features not observed in at least 70% of QC samples."
- [other] Flag column update mechanism: "Update the Flag column in fData to record flagged features with non-NA values."
- [other] Downstream exclusion of flagged features: "Verify that flagged features are excluded from subsequent multivariate analyses by default (all_features=FALSE)."
- [other] Position in workflow: after missing-value markup, before imputation: "Next, flag all the features with extensive amounts of missing values"
- [readme] MetaboSet data structure for QC-based filtering: "MetaboSet is built upon the ExpressionSet class from the Biobase package by Bioconductor"
- [readme] Non-targeted LC-MS metabolomics application context: "This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics."
