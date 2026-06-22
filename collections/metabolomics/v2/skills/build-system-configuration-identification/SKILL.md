---
name: build-system-configuration-identification
description: Use when you have cloned a source repository and need to compile it on a supported operating system (Windows 10, Ubuntu 22.04, macOS 12+ ARM64) but do not know what build tools, dependencies, or compilation commands are required.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3364
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - LipidSpace
  - qmake
  - CMake
  - Homebrew
  - apt (Advanced Package Tool)
  - git
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# build-system-configuration-identification

## Summary

Identify and analyze the build configuration file(s) in a source repository to determine dependencies, compilation targets, and platform-specific requirements before attempting cross-platform compilation. This skill enables reproducible builds by extracting metadata about the build system (e.g., Maven, Gradle, CMake, qmake) and its configuration parameters.

## When to use

You have cloned a source repository and need to compile it on a supported operating system (Windows 10, Ubuntu 22.04, macOS 12+ ARM64) but do not know what build tools, dependencies, or compilation commands are required. Use this skill when the repository structure is unfamiliar or when you need to verify platform-specific build requirements before proceeding.

## When NOT to use

- The software is distributed as a pre-compiled binary or wheel (no build system analysis needed).
- You are working with a containerized build (Docker) where the Dockerfile already specifies all dependencies — extract from the Dockerfile instead.
- The repository has no build configuration file or is a documentation-only or data-only repository.

## Inputs

- GitHub repository URL or local repository clone
- Target operating system (Windows 10, Ubuntu 22.04, macOS 12+ ARM64, or Linux distribution)

## Outputs

- Build configuration file(s) identified (path and format)
- List of platform-specific dependencies and versions
- Build command sequence (qmake/cmake/mvn invocation)
- Optional: Dependency installation commands per OS

## How to apply

Inspect the repository root and key subdirectories for build configuration files such as pom.xml (Maven), build.gradle (Gradle), CMakeLists.txt (CMake), LipidSpace.pro (qmake), setup.py (Python setuptools), or Dockerfile (containerized builds). Extract platform-specific dependencies listed in the configuration (e.g., Qt6, OpenSSL, compiler flags, GPU acceleration options like CUDA). For multi-platform projects, cross-reference the identified build system with platform-specific prerequisites documented in the README (e.g., Homebrew packages on macOS, apt packages on Ubuntu). Document the exact qmake or make commands required (e.g., 'qmake6 LipidSpace.pro && make'). Verify that dependency versions match the documented target OS versions to avoid incompatibility.

## Related tools

- **qmake** (Build configuration and generation for Qt-based projects; invoked to generate makefiles from .pro files) — https://doc.qt.io/qt-6/qmake-manual.html
- **CMake** (Platform-agnostic build configuration tool; generates native build files for the target OS) — https://cmake.org/
- **Homebrew** (MacOS package manager used to install build dependencies (Qt6, OpenSSL, libomp)) — https://brew.sh
- **apt (Advanced Package Tool)** (Linux package manager for Ubuntu; installs build essentials, Qt6, OpenBLAS, Mesa, and SSL libraries) — https://wiki.debian.org/Apt
- **git** (Version control and submodule management; used with --recurse-submodules flag for dependency cloning) — https://github.com/lifs-tools/lipidspace
- **LipidSpace** (Target application; Qt6-based GUI tool for lipidome analysis with platform-specific binary distributions) — https://github.com/lifs-tools/lipidspace

## Examples

```
git clone --recurse-submodules [redacted-email]:lifs-tools/lipidspace.git && cd lipidspace && qmake6 LipidSpace.pro && make
```

## Evaluation signals

- Build configuration file (e.g., LipidSpace.pro, CMakeLists.txt) exists in repository root and is parseable for key parameters (target OS, Qt version, compiler flags).
- All declared dependencies in the build configuration can be installed via the documented package manager (Homebrew on macOS, apt on Ubuntu).
- Platform-specific build commands complete without syntax or configuration errors (qmake6 successfully generates makefiles; cmake finds all required libraries).
- Generated build artifacts (executable, .dylib, .so, or .dll) are present in the expected output directory after compilation.
- Documented build command sequence matches the repository's CI/CD workflow file (e.g., GitHub Actions .yml) for that platform.

## Limitations

- ARM64 builds on macOS require custom compilation of OpenXLSX from source (pre-built binaries not provided for all architectures); this adds build time and complexity.
- Some Qt6 dependencies may not be available in older package manager versions; Ubuntu 22.04 is the minimum tested version on Linux.
- Optional NVIDIA CUDA acceleration for GPU-based distance calculations requires L4-family GPUs and separate CUDA installation; build succeeds without it but performance is reduced.
- The cppgoslin library must be separately installed and made discoverable via library paths (DYLD_LIBRARY_PATH on macOS, LD_LIBRARY_PATH on Linux) after identifying it in the build configuration.
- Build errors related to missing includes (e.g., 'lipidspace/CBTableWidget.h not found') indicate outdated cppgoslin; build configuration identification alone does not resolve this — reinstallation of the dependency is required.

## Evidence

- [other] Inspect the repository structure and identify the build configuration file (e.g., pom.xml, build.gradle, CMakeLists.txt, or setup.py).: "Inspect the repository structure and identify the build configuration file (e.g., pom.xml, build.gradle, CMakeLists.txt, or setup.py)."
- [other] Install platform-specific build dependencies and runtime requirements (e.g., Java Development Kit for Maven-based projects, compilers, or runtime libraries).: "Install platform-specific build dependencies and runtime requirements (e.g., Java Development Kit for Maven-based projects, compilers, or runtime libraries)."
- [readme] On Ubuntu 22.04, you can run sudo apt install build-essential libfontconfig1 qt6-base-dev qt6-base-dev-tools libqt6svg6-dev libqt6charts6-dev libopenblas-dev libomp-dev mesa-common-dev libglu1-mesa-dev libc6 libstdc++6 libssl-dev: "On Ubuntu 22.04, you can run sudo apt install build-essential libfontconfig1 qt6-base-dev qt6-base-dev-tools libqt6svg6-dev libqt6charts6-dev libopenblas-dev libomp-dev mesa-common-dev"
- [readme] brew install qt libomp openssl@3 cmake git: "brew install qt libomp openssl@3 cmake git"
- [readme] OpenXLSX must be built from source for ARM64. A build script is provided in the repository root: "OpenXLSX must be built from source for ARM64. A build script is provided in the repository root"
- [readme] git clone --recurse-submodules [redacted-email]:lifs-tools/lipidspace.git: "git clone --recurse-submodules [redacted-email]:lifs-tools/lipidspace.git"
- [readme] LipidSpace has been built and tested under Windows 10, Ubuntu 22.04 Linux, and macOS 12+ (ARM64 / Apple Silicon).: "LipidSpace has been built and tested under Windows 10, Ubuntu 22.04 Linux, and macOS 12+ (ARM64 / Apple Silicon)."
