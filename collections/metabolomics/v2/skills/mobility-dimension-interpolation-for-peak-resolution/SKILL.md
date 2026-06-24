---
name: mobility-dimension-interpolation-for-peak-resolution
description: Use when working with raw multiplexed IM-MS data (UIMF or Agilent MassHunter
  .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - .NET Framework
  - Microsoft Visual C++ Runtime x64
  - .NET Framework 4.7.2
  techniques:
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/jasms.4c00220
  title: PNNL PreProcessor
- doi: 10.1021/acs.jproteome.1c00425
  title: ''
evidence_spans:
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass
  spectrometry data files
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass
  spectrometry data files (MS-files) from drift tube (DT) and structure for lossless
  ion manipulations (SLIM) IM-MS
- Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files)
- Agilent MassHunter (.d) and UIMF mass spectrometry data files
- .NET Framework 4.7.2 or later (included with Windows 10 update 1803 and later releases
- Microsoft Visual C++ Runtime x64 (may already be installed, if the program doesn't
  work then you can download vcredist_x64.exe
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

# mobility-dimension-interpolation-for-peak-resolution

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpolate arrival time values across the ion mobility dimension in IM-MS data to improve peak deconvolution resolution before applying demultiplexing algorithms. This preprocessing step enhances the ability to resolve overlapping ions in multiplexed acquisitions by increasing effective mobility resolution.

## When to use

Apply this skill when working with raw multiplexed IM-MS data (UIMF or Agilent MassHunter .d format) where ion mobility dimension resolution limits peak deconvolution quality, particularly before executing ion mobility demultiplexing on low-abundance or closely-spaced m/z and mobility features that would otherwise appear as convoluted or jagged peaks.

## When NOT to use

- Data is already in conventional (non-multiplexed) IM-MS format requiring no demultiplexing
- Ion mobility dimension already has sufficient native resolution and peak overlap is not a limiting factor in analysis
- Input data is from instruments where mobility dimension is not discretely sampled (e.g., continuous flow systems) or lacks well-defined arrival time structure

## Inputs

- Raw IM-MS data file (UIMF format)
- Raw IM-MS data file (Agilent MassHunter .d format)
- Multiplexed acquisition frames with raw arrival time values

## Outputs

- Interpolated IM-MS dataset with densified ion mobility dimension
- Preprocessed data ready for demultiplexing and peak deconvolution

## How to apply

Load the raw IM-MS data file into PNNL PreProcessor and apply ion mobility dimension interpolation as a preparatory step before demultiplexing. The interpolation strategy enhances the spatial resolution of the mobility dimension by densifying the arrival time grid, which directly improves the subsequent HRdm (high-resolution demultiplexing) strategy's ability to deconvolve multiplexed frames and recover conventional IM-MS spectra. The rationale is that finer mobility resolution reduces peak overlap artifacts and allows the demultiplexing algorithm to identify and separate signals that would otherwise merge. This step is particularly effective for low-abundance ions where peak quality is already compromised by noise.

## Related tools

- **PNNL PreProcessor** (Primary execution environment that integrates ion mobility dimension interpolation as part of its preprocessing pipeline for demultiplexing and peak deconvolution) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Raw data acquisition and format (.d) provider; data source for interpolation) — https://www.agilent.com
- **.NET Framework 4.7.2** (Runtime dependency for PNNL PreProcessor execution)
- **Microsoft Visual C++ Runtime x64** (System library dependency for PNNL PreProcessor execution)

## Evaluation signals

- Verify that interpolated arrival time values are denser (finer grid spacing) than raw input without introducing spurious data points
- Confirm that multiplexed frames can be demultiplexed with higher peak deconvolution accuracy (fewer convoluted elution/mobility profiles) after interpolation versus without
- Check that jagged peak artifacts in low-abundance ions are reduced post-interpolation, indicating improved signal quality for downstream analysis
- Validate that the interpolated dataset maintains correct m/z and retention time dimensions unchanged; only mobility dimension is affected
- Ensure output file format (UIMF or .d) and metadata are preserved and exportable in the original instrument data format

## Limitations

- Interpolation does not recover information lost due to undersampling; it improves effective resolution only if true mobility variation exists between sample points
- Saturation repair algorithms applied downstream may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, even after interpolation
- Effectiveness is limited for very low-abundance ions where inherent noise dominates; smoothing and spike removal must follow to realize full benefit
- Interpolation is specific to discrete arrival-time-based mobility measurements (drift tube DT, SLIM); continuous or non-standardized mobility encoding may require alternative approaches

## Evidence

- [methods] Data interpolation of the ion mobility dimension to improve the results of the HRdm demultiplexing and peak deconvolution strategy: "Data interpolation of the ion mobility dimension to improve the results of the HRdm demultiplexing and peak deconvolution strategy"
- [other] Apply ion mobility dimension interpolation to improve demultiplexing resolution and peak deconvolution using the HRdm strategy: "Apply ion mobility dimension interpolation to improve demultiplexing resolution and peak deconvolution using the HRdm strategy"
- [methods] Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [readme] data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
- [methods] the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
