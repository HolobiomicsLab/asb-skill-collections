---
name: cli-application-invocation-with-file-io-management
description: Use when when you have vendor mass spectrometry raw files (e.g., .raw format) that must be converted to an open format (Aird) using a Windows .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - AirdPro V5
  - AirdPro V6
  - ProteoWizard
  - Docker Desktop for Mac
  - Wine
  - .NET Framework 4.8
  - AirdPro V5 / V6
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro V5 is now available at 2023.7
- AirdPro V6 is now available at 2024.4
- pwiz_bindings_cli.dll from the ProteoWizard project
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aird
    doi: 10.1186/s12859-021-04490-0
    title: aird
  dedup_kept_from: coll_aird
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-021-04490-0
  all_source_dois:
  - 10.1186/s12859-021-04490-0
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CLI Application Invocation with File I/O Management

## Summary

Execute a command-line interface (CLI) application within a containerized environment with mounted input and output volumes, managing vendor mass spectrometry file conversion and monitoring first-run initialization overhead. This skill is essential when batch-processing large proprietary data formats that require platform-specific runtime initialization.

## When to use

When you have vendor mass spectrometry raw files (e.g., .raw format) that must be converted to an open format (Aird) using a Windows .NET application running in a Docker container on macOS/Linux, and you need to account for first-run Wine initialization time (>30 minutes) and verify file integrity post-conversion.

## When NOT to use

- Input file is already in Aird format (.json + .aird pair) — skip conversion entirely.
- Running on native Windows with .NET Framework 4.7.2+ already installed — use the GUI AirdPro.exe directly instead of Docker/Wine overhead.
- Vendor file format is not supported by ProteoWizard (e.g., proprietary binary formats without public MSConvert plugins) — conversion will fail.

## Inputs

- vendor mass spectrometry raw file (e.g., .raw format from Thermo, Agilent, Bruker, or other ProteoWizard-supported formats)
- input directory path (mounted as Docker volume)
- output directory path (mounted as Docker volume)
- Docker container image (airdpro:cli)

## Outputs

- Aird index file (.json suffix)
- Aird data file (.aird suffix)
- conversion log or status record
- first-run initialization time measurement

## How to apply

Launch the airdpro:cli Docker container with volume mounts mapping the host input directory (containing vendor .raw files) and output directory to the container filesystem. Execute run-cli.sh or equivalent entry point against a sample vendor file, monitoring Wine initialization and .NET Framework 4.8 component download during first run (documented to exceed 30 minutes). Record startup time and watch for process completion. Verify output Aird file in the mounted output directory by checking file existence, size (non-zero), and format signature (Aird files consist of paired .json index and .aird data files with matching names). Subsequent runs will execute faster due to cached Wine/Framework state. Plan for 20–30% performance degradation when running through Wine versus native Windows execution.

## Related tools

- **Docker Desktop for Mac** (Container runtime for executing AirdPro CLI in an isolated, reproducible environment with file volume mounting)
- **Wine** (Windows application emulation layer to run .NET-compiled AirdPro within Linux container; requires initialization and .NET Framework download on first run)
- **.NET Framework 4.8** (Runtime dependency for AirdPro C# application; downloaded and installed by Wine on first container execution)
- **AirdPro V5 / V6** (CLI converter tool for transforming vendor mass spectrometry files to Aird format using compression and indexing strategies) — https://github.com/CSi-Studio/AirdPro
- **ProteoWizard** (Underlying library (pwiz_bindings_cli.dll) providing vendor file format parsers and MSConvert functionality for AirdPro)

## Examples

```
docker run --rm -v /path/to/vendor/files:/input -v /path/to/output:/output airdpro:cli ./run-cli.sh /input/sample.raw /output
```

## Evaluation signals

- Output directory contains both .json (index) and .aird (data) files with matching base names (e.g., sample.json + sample.aird).
- Aird data file size is non-zero and proportional to input vendor file size (expect ~20–50% of original depending on compression settings and ion mobility data presence in V6).
- First-run execution duration exceeds 30 minutes due to Wine initialization; subsequent runs complete in seconds to minutes.
- File system checks confirm output files are readable and contain valid Aird binary/JSON content (no truncation or corruption).
- Conversion task completes without error exits (exit code 0); check container logs for Wine initialization messages and conversion completion status.

## Limitations

- First-run Wine initialization and .NET Framework component download takes >30 minutes, creating significant startup latency for initial conversions.
- 20–30% performance degradation vs. native Windows execution due to Wine emulation overhead; batch processing is recommended to amortize initialization cost.
- Large-scale conversions may exhaust container memory; V6.0.0 includes stability improvements for memory overflow, but multi-node distributed deployment is recommended for very large datasets.
- Input vendor file format must be supported by ProteoWizard MSConvert; unsupported or corrupted vendor files will fail silently or with cryptic error messages.
- Output Aird format precision is configurable (mzPrecision parameter, default 0.0001); lossy compression may affect downstream analyses sensitive to mass accuracy.

## Evidence

- [readme] AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project.: "AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project."
- [methods] Wine needs to initialize and download .NET Framework components, taking more than 30 minutes: "Wine needs to initialize and download .NET Framework components, taking more than 30 minutes"
- [other] 1. Launch the airdpro:cli container with volume mounts for input vendor raw data and output directory. 2. Trigger Wine initialization by executing run-cli.sh against a sample vendor mass spectrometry raw file (e.g., .raw format). 3. Monitor and record the first-run Wine startup and .NET Framework component download time. 4. Verify that the Aird conversion process completes and produces a named output Aird file in the mounted output directory. 5. Confirm file integrity by checking file existence, size, and format signature.: "Launch the airdpro:cli container with volume mounts for input vendor raw data and output directory. Trigger Wine initialization by executing run-cli.sh against a sample vendor mass spectrometry raw"
- [methods] 20-30% performance degradation when running through Wine: "20-30% performance degradation when running through Wine"
- [readme] Aird Index File and Aird Data File show be stored in the same directory with the same file name but with different suffix: "Aird Index File and Aird Data File show be stored in the same directory with the same file name but with different suffix"
