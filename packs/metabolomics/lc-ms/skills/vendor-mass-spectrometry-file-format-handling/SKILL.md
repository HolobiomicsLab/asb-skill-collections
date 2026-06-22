---
name: vendor-mass-spectrometry-file-format-handling
description: Use when you have one or more vendor mass spectrometry raw files (Thermo .raw, Agilent .d, Sciex .wiff2, or other MSConvert-supported formats) that must be converted to Aird format for batch processing, cloud deployment, or integration with downstream analysis tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - AirdPro V5
  - AirdPro V6
  - ProteoWizard
  - AirdPro V5/V6
  - ProteoWizard MSConvert
  - Wine
  - .NET Framework 4.8
  - Docker Desktop for Mac / Docker Compose
  - Redis
  - AirdSDK
  techniques:
  - LC-MS
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

# vendor-mass-spectrometry-file-format-handling

## Summary

Convert vendor-proprietary mass spectrometry raw files (e.g., .raw, .d, .wiff2) to the open Aird format using AirdPro, a C# tool built on ProteoWizard bindings that enables computation-oriented downstream analysis with high compression and fast decoding. Apply this skill when you have vendor instrument output that must be converted to a standardized, compressed format for batch processing, archival, or integration into open-source analysis pipelines.

## When to use

You have one or more vendor mass spectrometry raw files (Thermo .raw, Agilent .d, Sciex .wiff2, or other MSConvert-supported formats) that must be converted to Aird format for batch processing, cloud deployment, or integration with downstream analysis tools. Use this skill especially when working with large-scale conversions (multiple files or high-volume data) or when you need reproducible, distributed conversion workflows via Docker and CLI automation.

## When NOT to use

- Input files are already in Aird, mzML, or mzXML format — skip conversion and proceed directly to analysis.
- You need real-time conversion feedback or interactive GUI-based file selection — use AirdPro GUI client instead of CLI, or run on a Windows workstation with .NET 4.7.2+.
- Your infrastructure does not support Docker or Wine — you must install AirdPro natively on Windows 7+ with .NET 4.7.2 and ProteoWizard MSConvert dependencies.

## Inputs

- Vendor mass spectrometry raw files (e.g., .raw, .d, .wiff2, or other MSConvert-supported formats)
- Acquisition method metadata (DDA, DIA/SWATH, PRM, or COMMON)
- m/z precision parameter (e.g., 0.0001 for default or user-specified value)
- Source and target directory paths for Docker volume mounts

## Outputs

- Aird data file (.aird)
- Aird index file (.json) with same base filename as .aird file
- Conversion log or task status from Docker container

## How to apply

Launch the AirdPro CLI tool via Docker (airdpro:cli image) with mounted volumes for input vendor files and output directory, specifying the acquisition method (DDA, DIA/SWATH, PRM, or COMMON) and desired m/z precision (default 0.0001). Execute run-cli.sh against the vendor raw file; allow first-run initialization to complete (>30 minutes for Wine .NET Framework download on initial execution). Monitor conversion progress and verify output: confirm the paired .aird data file and .json index file are created in the output directory with correct file size and format signature. For batch conversions, leverage Redis-backed task queues to distribute jobs across multiple AirdPro nodes. Expect 20–30% performance overhead when running through Wine on Linux; plan accordingly for large datasets.

## Related tools

- **AirdPro V5/V6** (Primary conversion engine (C# GUI/CLI client); performs vendor-to-Aird format conversion with compression strategies (ZDPD, StackZDPD, ZDVB) and acquisition-method detection) — https://github.com/CSi-Studio/AirdPro
- **ProteoWizard MSConvert** (Underlying library (pwiz_bindings_cli.dll) that handles vendor file format reading and normalization; supports all MSConvert-compatible vendor formats)
- **Wine** (Windows application runtime layer for Linux/Docker containers; enables execution of .NET-based AirdPro CLI in containerized environments)
- **.NET Framework 4.8** (Runtime dependency for AirdPro; installed and executed through Wine on Linux containers)
- **Docker Desktop for Mac / Docker Compose** (Container orchestration and environment management; provides isolated, reproducible execution of airdpro:cli with Wine and .NET dependencies pre-configured)
- **Redis** (Optional message broker for distributed batch conversion; queues ConvertJob objects (sourcePath, targetPath, mzPrecision, type) across multiple AirdPro nodes)
- **AirdSDK** (Secondary-development library for reading/processing Aird files; available in Java, C#, and Python) — https://github.com/CSi-Studio/Aird-SDK

## Examples

```
docker run --rm -v /path/to/vendor/raw:/input -v /path/to/output:/output airdpro:cli ./run-cli.sh /input/sample.raw /output DDA 0.0001
```

## Evaluation signals

- Paired .aird and .json files are present in the output directory with matching base filenames and non-zero file sizes.
- File integrity check: .aird file contains valid binary data matching Aird compression signatures (ZDPD/StackZDPD/ZDVB); .json index file parses as valid JSON with expected schema.
- Conversion completes without critical errors in Docker logs; Wine initialization and .NET Framework download succeed on first run (monitor for >30 minute initialization window).
- For batch jobs: all ConvertJob entries successfully dequeued from Redis and corresponding .aird/.json outputs generated with no missing or truncated files.
- Performance metric: conversion time per file is within expected range considering 20–30% Wine overhead; no memory overflow or out-of-bounds errors during processing (especially for large-scale conversions).

## Limitations

- First-run execution incurs >30 minute initialization overhead due to Wine and .NET Framework setup; subsequent runs are faster but still experience 20–30% performance degradation vs. native Windows execution.
- Requires Docker and Wine dependencies; not suitable for air-gapped or non-containerized environments without manual ProteoWizard and .NET installation.
- Acquisition method must be correctly specified (DDA, DIA/SWATH, PRM, COMMON) at conversion time; misclassification may produce suboptimal compression or incorrect spectral indexing.
- m/z precision truncation (via mzPrecision parameter) is lossy; users must validate that chosen precision (default 0.0001) does not compromise downstream identification accuracy for their analyte classes.
- CLI conversion does not provide real-time visual feedback; errors and progress must be monitored via container logs or external task-tracking system (e.g., Redis queue status).

## Evidence

- [other] Does execution of AirdPro CLI against a vendor mass spectrometry raw file via the airdpro:cli Docker image complete Wine initialization and produce a converted Aird output file?: "Does execution of AirdPro CLI against a vendor mass spectrometry raw file via the airdpro:cli Docker image complete Wine initialization and produce a converted Aird output file?"
- [other] first-run execution requires Wine to initialize and download .NET Framework components, a process documented to take more than 30 minutes: "first-run execution requires Wine to initialize and download .NET Framework components, a process documented to take more than 30 minutes"
- [readme] AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project.: "AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project."
- [readme] By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format.: "By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format."
- [other] 20-30% performance degradation when running through Wine: "20-30% performance degradation when running through Wine"
- [other] Launch the airdpro:cli container with volume mounts for input vendor raw data and output directory. Trigger Wine initialization by executing run-cli.sh against a sample vendor mass spectrometry raw file: "Launch the airdpro:cli container with volume mounts for input vendor raw data and output directory. Trigger Wine initialization by executing run-cli.sh against a sample vendor mass spectrometry raw"
- [readme] Aird Index File and Aird Data File show be stored in the same directory with the same file name but with different suffix: "Aird Index File and Aird Data File show be stored in the same directory with the same file name but with different suffix"
- [readme] The redis key is "ConvertTask", the value should be a Set data structure of a specific json model called "ConvertJob": "The redis key is "ConvertTask", the value should be a Set data structure of a specific json model called "ConvertJob""
