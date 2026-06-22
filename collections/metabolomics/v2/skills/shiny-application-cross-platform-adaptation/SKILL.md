---
name: shiny-application-cross-platform-adaptation
description: Use when when a Shiny application is documented or observed to run only on Windows, blocking deployment to Linux or macOS users. Typical triggers include hardcoded Windows path separators, unavailable packages on non-Windows systems, or system calls specific to the Windows API.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Shiny
  - R
  - RStudio / R IDE
derived_from:
- doi: 10.1016/j.aca.2025.344571
  title: quantyfey
evidence_spans:
- QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data
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

# shiny-application-cross-platform-adaptation

## Summary

Audit and refactor a Windows-only Shiny application to run on Linux and macOS by identifying platform-specific dependencies, replacing OS-dependent code patterns, and validating cross-platform functionality. This skill ensures interactive R web applications can reach users across operating systems.

## When to use

When a Shiny application is documented or observed to run only on Windows, blocking deployment to Linux or macOS users. Typical triggers include hardcoded Windows path separators, unavailable packages on non-Windows systems, or system calls specific to the Windows API.

## When NOT to use

- When the application intentionally requires Windows-only features (e.g., direct Windows API calls for hardware control) with no viable cross-platform alternative.
- When critical upstream dependencies have no maintained cross-platform equivalents and cannot be replaced.
- When the project scope explicitly excludes multi-platform support and this is a low-priority enhancement.

## Inputs

- Shiny application codebase (app.R, global.R, environment specifications)
- R package dependency declarations (DESCRIPTION, requirements files)
- System call and file I/O code patterns in the application
- Target operating system(s) (Linux, macOS)

## Outputs

- Platform-specific dependency inventory with severity and alternatives
- Refactored Shiny application files with platform abstraction and conditional imports
- Platform compatibility report documenting all changes and remaining constraints
- Validation report from successful launch on target non-Windows environment

## How to apply

Begin by static analysis of the Shiny codebase (app.R, global.R, and supporting R files) to enumerate Windows-only dependencies, file path conventions using backslash separators, and conditional code branches. Scan for R packages with Windows-only binaries or system library requirements. Document all incompatibilities with severity and propose alternatives—for example, replace Windows path separators with platform-agnostic file.path() calls, conditional imports using Sys.info()[['sysname']], or fallback packages. Modify configuration and initialization files to implement cross-platform detection and conditional loading. Test the refactored application launch on a target non-Windows environment (Linux or macOS) to verify initialization, UI rendering, and core functionality. Generate a compatibility report listing all changes, conditional imports, and any remaining OS-specific constraints.

## Related tools

- **Shiny** (Interactive web framework for R; the application runtime to be refactored for cross-platform deployment) — https://shiny.posit.co/
- **R** (Programming language and runtime environment; provides platform abstraction functions (Sys.info, file.path, conditional imports))
- **RStudio / R IDE** (Development environment for testing and launching the refactored Shiny application on multiple OS targets)

## Examples

```
setwd('path_to_QuantyFey_app.r'); source('app.R')  # Run on Linux/macOS after refactoring to use file.path(), Sys.info()[['sysname']] conditionals, and platform-agnostic package imports
```

## Evaluation signals

- Static analysis report lists all Windows-only dependencies, paths, and system calls with no false negatives in codebase scan.
- Refactored code uses platform-agnostic patterns: file.path() instead of backslash separators, Sys.info()[['sysname']] for conditional logic, cross-platform package equivalents.
- Application successfully initializes and renders UI on target Linux or macOS environment without errors.
- All core functionality (data loading, visualization, model fitting) executes without Windows-specific errors on target OS.
- Platform compatibility report is complete and accurate, with no undocumented OS-specific constraints remaining in the codebase.

## Limitations

- Some R packages have no maintained cross-platform binaries; adapter code or alternative packages must be available.
- Shiny applications relying on external system libraries (e.g., Ghostscript, GraphicsMagick) require those libraries installed on the target OS, which may be unavailable or difficult to deploy in restricted environments.
- Performance and UI responsiveness may differ between Windows and Unix-like systems due to differences in file I/O, process management, and rendering pipelines; testing on target OS is mandatory.
- Apptainer containerization for Linux is more complex to set up and runs slowly on macOS, limiting this as a universal fallback solution for all platforms.

## Evidence

- [intro] Windows-only restriction and platform dependencies: "QuantyFey is compatible with Windows operating systems only"
- [other] Audit workflow for identifying platform-specific code: "Audit the QuantyFey Shiny application codebase (from CDLMarkus/QuantyFey repository) to identify Windows-only dependencies, file path conventions, and system calls"
- [other] Platform abstraction and configuration refactoring: "Modify configuration files (app.R, global.R, or environment specifications) to abstract platform detection and implement cross-platform fallbacks"
- [other] Cross-platform validation testing: "Test the modified application launch on a Linux or macOS environment to verify successful initialization and basic functionality"
- [other] Documentation and reporting of changes: "Generate a platform compatibility report listing all changes, conditional imports, and any remaining OS-specific constraints"
- [readme] Apptainer as alternative deployment method for Linux: "The apptainer version is recommanded for running on Linux systems. For MacOS Systems, this version is generally slow and difficult to setup"
- [readme] R version and platform prerequisite alignment: "The launch directly from R with appropriate package control only works on R 4.2.x or the R 4.5.x versions"
