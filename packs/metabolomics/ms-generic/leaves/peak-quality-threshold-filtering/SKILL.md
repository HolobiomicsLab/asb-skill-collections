---
name: peak-quality-threshold-filtering
description: Use when after composite-map peak detection (scipy.signal.find_peaks) has identified candidate peaks on aligned mass tracks, but before compiling the final feature table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - asari peaks module
  - scipy.signal.find_peaks
  - evaluate_gaussian_peak_on_intensity_list
  - compute_noise_by_flanks
  - stats_detect_elution_peaks
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- See [peaks.evaluate_gaussian_peak_on_intensity_list](peaks.evaluate_gaussian_peak_on_intensity_list), [peaks.__peaks_cSelectivity_stats_](peaks.__peaks_cSelectivity_stats_),
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

# peak-quality-threshold-filtering

## Summary

A post-detection filtering step that applies quantitative thresholds on signal-to-noise ratio (SNR), peak shape goodness-of-fit, peak height, and prominence to remove low-quality peaks from composite-map peak detection output before constructing the final feature table. This reduces false positives while retaining reproducible, well-shaped features for downstream analysis.

## When to use

After composite-map peak detection (scipy.signal.find_peaks) has identified candidate peaks on aligned mass tracks, but before compiling the final feature table. Apply this skill when you have an unfiltered peak list with SNR, peak-shape metrics, peak height, and prominence values computed, and you need to reduce spurious or poorly-shaped detections to improve feature table quality and reproducibility.

## When NOT to use

- Input is already a curated feature table; re-filtering may remove valid biological signal.
- Peak detection has not yet been run on the composite map; filtering requires prior peak candidacy.
- SNR, peak-shape metrics, peak height, or prominence have not been pre-computed for the peak list.

## Inputs

- unfiltered peak list (JSON or structured format) from composite-map peak detection containing SNR, goodness_fitting (peakshape), peak_height, and prominence per peak
- RT alignment dictionaries mapping peaks to individual samples
- mass tracks (EICs) and associated intensity arrays

## Outputs

- filtered peak list with only peaks passing all four thresholds
- preferred_Feature_table.tsv with peak area and intensity values for retained features
- row count comparison between full_Feature_table.tsv and filtered table

## How to apply

Load the full unfiltered peak list from composite-map peak detection output containing SNR, goodness_fitting (peakshape), peak_height, and prominence values. Apply four sequential threshold filters: (1) SNR > 2 to retain peaks with sufficient signal-to-noise ratio; (2) goodness_fitting > 0.5 using gaussian peak evaluation to retain well-shaped peaks; (3) peak_height ≥ default 1e5 (configurable) to exclude noise-level detections; (4) prominence ≥ 20% of peak_height to retain only locally prominent peaks. Map filtered peaks back to individual samples via retention-time alignment dictionaries to extract sample-specific peak areas and intensities. Compile the filtered feature table (preferred_Feature_table.tsv) and compare row counts between full and filtered tables to confirm the reduction is appropriate relative to the unfiltered reference.

## Related tools

- **scipy.signal.find_peaks** (prior step: detects candidate peaks on composite mass track using local maxima and prominence control)
- **asari peaks module** (implements peak quality filtering, SNR computation, gaussian peak fitting, and prominence evaluation) — https://github.com/shuzhao-li/asari
- **evaluate_gaussian_peak_on_intensity_list** (computes goodness_fitting metric by fitting gaussian to peak shape) — https://github.com/shuzhao-li/asari
- **compute_noise_by_flanks** (estimates noise level from peak flanks to compute SNR) — https://github.com/shuzhao-li/asari
- **stats_detect_elution_peaks** (performs statistical peak detection with quality metrics pre-filtering) — https://github.com/shuzhao-li/asari

## Evaluation signals

- Row count of filtered feature table is substantially lower than full_Feature_table.tsv (confirming filtering removed spurious peaks)
- All retained peaks satisfy all four thresholds: SNR > 2, goodness_fitting > 0.5, peak_height ≥ 1e5, prominence ≥ 0.2 × peak_height
- Filtered feature table maps reproducibly back to individual samples via RT alignment; no sample-specific peak areas are null or inconsistent
- Visual inspection of a subset of retained peaks confirms visually well-shaped, prominent elution profiles vs. noisy or shoulder peaks in discarded list
- Preferr_Feature_table.tsv shows non-zero intensity values across expected sample cohorts, indicating filtering did not over-eliminate biology

## Limitations

- Default thresholds (SNR > 2, goodness_fitting > 0.5, peak_height 1e5, prominence 20%) may be overly stringent or permissive depending on instrument, ionization mode, and metabolite abundance distribution; threshold optimization may be required for non-standard sample types.
- Gaussian peak-shape assumption in goodness_fitting metric may underestimate quality of peaks with asymmetric or multi-lobed elution profiles common in complex matrices.
- Prominence threshold (20% of peak_height) does not account for baseline noise variation across the chromatographic dimension; peaks in high-noise regions may be incorrectly filtered even if biologically real.
- Filtering is applied uniformly across all m/z and retention time ranges; co-eluting isotopologue clusters or adduct families may be unexpectedly split if individual peak heights differ substantially.

## Evidence

- [other] Apply SNR threshold filter (SNR > 2) to retain only peaks with sufficient signal-to-noise ratio.: "Apply SNR threshold filter (SNR > 2) to retain only peaks with sufficient signal-to-noise ratio."
- [other] Apply peakshape threshold filter (goodness_fitting > 0.5) using gaussian peak evaluation to retain well-shaped peaks.: "Apply peakshape threshold filter (goodness_fitting > 0.5) using gaussian peak evaluation to retain well-shaped peaks."
- [other] Apply minimum peak height threshold (default 1e5) combined with prominence requirement (≥20% of peak_height) to retain only sufficiently tall and prominent peaks.: "Apply minimum peak height threshold (default 1e5) combined with prominence requirement (≥20% of peak_height) to retain only sufficiently tall and prominent peaks."
- [intro] Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases: "Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases"
- [readme] All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards (part of input parameters but default values are fine for most people).: "All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards"
