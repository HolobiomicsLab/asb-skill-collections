---
name: gaussian-peak-shape-evaluation
description: Use when after peak detection on a composite mass track has identified
  candidate peaks in a mass chromatogram, and before compiling the final feature table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - asari peaks module
  - scipy.signal.find_peaks
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- See [peaks.evaluate_gaussian_peak_on_intensity_list](peaks.evaluate_gaussian_peak_on_intensity_list),
  [peaks.__peaks_cSelectivity_stats_](peaks.__peaks_cSelectivity_stats_),
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

# Gaussian Peak Shape Evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantifies the goodness-of-fit of detected LC-MS peaks to a Gaussian model to filter out poorly shaped peaks and retain high-quality features. This metric serves as one of three orthogonal quality thresholds (alongside SNR and prominence) in asari's peak quality filtering pipeline.

## When to use

After peak detection on a composite mass track has identified candidate peaks in a mass chromatogram, and before compiling the final feature table. Apply this skill when you need to remove peaks with asymmetric, bimodal, or otherwise non-Gaussian elution profiles that may indicate co-elution, baseline noise, or instrumental artifacts rather than true analyte signals.

## When NOT to use

- Input peaks are already known to be high-quality standards or reference compounds (skip Gaussian evaluation and use direct intensity matching).
- Data are from GC-MS workflows where peak shape expectations differ from LC-MS Gaussian assumptions; alternative shape models may be required.
- Peak detection has not yet been performed; this skill applies only after candidate peaks have been identified, not during initial m/z binning or mass track construction.

## Inputs

- Composite map peak detection output (JSON or structured format) containing candidate peaks with m/z, retention time, intensity array, peak height, SNR, and prominence
- Detected peak intensity list (array of intensity values across scan range for single peak)

## Outputs

- Goodness-of-fit score (numeric, range 0–1 or similar correlation metric) per peak
- Binary pass/fail classification for each peak (goodness_fitting > 0.5)
- Filtered peak list subset passed to feature table compilation

## How to apply

Extract intensity values from the detected peak region (typically 5–10 scan points around the apex) for each candidate peak. Fit a Gaussian curve (via least-squares optimization or similar) to the intensity array and compute the goodness-of-fit metric (R² or similar correlation coefficient). Retain only peaks where goodness_fitting > 0.5 (default threshold). This threshold balances rejection of severely deformed peaks against over-filtering of realistic chromatographic variation. Combine this filter with parallel SNR (>2) and peak height/prominence thresholds; a peak must pass all three to enter the final feature table. The rationale is that Gaussian peaks indicate clean analyte elution, while non-Gaussian profiles suggest contamination or interference.

## Related tools

- **asari peaks module** (Implements evaluate_gaussian_peak_on_intensity_list() function to fit Gaussian curve and compute goodness-of-fit metric on intensity arrays) — https://github.com/shuzhao-li/asari
- **scipy.signal.find_peaks** (Detects local maxima and prominence on mass tracks prior to Gaussian shape evaluation; provides candidate peaks and prominence values passed to shape filter)

## Examples

```
from asari.peaks import evaluate_gaussian_peak_on_intensity_list; goodness = evaluate_gaussian_peak_on_intensity_list(intensity_array); peak_passes = goodness > 0.5
```

## Evaluation signals

- Goodness-of-fit scores for all peaks are in the valid range (0–1 or correlation coefficient bounds); no NaN or inf values.
- Peak count after shape filter is consistent with expected reduction (typically 20–50% of unfiltered peaks depending on sample complexity and instrument calibration).
- Peaks below goodness_fitting threshold show visibly asymmetric or multi-modal intensity profiles when plotted; peaks above threshold are unimodal Gaussian-like.
- Row count reduction from full_Feature_table.tsv (unfiltered) to preferred_Feature_table.tsv (filtered with SNR, shape, and height thresholds) is proportional and documented in project output.
- Manually inspected mass tracks (via dashboard or export) for a sample of rejected and retained peaks confirm that retained peaks have cleaner, more symmetric elution profiles.

## Limitations

- Goodness-of-fit threshold (0.5) is a fixed default and may not generalize across different LC instruments, columns, or flow rates where peak broadness and shape vary naturally.
- Peaks with shouldering or multiplet structure due to true co-elution (e.g., isomers) may fail the Gaussian filter even though they represent real analytes; no automatic distinction between instrumental artifact and biological co-elution is made.
- Very narrow peaks (single or few scans) may have high apparent goodness-of-fit by chance; this skill does not enforce minimum peak width, relying instead on the minimum peak height and prominence filters to exclude noise spikes.
- The Gaussian model assumes symmetric, unimodal peaks and does not account for tailing or fronting common in reversed-phase LC; alternative shape models may be needed for specialized chromatography modes.

## Evidence

- [other] Apply peakshape threshold filter (goodness_fitting > 0.5) using gaussian peak evaluation to retain well-shaped peaks.: "Apply peakshape threshold filter (goodness_fitting > 0.5) using gaussian peak evaluation to retain well-shaped peaks."
- [methods] See [peaks.evaluate_gaussian_peak_on_intensity_list](peaks.evaluate_gaussian_peak_on_intensity_list): "See [peaks.evaluate_gaussian_peak_on_intensity_list](peaks.evaluate_gaussian_peak_on_intensity_list)"
- [other] Asari applies peak quality filtering by tracking selectivity metrics on m/z, chromatography, and annotation databases to refine detected features after composite map peak detection.: "Asari applies peak quality filtering by tracking selectivity metrics on m/z, chromatography, and annotation databases to refine detected features after composite map peak detection."
- [readme] All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards: "All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards"
- [intro] Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing: "Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing"
