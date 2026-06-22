---
name: software-smoke-testing
description: Use when after successful compilation or artifact generation (e.g., after `mvn clean package`, `make`, or `python setup.py build`) and before promoting the artifact to testing, distribution, or end-user deployment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - LipidSpace
  - Qt6
  - cppGoslin
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

# software-smoke-testing

## Summary

A minimal functional verification step that confirms a freshly built software artifact (executable, JAR, binary, or wheel) is executable and responds to basic invocations on the target platform. Smoke testing catches platform-specific build failures and runtime linkage issues before integration or distribution.

## When to use

After successful compilation or artifact generation (e.g., after `mvn clean package`, `make`, or `python setup.py build`) and before promoting the artifact to testing, distribution, or end-user deployment. Use this skill whenever you need rapid confirmation that the build outputs are functional on a specific OS (Windows 10, Ubuntu 22.04, macOS 12+ ARM64, etc.) without running the full test suite.

## When NOT to use

- The artifact has not yet been built or does not exist at the expected path.
- You need comprehensive functional testing; smoke testing is shallow and does not validate features, data processing, or edge cases.
- The software is already deployed and running in production; use operational health checks instead.

## Inputs

- Compiled executable (e.g., LipidSpace.exe on Windows, LipidSpace binary on Linux/macOS)
- Generated JAR or wheel artifact
- Target platform specification (OS, version, architecture)

## Outputs

- Boolean pass/fail result
- Exit code and console output (stdout/stderr) from the test invocation
- Platform/environment metadata confirming successful execution on target OS

## How to apply

Execute a minimal, non-destructive command using the generated artifact—typically a help/version query or a trivial input—to verify the binary launches without crashing and produces output on the target platform. For LipidSpace, invoke the executable with `--help` or call it with no arguments to confirm GUI initialization or CLI responsiveness. Check both exit code (should be 0 for help; non-crash for GUI) and stderr/stdout for obvious runtime errors (missing libraries, segfaults, unresolved symbols). Document the platform, OS version, artifact path, command, and outcome. This is a gate: if the smoke test fails, the build is not fit for further testing or use.

## Related tools

- **LipidSpace** (Target artifact for cross-platform smoke testing; verification of GUI/CLI responsiveness post-build) — https://github.com/lifs-tools/lipidspace
- **Qt6** (Runtime dependency for LipidSpace GUI; successful invocation confirms Qt6 libraries are linked and accessible)
- **cppGoslin** (Dynamic library dependency for LipidSpace on macOS ARM64; smoke test verifies library is locatable via DYLD_LIBRARY_PATH or co-location) — https://github.com/lifs-tools/cppgoslin

## Examples

```
./LipidSpace --help
```

## Evaluation signals

- Artifact exits with code 0 when invoked with `--help` or returns expected help text without crashes.
- No segmentation faults, unresolved symbol errors, or missing library messages (e.g., 'libcppGoslin.dylib: Datei oder Verzeichnis nicht gefunden') in stderr.
- On GUI applications, the window opens or the tool responds to graphical initialization without hanging.
- Test is reproducible on the documented target platforms (Windows 10, Ubuntu 22.04, macOS 12+ ARM64) using pre-built binaries.
- Execution time is <10 seconds for help/version queries; no timeouts indicate linkage or runtime hangs.

## Limitations

- Smoke testing only validates startup and basic responsiveness; it does not exercise core functionality (e.g., lipidome comparison, graph-based distance calculation) or data import pathways.
- Platform-specific runtime dependencies (Qt6, OpenSSL, OpenBLAS, libomp) must already be installed on the target OS; smoke testing assumes the environment is configured correctly.
- For macOS ARM64, libcppGoslin.dylib must be explicitly copied or DYLD_LIBRARY_PATH set; smoke test may fail if the dylib is missing from the bundle or path.
- GUI-based tools (like LipidSpace) cannot be fully smoke-tested in headless environments (CI/CD without display server); alternative invocation or REST API endpoint testing may be required.

## Evidence

- [other] Run a basic smoke test (e.g., invoking the tool with --help or a minimal input) to confirm the artifact is executable and functional on the target platform.: "Run a basic smoke test (e.g., invoking the tool with --help or a minimal input) to confirm the artifact is executable and functional on the target platform."
- [readme] LipidSpace has been built and tested under Windows 10, Ubuntu 22.04 Linux, and macOS 12+ (ARM64 / Apple Silicon), demonstrating successful compilation and execution on these target platforms.: "LipidSpace has been built and tested under Windows 10, Ubuntu 22.04 Linux, and macOS 12+ (ARM64 / Apple Silicon), demonstrating successful compilation and execution on these target platforms."
- [readme] At runtime, `libcppGoslin.dylib` must be accessible. Copy it next to the executable or set `DYLD_LIBRARY_PATH`: "At runtime, `libcppGoslin.dylib` must be accessible. Copy it next to the executable or set `DYLD_LIBRARY_PATH`"
- [other] Verify compilation succeeded by checking for the generated executable, JAR, binary, or wheel artifact in the expected output directory.: "Verify compilation succeeded by checking for the generated executable, JAR, binary, or wheel artifact in the expected output directory."
