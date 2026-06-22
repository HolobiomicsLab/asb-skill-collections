---
name: metabolomics-software-build-reproducibility
description: Use when when developing or maintaining a multi-platform metabolomics GUI tool (such as Maven GUI) that must produce binary executables for end users, and you need to ensure that builds are reproducible across different OS platforms, dependency versions are pinned and tracked, and release artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0092
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
  - Maven (GUI)
  - maven_core
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-software-build-reproducibility

## Summary

Establish and maintain reproducible automated build pipelines for metabolomics analysis software across multiple platforms (macOS, Windows, Linux) using containerized CI/CD environments. This skill ensures that metabolomics tools like Maven GUI can be reliably compiled, packaged, and distributed with consistent dependency resolution and executable artifacts.

## When to use

When developing or maintaining a multi-platform metabolomics GUI tool (such as Maven GUI) that must produce binary executables for end users, and you need to ensure that builds are reproducible across different OS platforms, dependency versions are pinned and tracked, and release artifacts are automatically generated without manual compilation steps on each developer's machine.

## When NOT to use

- If the metabolomics software is pure Python, R, or another interpreted language with no compiled components — containerized package distribution (conda, pip, CRAN) may be simpler than binary CI/CD.
- If you only need to build for a single target platform — simpler local or single-platform CI/CD may suffice; multi-platform orchestration introduces complexity.
- If the metabolomics tool has no external GUI or binary distribution requirement (e.g., a command-line-only or web-hosted service) — this skill is specific to desktop GUI applications with downloadable executables.

## Inputs

- Git repository (eugenemel/maven or similar metabolomics tool source)
- Build configuration files (build.pro for qmake, INSTALL_ROOT settings, platform-specific make_dist scripts)
- Dependency specification (Qt5 version, zlib, sqlite3, etc.)
- CI/CD pipeline configuration (appveyor.yml, .travis.yml, or equivalent)

## Outputs

- Platform-specific executable binaries (maven_dev_*.exe for Windows, Maven.app bundle for macOS, AppImage or tarball for Linux)
- CI/CD build logs and status reports (pass/fail, artifact URLs)
- Release artifacts published to GitHub Releases or equivalent distribution channel
- Dependency lock files or pin specifications captured in CI/CD configuration

## How to apply

Set up platform-specific CI/CD jobs (e.g. Appveyor for Windows and macOS, Travis for Linux) that clone the repository recursively, install pinned versions of build dependencies (Qt5, qmake, make, gcc/clang via package managers like MSYS2 on Windows or Homebrew on macOS), configure the build with qmake -r build.pro, compile with make -j4 using parallel jobs, and generate distributable packages by running make INSTALL_ROOT=appdir install followed by platform-specific packaging scripts (make_dist_win32.sh, make_dist_osx.sh, make_dist_linux.sh). Verify that CI/CD logs confirm successful compilation, linking, and artifact generation (e.g., maven_dev_*.exe for Windows or Maven.app for macOS). Monitor CI/CD platform dashboards to confirm all matrix configurations pass before tagging a release.

## Related tools

- **Appveyor** (CI/CD platform that produces both macOS and Windows executables for Maven GUI as of November 2024) — https://ci.appveyor.com/project/eugenemel/maven
- **qmake** (Qt build configuration tool; used to generate Makefiles from build.pro for cross-platform compilation)
- **make** (Build execution tool; compiles source code with parallel jobs (make -j4) to generate object files and binaries)
- **Qt5** (GUI framework and runtime library required for Maven GUI compilation and execution on all platforms)
- **MSYS2** (Windows build environment providing mingw-w64 compiler, pacman package manager, and development tools for Windows executable generation) — http://www.msys2.org/
- **Homebrew** (macOS package manager used to install Qt5 and other development dependencies for macOS builds)
- **git** (Version control and source code cloning tool; used to fetch repository and recursively clone submodules (maven_core)) — https://github.com/eugenemel/maven
- **Maven (GUI)** (Target metabolomics analysis and visualization application being built and packaged by the CI/CD pipeline) — https://github.com/eugenemel/maven
- **maven_core** (Submodule library providing core metabolomics algorithms and data structures used by Maven GUI) — https://github.com/eugenemel/maven_core

## Examples

```
git clone --recursive [redacted-email]:eugenemel/maven.git maven && cd maven && qmake -r build.pro && make -j4 && make INSTALL_ROOT=appdir install && ./make_dist_osx.sh
```

## Evaluation signals

- CI/CD build status is reported as 'passed' for all targeted platforms (Windows and macOS as of November 2024) in Appveyor dashboard or equivalent.
- Binary artifacts (maven_dev_*.exe, Maven.app) are successfully generated and appear in CI/CD artifact logs with expected file sizes and timestamps.
- Executable binaries can be launched on target OS without missing library errors or unresolved symbols, indicating correct dependency linking.
- Release tag in git matches corresponding GitHub Release entry with downloadable executable artifacts attached.
- Build logs show no compiler warnings (or only expected/suppressed warnings), no linking failures, and successful completion of all qmake, make, and packaging steps.

## Limitations

- As of November 2024, Linux builds have been retired from the automated pipeline — the skill as documented now covers only Windows and macOS; practitioners needing Linux support must maintain a separate build environment or restore Travis CI configuration.
- CI/CD platforms (Appveyor, Travis) require authentication and may have rate limits, cost, or service disruptions — a single platform outage can block releases.
- Qt5 version pinning and MSYS2/Homebrew package versions can drift or become unavailable; periodic maintenance of dependency specifications is required to keep builds reproducible over time.
- Platform-specific packaging scripts (make_dist_*.sh) must be manually maintained for each new target OS or significant build environment change; errors in packaging scripts can produce invalid or incomplete executables despite successful compilation.

## Evidence

- [readme] As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor: "As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor"
- [readme] Build workflow and dependency installation across platforms: "qmake -r build.pro
make -j4"
- [readme] Windows build environment setup with MSYS2: "Install the MSYS2 platform for Windows"
- [readme] macOS build environment setup with Homebrew: "Install the Homebrew package management system"
- [readme] Packaging and distribution workflow: "make INSTALL_ROOT=appdir install
make_dist_[platform].sh"
- [readme] Qt5 as core runtime and build dependency: "Install the qt5 package"
- [other] Recursive clone of Maven repository and submodules: "git clone --recursive  [redacted-email]:eugenemel/maven.git maven"
- [other] Recursive cloning of maven_core submodule: "Cloning into 'maven_core'... https://github.com/eugenemel/maven_core/"
- [other] CI/CD status check requirement before release merge: "Once other members agree to release, merge the PR and ensure Travis and Appveyor pass"
