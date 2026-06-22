---
name: chromatographic-peak-detection-with-prominence-control
description: Use when after constructing baseline-corrected mass tracks (either composite across samples or per-sample) when you need to identify individual chromatographic peaks for feature extraction in LC-MS or GC-MS metabolomics workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - scipy.signal.find_peaks
  - scipy.signal.detrend
  - asari (peaks.audit_mass_track)
  - asari (peaks.stats_detect_elution_peaks)
  - asari (peaks.evaluate_gaussian_peak_on_intensity_list)
  - asari (peaks.__peaks_cSelectivity_stats_)
  - asari (peaks.compute_noise_by_flanks)
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari
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

# chromatographic-peak-detection-with-prominence-control

## Summary

Detect chromatographic peaks in mass-spectrometry intensity arrays using local maxima and dynamic prominence thresholds, applied to composite or individual mass tracks after baseline/noise removal and optional smoothing. This approach prioritizes signal selectivity and reduces false positives by tuning prominence relative to noise level and peak height.

## When to use

Apply this skill after constructing baseline-corrected mass tracks (either composite across samples or per-sample) when you need to identify individual chromatographic peaks for feature extraction in LC-MS or GC-MS metabolomics workflows. Use it specifically when you have intensity arrays with known noise characteristics and want to avoid over-detection of shallow peaks or under-detection due to fixed, global prominence thresholds.

## When NOT to use

- Input mass track has already been peak-detected and feature-summarized—do not re-apply peak detection to a feature table or aggregated peak list.
- Mass track exhibits extreme baseline drift or multiplicative noise that cannot be adequately corrected by the audit step (detrend, baseline subtraction); consider preprocessing first.
- You require detection of peaks in noisy, low-resolution data where Gaussian fitting is unreliable; this skill assumes sufficient chromatographic resolution to justify prominence-based filtering.

## Inputs

- aligned mass track (intensity array, full retention-time length, single m/z value)
- retention-time calibration dictionaries (rt_cal_dict per sample, if per-sample tracks)
- parameters: min_peak_height (integer, default ~5000–10000 counts), min_timepoints (integer, default 25 scans), noise_threshold_ppm (float, default 0.01 or 1%)

## Outputs

- detected peaks (list of dicts with scan indices, intensity, m/z, retention time, Gaussian fit metrics)
- peak quality metrics: cSelectivity (float, chromatographic selectivity), SNR (float, signal-to-noise ratio), goodness_fitting (float, Gaussian R²)
- filtered peak list (subset meeting SNR > 2 and Gaussian fit thresholds)

## How to apply

Begin by auditing each mass track: check intensity ceiling (cap at 1E8), detect low-intensity tracks (median < 1e3), and apply detrend if median > 10× min_peak_height or >50% of points exceed the height threshold. Compute baseline and noise from bottom-signal quartiles; apply moving-average smoothing if noise > 1% of max intensity AND max intensity < 10× min_peak_height. Subtract baseline+noise to isolate positive regions and split the track into segments. For each segment, invoke scipy.signal.find_peaks with a dynamic prominence parameter set to the maximum of: (1) 1/3 × min_peak_height, (2) noise level, and (3) 5% of segment max intensity. Use min_peak_height and min_timepoints (default 25 scans) as additional window controls. Finally, filter detected peaks by requiring goodness-of-fit to a Gaussian model, chromatographic selectivity (cSelectivity), and SNR > 2.

## Related tools

