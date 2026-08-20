---
name: noise-threshold-filtering-spectral-data
description: Use when working with raw IM-MS data (Agilent MassHunter .d or UIMF format) that contains low-abundance background noise, isolated high-intensity artifacts, or jagged peaks characteristic of low-abundance ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - .NET Framework 4.7.2
  - Microsoft Visual C++ Runtime x64
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/jasms.4c00220
  title: PNNL PreProcessor
- doi: 10.1021/acs.jproteome.1c00425
  title: ''
evidence_spans:
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files) from drift tube (DT) and structure for lossless ion manipulations (SLIM) IM-MS
- Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files)
- Agilent MassHunter (.d) and UIMF mass spectrometry data files
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pnnl_preprocessor_cq
    doi: 10.1021/jasms.4c00220
    title: PNNL PreProcessor
  dedup_kept_from: coll_pnnl_preprocessor_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00220
  all_source_dois:
  - 10.1021/jasms.4c00220
  - 10.1021/acs.jproteome.1c00425
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# noise-threshold-filtering-spectral-data

## Summary

Remove low-intensity noise and spike artifacts from ion mobility–mass spectrometry (IM-MS) data by applying intensity thresholds and spike detection algorithms. This preprocessing step enhances signal quality and reduces false positives before downstream analysis.

## When to use

Apply this skill when working with raw IM-MS data (Agilent MassHunter .d or UIMF format) that contains low-abundance background noise, isolated high-intensity artifacts, or jagged peaks characteristic of low-abundance ions. Use it as an early preprocessing step before demultiplexing, smoothing, or peak detection to improve signal-to-noise ratio and data interpretability.

## When NOT to use

- Input data is already processed or smoothed; applying additional threshold filtering may remove weak but valid signals.
- Analysis requires preservation of all intensity information for quantitation without lossy noise removal.
- Data has already undergone aggressive filtering or quality control upstream (e.g., vendor-level background subtraction).

## Inputs

- Raw IM-MS data file (Agilent MassHunter .d format or UIMF format)
- Low-intensity threshold parameter (instrument-dependent cutoff value)

## Outputs

- Noise-filtered IM-MS data file (MassHunter .d or UIMF format)
- Enhanced signal quality with reduced background noise and spike artifacts

## How to apply

Load raw IM-MS data into PNNL PreProcessor and configure a low-intensity threshold cutoff appropriate to your instrument and sample complexity. Apply the threshold uniformly across all frames and mobility dimensions to remove signals below the cutoff. Then apply the spike removal algorithm, which detects and eliminates isolated high-intensity artifacts that do not represent true ion signals. The rationale is that genuine ion signals persist across multiple frames and mobility bins, while noise spikes are typically localized; this two-stage filtering preserves real signals while eliminating instrumental noise and detector artifacts. Export the filtered data to a new MS-file in the same format with enhanced signal quality.

## Related tools

- **PNNL PreProcessor** (Primary software tool implementing noise filtering by low-intensity threshold and spike removal algorithms for IM-MS data) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Vendor instrument control and data format standard (.d files) supported as input and output format)
- **.NET Framework 4.7.2** (Runtime dependency required for PNNL PreProcessor execution)
- **Microsoft Visual C++ Runtime x64** (Runtime dependency for PNNL PreProcessor)

## Evaluation signals

- Verify that signal intensities below the specified threshold are completely removed across all frames and mobility bins; inspect a sample frame to confirm zero-valued regions correspond to below-threshold areas.
- Check that spike artifacts (isolated, high-intensity pixels not contiguous with neighboring frames) are eliminated while neighboring legitimate signal remains intact.
- Confirm output file is in the same MS-file format as input (.d or UIMF) and that metadata (frame count, mobility calibration, CCS values) are preserved.
- Compare peak shapes before and after filtering; genuine peaks should appear smoother with reduced jagged artifacts, while peak centroids should remain stable.
- Validate that the low-abundance ion signal is enhanced relative to background, as measured by improved signal-to-noise ratio or reduced false-positive feature detection in downstream analysis.

## Limitations

- Threshold parameter is user-configurable and instrument-dependent; incorrect threshold setting may remove weak but valid signals or retain residual noise.
- Saturation repair software (often applied in conjunction with noise filtering) may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, potentially masking true signal loss.
- Spike removal algorithm effectiveness depends on spike morphology; spikes that extend across multiple frames may not be detected as isolated artifacts.
- No changelog or version tracking information is provided in the tool, limiting reproducibility and version-specific parameter documentation.

## Evidence

- [other] removal of signal below a low intensity threshold and an algorithm to remove noise in the form of spikes from IM-MS data: "PNNL-PreProcessor implements noise filtering through two mechanisms: removal of signal below a low intensity threshold and an algorithm to remove noise in the form of spikes from IM-MS data."
- [other] Apply low-intensity threshold filtering and spike removal algorithm: "Apply low-intensity threshold filtering to remove noise signal below the specified intensity cutoff across all frames and mobility dimensions. 3. Apply spike removal algorithm to detect and eliminate"
- [methods] Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [readme] noise filtering by low intensity threshold and spike removal: "noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
- [methods] saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [other] Load raw IM-MS data and export filtered data to new MS-file: "Load the raw IM-MS data file (Agilent MassHunter .d or UIMF format) into PNNL PreProcessor. ... Export the filtered data to a new MS-file in the same instrument format (MassHunter .d or UIMF)"
