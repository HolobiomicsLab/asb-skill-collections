---
name: selectivity-metric-computation-chromatographic
description: Use when after peak detection on composite mass tracks when you need to evaluate whether a detected peak represents a pure, interference-free signal on its m/z channel.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - scipy.signal.find_peaks
  - asari.peaks.detect_evaluate_peaks_on_roi
  - asari.peaks.evaluate_gaussian_peak_on_intensity_list
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

# selectivity-metric-computation-chromatographic

## Summary

Compute chromatographic selectivity metrics (cSelectivity) to assess the purity and interference-free nature of detected elution peaks on mass tracks. This metric is essential for filtering low-quality peaks and tracking peak confidence across LC-MS metabolomics workflows.

## When to use

Apply this skill after peak detection on composite mass tracks when you need to evaluate whether a detected peak represents a pure, interference-free signal on its m/z channel. Use it as a quality filter during peak evaluation stages, particularly when integrating peaks from different mass regions or assessing peak confidence for annotation workflows. Essential when working with high-resolution LC-MS data where multiple ions may coelute at similar m/z values.

## When NOT to use

- Input is already a curated feature table with pre-filtered, high-confidence peaks — selectivity computation is redundant.
- Working with targeted, single-ion monitoring (SIM) or selected reaction monitoring (SRM) where coelution is structurally impossible.
- Peak detection has not yet been performed; selectivity requires detected peak candidates as input.

## Inputs

- mass track (intensity array indexed by scan/retention time)
- detected peak positions (apex scan indices)
- peak boundary/region of interest coordinates
- baseline and noise-filtered intensity values

## Outputs

- cSelectivity score per peak (0–1 range, higher = purer signal)
- peak quality assessment (pass/fail on selectivity threshold)
- annotated peak list with selectivity metadata

## How to apply

After detecting candidate peaks using scipy.signal.find_peaks on a mass track, compute cSelectivity for each peak by analyzing the peak's intensity profile relative to the overall signal on that m/z channel. The selectivity metric quantifies whether the peak stands out cleanly from background and coeluting interference. Retain peaks only if their cSelectivity values exceed quality thresholds (typically cSelectivity >0.5 in asari) alongside SNR and peakshape constraints. This computation is performed during the evaluation phase of detect_evaluate_peaks_on_roi, where peaks are assessed for Gaussian shape, SNR (>2), and selectivity before final feature reporting. The metric helps distinguish genuine chromatographic features from noise or minor shoulders on larger peaks.

## Related tools

- **scipy.signal.find_peaks** (Prerequisite peak detection using local maxima and prominence; selectivity is computed on detected peaks)
- **asari.peaks.detect_evaluate_peaks_on_roi** (Integration point where cSelectivity is evaluated alongside SNR and peakshape for peak filtering) — https://github.com/shuzhao-li/asari
- **asari.peaks.evaluate_gaussian_peak_on_intensity_list** (Companion metric evaluation function for peakshape and SNR alongside selectivity) — https://github.com/shuzhao-li/asari

## Evaluation signals

- Selectivity values are bounded in [0, 1]; verify no NaN, negative, or >1 values appear in output.
- Peaks passing selectivity threshold (cSelectivity > 0.5) correspond to chromatographically resolved signals; verify by visual inspection of raw mass track intensity profiles around apex.
- Peaks failing selectivity threshold show elevated interference or shoulder patterns; cross-check against baseline-subtracted intensity profiles.
- Feature table filtering on cSelectivity should reduce false positives (noise/interference peaks) without removing genuine low-abundance features; verify via ROC or precision-recall metrics if ground truth is available.
- Selectivity scores should correlate inversely with local background noise and coelution intensity; verify via correlation analysis with SNR and peakshape metrics.

## Limitations

- Selectivity computation is sensitive to baseline and noise filter estimation accuracy; poor baseline subtraction inflates apparent selectivity of contaminated peaks.
- The metric may not detect subtle coelution when peaks share very similar retention times and both contribute substantial signal; selectivity alone cannot distinguish unresolved multiplets.
- Selectivity thresholds (e.g., >0.5) are empirically derived and may require tuning for different ionization modes, chromatography types, or instrument configurations.
- High mass resolution alone does not guarantee high selectivity if multiple compounds ionize to the same m/z; selectivity is a chromatographic (retention time domain) purity metric, not a mass accuracy metric.

## Evidence

- [other] Evaluate detected peaks for Gaussian peakshape, cSelectivity, and signal-to-noise ratio (SNR); retain peaks passing thresholds (default SNR >2, peakshape >0.5).: "Evaluate detected peaks for Gaussian peakshape, cSelectivity, and signal-to-noise ratio (SNR); retain peaks passing thresholds (default SNR >2, peakshape >0.5)."
- [intro] Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases: "Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases"
- [other] See [peaks.stats_detect_elution_peaks](peaks.stats_detect_elution_peaks), [peaks.detect_evaluate_peaks_on_roi](peaks.detect_evaluate_peaks_on_roi).: "See [peaks.stats_detect_elution_peaks](peaks.stats_detect_elution_peaks), [peaks.detect_evaluate_peaks_on_roi](peaks.detect_evaluate_peaks_on_roi)."
- [other] For each segment (region of interest), detect peaks using scipy.signal.find_peaks with dynamic prominence and min_peak_height and min_timepoints constraints: "For each segment (region of interest), detect peaks using scipy.signal.find_peaks with dynamic prominence and min_peak_height and min_timepoints constraints on a sliding window"
