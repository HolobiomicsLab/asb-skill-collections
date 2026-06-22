---
name: retention-time-calibration-via-lowess-regression
description: Use when after mass track extraction and alignment across samples, when preparing to detect elution peaks on composite mass tracks. Use this when inter-sample retention time variation exceeds acceptable alignment tolerance (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pymzml
  - khipu
  - JMS
  - HMDB 4
  - chromatograms.rt_lowess_calibration
  - peaks.quick_detect_unique_elution_peak
  - scipy.signal (implied)
  - asari workflow module
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

# retention-time-calibration-via-lowess-regression

## Summary

A statistically guided approach to correct sample-level retention time drift in LC-MS metabolomics by identifying high-confidence landmark peaks and applying LOWESS (locally weighted scatterplot smoothing) regression with boundary extension. This ensures consistent peak alignment across samples before composite feature detection.

## When to use

After mass track extraction and alignment across samples, when preparing to detect elution peaks on composite mass tracks. Use this when inter-sample retention time variation exceeds acceptable alignment tolerance (e.g., >10–15 seconds in typical LC-MS), which is detected by observing that the same mass track exhibits multiple distinct elution profiles across samples rather than a single coherent peak.

## When NOT to use

- Input data are already RT-corrected or come from a single-sample analysis where cross-sample alignment is not needed.
- Landmark peaks with mSelectivity <0.99 or prominence <20% of peak height are predominant; calibration will be unstable.
- Retention time variation is <5 ppm or within expected instrument precision; calibration overhead outweighs benefit.

## Inputs

- list of mass tracks per sample (output from chromatograms.extract_massTracks_)
- per-sample MS1 spectra intensity and retention time data
- mSelectivity and peak prominence metrics for each candidate landmark peak
- sample list and run metadata

## Outputs

- rt_cal_dict: dictionary of retention time calibration parameters per sample
- RT-corrected mass tracks per sample (updated retention times for all peaks)
- calibration quality report (LOWESS curve fit, landmark peaks used, residual statistics)

## How to apply

First, identify landmark peaks on each sample's mass tracks by filtering for selectivity (mSelectivity >0.99, indicating the peak is present in only one sample or has minimal ambiguity) and prominence (>20% of peak height). These landmarks serve as internal reference points with high confidence. Next, apply chromatograms.rt_lowess_calibration with 10% boundary extension to generate a per-sample retention time calibration dictionary (rt_cal_dict). The LOWESS approach locally estimates the relationship between observed and expected retention times across the set of landmark peaks, smoothing non-linear drift while preserving genuine peak shape variation. The boundary extension ensures that peaks near the start and end of the chromatogram are also corrected. Finally, apply this rt_cal_dict to all detected peaks in that sample before aggregating intensities across samples into composite mass tracks.

## Related tools

- **chromatograms.rt_lowess_calibration** (Applies LOWESS-based retention time correction to a single sample using identified landmark peaks and 10% boundary extension) — https://github.com/shuzhao-li/asari
- **peaks.quick_detect_unique_elution_peak** (Identifies potential landmark peaks with high selectivity and prominence for use as calibration anchors) — https://github.com/shuzhao-li/asari
- **scipy.signal (implied)** (Underlying signal processing for LOWESS smoothing and peak prominence evaluation)
- **asari workflow module** (Orchestrates RT calibration step within the overall LC-MS processing pipeline) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.chromatograms import rt_lowess_calibration; rt_cal_dict = rt_lowess_calibration(sample_mass_tracks, landmark_peaks_mz_rt, boundary_extension=0.1)
```

## Evaluation signals

- Landmark peak mSelectivity ≥0.99 and prominence ≥20% of peak height; check that sufficient landmarks (typically ≥5–10) were identified per sample.
- LOWESS curve fit residuals should show no systematic bias across the retention time range; plot observed vs. fitted RT to inspect for non-linearity.
- After RT calibration, the same mass track should display a single, coherent elution profile when visualized across all samples, with peak retention times clustering within 10–20 seconds.
- Composite map peak detection should recover the same features (m/z, RT) across replicates; compare preferred_Feature_table.tsv entries before and after calibration for consistent peak counts and alignment.
- Validate calibration on known standards (if available in the dataset); their retention times should shift by <1 minute and show consistent ordering across samples.

## Limitations

- Requires sufficient high-quality landmark peaks (mSelectivity >0.99) in each sample; samples with poor peak quality or atypical chromatograms may have unstable calibration.
- LOWESS regression assumes a smooth, non-parametric relationship between observed and expected RT; highly non-linear or multi-modal drift patterns may not be fully corrected.
- Calibration is performed independently per sample; systematic instrument drift across the entire batch is not corrected (batch-level RT alignment is a separate step).
- 10% boundary extension may introduce artifacts if landmarks cluster near the chromatogram edges; sparse landmark distribution can lead to extrapolation errors.

## Evidence

- [methods] identify landmark peaks with mSelectivity >0.99 and prominence >20% of peak height, then apply chromatograms.rt_lowess_calibration with 10% boundary extension to obtain per-sample rt_cal_dict: "identify landmark peaks with mSelectivity >0.99 and prominence >20% of peak height, then apply chromatograms.rt_lowess_calibration with 10% boundary extension to obtain per-sample rt_cal_dict"
- [methods] See [chromatograms.rt_lowess_calibration](chromatograms.rt_lowess_calibration): "See [chromatograms.rt_lowess_calibration](chromatograms.rt_lowess_calibration)"
- [methods] Build composite mass tracks by summing aligned intensity values across all samples after RT calibration.: "Build composite mass tracks by summing aligned intensity values across all samples after RT calibration"
