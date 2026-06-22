---
name: imms-data-format-conversion
description: Use when when you have raw Agilent MassHunter (.d) or UIMF IM-MS data files from drift tube (DT) or structure for lossless ion manipulations (SLIM) instruments and need to ingest them into a preprocessing pipeline that requires standardized in-memory or intermediate representations for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - IM-MS Browser
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# IM-MS Data Format Conversion

## Summary

Convert ion mobility–mass spectrometry (IM-MS) raw data files between vendor-specific formats (Agilent MassHunter .d, UIMF) and standardized or proprietary interchange formats to enable downstream processing, demultiplexing, and metadata extraction in unified pipelines.

## When to use

When you have raw Agilent MassHunter (.d) or UIMF IM-MS data files from drift tube (DT) or structure for lossless ion manipulations (SLIM) instruments and need to ingest them into a preprocessing pipeline that requires standardized in-memory or intermediate representations for multidimensional smoothing, saturation repair, and metadata export.

## When NOT to use

- Input is already in a processed or feature-extracted format (e.g., quantified feature table, aligned peaks); conversion applies to raw instrument output only.
- Data has been converted to mzML or other open standards by a third-party tool; further conversion may lose vendor-specific metadata or introduce inconsistencies.
- File format is not Agilent MassHunter (.d) or UIMF; PNNL PreProcessor does not support other vendor formats without custom plugins.

## Inputs

- Agilent MassHunter (.d) file format
- UIMF (Universal Ion Mobility Format) file
- Raw IM-MS data from drift tube (DT) or SLIM instruments

## Outputs

- Internal preprocessed IM-MS data representation (frame-compressed, interpolated)
- Ion mobility frame metadata (field strength, pressure, temperature, MS actuals)
- Converted arrival time or CCS values (for SLIM data)
- Frame and mobility-indexed data arrays ready for demultiplexing and smoothing

## How to apply

Load raw Agilent MassHunter (.d) or UIMF IM-MS data files into PNNL PreProcessor using its built-in file parser, which automatically detects the input format and converts it to an internal representation suitable for subsequent algorithmic steps (data compression, interpolation, ion mobility demultiplexing, smoothing, and saturation repair). The conversion step preserves frame-level metadata (field strength, pressure, temperature, MS actuals) and ion mobility arrival time information needed for CCS conversion and demultiplexing. Check conversion success by verifying that frame counts, m/z ranges, and mobility dimension bounds match the source file metadata and that no parsing errors are logged.

## Related tools

- **PNNL PreProcessor** (Primary tool for loading and converting raw Agilent MassHunter (.d) and UIMF IM-MS data files into internal preprocessing representation) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Vendor software that generates raw .d files; PNNL PreProcessor integrates Agilent's Data Access Component Library to parse these files) — https://www.agilent.com
- **IM-MS Browser** (Companion tool providing method files (.m) for batch polygon extraction in PNNL PreProcessor)

## Evaluation signals

- Verify frame count, m/z range, and mobility dimension bounds match the source file header or instrument acquisition metadata.
- Check that ion mobility frame metadata (field strength, pressure, temperature, MS actuals) are correctly parsed and present in the converted representation.
- Confirm no parsing errors or format-mismatch warnings appear in tool logs during file load.
- For SLIM data, validate that converted arrival time values fall within expected ranges and that CCS conversion produces physically plausible values (typically 50–500 Ų for peptides).
- Spot-check intensity profiles in a few m/z and mobility bins before and after conversion to ensure no data truncation or transposition artifacts.

## Limitations

- PNNL PreProcessor only supports Agilent MassHunter (.d) and UIMF formats; other vendor formats (e.g., Waters raw, Bruker .d, Thermo .raw) are not supported without custom development.
- Closed-source binary distribution; the conversion logic is proprietary and depends on the Agilent Technologies Mass Hunter Data Access Component Library, which restricts source code availability and may have its own licensing constraints.
- Metadata preservation is limited to frame-level fields (field strength, pressure, temperature, MS actuals); instrument-specific or user-defined metadata stored in vendor extensions may not be converted.
- Large files may incur memory overhead during format conversion and subsequent interpolation; performance depends on data size and available RAM.

## Evidence

- [other] Load a raw Agilent MassHunter (.d) or UIMF IM-MS data file into PNNL PreProcessor: "Load a raw Agilent MassHunter (.d) or UIMF IM-MS data file into PNNL PreProcessor"
- [readme] tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files: "we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files"
- [methods] Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files) from drift tube (DT) and structure for lossless ion manipulations (SLIM): "Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files) from drift tube (DT) and structure for lossless ion manipulations (SLIM)"
- [other] Export ion mobility frame metadata (field strength, pressure, temperature, and MS actuals) to a text file: "Export ion mobility frame metadata (field strength, pressure, temperature, and MS actuals) to a text file"
- [methods] Data interpolation of the ion mobility dimension to improve the results of the HRdm demultiplexing and peak deconvolution strategy: "Data interpolation of the ion mobility dimension to improve the results of the HRdm demultiplexing and peak deconvolution strategy"
- [readme] the software binary depends on other software libraries which place further restrictions on its use and redistribution. By using PNNL-PreProcessor, you agree to comply with the restrictions imposed on you by the license agreements of the software libraries on which it depends: Agilent Technologies Mass Hunter Data Access Component Library: "the software binary depends on other software libraries which place further restrictions on its use and redistribution. By using PNNL-PreProcessor, you agree to comply with the restrictions imposed"
