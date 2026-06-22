---
name: left-censored-missing-value-classification
description: Use when you have a metabolomics dataset (LC/MS or GC/MS) with missing values and need to determine which are below the limit of detection (LOD) or limit of quantification (LOQ). Left-censored classification is necessary when the missingness is informative—i.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - R
  - GSimp
  - imputeLCMD (R package)
  - Trunc_KNN
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1005973
  title: GSimp
evidence_spans:
- '**GSimp.R** contains the core functions for GSimp'
- GSimp.R contains the core functions for GSimp
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gsimp_cq
    doi: 10.1371/journal.pcbi.1005973
    title: GSimp
  dedup_kept_from: coll_gsimp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1005973
  all_source_dois:
  - 10.1371/journal.pcbi.1005973
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# left-censored-missing-value-classification

## Summary

Identify and flag left-censored missing values in metabolomics data by distinguishing them from other missingness mechanisms (MCAR/MAR) based on detection limits and instrumental thresholds. This classification is essential for selecting appropriate imputation strategies, as left-censored missingness violates MCAR assumptions and requires truncated distributional methods.

## When to use

Apply this skill when you have a metabolomics dataset (LC/MS or GC/MS) with missing values and need to determine which are below the limit of detection (LOD) or limit of quantification (LOQ). Left-censored classification is necessary when the missingness is informative—i.e., when a metabolite feature failed to be quantified or detected due to instrumental sensitivity constraints rather than random absence or biological non-detection.

## When NOT to use

- Do not apply this skill to datasets where missingness is already confirmed to be MCAR/MAR (e.g., random sample drop-out, incomplete data collection) without instrumental thresholds—use non-truncated imputation instead.
- Do not use this skill when the data has already undergone value imputation or thresholding—classification must occur on raw or post-retrieval, pre-imputation data.
- Do not apply to datasets where the detection limit is unknown or undocumented, as the distinction between left-censored and other missingness cannot be reliably made.

## Inputs

- metabolomics data matrix (rows=samples, columns=metabolite features) with NA or zero encoding for missing values
- instrumental metadata: LOD/LOQ thresholds per feature or per assay batch
- optional: manual retrieval flags or post-retrieval annotation for untargeted data

## Outputs

- classified missing-value indicator matrix (left-censored vs. other missingness)
- detection limit boundary per feature (minimum non-missing value or quantile)
- missingness mechanism summary (left-censored proportion, MNAR evidence)

## How to apply

Load your metabolomics data matrix (rows=samples, columns=metabolite features) with missing values encoded as NA or zero. Compare the distribution of non-missing values in each feature against the instrumental detection threshold (LOD/LOQ) for that feature or assay batch. Flag any missing values that fall structurally below the minimum non-missing value as left-censored; this indicates the metabolite was present but undetectable. If manual retrieval has been performed (as in untargeted GC/MS workflows), exclude manually recovered values from the left-censored pool. Document the detection limit boundary for each feature, as this upper bound (hi='min' or quantile) will constrain the imputation model. Missingness in untargeted data with overlap between non-missing and retrieved values may indicate MCAR/MAR instead, requiring non-truncated methods.

## Related tools

- **GSimp** (provides missing value classification and left-censored imputation wrapper functions) — https://github.com/WandeRum/GSimp
- **imputeLCMD (R package)** (provides QRILC and impute.QRILC functions for quantile regression imputation of left-censored data)
- **Trunc_KNN** (kNN-TN algorithm for truncation-aware k-nearest neighbors imputation of left-censored data)

## Examples

```
source('GSimp.R'); NA_pos <- which(is.na(untargeted_data), arr.ind=TRUE); data_raw_log <- untargeted_data %>% log(); data_raw_log_qrilc <- impute.QRILC(data_raw_log) %>% extract2(1); hi_bound <- sapply(data_raw_log_qrilc, function(x) min(x, na.rm=TRUE)); left_censored_flag <- data.frame(row=NA_pos[,1], col=NA_pos[,2], is_left_censored=(data_raw_log_qrilc[NA_pos] < hi_bound[NA_pos[,2]]))
```

## Evaluation signals

- Verify that the proportion of left-censored values aligns with expected instrumental sensitivity and sample/compound complexity (e.g., untargeted GC/MS ~0.8% post-retrieval; targeted LC/MS with LOQ/LOD failures ~2.1%).
- Check that the detected upper bounds (minimum non-missing or quantiles per feature) are consistent with reported instrumental LOD/LOQ and do not fall above feature-specific maxima.
- Confirm that left-censored classification is mutually exclusive from MCAR/MAR (i.e., overlapping distributions in untargeted data after retrieval should reclassify to MCAR, not left-censored).
- Validate that the classified left-censored positions match the positions later used in the Gibbs sampler truncation bounds (lo=-Inf, hi='min') without drift or re-encoding.
- Cross-check classified missing positions against instrumental log files or batch metadata to confirm missingness co-occurs with expected LOD/LOQ exceedances, not with sample preparation failures.

## Limitations

- Classification depends critically on accurate LOD/LOQ metadata; undocumented or batch-variable thresholds will lead to misclassification.
- Untargeted metabolomics workflows with manual retrieval may blur the boundary between left-censored and MCAR/MAR; post-retrieval overlap in distributions requires re-evaluation of missingness mechanism.
- Classification is feature-specific: a single missing value may be left-censored in one context (strict LOQ) and MCAR in another (loose LOQ); threshold selection (e.g., minimum vs. 10% quantile) alters classification outcome.
- Left-censored classification does not account for right-censored missingness (high-intensity saturation or overflow), which requires opposite bounds (lo='max', hi=Inf) and is not addressed by GSimp's core design.
- If detection limits are estimated post-hoc from the non-missing distribution (e.g., 'min' value), circular reasoning can inflate left-censored counts; independent instrumental calibration is preferable.

## Evidence

- [other] Identify and flag left-censored missing values (detection limit threshold) using GSimp's missing value classification.: "Identify and flag left-censored missing values (detection limit threshold) using GSimp's missing value classification."
- [other] GSimp implements a Gibbs sampler based approach for left-censored missing value imputation, with core functions provided in GSimp.R that enable application to metabolomics datasets.: "GSimp implements a Gibbs sampler based approach for left-censored missing value imputation, with core functions provided in GSimp.R that enable application to metabolomics datasets."
- [readme] The targeted LC/MS dataset contains 40 samples and 41 variables with 88 missing elements are failed to be quantified due to LOQ/LOD.: "The targeted LC/MS dataset contains 40 samples and 41 variables with 88 missing elements are failed to be quantified due to LOQ/LOD."
- [readme] we found overlaps between non-missing values and retrieved missing values. Thus, we assumed that the majority of missingness in untargeted GC/MS-based metabolomics data are MCAR/MAR.: "we found overlaps between non-missing values and retrieved missing values. Thus, we assumed that the majority of missingness in untargeted GC/MS-based metabolomics data are MCAR/MAR."
- [readme] lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part: "lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part"
