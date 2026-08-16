---
name: integration-test-development
description: Use when when you have implemented or modified a data ingestion module
  (e.g., mzML parser) and need to verify that file deserialization produces correct
  internal representations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - .NET 6
  - .NET Standard
  - GitHub Actions
  - .NET Framework 4.7.2 / .NET 6
  - Visual Studio 2022
  - MS-DIAL MsdialWorkbench repository
  techniques:
  - mass-spectrometry
  license_tier: open
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

# integration-test-development

## Summary

Develop and execute integration tests to validate that parsed mass spectrometry raw data files (mzML format) correctly map metadata, spectral arrays, and quantitative fields into a software's internal data structures. This skill ensures reproducibility and correctness of file format ingestion pipelines across build configurations and CI/CD environments.

## When to use

When you have implemented or modified a data ingestion module (e.g., mzML parser) and need to verify that file deserialization produces correct internal representations. Specifically, when peak counts, mass accuracy, retention time values, instrument metadata, m/z arrays, and intensity arrays must match reference expectations from the source file without vendor-specific SDK dependencies.

## When NOT to use

- Input is proprietary vendor format (ABF, RAW, D folder) — unit testing for vendor SDKs is not currently set up; use only for mzML, CDF, or ABF formats supported in vendor unsupported mode.
- Partial or stub functionalities without full parser implementation — unit testing infrastructure for partial functionalities is not currently set up for trial.
- Testing requires reproducible builds across configurations other than version 5 series — only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly.

## Inputs

- mzML-format raw data file (reference file with known metadata and spectral characteristics)
- Implemented mzML parser module (source code or compiled library)
- Build environment configuration (.NET Framework 4.7.2 or .NET 6, Visual Studio or VSCode)

## Outputs

- Integration test suite (unit tests targeting parser output)
- Test execution report (pass/fail per assertion, coverage summary)
- CI/CD build log with test results from GitHub Actions
- Validated internal data structure instances (parsed mzML objects)

## How to apply

Load a reference mzML file using the implemented parser and extract parsed metadata (instrument type, acquisition parameters) and spectral arrays (m/z values, intensity values). Write test assertions that compare parsed peak counts, mass accuracy (typically ±5 ppm tolerance for Orbitrap or similar instruments), and retention time fields against expected ground-truth values from the reference file. Group tests by data category (metadata, peak properties, array consistency) and execute them via the CI/CD pipeline (GitHub Actions) against the version 5 series build configuration to ensure reproducibility. Verify that tests pass on both Debug vendor unsupported and Release configurations where applicable.

## Related tools

- **GitHub Actions** (CI/CD pipeline execution environment for running integration tests via the dotnet_test.yml workflow) — https://github.com/systemsomicslab/MsdialWorkbench
- **.NET Framework 4.7.2 / .NET 6** (Runtime and language framework for compiling and executing parser and test code)
- **Visual Studio 2022** (IDE for writing, debugging, and locally executing integration tests before CI/CD submission)
- **MS-DIAL MsdialWorkbench repository** (Source code repository containing mzML parser implementation, test frameworks, and build recipes) — https://github.com/systemsomicslab/MsdialWorkbench

## Evaluation signals

- All test assertions pass: parsed peak count equals reference count (exact match), mass accuracy falls within tolerance (e.g., ±5 ppm for reference m/z values), retention time fields match reference to within ±0.1 minute.
- Metadata extraction correctness: instrument type, acquisition parameters, and scan-level metadata are correctly deserialized and stored in internal structures without null or default-value artifacts.
- Spectral array consistency: m/z array and intensity array lengths match, m/z values are monotonically increasing or in expected order, intensity values are non-negative and finite.
- CI/CD reproducibility: test suite executes successfully on GitHub Actions runner under version 5 series configuration; build log shows no warnings related to parser deserialization.
- No vendor SDK dependencies: tests pass using only mzML format input and do not invoke proprietary vendor libraries or require runtime flags for vendor format support.

## Limitations

- Unit testing infrastructure for partial functionalities is not currently set up for trial; tests must target complete, functional parser implementations.
- Public version (vendor unsupported) cannot validate against proprietary raw data formats (ABF, RAW, D folders); tests are limited to mzML, CDF, and Reifycs ABF formats.
- Only version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly; tests should target this version to ensure reproducibility across contributors.
- Mass accuracy thresholds and peak-matching tolerances are not explicitly specified in the documentation; practitioners must define these based on their instrument specifications and may need empirical calibration.
- Integration tests verify parser correctness but do not validate downstream metabolomics or lipidomics analysis steps; they focus solely on data ingestion and internal structure population.

## Evidence

- [other] Write integration tests to check that parsed peak counts, mass accuracy, and retention time fields match expected values from the reference mzML file.: "Write integration tests to check that parsed peak counts, mass accuracy, and retention time fields match expected values from the reference mzML file."
- [other] Load a sample mzML file using the implemented parser and verify that metadata (instrument type, acquisition parameters) and spectral arrays (m/z values, intensity values) are correctly mapped to the internal structures.: "Load a sample mzML file using the implemented parser and verify that metadata (instrument type, acquisition parameters) and spectral arrays (m/z values, intensity values) are correctly mapped to the"
- [other] Execute tests via GitHub Actions CI/CD pipeline to ensure reproducibility on the version 5 series build.: "Execute tests via GitHub Actions CI/CD pipeline to ensure reproducibility on the version 5 series build."
- [readme] only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly: "only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly"
- [readme] The version we have made public does not utilize the MS vendor's SDK. Please be aware that it only supports input in the mzML format for raw data.: "The version we have made public does not utilize the MS vendor's SDK. Please be aware that it only supports input in the mzML format for raw data."
- [readme] we apologize that the unit testing aspect for partial functionalities is not currently set up for trial: "we apologize that the unit testing aspect for partial functionalities is not currently set up for trial"
