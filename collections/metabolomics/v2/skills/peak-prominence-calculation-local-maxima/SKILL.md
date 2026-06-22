---
name: peak-prominence-calculation-local-maxima
description: Use when when processing LC-MS mass tracks (EICs) and you need to identify genuine chromatographic peaks rather than noise artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - scipy.signal.find_peaks
  - scipy.signal.detrend
  - asari (peaks.stats_detect_elution_peaks, peaks.detect_evaluate_peaks_on_roi)
  - asari (peaks.evaluate_gaussian_peak_on_intensity_list)
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
  - build: coll_asari_cq
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari_cq
schema_version: 0.2.0
---

# Peak prominence calculation using local maxima

## Summary

Detect and quantify elution peaks on composite mass tracks by identifying local maxima and computing prominence—the vertical distance from each peak to the lowest contour line connecting it to higher peaks—with adaptive thresholds based on noise and signal intensity characteristics.

## When to use

When processing LC-MS mass tracks (EICs) and you need to identify genuine chromatographic peaks rather than noise artifacts. Trigger this skill when: (1) a composite mass track has been constructed from aligned samples, (2) the track has been baseline-subtracted and noise-filtered, and (3) you need to distinguish true elution peaks from background noise using statistical thresholds rather than fixed cutoffs.

## When NOT to use

- Mass track has not been baseline-subtracted or noise-filtered; prominence thresholds assume a noise-corrected signal.
- Input is already a feature table or annotated compound list; this skill is for initial peak detection on raw mass tracks, not post-hoc filtering.
- Mass track is from very-low-intensity samples (median < 1e3 for Orbitrap); such tracks should be flagged and handled separately or excluded.

## Inputs

- mass track intensity vector (1D array, post-baseline subtraction)
- noise level estimate (scalar, from lower quartile of intensity below min_intensity_threshold)
- max intensity value (scalar, for high-intensity threshold calculation)
- min_peak_height (scalar, default 1e5)
- min_timepoints (scalar, minimum consecutive scans for a valid peak, default 25)

## Outputs

- peak indices (array of positions in the mass track)
- peak prominence values (array of prominence scores)
- peak SNR and Gaussian peakshape metrics (floats per peak)
- binary pass/fail for each peak against quality thresholds

## How to apply

Apply scipy.signal.find_peaks on the baseline-corrected mass track intensity vector to identify local maxima, then compute prominence for each candidate peak. Adapt the prominence threshold dynamically: start with 1/3 × min_peak_height (default 1e5 for Orbitrap data), then refine to max(prominence, noise_level) for standard-intensity segments, or max(prominence, 5% × max_intensity) for high-intensity segments. Retain only peaks whose apex lies within a region of interest (positive-intensity segment after baseline/noise subtraction) and whose prominence and SNR meet minimum thresholds (default SNR > 2). This adaptive strategy avoids over-smoothing weak signals while suppressing false detections in noisy regions.

## Related tools

- **scipy.signal.find_peaks** (Core function to identify local maxima and compute prominence on baseline-corrected intensity vectors)
- **scipy.signal.detrend** (Pre-processing step applied before prominence detection on high-intensity tracks to remove low-frequency drift)
- **asari (peaks.stats_detect_elution_peaks, peaks.detect_evaluate_peaks_on_roi)** (Orchestrates adaptive prominence thresholding, region-of-interest segmentation, and peak quality evaluation) — https://github.com/shuzhao-li/asari
- **asari (peaks.evaluate_gaussian_peak_on_intensity_list)** (Post-detection validation of peakshape (Gaussian profile) and SNR for each detected peak) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.peaks import stats_detect_elution_peaks; peaks = stats_detect_elution_peaks(mass_track, min_peak_height=1e5, min_timepoints=25)
```

## Evaluation signals

- Detected peaks have apex positions strictly within segment boundaries (positive-intensity regions after baseline/noise subtraction).
- Prominence values are ≥ max(1/3 × min_peak_height, noise_level, or 5% max_intensity depending on segment type); no peak with prominence below dynamic threshold is retained.
- SNR of retained peaks exceeds minimum threshold (default > 2); computed as peak height / estimated noise level for each peak.
- Peakshape (Gaussian fit quality) of retained peaks exceeds minimum threshold (default > 0.5); indicates the peak is not spiky or multimodal noise.
- Peak spans ≥ min_timepoints consecutive scans; prevents false positives from single-scan or sub-scan artifacts.

## Limitations

- Prominence thresholds assume baseline and noise estimates are accurate; if baseline subtraction is poor or noise level is underestimated, the method may retain false positives or miss weak but valid peaks.
- Method assumes unimodal peaks; co-eluting compounds with overlapping chromatographic profiles will be detected as a single broad peak, reducing resolution.
- Performance depends on the sliding window size (default 25 scans); windows too small may miss extended peaks, while windows too large may smooth over multi-peak structures.
- High-intensity segments (max_intensity > 10 × min_peak_height) use a different prominence threshold (5% max_intensity) which may not be optimal for all instrument types or metabolite classes; requires empirical tuning per dataset.

## Evidence

- [other] Asari detects elution peaks (features) on the composite map using scipy.signal.find_peaks with local maxima and prominence control, applying selective smoothing via moving average when noise exceeds 1% of max intensity, and subtracting baseline and noise filters estimated from intensity values below the lower quartile.: "scipy.signal.find_peaks with local maxima and prominence control, applying selective smoothing via moving average when noise exceeds 1% of max intensity"
- [other] For each segment (region of interest), detect peaks using scipy.signal.find_peaks with dynamic prominence (initial: 1/3 × min_peak_height; refined: max of prominence and noise level; for high-intensity segments: max of prominence and 5% max intensity) and min_peak_height and min_timepoints constraints on a sliding window (default 25 scans).: "dynamic prominence (initial: 1/3 × min_peak_height; refined: max of prominence and noise level; for high-intensity segments: max of prominence and 5% max intensity)"
- [other] Evaluate detected peaks for Gaussian peakshape, cSelectivity, and signal-to-noise ratio (SNR); retain peaks passing thresholds (default SNR >2, peakshape >0.5).: "retain peaks passing thresholds (default SNR >2, peakshape >0.5)"
- [other] The mass track is subtracted by a filter (i.e. baseline + noise level).: "mass track is subtracted by a filter (i.e. baseline + noise level)"
- [other] Smoothing (chromatograms.smooth_moving_average) is applied when the noise level is higher than 1% of max intensity: "Smoothing (chromatograms.smooth_moving_average) is applied when the noise level is higher than 1% of max intensity"
