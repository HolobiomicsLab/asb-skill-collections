---
name: peak-evaluation-metrics-cselectivity-snr-gaussian-fit
description: Use when after scipy.signal.find_peaks has identified candidate peaks on a composite mass track segment, evaluate each peak to decide whether to retain it in the final feature table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - scipy.signal.find_peaks
  - peaks.evaluate_gaussian_peak_on_intensity_list
  - peaks.__peaks_cSelectivity_stats_
  - peaks.compute_noise_by_flanks
  - peaks.audit_mass_track
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari
schema_version: 0.2.0
---

# peak-evaluation-metrics-cSelectivity-SNR-gaussian-fit

## Summary

Evaluate detected peaks against three orthogonal quality criteria—chromatographic selectivity (cSelectivity), signal-to-noise ratio (SNR > 2), and gaussian fit quality—to retain only peaks meeting shape and signal thresholds. This multi-metric filtering ensures peaks are reproducible, well-resolved from background, and conform to expected peak shape.

## When to use

After scipy.signal.find_peaks has identified candidate peaks on a composite mass track segment, evaluate each peak to decide whether to retain it in the final feature table. Use this skill when you have detected peaks with coordinates (m/z, retention time) and need to filter by chromatographic selectivity, signal quality, and peak shape before reporting to downstream analysis or annotation.

## When NOT to use

- Peak detection has not yet been performed (use scipy.signal.find_peaks first).
- Input data are already feature-level aggregates (feature table) rather than individual mass-track peaks; this skill operates on single-m/z peak objects, not across-sample features.
- The mass track has not been audited (audit_mass_track must be applied to establish baseline, noise, and detrending); SNR and selectivity calculations depend on those outputs.

## Inputs

- list of detected peak coordinates (m/z, scan number/retention time index)
- intensity values from the segment containing the peak
- baseline and noise estimates for the mass track (from audit_mass_track)
- full mass track intensities (for selectivity and Gaussian fit evaluation)

## Outputs

- filtered list of peaks meeting SNR > 2, cSelectivity, and gaussian fit thresholds
- peak metadata including SNR, cSelectivity, and gaussian fit goodness_fitting score
- binary pass/fail decision per peak

## How to apply

For each detected peak, compute three independent metrics: (1) Gaussian fit quality using evaluate_gaussian_peak_on_intensity_list, which fits a Gaussian curve to the peak region and scores goodness of fit; (2) chromatographic selectivity (cSelectivity) using __peaks_cSelectivity_stats_, quantifying how well the peak is resolved from neighboring signals in the mass track; (3) signal-to-noise ratio (SNR) by dividing the peak's intensity by the noise floor (computed from bottom-signal quartiles via compute_noise_by_flanks). Retain only peaks where SNR > 2, cSelectivity exceeds a threshold (article does not specify exact value, but selectivity is tracked as a key metric), and gaussian fit goodness is acceptable. The rationale is that these three metrics are independent and complementary: SNR ensures signal strength, cSelectivity ensures chromatographic isolation, and gaussian fit ensures the peak conforms to expected peak shape and is not an artifact.

## Related tools

- **scipy.signal.find_peaks** (detects candidate peak locations before this evaluation step) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- **peaks.evaluate_gaussian_peak_on_intensity_list** (fits Gaussian curve to peak region and computes goodness_fitting metric) — https://github.com/shuzhao-li/asari
- **peaks.__peaks_cSelectivity_stats_** (computes chromatographic selectivity (cSelectivity) for each peak) — https://github.com/shuzhao-li/asari
- **peaks.compute_noise_by_flanks** (estimates noise floor from flanking regions to enable SNR calculation) — https://github.com/shuzhao-li/asari
- **peaks.audit_mass_track** (pre-processes mass track (baseline, detrending, smoothing) required for clean evaluation) — https://github.com/shuzhao-li/asari

## Evaluation signals

- All retained peaks have SNR > 2 (SNR = peak intensity / noise floor estimate); check that no peak with SNR ≤ 2 is retained.
- cSelectivity metric is computed and reported for every peak; verify that a cSelectivity value appears in the output peak metadata and is within expected range [0, 1] or similar normalized scale.
- gaussian_fit quality score (goodness_fitting) is computed and peaks meeting threshold are explicitly marked; confirm that peaks with poor Gaussian fit are rejected.
- Peak evaluation functions are invoked exactly once per detected peak (not multiple times or skipped); trace that evaluate_gaussian_peak_on_intensity_list, __peaks_cSelectivity_stats_, and SNR calculation are called for each candidate.
- Final feature table includes cSelectivity, SNR, and gaussian fit columns; spot-check a sample of peaks to verify reasonable values (e.g., SNR > 2, cSelectivity not at extremes for real peaks).

## Limitations

- Exact cSelectivity threshold value is not specified in the article; practitioners must calibrate this threshold empirically or use asari defaults.
- SNR calculation depends on accurate noise estimation via compute_noise_by_flanks, which may fail or underestimate noise in crowded or noisy mass tracks.
- Gaussian fit evaluation assumes peaks follow a Gaussian shape; highly asymmetric or multiply-charged peaks may fail this criterion even if they are valid metabolite peaks.
- The three metrics (SNR, cSelectivity, gaussian fit) are independent; a peak may fail one criterion while passing others—the article does not specify how to handle partial failures or whether weighted aggregation is used.
- Peak evaluation is applied per mass track segment; isolated peaks or peaks in sparse segments may have unreliable selectivity or fit estimates due to limited neighboring signal context.

## Evidence

- [methods] Evaluate detected peaks for gaussian fit (goodness_fitting), chromatographic selectivity (cSelectivity), and signal-to-noise ratio (SNR > 2), retaining only peaks meeting thresholds.: "Evaluate detected peaks for gaussian fit (goodness_fitting), chromatographic selectivity (cSelectivity), and signal-to-noise ratio (SNR > 2), retaining only peaks meeting thresholds."
- [methods] See [peaks.evaluate_gaussian_peak_on_intensity_list](peaks.evaluate_gaussian_peak_on_intensity_list): "See [peaks.evaluate_gaussian_peak_on_intensity_list](peaks.evaluate_gaussian_peak_on_intensity_list)"
- [methods] See [peaks.__peaks_cSelectivity_stats_](peaks.__peaks_cSelectivity_stats_): "See [peaks.__peaks_cSelectivity_stats_](peaks.__peaks_cSelectivity_stats_)"
- [methods] See [peaks.compute_noise_by_flanks](peaks.compute_noise_by_flanks).: "See [peaks.compute_noise_by_flanks](peaks.compute_noise_by_flanks)."
- [intro] Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases: "Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases"
