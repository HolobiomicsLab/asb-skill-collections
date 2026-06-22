---
name: signal-to-noise-ratio-calculation-peaks
description: Use when after elution peaks have been detected on composite mass tracks using local maxima and prominence detection, before reporting features in the final feature table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0218
  tools:
  - scipy.signal.find_peaks
  - scipy.signal.detrend
  - Python
  - asari.peaks.evaluate_gaussian_peak_on_intensity_list
  - asari.peaks.stats_detect_elution_peaks
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control that is dynamically determined on each mass track then each segment.
- detrend (scipy.signal.detrend) is performed on the mass track. Detrend is a regression method to ensure the baseline is not significantly rising or decreasing over the chromatography.
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

# Signal-to-Noise-Ratio Calculation for Peaks

## Summary

Quantifies the quality of detected chromatographic peaks by computing the ratio of peak intensity to local noise, enabling filtering of low-confidence features in LC-MS metabolomics. This metric is used to retain only peaks with SNR above a defined threshold (default SNR >2) during feature extraction from composite mass tracks.

## When to use

After elution peaks have been detected on composite mass tracks using local maxima and prominence detection, before reporting features in the final feature table. Apply this skill when you need to distinguish genuine metabolite signals from noise artifacts in high-resolution LC-MS data, particularly after baseline and noise filtering have been applied.

## When NOT to use

- Input peaks have not yet been baseline- and noise-corrected; SNR calculation requires prior noise estimation.
- Mass track has not been audited and rescaled; SNR thresholds may not be comparable across studies if intensity scales differ by >1E8.
- Feature table has already been generated and filtered; SNR is calculated during peak detection, not post-hoc.

## Inputs

- composite mass track (intensity array with aligned scans across samples)
- detected elution peak (with apex position, intensity, and boundary coordinates)
- estimated noise level (from intensity distribution below lower quartile)
- baseline-subtracted intensity values

## Outputs

- SNR value (float, unitless ratio)
- boolean pass/fail indicator (SNR >= threshold)
- filtered peak list (peaks passing SNR threshold)

## How to apply

For each detected peak on a baseline- and noise-subtracted composite mass track, calculate SNR as the ratio of peak intensity (typically the apex intensity) to the estimated noise level derived from intensity values below the lower quartile of the mass track plus the min_intensity_threshold. Evaluate each detected peak against the SNR threshold (default SNR >2); retain only peaks that meet or exceed this threshold. This filtering step is performed as part of the peak evaluation stage (alongside Gaussian peakshape and selectivity metrics) before peaks are added to the feature table. SNR serves as one of three primary quality gates, ensuring that reported features represent detectable signals rather than noise fluctuations.

## Related tools

- **scipy.signal.find_peaks** (detects local maxima and prominence on mass track prior to SNR evaluation)
- **asari.peaks.evaluate_gaussian_peak_on_intensity_list** (evaluates Gaussian peakshape alongside SNR to filter peaks during feature extraction) — https://github.com/shuzhao-li/asari
- **asari.peaks.stats_detect_elution_peaks** (orchestrates the full peak detection and SNR filtering pipeline on composite map) — https://github.com/shuzhao-li/asari

## Evaluation signals

- SNR values are strictly positive (>0) and dimensionless; check that all reported SNR values are numeric and greater than zero.
- Peak retention rate is consistent with threshold: at default SNR >2, expect ~70–90% of initially detected peaks to pass, depending on sample complexity and instrument noise characteristics.
- SNR values correlate inversely with baseline noise level: peaks in low-noise regions should have higher SNR; recalculate and verify if SNR distribution appears bimodal or inverted.
- Peaks with SNR below threshold are absent from final feature table; spot-check by computing SNR manually for a subset of borderline peaks and verifying they fall below the cutoff.
- SNR threshold consistency: default value of SNR >2 should be reported in output metadata; verify that the same threshold is applied across all samples in a batch.

## Limitations

- SNR calculation depends on accurate noise level estimation (from intensity values below lower quartile); if baseline/noise filtering fails, SNR may be artificially inflated or deflated.
- Fixed threshold (default SNR >2) may not be optimal for all sample types or ionization modes; low-abundance metabolites in clean samples might be retained despite low SNR, while high-noise samples may lose genuine features.
- SNR does not account for peak selectivity (chromatographic separation from co-eluting features); two peaks with identical SNR but different chromatographic resolution may have different biological interpretability.
- Composite map construction can bias SNR calculation if mass tracks are misaligned across samples; retention time shifts or mass errors upstream will propagate to SNR values.

## Evidence

- [other] Evaluate detected peaks for Gaussian peakshape, cSelectivity, and signal-to-noise ratio (SNR); retain peaks passing thresholds (default SNR >2, peakshape >0.5).: "Evaluate detected peaks for Gaussian peakshape, cSelectivity, and signal-to-noise ratio (SNR); retain peaks passing thresholds (default SNR >2, peakshape >0.5)."
- [other] the bottom signals are taken as intensity values below the lower quartile plus min_intensity_threshold: "the bottom signals are taken as intensity values below the lower quartile plus min_intensity_threshold"
- [readme] All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards (part of input parameters but default values are fine for most people).: "All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards"
