---
name: containerized-application-deployment-validation
description: Use when when deploying containerized versions of a multi-variant application
  (e.g., CLI, development, Linux, and Windows flavors) and you need to verify that
  each built image meets documented size constraints before registry push or production
  release.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - AirdPro V5
  - Docker (docker build, docker inspect, docker system df)
  - Dockerfile (multi-stage build with --target flag)
  - AirdPro V5 / V6
  license_tier: open
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro V5 is now available at 2023.7
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

# containerized-application-deployment-validation

## Summary

Validate Docker container images across multiple build targets by measuring uncompressed and compressed image sizes and comparing against documented specification ranges. This skill ensures reproducibility and correctness of multi-stage Docker builds for complex scientific applications.

## When to use

When deploying containerized versions of a multi-variant application (e.g., CLI, development, Linux, and Windows flavors) and you need to verify that each built image meets documented size constraints before registry push or production release. Particularly useful after dependency updates, compiler flag changes, or when adding new layers that may inflate image footprint.

## When NOT to use

- Single-stage Dockerfile without build targets — the skill explicitly requires multi-stage builds with `--target` support.
- Application where image size is not a deployment constraint or performance metric — skip if no documented size ranges exist.
- Continuous integration environment where Docker images are ephemeral and discarded after test; size validation adds overhead without persistent value.

## Inputs

- Dockerfile with multi-stage build targets (--target flag support)
- Source code repository containing all application variants
- Documented compressed size specification ranges per variant (GB)
- Docker daemon with sufficient disk space for all four image builds

## Outputs

- Structured verification report (JSON or tabular format) with fields: image_name, measured_uncompressed_size_gb, measured_compressed_size_gb, documented_range_gb, pass_fail_status
- Docker image artifacts (one per variant) stored locally or in registry
- Build validation exit status (0 = all variants pass, non-zero = at least one variant out of spec)

## How to apply

Execute the multi-stage Docker build process using `docker build --target` flags to produce all variants (e.g., `--target runtime-cli`, `--target runtime-dev`, `--target runtime-linux`, `--target runtime-windows`). Retrieve the uncompressed size of each built image using `docker inspect --format='{{.Size}}'` and query compressed size using `docker system df` or Docker API. Convert byte measurements to gigabytes and compare each result against the documented range for that variant (e.g., CLI 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB). Generate a structured verification report listing image name, measured size in GB, documented range, and pass/fail status. Fail the build validation if any variant falls outside its specified range, signaling the need for optimization or investigation.

## Related tools

- **Docker (docker build, docker inspect, docker system df)** (Multi-stage image builder and size inspector; executes --target flag builds and retrieves uncompressed and compressed image footprints)
- **Dockerfile (multi-stage build with --target flag)** (Configuration artifact defining build stages and variant targets (runtime-cli, runtime-dev, runtime-linux, runtime-windows)) — https://github.com/CSi-Studio/AirdPro
- **AirdPro V5 / V6** (Reference application being containerized and validated across four Docker image variants) — https://github.com/CSi-Studio/AirdPro

## Evaluation signals

- All four image variants build successfully without Docker daemon errors or layer caching failures.
- Measured uncompressed size (from `docker inspect`) and compressed size (from `docker system df`) are both recorded for each variant and fall within the documented range (e.g., CLI 6–7 GB) within ±5% tolerance.
- The structured verification report shows pass status for all variants; any fail status triggers a re-build or optimization cycle with documented root cause (e.g., new dependency, compiler flag change).
- Byte-to-GB conversion is correct and consistent across all measurements (e.g., no unit truncation or rounding errors that cause spurious failures).
- Compressed size is always smaller than uncompressed size, and compression ratio aligns with the application's documented compressor strategy (e.g., Zlib, Brotli, Zstd for AirdPro).

## Limitations

- Documented size ranges must be pre-established and maintained by the development team; this skill validates against spec but does not define spec.
- Docker system df measures only images on the local daemon; it does not account for registry-side compression or storage optimizations that may occur during push.
- First build may take substantially longer than subsequent builds due to layer caching; validation should account for initial timing variance and run multiple builds if consistency is critical.
- Size validation alone does not verify functional correctness, security vulnerabilities, or performance; pair this skill with integration and security testing.
- Wine-based Windows image variant may show 20–30% performance degradation in CI/CD pipelines and may require extended timeouts for Docker build operations.

## Evidence

- [other] Execute the multi-stage Docker build process via `docker build --target runtime-cli`, `docker build --target runtime-dev`, `docker build --target runtime-linux`, and `docker build --target runtime-windows` to produce all four image variants.: "Execute the multi-stage Docker build process via `docker build --target runtime-cli`, `docker build --target runtime-dev`, `docker build --target runtime-linux`, and `docker build --target"
- [other] Query each built image using `docker inspect --format='{{.Size}}'` to retrieve the uncompressed image size in bytes. Query the compressed size of each image stored on disk using `docker system df` or equivalent Docker API calls to determine the actual storage footprint.: "Query each built image using `docker inspect --format='{{.Size}}'` to retrieve the uncompressed image size in bytes. Query the compressed size of each image stored on disk using `docker system df` or"
- [other] Convert byte sizes to gigabytes and compare each against the documented range (cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB). Generate a structured verification report listing image name, measured size (GB), documented range, and pass/fail status for each variant.: "Convert byte sizes to gigabytes and compare each against the documented range (cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB). Generate a structured verification report listing image name,"
- [methods] Build all images (first build may take longer): "Build all images (first build may take longer)"
- [methods] 20-30% performance degradation when running through Wine: "20-30% performance degradation when running through Wine"
