---
name: automated-executable-distribution-generation
description: Use when you need to produce final distributable executable artifacts for a Qt5-based C++ application across multiple platforms (macOS, Windows, Linux), and you want to avoid manual build–package–release steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3552
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
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

# automated-executable-distribution-generation

## Summary

Automating the compilation and packaging of cross-platform GUI executables (macOS .app, Windows .exe, Linux binaries) using CI/CD pipelines (Appveyor, Travis) and platform-specific build tools (qmake, make, Qt5). This skill ensures reproducible, versioned distribution artifacts are generated consistently without manual intervention.

## When to use

Use this skill when you need to produce final distributable executable artifacts for a Qt5-based C++ application across multiple platforms (macOS, Windows, Linux), and you want to avoid manual build–package–release steps. Triggers include: preparing a new release version, ensuring platform parity in executable features, or reducing manual packaging errors in a multi-platform project.

## When NOT to use

- Your project does not use Qt5 or qmake-based build configuration; use platform-native build systems (CMake, Gradle, xcode) instead.
- You need real-time or on-demand builds; CI/CD pipelines are optimized for event-triggered (commit/tag) workflows, not interactive builds.
- Your target platforms are not Windows, macOS, or Linux; custom platforms require custom CI/CD agents or cross-compilation toolchains.

## Inputs

- Git repository URL (e.g., github.com/eugenemel/maven)
- build.pro (Qt project file)
- Platform-specific make_dist_*.sh scripts
- Source code (C++ with Qt5 dependencies)

## Outputs

- Windows executable (.exe file, e.g., maven_dev_*.exe)
- macOS application bundle (.app directory, e.g., Maven.app)
- Linux binary (if pipeline includes Linux; currently retired)
- Build log and CI/CD job artifacts

## How to apply

Configure a CI/CD pipeline (Appveyor for Windows/macOS, Travis for Linux) to monitor your repository for commits or tags. For each target platform, clone the repository recursively, install platform-specific build dependencies (Qt5 via Homebrew on macOS, MSYS2 on Windows, apt on Linux), configure the build with `qmake -r build.pro`, compile with `make -j4`, then generate a distributable package by running `make INSTALL_ROOT=appdir install` followed by a platform-specific shell script (e.g., `make_dist_win32.sh`, `make_dist_osx.sh`). Verify that the CI/CD service completes all stages and produces the final executable artifacts (e.g., `maven_dev_*.exe` for Windows, `Maven.app` for macOS). As of November 2024, macOS and Windows builds are produced by Appveyor; Linux builds have been retired from the automated pipeline.

## Related tools

- **Appveyor** (CI/CD platform that triggers, compiles, and packages Windows and macOS executables on each commit or tag) — https://ci.appveyor.com/project/eugenemel/maven
- **Travis CI** (CI/CD platform for Linux builds (now retired as of November 2024, but historically used)) — https://travis-ci.org/eugenemel/maven_core
- **qmake** (Qt build configuration tool; generates platform-specific Makefiles from .pro files)
- **make** (Build orchestration; compiles source code using generated Makefiles with parallel jobs (-j4))
- **Qt5** (Cross-platform GUI framework; provides the core libraries and runtime dependencies for executable)
- **MSYS2** (Windows development environment; provides MinGW toolchain, pacman package manager, and Qt5 packages for Windows builds) — http://www.msys2.org/
- **Homebrew** (macOS package manager; installs Qt5 and build tools on macOS build agents) — https://brew.sh
- **git** (Version control; clones repository recursively to fetch source and submodules) — https://github.com/eugenemel/maven

## Examples

```
qmake -r build.pro && make -j4 && make INSTALL_ROOT=appdir install && ./make_dist_win32.sh
```

## Evaluation signals

- CI/CD pipeline log shows all stages (install dependencies, configure, compile, package) completing successfully with exit code 0.
- Executable artifacts exist at expected paths and are non-empty: Windows (.exe file > 10 MB typical), macOS (.app bundle directory with executable bit set), Linux (ELF binary with execute permissions).
- Executable can be launched and responds to basic GUI initialization (no segfault or missing library errors on first run).
- Build artifacts are tagged with version identifier matching the Git tag or commit SHA, and appear in the repository's release page or CI/CD artifact store.
- Dependency tree is clean: `ldd` (Linux) or `otool -L` (macOS) or dependency walker (Windows) shows only expected Qt5 libraries and system dependencies, no broken links.

## Limitations

- Linux builds have been retired as of November 5, 2024; only Windows and macOS are currently automated. Future Linux support would require re-enabling Travis CI or switching to a unified multi-platform CI/CD service.
- qmake and Qt5 versions must match across the repository and CI/CD build agents; version mismatches can cause silent build failures or runtime incompatibilities.
- Platform-specific shell scripts (make_dist_*.sh) are not version-controlled centrally; changes to packaging logic require manual updates and testing on each platform.
- No built-in rollback or staging mechanism; failed builds may leave stale artifacts in the release pipeline, requiring manual cleanup.
- Cross-compilation (e.g., building Windows .exe on macOS) is not supported in this workflow; each platform must build on its native CI/CD agent.

## Evidence

- [readme] As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor: "As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor"
- [other] Clone repository, install build environment (Qt5, qmake, make), configure with qmake, compile with make -j4, create distributable package with make INSTALL_ROOT=appdir install and platform-specific script: "Configure the build using qmake -r build.pro. 4. Compile the project using make -j4 with parallel jobs. 5. Create a distributable package by running make INSTALL_ROOT=appdir install followed by the"
- [other] Verify AppVeyor successfully completes build stage and produces final executable artifacts: "Verify that AppVeyor successfully completes the build stage and produces the final executable artifacts (maven_dev_*.exe for Windows or Maven.app for macOS)"
- [readme] Windows requires MSYS2 platform with Qt5, zlib, sqlite; macOS requires Homebrew with Qt5; Linux requires PPA and Qt5.8, OpenGL, sqlite3: "Install the MSYS2 platform for Windows. 2. From a mingw64 prompt, install 64-bit QT, zlib, and sqlite. Install the Homebrew package management system. 2. Install the qt5 package"
- [readme] Git clone repository recursively to include submodules like maven_core: "git clone --recursive  [redacted-email]:eugenemel/maven.git maven. Cloning into 'maven_core'... https://github.com/eugenemel/maven_core/"
- [other] Release workflow: create branch, update CHANGELOG, merge PR, tag version, ensure CI/CD passes: "Once other members agree to release, merge the PR and ensure Travis and Appveyor pass. Tag with new version"
