---
name: multidimensional-signal-smoothing-imms
description: Use when processing raw IM-MS data (Agilent MassHunter .d or UIMF format) that contains jagged, low-abundance ion peaks or when saturation repair has been applied and the resulting reconstructed signals need artifact removal and enhancement.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3563
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - .NET Framework
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
- .NET Framework 4.7.2 or later (included with Windows 10 update 1803 and later releases
- Microsoft Visual C++ Runtime x64 (may already be installed, if the program doesn't work then you can download vcredist_x64.exe
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

# multidimensional-signal-smoothing-imms

## Summary

Multidimensional smoothing reduces noise and reconstructs low-abundance ion signals in IM-MS data by applying smoothing algorithms across m/z, drift time (or arrival time), and retention time dimensions. This skill is essential for improving signal-to-noise ratio and enabling reliable detection of weak analytes in ion mobility–mass spectrometry workflows.

## When to use

Apply this skill when processing raw IM-MS data (Agilent MassHunter .d or UIMF format) that contains jagged, low-abundance ion peaks or when saturation repair has been applied and the resulting reconstructed signals need artifact removal and enhancement. Use it as a preprocessing step before feature extraction or quantification when signal continuity across the m/z, mobility, and retention time dimensions is compromised by instrument noise or low signal intensity.

## When NOT to use

- Input data is already high-quality, high-abundance full-scan LC-MS (not IM-MS); multidimensional smoothing is IM-MS-specific and unnecessary for conventional LC-MS workflows.
- Peak profiles are highly convoluted due to severe interferences; smoothing may distort or incorrectly merge overlapping signals in complex co-elution regions.
- Real analyte peaks have very sharp, narrow profiles in the mobility or retention time dimension; aggressive smoothing may broaden or artificially merge distinct structural isomers or isobars.

## Inputs

- Raw IM-MS data file (Agilent MassHunter .d format or UIMF)
- Ion mobility demultiplexed frame data
- Spike-removed intermediate data product

## Outputs

- Smoothed IM-MS data with enhanced abundance profiles across m/z, drift time, and retention time dimensions
- Processed MS-file in original instrument data format (Agilent .d or UIMF)
- Artifact-reduced signal matrices ready for feature extraction or quantification

## How to apply

Load the raw IM-MS data file into PNNL PreProcessor, which implements multidimensional smoothing as part of its integrated preprocessing pipeline. The smoothing algorithm operates on the three-dimensional data structure (m/z × arrival time × retention time frame) to enhance real signals while removing artifacts in jagged peaks common in low-abundance ions. The smoothing is typically applied after ion mobility demultiplexing and spike removal, and before data compression and export. Key rationale: smoothing removes noise-induced peak fragmentation without requiring manual parameter tuning for individual peaks, and it must be applied before saturation repair in workflows where peak reconstruction is needed. Verify successful smoothing by examining that previously jagged abundance, elution, and mobility profiles are now continuous, and check that spike artifacts have been eliminated while real signal intensity is preserved.

## Related tools

- **PNNL PreProcessor** (Integrated preprocessing platform that implements multidimensional smoothing as a core algorithm in the IM-MS data pipeline; user selects smoothing as part of the preprocessing workflow applied to raw .d or UIMF files.) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Source instrument vendor software that generates raw IM-MS data files (.d format) that serve as input to PNNL PreProcessor multidimensional smoothing.) — https://www.agilent.com

## Evaluation signals

- Jagged or fragmented low-abundance ion peaks are reconstructed as continuous profiles across the m/z, drift time, and retention time dimensions.
- Spike artifacts (isolated high-intensity noise points) are eliminated from the data while baseline noise is reduced; verify by comparing before/after data in IM-MS Browser or equivalent visualization.
- Real signal intensity in the smoothed output is preserved or slightly enhanced compared to the input; no systematic loss of peak height for true analytes.
- Output logs or processing reports indicate no warnings about convoluted elution/mobility profiles that would indicate unsuccessful smoothing; check that post-smoothing peaks are suitable for downstream saturation repair if needed.
- Abundance and mobility profiles transition smoothly across retention time frames without discontinuities or artifacts introduced by the smoothing algorithm.

## Limitations

- Saturation repair software applied after smoothing may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, potentially creating false peaks or distorting true signals.
- Multidimensional smoothing assumes that true analyte signals are continuous across m/z, drift time, and retention time; highly resolved structural isomers or isobars with distinct narrow peaks may be artificially merged or broadened.
- The algorithm effectiveness depends on spike removal being applied first; if spike artifacts remain, smoothing may propagate or partially retain them as broadened structures.
- No user-tunable parameters for smoothing intensity are documented in the article, limiting ability to adapt smoothing aggressiveness to dataset-specific noise characteristics or analyte complexity.

## Evidence

- [methods] Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [methods] Multidimensional smoothing of data and repair of saturated peaks are core workflow components: "Multidimensional smoothing of data and repair of saturated peaks"
- [methods] The saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [intro] Tool provides multidimensional smoothing as part of its preprocessing utilities: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
- [intro] IM-MS provides separation power and ability to differentiate structural isomers, which are difficult to resolve using conventional LC-MS systems: "Ion mobility-mass spectrometry (IM-MS) provides an increasingly popular platform for analyzing complex samples due to its separation power and ability to differentiate structural isomers, which are"
