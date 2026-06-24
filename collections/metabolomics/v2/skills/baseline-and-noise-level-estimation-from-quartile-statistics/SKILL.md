---
name: baseline-and-noise-level-estimation-from-quartile-statistics
description: Use when before peak detection on a composite or individual mass track
  when you need to filter out low-intensity noise and baseline drift without removing
  true signal.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - asari peaks.audit_mass_track
  - asari peaks.compute_noise_by_flanks
  - scipy.signal.find_peaks
  - scipy.signal.detrend
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
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

# baseline-and-noise-level-estimation-from-quartile-statistics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Estimate chromatographic baseline and noise level from the bottom intensity quartiles of a mass track to enable robust peak detection in LC-MS metabolomics. This approach isolates baseline drift and electronic noise without assuming specific distributions, making it applicable to diverse sample compositions and instrument configurations.

## When to use

Before peak detection on a composite or individual mass track when you need to filter out low-intensity noise and baseline drift without removing true signal. Essential when the track exhibits non-zero baseline, varying noise floor, or requires dynamic thresholding to distinguish peaks from background.

## When NOT to use

- Input is already a feature table or list of detected peaks (baseline estimation is a preprocessing step for raw mass tracks, not for aggregated features).
- Mass track is known to be dominated by a single, continuous analyte signal with no baseline drift (quartile-based estimation may underestimate baseline if the majority of the track is true signal rather than background).
- You require explicit parametric baseline models (e.g., polynomial, spline) rather than data-driven quartile estimates.

## Inputs

- aligned mass track (intensity array with scan-number indices synchronized across samples via rt_cal_dict)
- composite mass track (summed intensities across all samples at each m/z)
- retention-time calibration dictionary (rt_cal_dict per sample)

## Outputs

- baseline estimate (scalar intensity value derived from quartile statistics)
- noise level estimate (scalar intensity value derived from quartile statistics)
- baseline-and-noise-corrected mass track (intensity array with baseline+noise subtracted)
- signal segments (list of contiguous intensity regions above baseline+noise threshold)

## How to apply

For each mass track (intensity array), compute statistics from the bottom signal quartiles (lowest 25% of intensity values) to estimate baseline and noise independently. Use these quartile-derived estimates to subtract baseline+noise from the full track, isolating positive intensity regions as segments for subsequent peak detection. The rationale is that the lowest quartile predominantly samples baseline and electronic noise rather than analyte signal; this avoids parametric assumptions and adapts to each track's local characteristics. Apply this filtering step as part of the audit_mass_track function before scipy.signal.find_peaks is invoked, ensuring that prominence and SNR thresholds downstream operate on cleaned, background-corrected data.

## Related tools

- **asari peaks.audit_mass_track** (Implements the full audit pipeline including baseline/noise estimation via quartile statistics, detrending, smoothing, and segmentation before peak detection.) — https://github.com/shuzhao-li/asari
- **asari peaks.compute_noise_by_flanks** (Computes noise level from the flanking regions (low-intensity edges) of detected peaks, complementary to quartile-based whole-track noise estimation.) — https://github.com/shuzhao-li/asari
- **scipy.signal.find_peaks** (Peak detection algorithm applied to baseline-and-noise-corrected segments; uses prominence and height thresholds calibrated relative to the noise estimate.)
- **scipy.signal.detrend** (Applied conditionally during audit_mass_track when median intensity > 10× min_peak_height and >50% of points exceed threshold; removes low-frequency drift before baseline/noise estimation.)

## Examples

```
peaks.audit_mass_track(mass_track_intensity_array, min_peak_height=5000, min_timepoints=25) returns baseline_estimate, noise_estimate, and baseline_noise_corrected_segments
```

## Evaluation signals

- Baseline estimate falls within or below the minimum intensity values of the bottom quartile; noise estimate is strictly positive and typically 1–10% of median track intensity.
- Baseline-corrected track contains no negative values (all intensities ≥ 0 after subtraction); segments identified after baseline removal correspond visually to chromatographic peaks.
- SNR of detected peaks (computed from corrected intensities) exceeds minimum threshold (SNR > 2); chromatographic selectivity (cSelectivity) metric is computed on background-corrected signal.
- Audit flags (max intensity ceiling, rescaling, detrend application, smoothing) are recorded and logged; output segments partition the mass track without overlaps and exclude low-intensity noise regions.
- Cross-sample consistency: baseline and noise estimates for the same composite m/z across independent processing runs differ by < 5% when using identical input parameters.

## Limitations

- Quartile-based estimation assumes that the bottom 25% of intensity samples are predominantly baseline/noise; in highly abundant signals or heavily-spiked samples, true analyte signal may contaminate the quartile, biasing baseline upward.
- The method does not account for structured baseline (e.g., co-eluting contaminants at the same m/z); such interference may require additional filtering or ion-mobility/MS/MS discrimination.
- Dynamic smoothing is applied only when noise > 1% of max intensity AND max intensity < 10× min_peak_height; very noisy or very intense tracks may not receive smoothing, potentially degrading peak definition.
- Baseline subtraction can amplify residual noise in low-intensity regions; subsequent peak detection requires min_peak_height and min_timepoints thresholds to avoid false positives from corrected noise artifacts.
- Composite mass tracks constructed from samples with widely different ion suppression or matrix effects may have unequal noise contributions, leading to mixed baseline/noise profiles that quartile estimation treats uniformly.

## Evidence

- [methods] compute baseline and noise from bottom-signal quartiles: "compute baseline and noise from bottom-signal quartiles"
- [methods] Subtract baseline+noise filter to isolate positive regions, splitting track into segments.: "Subtract baseline+noise filter to isolate positive regions, splitting track into segments."
- [methods] audit each composite mass track (peaks.audit_mass_track): check max intensity ceiling (1E8), apply rescaling if needed, detect low-intensity tracks (median < 1e3), perform detrend if median > 10× min_peak_height and >50% of points exceed threshold, compute baseline and noise from bottom-signal quartiles, apply smoothing (moving average) when noise > 1% of max intensity and max intensity < 10× min_peak_height.: "audit each composite mass track (peaks.audit_mass_track): check max intensity ceiling (1E8), apply rescaling if needed, detect low-intensity tracks (median < 1e3), perform detrend if median > 10×"
- [intro] Statistics guided peak detection based on local maxima and prominence with selective use of smoothing: "Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing"
- [methods] See [peaks.compute_noise_by_flanks](peaks.compute_noise_by_flanks).: "See [peaks.compute_noise_by_flanks](peaks.compute_noise_by_flanks)."
