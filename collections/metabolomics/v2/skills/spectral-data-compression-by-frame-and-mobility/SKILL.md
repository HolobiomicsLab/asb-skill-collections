---
name: spectral-data-compression-by-frame-and-mobility
description: Use when you have raw IM-MS data in Agilent MassHunter (.d) or UIMF format from drift tube (DT) or SLIM instruments, and you need to reduce data volume while preserving signal integrity for subsequent HRdm demultiplexing and peak deconvolution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - IM-MS Browser
  - .NET Framework 4.7.2
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

# spectral-data-compression-by-frame-and-mobility

## Summary

Reduce IM-MS data dimensionality and file size by compressing raw spectral intensity values along the frame (retention time) and ion mobility dimensions prior to demultiplexing and peak deconvolution. This preprocessing step improves computational efficiency and prepares data for downstream high-resolution demultiplexing workflows.

## When to use

Apply this skill when you have raw IM-MS data in Agilent MassHunter (.d) or UIMF format from drift tube (DT) or SLIM instruments, and you need to reduce data volume while preserving signal integrity for subsequent HRdm demultiplexing and peak deconvolution. Use it before any ion mobility demultiplexing or peak detection step to lower computational burden.

## When NOT to use

- Input data is already in processed feature table or consensus spectrum format (compression assumes frame/mobility-resolved raw intensity matrix).
- You require full original resolution for manual inspection or publication-quality chromatograms (compression introduces coarsening and is irreversible).
- Data exhibits highly convoluted elution/mobility profiles with severe interference; compression may confound subsequent repair algorithms.

## Inputs

- Agilent MassHunter raw data file (.d directory)
- UIMF raw data file
- Retention time range filter (optional: start_rt, end_rt in minutes)

## Outputs

- Compressed Agilent MassHunter MS-file (.d directory)
- Compressed UIMF MS-file
- Metadata export (frame and mobility bin definitions)

## How to apply

Load the raw MS-file (Agilent MassHunter .d or UIMF format) into PNNL PreProcessor. Apply data compression independently along the frame dimension (coalescing adjacent retention time bins) and the mobility dimension (coalescing adjacent arrival time bins), optionally filtering frames by retention time range to focus on regions of interest. The compression reduces redundancy in low-information regions while preserving intensity resolution in high-abundance regions. After compression, proceed immediately to data interpolation of the ion mobility dimension to restore signal quality and improve the downstream HRdm demultiplexing and peak deconvolution results. Export the compressed data as a new MS-file in the original instrument format.

## Related tools

- **PNNL PreProcessor** (Primary tool performing frame and mobility dimension compression, interpolation, and export) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Source data format provider; PNNL PreProcessor reads .d and exports to MassHunter format) — https://www.agilent.com
- **IM-MS Browser** (Optional tool for polygon extraction method definition in batch processing)
- **.NET Framework 4.7.2** (Runtime dependency for PNNL PreProcessor execution)

## Evaluation signals

- Compressed output file size is measurably smaller than input (typically 30–60% reduction depending on compression ratio)
- Frame and mobility bin definitions exported in metadata match the specified compression factors
- Downstream HRdm demultiplexing produces equivalent or improved peak deconvolution metrics (e.g. peak resolution, signal-to-noise) compared to uncompressed data after interpolation
- No NaN or invalid intensity values introduced in compressed output; all intensity values remain non-negative floats
- Retention time range filter (if applied) correctly excludes frames outside the specified range in output file

## Limitations

- Compression is lossy; original frame and mobility resolution cannot be recovered. Select compression factors to balance data reduction against analytical requirements.
- Saturation repair and spike removal algorithms may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, especially after coarse compression.
- No changelog or version tracking information is available in the repository, limiting reproducibility and transparency of compression algorithm updates.
- Compression effectiveness depends on data sparsity and signal structure; dense, uniformly intense data may not compress substantially.

## Evidence

- [other] Data compression by frame and mobility dimension to prepare IM-MS data for downstream demultiplexing and peak deconvolution: "data compression by frame and mobility dimension, and filter frames by retention time range if specified"
- [other] Compression followed by interpolation improves HRdm demultiplexing results: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering"
- [readme] PreProcessor tool capabilities and input formats: "we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files"
- [methods] Saturation repair limitations in convoluted profiles: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [other] Interpolation follows compression as part of the workflow: "Data interpolation of the ion mobility dimension to improve the results of the HRdm demultiplexing and peak deconvolution strategy"
