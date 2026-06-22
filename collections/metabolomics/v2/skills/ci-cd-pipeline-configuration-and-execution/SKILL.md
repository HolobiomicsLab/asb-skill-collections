---
name: ci-cd-pipeline-configuration-and-execution
description: Use when when you have a multi-platform Qt5 C++ project (Windows, macOS, Linux) that requires automated compilation and executable packaging across different operating systems.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3552
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
  - Appveyor
  - Travis CI
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
---

# CI/CD Pipeline Configuration and Execution

## Summary

Configure and execute automated build pipelines using CI/CD platforms (Appveyor, Travis) to produce cross-platform executables from source repositories. This skill ensures reproducible, platform-specific builds of Qt5-based GUI applications with minimal manual intervention.

## When to use

When you have a multi-platform Qt5 C++ project (Windows, macOS, Linux) that requires automated compilation and executable packaging across different operating systems. Use this skill when you need to validate that source code changes successfully compile and produce distributable binaries without human intervention at build time.

## When NOT to use

- If your project does not use Qt5 or qmake—different build systems (CMake, Autotools, Cargo) require different CI/CD configuration
- If you only target a single platform (Windows, macOS, or Linux)—single-platform builds do not require cross-platform CI/CD coordination
- If your project is already building successfully locally and you have no need for automated validation on every commit

## Inputs

- Git repository URL (e.g., github.com/eugenemel/maven)
- build.pro project configuration file
- Platform-specific dependency declarations (pacman commands for MSYS2, brew for macOS, apt for Linux)
- AppVeyor configuration (appveyor.yml or web UI settings)
- Source code tree with recursive submodules

## Outputs

- Platform-specific executable binaries (maven_dev_*.exe for Windows, Maven.app for macOS)
- Distributable application packages
- Build logs and test reports from CI/CD platform
- Release artifacts published to GitHub releases page

## How to apply

Clone the repository recursively using git to ensure all submodules (e.g., maven_core) are fetched. Install platform-specific build dependencies: Qt5, qmake, make, and MSYS2 on Windows. Configure the build by running `qmake -r build.pro` to generate platform-specific makefiles. Compile with `make -j4` using parallel jobs. After successful compilation, create distributable packages by running `make INSTALL_ROOT=appdir install` followed by platform-specific shell scripts (make_dist_win32.sh, make_dist_osx.sh). Configure Appveyor CI/CD service to monitor the repository and automatically trigger builds on commits; as of November 2024, both Windows and macOS builds are produced by Appveyor (Linux builds retired). Verify successful completion by checking that AppVeyor generates final executable artifacts (maven_dev_*.exe for Windows, Maven.app for macOS) and publishes them to GitHub releases.

## Related tools

- **Appveyor** (CI/CD platform responsible for building and packaging Windows and macOS executables; triggers on repository commits and produces distributable artifacts) — https://ci.appveyor.com
- **Travis CI** (CI/CD platform for Linux builds (now retired as of November 2024 but historically used for Maven GUI)) — https://travis-ci.org
- **qmake** (Qt meta-build system that generates platform-specific makefiles from build.pro configuration)
- **make** (Build executor that compiles source code in parallel using -j4 flag)
- **MSYS2** (Windows development environment providing mingw64 compiler, pacman package manager, and dependencies (Qt5, zlib, sqlite3)) — http://www.msys2.org/
- **Homebrew** (macOS package manager for installing Qt5 and setting environment paths for qmake) — https://brew.sh
- **git** (Version control for cloning repositories recursively with submodules (e.g., maven_core)) — https://github.com

## Examples

```
git clone --recursive [redacted-email]:eugenemel/maven.git maven && cd maven && qmake -r build.pro && make -j4 && make INSTALL_ROOT=appdir install && ./make_dist_osx.sh
```

## Evaluation signals

- AppVeyor build status badge shows 'passing' (green) for all commits to master branch
- Executable artifacts are generated and differ between platforms: Windows produces .exe files, macOS produces .app bundles
- GitHub releases page contains downloadable binaries with correct version tags and checksums
- Build logs show successful completion of all stages: dependency installation, qmake configuration, make compilation, packaging script execution, and artifact publication
- Recursive git clone successfully fetches all submodules (maven_core) without SSH key errors or 'not a valid identifier' warnings

## Limitations

- Linux builds have been retired as of November 5, 2024, so Linux executables are no longer produced automatically; Linux users must compile locally
- There is a known bug in MSYS2 packages causing 'not a valid identifier' errors during git operations; workaround requires moving envsubst.exe and reinstalling gettext
- Qt5 environment variables (PKG_CONFIG_PATH, LDFLAGS, CPPFLAGS) must be manually set on macOS after Homebrew installation; failure to do so causes linking errors
- Parallel compilation with -j4 may fail on systems with insufficient RAM or CPU cores; adjustment may be needed for resource-constrained environments

## Evidence

- [intro] As of November 5, 2024, both macOS and Windows executables for Maven GUI are produced by Appveyor, with Linux builds having been retired from the automated build pipeline.: "As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor"
- [other] Clone the maven repository recursively, install Qt5/qmake/make, configure with qmake -r build.pro, compile with make -j4, and create distributable packages using platform-specific make_dist scripts.: "qmake -r build.pro
make -j4

make INSTALL_ROOT=appdir install
make_dist_[platform].sh"
- [other] MSYS2 platform installation for Windows builds with Qt5 and dependencies via pacman.: "Install the MSYS2 platform for Windows

From a mingw64 prompt, install 64-bit QT, zlib, and sqlite"
- [other] Homebrew installation for macOS with Qt5 environment variable setup.: "Install the Homebrew package management system

Install the qt5 package

export PATH="/usr/local/opt/qt/bin:$PATH""
- [readme] Known MSYS2 bug causing git clone failure with export identifier error; requires envsubst workaround.: "There is a bug in MSYS2 packages that causes the following error: Cloning into 'maven_core'... export: `dashless

[WORKAROUND] mv /mingw64/bin/envsubst.exe /mingw64/bin/envsubst.exe.orig"
- [other] Verification that AppVeyor produces platform-specific executables.: "Verify that AppVeyor successfully completes the build stage and produces the final executable artifacts (maven_dev_*.exe for Windows or Maven.app for macOS)"
