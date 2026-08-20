---
name: cross-platform-build-environment-setup
description: Use when when you have a Qt5 C++ project (such as Maven GUI or Maven
  Core) that must be built on multiple target operating systems, and you need to install
  and verify platform-specific build dependencies (MSYS2 + mingw64 on Windows, Homebrew
  + Qt5 on macOS, PPA + Qt5.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Maven GUI
  - git
  - qmake
  - make
  - Qt5
  - MSYS2
  - Homebrew
  - pacman
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo12080684
  title: MAVEN2
evidence_spans:
- 'Maven GUI: Metabolomics Analysis and Visualization Engine'
- git clone --recursive [redacted-email]:eugenemel/maven.git maven
- qmake -r build.pro
- make -j4
- Install the qt5 package
- Install the MSYS2 platform for Windows
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_maven2_cq
    doi: 10.3390/metabo12080684
    title: MAVEN2
  dedup_kept_from: coll_maven2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12080684
  all_source_dois:
  - 10.3390/metabo12080684
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-platform-build-environment-setup

## Summary

Configure and validate native build environments for Qt5-based metabolomics software across Windows, macOS, and Linux platforms. This skill ensures dependency resolution, compiler toolchain setup, and environment variable configuration so that source code compiles to platform-specific executables.

## When to use

When you have a Qt5 C++ project (such as Maven GUI or Maven Core) that must be built on multiple target operating systems, and you need to install and verify platform-specific build dependencies (MSYS2 + mingw64 on Windows, Homebrew + Qt5 on macOS, PPA + Qt5.8 on Linux), set up compiler paths and library search paths, and confirm that qmake and make can successfully compile the project without missing dependencies or linker errors.

## When NOT to use

- The project does not depend on Qt5 or uses a different build system (e.g., CMake, Meson, setuptools); use the appropriate toolchain setup for that system instead.
- You are cross-compiling to a platform different from the host machine; this skill covers native builds only.
- Binary executables are already provided or the project is pre-packaged as a Docker image; environment setup is not needed.

## Inputs

- Qt5-based C++ project source tree (e.g., git clone eugenemel/maven)
- build.pro or similar qmake project configuration file
- Target platform identifier (Windows, macOS, or Linux with specific version)

## Outputs

- Installed and verified Qt5 development toolchain on target platform
- Set environment variables (PATH, LDFLAGS, CPPFLAGS, PKG_CONFIG_PATH) specific to platform
- Successful qmake configuration (build files generated in build directory)
- Compiled object files and, optionally, intermediate build artifacts ready for packaging

## How to apply

Begin by identifying the target platform and installing the appropriate package manager and base development toolchain: MSYS2 with pacman on Windows, Homebrew on macOS, or apt-get with PPA on Linux (Ubuntu 16.04 LTS). For each platform, install Qt5 and required libraries (sqlite3, zlib, libssl-dev, mesa-common-dev on Linux) using the platform's native package manager. On Windows, after MSYS2 installation, run pacman commands to install mingw-w64-x86_64-qt-creator and dependencies; on macOS, use brew install qt5 followed by explicit PATH, LDFLAGS, CPPFLAGS, and PKG_CONFIG_PATH exports; on Linux, add the Qt5.8 PPA and install qt58-meta-minimal plus OpenGL and database development libraries. After dependency installation, validate the environment by running qmake -r build.pro to configure the build, then make -j4 to compile with parallel jobs. If compilation succeeds without unresolved symbol errors or missing header files, the environment is correctly configured.

## Related tools

- **MSYS2** (Provides mingw64 compiler toolchain and pacman package manager for Windows build environment setup) — http://www.msys2.org/
- **Homebrew** (Package manager for macOS; used to install Qt5 and development libraries)
- **Qt5** (Cross-platform GUI framework; core build dependency providing qmake and Qt libraries)
- **qmake** (Qt build configuration tool; parses build.pro and generates platform-specific Makefiles)
- **make** (GNU build automation tool; compiles source code using generated Makefiles with parallel job support (-j4))
- **pacman** (MSYS2 package manager for Windows; installs Qt, git, zlib, sqlite3, and development tools) — https://github.com/msys2/MSYS2-packages
- **git** (Version control; clones project source trees recursively to obtain Maven and Maven Core dependencies)

## Examples

```
pacman -S --needed --noconfirm mingw-w64-x86_64-qt-creator zlib-devel mingw64/mingw-w64-x86_64-sqlite3 && git clone --recursive [redacted-email]:eugenemel/maven.git maven && cd maven && qmake -r build.pro && make -j4
```

## Evaluation signals

- qmake -r build.pro completes without errors and generates Makefile or platform-specific build configuration files in the build directory.
- make -j4 runs to completion without 'command not found', 'unresolved external symbol', or 'No rule to make target' errors.
- All required header files (Qt5 headers, sqlite3.h, zlib.h, openssl headers) are found during compilation; no '#include' resolution errors.
- Compiler and linker flags (LDFLAGS, CPPFLAGS, PKG_CONFIG_PATH) are correctly set, verified by examining qmake output or build log for expected -L and -I paths.
- Final executable artifact is generated in the expected location (maven_dev_*.exe on Windows, Maven.app on macOS, or binary in Linux build output).

## Limitations

- Platform-specific build configurations require separate setup and validation on each target OS; a build environment validated on macOS will not produce Windows executables without re-running setup on a Windows machine or CI/CD pipeline.
- Qt5 path and environment variable setup is brittle and platform-specific; incorrect LDFLAGS, CPPFLAGS, or PKG_CONFIG_PATH on macOS or Linux will cause silent linker failures or missing library errors.
- Linux builds require a specific PPA (beineri/opt-qt58-xenial) for Ubuntu 16.04 LTS; other Linux distributions may require different Qt5 installation methods and library paths.
- MSYS2 on Windows contains known bugs (e.g., envsubst export identifier error documented in maven_core README); workarounds such as renaming /mingw64/bin/envsubst.exe may be required.
- As of November 5, 2024, Linux builds have been retired from the automated build pipeline for Maven GUI, so Linux build environment setup is no longer maintained in CI/CD; manual validation may be needed.

## Evidence

- [readme] Install the MSYS2 platform for Windows, then from a mingw64 prompt, install 64-bit QT, zlib, and sqlite: "Install the [MSYS2 platform for Windows](http://www.msys2.org/)

2.  From a mingw64 prompt, install 64-bit QT, zlib, and sqlite"
- [readme] On macOS, install Homebrew and Qt5, then export PATH, LDFLAGS, CPPFLAGS, and PKG_CONFIG_PATH: "Install the [Homebrew package management system]()

2.  Install the qt5 package

        brew update
        brew install qt5

3.  Setup the environment for the newly installed qt5

        export"
- [other] Configure the build using qmake -r build.pro and compile using make -j4 with parallel jobs: "3. Configure the build using qmake -r build.pro. 4. Compile the project using make -j4 with parallel jobs."
- [readme] There is a known bug in MSYS2 packages causing an export identifier error during git clone on Windows: "*Note*: There is a [bug in MSYS2 packages](https://github.com/Alexpux/MSYS2-packages/issues/735) that causes the following error"
- [intro] As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor: "As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor"
