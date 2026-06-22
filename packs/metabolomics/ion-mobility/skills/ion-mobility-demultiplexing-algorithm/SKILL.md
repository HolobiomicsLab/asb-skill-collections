---
name: ion-mobility-demultiplexing-algorithm
description: Use when you have raw IM-MS data in UIMF or Agilent MassHunter .d format acquired using multiplexed (compressed) ion mobility pulse sequences, and you need to recover conventional (non-multiplexed) IM-MS spectra with resolved mobility and mass dimensions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - .NET Framework
  - Microsoft Visual C++ Runtime x64
  - IM-MS Browser
  - IMFE
  techniques:
  - ion-mobility-MS
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00220
  all_source_dois:
  - 10.1021/jasms.4c00220
  - 10.1021/acs.jproteome.1c00425
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-mobility-demultiplexing-algorithm

## Summary

This skill applies the PNNL demultiplexing and artifact removal algorithm to recover conventional IM-MS spectra from multiplexed ion mobility–mass spectrometry acquisitions. It is essential when raw data contains overlapping ion mobility frames that must be separated to recover individual mobility-resolved mass spectra.

## When to use

Apply this skill when you have raw IM-MS data in UIMF or Agilent MassHunter .d format acquired using multiplexed (compressed) ion mobility pulse sequences, and you need to recover conventional (non-multiplexed) IM-MS spectra with resolved mobility and mass dimensions. Demultiplexing is required before downstream analysis of low-abundance ions or structural isomer separation.

## When NOT to use

- Input data are already acquired as conventional (non-multiplexed) IM-MS; demultiplexing will degrade signal-to-noise ratio and is unnecessary.
- The sample contains highly convoluted elution/mobility profiles dominated by interferences, where demultiplexing may produce ambiguous or incorrect peak assignments.
- Data have already been demultiplexed by instrument software; re-demultiplexing will introduce redundant artifacts.

## Inputs

- UIMF raw data files (PNNL/Waters IM-MS format)
- Agilent MassHunter .d data folders (Agilent instrument format)
- Ion mobility frames with multiplexed (compressed) pulse sequences

## Outputs

- Demultiplexed IM-MS spectra in original instrument data format
- Recovered conventional (non-multiplexed) frames with resolved m/z and mobility dimensions
- Processed MS-file suitable for downstream omics analysis

## How to apply

Load the raw IM-MS data file into PNNL PreProcessor. First, apply ion mobility dimension interpolation using the HRdm (high-resolution demultiplexing) strategy to improve peak deconvolution resolution. Then execute the integrated PNNL demultiplexing and artifact removal algorithm, selecting an appropriate pulse coverage percentage parameter (lower values increase specificity; higher values maximize sensitivity for low-level signals). Follow demultiplexing with spike-removal to eliminate noise artifacts, then apply multidimensional smoothing to enhance real signals and reduce variations in abundance, elution, and mobility profiles. The rationale is that demultiplexing must precede smoothing to avoid propagating artifacts across frames; pulse coverage percentage should be tuned based on expected signal intensity and acceptable false positive rate.

## Related tools

- **PNNL PreProcessor** (Integrated platform implementing demultiplexing, interpolation, smoothing, spike removal, and saturation repair in a unified workflow) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Instrument vendor software for reading native .d data format; PNNL PreProcessor wraps the vendor Data Access Component Library) — https://www.agilent.com
- **IM-MS Browser** (Companion tool providing polygon extraction .m method files for batch feature selection during preprocessing)
- **IMFE** (IM to DDA conversion tool callable from within PNNL PreProcessor for mobility-aligned fragmentation data workflows)

## Evaluation signals

- Output frame count and mobility bin count match expected demultiplexing parameters (pulse coverage percentage); frames are no longer compressed or overlapped.
- Peak deconvolution success: singly-charged or multiply-charged peaks resolve to distinct m/z and mobility coordinates with <5% bin width bleed-over.
- Spike artifacts are absent after spike-removal algorithm; noise floor is reduced by >50% relative to input in low-intensity regions.
- Smoothing preserves intensity ratios: abundance ratios of co-eluting isomers remain within ±10% of pre-smoothing values, confirming no artificial peak merging.
- Output file is readable in original instrument format and imports into downstream analysis tools (e.g., LC-IM-MS feature finders) without format errors.

## Limitations

- Saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by sample interferences, requiring manual inspection or alternative repair strategies.
- Smoothing removes artifacts in jagged peaks common in low-abundance ions, but aggressive smoothing can blur fine structure; tuning of smoothing kernel width is empirical.
- The algorithm assumes multiplexing follows predictable pulse patterns; non-standard or corrupted frame headers may cause demultiplexing to fail or produce ambiguous results.
- No changelog documented in the repository; reproducibility and version tracking information are absent, making it difficult to audit changes across releases.

## Evidence

- [methods] How demultiplexing workflow is sequenced: "Apply ion mobility dimension interpolation to improve demultiplexing resolution and peak deconvolution using the HRdm strategy. Execute the integrated PNNL demultiplexing and artifact removal"
- [methods] Pulse coverage parameter tuning rationale: "A new selectable pulse coverage percentage parameter to recover multiplexed frames and maximize sensitivity for low-level signals"
- [methods] Artifact removal after demultiplexing: "Remove spike artifacts using the integrated spike-removal algorithm to reduce noise. Apply multidimensional smoothing to enhance real signals and reduce variations in abundance, elution, and mobility"
- [methods] Input data formats supported: "Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files) from drift tube (DT) and structure for lossless ion manipulations (SLIM)"
- [readme] Tool capabilities overview: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
- [methods] Saturation repair limitation: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
