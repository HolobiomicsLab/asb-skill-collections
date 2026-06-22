---
name: chromatographic-baseline-estimation
description: Use when you have extracted ion chromatogram (EIC) candidate data from untargeted LC/HRMS files (mzXML, mzML, or netCDF format) and need to identify genuine peaks within each EIC.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - IDSL.IPA
  - R
  - MZmine 2
  - xcms
derived_from:
- doi: 10.1021/acs.jproteome.2c00120
  title: IDSL.IPA
evidence_spans:
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight R package'
- light-weight R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_ipa_cq
    doi: 10.1021/acs.jproteome.2c00120
    title: IDSL.IPA
  dedup_kept_from: coll_idsl_ipa_cq
schema_version: 0.2.0
---

# chromatographic-baseline-estimation

## Summary

Estimation of the baseline signal intensity in LC/HRMS chromatograms to enable accurate peak detection and signal-to-noise ratio calculation. This is a prerequisite step in the IDSL.IPA peak detection workflow that distinguishes genuine peaks from noise by establishing a noise floor reference.

## When to use

Apply this skill when you have extracted ion chromatogram (EIC) candidate data from untargeted LC/HRMS files (mzXML, mzML, or netCDF format) and need to identify genuine peaks within each EIC. Baseline estimation is necessary before peak detection and quality filtering can proceed, particularly in population-scale studies (n > 500) where consistent, automated baseline estimation is critical.

## When NOT to use

- Input is already a feature table or aligned peak matrix — baseline estimation applies only to raw or minimally processed EIC signals.
- Data has already undergone noise reduction or signal smoothing by another tool (e.g., Savitzky-Golay filtering) — re-estimating baseline may introduce redundancy or conflict.
- Target m/z and retention time values are already known with high confidence — use targeted peak extraction (IPA_targeted function) instead.

## Inputs

- Extracted ion chromatogram (EIC) candidate data: m/z values, retention time ranges, and signal intensity profiles from LC/HRMS data
- EIC signal intensity time-series from a single m/z and retention time window

## Outputs

- Estimated baseline signal intensity profile aligned with EIC retention time axis
- Signal-to-noise ratio (S/N) values for downstream peak quality filtering
- Baseline-corrected peak intensity values

## How to apply

Within the IDSL.IPA workflow, baseline estimation operates on the signal intensity profile of each EIC candidate after EIC candidate generation. The algorithm analyzes the signal continuity and intensity transitions across the retention time range to establish a noise floor. This baseline is then used to calculate signal-to-noise ratio (S/N) and apply quality criteria such as minimum S/N thresholds and baseline separation requirements. The baseline estimation must be completed before peak apex detection and peak width constraints can be meaningfully applied, as these metrics depend on knowing the baseline noise level.

## Related tools

- **IDSL.IPA** (R package implementing the complete peak detection suite including baseline estimation as a sequential step after EIC candidate generation) — https://github.com/idslme/IDSL.IPA
- **R** (Runtime environment for executing IDSL.IPA baseline estimation and downstream peak detection algorithms)
- **MZmine 2** (Comparative peak picking tool; IDSL.IPA baseline and peak detection outperforms this tool)
- **xcms** (Comparative peak picking tool; IDSL.IPA baseline and peak detection outperforms this tool; also provides alternative S/N calculation method)

## Examples

```
library(IDSL.IPA); IPA_workflow("Address of the IPA parameter spreadsheet")
```

## Evaluation signals

- Detected peaks have baseline-corrected intensities that are positive and greater than zero, with apex intensity >> baseline level
- Signal-to-noise ratio values computed from the baseline estimate are consistent with manual inspection of chromatographic traces and reflect genuine peak vs. noise discrimination
- Peaks that pass baseline-derived S/N thresholds are subsequently retained after downstream filtering; peaks below threshold are rejected
- Baseline-corrected peak widths and retention times fall within algorithm-defined quality criteria (peak width constraints, baseline separation requirements)
- Comparison of peaklists from IDSL.IPA against MZmine 2 or xcms shows improved sensitivity and specificity due to robust baseline estimation

## Limitations

- Baseline estimation assumes signal intensity noise is reasonably uniform or slowly varying across the retention time range; steep baseline slopes or strong background gradients may reduce accuracy
- Algorithm performance depends on appropriate parameter tuning via the IPA parameter spreadsheet; default parameters may not suit all chromatographic methods or sample matrices
- Large-scale population studies (n > 500) require parallel processing configuration; single-threaded baseline estimation on many files is computationally intensive
- Baseline estimation is sensitive to the quality of the input EIC candidate data; poorly generated EIC candidates (e.g., off-target m/z windows) will yield unreliable baselines

## Evidence

- [readme] algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation: "algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation"
- [other] Apply the IDSL.IPA peak detection algorithm to identify peaks within each EIC candidate by analyzing signal continuity and intensity transitions: "Apply the IDSL.IPA peak detection algorithm to identify peaks within each EIC candidate by analyzing signal continuity and intensity transitions"
- [other] Filter detected peaks according to algorithm-defined quality criteria (signal-to-noise ratio, peak width constraints, baseline separation): "Filter detected peaks according to algorithm-defined quality criteria (signal-to-noise ratio, peak width constraints, baseline separation)"
- [readme] S/N using baseline, S/N using the xcms method, S/N using the RMS method: "S/N using baseline, S/N using the xcms method, S/N using the RMS method"
- [readme] IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, xcms, and MS-DIAL in terms of sensitivity, specificity and speed: "IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, xcms, and MS-DIAL in terms of sensitivity, specificity and speed"
