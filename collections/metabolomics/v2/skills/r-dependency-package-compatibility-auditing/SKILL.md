---
name: r-dependency-package-compatibility-auditing
description: Use when a Shiny application or R-based tool is known to run on only one operating system (e.g., Windows-only), and you need to identify the root causes preventing execution on Linux or macOS before undertaking cross-platform porting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3070
  tools:
  - Shiny
  - R
  - RTools
  - Apptainer
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
---

# R Dependency and Package Compatibility Auditing

## Summary

Systematically identify and document platform-specific R package dependencies, system library requirements, and conditional code branches that prevent cross-platform execution of Shiny applications. This skill produces a compatibility matrix and concrete remediation steps needed to enable deployment on alternative operating systems.

## When to use

Apply this skill when a Shiny application or R-based tool is known to run on only one operating system (e.g., Windows-only), and you need to identify the root causes preventing execution on Linux or macOS before undertaking cross-platform porting.

## When NOT to use

- The application is already confirmed to run cross-platform without OS-specific constraints; audit would be redundant.
- Source code is unavailable or proprietary; static analysis cannot be performed.
- The goal is to optimize performance rather than enable cross-platform compatibility; use profiling and benchmarking instead.

## Inputs

- Shiny application source code repository (R, global.R, app.R, and support modules)
- DESCRIPTION or renv.lock dependency manifest
- Configuration files (environment specifications, Docker/Apptainer definitions)
- README or installation documentation describing current platform limitations

## Outputs

- Platform compatibility audit report (list of incompatibilities with severity, location, and proposed fix)
- Modified configuration and code files with conditional imports and platform detection logic
- Cross-platform abstraction layers (e.g., platform-agnostic file path utilities)
- Test results from launch verification on target operating system(s)

## How to apply

Perform a four-stage audit: (1) Static codebase analysis to identify Windows-only dependencies, absolute file paths using backslash separators, and system-specific function calls (e.g., shell commands via system() or system2()); (2) Dependency scanning of R package imports, conditional library loading statements, and environment variables to flag packages unavailable on target platforms; (3) Configuration file review (app.R, global.R, .Rprofile, renv.lock, or DESCRIPTION) to locate OS-specific conditional logic and hard-coded paths; (4) Documentation of all incompatibilities with severity levels (blocking vs. non-critical) and suggested alternatives (e.g., replace file path separators with platform-agnostic file.path() calls, or substitute unavailable packages with cross-platform equivalents). Record findings in a compatibility report linking each incompatibility to its source location and proposed fix.

## Related tools

- **Shiny** (Target application framework being audited for platform-specific dependencies and conditional code branches)
- **R** (Execution environment; version-specific dependencies (e.g., R 4.2.x vs. 4.5.x) must be identified and abstracted)
- **RTools** (Windows-only prerequisite identified as platform-specific constraint requiring conditional handling or substitution)
- **Apptainer** (Alternative container deployment mechanism documented as workaround for Linux execution when native Shiny launch is incompatible) — https://apptainer.org/docs/admin/main/installation.html

## Evaluation signals

- All file path references in codebase use platform-agnostic functions (file.path(), normalizePath(), or fs:: package) rather than hardcoded backslashes or forward slashes
- Audit report enumerates ≥1 Windows-specific dependency (e.g., RTools version constraint, shell command, or unavailable CRAN package) with documented alternative or conditional fallback
- Modified application successfully initializes and loads core modules on verified non-Windows platform (Linux or macOS) without OS-related errors
- Conditional logic (if (.Platform$OS.type == 'windows') or equivalent) is present in configuration files for platform-specific code paths
- DESCRIPTION or renv.lock includes platform-agnostic dependency versions or notes unavailable packages with suggested replacements

## Limitations

- Audit identifies incompatibilities but does not guarantee successful remediation; some dependencies may have no viable cross-platform substitute (e.g., Windows-only commercial libraries).
- Static analysis may miss runtime-only incompatibilities that surface only during execution on target platform; verification testing on actual Linux/macOS systems is mandatory.
- Shiny applications using Apptainer on macOS are documented as slow and difficult to configure; pure R launch may be preferable, but requires additional macOS-specific prerequisites not fully detailed in provided README.
- RTools version coupling (e.g., R 4.2.x requires RTools 4.2) creates tight version constraints; compatibility matrix must account for multiple R versions if broader compatibility is desired.

## Evidence

- [other] QuantyFey is currently restricted to Windows operating systems, indicating the presence of unidentified platform-specific dependencies that must be resolved to enable cross-platform compatibility.: "QuantyFey is currently restricted to Windows operating systems, indicating the presence of unidentified platform-specific dependencies that must be resolved"
- [other] Audit the QuantyFey Shiny application codebase to identify Windows-only dependencies, file path conventions, and system calls. Scan for platform-specific R package requirements, system libraries, and conditional code branches using static analysis.: "Audit the QuantyFey Shiny application codebase to identify Windows-only dependencies, file path conventions, and system calls. Scan for platform-specific R package requirements, system libraries, and"
- [other] Document all identified platform incompatibilities with severity and suggested alternatives (e.g., replace Windows path separators with platform-agnostic file.path() calls, identify unavailable packages).: "replace Windows path separators with platform-agnostic file.path() calls, identify unavailable packages"
- [readme] The standalone version only works on Windows systems. It runs on R-portable 4.2.0 and runs locally on the user's computer.: "The standalone version only works on Windows systems. It runs on R-portable 4.2.0 and runs locally on the user's computer"
- [readme] The launch directly from R with appropriate package control only works on R 4.2.x or the R 4.5.x versions. Windows: current version of RTools for your R version. Linux: multiple prerequisites.: "The launch directly from R with appropriate package control only works on R 4.2.x or the R 4.5.x versions. Windows: current version of RTools for your R version. Linux: multiple prerequisites"
