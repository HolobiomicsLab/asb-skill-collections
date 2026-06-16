---
name: retention-time-alignment-index-mapping
description: Use when when processing multiple LC-MS samples with varying scan numbers or retention-time drift, before constructing composite mass tracks for peak detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0153
  tools:
  - Python
  - scipy.signal.detrend
  - asari.chromatograms.rt_lowess_calibration
  - asari.chromatograms.extract_massTracks_
  - asari.mass_functions.nn_cluster_by_mz_seeds
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

# Retention-time alignment index mapping

## Summary

Maps scan numbers across LC-MS samples to a reference retention-time coordinate system using sample-specific calibration dictionaries, enabling synchronized intensity summation across aligned mass tracks for downstream composite peak detection. This step is critical for accurate composite-map construction when samples have different scan acquisition patterns or retention-time drift.

## When to use

When processing multiple LC-MS samples with varying scan numbers or retention-time drift, before constructing composite mass tracks for peak detection. Specifically: (1) after extracting mass tracks and retention-time calibration data from individual samples, (2) when the goal is to sum intensity values across samples at synchronized m/z and retention-time positions, and (3) before applying find_peaks to the composite map to ensure peaks are detected at consistent retention-time positions across the cohort.

## When NOT to use

- Single-sample analysis: retention-time alignment is unnecessary when processing one sample in isolation.
- Pre-aligned data: if input samples are already synchronized to a common scan-number or retention-time grid, skip this step.
- Data with insufficient anchor landmarks: if fewer than ~5–10 stable anchor mass tracks are available for LOWESS calibration, the resulting rt_cal_dict may be unreliable; consider manual inspection or alternative alignment strategies.

## Inputs

- aligned mass tracks from all samples (intensity arrays indexed by scan number)
- retention-time calibration dictionary per sample (rt_cal_dict: mapping from sample scan numbers to reference coordinates)
- anchor mass tracks (m/z values with known isotope or adduct relationships for LOWESS fitting)
- reference sample scan-number index range

## Outputs

- synchronized scan-number indices for all samples mapped to reference coordinates
- composite mass tracks (summed intensity arrays per m/z, full-length, aligned across samples)
- MassGrid (aligned mass track matrix with synchronized retention-time positions)

## How to apply

For each sample in the dataset, apply its retention-time calibration dictionary (rt_cal_dict) to map the sample's scan-number indices to the reference sample's scan-number coordinates. This calibration is typically derived by fitting retention-time landmarks (e.g., anchor mass tracks corresponding to 13C/12C isotope or Na/H adduct patterns) using LOWESS regression (rt_lowess_calibration). Once all samples are mapped to the same scan-number index space, intensity values from individual mass tracks at corresponding m/z values can be summed element-wise across samples to produce composite mass tracks of uniform full-length arrays. The quality of alignment depends on the stability and number of anchor mass tracks used for calibration; poor alignment will lead to smoothing or splitting of peaks in the composite map. Validate that all samples' scan numbers fall within the reference range and that no out-of-bounds mapping occurs.

## Related tools

- **scipy.signal.detrend** (Applied during mass-track audit to remove linear or polynomial drift before alignment calibration) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.detrend.html
- **asari.chromatograms.rt_lowess_calibration** (Fits retention-time calibration curve (rt_cal_dict) using anchor mass tracks via LOWESS regression to map sample scan numbers to reference coordinates) — https://github.com/shuzhao-li/asari
- **asari.chromatograms.extract_massTracks_** (Extracts aligned mass tracks from individual samples prior to retention-time synchronization) — https://github.com/shuzhao-li/asari
- **asari.mass_functions.nn_cluster_by_mz_seeds** (Identifies anchor mass tracks (isotope and adduct relationships) used to define retention-time calibration landmarks) — https://github.com/shuzhao-li/asari

## Examples

```
# Within asari workflow after extracting mass tracks and anchor landmarks:
rt_cal_dict = chromatograms.rt_lowess_calibration(anchor_tracks, reference_sample_index)
synchronized_scans = {sample_id: rt_cal_dict[sample_id](sample_scan_nums) for sample_id, sample_scan_nums in samples.items()}
composite_mass_track = sum([aligned_tracks[sample_id] for sample_id in samples.keys()])
```

## Evaluation signals

- All sample scan numbers are successfully mapped to the reference coordinate system with no out-of-bounds indices; rt_cal_dict produces monotonically increasing or smoothly varying scan-number mappings.
- Composite mass tracks are full-length uniform arrays (same length across all m/z values) with no gaps or misalignment artifacts.
- Peak locations in the composite map align with visually inspected chromatograms (EICs) from individual samples; peaks do not exhibit artificial splitting or broadening due to misalignment.
- Retention-time calibration residuals (difference between observed and fitted anchor landmarks) are small (e.g., < 0.5 scans) and show no systematic bias across the retention-time range.
- Cross-sample peak consistency: features detected in the composite map have consistent m/z and retention-time positions when back-tracked to individual samples, with intensity ratios matching sample amounts or expected biological variation.

## Limitations

- LOWESS calibration assumes sufficient density and stability of anchor mass tracks across the full retention-time range; sparse or drifting landmarks may lead to unreliable calibration, especially at the edges of the chromatogram.
- The method does not account for non-linear retention-time effects (e.g., column degradation, temperature gradients) that vary by m/z; complex drift patterns may require sample-specific or m/z-stratified calibration.
- Misidentification of anchor mass tracks (e.g., false isotope or adduct patterns) propagates into the calibration curve; manual review of anchor selection is recommended for novel instrument configurations or sample types.
- The approach assumes all samples share a common mass-calibration grid (m/z values); if samples have very different mass ranges or mass resolution, separate mass grids and composite maps may be required.

## Evidence

- [other] Synchronize scan-number indices across samples by applying rt_cal_dict to map each sample's scan numbers to reference sample coordinates.: "Synchronize scan-number indices across samples by applying rt_cal_dict to map each sample's scan numbers to reference sample coordinates."
- [methods] Establish anchor mass tracks by finding m/z differences that match to either 13C/12C isotopes or Na/H adducts.: "Establish anchor mass tracks by finding m/z differences that match to either 13C/12C isotopes or Na/H adducts."
- [methods] See [chromatograms.rt_lowess_calibration](chromatograms.rt_lowess_calibration): "See [chromatograms.rt_lowess_calibration](chromatograms.rt_lowess_calibration)"
- [other] Sum intensity values element-wise across all samples for each unique m/z value in the mass grid, producing composite mass tracks as full-length intensity arrays.: "Sum intensity values element-wise across all samples for each unique m/z value in the mass grid, producing composite mass tracks as full-length intensity arrays."
- [methods] Aignment of mass tracks across samples, resulting in the MassGrid: "Aignment of mass tracks across samples, resulting in the MassGrid"
