---
name: retention-time-calibration-lowess-regression
description: 'Use when after mass track construction and before composite map building, when you need to align retention times across multiple LC-MS samples. Trigger conditions: (1) you have identified high-selectivity landmark peaks (mSelectivity > 0.99) in a reference sample;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - LOWESS
  - Python
  - scipy
  - scipy.signal.find_peaks
  - LOWESS (scipy implementation)
  - asari (chromatograms.rt_lowess_calibration)
  - asari (CompositeMap.calibrate_sample_RT)
  - asari (peaks.quick_detect_unique_elution_peak)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Perform a LOWESS (Locally Weighted Scatterplot Smoothing) regression to obtain a function to describe the relationship of the RT values
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-calibration-lowess-regression

## Summary

Uses LOWESS (Locally Weighted Scatterplot Smoothing) regression on high-selectivity landmark peaks to derive a retention-time mapping function between a reference sample and each current sample, enabling accurate RT alignment across LC-MS runs. This skill is essential for correcting systematic RT drift and enabling reliable feature matching in untargeted metabolomics.

## When to use

Apply this skill after mass track construction and before composite map building, when you need to align retention times across multiple LC-MS samples. Trigger conditions: (1) you have identified high-selectivity landmark peaks (mSelectivity > 0.99) in a reference sample; (2) the same mass tracks are present across current samples; (3) systematic RT drift is expected between samples (common in multi-sample LC-MS experiments); (4) you need a smooth, continuous RT transformation rather than a discrete point-to-point mapping.

## When NOT to use

- Fewer than ~5–10 high-selectivity landmark peaks are available; LOWESS requires sufficient data density to estimate local smoothing neighborhoods reliably.
- Retention time drift is non-smooth (e.g., abrupt jumps, multiple disconnected segments); LOWESS assumes local continuity and will produce artifacts across discontinuities.
- Mass tracks have not been pre-aligned across samples; this skill operates on already-matched mass tracks and cannot recover misaligned data.

## Inputs

- reference sample with identified high-selectivity landmark peaks (mSelectivity > 0.99)
- current sample mass tracks aligned to reference mass grid
- pairs of (sample_RT_scan_number, reference_RT_scan_number) from good landmark peaks

## Outputs

- rt_cal_dict: sparse scan-number mapping dictionary recording only differing RT values
- LOWESS regression function describing RT relationship between samples
- validated RT alignment with bounded extrapolation (±10% extension margins)

## How to apply

First, identify high-selectivity landmark peaks in the reference sample using stringent criteria: mSelectivity > 0.99, minimum peak height satisfied (default 1e5 for Orbitrap), peak prominence > 20% of peak height, and one peak per mass track (see constructors.set_RT_reference and peaks.quick_detect_unique_elution_peak). Second, select good landmark peaks from the current sample by applying the same selectivity filter but restricted to mass tracks already aligned to reference landmarks (CompositeMap.calibrate_sample_RT). Third, perform LOWESS regression on pairs of (sample_RT_scan_number, reference_RT_scan_number) using scipy.signal.find_peaks, adding 10% extension boundaries at both ends to constrain convergence and prevent extrapolation artifacts. Fourth, export the fitted regression function as a sparse scan-number mapping dictionary (rt_cal_dict) that records only differing values and respects sample RT boundaries. Finally, validate by confirming that landmark peak scan numbers map correctly through rt_cal_dict and that extrapolation remains bounded within ±10% extension margins.

## Related tools

- **scipy.signal.find_peaks** (Statistical peak detection on mass tracks to identify candidate landmarks before LOWESS fitting) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- **LOWESS (scipy implementation)** (Core regression method to fit smooth RT transformation function from landmark peak pairs)
- **asari (chromatograms.rt_lowess_calibration)** (Wrapper function that applies LOWESS and exports rt_cal_dict sparse mapping) — https://github.com/shuzhao-li/asari
- **asari (CompositeMap.calibrate_sample_RT)** (Orchestrates selection of good landmark peaks and invokes LOWESS calibration for each sample) — https://github.com/shuzhao-li/asari
- **asari (peaks.quick_detect_unique_elution_peak)** (Identifies high-selectivity landmark peaks in reference sample using selectivity and prominence filters) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.chromatograms import rt_lowess_calibration; rt_cal_dict = rt_lowess_calibration(sample_rt_numbers, reference_rt_numbers, sample_rt_min, sample_rt_max)
```

## Evaluation signals

- Landmark peak scan numbers from current sample map correctly through rt_cal_dict to reference RT space (visual inspection or numerical comparison within ±1–2 scan tolerance).
- rt_cal_dict contains only values that differ from identity mapping, indicating sparse representation and computational efficiency.
- Extrapolation remains bounded: all calculated RT values fall within sample RT boundaries ± 10% extension margins; no out-of-bounds predictions.
- LOWESS regression produces monotonically increasing or physically plausible RT transformation (no reversals or wild oscillations inconsistent with linear drift + local wobble).
- Post-alignment RT agreement: when identical metabolite features are detected in reference and current sample, their RT values in aligned space agree within expected instrument/column variability (typically < 0.5–2 min for LC-MS).

## Limitations

- LOWESS performance degrades if fewer than ~5–10 high-selectivity landmarks are available; datasets with sparse or absent selective peaks may require alternative alignment strategies (e.g., direct sample–sample pairing).
- Extension boundaries (±10%) are fixed; if true RT drift extends beyond this margin, convergence may be compromised or extrapolation may fail.
- The method assumes landmark peaks are truly conserved across samples; if landmarks are affected by sample-specific suppression, ion competition, or contamination, spurious mappings can result.
- Sparse rt_cal_dict representation assumes interpolation between recorded scan numbers is valid; for highly nonlinear local drifts with few landmarks, interpolation error may accumulate.

## Evidence

- [other] Identify high-selectivity landmark peaks in the reference sample using criteria: mSelectivity > 0.99, min_peak_height satisfied (default 1e5), prominence > 20% of peak height, and single peak per mass track.: "Identify high-selectivity landmark peaks in the reference sample using criteria: mSelectivity > 0.99, min_peak_height satisfied (default 1e5), prominence > 20% of peak height, and single peak per"
- [other] Select good landmark peaks from the current sample by applying the same selectivity criteria, restricted to mass tracks already aligned to the reference landmarks.: "Select good landmark peaks from the current sample by applying the same selectivity criteria, but restricted to mass tracks already aligned to the reference landmarks (see"
- [other] Perform LOWESS regression on pairs of (sample_RT_number, reference_RT_number), adding 10% extension boundaries at both ends to constrain convergence.: "Perform LOWESS regression (scipy.signal fitting) on the pairs of (sample_RT_number, reference_RT_number) from the good landmark peaks, adding 10% extension boundaries at both ends to constrain"
- [other] Export the regression function as a sparse scan-number mapping dictionary (rt_cal_dict) that records only differing values and stays within sample RT boundaries.: "Export the regression function as a sparse scan-number mapping dictionary (rt_cal_dict) that records only differing values and stays within sample RT boundaries (see"
- [other] Verify that rt_cal_dict enables accurate RT alignment by confirming landmark peak scan numbers map correctly and extrapolation remains bounded within ±10% extension margins.: "Validation: verify that rt_cal_dict enables accurate RT alignment by confirming landmark peak scan numbers map correctly and that extrapolation remains bounded within ±10% extension margins."
- [other] The retention-time alignment step performs a LOWESS regression to obtain a function describing the RT relationship between samples.: "The retention-time alignment step performs a LOWESS (Locally Weighted Scatterplot Smoothing) regression to obtain a function describing the RT relationship between samples."
