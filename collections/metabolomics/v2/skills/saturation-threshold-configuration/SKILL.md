---
name: saturation-threshold-configuration
description: Use when when executing peak integration on preprocessed GC-IMS data (after alignment and baseline correction) and you need to decide whether to include or exclude peaks that exhibit saturation artifacts from the RIP signal. Set a threshold (e.g., 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GCIMS
derived_from:
- doi: 10.1016/j.chemolab.2023.104938
  title: GCIMS
evidence_spans:
- library(ggplot2) library(cowplot) library(GCIMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcims_cq
    doi: 10.1016/j.chemolab.2023.104938
    title: GCIMS
  dedup_kept_from: coll_gcims_cq
schema_version: 0.2.0
---

# saturation-threshold-configuration

## Summary

Configure the RIP (Reactant Ion Peak) saturation threshold parameter during peak integration in GC-IMS preprocessing to control which saturated peaks are retained or excluded from the peak table. This parameter directly affects the quality and completeness of the final intensity matrix used in downstream analysis.

## When to use

When executing peak integration on preprocessed GC-IMS data (after alignment and baseline correction) and you need to decide whether to include or exclude peaks that exhibit saturation artifacts from the RIP signal. Set a threshold (e.g., 0.1) when you want to exclude peaks with RIP saturation above that proportion, balancing signal recovery against artifact contamination in your peak intensity matrix.

## When NOT to use

- If your goal is to retain all detected peaks regardless of saturation quality (use rip_saturation_threshold = 1.0 or omit the parameter entirely)
- If peaks are already integrated using a different method (e.g., adaptive integration) and you are only extracting the table, not re-integrating
- If you have not yet performed alignment and baseline correction on the dataset

## Inputs

- preprocessed GC-IMS dataset object (after alignment and baseline correction)
- peak detection results (from detectPeaks or clusterPeaks)
- integration method specification (e.g., 'fixed_size')

## Outputs

- integrated peak set with RIP saturation filtering applied
- peak_table_matrix with rows representing clusters and columns representing samples, containing intensity values with some entries as NA

## How to apply

Call the integratePeaks function with the rip_saturation_threshold parameter set to your chosen cutoff value (e.g., 0.1 for 10% saturation tolerance). This threshold controls the fraction of RIP signal saturation that peaks can tolerate before being excluded during integration. Peaks exceeding this saturation fraction will be filtered out, reducing noise but potentially losing weak signal. After integration, execute peakTable to extract the resulting peak intensity matrix; inspect the number of NA entries and the ratio of retained peaks to original detections to confirm the threshold was appropriate for your data quality requirements.

## Related tools

- **GCIMS** (R package providing integratePeaks and peakTable functions for GC-IMS preprocessing) — https://github.com/sipss/GCIMS
- **R** (runtime environment for executing GCIMS workflow functions)

## Examples

```
integrated_result <- integratePeaks(peak_clusters, integration_size_method = 'fixed_size', rip_saturation_threshold = 0.1); peak_table_matrix <- peakTable(integrated_result)
```

## Evaluation signals

- Verify that the returned peak_table_matrix has dimensions consistent with your sample count (columns) and detected peak clusters (rows)
- Check that the number of NA entries in the matrix is reasonable for your RIP threshold choice; higher thresholds should yield fewer NAs
- Compare the count of retained peaks against the original peak detection output to confirm saturation filtering was applied
- Examine a sample of intensity values to confirm they are numeric and fall within the expected dynamic range for your GC-IMS instrument
- Confirm that downstream imputation and statistical analysis steps run without error on the returned matrix

## Limitations

- The rip_saturation_threshold parameter is global across all samples; if RIP saturation varies strongly between samples, a single threshold may over-filter some samples or under-filter others
- Peaks excluded due to saturation cannot be recovered; no metadata is retained about which peaks were filtered, complicating post-hoc sensitivity analysis
- The NA entries in the resulting peak_table_matrix require imputation in downstream steps; the choice of imputation method can influence downstream statistical conclusions

## Evidence

- [other] integration_size_method and rip_saturation_threshold parameters control peak integration: "Execute integratePeaks function with integration_size_method set to 'fixed_size' and rip_saturation_threshold parameter set to 0.1"
- [other] peakTable produces matrix with rows as clusters, columns as samples, containing intensities and NAs: "The peakTable function produces a peak_table_matrix with rows representing clusters and columns representing samples, containing intensity values with some entries as NA that require imputation."
- [intro] Pressure and temperature fluctuations cause misalignments that require correction before peak integration: "Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time"
- [other] GCIMS workflow requires baseline correction before peak integration: "Load the preprocessed GC-IMS dataset (after alignment and baseline correction) into R using the GCIMS package."
