---
name: quality-control-metric-distribution-analysis
description: Use when after composite-map peak detection has produced an unfiltered peak list with SNR, peakshape (goodness_fitting), peak_height, and prominence values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - asari peaks module
  - scipy.signal.find_peaks
  - Python (pandas, numpy, matplotlib)
  - JMS (Json's Metabolite Services)
  techniques:
  - LC-MS
  - GC-MS
  - direct-infusion-MS
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

# quality-control-metric-distribution-analysis

## Summary

Analyze the distribution and selectivity of peak quality metrics (SNR, peak shape goodness-of-fit, peak height, prominence) across detected features to assess filtering efficacy and inform threshold tuning in LC-MS metabolomics workflows. This skill validates that peak filtering reduces false positives while retaining signal-rich features.

## When to use

After composite-map peak detection has produced an unfiltered peak list with SNR, peakshape (goodness_fitting), peak_height, and prominence values. Use this skill to quantify how many features are retained or rejected under candidate threshold combinations, and to inspect metric distributions for anomalies or bimodality that suggest misalignment or contamination. Critical before committing to a final feature table when baseline thresholds (SNR > 2, goodness_fitting > 0.5, peak_height ≥ 1e5 with ≥20% prominence) may not suit your instrument or sample type.

## When NOT to use

- Input is already a filtered feature table or post-hoc statistical comparison table; re-filtering risks losing reproducibility.
- Peak detection has not yet been performed or the unfiltered peak list lacks SNR, peakshape, peak_height, or prominence annotations.
- The analysis goal is rapid feature prioritization rather than comprehensive QC; use simpler single-threshold ranking instead.
- Sample metadata or RT alignment is not available to map peaks back to individual samples for verification.

## Inputs

- Unfiltered peak list (JSON or TSV) from asari composite map peak detection with columns: id, m/z, retention_time, SNR, goodness_fitting (peakshape), peak_height, prominence, scan_index
- Sample metadata or RT alignment dictionary mapping peaks to individual samples
- Optional: project configuration with candidate threshold values (SNR_min, goodness_fit_min, peak_height_min, prominence_fraction_min)

## Outputs

- Quality control report (TSV or JSON) with counts of peaks passing each filter stage
- Distribution plots (histograms, box plots, or violin plots) of SNR, goodness_fitting, peak_height, and prominence across all peaks and per sample
- Filtered feature table (preferred_Feature_table.tsv) with peak area intensity values for peaks passing all thresholds
- Audit log documenting threshold values, rejection counts, and any anomalies (e.g., samples with >95% peak rejection)

## How to apply

Load the full unfiltered peak list (JSON or structured format) from composite track peak detection output, extract SNR, goodness_fitting, peak_height, and prominence columns, and generate histograms, box plots, or cumulative distribution functions for each metric. Apply sequential filtering thresholds (SNR > 2 → goodness_fitting > 0.5 → peak_height ≥ 1e5 AND prominence ≥ 20% of peak_height) and count retained vs. rejected peaks at each step. Visualize metric distributions before and after filtering to confirm that thresholds remove low-quality outliers without excessive loss of valid signal. Validate that the filtered peak list maps correctly back to individual samples via RT alignment dictionaries and that sample-specific peak areas are non-negative and fall within expected intensity ranges. Document the row count reduction (e.g., 'unfiltered: 50,000 peaks → filtered: 8,500 peaks') and flag any samples or m/z ranges with unexpectedly high rejection rates as potential quality issues.

## Related tools

- **asari peaks module** (Implements peak quality filtering functions (SNR, goodness_fitting, peak_height, prominence thresholds) and audit_mass_track, stats_detect_elution_peaks, evaluate_gaussian_peak_on_intensity_list, and compute_noise_by_flanks for metric calculation) — https://github.com/shuzhao-li/asari
- **scipy.signal.find_peaks** (Underlying peak detection algorithm using local maxima and prominence control; metrics are computed on detected peaks)
- **Python (pandas, numpy, matplotlib)** (Data loading, filtering, aggregation, and visualization of metric distributions across peaks and samples)
- **JMS (Json's Metabolite Services)** (Provides reusable data structures for peaks and indexed data stores to standardize metric representation and lookups) — https://github.com/metabolomics-cloud/JMS

## Examples

```
python3 -c "import asari; peaks = asari.io.load_json('composite_peaks.json'); filtered = [p for p in peaks if p['SNR'] > 2 and p['goodness_fitting'] > 0.5 and p['peak_height'] >= 1e5 and p['prominence'] >= 0.2 * p['peak_height']]; print(f'Unfiltered: {len(peaks)}, Filtered: {len(filtered)}, Reduction: {100*(1-len(filtered)/len(peaks)):.1f}%')"
```

## Evaluation signals

- Row count reduction is monotonic and proportional to thresholds: applying SNR > 2 reduces count, then goodness_fitting > 0.5 reduces further, then peak_height and prominence filters reduce further. Total reduction should be 50–90% depending on sample quality.
- SNR, goodness_fitting, peak_height, and prominence distributions are non-bimodal (single peak) after filtering and do not show long left-tail outliers, indicating good instrument calibration and alignment.
- Filtered peak areas and intensities are non-negative, fall within expected dynamic range (e.g., 1e5 to 1e9 for high-resolution MS), and show no NaN or inf values.
- Sample-specific peak area matrices map correctly: all peaks in the filtered feature table appear in at least one sample with a valid retention time and m/z, and row/column counts match documented sample and feature counts.
- Audit log confirms that no more than 5–10% of samples have >95% peak rejection; >10% rejection in any sample suggests systematic drift, contamination, or miscalibration requiring investigation.

## Limitations

- Default thresholds (SNR > 2, goodness_fitting > 0.5, peak_height ≥ 1e5, prominence ≥ 20%) are tuned for typical LC-MS metabolomics instruments and may require adjustment for GC-MS, DI-MS, or high-noise environments.
- Peak height and prominence are absolute metrics; they may not translate across instruments with different ionization efficiency or detector gain. Relative metrics (e.g., SNR, goodness_fitting) are more transferable.
- Goodness_fitting (peakshape) assumes Gaussian-like peaks; co-elution or peak tailing can inflate false rejections. Visual inspection of chromatograms for borderline peaks is recommended.
- Filtering is applied uniformly across all m/z and RT ranges; biologically rare features (e.g., low-abundance lipids) may be disproportionately filtered if they naturally have lower SNR or peak height. Sample-specific or class-specific thresholds may be needed.
- Missing signals: No guidance on how to handle or visualize peaks with missing metric values (e.g., single-scan peaks where prominence is undefined).

## Evidence

- [other] Apply SNR threshold filter (SNR > 2) to retain only peaks with sufficient signal-to-noise ratio.: "Apply SNR threshold filter (SNR > 2) to retain only peaks with sufficient signal-to-noise ratio."
- [other] Apply peakshape threshold filter (goodness_fitting > 0.5) using gaussian peak evaluation to retain well-shaped peaks.: "Apply peakshape threshold filter (goodness_fitting > 0.5) using gaussian peak evaluation to retain well-shaped peaks."
- [other] Apply minimum peak height threshold (default 1e5) combined with prominence requirement (≥20% of peak_height) to retain only sufficiently tall and prominent peaks.: "Apply minimum peak height threshold (default 1e5) combined with prominence requirement (≥20% of peak_height) to retain only sufficiently tall and prominent peaks."
- [intro] Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases: "Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases"
- [readme] All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards (part of input parameters but default values are fine for most people).: "All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards (part of input parameters but default values are fine for most people)."
- [other] Count rows in both full and filtered tables and confirm row count reduction is appropriate relative to the unfiltered reference.: "Count rows in both full and filtered tables and confirm row count reduction is appropriate relative to the unfiltered reference."
