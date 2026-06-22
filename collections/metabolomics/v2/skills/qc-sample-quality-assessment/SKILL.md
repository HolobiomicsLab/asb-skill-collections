---
name: qc-sample-quality-assessment
description: Use when after drift correction and before imputation when you have LC-MS data with designated QC samples and you need to remove features with poor reproducibility across QC replicates.
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
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package by Bioconductor'
- '```MetaboSet``` objects are the primary data structure of this package. ```MetaboSet``` is built upon the ```ExpressionSet``` class'
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
---

# QC Sample Quality Assessment

## Summary

Flag and filter molecular features in LC-MS metabolomics data based on their detection rate across Quality Control (QC) samples to remove low-quality features before multivariate analysis. This is a critical quality-control step in the notame preprocessing workflow that identifies features failing to meet minimum reproducibility thresholds.

## When to use

Apply this skill after drift correction and before imputation when you have LC-MS data with designated QC samples and you need to remove features with poor reproducibility across QC replicates. The skill is particularly important when QC samples are available to benchmark detection consistency and when downstream multivariate analyses require high-confidence features.

## When NOT to use

- QC samples are not available or QC sample labels are not present in the pData QC column.
- The data has already been filtered to remove low-detection features by external peak-picking software.
- Analysis goals require using all detected features regardless of reproducibility (use all_features=TRUE instead).

## Inputs

- MetaboSet object containing LC-MS abundances (exprs), sample metadata (pData with QC sample labels in QC column), and feature information (fData)

## Outputs

- MetaboSet object with updated Flag column in fData marking features that fail the 70% QC detection-rate threshold with non-NA values
- Binary feature inclusion/exclusion status usable for downstream filtering in multivariate analyses

## How to apply

Use the flag_detection function from notame on a MetaboSet object with a qc_limit parameter set to 0.7 (the 70% QC detection-rate acceptance threshold). The function identifies features not observed in at least 70% of QC samples and updates the Flag column in the fData slot with non-NA values to mark failed features. This flagged status is then used downstream to filter features (via all_features=FALSE) before entering multivariate analyses, effectively excluding low-reproducibility features while preserving the full feature set for reference.

## Related tools

- **notame** (Provides flag_detection function to flag features based on QC sample detection rate; bundles LC-MS preprocessing methods including quality control filtering) — https://github.com/hanhineva-lab/notame
- **Biobase** (Provides ExpressionSet class structure underlying MetaboSet object that stores fData, pData, and exprs matrices)
- **R** (Execution environment for flag_detection and MetaboSet object manipulation)

## Examples

```
flag_detection(metaboset_object, qc_limit = 0.7)
```

## Evaluation signals

- Flag column in fData contains non-NA values exclusively for features with detection rate < 70% across QC samples; all other features have NA values.
- Verify that flagged features are reproducibly excluded when all_features=FALSE is used in downstream multivariate analyses by checking feature lists before and after filtering.
- Cross-check detection rates: manually calculate the proportion of non-zero/non-NA abundances for flagged features across QC samples and confirm they fall below the 0.7 threshold.
- Confirm QC sample identification: verify that the QC column in pData correctly identifies all QC replicates used in the detection-rate calculation.
- Post-filtering feature count should be lower than pre-filtering count; the reduction magnitude indicates the stringency of the 70% threshold applied.

## Limitations

- The 70% threshold is a fixed default; features with detection rates slightly below this cutoff may still be useful in specific applications but will be unconditionally flagged.
- QC sample labeling must be accurate and complete in the QC column of pData; mislabeled or missing QC identifiers will produce incorrect detection-rate calculations.
- The method assumes QC samples are representative replicates of the entire sample set; if QC samples have different matrix properties or are spiked differently, detection-rate comparisons may not reflect true feature reproducibility in biological samples.
- The notame package API is experimental and subject to breaking changes; function signatures and default parameters may change between versions.

## Evidence

- [other] The flag_detection function flags features based on detection rate, operating as a filter step in the notame workflow to identify features failing quality acceptance criteria by updating the Flag column of the MetaboSet object.: "The flag_detection function flags features based on detection rate, operating as a filter step in the notame workflow to identify features failing quality acceptance criteria by updating the Flag"
- [other] Apply flag_detection with qc_limit=0.7 to identify features not observed in at least 70% of QC samples. Update the Flag column in fData to record flagged features with non-NA values. Verify that flagged features are excluded from subsequent multivariate analyses by default (all_features=FALSE).: "Apply flag_detection with qc_limit=0.7 to identify features not observed in at least 70% of QC samples. Update the Flag column in fData to record flagged features with non-NA values. Verify that"
- [other] ```flag_detection``` is used to flag features based on detection: "```flag_detection``` is used to flag features based on detection"
- [other] Next, flag all the features with extensive amounts of missing values: "Next, flag all the features with extensive amounts of missing values"
- [readme] The package API is still quite experimental, and breaking changes are possible: "The package API is still quite experimental, and breaking changes are possible"
