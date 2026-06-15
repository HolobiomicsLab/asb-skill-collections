---
name: system-library-dependency-mapping
description: Use when a Shiny application or similar cross-platform tool is restricted to a single operating system (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0361
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Shiny
  - R (base and package ecosystem)
  - RTools
derived_from:
- doi: 10.1016/j.aca.2025.344571
  title: quantyfey
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_quantyfey
    doi: 10.1016/j.aca.2025.344571
    title: quantyfey
  dedup_kept_from: coll_quantyfey
schema_version: 0.2.0
---

# system-library-dependency-mapping

## Summary

Identify and document platform-specific system library dependencies, file path conventions, and conditional code branches in a cross-platform application to enable targeted remediation and cross-platform compatibility testing. This skill applies static analysis and codebase auditing to surface hidden OS-specific constraints before attempting deployment.

## When to use

A Shiny application or similar cross-platform tool is restricted to a single operating system (e.g. Windows-only) and you need to understand which unidentified system libraries, package availability constraints, or hardcoded OS conventions are preventing deployment to alternative platforms (Linux, macOS). Use this skill when the application fails to launch or exhibits errors on non-native platforms and root cause analysis is required.

## When NOT to use

- The application is already cross-platform compatible or has no platform-specific constraints—dependency mapping is unnecessary overhead.
- The application must remain Windows-only by design (e.g. requires Windows-only proprietary libraries or hardware interfaces) and cross-platform support is not a goal.
- You are working with a compiled binary or black-box executable where source code inspection and static analysis are not feasible.

## Inputs

- R Shiny application source code (app.R, global.R, module files)
- Package dependency declarations (DESCRIPTION file, library() or require() calls)
- Configuration and environment files (renv.lock, packrat snapshots, or package manifests)
- Codebase static analysis results or manual code inspection notes

## Outputs

- Platform compatibility audit report (list of Windows-only dependencies, file path issues, and unavailable packages)
- Modified codebase with platform detection logic and conditional imports
- Platform-agnostic file path and system call implementations
- Remediation recommendations (e.g. suggested R package alternatives, fallback strategies)
- Cross-platform launch verification log (initialization and functionality tests on Linux/macOS)

## How to apply

Conduct a systematic audit of the application codebase by (1) scanning R package imports and checking package availability matrices across target operating systems (e.g. via CRAN archives and platform-specific mirrors); (2) searching for Windows-only system calls, hardcoded path separators (backslashes), registry lookups, or conditional code branches using static analysis; (3) identifying missing system libraries (e.g. C/C++ dependencies, system binaries, or compiled packages with unavailable binaries) required by R packages; (4) documenting each incompatibility with severity (blocking vs. minor), affected code locations, and suggested platform-agnostic alternatives (e.g. replace file path concatenation with platform-agnostic file.path() calls); (5) modifying configuration files (app.R, global.R, environment specs) to implement platform detection logic and fallback behavior; (6) validating remediation by launching the modified application on each target platform (Linux, macOS) and confirming successful initialization and basic functionality. Success is confirmed when the application initializes without OS-specific errors and core UI/data-loading features function identically across platforms.

## Related tools

- **Shiny** (R web application framework for which platform-specific dependencies must be audited and remediated)
- **R (base and package ecosystem)** (Source language and runtime environment; packages and imports must be scanned for platform availability and conditional compilation)
- **RTools** (Windows-specific development tools for R package compilation; absence on Linux/macOS is a documented constraint)

## Evaluation signals

- All Windows-only system calls (e.g. registry queries, Drive letters, UNC paths) are documented with severity and location in the audit report.
- File path concatenation throughout the codebase uses platform-agnostic functions (file.path(), fs::path_join()) rather than hardcoded separators.
- Package dependency matrix (CRAN/Bioconductor availability across Windows, Linux, macOS) is documented for all imported packages; missing binaries are flagged with fallback suggestions.
- Modified app.R / global.R includes Sys.info() or .Platform detection logic to conditionally load OS-specific packages or set environment variables.
- Application successfully initializes on at least one non-Windows platform (Linux or macOS) with no platform-related errors in console output; data loading and interactive features respond normally.

## Limitations

- Static analysis may not detect runtime OS-specific failures (e.g. environment variable dependencies, file permission issues) that only surface during execution on the target platform.
- Some R packages with native C/C++ dependencies may have incomplete or missing binaries on Linux or macOS despite appearing in package repositories; fallback to compilation from source may be slow or fail if system headers are missing.
- Apptainer containerization is an alternative to source-level remediation but introduces dependency on Apptainer infrastructure; the README notes Apptainer setup is 'complicated on macOS and runs not very fast', making it an imperfect substitute.
- File path abstractions alone may not resolve all OS differences (e.g. line ending conventions, case sensitivity in filenames, permission models).

## Evidence

- [other] QuantyFey is currently restricted to Windows operating systems, indicating the presence of unidentified platform-specific dependencies that must be resolved to enable cross-platform compatibility.: "QuantyFey is currently restricted to Windows operating systems, indicating the presence of unidentified platform-specific dependencies that must be resolved"
- [other] Audit the QuantyFey Shiny application codebase to identify Windows-only dependencies, file path conventions, and system calls.: "Audit the QuantyFey Shiny application codebase to identify Windows-only dependencies, file path conventions, and system calls"
- [other] Document all identified platform incompatibilities with severity and suggested alternatives (e.g. replace Windows path separators with platform-agnostic file.path() calls, identify unavailable packages).: "Document all identified platform incompatibilities with severity and suggested alternatives (e.g. replace Windows path separators with platform-agnostic file.path() calls, identify unavailable"
- [other] Test the modified application launch on a Linux or macOS environment to verify successful initialization and basic functionality.: "Test the modified application launch on a Linux or macOS environment to verify successful initialization and basic functionality"
- [intro] QuantyFey is compatible with Windows operating systems only.: "QuantyFey is compatible with Windows operating systems only"
- [readme] The standalone version only works on Windows systems. It runs on R-portable 4.2.0 and runs locally on the user's computer.: "The standalone version only works on Windows systems. It runs on R-portable 4.2.0 and runs locally on the user's computer"
- [readme] The apptainer version is recommanded for running on Linux systems. For MacOS Systems, this version is generally slow and difficult to setup.: "The apptainer version is recommanded for running on Linux systems. For MacOS Systems, this version is generally slow and difficult to setup"
