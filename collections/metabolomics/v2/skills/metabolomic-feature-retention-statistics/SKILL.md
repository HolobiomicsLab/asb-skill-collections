---
name: metabolomic-feature-retention-statistics
description: Use when after applying the CV_ratio() filtering function to a normalized metabolomic feature matrix (e.g., Urine_RP_NEG_norm.txt) in margheRita, generate retention statistics to report how many features passed the threshold (CV ratio > 1.0) and characterize the distribution of retained CV ratios.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - margheRita
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow
- The R package margheRita
- The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-feature-retention-statistics

## Summary

Quantify and report the feature count and coefficient-of-variation distribution before and after applying a CV-ratio filter to metabolomic feature matrices. This skill documents the filtering outcome and provides summary statistics needed to assess data reduction and filter efficacy.

## When to use

After applying the CV_ratio() filtering function to a normalized metabolomic feature matrix (e.g., Urine_RP_NEG_norm.txt) in margheRita, generate retention statistics to report how many features passed the threshold (CV ratio > 1.0) and characterize the distribution of retained CV ratios. Use this skill whenever you need to quantify the impact of quality-control filtering on feature count and provide evidence of feature stability across sample groups.

## When NOT to use

- Input is already a filtered or pre-screened feature table without access to the original unnormalized data or CV ratio calculations.
- Sample metadata does not clearly distinguish QC from non-QC samples, making CV stratification impossible.
- CV_ratio() has not yet been applied, or no threshold filtering has been performed (skill addresses post-filter statistics, not pre-filter exploration).

## Inputs

- Normalized metabolomic feature matrix (e.g., from MS-DIAL output via margheRita, dimensions: features × samples)
- Sample metadata annotating QC vs. non-QC sample status
- CV ratio vector output from CV_ratio() function (one ratio per feature)

## Outputs

- Feature retention summary table (feature counts before/after, count retained, percentage retained)
- CV ratio distribution statistics (median, mean, min, max, quartiles of retained features)
- Filtered feature matrix (features × samples, subset to retained features only)
- Optional visualization (histogram or density plot of CV ratio distribution)

## How to apply

After calling CV_ratio() on your normalized feature matrix (with QC vs. non-QC sample annotations), compute and report: (1) feature count before and after filtering (e.g., 539 → 303); (2) the distribution of CV ratios for retained features (median, mean, percentiles); (3) percentage of features retained; and (4) optionally, the range and quartiles of CV ratios to characterize feature stability. The CV ratio threshold (default 1.0) ensures retained features show greater variation in real samples than in QC samples, indicating biological signal rather than instrumental noise. Document these metrics in a summary table and optionally visualize the CV ratio distribution (e.g., histogram or density plot) to assess filtering stringency.

## Related tools

- **margheRita** (Provides CV_ratio() function to compute and apply coefficient-of-variation ratio filtering; outputs filtered feature matrix and CV ratio statistics.) — https://github.com/emosca-cnr/margheRita
- **R** (Statistical computing environment for calculating and summarizing CV ratio distributions and generating summary tables and plots.)

## Examples

```
# After applying CV_ratio() filtering in margheRita:
# Compute and report retention statistics
feature_count_before <- 539; feature_count_after <- 303
retention_pct <- (feature_count_after / feature_count_before) * 100
cat(sprintf('Features retained: %d/%d (%.1f%%)\nMedian CV ratio: 1.1032\n', feature_count_after, feature_count_before, retention_pct))
```

## Evaluation signals

- Feature count before and after filtering matches the input and output dimensions of the filtered feature matrix (e.g., 539 → 303 features).
- Retention percentage is between 0 and 100% and represents the proportion of features with CV ratio > threshold.
- Median and mean CV ratios of retained features are ≥ 1.0 (or equal to the applied threshold), confirming all retained features meet the filtering criterion.
- CV ratio distribution (histogram or density plot) shows a unimodal or multimodal distribution centered at or above the threshold, with no retained features below 1.0.
- Summary statistics are accompanied by the original feature count, threshold used (default 1.0), and date/tool version (margheRita), enabling reproducibility and audit trail.

## Limitations

- CV ratio filter relies on adequate QC sample replication; insufficient QC samples (e.g., <3) may produce unstable CV estimates and misleading ratios.
- Filter does not account for features with zero or near-zero variance in QC samples, which could produce undefined or infinite CV ratios; these edge cases must be handled separately.
- Retention statistics are threshold-dependent; changing the CV ratio threshold (default 1.0) will alter feature count and distribution; threshold choice should be justified by biological context or prior validation.
- CV ratio filtering assumes normalization has been applied; unnormalized or poorly normalized data may produce biased or uninformative CV ratios.

## Evidence

- [other] Feature retention and CV ratio distribution from task_003: "The CV_ratio() function retains only features with a CV ratio (non-QC samples / QC samples) exceeding the default threshold of 1, producing a distribution with median 1.1032 and resulting in 303"
- [other] CV_ratio filtering workflow step: "Compute the CV ratio (CV_non-QC / CV_QC) for each feature. Apply the threshold filter, retaining only features where CV_ratio > 1.0. Output the filtered feature table and generate summary statistics"
- [readme] margheRita capability for CV-based filtering: "filtering by coefficient of variation (samples vs QCs) and probabilistic quotient normalization"
- [readme] MS-DIAL workflow context for margheRita: "The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)."
