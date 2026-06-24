---
name: artifact-size-measurement-and-range-verification
description: Use when you have built multiple Docker image variants (e.g., cli, dev,
  linux, windows) from a multi-stage Dockerfile and need to verify that their uncompressed
  and compressed storage footprints fall within documented acceptable ranges (e.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - AirdPro V5
  - Docker (docker build, docker inspect, docker system df)
  - Dockerfile (multi-stage build with --target flag)
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

# artifact-size-measurement-and-range-verification

## Summary

Measure uncompressed and compressed sizes of built Docker image artifacts, compare against documented acceptable ranges, and generate a structured pass/fail verification report. This skill ensures Docker image variants meet storage and distribution requirements before deployment.

## When to use

You have built multiple Docker image variants (e.g., cli, dev, linux, windows) from a multi-stage Dockerfile and need to verify that their uncompressed and compressed storage footprints fall within documented acceptable ranges (e.g., cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB) before release or deployment.

## When NOT to use

- Docker images have not yet been built; execute the build step first.
- No documented size range specifications are available for the image variants; establish baseline ranges before running verification.
- Image variants do not have distinct, named build targets in the Dockerfile; refactor the Dockerfile to support --target before applying this skill.

## Inputs

- Multi-stage Dockerfile with named build targets (runtime-cli, runtime-dev, runtime-linux, runtime-windows)
- Docker daemon with built or buildable images
- Documented size range specifications per variant (e.g., JSON or text file with variant name and min/max GB)

## Outputs

- Structured verification report (CSV, JSON, or tabular format) with columns: image_name, uncompressed_size_gb, compressed_size_gb, documented_range_gb, pass_fail_status
- Size measurements in gigabytes (both uncompressed and compressed)

## How to apply

Execute multi-stage Docker builds for each image variant using the --target flag (e.g., `docker build --target runtime-cli`). Query uncompressed image size in bytes using `docker inspect --format='{{.Size}}'` for each built image. Retrieve compressed size using `docker system df` or Docker API calls to measure actual storage footprint on disk. Convert both byte measurements to gigabytes. Compare each measured value (uncompressed and compressed) against the documented range for that variant. Generate a structured report listing image name, measured size (GB), documented range (GB), and pass/fail status. Pass criterion: measured size must fall within or below the documented range for storage compliance.

## Related tools

- **Docker (docker build, docker inspect, docker system df)** (Build Docker images with named targets, query uncompressed image sizes via inspect, and retrieve compressed disk footprint via system df)
- **Dockerfile (multi-stage build with --target flag)** (Define build stages and named targets (runtime-cli, runtime-dev, runtime-linux, runtime-windows) to enable selective image variant construction)
- **AirdPro V5** (Reference system for which Docker image size audit is being conducted) — https://github.com/CSi-Studio/AirdPro

## Evaluation signals

- All four image variants (cli, dev, linux, windows) are successfully built and queryable via `docker inspect`.
- Uncompressed size measurements returned by `docker inspect --format='{{.Size}}'` are non-zero and in bytes.
- Compressed size measurements from `docker system df` are retrieved for each variant and are smaller than or equal to uncompressed sizes.
- All measured sizes (both uncompressed and compressed, converted to GB) fall within or below the documented range for each variant (e.g., cli measured ≤ 7 GB, dev ≤ 11 GB, linux ≤ 10 GB, windows ≤ 5 GB).
- Verification report is generated with no missing data; all variants have a documented range, measured size, and clear pass/fail status.

## Limitations

- Docker system df reports compressed size as stored on the local Docker daemon; actual distribution size may vary depending on registry compression, image layers, and pull-time deduplication.
- Uncompressed size from `docker inspect` reflects the extracted filesystem size; this may not account for layer-level decompression overhead or intermediate build artifacts.
- Documented size ranges must be established and maintained separately; if ranges are outdated or incorrect, verification will be unreliable.
- Multi-stage builds with overlapping dependencies may produce counterintuitive size ratios between variants; measured sizes should be interpreted in context of each variant's dependencies and tools.

## Evidence

- [other] Execute the multi-stage Docker build process via `docker build --target runtime-cli`, `docker build --target runtime-dev`, `docker build --target runtime-linux`, and `docker build --target runtime-windows` to produce all four image variants.: "Execute the multi-stage Docker build process via `docker build --target runtime-cli`, `docker build --target runtime-dev`, `docker build --target runtime-linux`, and `docker build --target"
- [other] Query each built image using `docker inspect --format='{{.Size}}'` to retrieve the uncompressed image size in bytes.: "Query each built image using `docker inspect --format='{{.Size}}'` to retrieve the uncompressed image size in bytes."
- [other] Query the compressed size of each image stored on disk using `docker system df` or equivalent Docker API calls to determine the actual storage footprint.: "Query the compressed size of each image stored on disk using `docker system df` or equivalent Docker API calls to determine the actual storage footprint."
- [other] Convert byte sizes to gigabytes and compare each against the documented range (cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB).: "Convert byte sizes to gigabytes and compare each against the documented range (cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB)."
- [other] Generate a structured verification report listing image name, measured size (GB), documented range, and pass/fail status for each variant.: "Generate a structured verification report listing image name, measured size (GB), documented range, and pass/fail status for each variant."
