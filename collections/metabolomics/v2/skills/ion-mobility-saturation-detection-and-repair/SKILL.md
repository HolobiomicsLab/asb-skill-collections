---
name: ion-mobility-saturation-detection-and-repair
description: Use when preprocessing raw Agilent MassHunter (.d) or UIMF IM-MS data files that exhibit signal saturation—ion intensity clipping caused by detector or amplifier limits—which distorts peak shape and abundance estimates across the m/z and drift-time axes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3635
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - IM-MS Browser
  - IMFE (Ion Mobility Frame Extraction)
  techniques:
  - LC-MS
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

# ion-mobility-saturation-detection-and-repair

## Summary

Detects and reconstructs saturated ion signals in IM-MS data using multidimensional smoothing across m/z, mobility, and retention time dimensions, then exports frame-level metadata (field strength, pressure, temperature, MS actuals) to enable validation and downstream analysis.

## When to use

Apply this skill when preprocessing raw Agilent MassHunter (.d) or UIMF IM-MS data files that exhibit signal saturation—ion intensity clipping caused by detector or amplifier limits—which distorts peak shape and abundance estimates across the m/z and drift-time axes. The skill is essential before quantitative omics workflows (proteomics, metabolomics) where accurate intensity recovery is required.

## When NOT to use

- Input is already a processed feature table or quantification matrix—saturation repair must occur on raw ion-level data before aggregation.
- Data origin is unclear or from instruments not supported by PNNL PreProcessor (e.g., Bruker, Waters native formats without conversion)—compatibility and vendor-specific file format parsing are prerequisites.
- Ions exhibit highly convoluted elution/mobility profiles due to severe interference; saturation repair may produce incorrect reconstructions in such cases.

## Inputs

- Agilent MassHunter (.d) raw data file
- UIMF (Unified Ion Mobility Format) raw data file
- Ion mobility-mass spectrometry acquisition data from drift-tube (DT) or SLIM instruments

## Outputs

- Saturation-corrected ion mobility frame data
- Ion mobility frame metadata export (field strength, pressure, temperature, MS actuals in text format)
- Preprocessing log with warnings about repair confidence and convoluted profiles
- Smoothed multidimensional signal reconstructed across m/z, mobility, and retention time

## How to apply

Load a raw Agilent MassHunter (.d) or UIMF file into PNNL PreProcessor. Apply the built-in multidimensional smoothing algorithm, which simultaneously repairs saturated peaks across m/z, ion mobility, and retention time dimensions by reconstructing signal intensity from neighboring unsaturated frames and scans. After repair, export ion mobility frame metadata (field strength, pressure, temperature, and MS instrument actuals) to a text file for audit and QC. Verify repair success by examining output logs for warnings about convoluted elution/mobility profiles that may have resulted in incorrect repairs; flag ions with highly overlapped profiles for manual review. The algorithm enhances real signals while removing artifacts in jagged peaks common in low-abundance ions.

## Related tools

- **PNNL PreProcessor** (Primary preprocessing engine; orchestrates saturation repair as part of multidimensional smoothing pipeline) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Source data acquisition and native file format (.d) container; PreProcessor reads proprietary formats via MassHunter Data Access Component Library) — https://www.agilent.com
- **IM-MS Browser** (Supports polygon extraction for batch processing; provides .m method files used by PreProcessor for standardized frame setup)
- **IMFE (Ion Mobility Frame Extraction)** (Callable from within PNNL PreProcessor; converts ion mobility data to DDA format for downstream fragmentation analysis)

## Evaluation signals

- Output logs contain no ERRORS for saturation repair step; presence of INFO messages confirming repair application across all affected frames.
- Exported metadata file is valid text format with populated fields for field strength, pressure, temperature, and MS instrument parameters—schema check confirms required columns are present and numeric values are within physically plausible ranges.
- Comparison of pre- and post-repair intensity profiles for saturated ions shows smooth reconstruction (no cliff edges or discontinuities) and intensity increase in previously clipped regions; jagged low-abundance peaks are visibly smoothed.
- Log warnings explicitly flag any ions with convoluted elution/mobility profiles; these warnings enable targeted review and justify exclusion from downstream quantification if repair confidence is low.
- Repaired data passes downstream demultiplexing and peak deconvolution steps without anomalous failures; ion abundance estimates for validated standards/controls agree with expected stoichiometry and known purity.

## Limitations

- Saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences; manual inspection of flagged ions is recommended.
- Repair accuracy depends on adjacent frame quality and uniformity; isolated saturated frames or severe saturation across most of the chromatogram may yield unreliable reconstructions.
- Metadata export does not include per-scan or per-frame saturation flags; practitioners must cross-reference repair logs to identify which specific frames underwent saturation correction.
- PNNL PreProcessor is closed-source and binary-only due to vendor restrictions on proprietary Agilent data format handling; algorithm implementation details and internal thresholds cannot be independently verified or modified.

## Evidence

- [methods] Saturation repair as part of multidimensional smoothing and metadata export: "PNNL-PreProcessor implements saturation repair as part of multidimensional smoothing of data, and provides metadata export functionality as separate utilities within its preprocessing pipeline"
- [methods] Repair algorithm spans three dimensions: "Apply multidimensional smoothing and saturation repair algorithm to detect and reconstruct saturated peaks across the m/z, mobility, and retention time dimensions."
- [methods] Metadata export content specification: "Export ion mobility frame metadata (field strength, pressure, temperature, and MS actuals) to a text file."
- [methods] Limitation on convoluted profiles: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [methods] Effect on low-abundance signals: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [readme] Tool capabilities overview: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
