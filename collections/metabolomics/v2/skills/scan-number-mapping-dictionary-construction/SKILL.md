---
name: scan-number-mapping-dictionary-construction
description: Use when after performing LOWESS regression on landmark peak RT pairs between a sample and reference, you need to encode the learned RT transformation as a reusable, memory-efficient lookup table that can be applied during feature alignment without recomputing the regression for every sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - scipy
  - scipy.signal.lowess
  - asari (chromatograms.rt_lowess_calibration)
  - asari (constructors.set_RT_reference, peaks.quick_detect_unique_elution_peak)
  - asari (CompositeMap.calibrate_sample_RT)
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- scipy.signal module for LOWESS fitting via the regression function
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari_cq
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Construct scan-number mapping dictionary from LOWESS retention-time alignment

## Summary

Export a LOWESS regression function describing retention-time (RT) relationships between a sample and reference into a sparse scan-number mapping dictionary (rt_cal_dict) that records only differing values and constrains extrapolation within sample RT boundaries. This enables efficient, reproducible RT alignment across LC-MS samples.

## When to use

After performing LOWESS regression on landmark peak RT pairs between a sample and reference, you need to encode the learned RT transformation as a reusable, memory-efficient lookup table that can be applied during feature alignment without recomputing the regression for every sample.

## When NOT to use

- Sample has fewer than ~5–10 high-quality landmark peaks; insufficient data points make LOWESS fitting unreliable.
- RT shift is non-monotonic or exhibits discontinuities; LOWESS may produce invalid mappings that reverse or collapse scan order.
- RT alignment is already complete or sample is already calibrated; constructing a second mapping dictionary would introduce redundant or conflicting transformations.

## Inputs

- LOWESS regression function (scipy.signal.lowess output)
- List of landmark peak (sample_RT_number, reference_RT_number) pairs
- Sample RT range (min and max scan number)
- Reference RT range (for boundary extension calculation)

## Outputs

- Sparse scan-number mapping dictionary (rt_cal_dict) as JSON or Python dict
- Validation report confirming landmark peak scan number mappings and boundary adherence

## How to apply

Given a LOWESS regression function fitted on pairs of (sample_RT_number, reference_RT_number) from high-selectivity landmark peaks (selectivity > 0.99, prominence > 20% of peak height), export the function as a sparse dictionary (rt_cal_dict) that stores only scan numbers where the calibrated RT differs from the uncalibrated scan number. Add 10% extension boundaries at both ends of the RT range to constrain convergence and prevent out-of-bounds extrapolation. Validate the mapping by confirming that landmark peak scan numbers map correctly and that all extrapolated values remain within ±10% extension margins of the sample's original RT boundaries. The resulting rt_cal_dict should stay within sample RT boundaries and be compact enough for efficient storage and lookups during composite map construction.

## Related tools

- **scipy.signal.lowess** (Performs LOWESS regression on landmark peak RT pairs to estimate the smooth, non-parametric RT transformation function) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lowess.html
- **asari (chromatograms.rt_lowess_calibration)** (Core function that exports the LOWESS regression function as a sparse rt_cal_dict and enforces boundary constraints) — https://github.com/shuzhao-li/asari
- **asari (constructors.set_RT_reference, peaks.quick_detect_unique_elution_peak)** (Identifies high-selectivity landmark peaks in reference sample used to seed LOWESS regression) — https://github.com/shuzhao-li/asari
- **asari (CompositeMap.calibrate_sample_RT)** (Selects good landmark peaks from current sample by applying selectivity criteria and mass track alignment constraints) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.chromatograms import rt_lowess_calibration; rt_cal_dict = rt_lowess_calibration(sample_rts, reference_rts, sample_rt_min, sample_rt_max, extension_pct=0.1)
```

## Evaluation signals

- rt_cal_dict contains only scan numbers where calibrated RT differs from uncalibrated scan number; sparsity should be 50–80% of original scan range.
- All keys and values in rt_cal_dict remain within [sample_RT_min - 10%, sample_RT_max + 10%] bounds; no extrapolation beyond boundaries.
- Landmark peak scan numbers from the LOWESS fit map bidirectionally: applying rt_cal_dict to sample peak scans recovers the corresponding reference peak scans with ≤ 1 scan difference.
- rt_cal_dict can be serialized to JSON and deserialized without loss of precision; round-trip test confirms integer scan numbers.
- Independent validation on a held-out subset of landmark peaks (not used in LOWESS fit) shows RT alignment error < 2 scan numbers.

## Limitations

- LOWESS fit quality depends on the number and distribution of landmark peaks; sparse or clustered peaks may produce discontinuous or overly smoothed mappings.
- 10% extension boundary is a heuristic; extreme RT shifts or non-linear instrumental drift may require dataset-specific tuning.
- rt_cal_dict assumes monotonic RT relationship between sample and reference; non-linear or multi-modal RT transformations are not supported and will cause scan reversals.
- Sparse encoding loses information about the underlying LOWESS regression; if fine-grained RT interpolation is needed later, the original regression function must be preserved separately.

## Evidence

- [other] Perform LOWESS regression (scipy.signal fitting) on the pairs of (sample_RT_number, reference_RT_number) from the good landmark peaks, adding 10% extension boundaries at both ends to constrain convergence.: "Perform LOWESS regression (scipy.signal fitting) on the pairs of (sample_RT_number, reference_RT_number) from the good landmark peaks, adding 10% extension boundaries at both ends to constrain"
- [other] Export the regression function as a sparse scan-number mapping dictionary (rt_cal_dict) that records only differing values and stays within sample RT boundaries: "Export the regression function as a sparse scan-number mapping dictionary (rt_cal_dict) that records only differing values and stays within sample RT boundaries"
- [other] verify that rt_cal_dict enables accurate RT alignment by confirming landmark peak scan numbers map correctly and that extrapolation remains bounded within ±10% extension margins.: "verify that rt_cal_dict enables accurate RT alignment by confirming landmark peak scan numbers map correctly and that extrapolation remains bounded within ±10% extension margins."
- [other] Identify high-selectivity landmark peaks in the reference sample using criteria: mSelectivity > 0.99, min_peak_height satisfied (default 1e5), prominence > 20% of peak height, and single peak per mass track: "Identify high-selectivity landmark peaks in the reference sample using criteria: mSelectivity > 0.99, min_peak_height satisfied (default 1e5), prominence > 20% of peak height, and single peak per"
