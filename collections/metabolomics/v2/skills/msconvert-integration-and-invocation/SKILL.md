---
name: msconvert-integration-and-invocation
description: Use when when you have vendor-format LC-MS acquisition files (Thermo .raw, Bruker .d, Sciex .ms, Agilent, Waters formats) that need to be ingested into a quality control or data processing pipeline that requires open, standardized spectral formats.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MSConvert
  - Rapid QC-MS
  - MS-DIAL
derived_from:
- doi: 10.1021/acs.analchem.4c00786
  title: Rapid QC-MS
evidence_spans:
- its dependency on MSConvert for vendor format data conversion
- its dependency on [MSConvert](https://proteowizard.sourceforge.io/tools/msconvert.html) for vendor format data conversion
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
---

# msconvert-integration-and-invocation

## Summary

Integration of MSConvert as a vendor-format-to-mzML conversion dependency within LC-MS quality control pipelines. This skill enables transformation of proprietary mass spectrometry acquisition files (.raw, .d, .ms) into open mzML format for downstream processing and analysis.

## When to use

When you have vendor-format LC-MS acquisition files (Thermo .raw, Bruker .d, Sciex .ms, Agilent, Waters formats) that need to be ingested into a quality control or data processing pipeline that requires open, standardized spectral formats. Use this skill as the input-preparation step before QC checks or peak detection.

## When NOT to use

- Input data is already in mzML, NetCDF, or other open standard format — conversion is unnecessary.
- Running on non-Windows systems without MSConvert compiled/available (MacOS users cannot reliably convert vendor formats; the README states 'Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert').
- Vendor format is not supported by the installed MSConvert version — check ProteoWizard documentation for supported formats before invoking.

## Inputs

- Vendor-format LC-MS acquisition file (.raw, .d, .ms, .wiff, .umd)
- MSConvert executable (Windows; path or module reference)
- Target output directory or path specification

## Outputs

- mzML-formatted spectral data file
- Conversion log or stderr output
- Metadata: scan count, retention time range, m/z range, intensity statistics

## How to apply

Locate or verify MSConvert availability in the system PATH or as a standalone module executable. Design a wrapper function or subprocess call that invokes MSConvert with the vendor acquisition file as input and specifies mzML as the output format (e.g., `msconvert input.raw --mzML --outdir output/`). Execute the conversion on a representative vendor-format file. Validate that the output mzML file is well-formed by verifying it contains expected spectral metadata: scan count, retention times, m/z values, and intensity arrays. Document the MSConvert version, supported vendor formats tested, input/output paths, and the integration point within your pipeline (e.g., pre-QC ingestion step).

## Related tools

- **MSConvert** (Executable dependency for vendor-format-to-mzML conversion; invoked as a subprocess wrapper to transform proprietary LC-MS acquisition files into open format) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **Rapid QC-MS** (Downstream quality control pipeline that consumes mzML output from MSConvert for automated QC checks and real-time monitoring) — https://github.com/czbiohub-sf/Rapid-QC-MS
- **MS-DIAL** (Post-conversion data processing and identification tool that receives mzML files for peak detection and metabolite annotation) — http://prime.psc.riken.jp/compms/msdial/main.html

## Examples

```
msconvert input.raw --mzML --outdir ./converted_data/
```

## Evaluation signals

- Output mzML file exists and is readable by downstream tools (mzML schema validation via libmzML or equivalent).
- Spectral metadata invariants: scan count > 0, retention time range is non-empty and monotonically increasing, m/z values are positive and within expected range (50–2000 m/z typical), intensity arrays match scan count.
- File size comparison: mzML output is typically 1.5–3× the size of compressed vendor format due to XML verbosity and preserved precision.
- Round-trip validation: re-open mzML in a mass spectrometry viewer (e.g., ProteoWizard SeeMS) and visually confirm chromatogram and spectrum appearance match the original vendor file.
- Integration point verification: mzML file is successfully ingested by the downstream QC pipeline without file-format errors or parse exceptions.

## Limitations

- Windows-only: MSConvert is designed for Windows platforms; MacOS and Linux users cannot reliably perform vendor format conversion (README: 'Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert').
- Vendor-specific testing: Rapid QC-MS has only been extensively tested on Thermo Fisher mass spectrometers and Thermo RAW files; bugs and compatibility issues may occur with Agilent, Bruker, Sciex, and Waters formats (README: 'Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers').
- MSConvert and MS-DIAL must be installed separately: they are not included in the Rapid QC-MS pip package and require manual installation on the system.
- Performance: conversion speed depends on file size and system resources; large multi-hour LC-MS runs may require significant time and disk space for mzML output.
- Metadata loss: proprietary vendor metadata not in mzML schema (e.g., instrument tuning parameters, detector calibration) may not be preserved during conversion.

## Evidence

- [intro] its dependency on MSConvert for vendor format data conversion: "its dependency on MSConvert for vendor format data conversion"
- [other] Rapid QC-MS requires MSConvert as a dependency for vendor format data conversion, functioning as an input-preparation step that transforms proprietary LC-MS acquisition files into open formats compatible with downstream QC processing.: "Rapid QC-MS requires MSConvert as a dependency for vendor format data conversion, functioning as an input-preparation step that transforms proprietary LC-MS acquisition files into open formats"
- [other] Locate or download MSConvert executable and confirm availability in the system PATH or as a standalone module. Design a wrapper function or subprocess call that invokes MSConvert with the vendor acquisition file (e.g., .raw, .d, .ms) as input and specifies mzML as the output format. Execute MSConvert conversion on a representative vendor-format LC-MS file. Validate that the output mzML file is well-formed and contains expected spectral metadata (scan count, retention times, m/z values, intensities).: "Locate or download MSConvert executable and confirm availability in the system PATH or as a standalone module. Design a wrapper function or subprocess call that invokes MSConvert with the vendor"
- [readme] Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert for vendor format data conversion and MS-DIAL for data processing and identification.: "Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert for vendor format data conversion and MS-DIAL for data processing and identification."
- [readme] Because MSConvert converts raw acquired data into open mzML format before routing it to the data processing pipeline, the package will work seamlessly with data of all vendor formats.: "Because MSConvert converts raw acquired data into open mzML format before routing it to the data processing pipeline, the package will work seamlessly with data of all vendor formats."
- [readme] Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files. As such, it is expected that there may be bugs and issues with processing data of other vendor formats.: "Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files. As such, it is expected that there may be bugs and issues with"
