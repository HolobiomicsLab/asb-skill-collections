---
name: composite-mass-track-construction
description: Use when when processing a multi-sample LC-MS metabolomics project after mass-track extraction and retention-time calibration have been applied to all individual samples, and you need to detect peaks across the entire cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3643
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - scipy.signal.find_peaks
  - scipy.signal.detrend
  - asari peaks.audit_mass_track
  - asari chromatograms.rt_lowess_calibration
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

# composite-mass-track-construction

## Summary

Construct a single composite mass track by element-wise summation of intensity values across aligned mass tracks from all samples at each m/z value, enabling efficient single-pass peak detection instead of per-sample detection. This reduces computational cost from O(N) to O(1) peak-detection algorithm invocations while preserving signal fidelity across the cohort.

## When to use

When processing a multi-sample LC-MS metabolomics project after mass-track extraction and retention-time calibration have been applied to all individual samples, and you need to detect peaks across the entire cohort. This approach is especially valuable when N > 10 samples, as it avoids redundant peak-detection invocations and enables detection of low-abundance features visible only when signal is pooled across samples.

## When NOT to use

- When input samples have drastically different ionization efficiency or sample loads (pooling may obscure sample-specific rare peaks or introduce bias toward dominant samples).
- When retentiontime miscalibration across samples is severe (misaligned scans will blur the composite track and lower peak definition).
- When peak detection must preserve sample-level spatial information or variance (composite pooling loses per-sample intensity and signal heterogeneity).

## Inputs

- aligned mass tracks from all samples (one mass track per m/z per sample)
- retention-time calibration dictionaries (rt_cal_dict) mapping sample scan numbers to reference coordinates
- reference sample scan-number range (defines synchronized coordinate system)
- min_peak_height threshold (default tunable, used for dynamic prominence calculation)
- min_timepoints for peak width control (default 25 scans)

## Outputs

- composite mass track (intensity array of full retention-time length, summed across all N samples)
- detected peaks on composite track with metrics: m/z, retention time, intensity, prominence, gaussian fit goodness (goodness_fitting), chromatographic selectivity (cSelectivity), signal-to-noise ratio (SNR)
- audit report on composite track (max intensity value, rescaling applied, detrending applied, baseline and noise estimates)

## How to apply

After extracting aligned mass tracks from each sample and obtaining retention-time calibration dictionaries (rt_cal_dict), synchronize scan-number indices across all samples by applying rt_cal_dict to map each sample's scan numbers to a reference sample coordinate system. For each unique m/z value in the aligned mass grid, sum the intensity arrays element-wise across all samples to produce a single composite mass track of full retention-time length. Audit the composite track using peaks.audit_mass_track (check intensity ceiling at 1E8, apply rescaling if needed, detect low-intensity tracks with median < 1e3, detrend if median > 10× min_peak_height and >50% of points exceed threshold, compute baseline and noise from bottom-signal quartiles, apply moving-average smoothing when noise > 1% of max intensity and max intensity < 10× min_peak_height). Subtract the baseline and noise filter to isolate positive regions, splitting the track into segments. Then apply scipy.signal.find_peaks to each segment once, using dynamic prominence (max of 1/3 min_peak_height, noise level, and 5% of segment max intensity) and min_timepoints (default 25 scans) for window control, rather than calling find_peaks N times on individual samples.

## Related tools

- **scipy.signal.find_peaks** (Applied once per composite track segment to detect local maxima with prominence control, replacing N per-sample invocations) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- **scipy.signal.detrend** (Applied conditionally during composite mass-track audit to remove low-frequency drift when median intensity > 10× min_peak_height and >50% of points exceed threshold) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.detrend.html
- **asari peaks.audit_mass_track** (Inspects composite track intensity range, applies rescaling, detects low-signal regions, computes baseline and noise estimates, and applies smoothing per configured thresholds before peak detection) — https://github.com/shuzhao-li-lab/asari
- **asari chromatograms.rt_lowess_calibration** (Generates retention-time calibration dictionaries used to synchronize scan indices across samples prior to composite track construction) — https://github.com/shuzhao-li-lab/asari

## Evaluation signals

- Verify that scipy.signal.find_peaks is invoked exactly once per composite track (or once per segment within a composite track), not N times, by instrumenting or logging the call stack.
- Confirm that the composite track intensity array has length equal to the full reference retention-time span (number of scans in reference sample) and contains element-wise sums of all aligned input tracks.
- Check that detected peaks include all four required metrics: goodness_fitting (gaussian fit), cSelectivity (chromatographic selectivity), SNR > 2 (signal-to-noise ratio), and min_peak_height threshold met.
- Validate that reported peak retention times fall within the range of scans present in all or nearly all input samples (indicating genuine pooled signal, not noise from misaligned outliers).
- Audit log should show that audit_mass_track executed once per composite track with reported baseline, noise, and detrending decisions.

## Limitations

- Composite pooling assumes that retention time is sufficiently synchronized across samples via rt_cal_dict; large inter-sample drift will blur peaks and reduce sensitivity.
- Pooling assumes similar sample loading and ionization efficiency across the cohort; highly unbalanced samples may dominate the composite signal and obscure low-abundance metabolites in weaker samples.
- The single composite peak list does not preserve per-sample signal heterogeneity; downstream abundance tables must be extracted by mapping detected peaks back to individual sample mass tracks via mass-to-feature association, which requires the original sample-level data.
- Very low-abundance metabolites visible in only 1–2 samples may be diluted below detection threshold in the composite track if other samples have zero signal; per-sample detection may recover these features, trading computational cost for sensitivity.
- Baseline and noise estimation are computed once from the composite pooled signal; samples with anomalous noise or drift may skew these estimates and lead to suboptimal thresholds for the composite detection step.

## Evidence

- [other] Asari implements peak detection using scipy.signal.find_peaks on a composite map constructed from summed mass tracks across all samples, reducing the number of peak-detection algorithm calls from N (one per sample) to one (composite), thereby improving scalability and computational efficiency.: "Asari implements peak detection using scipy.signal.find_peaks on a composite map constructed from summed mass tracks across all samples, reducing the number of peak-detection algorithm calls from N"
- [other] Sum intensity values element-wise across all samples for each unique m/z value in the mass grid, producing composite mass tracks as full-length intensity arrays.: "Sum intensity values element-wise across all samples for each unique m/z value in the mass grid, producing composite mass tracks as full-length intensity arrays."
- [other] Synchronize scan-number indices across samples by applying rt_cal_dict to map each sample's scan numbers to reference sample coordinates.: "Synchronize scan-number indices across samples by applying rt_cal_dict to map each sample's scan numbers to reference sample coordinates."
- [other] Audit each composite mass track (peaks.audit_mass_track): check max intensity ceiling (1E8), apply rescaling if needed, detect low-intensity tracks (median < 1e3), perform detrend if median > 10× min_peak_height and >50% of points exceed threshold, compute baseline and noise from bottom-signal quartiles, apply smoothing (moving average) when noise > 1% of max intensity and max intensity < 10× min_peak_height.: "Audit each composite mass track (peaks.audit_mass_track): check max intensity ceiling (1E8), apply rescaling if needed, detect low-intensity tracks (median < 1e3), perform detrend if median > 10×"
- [readme] Peak detection on a composite map instead of repeated on individual samples: "Peak detection on a composite map instead of repeated on individual samples"
