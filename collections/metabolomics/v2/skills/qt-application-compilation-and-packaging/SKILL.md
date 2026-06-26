---
name: qt-application-compilation-and-packaging
description: Use when you have a Qt5-based C++ GUI application source tree (e.g.,
  Maven GUI) that must be compiled and packaged for end-user distribution across macOS
  and Windows platforms, especially when automated builds are managed by CI/CD services
  (AppVeyor, Travis).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3552
  edam_topics:
  - http://edamontology.org/topic_0659
  tools:
  - Maven GUI
  - git
  - qmake
  - make
  - Qt5
  - MSYS2
  - Homebrew
  - pacman
  - Appveyor
  - Travis
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

# Qt Application Compilation and Packaging

## Summary

This skill automates the compilation and distribution of Qt-based GUI applications across multiple platforms (macOS, Windows, Linux) using qmake, make, and platform-specific packaging scripts. It is essential for creating reproducible, distributable binaries from Qt source code within a CI/CD environment.

## When to use

Apply this skill when you have a Qt5-based C++ GUI application source tree (e.g., Maven GUI) that must be compiled and packaged for end-user distribution across macOS and Windows platforms, especially when automated builds are managed by CI/CD services (AppVeyor, Travis). Use it when the project uses qmake as its build configuration tool and requires both platform-specific executables (.exe for Windows, .app for macOS) and distributable packages.

## When NOT to use

- When the Qt application uses CMake instead of qmake as the primary build system—adapt the configuration step accordingly.
- When targeting platforms for which automated CI/CD builds have been retired (e.g., Linux builds for Maven GUI as of November 2024), unless you manually configure a new CI/CD platform or build locally.
- When the application lacks platform-specific distribution scripts (make_dist_*.sh) or when the build environment cannot satisfy Qt5 and compiler dependencies for the target platform.

## Inputs

- Qt5 C++ source tree with qmake project files (build.pro, .pro files)
- Linked git submodules or dependencies (e.g., maven_core library)
- Platform-specific environment (macOS with Homebrew, Windows with MSYS2/mingw64, or Linux with Qt5 PPA)

## Outputs

- Platform-specific executable (maven_dev_*.exe for Windows, Maven.app for macOS)
- Distributable package archive or installer
- Build artifacts verified by CI/CD platform (AppVeyor, Travis)

## How to apply

First, clone the Qt application repository recursively (e.g., `git clone --recursive [redacted-email]:eugenemel/maven.git maven`) to obtain the main project and all linked dependencies. Set up the build environment by installing Qt5 development libraries and build tools appropriate to the target platform: on macOS use Homebrew (e.g., `brew install qt5`); on Windows use MSYS2 with mingw64 packages (e.g., `pacman -S mingw-w64-x86_64-qt-creator`). Configure the build by invoking `qmake -r build.pro` to generate platform-specific Makefiles, then compile using `make -j4` with parallel jobs for speed. Finally, create a distributable package by installing to a temporary root directory (`make INSTALL_ROOT=appdir install`) and running the platform-specific distribution script (e.g., `make_dist_osx.sh` or `make_dist_win32.sh`), which generates the final executable artifact (Maven.app for macOS or maven_dev_*.exe for Windows). Verify successful build completion by checking that the CI/CD platform (AppVeyor as of November 2024 for Maven GUI) reports a passed build stage and produces the expected binary artifact.

## Related tools

- **qmake** (Qt build configuration generator; invoked to translate .pro files into platform-specific Makefiles) — http://doc.qt.io/
- **make** (GNU build automation tool; executes Makefile targets to compile source and install artifacts)
- **git** (Version control and recursive repository cloning for obtaining Qt application source and linked submodules) — https://github.com
- **Qt5** (C++ framework and libraries providing GUI components, signals/slots, and cross-platform abstractions for the application) — https://www.qt.io/
- **Homebrew** (Package manager for macOS; used to install Qt5 development libraries and build tools (qmake, make)) — https://brew.sh/
- **MSYS2** (Unix-like environment and package manager for Windows; provides mingw64 toolchain, Qt5, zlib, sqlite3, and build utilities) — https://www.msys2.org/
- **Appveyor** (CI/CD platform responsible for automated compilation and packaging of macOS and Windows executables) — https://ci.appveyor.com/project/eugenemel/maven
- **Travis** (Legacy CI/CD platform (retired for Maven GUI as of Nov 2024) previously used for Linux builds) — https://travis-ci.org/eugenemel/maven_core

## Examples

```
git clone --recursive [redacted-email]:eugenemel/maven.git maven && cd maven && qmake -r build.pro && make -j4 && make INSTALL_ROOT=appdir install && ./make_dist_osx.sh
```

## Evaluation signals

- CI/CD platform (AppVeyor) build stage completes successfully with no compilation or linking errors.
- Expected executable artifacts are produced: Maven.app (macOS) or maven_dev_*.exe (Windows) in the specified output directory.
- The final package passes verification checks performed by the CI/CD platform, confirming the binary is ready for distribution.
- Recursive git clone and qmake configuration complete without dependency or environment setup errors on each target platform.
- Platform-specific distribution scripts execute without error and produce a distributable package (not just raw binaries) suitable for end-user installation.

## Limitations

- Linux automated builds for Maven GUI have been retired as of November 5, 2024; only macOS and Windows are currently supported via AppVeyor CI/CD.
- MSYS2 on Windows has a known bug (issue #735) that can cause git operations to fail with an 'not a valid identifier' error during environment variable export; requires manual workaround (e.g., moving envsubst.exe and installing gettext).
- Build success depends on platform-specific availability of Qt5 development libraries; different package managers and versions (Homebrew on macOS, pacman on MSYS2, apt on Linux Ubuntu) introduce platform-specific configuration overhead.

## Evidence

- [intro] As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor: "As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor"
- [other] git clone --recursive [redacted-email]:eugenemel/maven.git maven; qmake -r build.pro; make -j4: "git clone --recursive  [redacted-email]:eugenemel/maven.git maven"
- [other] qmake -r build.pro; make -j4 compilation workflow: "qmake -r build.pro
make -j4"
- [other] make INSTALL_ROOT=appdir install; make_dist_[platform].sh distribution script invocation: "make INSTALL_ROOT=appdir install
make_dist_[platform].sh"
- [readme] Install Qt5, qmake, and make on target platform via Homebrew or MSYS2: "Install the qt5 package"
- [readme] MSYS2 known bug causing environment variable identifier error during git operations: "There is a [bug in MSYS2 packages](https://github.com/Alexpux/MSYS2-packages/issues/735) that causes the following error"
- [other] Verify AppVeyor successfully completes build stage and produces final executable artifacts: "Verify that AppVeyor successfully completes the build stage and produces the final executable artifacts (maven_dev_*.exe for Windows or Maven.app for macOS)"
