---
name: snr-based-signal-validation
description: Use when after composite map peak detection has generated a full unfiltered peak list with SNR values computed for each candidate peak.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - scipy.signal.find_peaks
  - asari peaks module
  - compute_noise_by_flanks
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control
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
---

# SNR-based signal validation

## Summary

Filters detected LC-MS peaks by applying a signal-to-noise ratio (SNR > 2) threshold to retain only peaks with sufficient signal separation from background noise. This is a foundational selectivity step in the asari peak quality pipeline that reduces false positive features before downstream filtering on peak shape and height.

## When to use

Apply this skill after composite map peak detection has generated a full unfiltered peak list with SNR values computed for each candidate peak. Use it as the first selectivity gate when you need to remove low-confidence peaks driven by noise, particularly before applying stricter shape and prominence thresholds. It is most appropriate when processing high-resolution LC-MS data where SNR can be reliably estimated from intensity flanks.

## When NOT to use

- Input is already a final feature table (preferred_Feature_table.tsv or equivalent) — SNR filtering is a raw peak processing step, not a post-hoc feature refinement step.
- SNR values are not available or reliably computed in the peak list — the filter requires valid SNR metadata for each peak.
- The analysis goal is to maximize sensitivity and retain all possible weak signals — SNR > 2 is a conservative threshold that intentionally removes noise-driven peaks, which may not suit ultra-sensitive discovery applications.

## Inputs

- Full unfiltered peak list in JSON or tabular format from composite map peak detection
- Peak-level metadata including SNR (signal-to-noise ratio) and intensity values for each candidate peak
- Computed noise estimates (from flanking regions around each peak)

## Outputs

- SNR-filtered peak list (JSON or tabular) retaining only peaks with SNR > 2
- Row count reduction report (full vs. filtered peak counts) documenting selectivity

## How to apply

Load the full unfiltered peak list (JSON or structured tabular format) output from composite track peak detection, which must contain SNR values for each detected peak. Apply a threshold filter retaining only peaks where SNR > 2, removing all peaks that fall below this cutoff. The SNR threshold of 2 reflects a pragmatic balance: it removes noise-driven false positives while retaining genuine weak signals. This filtering step leverages the `compute_noise_by_flanks` function to estimate local baseline noise from intensity values adjacent to each peak, allowing SNR to be computed as the ratio of peak intensity to flanking noise. After SNR filtering, the remaining peak list is passed to subsequent quality filters (peak shape goodness-of-fit and peak height/prominence thresholds) to progressively refine feature quality. Document the count of peaks retained at this stage to confirm signal filtering is appropriate relative to the unfiltered reference.

## Related tools

- **asari peaks module** (Implements SNR calculation via compute_noise_by_flanks and applies SNR filtering as part of the peak quality selectivity pipeline) — https://github.com/shuzhao-li/asari
- **scipy.signal.find_peaks** (Underlying local maxima detection with prominence control that precedes SNR filtering) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- **compute_noise_by_flanks** (Computes local baseline noise estimates from intensity values flanking each peak, enabling SNR calculation) — https://github.com/shuzhao-li/asari

## Evaluation signals

- Peak count after SNR filtering is lower than the unfiltered peak count; validate that row count reduction is proportional to expected false positive rate in the input data.
- All retained peaks have SNR ≥ 2.0; spot-check a sample of filtered peaks to confirm SNR metadata meets threshold.
- SNR distribution statistics (median, min, max) of filtered peaks show expected shift toward higher SNR relative to full peak list.
- Downstream peak shape and height filters process the SNR-filtered list without encountering missing or anomalous SNR values.
- Final feature table row count aligns with expected feature count given the input sample complexity and instrument resolution.

## Limitations

- SNR > 2 is a fixed, global threshold that does not adapt to sample-specific noise levels, matrix effects, or ion suppression. Challenging matrices may require per-ion or per-sample SNR calibration.
- SNR estimation via flanking intensity assumes stable baseline noise; peaks near chromatographic interferences or with skewed peak shapes may have biased noise estimates.
- The threshold is tuned for centroid mzML data at high mass resolution; conversion or preprocessing artifacts may invalidate SNR estimates.
- This filter is applied before composite map assembly across samples, so it cannot leverage cross-sample abundance patterns to disambiguate noise from true low-intensity signals present in only a few samples.

## Evidence

- [other] Apply SNR threshold filter (SNR > 2) to retain only peaks with sufficient signal-to-noise ratio.: "Apply SNR threshold filter (SNR > 2) to retain only peaks with sufficient signal-to-noise ratio."
- [other] Asari applies peak quality filtering by tracking selectivity metrics on m/z, chromatography, and annotation databases to refine detected features after composite map peak detection.: "Asari applies peak quality filtering by tracking selectivity metrics on m/z, chromatography, and annotation databases to refine detected features after composite map peak detection."
- [readme] All peaks are kept in export/full_Feature_table.tsv if they meet signal (snr) and shape standards (part of input parameters but default values are fine for most people).: "All peaks are kept in export/full_Feature_table.tsv if they meet signal (snr) and shape standards (part of input parameters but default values are fine for most people)."
- [methods] Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control: "Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control"
- [methods] See peaks.compute_noise_by_flanks: "See [peaks.compute_noise_by_flanks](peaks.compute_noise_by_flanks)."
