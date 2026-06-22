---
name: ion-mobility-mass-spectrometry-data-preprocessing
description: Use when when you have raw IM-MS data from drift tube (DT) or SLIM instruments in Agilent MassHunter (.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - IM-MS Browser
  - IMFE
  - .NET Framework 4.7.2
  - Microsoft Visual C++ Runtime x64
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
---

# ion-mobility-mass-spectrometry-data-preprocessing

## Summary

Preprocessing pipeline for IM-MS data that removes noise, corrects artifacts, and interpolates ion mobility dimensions to prepare raw Agilent MassHunter (.d) or UIMF files for downstream omics analysis. This skill combines low-intensity thresholding, spike removal, multidimensional smoothing, and saturation repair to enhance signal quality in complex samples.

## When to use

When you have raw IM-MS data from drift tube (DT) or SLIM instruments in Agilent MassHunter (.d) or UIMF format and need to reduce noise, eliminate isolated high-intensity artifacts, smooth jagged low-abundance ion peaks, or repair saturated signal before feature extraction or peak deconvolution. Apply this skill especially when analyzing complex omics samples where structural isomer separation and low-abundance signal recovery are priorities.

## When NOT to use

- Input is already a deconvoluted feature table or extracted ion chromatogram; preprocessing should occur before feature extraction.
- Data is from a non-IM-MS platform (e.g., conventional LC-MS) where the ion mobility dimension and demultiplexing algorithms do not apply.
- Ions have highly convoluted elution/mobility profiles caused by interferences, where saturation repair may produce incorrect results.

## Inputs

- Raw IM-MS data file in Agilent MassHunter (.d) format
- Raw IM-MS data file in UIMF (structure for lossless ion manipulations) format
- Retention time range specification (optional, for temporal filtering)
- Low-intensity threshold value (user-configurable, in intensity units)

## Outputs

- Preprocessed IM-MS data file in Agilent MassHunter (.d) format
- Preprocessed IM-MS data file in UIMF format
- Metadata export file
- Converted arrival time to collisional cross section (CCS) data for SLIM instruments (optional)

## How to apply

Load the raw IM-MS file (Agilent MassHunter .d or UIMF format) into PNNL PreProcessor. Apply data compression and interpolation of the ion mobility dimension to improve demultiplexing and peak deconvolution. Remove signal below a specified low-intensity threshold across all frames and mobility dimensions to eliminate baseline noise. Apply the spike removal algorithm to detect and eliminate isolated high-intensity artifacts that do not represent true ion signals. Perform multidimensional smoothing to remove jagged-peak artifacts common in low-abundance ions while preserving real signals. Repair saturated peaks using the saturation repair module, noting that this may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences. Export the filtered, corrected data to a new MS-file in the original instrument format (MassHunter .d or UIMF) with enhanced signal quality.

## Related tools

- **PNNL PreProcessor** (Primary software tool that implements the complete preprocessing pipeline including noise filtering, interpolation, demultiplexing, smoothing, and saturation repair for IM-MS data.) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Instrument software and data format provider; PNNL PreProcessor reads and writes Agilent MassHunter (.d) MS-files.)
- **IM-MS Browser** (Companion tool that provides method files (.m) for batch polygon extraction during preprocessing.)
- **IMFE** (Tool called from within PNNL PreProcessor for conversion of All Ions IM/MS mobility-aligned fragmentation data to DDA format.)
- **.NET Framework 4.7.2** (Runtime dependency required to execute PNNL PreProcessor.)
- **Microsoft Visual C++ Runtime x64** (Runtime dependency for PNNL PreProcessor execution.)

## Evaluation signals

- Output file format is correct (MassHunter .d or UIMF) and contains the same number of frames and scans as input, with reduced noise intensity and no low-intensity signal below the specified threshold.
- Spike removal verification: isolated high-intensity single-scan artifacts are eliminated while multi-scan real signals remain intact; compare intensity distribution histograms before and after.
- Smoothing effectiveness: low-abundance ion peaks should show reduced jaggedness and artifact-free intensity profiles when visualized in mass spectrometry software; visual inspection via IM-MS Browser or Agilent MassHunter.
- Saturation repair validation: saturated peaks (clipped intensity values) are restored to realistic profiles; compare raw vs. preprocessed chromatogram shapes for known high-abundance analytes.
- Metadata export consistency: exported metadata (frame/scan count, retention time range, CCS values if applicable) are consistent with the preprocessed data file structure.

## Limitations

- Saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, as the algorithm cannot reliably distinguish signal from noise in such cases.
- The spike removal algorithm uses heuristic thresholds that may not adapt to all sample types; validation with known spike artifacts is recommended for new sample matrices.
- No changelog available in the repository, limiting reproducibility and version tracking information for troubleshooting or method reproduction across different software releases.
- The tool is closed-source due to restrictions from the instrument vendor on proprietary data formats, limiting algorithm transparency and customization options.

## Evidence

- [other] Load the raw IM-MS data file (Agilent MassHunter .d or UIMF format) into PNNL PreProcessor: "Load the raw IM-MS data file (Agilent MassHunter .d or UIMF format) into PNNL PreProcessor."
- [other] Low-intensity threshold and spike removal mechanisms: "PNNL-PreProcessor implements noise filtering through two mechanisms: removal of signal below a low intensity threshold and an algorithm to remove noise in the form of spikes from IM-MS data."
- [methods] Data compression, interpolation, and demultiplexing workflow: "Data compression (by frame and mobility) and filtering by retention time range; Data interpolation of the ion mobility dimension to improve the results of the HRdm demultiplexing and peak"
- [methods] Smoothing removes jagged peak artifacts in low-abundance ions: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [methods] Saturation repair may fail on convoluted profiles: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [readme] Tool suite description from README: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
- [intro] IM-MS application domain and advantages: "Ion mobility-mass spectrometry (IM-MS) provides an increasingly popular platform for analyzing complex samples due to its separation power and ability to differentiate structural isomers"
- [other] Export format and file type output: "Export the filtered data to a new MS-file in the same instrument format (MassHunter .d or UIMF)"
