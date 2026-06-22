---
name: dependency-resolution-for-build-environments
description: Use when when preparing to build LipidSpace or similar desktop/CLI applications from source across multiple target platforms (Windows 10, Ubuntu 22.04, macOS 12+ ARM64), or when encountering build failures due to missing headers, libraries, or incompatible tool versions.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - LipidSpace
  - Homebrew
  - apt (Ubuntu package manager)
  - Qt6
  - CMake
  - OpenXLSX
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
---

# dependency-resolution-for-build-environments

## Summary

Identify, install, and verify platform-specific build dependencies and runtime libraries required to compile and execute cross-platform scientific software. This skill ensures that all prerequisite tools, compilers, and libraries are correctly resolved before the build process begins.

## When to use

When preparing to build LipidSpace or similar desktop/CLI applications from source across multiple target platforms (Windows 10, Ubuntu 22.04, macOS 12+ ARM64), or when encountering build failures due to missing headers, libraries, or incompatible tool versions.

## When NOT to use

- Binary distributions or precompiled packages are available and installation is preferred over building from source.
- The target platform is not among the documented supported OS list (e.g., attempting to build on unsupported Linux distributions or older macOS versions).
- The development environment already has all dependencies installed and verified; focus should move to the build configuration step.

## Inputs

- Repository clone with build configuration files (CMakeLists.txt, LipidSpace.pro, etc.)
- Target operating system identifier (Windows 10, Ubuntu 22.04, macOS 12+ ARM64)
- README or build documentation listing prerequisites

## Outputs

- Verified installation of all build tools (compilers, qmake, cmake, git)
- Verified installation of runtime libraries (Qt6, OpenSSL, BLAS, OpenMP, OpenXLSX)
- Populated PATH and library environment variables (LD_LIBRARY_PATH, DYLD_LIBRARY_PATH, etc.)
- Success indicator: ability to invoke key tools (e.g., qmake6 --version) without error

## How to apply

First, inspect the repository's build configuration files (e.g., CMakeLists.txt, qmake .pro files, pom.xml, setup.py) and any platform-specific build instructions in the README to identify declared dependencies. For each target OS, install the corresponding package set using the native package manager (Homebrew on macOS, apt on Ubuntu, etc.). On macOS ARM64, special attention must be paid to architecture-specific builds: verify that prebuilt libraries target arm64 or build from source if needed (e.g., OpenXLSX via provided build scripts). After installation, confirm that critical binaries (qmake6, cmake, git) are discoverable on the PATH, and that library paths are correctly exported (e.g., DYLD_LIBRARY_PATH on macOS). Only after successful dependency resolution proceed to configure and compile.

## Related tools

- **Homebrew** (Package manager for macOS; used to install Qt6, OpenSSL, CMake, Git, and other build dependencies on ARM64 systems) — https://brew.sh
- **apt (Ubuntu package manager)** (System package manager; used to install Qt6 dev libraries, build-essential, OpenBLAS, libomp, Mesa, and SSL libraries on Ubuntu 22.04)
- **Qt6** (GUI framework; core runtime and build-time dependency for LipidSpace compilation via qmake6) — https://www.qt.io/product/qt6
- **CMake** (Build system configuration tool; used to build OpenXLSX dependency from source on macOS ARM64)
- **OpenXLSX** (Library for reading/writing Excel files; must be built from source on macOS ARM64 targeting arm64 architecture) — https://github.com/lifs-tools/lipidspace

## Examples

```
brew install qt libomp openssl@3 cmake git && export PATH="/opt/homebrew/opt/qt/bin:$PATH" && xcode-select --install && chmod +x build-openxlsx-macos-arm64.sh && ./build-openxlsx-macos-arm64.sh
```

## Evaluation signals

- Platform-specific package installation command (apt install, brew install) completes without errors.
- Key build tool invocations return version information without 'command not found' errors (e.g., qmake6 --version, cmake --version).
- Library header files are discoverable during the build configuration step (no fatal errors like 'lipidspace/CBTableWidget.h: Datei oder Verzeichnis nicht gefunden').
- On macOS ARM64, architecture-specific library validation passes (e.g., `file libcppGoslin.dylib` confirms arm64 Mach-O format).
- The subsequent build command (qmake6 LipidSpace.pro && make) progresses past the initial dependency check phase without linker errors.

## Limitations

- Qt6 availability varies significantly across Linux distributions; Ubuntu 22.04 is explicitly documented; older distributions may require manual Qt6 build or backported packages.
- ARM64 support on macOS requires architecture-specific builds for dependencies like OpenXLSX; prebuilt binaries for x86_64 will not work and must be recompiled.
- cppgoslin library must be installed system-wide on macOS (make && sudo make install) before LipidSpace compilation; installation errors are not automatically reported until link time.
- NVIDIA CUDA support for GPU-accelerated builds requires matching architecture (sm_89 for L4 GPUs); mismatches will silently produce code that does not use the GPU.
- No changelog is available, making it difficult to track dependency version changes across releases.

## Evidence

- [readme] LipidSpace uses the QT6 libraries for the graphical user interface.: "LipidSpace uses the [QT6](https://www.qt.io/product/qt6) libraries for the graphical user interface."
- [readme] On Ubuntu 22.04, install build-essential, Qt6 dev tools, libqt6svg6-dev, libqt6charts6-dev, libopenblas-dev, libomp-dev, mesa, libglu1, and libssl-dev.: "sudo apt install build-essential libfontconfig1 qt6-base-dev qt6-base-dev-tools libqt6svg6-dev libqt6charts6-dev libopenblas-dev libomp-dev mesa-common-dev libglu1-mesa-dev libc6 libstdc++6 libssl-dev"
- [readme] On macOS ARM64, install Homebrew dependencies and ensure Xcode Command Line Tools are present, then build OpenXLSX from source.: "brew install qt libomp openssl@3 cmake git"
- [readme] OpenXLSX must be built from source for ARM64 targeting arm64 architecture using a provided build script.: "OpenXLSX must be built from source for ARM64. A build script is provided in the repository root"
- [readme] The latest cppgoslin library must be installed system-wide; build errors indicate missing header files if not installed.: "Please make sure that you have the latest version of cppgoslin (https://github.com/lifs-tools/cppgoslin) installed on your computer (make && sudo make install)."
- [readme] LipidSpace has been built and tested on Windows 10, Ubuntu 22.04, and macOS 12+ ARM64.: "LipidSpace has been built and tested under Windows 10, Ubuntu 22.04 Linux, and macOS 12+ (ARM64 / Apple Silicon)."
