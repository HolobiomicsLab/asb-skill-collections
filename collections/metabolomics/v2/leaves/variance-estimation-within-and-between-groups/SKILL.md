---
name: variance-estimation-within-and-between-groups
description: Use when you have a QC-annotated LC-MS feature intensity table (CSV or
  data frame) with replicate QC samples and biological samples from multiple batches
  or run orders, and you need to assess which features maintain consistent signal
  intensity across technical replicates (within-group) relative to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0092
  tools:
  - R ≥4.1.2
  - R
  - OUKS
  - MetCorR
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.1c00392
  title: Omics Untargeted Key Script
evidence_spans:
- '[![](https://img.shields.io/badge/R≥4.1.2-5fb9ed.svg?style=flat&logo=r&logoColor=white?)](https://cran.r-project.org/index.html)'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# variance-estimation-within-and-between-groups

## Summary

Estimate within-group and between-group variance components for LC-MS metabolomic features to compute quality metrics (D-Ratio) that assess feature reliability in QC-annotated datasets. This skill enables discrimination of robust features from those affected by instrumental drift or batch effects.

## When to use

You have a QC-annotated LC-MS feature intensity table (CSV or data frame) with replicate QC samples and biological samples from multiple batches or run orders, and you need to assess which features maintain consistent signal intensity across technical replicates (within-group) relative to their mean intensity (between-group). Apply this skill before filtering to identify and remove unreliable features in Step 4 (Correction) or Step 6 (Filtering) of the OUKS workflow.

## When NOT to use

- Input is already a quality-filtered or pre-screened feature table with low-quality features already removed.
- No QC replicate samples are available in the dataset (D-Ratio requires replicate QC intensities).
- Feature intensities have already been normalized or log-transformed in ways that obscure the original within-sample variance structure.

## Inputs

- QC-annotated feature intensity table (CSV or R data frame)
- Feature identifiers (m/z, retention time, or compound name)
- Sample metadata with QC replicate labels and batch/run-order information

## Outputs

- D-Ratio data frame with feature identifiers and corresponding D-Ratio scores
- CSV file of D-Ratio table for export and downstream filtering

## How to apply

Extract intensity values for each feature from QC sample replicates and all samples. For each feature, calculate within-group variance as the pooled standard deviation across all samples (or within QC replicates specifically), and between-group variance as the mean intensity in QC replicates or the ratio of mean-to-standard-deviation. Compute the D-Ratio as the ratio of between-group variance (or mean QC intensity) to within-group variance (pooled SD). Higher D-Ratio values indicate features with greater signal intensity relative to technical noise, making them more reliable for downstream biomarker discovery. Compile per-feature D-Ratio scores into a data frame indexed by feature identifier, suitable for threshold-based filtering in Step 6.

## Related tools

- **R** (Primary scripting environment for calculating D-Ratio variance components and compiling output tables) — https://cran.r-project.org/index.html
- **OUKS** (Comprehensive LC-MS metabolomics workflow; Step 4 (Correction) implements D-Ratio computation, Step 6 (Filtering) applies D-Ratio thresholds) — https://github.com/plyush1993/OUKS
- **MetCorR** (QC-based signal drift correction using GAMs; complements D-Ratio by using QC samples to model and remove instrumental drift before variance estimation) — https://github.com/plyush1993/MetCorR

## Examples

```
# Load QC-annotated feature table and compute D-Ratio
feature_table <- read.csv('features.csv', row.names=1)
qc_samples <- colnames(feature_table)[grepl('QC', colnames(feature_table))]
qc_intensity <- feature_table[, qc_samples]
mean_qc <- rowMeans(qc_intensity)
sd_pooled <- apply(feature_table, 1, sd)
d_ratio <- mean_qc / sd_pooled
d_ratio_df <- data.frame(feature_id=rownames(feature_table), d_ratio=d_ratio)
write.csv(d_ratio_df, 'D_Ratio_output.csv', row.names=FALSE)
```

## Evaluation signals

- D-Ratio values are numeric and positive; no NaN or Inf values for valid features with non-zero QC intensity and variance.
- D-Ratio distribution has expected shape: higher median D-Ratio for high-confidence features (e.g., annotated metabolites) vs. lower for noise-like features.
- Features filtered using D-Ratio threshold show improved correlation stability in downstream statistical analyses (e.g., reduced variance in biomarker candidate sets).
- QC sample replicates produce identical or near-identical D-Ratio values for the same feature, confirming reproducibility of variance estimation.
- D-Ratio values are inversely correlated with coefficient of variation (CV) across samples, validating that high D-Ratio reflects low technical noise.

## Limitations

- D-Ratio computation requires at least 2 QC replicates; datasets with <2 QC replicates cannot estimate within-group variance reliably.
- D-Ratio is sensitive to outlier intensity values; preprocessing steps (e.g., removal of extreme values or imputation method) can affect ratio calculation.
- No published guidance on optimal D-Ratio threshold for filtering; threshold selection may require pilot data or empirical tuning for each LC-MS platform and metabolite class.
- D-Ratio assumes QC replicates are representative of feature behavior across all biological samples; if QC composition differs significantly from study samples, D-Ratio may not reflect true feature reliability in the biological context.

## Evidence

- [other] Calculate the D-Ratio for each feature as the ratio of between-group variance to within-group variance (or mean intensity in QC replicates to pooled standard deviation across all samples): "Calculate the D-Ratio for each feature as the ratio of between-group variance to within-group variance (or mean intensity in QC replicates to pooled standard deviation across all samples), following"
- [other] OUKS step 4 (Correction) implements D-Ratio as a quality metric for evaluating features in QC-annotated metabolomic data, with outputs subsequently used in step 6 (Filtering) where D-Ratio filtering is applied to remove unreliable features.: "OUKS step 4 (Correction) implements D-Ratio as a quality metric for evaluating features in QC-annotated metabolomic data, with outputs subsequently used in step 6 (Filtering) where D-Ratio filtering"
- [readme] 4. Correction: D-Ratio metric, RLA-plot, correlogram, 2-factors PCA: ""4. Correction": D-Ratio metric, RLA-plot, correlogram, 2-factors PCA"
- [readme] 6. Filtering: D-Ratio filtering was added.: ""6. Filtering": D-Ratio filtering was added."
- [readme] R based open-source collection of scripts called OUKS (Omics Untargeted Key Script) providing comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox: "R based open-source collection of scripts called :red_circle:*OUKS*:large_blue_circle: (*Omics Untargeted Key Script*) providing comprehensive nine step LC-MS untargeted metabolomic profiling data"
