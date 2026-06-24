---
name: docker-image-registry-inspection
description: Use when after building multiple Docker image variants (e.g., cli, dev,
  linux, windows) using multi-stage builds with --target flags, and you need to verify
  that each variant's size falls within documented ranges (e.g., cli 6–7 GB, dev 9–11
  GB, linux 8–10 GB, windows 4–5 GB).
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - AirdPro V5
  - Docker Desktop for Mac
  - Docker Compose
  - Docker (docker build, docker inspect, docker system df)
  - Docker (docker build, docker inspect, docker system df, docker history)
  - Dockerfile (multi-stage build configuration)
  license_tier: restricted
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro V5 is now available at 2023.7
- Docker Desktop for Mac (version 20.10+)
- Docker Compose configuration
- Build all images (first build may take longer)
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

# Docker Image Registry Inspection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Inspect and audit Docker image variants (uncompressed and compressed sizes, layer composition) to verify they meet documented size specifications and functional requirements. This skill is essential for validating multi-stage Docker builds and ensuring consistency across image variants before deployment.

## When to use

After building multiple Docker image variants (e.g., cli, dev, linux, windows) using multi-stage builds with --target flags, and you need to verify that each variant's size falls within documented ranges (e.g., cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB). Also apply this skill when auditing existing images in a local Docker daemon or registry to detect size drift or bloat.

## When NOT to use

- Input images have not yet been built or do not exist in the local Docker daemon — build first using docker build --target.
- You are inspecting images from a remote registry (Docker Hub, ECR, etc.) without first pulling them locally; docker inspect requires local access.
- You only need to verify that an image runs correctly, not that it meets size constraints — use docker run and functional testing instead.

## Inputs

- Built Docker images (referenced by name:tag or image ID)
- Dockerfile with multi-stage build configuration
- Documented size specification ranges (per variant)
- Local Docker daemon with images present

## Outputs

- Structured inspection report (CSV or JSON) with columns: image_name, uncompressed_size_gb, compressed_size_gb, documented_range_gb, pass_fail_status
- Layer composition analysis (from docker history)
- Verification pass/fail summary

## How to apply

First, execute docker build --target <stage_name> for each image variant to produce all four targets (runtime-cli, runtime-dev, runtime-linux, runtime-windows). Then query each image's uncompressed size using docker inspect --format='{{.Size}}' to retrieve bytes. To measure actual storage footprint (compressed size on disk), use docker system df or equivalent Docker API calls. Convert reported byte sizes to gigabytes and compare each against the documented range for that variant. Finally, generate a structured verification report that lists image name, measured size (GB), documented size range, pass/fail status, and any size anomalies. Use docker history <image> to inspect layer composition if an image exceeds its documented range, to identify which build stage or dependency contributed to size overage.

## Related tools

- **Docker (docker build, docker inspect, docker system df, docker history)** (Build multi-stage images with --target flag, query image metadata (size), and inspect layer composition) — https://www.docker.com/
- **Dockerfile (multi-stage build configuration)** (Defines build targets (runtime-cli, runtime-dev, runtime-linux, runtime-windows) and layer structure for size auditing)
- **Docker Desktop for Mac** (Local Docker daemon environment for building and inspecting images)

## Examples

```
docker build --target runtime-cli . && docker inspect --format='{{.Size}}' airdpro:cli && docker system df
```

## Evaluation signals

- Each image's uncompressed size (from docker inspect --format='{{.Size}}') matches the documented range within ±5% (e.g., cli measured 6.5 GB vs. documented 6–7 GB range)
- Compressed size (from docker system df) is smaller than uncompressed by a factor consistent with typical Docker layer compression (typically 30–50%)
- Pass/fail status in report is consistent: all variants with sizes within documented ranges show PASS; any outside the range show FAIL with the excess magnitude
- docker history output shows no unexpected large layers; each layer is proportional to its declared dependencies (e.g., Wine + .NET Framework 4.8 is the dominant layer in the cli variant)
- All four image variants are present and inspectable; no 'image not found' errors when querying by name or ID

## Limitations

- docker inspect and docker system df report sizes for images in the local Docker daemon only; images in remote registries must be pulled first, which requires network access and local storage.
- Compressed size varies based on the Docker storage driver (overlay2, aufs, devicemapper) and host filesystem; identical images may report different compressed sizes on different machines.
- Documented size ranges (6–7 GB for cli, 9–11 GB for dev, etc.) are specific to AirdPro and depend on the exact .NET Framework version, Wine build, and dependency versions; size may vary with OS or build date.
- Multi-stage builds with --target require that all intermediate stages (base, builder, runtime-*) be defined in the Dockerfile; missing or incorrectly named targets will cause docker build --target to fail.

## Evidence

- [other] Execute the multi-stage Docker build process via `docker build --target runtime-cli`, `docker build --target runtime-dev`, `docker build --target runtime-linux`, and `docker build --target runtime-windows` to produce all four image variants.: "Execute the multi-stage Docker build process via `docker build --target runtime-cli`, `docker build --target runtime-dev`, `docker build --target runtime-linux`, and `docker build --target"
- [other] Query each built image using `docker inspect --format='{{.Size}}'` to retrieve the uncompressed image size in bytes.: "Query each built image using `docker inspect --format='{{.Size}}'` to retrieve the uncompressed image size in bytes."
- [other] Query the compressed size of each image stored on disk using `docker system df` or equivalent Docker API calls to determine the actual storage footprint.: "Query the compressed size of each image stored on disk using `docker system df` or equivalent Docker API calls to determine the actual storage footprint."
- [other] Convert byte sizes to gigabytes and compare each against the documented range (cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB).: "Convert byte sizes to gigabytes and compare each against the documented range (cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB)."
- [other] Generate a structured verification report listing image name, measured size (GB), documented range, and pass/fail status for each variant.: "Generate a structured verification report listing image name, measured size (GB), documented range, and pass/fail status for each variant."
- [other] AirdPro is built using Docker with Wine to run the C#-based application in Linux containers, leveraging .NET Framework 4.8 and pwiz_bindings_cli.dll from ProteoWizard: "AirdPro is built using Docker with Wine to run the C#-based application in Linux containers, leveraging .NET Framework 4.8 and pwiz_bindings_cli.dll from ProteoWizard"
