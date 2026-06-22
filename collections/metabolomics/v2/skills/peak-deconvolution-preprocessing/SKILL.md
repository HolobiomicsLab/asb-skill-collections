---
name: peak-deconvolution-preprocessing
description: Use when you have raw IM-MS data in Agilent MassHunter (.d) or UIMF format from drift tube (DT) or SLIM instruments, and you intend to perform HRdm demultiplexing or peak deconvolution to resolve co-eluting or structurally similar ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - IM-MS Browser
  - IMFE
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

# peak-deconvolution-preprocessing

## Summary

Prepare ion mobility-mass spectrometry (IM-MS) data for high-resolution demultiplexing and peak deconvolution by applying data compression, interpolation, smoothing, and noise filtering. This preprocessing step enhances the quality of downstream peak deconvolution and structural isomer resolution in complex omics samples.

## When to use

Apply this skill when you have raw IM-MS data in Agilent MassHunter (.d) or UIMF format from drift tube (DT) or SLIM instruments, and you intend to perform HRdm demultiplexing or peak deconvolution to resolve co-eluting or structurally similar ions. Use it particularly when input data exhibits low-abundance ion artifacts, saturation in high-intensity signals, or jagged peak profiles that would degrade downstream deconvolution accuracy.

## When NOT to use

- Input is already a feature table, intensity matrix, or aggregated quantitative data — preprocessing is only applicable to raw IM-MS spectra.
- Data comes from a different instrument platform (e.g., conventional LC-MS without ion mobility) — PNNL PreProcessor is specific to IM-MS file formats.
- Ions exhibit highly convoluted elution/mobility profiles caused by severe interferences — saturation repair may produce incorrect results in such cases.

## Inputs

- Raw IM-MS data file (Agilent MassHunter .d format)
- Raw IM-MS data file (UIMF format)
- Retention time range specification (optional)
- Noise intensity threshold parameter (optional)
- Pulse coverage percentage for demultiplexing (optional)

## Outputs

- Compressed and interpolated IM-MS data file (Agilent MassHunter .d or UIMF format)
- Smoothed, spike-removed, and saturation-repaired peak data
- Preprocessed data ready for HRdm demultiplexing and peak deconvolution

## How to apply

Load raw MS-file (Agilent MassHunter .d or UIMF format) into PNNL PreProcessor and apply data compression by frame and mobility dimension, filtering frames by retention time range if specified. Perform data interpolation of the ion mobility dimension to improve separation. Apply multidimensional smoothing to remove artifacts in jagged peaks common in low-abundance ions, and use spike removal and low intensity threshold noise filtering to suppress false signals. Finally, apply saturation repair to correct peak distortions caused by detector saturation. Export the preprocessed data as a new MS-file in the original instrument format for input to HRdm demultiplexing and peak deconvolution algorithms.

## Related tools

- **PNNL PreProcessor** (Primary preprocessing engine providing data compression, interpolation, demultiplexing, smoothing, noise filtering, and saturation repair for IM-MS data.) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Source instrument data acquisition and file format (.d) standard for DT-IM-MS systems.)
- **IM-MS Browser** (Optional companion tool for polygon-based ion extraction and batch processing integration with PNNL PreProcessor.)
- **IMFE** (Integrated tool for converting IM to data-dependent acquisition (DDA) fragmentation data; callable from within PNNL PreProcessor for All Ions IM/MS workflows.)

## Evaluation signals

- Output IM-MS file is valid and opens in Agilent MassHunter or corresponding UIMF reader without corruption or truncation errors.
- Ion mobility dimension is interpolated with no gaps between consecutive scans and smooth mobility continuity across frames.
- Jagged peaks in low-abundance ion regions are visually smoothed and artifact spikes are removed while high-intensity real signals are preserved.
- Peak intensity profiles for saturated signals show corrected reconstructed values that match expected concentration trends, with no clipping artifacts.
- Downstream HRdm demultiplexing and peak deconvolution results show improved separation of co-eluting or structurally similar ions compared to unpreprocessed data.

## Limitations

- Saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, leading to false peak reconstructions.
- Data compression by frame and mobility reduces raw data dimensionality; over-compression may lose fine structural detail needed for resolving closely-spaced isomers.
- Multidimensional smoothing and spike removal use fixed or user-defined thresholds; optimal parameters are sample- and instrument-dependent and may require empirical tuning.
- No changelog or version tracking is provided in the distribution, limiting reproducibility and traceability of algorithm changes across software releases.

## Evidence

- [intro] data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export: "software tool with various algorithms and utilities including data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold"
- [methods] data compression and interpolation improve downstream demultiplexing and deconvolution: "Data interpolation of the ion mobility dimension to improve the results of the HRdm demultiplexing and peak deconvolution strategy"
- [methods] smoothing removes jagged peaks from low-abundance ions: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [methods] saturation repair limitation with convoluted profiles: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [methods] file format and compression workflow: "Data compression (by frame and mobility) and filtering by retention time range"
- [readme] tool description and IM-MS motivation from README: "Ion mobility-mass spectrometry (IM-MS) provides an increasingly popular platform for analyzing complex samples due to its separation power and ability to differentiate structural isomers, which are"
