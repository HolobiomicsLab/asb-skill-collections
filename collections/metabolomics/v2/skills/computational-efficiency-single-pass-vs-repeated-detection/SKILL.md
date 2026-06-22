---
name: computational-efficiency-single-pass-vs-repeated-detection
description: 'Use when when processing aligned LC-MS data across multiple samples where the computational bottleneck is repeated peak-detection algorithm calls (one per sample per m/z value). Typical scenario: >10 samples with >1000 m/z values each, where N individual find_peaks invocations dominate runtime.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3391
  tools:
  - Python
  - scipy.signal.find_peaks
  - scipy.signal.detrend
  - asari.peaks.audit_mass_track
  - asari.peaks.stats_detect_elution_peaks
  - asari.peaks.evaluate_gaussian_peak_on_intensity_list
  - asari.peaks.__peaks_cSelectivity_stats__
  - asari.chromatograms.rt_lowess_calibration
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# computational-efficiency-single-pass-vs-repeated-detection

## Summary

Replace per-sample peak detection with single-pass detection on a composite mass track (summed intensities across all samples) to reduce scipy.signal.find_peaks invocations from N to 1, dramatically improving computational scalability in untargeted LC-MS metabolomics without sacrificing peak quality metrics.

## When to use

When processing aligned LC-MS data across multiple samples where the computational bottleneck is repeated peak-detection algorithm calls (one per sample per m/z value). Typical scenario: >10 samples with >1000 m/z values each, where N individual find_peaks invocations dominate runtime. Particularly valuable when samples are aligned to a common retention-time reference via rt_cal_dict calibration dictionaries and when composite signal is strong enough to enable robust peak detection (median intensity >1e3).

## When NOT to use

- Input is already a per-sample feature table or pre-aggregated peak list; skip composite construction.
- Samples are poorly aligned or rt_cal_dict calibration fails; composite will be corrupted by misaligned noise.
- Composite signal is too weak (median intensity <1e3) to reliably detect peaks; per-sample detection may recover low-abundance features.
- Peak detection is not a computational bottleneck (e.g., small projects with <5 samples or <100 m/z values per sample).

## Inputs

- aligned mass tracks (intensity arrays indexed by m/z) from all N samples
- retention-time calibration dictionaries (rt_cal_dict) mapping per-sample scan numbers to reference coordinates
- mass grid (m/z values common across aligned samples)
- detection parameters: min_peak_height, min_timepoints (default 25 scans), intensity ceiling (1E8), noise/smoothing thresholds

## Outputs

- composite mass tracks (summed-intensity arrays per m/z)
- detected peaks with m/z, retention time, intensity, cSelectivity, SNR, gaussian fit metrics
- audit metadata: baseline, noise, smoothing flags, detrend status per composite track
- mapping of detected peaks back to constituent sample contributions (via cmap, mass_grid_mapping)

## How to apply

After aligning and calibrating retention times across all samples via rt_cal_dict, synchronize scan-number indices to a reference sample coordinate system. Sum intensity values element-wise across all N samples for each m/z value to construct composite mass tracks (full-length intensity arrays). Audit each composite track: check intensity ceiling (1E8), detect and detrend if median >10× min_peak_height and >50% of points exceed threshold, compute baseline/noise from bottom-signal quartiles, apply moving-average smoothing if noise >1% of max intensity AND max intensity <10× min_peak_height. Subtract baseline+noise to isolate positive regions, split into segments, and invoke scipy.signal.find_peaks exactly once per segment (not N times) with dynamic prominence (max of 1/3 min_peak_height, noise level, 5% segment max). Filter detected peaks by gaussian fit goodness, chromatographic selectivity (cSelectivity), and SNR >2. This approach leverages increased signal-to-noise in the composite to enable single-pass detection while maintaining per-peak quality metrics traceable back to individual samples.

## Related tools

- **scipy.signal.find_peaks** (Core peak-detection algorithm invoked once per composite mass-track segment; detects local maxima with prominence and min-height control) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- **scipy.signal.detrend** (Removes polynomial drift from composite mass tracks before peak detection when median intensity >10× min_peak_height) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.detrend.html
- **asari.peaks.audit_mass_track** (Audits composite track intensity ceiling, noise floor, smoothing necessity, and baseline; gates detrending and smoothing decisions) — https://github.com/shuzhao-li/asari
- **asari.peaks.stats_detect_elution_peaks** (Invokes find_peaks on detrended/smoothed composite segments with dynamic prominence based on noise and segment max) — https://github.com/shuzhao-li/asari
- **asari.peaks.evaluate_gaussian_peak_on_intensity_list** (Fits gaussian to each detected peak and computes goodness_fitting metric for quality filtering) — https://github.com/shuzhao-li/asari
- **asari.peaks.__peaks_cSelectivity_stats__** (Computes chromatographic selectivity (cSelectivity) metric measuring peak isolation and shape consistency) — https://github.com/shuzhao-li/asari
- **asari.chromatograms.rt_lowess_calibration** (Pre-processing step to construct rt_cal_dict for aligning retention times across samples before composite construction) — https://github.com/shuzhao-li/asari

