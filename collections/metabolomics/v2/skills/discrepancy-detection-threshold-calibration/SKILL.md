---
name: discrepancy-detection-threshold-calibration
description: Use when normalizing metabolomics data using both QC and biological samples together.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.09.30.679445v1
  all_source_dois:
  - 10.1101/2025.09.30.679445v1
  - 10.1021/acs.analchem.5c06841
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# discrepancy-detection-threshold-calibration

## Summary

Identify and flag metabolic features with significant distributional differences between QC and biological samples during normalization by computing discrepancy metrics and applying statistical thresholds. This quality-control step ensures that QC samples remain representative of biological sample behavior and detects potential normalization failures or sample-type contamination.

## When to use

Apply this skill when normalizing metabolomics data using both QC and biological samples together. Use it to validate that QC samples behave similarly to biological samples across metabolic features, or to detect features where QC and biological distributions have diverged significantly—indicating either problematic normalization or systematic differences between sample types that warrant investigation.

## When NOT to use

- When only QC samples are used for normalization; the discrepancy check assumes both sample types are present and jointly normalized.
- When sample type information is missing, ambiguous, or not reliably assigned to each sample in metadata.
- When metabolomics data have not yet been normalized, or when raw unnormalized intensities are the only input available (discrepancy detection is most meaningful post-normalization).

## Inputs

- Normalized metabolomics data matrix (rows = metabolic features; columns = samples)
- Sample metadata vector (QC vs. biological classification)
- Batch assignment vector (optional, for stratified analysis)

## Outputs

- Discrepancy report table (CSV format): flagged features, discrepancy metrics, p-values or effect sizes, affected samples
- Diagnostic plots (per-feature intensity vs. run-order, colored by sample type)
- Summary statistics table (mean, variance, quantiles per feature per sample type)

## How to apply

Load normalized metabolomics data (rows = metabolic features, columns = samples) along with sample metadata classifying each sample as QC or biological. Partition the data into QC and biological subsets. For each metabolic feature, compute distributional statistics (mean, variance, robust quantiles) within each subset. Calculate a discrepancy metric (e.g., fold-change between subset means, effect size, or distance measure) for each feature. Apply a statistical threshold or cutoff—justified by prior validation, effect-size conventions, or pilot data—to identify features exceeding the discrepancy boundary. Generate a flagged-feature report listing the feature name, computed discrepancy value, direction of difference, and affected samples. Examine diagnostic plots to verify that flagged features represent genuine distributional divergence rather than noise or sparse features.

## Related tools

- **Metanorm** (R package that implements QC/biological-sample discrepancy checking via the QCcheck parameter; computes distributional statistics and applies thresholds to flag discrepant features) — https://github.com/UGent-LIMET/Metanorm
- **R** (Host language for Metanorm; used to load data, partition samples, compute statistics, apply thresholds, and generate reports)

## Examples

```
normdat <- metanorm(rawdata[1:5,], model = "tGAM", type = metanorm.qc, QCcheck = TRUE, batch = batch, plotdir = "~/Documents/metanormExample/")
```

## Evaluation signals

- Discrepancy report contains no negative or missing values in the fold-change or effect-size column; threshold is monotonically applied (all flagged features exceed the cutoff).
- Diagnostic plots show visual separation (in intensity distributions, boxplots, or quantile-quantile plots) between QC and biological subsets for flagged features; non-flagged features show overlapping distributions.
- The flagged feature count and discrepancy distribution are consistent with expected rates in independent validation or pilot data (e.g., 5–15% of features flagged at p < 0.05).
- Samples listed as 'affected' in the report correspond to the subset (QC or biological) with the larger discrepancy value; no sample mislabeling.
- Applying a more stringent threshold reduces the flagged-feature count monotonically; applying a more lenient threshold increases it, confirming threshold calibration is functioning.

## Limitations

- Discrepancy detection assumes sufficiently large and balanced numbers of QC and biological samples; small QC cohorts or highly imbalanced designs may produce unstable distributional estimates.
- The choice of discrepancy metric (fold-change, effect size, distance measure) and threshold value is not fully automated; guidance from prior validation data or pilot runs is recommended to avoid over- or under-flagging.
- Features with very low abundance or high variance within sample types may generate spurious discrepancy signals; filtering by abundance or robustness thresholds before discrepancy computation is advisable.
- The README notes 'use cases differ and unforeseen circumstances may cause unexpected behaviour'; results should be inspected visually via diagnostic plots to identify anomalies (e.g., artifacts from extreme outliers).

## Evidence

- [other] Metanorm implements a mechanism to check for discrepancies between QC and biological samples when both sample types are used together for normalization.: "Metanorm implements a mechanism to check for discrepancies between QC and biological samples when both sample types are used together for normalization"
- [other] The workflow computes distributional statistics per feature within each sample-type subset, calculates discrepancy metrics (fold-change, effect size, distance measure), applies statistical thresholds, and generates a report.: "Compute distributional statistics (mean, variance, or robust quantiles) for each metabolic feature within each subset. 4. Calculate discrepancy metrics (e.g., fold-change, effect size, or distance"
- [intro] Both QC and biological samples should be used for normalization, with metanorm checking for discrepancies between them.: "We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples"
- [readme] The QCcheck parameter in Metanorm enables discrepancy detection during normalization.: "QCcheck = TRUE,      # check whether QCs are representative"
- [readme] Diagnostic plots allow fine-grained assessment of whether sample types behave differently.: "Individual compound pre- vs. post-normalization intensity vs. order plots can be retrieved from the *plotdir* directory. These allow finegrained assessment of normalization performance"
