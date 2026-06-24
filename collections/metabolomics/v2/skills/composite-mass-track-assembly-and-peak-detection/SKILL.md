---
name: composite-mass-track-assembly-and-peak-detection
description: Use when after mass tracks have been aligned across all samples into
  a MassGrid (via sample-wise or centroid-based alignment), you have a unified set
  of m/z features tracked across the entire study.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pymzml
  - khipu
  - JMS
  - HMDB 4
  - scipy.signal.find_peaks
  - scipy.signal.detrend
  - asari.peaks.stats_detect_elution_peaks
  - asari.peaks.evaluate_gaussian_peak_on_intensity_list
  - asari.chromatograms.rt_lowess_calibration
  - asari.MassGrid
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
- The default method uses `pymzml` to parse mzML files.
- The preannotaion is done via another package khipu (https://github.com/shuzhao-li-lab/khipu)
- The empirical compounds are searched against known compound database (default HMDB
  4) via another package JMS (https://github.com/shuzhao-li/JMS).
- known compound database (default HMDB 4)
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

# composite-mass-track-assembly-and-peak-detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assemble aligned mass tracks from multiple LC-MS samples into a composite mass track, then detect elution peaks on this composite map using statistics-guided local maxima detection. This approach prioritizes mass resolution and selectivity, avoiding repeated peak detection on individual samples and improving reproducibility across the cohort.

## When to use

After mass tracks have been aligned across all samples into a MassGrid (via sample-wise or centroid-based alignment), you have a unified set of m/z features tracked across the entire study. Use this skill when you need to identify reproducible, high-confidence peaks across the cohort by detecting peaks on the aggregate signal rather than individually per sample, especially for studies with ≤10 samples using anchor-first alignment or larger studies using centroid-based alignment.

## When NOT to use

- Input mass tracks have not yet been aligned across samples into a MassGrid — run mass alignment first.
- RT calibration has not been performed — composite assembly requires rt_cal_dict; apply chromatograms.rt_lowess_calibration before this step.
- You need to detect peaks on individual samples independently (e.g., single-sample metabolomics, where cohort-level assembly is not applicable).

## Inputs

- aligned_MassGrid (object containing per-sample mass tracks aligned across cohort)
- per-sample_rt_calibration_dictionaries (rt_cal_dict keyed by sample ID)
- intensity_alignment_matrix (composite signal per m/z feature × sample)

## Outputs

- CompositeMap.FeatureTable (peak detections mapped to samples with areas/intensities)
- cmap.pickle (serialized composite map object for traceability)
- full_Feature_table.tsv (all detected features meeting SNR >2 and peakshape >0.5)

## How to apply

Construct composite mass tracks by summing aligned intensity values across all samples after retention time (RT) calibration has been applied. Feed each composite mass track to peaks.stats_detect_elution_peaks, which uses scipy.signal.find_peaks (local maxima method) with adaptive prominence filtering (minimum 1/3 of min_peak_height, default 1e5 intensity units) and optional detrending or smoothing. Evaluate detected peaks against peakshape >0.5 (gaussian fit quality) and signal-to-noise ratio (SNR) >2 using peaks.evaluate_gaussian_peak_on_intensity_list. This statistic-guided approach leverages the composite signal to reduce noise while preserving selectivity. Map detected features back to individual samples via RT alignment dictionaries (rt_cal_dict per sample) to extract per-sample peak areas and intensities, recording results in CompositeMap.FeatureTable.

## Related tools

- **scipy.signal.find_peaks** (Local maxima detection with prominence control on composite mass track intensity)
- **scipy.signal.detrend** (Optional smoothing/detrending of mass track before peak detection)
- **asari.peaks.stats_detect_elution_peaks** (Primary peak detection function that wraps find_peaks with adaptive prominence and noise filtering) — https://github.com/shuzhao-li/asari
- **asari.peaks.evaluate_gaussian_peak_on_intensity_list** (Quality filtering of detected peaks by gaussian peakshape and SNR metrics) — https://github.com/shuzhao-li/asari
- **asari.chromatograms.rt_lowess_calibration** (Pre-requisite RT calibration per sample to enable accurate peak mapping back to individual samples) — https://github.com/shuzhao-li/asari
- **asari.MassGrid** (Data structure holding aligned mass tracks across samples; input to composite assembly) — https://github.com/shuzhao-li/asari

## Examples

```
python3 -m asari.main process -i mydir/projectx_dir --mode pos
```

## Evaluation signals

- All detected peaks satisfy peakshape >0.5 (gaussian fit quality) and SNR >2 as recorded in CompositeMap.FeatureTable.
- Peak positions (m/z, RT) are consistent across samples where the feature is present; verify by inspecting full_Feature_table.tsv for features with >1 sample.
- cmap.pickle object is successfully serialized and can be deserialized without errors, confirming internal data structure integrity.
- Composite peak intensity values sum approximately to the sum of per-sample intensities (accounting for RT alignment shifts), validating that alignment and summing was correct.
- Feature count in preferred_Feature_table.tsv (filtered for selectivity) is lower than full_Feature_table.tsv, showing that QC filtering was applied.

## Limitations

- Peak detection relies on local maxima and prominence control; overlapping or severely tailed peaks may not resolve into separate features.
- Composite assembly assumes that RT calibration landmarks (mSelectivity >0.99, prominence >20% of peak height) exist in most samples; sparse landmark peaks will degrade calibration accuracy.
- Adaptive prominence threshold (default 1/3 of min_peak_height = 1e5) may suppress weak but reproducible features in low-abundance studies; user adjustment is necessary.
- Mass resolution advantages (0.001 amu binning, 5 ppm tolerance) assume high-resolution MS data; centroid data with coarser m/z spacing will reduce mass separation gains.

## Evidence

- [methods] Build composite mass tracks by summing aligned intensity values across all samples after RT calibration. Feed each composite mass track to peaks.stats_detect_elution_peaks, which uses scipy.signal.find_peaks (local maxima method) with adaptive prominence filtering (minimum 1/3 of min_peak_height, default 1e5).: "Build composite mass tracks by summing aligned intensity values across all samples after RT calibration. Detect elution peaks on composite mass tracks using peaks.stats_detect_elution_peaks with"
- [intro] Peak detection on a composite map instead of repeated on individual samples.: "Peak detection on a composite map instead of repeated on individual samples"
- [methods] Evaluate peaks with peaks.evaluate_gaussian_peak_on_intensity_list for peakshape >0.5 and SNR >2.: "evaluate peaks with peaks.evaluate_gaussian_peak_on_intensity_list for peakshape >0.5 and SNR >2"
- [methods] Map detected features back to individual samples via RT alignment dictionaries to extract peak areas and intensities, recording results in CompositeMap.FeatureTable.: "Map detected features back to individual samples via RT alignment dictionaries to extract peak areas and intensities, recording results in CompositeMap.FeatureTable"
- [intro] Statistics guided peak detection based on local maxima and prominence with selective use of smoothing.: "Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing"
- [intro] Reproducible tracking and backtracking between features and mass tracks (EICs).: "Reproducible, track and backtrack between features and mass tracks (EICs)"
