---
name: qc-biological-sample-stratification
description: Use when after metabolomics data normalization when both QC (quality control) and biological samples have been used in the same normalization run.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - Metanorm
derived_from:
- doi: 10.1101/2025.09.30.679445v1
  title: Metanorm
- doi: 10.1021/acs.analchem.5c06841
  title: ''
evidence_spans:
- The R package implements three (new) robust normalization methods
- Metanorm supports robust metabolomics data normalization across scales and experimental designs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metanorm_cq
    doi: 10.1101/2025.09.30.679445v1
    title: Metanorm
  dedup_kept_from: coll_metanorm_cq
schema_version: 0.2.0
---

# QC/Biological-Sample Stratification and Discrepancy Detection

## Summary

Partition normalized metabolomics data into QC and biological sample subsets, compute distributional statistics per subset, and identify features with significant discrepancies between the two groups to flag potential normalization artifacts or sample contamination. This quality-control step ensures that QC samples remain representative when both sample types are used together during normalization.

## When to use

Apply this skill after metabolomics data normalization when both QC (quality control) and biological samples have been used in the same normalization run. Use it to detect whether QC and biological sample distributions diverge unexpectedly for individual metabolic features, which may indicate batch effects that escaped normalization, sample contamination, or QC samples that are no longer representative of the biological cohort.

## When NOT to use

- Input contains only QC samples or only biological samples (stratification requires both groups present).
- Normalization was performed using QC samples only (QConly = TRUE in Metanorm) with no biological samples included in the normalization model; in this case, discrepancy detection is less informative for validating the normalization approach.
- Data has not yet been normalized; perform normalization first, then apply this skill to assess normalization quality.

## Inputs

- Normalized metabolomics data matrix (rows = metabolic features, columns = samples; numerical)
- Sample metadata vector (indicating QC vs. biological classification for each sample)
- Batch assignment vector (optional; to stratify analysis by batch)

## Outputs

- Discrepancy report table (CSV format): feature name, discrepancy metric value, statistical significance, affected samples
- Flagged feature list (subset of features exceeding discrepancy threshold)
- Diagnostic visualizations (pre- vs. post-normalization intensity plots stratified by sample type, optional PC score plots)

## How to apply

Load the normalized metabolomics data matrix (rows = metabolic features, columns = samples) and the sample metadata vector indicating each sample's type (QC vs. biological). Partition the data into two subsets based on sample type. For each metabolic feature, compute distributional statistics (mean, variance, or robust quantiles such as median absolute deviation) within each subset. Calculate discrepancy metrics between QC and biological distributions per feature—such as fold-change in mean intensity, effect size (e.g., Cohen's d), or distance measures (e.g., Kolmogorov–Smirnov statistic). Apply a statistical threshold or cutoff to identify features with significant discrepancies relative to the overall distribution of discrepancy values across all features. Generate a report table listing flagged features, their discrepancy values, affected samples, and optionally visualizations (e.g., intensity vs. run order plots stratified by sample type) to support interpretation.

## Related tools

- **Metanorm** (R package that implements QC/biological-sample discrepancy checking via the QCcheck parameter; computes and reports discrepancies during normalization workflow) — https://github.com/UGent-LIMET/Metanorm
- **R** (Statistical computing environment used to load data, partition samples, compute distributional statistics, calculate discrepancy metrics, and generate reports and visualizations) — https://cloud.r-project.org/

## Examples

```
normdat <- metanorm(rawdata[1:5,], model = "tGAM", type = metanorm.qc, QCcheck = TRUE, batch = batch, plotdir = "~/Documents/metanormExample/")
```

## Evaluation signals

- Discrepancy report contains all features tested; no features are missing from the table or have undefined/NA values for core metrics.
- Flagged features (those exceeding the discrepancy threshold) show visible separation in pre- vs. post-normalization intensity plots when stratified by sample type, confirming that discrepancies reflect real distributional shifts.
- The distribution of discrepancy values across all features is approximately unimodal or bimodal (not pathologically skewed), supporting validity of the threshold cutoff.
- QC samples that are flagged as problematic in the discrepancy report correlate with external metadata (e.g., instrumental maintenance events, sample batch annotations) or show systematic trends in intensity drift over the run sequence.
- PC score plots before and after normalization show batch effects diminished when biological samples and QC samples are plotted separately, indicating successful normalization without introducing artificial QC–biological divergence.

## Limitations

- Discrepancy detection assumes that QC and biological sample distributions should be broadly similar after normalization; if the biological cohort contains genuine subgroups (e.g., disease vs. control), intrinsic biological differences may be misinterpreted as normalization failures.
- Threshold selection (cutoff value for flagging features) is not automated; practitioners must specify a statistical or effect-size threshold, and different thresholds may yield different conclusions about data quality.
- The skill does not correct discrepancies; it only identifies and reports them. Remediation may require re-normalization with adjusted parameters, removal of problematic samples, or investigation of instrumental/batch issues.
- Robust quantiles and distance measures are sensitive to the number of samples in each subset; very small QC or biological sample counts may yield unstable estimates.

## Evidence

- [intro] Both QC and biological samples should be used for normalization, with metanorm checking for discrepancies between them: "We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples"
- [other] Metanorm partitions data by sample type and computes distributional metrics to flag features with significant divergence: "Partition the dataset into QC sample subset and biological sample subset. 3. Compute distributional statistics (mean, variance, or robust quantiles) for each metabolic feature within each subset. 4."
- [other] Discrepancy detection output is formatted as a structured report for downstream review: "Generate a discrepancy report table listing flagged features, their discrepancy values, and affected samples, and save as CSV"
- [readme] QCcheck parameter enables discrepancy detection in Metanorm: "QCcheck = TRUE,      # check whether QCs are representative"
- [readme] Diagnostic plots support manual validation of normalization performance and discrepancy findings: "Individual compound pre- vs. post-normalization intensity vs. order plots can be retrieved from the plotdir directory. These allow finegrained assessment of normalization performance."
