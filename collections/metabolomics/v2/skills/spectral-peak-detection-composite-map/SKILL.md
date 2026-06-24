---
name: spectral-peak-detection-composite-map
description: Use when when you have aligned mass tracks (extracted ion chromatograms)
  across multiple LC-MS samples consolidated into a composite map and need to detect
  reproducible elution peaks (features) that will be tracked back to individual samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - scipy.signal.find_peaks
  - scipy.signal.detrend
  - asari peaks.audit_mass_track
  - asari peaks.stats_detect_elution_peaks
  - asari peaks.detect_evaluate_peaks_on_roi
  - asari chromatograms.smooth_moving_average
  - asari peaks.evaluate_gaussian_peak_on_intensity_list
  techniques:
  - LC-MS
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

# spectral-peak-detection-composite-map

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Statistics-guided elution peak detection on a composite mass track using local maxima, prominence control, selective smoothing, and baseline filtering. This approach detects features across all samples simultaneously rather than repeated on individual samples, leveraging high mass resolution to improve sensitivity and reproducibility.

## When to use

When you have aligned mass tracks (extracted ion chromatograms) across multiple LC-MS samples consolidated into a composite map and need to detect reproducible elution peaks (features) that will be tracked back to individual samples. Apply this skill after mass track construction and alignment but before feature assignment and annotation.

## When NOT to use

- If individual sample mass tracks have not yet been aligned and consolidated into a composite map—apply mass track alignment first
- If the mass track has already been peak-picked and you are working at the feature level rather than the chromatographic level
- If input data are not centroid mzML format or have not been extracted as mass tracks (EICs)—use data conversion and extraction workflows first

## Inputs

- composite mass track (aligned intensity values across retention time)
- mass track metadata (max intensity, median intensity, data point count)
- parameter set (min_peak_height, min_intensity_threshold, SNR threshold, peakshape threshold, sliding window size)

## Outputs

- list of detected elution peaks (features) with apex position, prominence, SNR, peakshape, and selectivity metrics
- validated peak assignments anchored to segment boundaries
- audit trail of preprocessing decisions (rescaling applied, detrending applied, smoothing applied)

## How to apply

First, audit the composite mass track: rescale if max intensity exceeds 1E8 to normalize peak detection across studies. Classify the track as low-intensity (median < 1e3) or high-intensity, and estimate baseline and noise level from bottom signals (values below lower quartile plus min_intensity_threshold). Conditionally apply detrending (scipy.signal.detrend) if >50% of data points exceed min_intensity_threshold and median intensity >10× min_peak_height. Apply smoothing (moving average) only if noise level >1% of max intensity and max intensity <10× min_peak_height. Subtract baseline and noise filter to create regions of positive intensity, then detect peaks using scipy.signal.find_peaks with dynamic prominence (initial: 1/3 × min_peak_height; refined to max of prominence and noise level; for high-intensity segments: max of prominence and 5% max intensity) and min_peak_height and min_timepoints constraints on a sliding window (default 25 scans). Finally, evaluate detected peaks for Gaussian peakshape, selectivity, and signal-to-noise ratio (SNR); retain peaks passing thresholds (default SNR >2, peakshape >0.5).

## Related tools

