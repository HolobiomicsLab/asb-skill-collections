---
name: eic-signal-peak-detection
description: Use when after EIC candidate generation from LC/HRMS data (mzXML, mzML, or netCDF formats), when you need to localize discrete peaks within chromatographic profiles and assign retention time boundaries, apex intensities, and quality scores prior to peak annotation or cross-sample alignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3172
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00120
  all_source_dois:
  - 10.1021/acs.jproteome.2c00120
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# EIC Signal Peak Detection

## Summary

Identifies and delineates individual peaks within extracted ion chromatograms (EICs) from LC/HRMS data by analyzing signal continuity, intensity transitions, and morphological properties. This is a critical intermediate step between EIC candidate generation and peak property quantification in untargeted metabolomics workflows.

## When to use

After EIC candidate generation from LC/HRMS data (mzXML, mzML, or netCDF formats), when you need to localize discrete peaks within chromatographic profiles and assign retention time boundaries, apex intensities, and quality scores prior to peak annotation or cross-sample alignment. Use this skill when processing population-scale untargeted studies (n > 500) where automated, reproducible peak boundary detection is required.

## When NOT to use

- Input is already a peak feature table or matrix of aligned peak heights across samples — skip directly to statistical analysis or annotation.
- EIC candidate generation step was not completed or no candidate m/z-RT windows are available.
- Data are from targeted analysis with pre-defined m/z-RT pairs; use the IPA_targeted function instead.

## Inputs

- EIC candidate profiles with m/z values, retention time ranges, and intensity arrays
- LC/HRMS raw data in mzXML, mzML, or netCDF format
- IDSL.IPA parameter spreadsheet specifying S/N thresholds, peak width bounds, and smoothing parameters

## Outputs

- Peak list with retention time start/end, m/z, apex intensity, and detection confidence score
- Peak properties including peak area, peak width, asymmetry factor, USP tailing factor, S/N ratio (baseline, xcms, and RMS methods)
- Individual peaklists in .Rdata and .csv formats

## How to apply

Load EIC candidate data containing m/z values, retention time ranges, and signal intensity profiles into the IDSL.IPA peak detection algorithm. The algorithm analyzes signal continuity and intensity transitions within each EIC to identify peak boundaries. Apply algorithm-defined quality filters including signal-to-noise ratio thresholds, peak width constraints (e.g., minimum/maximum scan width), and baseline separation criteria. Output consists of a detected peak list annotated with retention time boundaries, m/z, apex intensity, and detection confidence scores. The method employs derivative-based analysis and baseline estimation to distinguish true peaks from noise and chromatographic artifacts.

## Related tools

- **IDSL.IPA** (Implements the peak detection algorithm as part of its suite for LC/HRMS peak extraction; orchestrates EIC candidate analysis, peak boundary identification, quality filtering, and peak property calculation.) — https://github.com/idslme/IDSL.IPA
- **R** (Execution environment for IDSL.IPA package; used to load data, invoke peak detection functions, and export results.)
- **MZmine 2** (Alternative peak picking tool for comparison and validation; IDSL.IPA has demonstrated superior sensitivity, specificity, and speed.)
- **xcms** (Comparative peak picking algorithm; IDSL.IPA outperforms xcms for untargeted LC/HRMS peak detection.)

## Examples

```
library(IDSL.IPA)
IPA_workflow("Address of the IPA parameter spreadsheet")
```

## Evaluation signals

- Peak detection confidence scores are within expected range (0–1 or similar metric) and show unimodal or bimodal distribution across samples; extreme outliers may indicate parameter miscalibration.
- Detected peak widths (in scans or time units) fall within user-specified bounds (e.g., PARAM_MIN_PEAK_WIDTH to PARAM_MAX_PEAK_WIDTH); peaks outside these bounds should be rare or absent.
- Signal-to-noise ratios for detected peaks exceed the minimum S/N threshold specified in the parameter spreadsheet (e.g., S/N ≥ 3 or user-defined cutoff); peaks below threshold should be flagged or excluded.
- Peak apex intensity and area values are consistent with visual inspection of raw EIC profiles; systematic over- or under-estimation suggests baseline estimation or smoothing misconfiguration.
- Cross-batch reproducibility: detected peaks from replicate injections show ≤ 5–10% variation in retention time and m/z (after mass and RT correction), indicating stable peak boundary assignment.

## Limitations

- Peak detection quality depends critically on parameter tuning (peak width bounds, S/N thresholds, smoothing windows); population-specific data require pilot parameter optimization.
- Overlapping or coeluting peaks may not be resolved as separate peaks; the algorithm assumes baseline separation unless ion pairing or isotope criteria are applied.
- Retention time drift across a batch can cause peak boundary inconsistency if not corrected before detection; IDSL.IPA includes retention time correction as a downstream step but not integrated into peak detection itself.
- Noisy or low-intensity EICs with S/N < threshold will not yield detected peaks; true but weak signals may be missed if S/N parameter is set too stringently.
- Peak detection does not perform compound annotation; m/z-RT pairs must be matched to reference libraries or molecular formula tools (e.g., IDSL.UFA, IDSL.UFAx) in downstream steps.

## Evidence

- [other] EIC candidate data input specification: "Load EIC candidate data (m/z values, retention time ranges, and signal intensity profiles) into R."
- [other] Peak detection algorithm and quality filtering: "Apply the IDSL.IPA peak detection algorithm to identify peaks within each EIC candidate by analyzing signal continuity and intensity transitions. Filter detected peaks according to algorithm-defined"
- [other] Peak detection output specification: "Output detected peak list with retention time, m/z, peak apex intensity, and detection confidence scores."
- [readme] Workflow position and scope: "IDSL.IPA is a suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction"
- [readme] Peak property calculation scope: "Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R13C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor, skewness"
- [readme] Comparative performance: "IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, xcms, and MS-DIAL in terms of sensitivity, specificity and speed."
