---
name: dmodx-orthogonal-distance-metric
description: Use when apply DModX when you have a normalized LC-MS feature matrix (post-normalization, Step 7 in OUKS) and need to identify samples whose metabolomic profiles are systematically displaced from the learned PCA subspace—indicating potential technical artifacts, extreme biological phenotypes, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R ≥4.1.2
  - R
  - 'OUKS (Step 9: Statistics.R)'
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jproteome.1c00392
  title: Omics Untargeted Key Script
evidence_spans:
- '[![](https://img.shields.io/badge/R≥4.1.2-5fb9ed.svg?style=flat&logo=r&logoColor=white?)](https://cran.r-project.org/index.html)'
- R based open-source collection of scripts called :red_circle:*OUKS*
- R ≥4.1.2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omics_untargeted_key_script_cq
    doi: 10.1021/acs.jproteome.1c00392
    title: Omics Untargeted Key Script
  dedup_kept_from: coll_omics_untargeted_key_script_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.1c00392
  all_source_dois:
  - 10.1021/acs.jproteome.1c00392
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# DModX Orthogonal Distance Metric

## Summary

DModX (Distance to Model in X-space) quantifies the orthogonal distance of each sample from the principal component model subspace in untargeted LC-MS metabolomic data, enabling detection of samples that deviate structurally from the main dataset population. This metric complements Hotelling T-squared for robust multivariate outlier detection in preprocessed feature matrices.

## When to use

Apply DModX when you have a normalized LC-MS feature matrix (post-normalization, Step 7 in OUKS) and need to identify samples whose metabolomic profiles are systematically displaced from the learned PCA subspace—indicating potential technical artifacts, extreme biological phenotypes, or sample contamination that should be flagged before statistical hypothesis testing.

## When NOT to use

- Input feature matrix has not been normalized (Box-Cox or equivalent); DModX is most interpretable on variance-stabilized data.
- Sample size is extremely small (<10–15); PCA model and percentile thresholds become unstable with insufficient training data.
- You have already filtered or removed obvious outliers by other means (e.g., QC-based drift correction); DModX may flag fewer additional samples.

## Inputs

- Preprocessed feature matrix (normalized, post-Step 7 normalization)
- Sample metadata (optional, for stratified threshold definition)

## Outputs

- Per-sample DModX scores (numeric vector)
- Per-sample outlier flags (logical/binary vector)
- Tabular outlier report with sample IDs, DModX scores, and threshold status

## How to apply

After normalization (Box-Cox transformation), construct a PCA model on the preprocessed feature matrix to define the principal component subspace. For each sample, compute its orthogonal projection residual—the Euclidean distance from the sample to its projection onto the PCA subspace. Establish a DModX threshold (typically the 95th percentile of the training distribution or a user-specified limit based on expected model fit). Flag samples exceeding this threshold as outliers. Output per-sample DModX scores and binary outlier status (TRUE/FALSE). The rationale is that legitimate samples cluster near the model, while outliers (batch effects, instrument drift, biological extremes) produce large residuals in the X-space orthogonal to the learned components.

## Related tools

- **R** (Computational environment for PCA model construction, orthogonal distance calculation, and outlier flag generation) — https://cran.r-project.org/index.html
- **OUKS (Step 9: Statistics.R)** (End-to-end R script implementing DModX alongside Hotelling T-squared for integrated multivariate outlier detection) — https://github.com/plyush1993/OUKS

## Examples

```
# Load normalized feature matrix post-Step 7; compute PCA and DModX outlier scores
pca_model <- prcomp(feature_matrix, scale=TRUE, center=TRUE)
ordist <- rowSums((feature_matrix - predict(pca_model)) ^ 2) ^ 0.5
dmodx_threshold <- quantile(ordist, 0.95)
outlier_flags <- ordist > dmodx_threshold
outlier_report <- data.frame(sample_id=rownames(feature_matrix), DModX=ordist, outlier=outlier_flags)
```

## Evaluation signals

- DModX scores are non-negative, non-zero for all samples, with a right-skewed distribution typical of distance metrics.
- Outlier flags (TRUE/FALSE) are consistent with visual PCA score plots—flagged samples should appear distant from the main ellipse cloud.
- Approximately 5% of samples are flagged at the 95th percentile threshold (or close to the user-specified limit), validating threshold calibration.
- Joint inspection with Hotelling T-squared: samples flagged by DModX should largely differ from those flagged by T-squared alone, indicating complementary information (orthogonal vs. Mahalanobis distance).
- Flagged samples correlate with known batch effects, instrument drift timestamps, or biological extremes (e.g., disease severity outliers) when metadata are available.

## Limitations

- DModX depends on PCA model quality; if the number of PCs is poorly chosen (too few or too many), threshold calibration and outlier detection sensitivity may degrade.
- No guidance provided in the OUKS paper or README on automatic PC selection or sensitivity analysis for threshold tuning; practitioner must specify these parameters manually.
- DModX is sensitive to the preprocessing method (normalization, imputation strategy); different Box-Cox implementations or missing-value fill methods will alter scores.
- The metric assumes that legitimate samples cluster in a lower-dimensional subspace; highly heterogeneous biological cohorts (e.g., multiple disease subtypes with distinct metabolomes) may not satisfy this assumption, leading to high false-positive outlier flags.
- Computational scalability and performance characteristics for very large datasets (>10,000 samples or >10,000 features) are not documented.

## Evidence

- [other] Compute DModX (distance to model in X-space) metric as the orthogonal distance of each sample from the principal component model subspace.: "Compute DModX (distance to model in X-space) metric as the orthogonal distance of each sample from the principal component model subspace."
- [other] Define outlier thresholds for T-squared (e.g., critical value from F-distribution or 95th percentile) and DModX (95th percentile or user-specified limit).: "Define outlier thresholds for T-squared (e.g., critical value from F-distribution or 95th percentile) and DModX (95th percentile or user-specified limit)."
- [other] Flag samples exceeding either threshold as outliers and generate per-sample outlier status (TRUE/FALSE) with associated scores.: "Flag samples exceeding either threshold as outliers and generate per-sample outlier status (TRUE/FALSE) with associated scores."
- [readme] comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox: "comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox"
