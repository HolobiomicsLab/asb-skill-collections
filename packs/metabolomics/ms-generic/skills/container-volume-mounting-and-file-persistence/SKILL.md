---
name: container-volume-mounting-and-file-persistence
description: Use when executing containerized conversion tools (e.g., AirdPro CLI) that must read vendor-format mass spectrometry raw files from the host filesystem and write converted output (e.g., .aird files) back to a persistent host directory. This is essential when first-run Wine initialization and .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
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
  - AirdPro CLI
  - run-cli.sh
  techniques:
  - mass-spectrometry
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Container Volume Mounting and File Persistence

## Summary

Mount host directories into Docker containers to enable persistent input/output handling for file format conversion workflows. This skill ensures that vendor mass spectrometry raw files and converted output remain accessible across container restarts and first-run initialization sequences.

## When to use

Use this skill when executing containerized conversion tools (e.g., AirdPro CLI) that must read vendor-format mass spectrometry raw files from the host filesystem and write converted output (e.g., .aird files) back to a persistent host directory. This is essential when first-run Wine initialization and .NET Framework downloads take 30+ minutes and must not be lost if the container is interrupted.

## When NOT to use

- Input vendor files are already in a container image or ephemeral storage — use this skill only when files must persist across container lifecycle events.
- Output files are temporary or expected to be discarded — volume mounting adds overhead; use container-internal tmpfs or unnamed volumes instead.
- The conversion tool does not support configurable input/output paths — verify the tool CLI accepts explicit file or directory arguments before applying this skill.

## Inputs

- Vendor mass spectrometry raw file path on host (e.g., .raw, .d folder)
- Host output directory path (must exist and be writable)
- Docker container image reference (e.g., airdpro:cli)

## Outputs

- Converted Aird data file (.aird) in host output directory
- Aird index file (.json) with matching filename in same directory
- Container logs documenting Wine initialization and conversion status

## How to apply

Launch the Docker container with explicit volume mounts using the `-v` flag to bind host input and output directories to container mount points. For AirdPro CLI: mount the directory containing vendor raw data (e.g., .raw, .d folder formats) to a container path (e.g., `/data/input`), and mount an output directory to `/data/output`. Execute the conversion command (e.g., `run-cli.sh`) against the mounted input path. After conversion completes, verify that the named .aird output file and accompanying .json index file exist in the host output directory with correct file size and format signature. This approach decouples container lifecycle from data persistence and allows monitoring of Wine initialization progress on the host.

## Related tools

- **Docker Desktop for Mac** (Container runtime for launching AirdPro CLI with volume mounts; version 20.10+ required) — https://www.docker.com/products/docker-desktop
- **Wine** (Windows application emulator running inside container to execute AirdPro .NET binaries; requires 30+ minutes for first-run .NET Framework initialization)
- **.NET Framework 4.8** (Runtime dependency for AirdPro installed via Wine; downloaded during container first run)
- **AirdPro CLI** (Conversion tool invoked against mounted vendor raw file; produces .aird and .json output to mounted output volume) — https://github.com/CSi-Studio/AirdPro
- **run-cli.sh** (Container entry script that triggers Wine initialization and AirdPro conversion) — https://github.com/CSi-Studio/AirdPro

## Examples

```
docker run -v /path/to/vendor/raw:/data/input -v /path/to/output:/data/output airdpro:cli ./run-cli.sh /data/input/sample.raw /data/output/sample.aird
```

## Evaluation signals

- Verify output .aird file exists in the mounted host output directory with non-zero file size.
- Confirm accompanying .json index file exists in the same directory with matching base filename.
- Check file integrity by examining format signature (e.g., first bytes match Aird specification for binary .aird and valid JSON structure for .json index).
- Confirm Wine initialization completed and .NET Framework components were downloaded on first run (monitor container logs for Wine startup messages; second and subsequent runs should skip this phase).
- Verify vendor raw file was read from mounted input directory by checking container logs for input path references and successful parsing of vendor format metadata.

## Limitations

- First-run container execution incurs 30+ minute Wine initialization and .NET Framework 4.8 download overhead; cannot be parallelized across multiple containers without separate image layers.
- 20–30% performance degradation when running AirdPro through Wine relative to native Windows execution; suitable for batch processing but not real-time conversion.
- Volume mount performance depends on the Docker Desktop host OS and storage backend; macOS especially may experience slower I/O on large vendor raw files due to file sharing overhead.
- Vendor file format support is limited to those recognized by ProteoWizard MSConvert (the underlying library); custom or proprietary vendor formats not in MSConvert's list will fail silently or with generic errors.
- Requires explicit directory creation and permission setup on the host before mounting; read/write permissions must align between container user (often root in airdpro:cli image) and host filesystem ownership.

## Evidence

- [other] Launch the airdpro:cli container with volume mounts for input vendor raw data and output directory: "Launch the airdpro:cli container with volume mounts for input vendor raw data and output directory."
- [methods] Wine needs to initialize and download .NET Framework components, taking more than 30 minutes: "Wine needs to initialize and download .NET Framework components, taking more than 30 minutes"
- [other] Verify that the Aird conversion process completes and produces a named output Aird file in the mounted output directory: "Verify that the Aird conversion process completes and produces a named output Aird file in the mounted output directory."
- [other] Confirm file integrity by checking file existence, size, and format signature: "Confirm file integrity by checking file existence, size, and format signature."
- [readme] Aird Index File and Aird Data File show be stored in the same directory with the same file name but with different suffix: "Aird Index File and Aird Data File show be stored in the same directory with the same file name but with different suffix"
- [readme] AirdPro can convert all the vendor format that MSConvert supports to Aird format: "AirdPro can convert all the vendor format that MSConvert supports to Aird format."
- [methods] 20-30% performance degradation when running through Wine: "20-30% performance degradation when running through Wine"
