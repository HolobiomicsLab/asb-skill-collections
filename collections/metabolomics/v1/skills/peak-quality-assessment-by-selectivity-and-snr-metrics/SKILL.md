---
name: peak-quality-assessment-by-selectivity-and-snr-metrics
description: Use when after elution peaks have been detected on composite mass tracks using local maxima and prominence thresholds, and before mapping detected features back to individual samples or performing pre-annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0593
  tools:
  - Python
  - pymzml
  - khipu
  - JMS
  - HMDB 4
  - peaks.evaluate_gaussian_peak_on_intensity_list
  - peaks.compute_noise_by_flanks
  - peaks.__peaks_cSelectivity_stats_
  - peaks.stats_detect_elution_peaks
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- The default method uses `pymzml` to parse mzML files.
- The preannotaion is done via another package khipu (https://github.com/shuzhao-li-lab/khipu)
- The empirical compounds are searched against known compound database (default HMDB 4) via another package JMS (https://github.com/shuzhao-li/JMS).
- known compound database (default HMDB 4)
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

# peak-quality-assessment-by-selectivity-and-snr-metrics

## Summary

Evaluate detected LC-MS peaks on composite mass tracks using selectivity (mSelectivity >0.99) and signal-to-noise ratio (SNR >2) metrics alongside Gaussian peakshape quality (>0.5) to filter spurious or low-confidence features before downstream annotation. This statistical approach prioritizes high-confidence peaks while minimizing retention of noise-driven artifacts.

## When to use

After elution peaks have been detected on composite mass tracks using local maxima and prominence thresholds, and before mapping detected features back to individual samples or performing pre-annotation. Apply this skill whenever you need to distinguish genuine metabolite peaks from instrumental noise, baseline fluctuations, or co-eluting contaminants that passed initial prominence filtering.

## When NOT to use

- Input already consists of a pre-filtered feature table (e.g., preferred_Feature_table.tsv); quality assessment was already applied upstream.
- Peak detection has not yet been performed or peaks are not yet mapped to a composite mass track; apply peak detection first.
- Dataset consists of targeted peaks with known m/z and RT windows; replace mSelectivity with targeted m/z tolerance and use simplified SNR thresholds instead.

## Inputs

- composite_mass_track_with_detected_peaks (EIC intensity list with local maxima indices identified)
- peak_height_list (intensity values at candidate peak positions)
- noise_estimate_by_flanking_regions (scalar or per-peak noise level from baseline flanks)
- mass_selectivity_vector (m/z concentration metric for each peak)
- gaussian_fit_parameters (peakshape coefficient and residual from Gaussian profile evaluation)

## Outputs

- quality_filtered_peak_list (peak indices and properties passing selectivity, SNR, and peakshape thresholds)
- peak_quality_metrics_table (per-peak mSelectivity, SNR, peakshape values and binary pass/fail flags)
- rejected_peak_log (peaks failing one or more thresholds, with reason and threshold values)

## How to apply

For each detected peak on the composite mass track, compute three complementary quality metrics: (1) mSelectivity, which measures how selectively a peak is concentrated in m/z space relative to neighboring mass tracks—retain only peaks with mSelectivity >0.99; (2) SNR, calculated from the peak height and baseline noise (estimated via flanking regions using peaks.compute_noise_by_flanks)—apply threshold SNR >2; (3) peakshape, obtained via Gaussian fitting using peaks.evaluate_gaussian_peak_on_intensity_list—accept only peaks with peakshape >0.5. These three independent criteria filter peaks in sequence: first by mass selectivity (reducing m/z confusion), then by signal amplitude relative to local noise, finally by chromatographic profile regularity. Peaks meeting all three thresholds are retained for feature mapping and annotation; those failing any threshold are flagged or removed depending on downstream workflow stringency.

## Related tools

- **peaks.evaluate_gaussian_peak_on_intensity_list** (Computes peakshape coefficient via Gaussian fitting to evaluate chromatographic profile regularity; used to filter peaks with irregular or non-Gaussian shapes) — https://github.com/shuzhao-li/asari
- **peaks.compute_noise_by_flanks** (Estimates baseline noise from flanking regions on either side of a candidate peak; enables SNR calculation) — https://github.com/shuzhao-li/asari
- **peaks.__peaks_cSelectivity_stats_** (Computes m/z selectivity (mSelectivity) metric to measure peak concentration in m/z space; used to filter peaks with low m/z specificity) — https://github.com/shuzhao-li/asari
- **peaks.stats_detect_elution_peaks** (Upstream peak detection module that identifies candidate peaks on composite mass tracks; supplies peak indices and properties to quality assessment) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.peaks import evaluate_gaussian_peak_on_intensity_list, compute_noise_by_flanks; peakshape_score, _ = evaluate_gaussian_peak_on_intensity_list(intensity_list[peak_start:peak_end]); noise_level = compute_noise_by_flanks(intensity_list, peak_start, peak_end); snr = peak_height / noise_level; passed = (mSelectivity >= 0.99) and (snr >= 2) and (peakshape_score >= 0.5)
```

## Evaluation signals

- Rejected peak count and percentage: assess whether filtering removes expected proportion of noise (typically 10–30% of detected peaks depending on sample quality and MS instrument noise floor).
- mSelectivity distribution: histogram of mSelectivity values should show bimodal or left-skewed pattern with >90% of retained peaks clustered above 0.99, indicating mass resolution adequately separates co-eluting ions.
- SNR vs. annotation success: cross-validate retained peaks against downstream pre-annotation (khipu) and database matching (JMS/HMDB); retained peaks should have significantly higher match rate and lower isomer ambiguity than rejected peaks.
- Peakshape histogram: retained peaks should have peakshape distribution concentrated >0.6, with median >0.8; rejected peaks with peakshape <0.5 should correlate with irregular/asymmetric EIC profiles or baseline noise.
- Reproducibility check: re-running quality assessment on independently processed replicates of the same sample should produce >95% concordant peak sets (same peaks pass/fail thresholds), confirming threshold robustness.

## Limitations

- mSelectivity threshold (0.99) assumes high mass resolution (e.g., Q-TOF, Orbitrap); low-resolution instruments (unit mass accuracy) will have inflated mSelectivity values and require empirical recalibration.
- SNR >2 threshold is data-dependent and assumes noise is dominated by random instrumental variation; samples with high chemical background or batch-dependent contamination may require higher SNR cutoffs to suppress false positives.
- Peakshape >0.5 criterion assumes Gaussian chromatographic profiles; peaks from irregular sample matrices, unresolved isomers, or secondary ionization events may have legitimately lower peakshape scores but still represent true metabolites.
- The three metrics are applied independently without weighting or correlation adjustment; a peak failing one threshold by a narrow margin (e.g., SNR = 1.9) is rejected equally to one failing all three, potentially discarding borderline true features in noisy sample regions.
- Noise estimation by flanks assumes sufficient baseline data on both sides of a peak; peaks at chromatogram edges or in clusters of closely eluting peaks may have unreliable noise estimates, leading to inaccurate SNR.

## Evidence

- [other] Detect elution peaks on composite mass tracks using peaks.stats_detect_elution_peaks with scipy.signal.find_peaks (local maxima method), adaptive prominence (min 1/3 of min_peak_height, default 1e5), noise-based filtering, and optional detrending or smoothing; evaluate peaks with peaks.evaluate_gaussian_peak_on_intensity_list for peakshape >0.5 and SNR >2.: "evaluate peaks with peaks.evaluate_gaussian_peak_on_intensity_list for peakshape >0.5 and SNR >2"
- [other] Retain peaks with mSelectivity >0.99 and prominence >20% of peak height, then apply chromatograms.rt_lowess_calibration: "Calibrate retention time for each sample by identifying landmark peaks with mSelectivity >0.99 and prominence >20%"
- [intro] Tracking peak quality and selectivity metrics on m/z, chromatography and annotation databases: "Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases"
- [intro] Reproducible, track and backtrack between features and mass tracks (EICs): "Reproducible, track and backtrack between features and mass tracks (EICs)"
- [readme] All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards (part of input parameters but default values are fine for most people).: "All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards"
