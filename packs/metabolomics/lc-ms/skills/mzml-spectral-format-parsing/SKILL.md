---
name: mzml-spectral-format-parsing
description: Use when you have mzML-format raw data files (from any mass spectrometry vendor or conversion tool) and need to ingest them into MS-DIAL version 5 or later for untargeted metabolomics or lipidomics analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - .NET 6
  - .NET Standard
  - GitHub Actions
  - Visual Studio Community 2022
  - .NET Framework 4.7.2
  - MS-DIAL MsdialWorkbench
  techniques:
  - LC-MS
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

# mzml-spectral-format-parsing

## Summary

Parse mzML-format raw mass spectrometry data files into internal data structures compatible with MS-DIAL's metabolomics workflow. This skill is essential when working with open-source or vendor-agnostic MS-DIAL builds that depend exclusively on mzML as the supported raw data input format.

## When to use

You have mzML-format raw data files (from any mass spectrometry vendor or conversion tool) and need to ingest them into MS-DIAL version 5 or later for untargeted metabolomics or lipidomics analysis. MS-DIAL's public build does not include vendor-specific SDKs and therefore requires mzML as the sole input format; use this skill when proprietary formats (e.g., .raw, .d) are not available or when reproducible, open builds are required.

## When NOT to use

- Input is a proprietary vendor format (.raw, .d, .ms2) and you have access to the vendor-specific MS-DIAL release build that includes proprietary SDKs — use the vendor-supported build instead.
- You require support for abf or NetCDF formats exclusively — MS-DIAL's public build supports these alternatives (abf from Reifycs, cdf/NetCDF), but mzML parsing is not applicable.
- Unit testing infrastructure for partial functionalities is required — MS-DIAL's public repository does not currently have unit testing set up for partial functionalities; full integration testing via GitHub Actions is the approved approach.

## Inputs

- mzML-format raw data file (XML-based mass spectrometry data file)
- MS-DIAL repository source code (MsdialWorkbench)
- Build recipe from .github/workflows/dotnet_test.yml
- Reference mzML file with known metadata and spectral values

## Outputs

- Parsed internal data structures containing instrument metadata
- Spectral arrays (m/z and intensity arrays) mapped to internal model
- Retention time and acquisition parameter fields extracted from mzML
- Integration test results validating peak counts and mass accuracy
- CI/CD test logs from GitHub Actions

## How to apply

Clone the MS-DIAL repository and set up the build environment using Visual Studio Community 2022 with .NET Framework 4.7.2 or .NET 6 (following the build recipe in .github/workflows/dotnet_test.yml). Locate or implement the mzML parser module within the codebase that deserializes the mzML XML into MS-DIAL's internal data structures. Load a sample mzML file and verify that metadata (instrument type, acquisition parameters) and spectral arrays (m/z values, intensity values) are correctly mapped. Write integration tests that check parsed peak counts, mass accuracy, and retention time fields against reference values extracted from the mzML file. Execute tests via the GitHub Actions CI/CD pipeline (section `test:`) to ensure reproducibility on the version 5 series build. The parsing workflow is independent of vendor SDKs and must handle both centroided and profile-mode spectra.

## Related tools

- **Visual Studio Community 2022** (IDE for cloning, building, and debugging the MS-DIAL source code with .NET Framework and .NET 6 toolchains) — https://visualstudio.microsoft.com/
- **.NET Framework 4.7.2** (Runtime framework for building and executing MS-DIAL mzML parser on Windows)
- **.NET 6** (Alternative modern cross-platform runtime framework for MS-DIAL builds)
- **GitHub Actions** (CI/CD pipeline for automated reproducible builds and test execution of mzML parsing integration tests) — https://github.com/systemsomicslab/MsdialWorkbench/blob/master/.github/workflows/dotnet_test.yml
- **MS-DIAL MsdialWorkbench** (Source repository containing mzML parser module and build recipes for version 5 series) — https://github.com/systemsomicslab/MsdialWorkbench

## Evaluation signals

- Parsed peak counts match the reference mzML file's spectrum array lengths (no data loss or duplication).
- Extracted m/z and intensity arrays are numerically identical to values in the reference mzML after deserialization.
- Retention time fields are correctly mapped from mzML scan metadata and match expected acquisition timestamps.
- Mass accuracy of parsed m/z values remains within vendor specification (typically ≤ 5 ppm for high-resolution MS).
- GitHub Actions CI/CD pipeline executes all integration tests without failure on the version 5 series build configuration.

## Limitations

- The public MS-DIAL build only supports mzML format for raw data input; proprietary formats require vendor SDK-enabled release builds.
- Unit testing infrastructure for partial functionalities is not currently set up for trial — only full integration testing via GitHub Actions CI/CD is officially supported.
- Only MS-DIAL version 5 series has reproducible builds that can be guaranteed openly; earlier versions may have undocumented parsing logic.
- Profile-mode and centroided spectral modes must both be validated separately; the mzML standard does not enforce a single representation.

## Evidence

- [readme] The version we have made public does not utilize the MS vendor's SDK. Please be aware that it only supports input in the mzML format for raw data.: "The version we have made public does not utilize the MS vendor's SDK. Please be aware that it only supports input in the mzML format for raw data."
- [other] MS-DIAL's public version implements mzML as its sole supported raw data input format, requiring a dedicated parsing pathway that converts mzML files into the software's internal data structures, independent of vendor-specific mass spectrometry SDKs.: "MS-DIAL's public version implements mzML as its sole supported raw data input format, requiring a dedicated parsing pathway that converts mzML files into the software's internal data structures"
- [readme] only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly: "only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly"
- [methods] we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6: "we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6"
- [readme] The 'Debug/Release vendor unsupported' version is a special configuration designed for the purpose of source code distribution.: "The 'Debug/Release vendor unsupported' version is a special configuration designed for the purpose of source code distribution."
- [methods] the unit testing aspect for partial functionalities is not currently set up for trial: "the unit testing aspect for partial functionalities is not currently set up for trial"
