---
name: wine-windows-runtime-initialization-diagnostics
description: Use when you are deploying a Windows .NET application (e.g., AirdPro CLI) inside a Docker container on a non-Windows host and need to understand whether Wine initialization completes, how long it takes (documented as >30 minutes), whether .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Wine
  - AirdPro V5
  - AirdPro V6
  - ProteoWizard
  - Docker Desktop for Mac
  - .NET Framework 4.8
  - AirdPro (V5 or V6)
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- Wine to run Windows applications in Linux containers
- AirdPro V5 is now available at 2023.7
- AirdPro V6 is now available at 2024.4
- pwiz_bindings_cli.dll from the ProteoWizard project
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aird
    doi: 10.1186/s12859-021-04490-0
    title: aird
  dedup_kept_from: coll_aird
schema_version: 0.2.0
---

# wine-windows-runtime-initialization-diagnostics

## Summary

Diagnose and document Wine initialization behavior and .NET Framework component download timing when executing Windows-compiled scientific software (such as AirdPro) in containerized Linux environments. This skill captures first-run Wine startup overhead, resource requirements, and completion signals to validate readiness for batch mass spectrometry data conversion workflows.

## When to use

You are deploying a Windows .NET application (e.g., AirdPro CLI) inside a Docker container on a non-Windows host and need to understand whether Wine initialization completes, how long it takes (documented as >30 minutes), whether .NET Framework components are downloaded and installed, and whether the application is ready to process vendor mass spectrometry raw files without timeout or incomplete initialization errors.

## When NOT to use

- The application is already running natively on Windows or using a native Windows .NET runtime; Wine initialization overhead is specific to cross-platform containerization.
- The vendor mass spectrometry file format is not supported by ProteoWizard (e.g., proprietary formats without public specifications); Wine diagnostics will not resolve format incompatibility.
- The Docker host has insufficient disk space (>10 GB recommended for .NET Framework download); initialization will fail due to resource constraints, not Wine configuration issues.

## Inputs

- Docker container image (airdpro:cli)
- Vendor mass spectrometry raw file (.raw format or other ProteoWizard-supported format)
- Input directory with volume mount permissions
- Output directory with write permissions

## Outputs

- Aird output file (.aird data file and .json index file)
- Wine initialization log output (timestamps, component downloads)
- First-run startup duration in seconds or minutes
- File integrity report (size, format signature, completeness)

## How to apply

Launch the airdpro:cli Docker container with volume mounts for input vendor raw data (e.g., .raw format) and an output directory. Execute the run-cli.sh script against a sample vendor mass spectrometry file to trigger Wine initialization and .NET Framework 4.8 component download. Monitor and record wall-clock time from container start through first successful file conversion completion. Verify the presence and integrity of the output Aird file (check file existence, size > 0, and Aird format signature). Document any Wine-related errors, package download logs, or timeout failures. Compare first-run initialization time against documented >30 minute threshold to assess whether the runtime environment is functioning as expected.

## Related tools

- **Docker Desktop for Mac** (Container runtime for launching airdpro:cli image with volume mounts and environment setup)
- **Wine** (Windows API emulation layer that initializes and downloads .NET Framework 4.8 components on first execution)
- **.NET Framework 4.8** (Windows runtime dependency installed and executed through Wine; required for AirdPro CLI execution)
- **AirdPro (V5 or V6)** (C# mass spectrometry file converter; CLI entry point via run-cli.sh; subject of Wine initialization diagnostics) — https://github.com/CSi-Studio/AirdPro
- **ProteoWizard** (Underlying library (pwiz_bindings_cli.dll) that enables vendor file format support and conversion logic in AirdPro)

## Examples

```
docker run --rm -v /path/to/vendor_raw:/input -v /path/to/output:/output airdpro:cli bash run-cli.sh /input/sample.raw /output/sample.aird && ls -lh /path/to/output/*.aird /path/to/output/*.json
```

## Evaluation signals

- First-run Wine initialization completes without timeout or critical errors; subsequent invocations skip initialization and exhibit 20-30% performance degradation compared to native Windows execution, confirming cached .NET Framework components.
- Output Aird file exists in the mounted output directory, has non-zero file size, and contains valid Aird format signature (.json index and .aird data files present with matching base name).
- Wine initialization log shows successful download and installation of .NET Framework 4.8 components; wall-clock duration is within documented >30 minute window for first run.
- No file-size overflow or incomplete conversion; verify conversion process did not terminate early due to out-of-memory or disk-space errors during Wine or framework initialization.
- Subsequent conversions on the same container (second and third runs) complete faster than first run, confirming Wine caching and initialization completion.

## Limitations

- First-run initialization takes >30 minutes due to .NET Framework component download; batch workflows must account for this startup latency or pre-warm the container image.
- Wine introduces 20-30% performance degradation compared to native Windows execution; CPU-intensive conversions of large vendor files will be slower than expected from single-threaded timing benchmarks.
- Wine requires full Linux container context (e.g., cannot run Wine inside Docker on macOS with Docker Desktop; XQuartz may be needed for GUI variants); nested virtualization or container-in-container limitations apply.
- No changelog available in the README; version-specific Wine or .NET Framework compatibility issues cannot be traced through published release notes.

## Evidence

- [methods] Wine needs to initialize and download .NET Framework components, taking more than 30 minutes: "Wine needs to initialize and download .NET Framework components, taking more than 30 minutes"
- [other] AirdPro converts vendor mass spectrometry files to Aird format; first-run execution requires Wine to initialize: "AirdPro converts vendor mass spectrometry files to Aird format; first-run execution requires Wine to initialize and download .NET Framework components, a process documented to take more than 30"
- [methods] 20-30% performance degradation when running through Wine: "20-30% performance degradation when running through Wine"
- [other] Launch the airdpro:cli container with volume mounts for input vendor raw data and output directory: "Launch the airdpro:cli container with volume mounts for input vendor raw data and output directory."
- [other] Verify that the Aird conversion process completes and produces a named output Aird file in the mounted output directory: "Verify that the Aird conversion process completes and produces a named output Aird file in the mounted output directory."
