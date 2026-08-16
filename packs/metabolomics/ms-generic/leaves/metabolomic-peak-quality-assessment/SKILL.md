---
name: metabolomic-peak-quality-assessment
description: Use when after peak detection in untargeted LC/HRMS workflows, when you have a list of candidate peaks with signal intensity profiles and need to filter them according to data quality thresholds (signal-to-noise ratio, peak width, baseline separation, and isotopic pairing consistency) before.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - IDSL.IPA
  - R
  - IDSL.UFA
  - IDSL.CSA
  techniques:
  - mass-spectrometry
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00120
  all_source_dois:
  - 10.1021/acs.jproteome.2c00120
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-peak-quality-assessment

## Summary

Evaluate detected peaks from LC/HRMS data using quantitative chromatographic properties and signal quality metrics to filter peaks meeting sensitivity, specificity, and reproducibility standards. This skill ensures high-confidence peak lists suitable for population-scale untargeted metabolomics studies.

## When to use

After peak detection in untargeted LC/HRMS workflows, when you have a list of candidate peaks with signal intensity profiles and need to filter them according to data quality thresholds (signal-to-noise ratio, peak width, baseline separation, and isotopic pairing consistency) before downstream alignment and annotation.

## When NOT to use

- Input peaks already pass through a different peak quality filter (e.g., from MZmine 2 or xcms vendor workflow) — applying IDSL.IPA's evaluation may introduce redundant or conflicting quality criteria.
- Data are targeted analysis with pre-defined m/z-RT pairs — use IDSL.IPA's IPA_targeted function instead of the full EIC-to-peak-detection-to-evaluation pipeline.
- Chromatographic method or instrument differs substantially from supported formats (mzXML, mzML, netCDF) or produces atypical peak shapes for which published metric thresholds do not apply.

## Inputs

- Detected peak list (retention time, m/z, apex intensity, detection confidence scores)
- EIC signal intensity profiles (continuity and intensity transitions per candidate)
- Mass spectrometry acquisition parameters (scan rate, baseline noise estimate)

## Outputs

- Filtered peak list with retention time, m/z, peak area, and 19 computed chromatographic properties
- Quality assessment report with per-peak metrics (S/N, peak width, asymmetry, gaussianity, nIsoPair)
- Gap-filled peak height tables and pairwise correlation lists for adduct/fragment detection

## How to apply

Apply IDSL.IPA's peak property evaluation algorithm to compute 19 chromatographic metrics per detected peak, including signal-to-noise ratio (using baseline, xcms, or RMS methods), peak width, asymmetry factor, USP tailing factor, gaussianity, and nIsoPair/RCS for isotopic coherence. Define cutoff thresholds for each metric based on your chromatographic method and mass spectrometry platform (e.g., S/N > baseline threshold, peak width within expected range, tailing factor near 1.0 for symmetric peaks). Filter retained peaks by applying these thresholds sequentially; peaks failing any criterion are excluded. Rationale: multi-dimensional quality filtering reduces false positives and improves alignment reliability across population-size studies by selecting only peaks with good peak shape, sufficient signal above noise, and consistent isotopic signatures.

## Related tools

- **IDSL.IPA** (Implements peak property evaluation, calculates 19 chromatographic metrics, applies quality filtering thresholds, and outputs filtered peak lists with confidence scores) — https://github.com/idslme/IDSL.IPA
- **R** (Execution environment for IDSL.IPA package and statistical analysis of peak quality metrics)
- **IDSL.UFA** (Downstream molecular formula annotation tool integrated with IDSL.IPA filtered peak lists) — https://github.com/idslme/IDSL.UFA
- **IDSL.CSA** (Composite spectra generation by clustering recurring ions from quality-filtered peaks) — https://github.com/idslme/IDSL.CSA

## Examples

```
library(IDSL.IPA)
IPA_workflow("path/to/IPA_parameters.xlsx")
```

## Evaluation signals

- Filtered peak list row count < input candidate count; verify that exclusion rate is consistent with thresholds applied (e.g., typical metabolomics studies report 50–80% retention after quality filtering).
- All retained peaks have S/N ≥ specified baseline threshold and peak width within biologically plausible range (e.g., 0.01–2 min for typical LC methods).
- Asymmetry factor and USP tailing factor values cluster near 1.0 for retained peaks; heavily tailed or fronted peaks are excluded or flagged.
- nIsoPair and RCS metrics confirm isotopic coherence (e.g., ¹³C isotologues detected with expected mass offset and intensity ratio ≈ 1.1× per carbon).
- Peaks retained after filtering show improved alignment consistency and reduced false positives in downstream cross-sample peak alignment compared to unfiltered candidate list.

## Limitations

- Peak quality metric thresholds are tunable but require instrument-specific calibration; default parameters in IPA_parameters.xlsx may not generalize to all LC/HRMS platforms or chromatographic methods.
- Highly overlapping or co-eluting peaks may be incorrectly flagged as poor quality even if biologically relevant; visual inspection or targeted EIC review recommended for borderline cases.
- S/N calculation methods (baseline, xcms, RMS) yield different results; consistent method choice must be specified in PARAM configuration and documented.
- The 19-metric evaluation assumes standard metabolite mass range and peak shape; atypical compounds (very lipophilic, highly charged, or fragile metabolites) may not meet published thresholds.
- No built-in changelog documented; version-to-version threshold or metric changes may not be transparent.

## Evidence

- [readme] Peak property evaluation algorithm with 19 metrics: "Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R13C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor, skewness"
- [intro] Position and function in workflow: "algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation"
- [other] Quality filtering based on signal-to-noise and peak width: "Filter detected peaks according to algorithm-defined quality criteria (signal-to-noise ratio, peak width constraints, baseline separation)."
- [other] Output includes confidence scores: "Output detected peak list with retention time, m/z, peak apex intensity, and detection confidence scores."
- [readme] Population-scale application and performance: "IDSL.IPA generates comprehensive and high-quality datasets from untargeted analysis of organic small molecules for population-size studies."
- [readme] S/N definition variants: "Definition of Signal to Noise ratio (S/N)"
