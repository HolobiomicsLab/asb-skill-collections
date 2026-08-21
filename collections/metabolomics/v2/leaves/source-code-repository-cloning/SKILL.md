---
name: source-code-repository-cloning
description: Use when you need to obtain the full source code of a scientific tool
  (such as LipidSpace) to build it locally, verify cross-platform compilation, inspect
  the codebase structure, or set up a development environment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - LipidSpace
  - Git
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c02449
  title: LipidSpace
evidence_spans:
- LipidSpace is a stand-alone tool to analyze and compare lipidomes
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidspace_cq
    doi: 10.1021/acs.analchem.3c02449
    title: LipidSpace
  dedup_kept_from: coll_lipidspace_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c02449
  all_source_dois:
  - 10.1021/acs.analchem.3c02449
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# source-code-repository-cloning

## Summary

Clone a source code repository with all submodules and dependencies to establish a local development environment. This skill is essential for obtaining the complete, buildable codebase before compilation or deployment on target platforms.

## When to use

You need to obtain the full source code of a scientific tool (such as LipidSpace) to build it locally, verify cross-platform compilation, inspect the codebase structure, or set up a development environment. Use this skill when the project provides a Git repository URL and you have access to a terminal with Git installed.

## When NOT to use

- A pre-built binary or container image is already available and meets your deployment or testing requirements.
- You only need to download a compiled release artifact (e.g., LipidSpace.zip from the official download page), not modify or build the source.
- The repository is archived, deprecated, or no longer maintained, and the codebase contains known unresolved build failures on your target platform.

## Inputs

- Git repository URL (SSH or HTTPS)
- SSH keys or HTTPS credentials (if repository is private)
- Target filesystem path with sufficient free space

## Outputs

- Local cloned repository directory with all source files
- Initialized submodule directories containing vendored dependencies
- Git metadata (.git directory) for version control operations

## How to apply

Execute a recursive clone command that retrieves the main repository and all nested submodules in a single operation. For projects like LipidSpace that depend on external libraries (e.g., OpenXLSX, cppGoslin), the `--recurse-submodules` flag ensures that vendored dependencies are also checked out, preventing missing library errors during the build phase. Verify the clone succeeded by inspecting the repository structure and confirming the presence of build configuration files (e.g., LipidSpace.pro, CMakeLists.txt) and expected subdirectories like `libraries/`. This step must precede any platform-specific dependency installation or build invocation.

## Related tools

- **Git** (Version control system used to clone the repository and manage submodules) — https://git-scm.com
- **LipidSpace** (Target scientific tool whose repository is cloned to enable local build and cross-platform testing) — https://github.com/lifs-tools/lipidspace

## Examples

```
git clone --recurse-submodules [redacted-email]:lifs-tools/lipidspace.git && cd lipidspace && ls -la libraries/
```

## Evaluation signals

- Repository clone exits with status 0 and displays no fatal errors (e.g., 'Cloning into' message completes without SSL/SSH failure).
- All submodule directories (e.g., `libraries/cppgoslin/`, `libraries/OpenXLSX/`) are populated with source files and metadata, not empty.
- Build configuration files (LipidSpace.pro, qmake6 project files, CMakeLists.txt, or pom.xml) are present in the repository root.
- Git log can be displayed (`git log --oneline`) and shows commit history, confirming a complete checkout.
- Expected source tree structure matches documentation (e.g., presence of `src/`, `ui/`, `build/`, and `libraries/` directories as shown in the README).

## Limitations

- Recursive cloning with large submodules (e.g., precompiled binaries) may require significant disk space and bandwidth; the full clone size is not always documented in advance.
- SSH key authentication requires prior setup of SSH keys and configuration; HTTPS may fail if credentials expire or network policies block Git protocol.
- Cloning does not verify the integrity or compatibility of submodule versions with the parent repository; mismatched submodule commits can cause downstream build failures (e.g., missing symbols in cppGoslin for ARM64).
- Windows users may encounter line-ending issues (CRLF vs. LF) if Git is not configured with `core.autocrlf=true`, causing build or execution errors on Unix-like platforms.

## Evidence

- [readme] git clone --recurse-submodules [redacted-email]:lifs-tools/lipidspace.git: "git clone --recurse-submodules [redacted-email]:lifs-tools/lipidspace.git"
- [other] LipidSpace has been built and tested under Windows 10, Ubuntu 22.04 Linux, and macOS 12+ (ARM64 / Apple Silicon), demonstrating successful compilation and execution on these target platforms.: "LipidSpace has been built and tested under Windows 10, Ubuntu 22.04 Linux, and macOS 12+ (ARM64 / Apple Silicon), demonstrating successful compilation and execution on these target platforms."
- [readme] OpenXLSX must be built from source for ARM64. A build script is provided in the repository root: "OpenXLSX must be built from source for ARM64. A build script is provided in the repository root"
- [other] Clone the lifs-tools/lipidspace repository from GitHub. Inspect the repository structure and identify the build configuration file.: "Clone the lifs-tools/lipidspace repository from GitHub. Inspect the repository structure and identify the build configuration file."
