---
name: file-path-abstraction-and-normalization
description: Use when a Shiny application or R package is confirmed to work on one
  OS (e.g., Windows only) but fails to initialize or run on others due to unresolved
  file path conventions, system library calls, or OS-specific package dependencies.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0203
  tools:
  - Shiny
  - R (base)
  - RTools
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

# file-path-abstraction-and-normalization

## Summary

Abstracts platform-specific file path conventions (Windows backslashes vs. Unix forward slashes) and system calls to enable a codebase to run identically across Windows, Linux, and macOS. This skill ensures cross-platform portability by replacing hardcoded path separators with platform-agnostic functions and implementing conditional imports for OS-specific libraries.

## When to use

Apply this skill when a Shiny application or R package is confirmed to work on one OS (e.g., Windows only) but fails to initialize or run on others due to unresolved file path conventions, system library calls, or OS-specific package dependencies. Trigger: static analysis reveals hardcoded backslashes, Windows-only system calls, or absolute paths in configuration files (app.R, global.R, environment specifications).

## When NOT to use

- The application already runs identically on all target operating systems — no cross-platform incompatibilities exist.
- The codebase uses only platform-agnostic tools and no OS-specific dependencies — abstraction is already complete.
- The goal is to optimize performance on a single OS; cross-platform support is out of scope.

## Inputs

- Source codebase (R scripts: app.R, global.R, custom modules)
- Configuration and environment specification files
- Package dependency declarations (DESCRIPTION, requirements.txt, or environment.yml)

## Outputs

- Modified codebase with platform-agnostic file path functions
- Updated configuration files with OS detection and conditional imports
- Platform compatibility report documenting all changes and remaining constraints
- Test results confirming successful application launch on Windows, Linux, and macOS

## How to apply

Audit the entire codebase for platform-specific path separators (backslashes) and system calls using static analysis or grep patterns. Replace all hardcoded path separators with platform-agnostic R functions such as file.path() or normalizePath(), which automatically adapt to the operating system. Identify conditional code branches and Windows-only package requirements (e.g., RTools availability on Windows), then implement conditional imports using .Platform$OS.type or Sys.info()["sysname"] checks. Modify configuration files to abstract OS detection and provide fallbacks (e.g., use Sys.which() for finding system binaries instead of hardcoded paths). Test the modified application launch on each target OS (Linux, macOS, Windows) to verify successful initialization and basic functionality. Document all changes, conditional imports, and any remaining OS-specific constraints in a platform compatibility report.

## Related tools

- **Shiny** (Web application framework hosting the interactive interface that must be made cross-platform compatible)
- **R (base)** (Provides file.path() and normalizePath() functions for platform-agnostic path handling, and Sys.info() for OS detection)
- **RTools** (Windows-specific toolchain; conditional requirement for Windows builds that must be wrapped in OS checks)

## Examples

```
# In R/RStudio: audit and refactor paths in app.R
# Replace: file_path <- "data\\samples.csv"
# With: file_path <- file.path("data", "samples.csv")
# Add OS detection:
if (Sys.info()["sysname"] == "Windows") { Sys.setenv(R_LIBS_USER = "path/to/windows/libs") }
shiny::runApp(appDir=".", launch.browser=TRUE)
```

## Evaluation signals

- No hardcoded backslashes or forward slashes in file paths; all path operations use file.path() or normalizePath().
- Application initializes and launches successfully on Windows, Linux, and macOS without errors related to file system paths or OS-specific calls.
- All OS-specific imports and library calls are wrapped in conditional checks (e.g., if (Sys.info()["sysname"] == "Windows") { ... }).
- Platform compatibility report exists and lists all modified files, conditional imports applied, and any persisting OS constraints.
- No references to absolute paths or hardcoded system binaries; use of Sys.which() or equivalent for executable discovery.

## Limitations

- Some R packages may not have equivalent implementations across all operating systems; fallbacks or alternative packages must be identified and tested separately.
- macOS support via Apptainer is documented as slow and difficult to set up in the README; direct R/RStudio launch is recommended as a workaround.
- System libraries required by R packages (e.g., for compilation) may differ across OS distributions; the skill addresses code-level abstraction but does not resolve missing system dependencies on Linux.
- The Standalone version (compiled executable) is Windows-only; cross-platform support via this distribution method requires additional containerization (Apptainer) or R-based distribution.

## Evidence

- [other] identify Windows-only dependencies, file path conventions, and system calls: "Audit the QuantyFey Shiny application codebase (from CDLMarkus/QuantyFey repository) to identify Windows-only dependencies, file path conventions, and system calls."
- [other] replace Windows path separators with platform-agnostic file.path() calls: "replace Windows path separators with platform-agnostic file.path() calls, identify unavailable packages"
- [intro] QuantyFey is compatible with Windows operating systems only: "QuantyFey is compatible with Windows operating systems only"
- [other] abstract platform detection and implement cross-platform fallbacks: "Modify configuration files (app.R, global.R, or environment specifications) to abstract platform detection and implement cross-platform fallbacks."
- [other] Test the modified application launch on a Linux or macOS environment to verify successful initialization and basic functionality: "Test the modified application launch on a Linux or macOS environment to verify successful initialization and basic functionality."
- [readme] Launch QuantyFey from your local R, or RStudio works on Windows, Linux, and Mac with different prerequisites: "Launch QuantyFey from your local R, or RStudio - Windows: current version of RTools for your R version; Linux: multiple prerequisites; Mac: no additional prerequisites required"