## Examples

```
```python
from asari.peaks import audit_mass_track, stats_detect_elution_peaks
from scipy.signal import find_peaks
import numpy as np

# Composite mass track from summed intensities across N aligned samples
composite_track = np.sum([sample_track for sample_track in aligned_samples], axis=0)

# Audit and preprocess
audit_result = audit_mass_track(composite_track, min_peak_height=10000)
processed_track = audit_result['processed_track']

# Single-pass peak detection on composite (N=1, not N invocations)
peaks, properties = find_peaks(
    processed_track,
    height=10000,
    prominence=max(3333, audit_result['noise_level'], 0.05*processed_track.max())
)

# Evaluate peak quality
for peak_idx in peaks:
    cSelectivity = compute_cSelectivity(processed_track, peak_idx)
    snr = compute_SNR(processed_track[peak_idx], audit_result['noise_level'])
    if snr > 2 and cSelectivity > 0:
        print(f'Peak at scan {peak_idx}: SNR={snr:.2f}, cSelectivity={cSelectivity:.3f}')
```
```

## Evaluation signals

- Peak detection invokes find_peaks exactly 1 time per composite mass track (audit log or code profiling confirms N→1 reduction).
- All detected peaks include non-null cSelectivity, SNR, and gaussian fit goodness metrics, verifying per-peak quality evaluation was applied.
- Composite track construction is verified: sum of per-sample intensities at each m/z matches element-wise sum of input mass tracks.
- Retention-time synchronization is correct: rt_cal_dict was applied to map all sample scan numbers to reference coordinates before summation (check alignment audit).
- Runtime is measured: wall-clock time for peak detection on composite is <1/N of wall-clock time for per-sample detection on the same m/z values (where N = number of samples).
- Output feature table reports peaks with cSelectivity >0 (indicating selectivity was evaluated) and SNR ≥2 threshold applied (per documented filter).

## Limitations

- Composite detection relies on strong summed signal; low-abundance features present in few samples may be lost if individual sample SNR is <2 but composite SNR >2 threshold is marginal.
- Retention-time calibration (rt_cal_dict) must succeed for all samples; failure in any sample corrupts the alignment and composite construction.
- Intensity ceiling (1E8) and noise-floor thresholds (median >1e3) are tuned for typical LC-MS data; extreme dynamic range or very noisy samples may require parameter retuning.
- Per-sample abundance variation is invisible in composite detection; peaks present in only 1–2 samples will not be highlighted during composite detection and must be recovered post-hoc if needed.
- Composite approach assumes additive intensity model; ion-suppression effects or sample-dependent chromatographic shifts are averaged out, potentially masking sample-specific phenomena.

## Evidence

- [other] Asari implements peak detection using scipy.signal.find_peaks on a composite map constructed from summed mass tracks across all samples, reducing the number of peak-detection algorithm calls from N (one per sample) to one (composite), thereby improving scalability and computational efficiency.: "peak detection using scipy.signal.find_peaks on a composite map constructed from summed mass tracks across all samples, reducing the number of peak-detection algorithm calls from N (one per sample)"
- [other] Sum intensity values element-wise across all samples for each unique m/z value in the mass grid, producing composite mass tracks as full-length intensity arrays.: "Sum intensity values element-wise across all samples for each unique m/z value in the mass grid, producing composite mass tracks as full-length intensity arrays."
- [other] Audit each composite mass track (peaks.audit_mass_track): check max intensity ceiling (1E8), apply rescaling if needed, detect low-intensity tracks (median < 1e3), perform detrend if median > 10× min_peak_height and >50% of points exceed threshold: "check max intensity ceiling (1E8), detect low-intensity tracks (median < 1e3), perform detrend if median > 10× min_peak_height and >50% of points exceed threshold"
- [other] Apply scipy.signal.find_peaks on each segment with dynamic prominence (max of 1/3 min_peak_height, noise level, and 5% of segment max intensity), using min_peak_height and min_timepoints (default 25 scans) for window control.: "Apply scipy.signal.find_peaks on each segment with dynamic prominence (max of 1/3 min_peak_height, noise level, and 5% of segment max intensity)"
- [other] Evaluate detected peaks for gaussian fit (goodness_fitting), chromatographic selectivity (cSelectivity), and signal-to-noise ratio (SNR > 2), retaining only peaks meeting thresholds.: "Evaluate detected peaks for gaussian fit (goodness_fitting), chromatographic selectivity (cSelectivity), and signal-to-noise ratio (SNR > 2), retaining only peaks meeting thresholds."
- [intro] Peak detection on a composite map instead of repeated on individual samples: "Peak detection on a composite map instead of repeated on individual samples"
- [other] Synchronize scan-number indices across samples by applying rt_cal_dict to map each sample's scan numbers to reference sample coordinates.: "Synchronize scan-number indices across samples by applying rt_cal_dict to map each sample's scan numbers to reference sample coordinates."
