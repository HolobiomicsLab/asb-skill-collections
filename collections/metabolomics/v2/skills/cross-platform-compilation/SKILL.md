---
name: cross-platform-compilation
description: Use when when releasing a new version of a tool, onboarding to a new development platform, or validating that a tool meets its documented platform support claims (e.g., Windows 10, Ubuntu 22.04, macOS 12+ ARM64). Apply this skill before publishing binaries or claiming multi-platform support.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - LipidSpace
  - Qt6
  - cppgoslin
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

# cross-platform-compilation

## Summary

Verify that a bioinformatics tool successfully compiles and executes on documented target platforms (Windows, Linux, macOS) by following platform-specific build procedures and smoke-testing the resulting artifacts. This skill ensures reproducibility and accessibility of the tool across operating systems.

## When to use

When releasing a new version of a tool, onboarding to a new development platform, or validating that a tool meets its documented platform support claims (e.g., Windows 10, Ubuntu 22.04, macOS 12+ ARM64). Apply this skill before publishing binaries or claiming multi-platform support.

## When NOT to use

- Tool is distributed only as a web service or SaaS platform without client binaries.
- Target platform is not listed in the tool's documented supported OS list.
- Build dependencies are not publicly available or require proprietary toolchains.

## Inputs

- Git repository URL with full source code and submodules
- Documentation of target platforms and build requirements
- Build configuration files (qmake .pro, CMakeLists.txt, pom.xml, setup.py, or Dockerfile)

## Outputs

- Compiled executable or binary artifact (EXE, binary, JAR, wheel, or DMG)
- Build log confirming compilation success on each target platform
- Smoke-test results (tool invocation with --help, example dataset import, or minimal analysis run)
- List of platform-specific runtime dependencies and library paths

## How to apply

Clone the repository with all submodules, identify the build system (qmake, Maven, CMake, etc.), install platform-specific build dependencies (Qt6 libraries, compilers, OpenSSL, development headers), execute the platform-appropriate build command (e.g., `qmake6 LipidSpace.pro && make`), verify the expected output artifact exists in the build directory, and run a smoke test (e.g., `--help` or loading example data) to confirm the executable is functional. On macOS ARM64, special attention to bundled dylibs and architecture-specific compilation (e.g., OpenXLSX built from source for arm64) is required. Document any platform-specific workarounds or library paths needed at runtime.

## Related tools

- **LipidSpace** (Lipidomics analysis tool used as exemplar for cross-platform compilation testing) — https://github.com/lifs-tools/lipidspace
- **Qt6** (GUI framework required for LipidSpace builds; platform-specific installation via Homebrew, apt, or source)
- **cppgoslin** (Lipid parsing library dependency; must be built and installed before LipidSpace compilation) — https://github.com/lifs-tools/cppgoslin

## Examples

```
git clone --recurse-submodules [redacted-email]:lifs-tools/lipidspace.git && cd lipidspace && qmake6 LipidSpace.pro && make && ./LipidSpace --help
```

## Evaluation signals

- Build completes without errors on all three target platforms (Windows 10, Ubuntu 22.04, macOS 12+ ARM64).
- Compiled executable exists in expected output directory (e.g., Build/ folder for qmake, or .exe/.sh/.app for native builds).
- Smoke test succeeds: tool responds to --help, loads bundled example dataset, or completes minimal analysis without segfault/runtime error.
- No unresolved shared library references at runtime (check with `ldd`, `otool -L`, or `objdump -p` depending on platform).
- Platform-specific workarounds documented (e.g., DYLD_LIBRARY_PATH on macOS, qmake6 PATH export, OpenXLSX arm64 build script).

## Limitations

- macOS ARM64 requires special handling: OpenXLSX must be built from source using the provided build script; libcppGoslin.dylib must be copied or DYLD_LIBRARY_PATH set at runtime.
- Qt6 is a heavyweight GUI dependency; installation and version compatibility can vary by platform and package manager.
- Windows build procedures are not detailed in the provided README; only qmake-based Linux/macOS builds are documented.
- Build times and disk space requirements vary significantly by platform and dependency caching state.
- Some features (e.g., NVIDIA CUDA GPU acceleration) are optional and require additional hardware/drivers not present on all platforms.

## Evidence

- [readme] LipidSpace has been built and tested under Windows 10, Ubuntu 22.04 Linux, and macOS 12+ (ARM64 / Apple Silicon), demonstrating successful compilation and execution on these target platforms.: "LipidSpace has been built and tested under Windows 10, Ubuntu 22.04 Linux, and macOS 12+ (ARM64 / Apple Silicon)"
- [other] Clone the repository, inspect build configuration files, install platform-specific dependencies, execute the build command, verify the generated artifact, and run a smoke test.: "Clone the lifs-tools/lipidspace repository from GitHub. 2. Inspect the repository structure and identify the build configuration file (e.g., pom.xml, build.gradle, CMakeLists.txt, or setup.py). 3."
- [readme] Qt6 is required for the GUI; macOS requires Homebrew-installed Qt, Linux requires qt6-base-dev from apt.: "LipidSpace uses the QT6 libraries for the graphical user interface."
- [readme] OpenXLSX must be compiled from source for ARM64; a build script is provided.: "OpenXLSX must be built from source for ARM64. A build script is provided in the repository root"
- [readme] qmake6 and make are the standard build commands; runtime library paths must be set on macOS.: "qmake6 LipidSpace.pro
make

At runtime, `libcppGoslin.dylib` must be accessible. Copy it next to the executable or set `DYLD_LIBRARY_PATH`"