- **scipy.signal.find_peaks** (core local-maxima detection engine; invoked once per mass track segment with dynamic prominence parameter) — https://scipy.org
- **scipy.signal.detrend** (removes polynomial or mean baseline drift from mass track before peak detection) — https://scipy.org
- **asari (peaks.audit_mass_track)** (validates and conditions mass track intensity ceiling, rescaling, smoothing, baseline/noise computation before peak detection) — https://github.com/shuzhao-li/asari
- **asari (peaks.stats_detect_elution_peaks)** (orchestrates the full peak-detection workflow including find_peaks invocation with prominence and height controls) — https://github.com/shuzhao-li/asari
- **asari (peaks.evaluate_gaussian_peak_on_intensity_list)** (fits Gaussian model to detected peak and computes goodness_fitting metric for quality filtering) — https://github.com/shuzhao-li/asari
- **asari (peaks.__peaks_cSelectivity_stats_)** (computes chromatographic selectivity (cSelectivity) metric to filter peaks for specificity) — https://github.com/shuzhao-li/asari
- **asari (peaks.compute_noise_by_flanks)** (estimates noise level from signal flanks for use in dynamic prominence calculation) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.peaks import stats_detect_elution_peaks; detected = stats_detect_elution_peaks(mass_track, min_peak_height=5000, min_timepoints=25, noise=150.0)
```

## Evaluation signals

- Verify that scipy.signal.find_peaks is invoked exactly once per composite mass track (or once per segment within a per-sample track), not N times—log or count function calls.
- Confirm that all reported peaks include three required metrics: cSelectivity (float), SNR (float ≥ 2), and Gaussian goodness_fitting (R² or equivalent)—audit output JSON/CSV schema.
- Cross-check that peaks with SNR ≤ 2 or failing Gaussian fit are excluded from the final peak list—compare against full candidate peak set before filtering.
- Validate that dynamic prominence was computed for each segment as max(1/3 × min_peak_height, noise level, 5% × segment max intensity)—spot-check a few segments in logs or intermediate outputs.
- Confirm that baseline and noise estimates are derived from bottom-signal quartiles and that detrend/smoothing was applied only when audit conditions are met (median, thresholds)—trace audit_mass_track output.

## Limitations

- Gaussian fitting assumes peaks are approximately bell-shaped; highly asymmetric or multi-modal peaks may not fit well and will be incorrectly filtered.
- Dynamic prominence depends on accurate noise estimation from flanks; in extremely noisy or low-intensity tracks (median < 1e3), noise computation may be unreliable and prominence thresholds may be too high or too low.
- The default min_timepoints = 25 scans assumes typical chromatographic resolution; for very fast gradients or high-frequency sampling, this threshold may prune valid narrow peaks.
- Detrending and smoothing are conditional on audit thresholds; if a mass track exhibits complex baseline drift not captured by the median or 10× min_peak_height rule, these corrections may be skipped, leaving residual artifacts.
- SNR computation and cSelectivity depend on sample registration and cross-sample alignment quality; misaligned or poorly calibrated retention-time dictionaries will degrade selectivity filtering.

## Evidence

- [methods] Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control: "Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control"
- [other] Apply scipy.signal.find_peaks on each segment with dynamic prominence (max of 1/3 min_peak_height, noise level, and 5% of segment max intensity): "Apply scipy.signal.find_peaks on each segment with dynamic prominence (max of 1/3 min_peak_height, noise level, and 5% of segment max intensity), using min_peak_height and min_timepoints (default 25"
- [other] Audit each composite mass track (peaks.audit_mass_track): check max intensity ceiling (1E8), apply rescaling if needed, detect low-intensity tracks (median < 1e3), perform detrend if median > 10× min_peak_height and >50% of points exceed threshold: "Audit each composite mass track (peaks.audit_mass_track): check max intensity ceiling (1E8), apply rescaling if needed, detect low-intensity tracks (median < 1e3), perform detrend if median > 10×"
- [other] Evaluate detected peaks for gaussian fit (goodness_fitting), chromatographic selectivity (cSelectivity), and signal-to-noise ratio (SNR > 2), retaining only peaks meeting thresholds.: "Evaluate detected peaks for gaussian fit (goodness_fitting), chromatographic selectivity (cSelectivity), and signal-to-noise ratio (SNR > 2), retaining only peaks meeting thresholds."
- [intro] Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing: "Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing"