- **scipy.signal.find_peaks** (Core peak detection using local maxima and prominence control on preprocessed mass track intensity values)
- **scipy.signal.detrend** (Conditional detrending of mass track to remove linear trends before peak detection on high-intensity segments)
- **asari peaks.audit_mass_track** (Audits and rescales mass track to preset ceiling (1E8) and classifies intensity level for conditional preprocessing) — https://github.com/shuzhao-li/asari
- **asari peaks.stats_detect_elution_peaks** (Orchestrates the complete statistics-guided peak detection workflow including baseline estimation and evaluation) — https://github.com/shuzhao-li/asari
- **asari peaks.detect_evaluate_peaks_on_roi** (Detects and evaluates peaks on individual regions of interest with Gaussian peakshape and SNR metrics) — https://github.com/shuzhao-li/asari
- **asari chromatograms.smooth_moving_average** (Applies selective moving average smoothing when noise exceeds 1% of max intensity) — https://github.com/shuzhao-li/asari
- **asari peaks.evaluate_gaussian_peak_on_intensity_list** (Evaluates detected peaks for Gaussian peakshape quality metric) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.peaks import stats_detect_elution_peaks; peaks_on_composite = stats_detect_elution_peaks(mass_track, min_peak_height=1e5, min_intensity_threshold=1e3, min_snr=2, min_peakshape=0.5)
```

## Evaluation signals

- Detected peak apex positions fall within segment boundaries after baseline and noise filter subtraction
- SNR and peakshape values for retained peaks are within reported thresholds (default SNR >2, peakshape >0.5)
- Prominence values are consistent with local signal characteristics and match dynamic prominence calculation (noise level or 1/3 × min_peak_height depending on segment intensity)
- Rescaling was applied if max intensity exceeded 1E8; detrending decision aligns with >50% data points above min_intensity_threshold AND median >10× min_peak_height
- Smoothing was applied only when noise level >1% of max intensity AND max intensity <10× min_peak_height; baseline/noise filter subtraction produced continuous positive-intensity segments

## Limitations

- Low-intensity tracks (median < 1e3) skip detrending and may have higher noise; peak detection sensitivity depends on accurate noise level estimation from lower quartile
- Default min_peak_height (1e5 for Orbitrap) and sliding window size (25 scans) are tuned for standard LC-MS; non-standard retention time resolution or peak widths may require parameter adjustment
- Selective smoothing (moving average) is applied only under specific noise/intensity conditions and may miss peaks in edge cases where noise is near the 1% threshold
- Peak evaluation relies on Gaussian peakshape fit quality, which may reject legitimate non-Gaussian peaks or peaks with asymmetry; selectivity metric definition is not fully specified in the workflow
- Composite map approach assumes good alignment across samples; misalignment in retention time or mass dimension will propagate as false positives or missed peaks

## Evidence

- [intro] Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing: "Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing"
- [intro] Peak detection on a composite map instead of repeated on individual samples: "Peak detection on a composite map instead of repeated on individual samples"
- [other] Asari detects elution peaks (features) on the composite map using scipy.signal.find_peaks with local maxima and prominence control, applying selective smoothing via moving average when noise exceeds 1% of max intensity, and subtracting baseline and noise filters estimated from intensity values below the lower quartile.: "Asari detects elution peaks (features) on the composite map using scipy.signal.find_peaks with local maxima and prominence control, applying selective smoothing via moving average when noise exceeds"
- [other] Classify the track as low-intensity (median < 1e3) or high-intensity and estimate baseline and noise level from bottom signals (values below lower quartile plus min_intensity_threshold).: "Classify the track as low-intensity (median < 1e3) or high-intensity and estimate baseline and noise level from bottom signals (values below lower quartile plus min_intensity_threshold)."
- [other] Apply smoothing (moving average) only if noise level >1% of max intensity and max intensity <10× min_peak_height.: "Apply smoothing (moving average) only if noise level >1% of max intensity and max intensity <10× min_peak_height."
- [other] For each segment (region of interest), detect peaks using scipy.signal.find_peaks with dynamic prominence (initial: 1/3 × min_peak_height; refined: max of prominence and noise level; for high-intensity segments: max of prominence and 5% max intensity) and min_peak_height and min_timepoints constraints on a sliding window (default 25 scans).: "For each segment (region of interest), detect peaks using scipy.signal.find_peaks with dynamic prominence (initial: 1/3 × min_peak_height; refined: max of prominence and noise level; for"
- [other] Evaluate detected peaks for Gaussian peakshape, cSelectivity, and signal-to-noise ratio (SNR); retain peaks passing thresholds (default SNR >2, peakshape >0.5).: "Evaluate detected peaks for Gaussian peakshape, cSelectivity, and signal-to-noise ratio (SNR); retain peaks passing thresholds (default SNR >2, peakshape >0.5)."
- [other] If the max intensity of a mass track is higher that a preset ceiling (1E8), the mass track is rescaled under the preset ceiling: "If the max intensity of a mass track is higher that a preset ceiling (1E8), the mass track is rescaled under the preset ceiling"
- [other] Else, if over half the data points are above min_intensity_threshold and the median intensity is higher than 10 times of preset min_peak_height (default 1e5 for Orbitrap data), detrend: "Else, if over half the data points are above min_intensity_threshold and the median intensity is higher than 10 times of preset min_peak_height (default 1e5 for Orbitrap data), detrend"
