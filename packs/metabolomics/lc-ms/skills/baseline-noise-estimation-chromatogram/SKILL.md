---
name: baseline-noise-estimation-chromatogram
description: Use when after auditing and optionally rescaling a mass track (composite mass chromatogram) when you need to subtract background signal and set dynamic prominence thresholds for peak detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - scipy.stats.describe or numpy.percentile
  - asari.peaks.audit_mass_track
  - asari.peaks.stats_detect_elution_peaks
  techniques:
  - LC-MS
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

# baseline-noise-estimation-chromatogram

## Summary

Estimate baseline and noise level from low-intensity regions of a mass track to enable adaptive filtering and peak detection thresholding in LC-MS metabolomics. This step prepares the chromatogram for robust, data-driven peak calling by establishing intensity thresholds that adapt to the signal characteristics of individual mass tracks.

## When to use

Apply this skill after auditing and optionally rescaling a mass track (composite mass chromatogram) when you need to subtract background signal and set dynamic prominence thresholds for peak detection. Baseline and noise estimation is mandatory when the mass track median intensity is above the low-intensity threshold (default 1e3 for Orbitrap data), indicating sufficient signal complexity to justify adaptive filtering.

## When NOT to use

- If the mass track is classified as low-intensity (median < min_intensity_threshold), skip baseline and noise estimation and treat the entire track as background.
- If the mass track has already been filtered or preprocessed by an external baseline correction tool; applying this skill twice may over-subtract signal.
- If you are working with data from a targeted analysis where baseline and noise parameters are already supplied by the instrument vendor or a reference standard.

## Inputs

- mass track (1D intensity array indexed by scan/timepoint)
- min_intensity_threshold (numeric, default 1e3)
- median intensity of the track
- full set of intensity values (unsorted)

## Outputs

- baseline estimate (scalar intensity)
- noise level estimate (scalar intensity)
- baseline + noise filter (scalar)
- intensity values below lower quartile (for bottom signals)

## How to apply

Extract intensity values from the lower quartile of the mass track and combine with the min_intensity_threshold (default 1e3) to define the 'bottom signals' representing baseline and noise. For each mass track, compute the baseline as the minimum of these bottom signals and the noise level as the difference between the lower quartile and baseline. These values are then used to subtract a composite filter (baseline + noise level) from the raw intensity trace, creating segments of positive residual intensity for subsequent peak detection. The rationale is that low-intensity regions are assumed to contain predominantly baseline drift and instrument noise rather than analyte signal, allowing estimation without requiring a separate blank sample.

## Related tools

- **scipy.stats.describe or numpy.percentile** (Compute lower quartile and descriptive statistics on intensity array to identify bottom signals)
- **asari.peaks.audit_mass_track** (Precursor step that classifies track intensity and triggers baseline estimation when appropriate) — https://github.com/shuzhao-li/asari
- **asari.peaks.stats_detect_elution_peaks** (Downstream consumer of baseline and noise estimates; uses them to subtract filter and set dynamic prominence thresholds) — https://github.com/shuzhao-li/asari

## Examples

```
# After audit_mass_track classifies the track as high-intensity:
lower_quartile = np.percentile(mass_track_intensities, 25)
bottom_signals = mass_track_intensities[mass_track_intensities < (lower_quartile + min_intensity_threshold)]
baseline = np.min(bottom_signals) if len(bottom_signals) > 0 else min_intensity_threshold
noise_level = lower_quartile - baseline
filter_threshold = baseline + noise_level
filtered_track = mass_track_intensities - filter_threshold
filtered_track = np.maximum(filtered_track, 0)  # keep only positive residuals
```

## Evaluation signals

- Baseline estimate is non-negative and less than the median intensity of the mass track.
- Noise level is non-negative and typically <1–5% of the max intensity for high-quality chromatograms.
- Baseline + noise filter value is positive and subtracts at least 50% of low-intensity signals, leaving only >0 residuals in 'positive intensity segments'.
- After subtraction of the baseline + noise filter, the resulting mass track has a clear separation between background (≤0) and signal regions (>0), visible as distinct peaks above the x-axis.
- Peak detection on the filtered track yields peaks with prominence and SNR metrics consistent with the estimated noise level (default SNR >2).

## Limitations

- Assumes that bottom signals (values below lower quartile + min_intensity_threshold) are purely noise or baseline; this assumption fails if a weak but genuine analyte signal populates the lower quartile.
- The min_intensity_threshold parameter (default 1e3) is tuned for Orbitrap instruments; different MS platforms (e.g., QTOF, ion trap) may require re-tuning.
- If a mass track contains only noise or is severely degraded (e.g., detector saturation, column bleed), baseline and noise estimates may be uninformative or misleading.
- The lower quartile method does not account for non-stationary noise (e.g., time-varying baseline drift or instrument drift over long acquisition); detrending may be necessary before or after baseline estimation.

## Evidence

- [other] If a track is not low-intensity (see b), the bottom signals are taken as intensity values below the lower quartile plus min_intensity_threshold.: "If a track is not low-intensity (see b), the bottom signals are taken as intensity values below the lower quartile plus min_intensity_threshold."
- [other] Classify the track as low-intensity (median < 1e3) or high-intensity and estimate baseline and noise level from bottom signals (values below lower quartile plus min_intensity_threshold).: "Classify the track as low-intensity (median < 1e3) or high-intensity and estimate baseline and noise level from bottom signals (values below lower quartile plus min_intensity_threshold)."
- [other] The mass track is subtracted by a filter (i.e. baseline + noise level).: "The mass track is subtracted by a filter (i.e. baseline + noise level)."
- [intro] Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing: "Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing"
