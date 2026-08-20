---
name: inter-sample-variance-calculation
description: Use when after applying batch correction (e.g., via pycombat) to a multi-batch
  feature table, to validate whether the correction has reduced systematic intensity
  differences between batches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - ThermoRawFileParser
  - pycombat
  - Python
  - PCPFM
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- Batch correction is performed using pycombat.
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# inter-sample-variance-calculation

## Summary

Calculate median inter-batch variance for high-intensity features across sample groups to quantify the magnitude of batch effects in multi-batch metabolomics feature tables before and after correction.

## When to use

After applying batch correction (e.g., via pycombat) to a multi-batch feature table, to validate whether the correction has reduced systematic intensity differences between batches. This is necessary when you have feature tables with samples collected in multiple batches and need to confirm that batch-effect attenuation has been achieved while preserving sample and feature dimensions.

## When NOT to use

- Input feature table has already been evaluated for batch effects and correction is not planned or not applicable (single-batch study).
- Feature table has undergone filtering that removed most high-intensity features, leaving insufficient statistical power to estimate inter-batch variance.
- Batch labels are missing or inconsistent in the sample metadata, preventing reliable grouping of samples by batch.

## Inputs

- Interpolated (post-imputation) feature table with m/z-retention time features as rows and samples as columns
- Sample metadata CSV/TSV with sample identifiers and batch labels
- Uncorrected feature table intensity matrix (optional, for comparison baseline)

## Outputs

- Median inter-batch variance for high-intensity features (uncorrected)
- Median inter-batch variance for high-intensity features (batch-corrected)
- Variance reduction summary (e.g., percentage decrease or fold-change)
- Optionally: per-batch variance profiles for visualization

## How to apply

Load the feature table (both uncorrected and batch-corrected versions) along with sample metadata containing batch labels. Subset the feature table to high-intensity features (those with median or mean intensity above a defined threshold) to focus on signals robust enough to assess batch variance. Group samples by the batch field in the metadata. For each batch-grouped cohort, calculate the variance (or standard deviation) of intensities for each selected feature across samples within that batch. Aggregate these batch-specific variances to a single metric (e.g., median or mean of per-feature variances across all batches). Compare this summary statistic between the uncorrected and corrected tables; successful batch correction should show lower inter-batch variance in the corrected output. Document the threshold used to select high-intensity features and the variance aggregation method for reproducibility.

## Related tools

- **pycombat** (Performs ComBat-based batch correction on the feature table; inter-sample variance calculation is used to validate the output)
- **Python** (Language for implementing variance calculations, grouping samples by batch, and aggregating statistics)
- **PCPFM** (Pipeline that integrates batch correction and quality-control steps; this skill fits within the data normalization and batch correction workflow) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics

## Evaluation signals

- Corrected table median inter-batch variance is lower than uncorrected table median inter-batch variance, demonstrating successful batch effect attenuation.
- The subset of high-intensity features used for variance calculation is stable and reproducible across independent runs (same feature selection threshold and grouping logic).
- Feature count and sample count in the corrected table are identical to the uncorrected table, confirming no rows or columns were dropped during batch correction.
- Variance reduction is consistent across multiple high-intensity features (e.g., >70% of features show reduced inter-batch variance post-correction), not driven by outliers.
- The batch field values in metadata perfectly match the sample identifiers in the feature table, with no missing or ambiguous batch assignments.

## Limitations

- Requires clear, non-ambiguous batch labels in the sample metadata; missing or inconsistent batch assignments will produce incorrect variance estimates.
- Selection of high-intensity feature subset is threshold-dependent; different intensity thresholds may yield different conclusions about batch-correction efficacy.
- Inter-batch variance reduction does not guarantee preservation of biological signal; it is a necessary but not sufficient condition for valid batch correction.
- Variance calculation assumes that batch effects manifest primarily as intensity shifts rather than feature detection differences; differential feature availability across batches is not captured by this metric.

## Evidence

- [other] Calculate median inter-batch variance for a subset of high-intensity features in both uncorrected and corrected tables using sample grouping by the batch field.: "Calculate median inter-batch variance for a subset of high-intensity features in both uncorrected and corrected tables using sample grouping by the batch field."
- [other] Confirm that corrected table median inter-batch variance is lower than uncorrected median inter-batch variance, demonstrating successful batch effect attenuation.: "Confirm that corrected table median inter-batch variance is lower than uncorrected median inter-batch variance, demonstrating successful batch effect attenuation."
- [other] Verify that the output table has identical dimensions (sample count and feature count) to the input table.: "Verify that the output table has identical dimensions (sample count and feature count) to the input table."
- [readme] data normalization and batch correction: "data normalization and batch correction"
