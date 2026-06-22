---
name: vendor-format-recognition-and-handling
description: 'Use when when Rapid QC-MS receives vendor-format LC-MS acquisition files from instrument data folders and must prepare them for automated QC checks and MS-DIAL processing. Specifically: input files are in proprietary vendor formats (Thermo .raw, Bruker .d, Sciex .'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - MSConvert
  - MS-DIAL
  - Rapid QC-MS
derived_from:
- doi: 10.1021/acs.analchem.4c00786
  title: Rapid QC-MS
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapid_qc_ms_cq
    doi: 10.1021/acs.analchem.4c00786
    title: Rapid QC-MS
  dedup_kept_from: coll_rapid_qc_ms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c00786
  all_source_dois:
  - 10.1021/acs.analchem.4c00786
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# vendor-format-recognition-and-handling

## Summary

Recognize proprietary LC-MS vendor file formats (.raw, .d, .ms) and route them through MSConvert to convert to open mzML format for downstream quality control processing. This skill ensures compatibility across heterogeneous mass spectrometry instruments by standardizing input data before QC analysis.

## When to use

When Rapid QC-MS receives vendor-format LC-MS acquisition files from instrument data folders and must prepare them for automated QC checks and MS-DIAL processing. Specifically: input files are in proprietary vendor formats (Thermo .raw, Bruker .d, Sciex .ms, Waters formats), the analysis pipeline requires open-format spectral data, or cross-instrument portability is required.

## When NOT to use

- Input is already in mzML or other open standard format (skip conversion, pass directly to QC).
- MSConvert is unavailable and cannot be installed on the system (use alternative converters or abort pipeline with error message).
- Running on MacOS without manual MSConvert setup—README states MacOS users can only monitor/view data, not convert vendor formats due to MSConvert platform dependency.

## Inputs

- Vendor-format LC-MS acquisition file (.raw, .d, .ms, or other proprietary format)
- MSConvert executable (path or module reference)
- Target output directory for mzML files

## Outputs

- mzML-formatted spectral data file (open format compatible with downstream QC)
- Conversion log or status report (success/failure, file size, metadata summary)

## How to apply

Locate or confirm MSConvert availability in the system PATH or as a standalone module executable. Design a subprocess wrapper that invokes MSConvert with the vendor-format file (e.g., .raw, .d, .ms) as input and specifies mzML as the output format. Execute the conversion on representative vendor files from the instrument data directory. Validate that the output mzML is well-formed by checking spectral metadata integrity (scan count, retention times, m/z values, intensities match or exceed source file expectations). Document supported vendor formats and integration point within the Rapid QC-MS pipeline to enable users to configure format-specific conversion parameters.

## Related tools

- **MSConvert** (Vendor-format-to-mzML converter; mandatory dependency for converting proprietary LC-MS acquisition files into open mzML format prior to QC analysis) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **MS-DIAL** (Downstream data processing and identification tool that accepts converted mzML files) — http://prime.psc.riken.jp/compms/msdial/main.html
- **Rapid QC-MS** (Parent pipeline that integrates vendor format conversion as input-preparation step) — https://github.com/czbiohub-sf/Rapid-QC-MS

## Evaluation signals

- Output mzML file exists at the specified path and is non-empty (file size > 0 bytes).
- mzML XML schema validation passes; file is well-formed XML with expected mzML namespace and root elements.
- Spectral metadata in mzML matches source: scan count, retention time range, m/z range, and intensity statistics are consistent with vendor file metadata.
- Conversion completes without error codes; stderr is empty or contains only non-fatal warnings.
- Downstream MS-DIAL processing accepts the mzML file without format rejection errors.

## Limitations

- Rapid QC-MS is designed to run on Windows; MacOS users cannot perform vendor format conversion due to MSConvert platform dependency, though they can view results.
- Extensive testing has been performed only on Thermo Fisher instruments and .raw files; other vendor formats (Agilent, Bruker, Sciex, Waters) may contain bugs or unsupported metadata fields.
- MSConvert must be installed manually; it is not included in the Python pip package and requires separate download and system PATH configuration.
- Conversion performance and accuracy depend on MSConvert version and vendor file complexity; corrupted or incomplete source files may fail silently or produce invalid mzML.

## Evidence

- [other] Rapid QC-MS requires MSConvert as a dependency for vendor format data conversion, functioning as an input-preparation step that transforms proprietary LC-MS acquisition files into open formats compatible with downstream QC processing.: "Rapid QC-MS requires MSConvert as a dependency for vendor format data conversion, functioning as an input-preparation step that transforms proprietary LC-MS acquisition files into open formats"
- [readme] its dependency on MSConvert for vendor format data conversion and MS-DIAL for data processing and identification: "its dependency on MSConvert for vendor format data conversion and MS-DIAL for data processing and identification"
- [readme] Because MSConvert converts raw acquired data into open mzML format before routing it to the data processing pipeline, the package will work seamlessly with data of all vendor formats.: "Because MSConvert converts raw acquired data into open mzML format before routing it to the data processing pipeline"
- [readme] Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files.: "Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files."
- [readme] Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert for vendor format data conversion: "Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert"
- [readme] MacOS users can still use Rapid QC-MS to monitor / view their instrument run data: "MacOS users can still use Rapid QC-MS to monitor / view their instrument run data"
