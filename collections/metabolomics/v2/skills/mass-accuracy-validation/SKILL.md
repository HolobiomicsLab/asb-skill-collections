---
name: mass-accuracy-validation
description: Use when after implementing or modifying an mzML parser module that converts
  mzML files into MS-DIAL's internal data model, and before integrating the parser
  into the production analysis pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - .NET 6
  - .NET Standard
  - GitHub Actions
  - MS-DIAL
  - .NET Framework 4.7.2 / .NET 6
  - Visual Studio / Visual Studio Code
  - GitHub Actions CI/CD
  - masscube
  - Python
  - MSConvert
  - Rapid QC-MS
  techniques:
  - mass-spectrometry
  license_tier: noncommercial
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: huaxuyu/masscube
derived_from:
- doi: 10.1021/acs.analchem.0c01980
  title: CorrDec
- doi: 10.1038/s41467-025-60640-5
  title: ''
- doi: 10.1021/acs.analchem.4c00786
  title: ''
evidence_spans:
- we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and
  .NET 6
- The .NET class libraries adhere at least to the specifications of .NET Standard
  2.0
- To conduct tests, please refer to section `test:` of GitHub Actions
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing
- masscube is an integrated Python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corrdec_cq
    doi: 10.1021/acs.analchem.0c01980
    title: CorrDec
  - build: coll_masscube_cq
    doi: 10.1038/s41467-025-60640-5
    title: MassCube
  - build: coll_rapid_qc_ms_cq
    doi: 10.1021/acs.analchem.4c00786
    title: Rapid QC-MS
  dedup_kept_from: coll_corrdec_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01980
  all_source_dois:
  - 10.1021/acs.analchem.0c01980
  - 10.1038/s41467-025-60640-5
  - 10.1021/acs.analchem.4c00786
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-accuracy-validation

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Verification that parsed mass spectrometry spectral data (m/z values and intensity arrays) extracted from mzML-format raw data files maintain expected mass accuracy when mapped to MS-DIAL's internal data structures. This skill ensures that deserialization and format conversion workflows preserve measurement fidelity prior to downstream metabolomics or lipidomics analysis.

## When to use

After implementing or modifying an mzML parser module that converts mzML files into MS-DIAL's internal data model, and before integrating the parser into the production analysis pipeline. Use this skill when you have a reference mzML file with known or independently validated m/z calibration, and you need to confirm that the parsed spectral arrays (m/z values, intensity values) are correctly mapped without systematic bias or loss of precision.

## When NOT to use

- Input is already in MS-DIAL's native internal format; use this skill only when parsing from external file formats such as mzML.
- Reference calibration data is unavailable or unreliable; mass accuracy validation requires a known-good standard for comparison.
- Only vendor-specific proprietary raw data formats are available (e.g., .raw from Thermo Fisher); the public MS-DIAL version only supports mzML, abf (Reifycs), and cdf (NetCDF) formats.

## Inputs

- mzML-format raw data file
- reference m/z calibration data or independently validated spectral array
- MS-DIAL internal data model specification

## Outputs

- parsed spectral arrays (m/z values, intensity values) mapped to internal structures
- mass accuracy report (absolute error in ppm or Da per peak)
- integration test results (pass/fail status for mass accuracy, peak count, retention time)

## How to apply

Load a sample mzML file using the implemented parser and extract the resulting m/z and intensity arrays along with metadata (instrument type, acquisition parameters, retention time). Compare the parsed m/z values against reference values from the source mzML file or from an external mass calibration standard, computing the absolute mass error in ppm or Da for representative peaks across the full m/z range. Flag any m/z values that deviate by more than the instrument's typical mass accuracy specification (commonly 5 ppm for high-resolution instruments, 10–20 ppm for lower-resolution systems). Write integration tests that verify peak counts match expectations, mass accuracy falls within tolerance, and retention time fields are correctly populated. Execute tests via the GitHub Actions CI/CD pipeline to ensure reproducibility across the version 5 series build.

## Related tools

- **MS-DIAL** (Target software whose internal data model is the destination for parsed mzML spectral data; defines the schema and validation rules for mass accuracy checks) — https://github.com/systemsomicslab/MsdialWorkbench
- **.NET Framework 4.7.2 / .NET 6** (Runtime environment for building and executing the mzML parser and validation tests)
- **Visual Studio / Visual Studio Code** (IDE for implementing the parser module, writing integration tests, and debugging mass accuracy discrepancies)
- **GitHub Actions CI/CD** (Automated test execution platform to ensure mass accuracy validation passes reproducibly across the version 5 series build) — https://github.com/systemsomicslab/MsdialWorkbench/blob/master/.github/workflows/dotnet_test.yml

## Evaluation signals

- Absolute mass error (in ppm or Da) for each parsed peak falls within the instrument's specified mass accuracy tolerance (e.g., < 5 ppm for high-resolution MS).
- Peak count in parsed spectral arrays matches the expected count from the reference mzML file.
- Retention time fields are correctly extracted and populated in the internal data structures without systematic offset.
- Integration tests pass on the GitHub Actions CI/CD pipeline, confirming reproducibility across the version 5 series build environment.
- No systematic bias in mass error across the full m/z range (i.e., high and low m/z regions show comparable accuracy).

## Limitations

- Unit testing infrastructure for partial functionalities is not currently set up for trial, which may limit granular validation of individual parser submodules.
- The public version of MS-DIAL only supports mzML, abf, and cdf formats; mass accuracy validation cannot be applied to proprietary vendor formats (e.g., Thermo .raw) without access to vendor SDKs, which are not included in the open-source distribution.
- Mass accuracy validation is only guaranteed for version 5 series builds; earlier versions do not have reproducible builds that can be verified openly.
- Validation accuracy depends on the quality and completeness of the reference mzML file; systematic errors in the source file will propagate to validation results.

## Evidence

- [other] MS-DIAL's public version implements mzML as its sole supported raw data input format, requiring a dedicated parsing pathway that converts mzML files into the software's internal data structures: "MS-DIAL's public version implements mzML as its sole supported raw data input format, requiring a dedicated parsing pathway that converts mzML files into the software's internal data structures"
- [other] Load a sample mzML file using the implemented parser and verify that metadata (instrument type, acquisition parameters) and spectral arrays (m/z values, intensity values) are correctly mapped to the internal structures.: "Load a sample mzML file using the implemented parser and verify that metadata (instrument type, acquisition parameters) and spectral arrays (m/z values, intensity values) are correctly mapped to the"
- [other] Write integration tests to check that parsed peak counts, mass accuracy, and retention time fields match expected values from the reference mzML file.: "Write integration tests to check that parsed peak counts, mass accuracy, and retention time fields match expected values from the reference mzML file"
- [other] Execute tests via GitHub Actions CI/CD pipeline to ensure reproducibility on the version 5 series build.: "Execute tests via GitHub Actions CI/CD pipeline to ensure reproducibility on the version 5 series build"
- [readme] The version we have made public does not utilize the MS vendor's SDK. Please be aware that it only supports input in the mzML format for raw data.: "The version we have made public does not utilize the MS vendor's SDK. Please be aware that it only supports input in the mzML format for raw data."
- [readme] only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly: "only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly"
