---
name: build-artifact-validation
description: Use when after completing a platform-specific build (e.g., mvn clean
  package, qmake6 && make, cmake && make) to confirm the generated artifact is not
  corrupted and can execute on the intended OS (Windows 10, Ubuntu 22.04, macOS 12+
  ARM64, or other documented targets).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - LipidSpace
  - LipidSpaceRest
  license_tier: open
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

# build-artifact-validation

## Summary

Verify that a compiled software artifact (executable, JAR, binary, or wheel) is functional and executable on its target platform by invoking basic smoke tests. This skill confirms successful cross-platform builds and detects runtime dependency failures early.

## When to use

After completing a platform-specific build (e.g., mvn clean package, qmake6 && make, cmake && make) to confirm the generated artifact is not corrupted and can execute on the intended OS (Windows 10, Ubuntu 22.04, macOS 12+ ARM64, or other documented targets). Use this skill before packaging for distribution or documenting supported platforms.

## When NOT to use

- Build has not yet completed or artifact does not exist—run the full build first
- You are performing unit/integration testing requiring complex input data or fixtures—use the project's test suite instead
- Artifact is already packaged and distributed; use instead to validate on end-user systems post-download

## Inputs

- Build system configuration file (pom.xml, build.gradle, CMakeLists.txt, LipidSpace.pro, or setup.py)
- Compiled artifact (executable, .exe, .jar, binary, .dylib, or .whl file)
- Target platform identifier (Windows 10, Ubuntu 22.04, macOS 12+ ARM64)

## Outputs

- Verification report: artifact is executable and functional on target platform
- Runtime dependency verification (libraries accessible, linked correctly)
- Exit code and output from smoke test invocation

## How to apply

Locate the build output directory and identify the generated artifact (executable path, .exe, .jar, .so/.dylib, or .whl file). Invoke the artifact with a minimal, non-destructive command—typically --help, --version, or a dry-run flag—to confirm the binary is executable and linked correctly. On macOS ARM64, verify that runtime dylib dependencies (e.g., libcppGoslin.dylib) are accessible via DYLD_LIBRARY_PATH or co-located next to the executable. If the smoke test succeeds (exit code 0, expected output), the artifact is fit for user distribution. If it fails, trace the error (missing library, segfault, missing dependency) and re-run the full build with corrected prerequisites.

## Related tools

- **LipidSpace** (Target artifact under validation; GUI-based tool requiring QT6 runtime and platform-specific compiled binary) — https://github.com/lifs-tools/lipidspace
- **LipidSpaceRest** (Alternative REST API variant of LipidSpace; requires similar platform-specific build and runtime validation) — https://github.com/lifs-tools/lipidspace

## Examples

```
./LipidSpace --help
```

## Evaluation signals

- Smoke test (--help, --version, or minimal invocation) exits with code 0 and produces expected output without segmentation faults or undefined behavior
- All runtime dependencies (QT6 libraries, libcppGoslin.dylib on macOS, libOpenXLSX.a, openssl@3) are accessible and linked correctly
- Artifact executes on all documented target platforms (Windows 10, Ubuntu 22.04, macOS 12+ ARM64) without modification
- No missing symbol, file not found, or platform-specific runtime errors appear in stderr
- Build artifact file size and modification timestamp are consistent with the build execution timestamp

## Limitations

- Smoke tests verify only binary availability and basic execution; they do not validate functional correctness, numerical accuracy, or complex workflows
- Platform-specific dependencies (e.g., QT6, OpenSSL, CUDA) must be pre-installed on the target OS; this skill does not check for unmet system dependencies before invocation
- macOS ARM64 builds require explicit handling of dylib placement or DYLD_LIBRARY_PATH configuration; validation may fail silently if libraries are not accessible at runtime
- Validation on macOS ARM64 requires that OpenXLSX has been built from source for arm64 architecture; pre-compiled x86_64 binaries will fail with architecture mismatch errors

## Evidence

- [other] Verify compilation succeeded by checking for the generated executable, JAR, binary, or wheel artifact in the expected output directory.: "Verify compilation succeeded by checking for the generated executable, JAR, binary, or wheel artifact in the expected output directory."
- [other] Run a basic smoke test (e.g., invoking the tool with --help or a minimal input) to confirm the artifact is executable and functional on the target platform.: "Run a basic smoke test (e.g., invoking the tool with --help or a minimal input) to confirm the artifact is executable and functional on the target platform."
- [readme] LipidSpace has been built and tested under Windows 10, Ubuntu 22.04 Linux, and macOS 12+ (ARM64 / Apple Silicon), demonstrating successful compilation and execution on these target platforms.: "LipidSpace has been built and tested under Windows 10, Ubuntu 22.04 Linux, and macOS 12+ (ARM64 / Apple Silicon), demonstrating successful compilation and execution on these target platforms."
- [readme] At runtime, `libcppGoslin.dylib` must be accessible. Copy it next to the executable or set `DYLD_LIBRARY_PATH`: "At runtime, `libcppGoslin.dylib` must be accessible. Copy it next to the executable or set `DYLD_LIBRARY_PATH`"
- [readme] OpenXLSX must be built from source for ARM64. A build script is provided in the repository root: "OpenXLSX must be built from source for ARM64. A build script is provided in the repository root"
