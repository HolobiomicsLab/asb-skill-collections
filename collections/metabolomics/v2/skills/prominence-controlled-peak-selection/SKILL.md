---
name: prominence-controlled-peak-selection
description: Use when after initial peak detection on composite mass tracks via local maxima and smoothing, when you have unfiltered peak lists (JSON or structured format) containing prominence values and need to reduce the number of detected features while maintaining signal quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - asari peaks module
  - scipy.signal.find_peaks
  - asari peaks.compute_noise_by_flanks
  - asari peaks.stats_detect_elution_peaks
  - asari peaks.evaluate_gaussian_peak_on_intensity_list
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# prominence-controlled-peak-selection

## Summary

Apply prominence thresholds to peaks detected on composite mass chromatograms to retain only elution features with sufficient signal prominence relative to their local baseline. This is a key filtering step in asari's statistics-guided peak detection that reduces false positives while preserving genuine metabolite signals.

## When to use

After initial peak detection on composite mass tracks via local maxima and smoothing, when you have unfiltered peak lists (JSON or structured format) containing prominence values and need to reduce the number of detected features while maintaining signal quality. Use this when the raw peak detection includes many marginal peaks that lack chromatographic prominence—typical in high-resolution LC-MS metabolomics where baseline noise and shoulder peaks are common.

## When NOT to use

- Input is already a curated or manually validated feature table; re-filtering may remove intentional, low-prominence features.
- Peaks were detected on individual samples rather than on a composite map; prominence filtering is most effective on composite detection where baseline and noise are aggregated.
- The analysis goal requires retention of all detectable signals including marginal peaks (e.g., rare metabolites, exposome applications where even single-sample features are important).

## Inputs

- unfiltered peak list (JSON or structured format) from composite map peak detection
- peak detection output with prominence, peak_height, SNR, and goodness_fitting (peakshape) values
- RT alignment dictionaries mapping features to sample-specific peak areas and intensities

## Outputs

- prominence-filtered peak list (subset of input)
- filtered feature table (preferred_Feature_table.tsv) with sample-wise peak areas and intensities
- row count comparison (full vs. filtered table) documenting reduction statistics

## How to apply

Load the unfiltered peak list from composite track peak detection output, which contains prominence values calculated as the height of each peak above its local baseline (computed from flanking signal). Apply a minimum prominence threshold (default ≥20% of peak height) to retain only peaks where the prominence is substantial relative to the peak's absolute intensity. This filtering leverages scipy.signal.find_peaks prominence detection, which measures vertical distance from the peak to the lowest contour line on either side. The rationale is that prominent peaks indicate true chromatographic features rather than noise artifacts. Compile the filtered peak list, map it back to individual samples via RT alignment dictionaries, and generate the filtered feature table (preferred_Feature_table.tsv). Verify that the row count reduction is appropriate by comparing the full unfiltered table (export/full_Feature_table.tsv) to the filtered output.

## Related tools

- **scipy.signal.find_peaks** (Core algorithm for prominence detection; asari wraps this to extract prominence values from each peak's local baseline context) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- **asari peaks module** (Implements peak quality filtering (SNR, peakshape, prominence thresholds) and computes noise-by-flanks to establish prominence baselines) — https://github.com/shuzhao-li/asari
- **asari peaks.compute_noise_by_flanks** (Calculates local noise level from flanking signal; used to compute prominence in context of actual baseline variability) — https://github.com/shuzhao-li/asari
- **asari peaks.stats_detect_elution_peaks** (Performs peak detection and quality filtering including prominence thresholds on mass tracks) — https://github.com/shuzhao-li/asari
- **asari peaks.evaluate_gaussian_peak_on_intensity_list** (Evaluates peak shape goodness-of-fit (peakshape metric) used in conjunction with prominence for peak quality assessment) — https://github.com/shuzhao-li/asari

## Evaluation signals

- Row count of filtered feature table is substantially lower than unfiltered table (export/full_Feature_table.tsv), confirming peaks were removed by prominence threshold.
- All retained peaks have prominence ≥ 20% of peak_height (or user-specified threshold); verify by spot-checking prominence values in filtered output.
- No sharp discontinuities in peak area distributions or RT values post-filtering; retained peaks should represent a continuous subset of quality features.
- Signal-to-noise ratio (SNR) of retained peaks is ≥2 and peak shape (goodness_fitting) is >0.5, confirming multi-criteria filtering was applied correctly.
- Biological reproducibility: features present in filtered table are consistent across replicate samples; prominent peaks should align in retention time and m/z across technical replicates.

## Limitations

- Prominence filtering is most effective on composite map detection; if applied to individual-sample detection, baseline estimates may be local and inconsistent across samples, reducing filtering efficacy.
- Default 20% prominence threshold may be too stringent for very low-abundance metabolites or sparse sample coverage; parameter tuning required for non-standard biological matrices.
- Prominence is sensitive to local baseline quality; heavily contaminated or noisy samples may produce unreliable prominence estimates, potentially filtering out valid features or retaining artifacts.
- The article notes that all peaks meeting SNR (>2) and peakshape (>0.5) standards are kept in the full feature table; prominence filtering alone does not guarantee removal of contaminants or false positives if they happen to be chromatographically prominent.

## Evidence

- [other] Apply minimum peak height threshold (default 1e5) combined with prominence requirement (≥20% of peak_height) to retain only sufficiently tall and prominent peaks.: "Apply minimum peak height threshold (default 1e5) combined with prominence requirement (≥20% of peak_height) to retain only sufficiently tall and prominent peaks."
- [methods] Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control: "Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control"
- [intro] Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing: "Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing"
- [intro] Peak detection on a composite map instead of repeated on individual samples: "Peak detection on a composite map instead of repeated on individual samples"
- [readme] All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards: "All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards"
