---
name: metadata-structure-mapping
description: Use when you have mzML-format raw data files from mass spectrometry experiments and need to ingest them into MS-DIAL for untargeted metabolomics or lipidomics analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - .NET 6
  - .NET Standard
  - GitHub Actions
  - .NET Framework 4.7.2 / .NET 6
  - Visual Studio / Visual Studio Code
  - MsdialWorkbench repository
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.0c01980
  title: CorrDec
evidence_spans:
- we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6
- The .NET class libraries adhere at least to the specifications of .NET Standard 2.0
- To conduct tests, please refer to section `test:` of GitHub Actions
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corrdec_cq
    doi: 10.1021/acs.analchem.0c01980
    title: CorrDec
  dedup_kept_from: coll_corrdec_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01980
  all_source_dois:
  - 10.1021/acs.analchem.0c01980
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metadata-structure-mapping

## Summary

Map raw data file metadata (instrument type, acquisition parameters) and spectral arrays (m/z, intensity values) from an external format (mzML) into a software's internal data structures. This skill is essential when ingesting vendor-neutral or open-standard mass spectrometry data into MS-DIAL or similar metabolomics platforms that require format deserialization before spectral processing.

## When to use

Apply this skill when you have mzML-format raw data files from mass spectrometry experiments and need to ingest them into MS-DIAL for untargeted metabolomics or lipidomics analysis. Specifically, use this skill before peak detection, annotation, or quantification workflows when the input has not yet been parsed into the target software's internal representation of instrument metadata and spectral peaks.

## When NOT to use

- Input is a proprietary vendor format (e.g., .raw from Thermo, .d from Agilent, .ms from Waters) — the public MS-DIAL version 5 does not support vendor SDKs and only accepts mzML, abf, or cdf formats.
- Input is already parsed into MS-DIAL's internal structures — no re-mapping needed.
- Unit testing infrastructure for partial functionalities is required — the article notes this is not currently set up for trial in the public repository.

## Inputs

- mzML-format raw data file (.mzML or .mzML.gz)
- Reference mzML metadata (instrument type, acquisition parameters)
- MS-DIAL source code repository (systemsomicslab/MsdialWorkbench)

## Outputs

- Parsed internal data structure representation (instrument metadata, acquisition parameters, spectral peaks with m/z and intensity arrays)
- Validated mapping between mzML fields and internal object model
- Test results verifying peak counts, mass accuracy, and retention time correctness

## How to apply

Locate or implement the mzML parser module in the MS-DIAL codebase (e.g., in the MsdialWorkbench repository under the parsing/deserialization subsystem). Load a sample mzML file using the parser and verify that metadata fields (instrument type, scan parameters, retention time) and spectral array pairs (m/z values, intensity values) are correctly mapped to the internal data structures. Execute unit and integration tests to confirm that parsed peak counts, mass accuracy (typically validated against reference mzML metadata), and retention time fields match expected values. Run tests via the GitHub Actions CI/CD pipeline (section `test:` in the workflow configuration) to ensure reproducibility. Only the MS-DIAL version 5 series supports reproducible open builds; confirm you are targeting that version or later.

## Related tools

- **.NET Framework 4.7.2 / .NET 6** (Runtime and class library framework for building and running MS-DIAL and its mzML parser module) — https://github.com/systemsomicslab/MsdialWorkbench
- **Visual Studio / Visual Studio Code** (IDE for editing, debugging, and building the mzML parser code and integration tests) — https://github.com/systemsomicslab/MsdialWorkbench
- **GitHub Actions** (CI/CD system for executing and validating mapping tests on version 5 series builds) — https://github.com/systemsomicslab/MsdialWorkbench/blob/master/.github/workflows/dotnet_test.yml
- **MsdialWorkbench repository** (Source code repository containing mzML parser module, internal data structures, and build recipe) — https://github.com/systemsomicslab/MsdialWorkbench

## Evaluation signals

- Parsed metadata fields (instrument type, acquisition parameters) match values in the reference mzML file.
- Spectral peak counts extracted from the mzML file match reference counts.
- Mass accuracy (m/z values) and retention time fields fall within expected tolerances relative to the reference mzML.
- Unit and integration tests pass via GitHub Actions CI/CD pipeline without errors.
- Internal data structure objects are successfully instantiated with no null or missing mandatory fields from mzML input.

## Limitations

- The public MS-DIAL version 5 series does not utilize MS vendor SDKs and only supports mzML, abf (Reifycs), and cdf (NetCDF) formats; proprietary vendor formats cannot be mapped without a separate vendor-supported build configuration.
- Unit testing infrastructure for partial functionalities is not currently set up for trial in the public repository, limiting granular validation of individual parser components.
- Reproducible builds are only guaranteed for the version 5 series; older versions may have unpredictable or unavailable build artifacts.

## Evidence

- [other] MS-DIAL's public version implements mzML as its sole supported raw data input format, requiring a dedicated parsing pathway that converts mzML files into the software's internal data structures: "MS-DIAL's public version implements mzML as its sole supported raw data input format, requiring a dedicated parsing pathway that converts mzML files into the software's internal data structures"
- [other] Implement or locate the mzML parser module in the codebase that handles file format deserialization into the internal data model.: "Implement or locate the mzML parser module in the codebase that handles file format deserialization into the internal data model"
- [other] Load a sample mzML file using the implemented parser and verify that metadata (instrument type, acquisition parameters) and spectral arrays (m/z values, intensity values) are correctly mapped to the internal structures.: "Load a sample mzML file using the implemented parser and verify that metadata (instrument type, acquisition parameters) and spectral arrays (m/z values, intensity values) are correctly mapped to the"
- [other] Write integration tests to check that parsed peak counts, mass accuracy, and retention time fields match expected values from the reference mzML file.: "Write integration tests to check that parsed peak counts, mass accuracy, and retention time fields match expected values from the reference mzML file"
- [readme] The version we have made public does not utilize the MS vendor's SDK. Please be aware that it only supports input in the mzML format for raw data.: "The version we have made public does not utilize the MS vendor's SDK. Please be aware that it only supports input in the mzML format for raw data."
- [methods] only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly: "only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly"
- [other] Execute tests via GitHub Actions CI/CD pipeline to ensure reproducibility on the version 5 series build.: "Execute tests via GitHub Actions CI/CD pipeline to ensure reproducibility on the version 5 series build"
