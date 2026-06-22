---
name: docker-container-volume-mounting
description: 'Use when when you have vendor raw mass spectrometry files on the host machine that need to be processed by a containerized tool (e.g., AirdPro), and the container must read input from and write output to specific host paths. Typical trigger: you have a .'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - AirdPro V6
  - pwiz_bindings_cli.dll
  - ProteoWizard
  - Docker Desktop for Mac
  - Docker Engine
  - AirdPro
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro V6 is now available at 2024.4
- based on pwiz_bindings_cli.dll from the ProteoWizard project
- pwiz_bindings_cli.dll from the ProteoWizard project
- based on pwiz_bindings_cli.dll from the ProteoWizard project.
- Docker Desktop for Mac (version 20.10+)
- this project enables AirdPro to run on macOS through Docker + Wine technology.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aird_cq
    doi: 10.1186/s12859-021-04490-0
    title: aird
  dedup_kept_from: coll_aird_cq
schema_version: 0.2.0
---

# docker-container-volume-mounting

## Summary

Mount host filesystem directories into Docker containers to enable input/output file exchange and persistent data storage. This skill is essential for containerized scientific workflows where raw data must be read from the host and results written back.

## When to use

When you have vendor raw mass spectrometry files on the host machine that need to be processed by a containerized tool (e.g., AirdPro), and the container must read input from and write output to specific host paths. Typical trigger: you have a .raw or other vendor format file at a known host path, and a Docker image that can convert it to mzML or Aird format.

## When NOT to use

- The input file is already inside the container image at a fixed path — direct mounting is unnecessary and may cause conflicts.
- You need bidirectional real-time synchronization between host and container — use Docker volumes or bind mounts with careful concurrency control instead.
- The input data is in a cloud storage bucket or remote URL and you want to avoid downloading to the host first — fetch into the container directly or use a separate orchestration layer.

## Inputs

- Host filesystem directory containing vendor raw files (e.g., .raw, .d folder)
- Docker image URI or container name
- Mount point path within the container (e.g., /data)

## Outputs

- Converted file written to the mounted host directory (e.g., .mzML, .aird)
- Container logs and exit status

## How to apply

Mount the host input directory to a standard container path (e.g., /data) using the -v flag in docker run. Place the vendor raw file in the mounted input directory on the host before invoking the container. Execute the container's CLI with arguments that reference the mounted paths (e.g., -i /data/input.raw -o /data/output.mzML). After container completion, retrieve the output file from the mounted directory on the host. Verify that the output file exists, is non-empty, and passes format validation (e.g., XML schema check for mzML).

## Related tools

- **AirdPro** (Containerized CLI tool that performs vendor raw file to mzML/Aird conversion; invoked with mounted input/output paths) — https://github.com/CSi-Studio/AirdPro
- **Docker Engine** (Runtime that executes the mounted container and enforces volume mount isolation)
- **pwiz_bindings_cli.dll** (ProteoWizard library bundled in the AirdPro container; performs the actual vendor format parsing and conversion)

## Examples

```
docker run --rm -v $(pwd)/input:/data/input -v $(pwd)/output:/data/output airdpro:v6 run-cli.sh -i /data/input/sample.raw -o /data/output/sample.mzML
```

## Evaluation signals

- Output file exists at the expected host path after container exits with status 0.
- Output file size is greater than zero and is appropriate for the data size (not truncated or corrupted).
- Output mzML file parses as valid XML and contains expected MS data schema elements (spectrum, precursor, product).
- Input file on host is not modified or deleted during or after container execution.
- Container logs confirm successful file I/O at the mounted paths (e.g., 'Reading from /data/input.raw', 'Writing to /data/output.mzML').

## Limitations

- File permission mismatches between host UID/GID and container user may cause read or write errors; may require explicit ownership or mode flags.
- Performance overhead from bind-mounting on macOS (Docker Desktop for Mac) is significant due to FUSE/osxfs; consider Docker volumes for large repeated I/O.
- Mounted volumes are not persistent across container deletions unless they are named Docker volumes; bind mounts to host paths persist but tie deployment to a specific host directory layout.
- Concurrent writes from multiple containers to the same mount point can cause corruption; serialize access or use file locking within containers.

## Evidence

- [other] Mount the input vendor raw file into the Docker container's /data directory: "Mount the input vendor raw file into the Docker container's /data directory. 2. Invoke run-cli.sh with arguments specifying input file path (-i /data/input.raw) and output file path (-o"
- [other] The container executes AirdPro's CLI interface, which calls pwiz_bindings_cli.dll from ProteoWizard to perform the conversion from vendor format to mzML: "The container executes AirdPro's CLI interface, which calls pwiz_bindings_cli.dll from ProteoWizard to perform the conversion from vendor format to mzML."
- [other] Verify the output mzML file is present and is valid XML: "4. Verify the output mzML file is present and is valid XML."
- [methods] Docker Desktop for Mac (version 20.10+): "Docker Desktop for Mac (version 20.10+)"
