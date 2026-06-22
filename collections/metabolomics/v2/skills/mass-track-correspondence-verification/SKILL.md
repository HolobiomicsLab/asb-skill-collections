---
name: mass-track-correspondence-verification
description: Use when after constructing a LOWESS regression function (rt_cal_dict) to align retention times between a reference sample and a current sample, validate that high-selectivity landmark peaks in the reference sample (mSelectivity > 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - scipy
  - scipy.signal (LOWESS)
  - asari (chromatograms.rt_lowess_calibration)
  - asari (peaks.quick_detect_unique_elution_peak)
  - asari (peaks.audit_mass_track)
  - asari (CompositeMap.calibrate_sample_RT)
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- scipy.signal module for LOWESS fitting via the regression function
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

# mass-track-correspondence-verification

## Summary

Verify that landmark peaks identified in a reference sample correctly map to their counterparts in aligned samples by checking scan-number correspondence after LOWESS-based retention time calibration. This confirms that the RT alignment function preserves peak identity across the sample cohort.

## When to use

After constructing a LOWESS regression function (rt_cal_dict) to align retention times between a reference sample and a current sample, validate that high-selectivity landmark peaks in the reference sample (mSelectivity > 0.99, prominence > 20% of peak height) correctly correspond to their aligned landmarks in the current sample by verifying scan-number mappings stay within the calibration bounds.

## When NOT to use

- Before LOWESS regression has been performed on landmark peak pairs—verification requires a fitted rt_cal_dict.
- When landmark peaks have not been filtered for high selectivity (mSelectivity ≤ 0.99 or no prominence filter applied)—correspondence checks assume selectivity pre-filtering.
- If the goal is to detect individual outlier peaks in a mass track; use audit_mass_track or stats_detect_elution_peaks instead for peak-level QC.

## Inputs

- rt_cal_dict (sparse scan-number mapping dictionary from LOWESS calibration)
- landmark_peaks_reference (high-selectivity peaks from reference sample: mSelectivity > 0.99, prominence > 20% of peak height)
- landmark_peaks_current (good-selectivity peaks from current sample, restricted to mass tracks aligned to reference landmarks)
- scan_number_pairs (tuples of sample_RT_number and reference_RT_number from good landmark peaks)

## Outputs

- validation_report (boolean pass/fail and diagnostic metrics)
- correspondence_mapping (verified scan-number alignments for each landmark peak)
- out_of_bounds_landmarks (list of landmark peaks failing calibration bounds checks)

## How to apply

Apply the generated rt_cal_dict sparse calibration dictionary to transform scan numbers of landmark peaks from the current sample into reference RT space. Verify that each transformed scan number (1) matches the recorded reference scan number for that landmark peak within acceptable tolerance, (2) remains within the ±10% extension margins applied during LOWESS regression fitting to ensure extrapolation validity, and (3) maintains monotonic ordering (no RT inversions). If any landmark peak fails these checks, investigate whether the peak selectivity criteria were too permissive, whether the LOWESS regression overfitted due to outlier peaks, or whether genuine sample-to-sample retention time drift exceeds the model's assumptions. Re-audit mass tracks (audit_mass_track) or relax min_peak_height thresholds if a systematic calibration failure is detected.

## Related tools

- **scipy.signal (LOWESS)** (Generates the regression function mapping sample RT to reference RT; calibration function is then verified by correspondence checks) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html
- **asari (chromatograms.rt_lowess_calibration)** (Produces the rt_cal_dict sparse mapping dictionary; correspondence verification operates on its outputs) — https://github.com/shuzhao-li/asari
- **asari (peaks.quick_detect_unique_elution_peak)** (Identifies high-selectivity landmark peaks used as inputs to correspondence verification) — https://github.com/shuzhao-li/asari
- **asari (peaks.audit_mass_track)** (Provides low-level mass track quality metrics; failures in correspondence may trigger re-audit) — https://github.com/shuzhao-li/asari
- **asari (CompositeMap.calibrate_sample_RT)** (Orchestrates RT calibration workflow; correspondence verification is a validation step within this stage) — https://github.com/shuzhao-li/asari

## Evaluation signals

- All landmark peak scan numbers transform via rt_cal_dict without raising out-of-bounds exceptions (transformed values remain within sample RT boundaries)
- Transformed scan numbers match recorded reference scan numbers for each landmark peak with zero or minimal expected rounding error
- Monotonic ordering is preserved: if scan_number_i < scan_number_j in current sample, then calibrated_scan_i < calibrated_scan_j in reference space
- At least 90% of landmark peaks pass correspondence verification; failures are systematically logged with reason codes (e.g., selectivity dropout, extrapolation exceeds ±10%)
- rt_cal_dict does not contain gaps or discontinuities that would violate RT relationship continuity implied by LOWESS smoothing

## Limitations

- Landmark peak identification depends on stringent selectivity thresholds (mSelectivity > 0.99); if few or no peaks meet this criterion in a sample, correspondence verification has insufficient data and cannot validate the RT calibration.
- LOWESS regression adds ±10% extension boundaries to stabilize convergence; validation is restricted to scans within these margins, so RT alignment for very early or very late eluting peaks may not be verifiable.
- Correspondence checks assume that mass track alignment has already succeeded; if misaligned mass tracks are passed to landmark detection, landmark pairs will be spurious and correspondence verification will falsely pass.
- The method does not detect bimodal or multimodal RT drift; if retention time shifts non-monotonically across the sample, LOWESS may produce a smooth function that obscures the underlying pathology.

## Evidence

- [other] Validation: verify that rt_cal_dict enables accurate RT alignment by confirming landmark peak scan numbers map correctly and that extrapolation remains bounded within ±10% extension margins.: "verify that rt_cal_dict enables accurate RT alignment by confirming landmark peak scan numbers map correctly and that extrapolation remains bounded within ±10% extension margins"
- [other] Identify high-selectivity landmark peaks in the reference sample using criteria: mSelectivity > 0.99, min_peak_height satisfied (default 1e5), prominence > 20% of peak height, and single peak per mass track.: "Identify high-selectivity landmark peaks in the reference sample using criteria: mSelectivity > 0.99, min_peak_height satisfied (default 1e5), prominence > 20% of peak height"
- [other] Select good landmark peaks from the current sample by applying the same selectivity criteria, but restricted to mass tracks already aligned to the reference landmarks.: "Select good landmark peaks from the current sample by applying the same selectivity criteria, but restricted to mass tracks already aligned to the reference landmarks"
- [other] Perform LOWESS regression (scipy.signal fitting) on the pairs of (sample_RT_number, reference_RT_number) from the good landmark peaks, adding 10% extension boundaries at both ends to constrain convergence.: "Perform LOWESS regression (scipy.signal fitting) on the pairs of (sample_RT_number, reference_RT_number) from the good landmark peaks, adding 10% extension boundaries"
- [other] Export the regression function as a sparse scan-number mapping dictionary (rt_cal_dict) that records only differing values and stays within sample RT boundaries.: "Export the regression function as a sparse scan-number mapping dictionary (rt_cal_dict) that records only differing values and stays within sample RT boundaries"
