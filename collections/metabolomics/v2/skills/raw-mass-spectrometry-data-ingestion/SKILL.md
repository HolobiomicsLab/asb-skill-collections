---
name: raw-mass-spectrometry-data-ingestion
description: Use when you have raw mass spectrometry data in mzML, abf (Reifycs),
  or cdf (NetCDF) format and need to load it into MS-DIAL or a similar open-source
  metabolomics platform.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - .NET 6
  - .NET Standard
  - GitHub Actions
  - MS-DIAL
  - .NET Framework 4.7.2 / .NET 6
  - Visual Studio / Visual Studio Code
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.0c01980
  title: CorrDec
evidence_spans:
- we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and
  .NET 6
- The .NET class libraries adhere at least to the specifications of .NET Standard
  2.0
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# raw-mass-spectrometry-data-ingestion

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse and deserialize raw mass spectrometry data files (mzML, abf, cdf formats) into a software's internal data structures, mapping metadata (instrument type, acquisition parameters) and spectral arrays (m/z values, intensity values) for downstream metabolomics or lipidomics analysis. This skill is essential when ingesting vendor-independent or open-format MS data into analysis platforms that do not bundle proprietary manufacturer SDKs.

## When to use

You have raw mass spectrometry data in mzML, abf (Reifycs), or cdf (NetCDF) format and need to load it into MS-DIAL or a similar open-source metabolomics platform. This is particularly necessary when working with the public 'vendor unsupported' build of MS-DIAL v5, which lacks access to proprietary manufacturer data readers, or when you want reproducible, open-science builds that do not depend on closed-source SDKs.

## When NOT to use

- Input is proprietary vendor format (e.g., Thermo .raw, Waters .raw) and you are using the public 'vendor unsupported' MS-DIAL build — these formats require closed-source manufacturer SDKs not included in the open-source distribution.
- You have already-processed peak tables or feature matrices rather than raw chromatography/MS data — ingestion handles file deserialization, not feature extraction.
- Unit testing infrastructure is required for all partial functionalities — the article notes this is not currently set up for trial in the public build.

## Inputs

- mzML-format raw data file
- abf-format raw data file (Reifycs)
- cdf-format raw data file (NetCDF)
- MS-DIAL source code repository

## Outputs

- Internal data structure representation of spectral metadata and arrays
- Parsed peak list with m/z, intensity, and retention time values
- Integration test results confirming mass accuracy and peak count parity

## How to apply

Clone the MS-DIAL repository and set up the build environment using .NET Framework 4.7.2 or .NET 6 according to the build recipe in .github/workflows/dotnet_test.yml. Locate or implement the mzML (or abf/cdf) parser module in the codebase that deserializes the file format into the software's internal data model. Load a sample file using the parser and verify that metadata fields (instrument type, acquisition parameters, retention time) and spectral arrays (m/z and intensity values) are correctly mapped to internal structures. Write integration tests that check parsed peak counts, mass accuracy, and retention time fields match reference values from the input file. Execute tests via the GitHub Actions CI/CD pipeline (test: section) to ensure reproducibility on the version 5 series build.

## Related tools

- **MS-DIAL** (Platform whose internal data structures receive the parsed mzML/abf/cdf input; provides parser modules and integration test framework via GitHub Actions) — https://github.com/systemsomicslab/MsdialWorkbench
- **.NET Framework 4.7.2 / .NET 6** (Build and runtime environment for compiling MS-DIAL parser modules and executing CI/CD test suite)
- **Visual Studio / Visual Studio Code** (Development environment for locating, editing, and debugging mzML/abf/cdf parser code)
- **GitHub Actions** (CI/CD pipeline that executes parser integration tests to validate file deserialization and spectral array mapping reproducibly) — https://github.com/systemsomicslab/MsdialWorkbench/blob/master/.github/workflows/dotnet_test.yml

## Evaluation signals

- Parsed metadata fields (instrument type, acquisition parameters, retention time) match values present in the reference mzML/abf/cdf file header.
- Spectral array m/z and intensity values match expected numeric ranges and totals from the original file.
- Peak count in parsed output equals peak count in reference file; mass accuracy is within instrument specifications.
- GitHub Actions test: section executes without failure, confirming parser output on version 5 series reproducible build.
- Integration test assertions on retention time and mass accuracy fields pass for multiple representative sample files.

## Limitations

- The public MS-DIAL v5 'vendor unsupported' build only supports mzML, abf, and cdf formats; proprietary manufacturer formats (Thermo .raw, Waters .raw, Sciex .wiff) require the proprietary build or closed-source SDKs.
- Unit testing infrastructure for partial functionalities is not currently set up for trial in the public distribution; only end-to-end integration tests via GitHub Actions are available.
- Only version 5 series builds guarantee reproducible, openly-verifiable compilation; earlier versions may not be independently buildable.
- File parsing depends on correct mzML schema compliance; non-standard or corrupted XML structure may cause deserialization failure without detailed diagnostic output.

## Evidence

- [other] MS-DIAL's public version implements mzML as its sole supported raw data input format, requiring a dedicated parsing pathway that converts mzML files into the software's internal data structures, independent of vendor-specific mass spectrometry SDKs.: "The version we have made public does not utilize the MS vendor's SDK. Please be aware that it only supports input in the mzML format for raw data."
- [readme] The 'vendor unsupported' build supports only open formats: abf (Reifycs), cdf (NetCDF), and mzML.: "For the 'Debug/Release vendor unsupported' version, only the following formats are supported: **abf**(Reifycs), **cdf**(NetCDF), and **mzml**."
- [methods] Build environment uses .NET Framework 4.7.2, .NET Core 3.1, or .NET 6.: "we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6"
- [methods] Only version 5 series has reproducible builds that can be guaranteed openly.: "only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly"
- [methods] Unit testing infrastructure for partial functionalities is not currently set up for trial.: "we apologize that the unit testing aspect for partial functionalities is not currently set up for trial"
