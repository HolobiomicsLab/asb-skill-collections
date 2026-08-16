---
name: platform-specific-code-refactoring
description: Use when a Shiny application or R package currently runs only on Windows
  and you need to enable deployment on Linux or macOS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Shiny
  - R
  license_tier: open
derived_from:
- doi: 10.1016/j.aca.2025.344571
  title: quantyfey
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_quantyfey
    doi: 10.1016/j.aca.2025.344571
    title: quantyfey
  dedup_kept_from: coll_quantyfey
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.aca.2025.344571
  all_source_dois:
  - 10.1016/j.aca.2025.344571
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# platform-specific-code-refactoring

## Summary

Identify and refactor Windows-only dependencies, file path conventions, and system calls in a Shiny application codebase to enable cross-platform (Linux/macOS) compatibility. This skill involves static analysis, conditional import abstraction, and verification testing on target platforms.

## When to use

A Shiny application or R package currently runs only on Windows and you need to enable deployment on Linux or macOS. Triggers include: hardcoded Windows path separators (backslashes), Windows-only system calls, unavailable packages on non-Windows platforms, or environment-specific conditional code branches that lack fallbacks.

## When NOT to use

- The application already runs successfully on Linux/macOS with no known platform-specific blockers.
- The application uses Windows-only proprietary APIs or libraries that have no viable cross-platform replacement.
- The project scope explicitly excludes non-Windows platforms as unsupported use cases.

## Inputs

- Shiny application codebase (app.R, global.R, supporting R scripts)
- Environment specification files (DESCRIPTION, package dependencies)
- Configuration and initialization files

## Outputs

- Platform incompatibility audit report (Windows-only dependencies identified with severity)
- Refactored codebase with platform detection and conditional fallbacks
- Platform compatibility report (changes made, conditional imports, remaining constraints)
- Test results from Linux/macOS deployment verification

## How to apply

Audit the application codebase (entry points like app.R and global.R) to identify Windows-only dependencies using static analysis—search for Windows path conventions, system library calls, and conditional code branches. Document each incompatibility with severity and propose platform-agnostic alternatives (e.g., replace Windows path separators with file.path() calls, use conditional imports via if(.Platform$OS.type == 'unix')). Modify configuration files to implement platform detection logic and fallback strategies for unavailable packages. Test the refactored application on Linux or macOS environments to verify successful initialization and basic functionality. Generate a compatibility report listing all changes, conditional imports, and any remaining OS-specific constraints.

## Related tools

- **Shiny** (Web application framework in which platform-specific dependencies are identified and refactored for cross-platform compatibility) — https://github.com/rstudio/shiny
- **R** (Programming language used to implement conditional code branches, platform detection, and cross-platform file path abstractions)

## Evaluation signals

- No Windows-specific file path separators (backslashes) remain in refactored code; all use file.path() or forward slashes with normalizePath().
- Platform detection logic (e.g., if(.Platform$OS.type == 'unix')) is present for all conditional package imports and system calls.
- Application initializes and loads without errors on both Linux and macOS test environments after refactoring.
- All identified platform incompatibilities are documented in the compatibility report with proposed or implemented alternatives.
- Codebase includes fallback imports or graceful degradation for packages unavailable on non-Windows platforms.

## Limitations

- Some R packages may not be available on Linux/macOS; viable alternatives must be identified or the feature requiring them must be disabled conditionally.
- System calls (e.g., shell commands) may behave differently across platforms; platform-specific command syntax must be abstracted or eliminated.
- Apptainer containerization is reported to be slow and difficult to setup on macOS; direct R/RStudio launch may be the only practical deployment path on macOS.
- Testing coverage depends on availability of Linux and macOS environments; missing test infrastructure may limit confidence in cross-platform verification.

## Evidence

- [other] Audit the QuantyFey Shiny application codebase to identify Windows-only dependencies, file path conventions, and system calls.: "Audit the QuantyFey Shiny application codebase (from CDLMarkus/QuantyFey repository) to identify Windows-only dependencies, file path conventions, and system calls."
- [other] Replace Windows path separators with platform-agnostic file.path() calls, identify unavailable packages.: "replace Windows path separators with platform-agnostic file.path() calls, identify unavailable packages"
- [other] Test the modified application launch on a Linux or macOS environment to verify successful initialization and basic functionality.: "Test the modified application launch on a Linux or macOS environment to verify successful initialization and basic functionality."
- [intro] QuantyFey is compatible with Windows operating systems only.: "QuantyFey is compatible with Windows operating systems only"
- [readme] The apptainer version is recommanded for running on Linux systems. For MacOS Systems, this version is generally slow and difficult to setup.: "The apptainer version is recommanded for running on Linux systems. For MacOS Systems, this version is generally slow and difficult to setup."
