---
name: ion-mobility-dimension-interpolation
description: Use when when processing raw IM-MS data (Agilent MassHunter .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3195
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
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

# ion-mobility-dimension-interpolation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpolation of the ion mobility dimension in IM-MS data to smooth and regularize mobility profiles, improving downstream demultiplexing and peak deconvolution in drift-tube or SLIM instruments. Applied after data compression to enhance resolution of overlapping or low-abundance ion signals.

## When to use

When processing raw IM-MS data (Agilent MassHunter .d or UIMF format) from drift-tube or SLIM instruments where ion mobility profiles are sparse, jagged, or undersampled, and you intend to perform HRdm demultiplexing or high-resolution peak deconvolution on complex, low-abundance ion populations.

## When NOT to use

- Input is already a deconvoluted feature table or peak list — interpolation of the raw mobility dimension is not applicable to extracted features.
- Data from conventional LC-MS (without ion mobility separation) — interpolation of ion mobility dimension requires explicit mobility dimension data.
- Ions with highly convoluted elution/mobility profiles caused by interferences — saturation and multidimensional artifacts may cause interpolation to produce incorrect smoothed values.

## Inputs

- raw IM-MS data file (Agilent MassHunter .d format or UIMF format)
- frame-and-mobility-compressed data (output of prior compression step)

## Outputs

- interpolated IM-MS data file (Agilent MassHunter .d or UIMF format with smoothed ion mobility dimension)

## How to apply

Load the raw MS-file (Agilent MassHunter .d or UIMF) into PNNL PreProcessor and apply data compression by frame and mobility dimension. Then invoke the data interpolation step on the ion mobility dimension to regularize and smooth the mobility profiles across all frames and m/z values. This interpolation is applied before demultiplexing and peak deconvolution to enhance signal continuity and reduce artifacts in low-abundance ions. The rationale is that interpolation removes jagged peaks common in sparse mobility data while preserving real signals, thereby improving downstream HRdm demultiplexing and peak deconvolution results. Export the interpolated data in the original instrument format.

## Related tools

- **PNNL PreProcessor** (Executes data compression by frame and mobility, applies ion mobility dimension interpolation, and exports interpolated data in original MS-file format) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Provides native MS-file formats (.d and UIMF) that PNNL PreProcessor reads and writes; source of raw IM-MS data)

## Evaluation signals

- Output mobility profiles are continuous across all frames without gaps or jagged peaks characteristic of sparse raw data
- Low-abundance ion signals show enhanced definition and reduced noise spikes after interpolation, confirmed by visual inspection of mobility-resolved chromatograms
- Demultiplexing and peak deconvolution results (HRdm algorithm) show improved peak capacity and reduced interference artifacts downstream
- Output file retains identical frame count, retention time range, and m/z range as input; only ion mobility dimension values are smoothed
- Data integrity check: no saturation errors introduced; ions with highly convoluted profiles are flagged or excluded if saturation repair was also applied

## Limitations

- Interpolation may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, particularly when saturation repair is also applied.
- Optimal interpolation method and parameters are not explicitly detailed in the article; algorithm specifics (kernel type, bandwidth, edge handling) remain proprietary to the PNNL PreProcessor binary.
- No changelog or version-tracking information available in the repository, limiting reproducibility and traceability of interpolation algorithm changes across tool versions.

## Evidence

- [methods] Data interpolation of the ion mobility dimension to improve the results of the HRdm demultiplexing and peak deconvolution strategy: "Data interpolation of the ion mobility dimension to improve the results of the HRdm demultiplexing and peak deconvolution strategy"
- [intro] data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
- [methods] Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [methods] the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [readme] Ion mobility-mass spectrometry (IM-MS) provides an increasingly popular platform for analyzing complex samples due to its separation power and ability to differentiate structural isomers: "Ion mobility-mass spectrometry (IM-MS) provides an increasingly popular platform for analyzing complex samples due to its separation power and ability to differentiate structural isomers"
