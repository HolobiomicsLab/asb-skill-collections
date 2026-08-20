---
name: gaussian-peakshape-fitting-evaluation
description: Use when after peak detection on mass track segments using find_peaks,
  when you need to distinguish genuine chromatographic peaks from noise-induced false
  positives or irregular shapes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0621
  tools:
  - Python
  - scipy.signal.find_peaks
  - asari.peaks.evaluate_gaussian_peak_on_intensity_list
  - asari.peaks.detect_evaluate_peaks_on_roi
  - Python (numpy, scipy.optimize)
  techniques:
  - GC-MS
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

# Gaussian peakshape fitting and evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluates detected elution peaks against expected Gaussian shape to filter for chromatographic quality and reduce false positives. Applied after peak detection to retain only peaks with peakshape scores above a threshold (default > 0.5), ensuring detected features represent genuine metabolites rather than noise or artifacts.

## When to use

After peak detection on mass track segments using find_peaks, when you need to distinguish genuine chromatographic peaks from noise-induced false positives or irregular shapes. Particularly important in high-intensity regions where prominence-based detection alone may capture non-Gaussian features or shoulders.

## When NOT to use

- Input is already a feature table or pre-filtered peak list — use this skill during initial peak detection, not post-hoc validation.
- Data are from instruments with non-Gaussian elution profiles (e.g. gas chromatography with tailing or fronting, or highly irregular retention behavior) — Gaussian model assumptions may not hold.
- Peak detection has not yet been performed or apex positions are not reliably identified — peakshape evaluation requires a well-localized apex.

## Inputs

- detected_peaks (list of peak objects with apex position, intensity window, m/z and retention time)
- mass_track_segment (region of interest: intensity array subset after baseline/noise subtraction)
- peakshape_threshold (numeric, default 0.5)
- snr_threshold (numeric, default 2)

## Outputs

- filtered_peaks (peak objects passing peakshape and SNR criteria, with peakshape and SNR scores recorded)
- peak_quality_metrics (table of peakshape, SNR, and apex position for each retained peak)

## How to apply

For each detected peak, fit a Gaussian model to the intensity values in a window around the apex position and calculate a peakshape metric (e.g., ratio of observed peak area to fitted Gaussian area, or R² of fit). Retain peaks only if peakshape exceeds the threshold (default 0.5). This filtering is applied in conjunction with SNR thresholds (default SNR > 2) and validates that the apex position lies within the segment boundaries. The rationale is that metabolite peaks follow Gaussian elution profiles in LC; deviations suggest either co-eluting compounds, baseline artifacts, or instrumental noise rather than a single resolved feature.

## Related tools

- **scipy.signal.find_peaks** (Detects local maxima and prominence on mass track; output feeds into peakshape evaluation) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- **asari.peaks.evaluate_gaussian_peak_on_intensity_list** (Core function implementing Gaussian peakshape fitting and metric calculation) — https://github.com/shuzhao-li/asari
- **asari.peaks.detect_evaluate_peaks_on_roi** (Orchestrates peak detection and peakshape evaluation on each region of interest) — https://github.com/shuzhao-li/asari
- **Python (numpy, scipy.optimize)** (Underlying fitting and numerical optimization for Gaussian model)

## Examples

```
from asari.peaks import evaluate_gaussian_peak_on_intensity_list; peakshape = evaluate_gaussian_peak_on_intensity_list(intensity_window, apex_idx); retained = peak if peakshape > 0.5 and snr > 2 else None
```

## Evaluation signals

- Peakshape scores for retained peaks are >= 0.5 and SNR >= 2; rejected peaks are logged with their failure reason
- Apex positions of retained peaks fall strictly within segment boundaries (no boundary violations)
- Peakshape distribution (histogram or summary stats) is unimodal and concentrated in the 0.5–1.0 range, indicating consistent Gaussian fit quality
- Comparison of rejected vs. retained peaks shows that rejected peaks have visibly irregular or multi-modal intensity profiles around the apex
- Reproducibility check: same mass track and parameters re-processed yields identical peakshape scores and the same set of retained peaks

## Limitations

- Assumes Gaussian elution profile; real peaks may be slightly tailed or fronted, especially at high intensity or under non-ideal chromatographic conditions.
- Peakshape threshold (default 0.5) is a heuristic; may require tuning for different instrument types, column chemistry, or metabolite classes.
- Co-eluting peaks or shoulder peaks may pass Gaussian fitting if the fit window is too narrow; requires integration with retention time alignment and mass separation.
- Very low-intensity peaks near noise floor may show artificially good peakshape due to stochastic noise that happens to fit a Gaussian; SNR threshold mitigates but does not eliminate this.
- Computational cost scales with number of detected peaks and window size; large feature tables may benefit from vectorized evaluation.

## Evidence

- [other] Evaluate detected peaks for Gaussian peakshape, cSelectivity, and signal-to-noise ratio (SNR); retain peaks passing thresholds (default SNR >2, peakshape >0.5).: "Evaluate detected peaks for Gaussian peakshape, cSelectivity, and signal-to-noise ratio (SNR); retain peaks passing thresholds (default SNR >2, peakshape >0.5)."
- [other] Validation: verify that detected peaks have apex positions within segment boundaries, SNR and peakshape values within reported thresholds, and prominence values consistent with local signal characteristics.: "Validation: verify that detected peaks have apex positions within segment boundaries, SNR and peakshape values within reported thresholds, and prominence values consistent with local signal"
- [other] See [peaks.evaluate_gaussian_peak_on_intensity_list](peaks.evaluate_gaussian_peak_on_intensity_list): "See [peaks.evaluate_gaussian_peak_on_intensity_list](peaks.evaluate_gaussian_peak_on_intensity_list)"
