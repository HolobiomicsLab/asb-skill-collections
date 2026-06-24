---
name: spectral-peak-smoothing-artifact-removal
description: Use when raw Agilent MassHunter (.d) or UIMF mass spectrometry files
  exhibit jagged or noisy peaks, particularly for low-abundance ions where signal-to-noise
  ratio is poor.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - .NET Framework 4.7.2 or later
  - Microsoft Visual C++ Runtime x64
  techniques:
  - LC-MS
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

# spectral-peak-smoothing-artifact-removal

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Multidimensional smoothing reduces noise and artifacts in TOF-MS and IM-MS data by attenuating jagged peaks common in low-abundance ions while preserving real signals. This preprocessing step enhances signal quality across elution time, m/z, and ion mobility dimensions before downstream analysis.

## When to use

Apply this skill when raw Agilent MassHunter (.d) or UIMF mass spectrometry files exhibit jagged or noisy peaks, particularly for low-abundance ions where signal-to-noise ratio is poor. Use it as an early preprocessing step before feature detection, saturation repair, or quantification to improve peak definition and reduce false positives from noise artifacts.

## When NOT to use

- Input data is already heavily processed or quantified (e.g., a feature table or aligned peak list); smoothing should occur at raw data stage only.
- Peak shapes are intentionally broad or multiplet due to instrumental design; smoothing may collapse or distort legitimate structural information.
- High-resolution isotopic or spatial profile information must be preserved exactly; multidimensional smoothing may blur fine spectral detail.

## Inputs

- Raw Agilent MassHunter data file (.d format)
- Raw UIMF (Unified Ion Mobility Format) data file
- Ion mobility-mass spectrometry data from drift tube (DT) or SLIM instruments

## Outputs

- Smoothed mass spectrometry data file (.d or UIMF format)
- Preprocessed dataset with reduced noise and enhanced peak quality
- Output log documenting artifact removal and smoothing statistics

## How to apply

Load the raw IM-MS or TOF-MS data file (.d format from Agilent MassHunter or UIMF format) into the PNNL PreProcessor. Select the multidimensional smoothing operation from the preprocessing utilities menu. The algorithm reduces variations across abundance, elution time, and spectral dimensions simultaneously while preserving signal integrity of true peaks. Execute the smoothing pass on the entire dataset or filtered retention time range, generating output in native Agilent MassHunter format (.d) or UIMF. Verify artifact removal in the output log and validate peak quality by comparing input and output peak morphology, particularly for low-intensity features.

## Related tools

- **PNNL PreProcessor** (Primary execution environment; implements multidimensional smoothing algorithm and manages I/O for .d and UIMF formats) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Provides native data format (.d) support and integration for reading/writing processed datasets)
- **.NET Framework 4.7.2 or later** (Required runtime dependency for PNNL PreProcessor execution)
- **Microsoft Visual C++ Runtime x64** (Required runtime library for PNNL PreProcessor binary execution)

## Evaluation signals

- Jagged peaks in low-abundance ion traces are visibly reduced in output compared to input; real signal peaks remain sharp and well-defined.
- Output data file (.d or UIMF) is valid and readable by downstream tools (IM-MS Browser, IMFE); no corruption or format errors.
- Preprocessing log confirms smoothing operation completed without errors; artifact removal count and statistics are documented.
- Peak intensity, retention time/drift time, and m/z centroids of high-abundance ions remain stable (within <1% tolerance) before and after smoothing.
- Signal-to-noise ratio improves for low-intensity features; spike noise and isolated false peaks are attenuated while contiguous peak regions preserve height.

## Limitations

- Saturation repair software (often applied alongside smoothing) may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, limiting reliability in complex mixtures.
- Multidimensional smoothing effectiveness depends on parameter tuning (not detailed in the article); over-smoothing may collapse real peaks or lose structural information.
- No changelog or version-tracking information is available, limiting reproducibility and traceability of results across software releases.
- Algorithm behavior on edge cases (e.g., extremely low-abundance data, unusual isotopic patterns, or non-standard instrumental configurations) is not validated in the published work.

## Evidence

- [methods] Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced.: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [intro] PNNL-PreProcessor provides a software tool with various algorithms and utilities including data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering, saturation repair and metadata export: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
- [methods] We have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files: "we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files"
- [methods] Multidimensional smoothing of data and repair of saturated peaks: "Multidimensional smoothing of data and repair of saturated peaks"
- [methods] the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [intro] Ion mobility-mass spectrometry (IM-MS) provides an increasingly popular platform for analyzing complex samples due to its separation power and ability to differentiate structural isomers: "Ion mobility-mass spectrometry (IM-MS) provides an increasingly popular platform for analyzing complex samples due to its separation power and ability to differentiate structural isomers"
- [readme] Ion mobility-mass spectrometry (IM-MS) provides an increasingly popular platform for analyzing complex samples due to its separation power and ability to differentiate structural isomers, which are difficult to resolve using conventional LC-MS systems. Here we provide a software tool with various algorithms and utilities to improve workflows using this technology: data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export.: "Here we provide a software tool with various algorithms and utilities to improve workflows using this technology: data compression and interpolation, ion mobility demultiplexing, multidimensional"
