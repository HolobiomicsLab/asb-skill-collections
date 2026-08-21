---
name: multi-stage-dockerfile-interpretation
description: Use when you need to validate that Docker image builds for multiple deployment
  variants (e.g., cli, dev, linux, windows) meet documented compressed size ranges,
  or when you must audit storage footprint across a multi-target build pipeline without
  pre-computed metrics.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - AirdPro V5
  - Dockerfile (multi-stage build with --target flag)
  - Docker
  - Dockerfile (multi-stage build syntax)
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro V5 is now available at 2023.7
- Dockerfile uses an optimized build strategy
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

# Multi-stage Dockerfile Interpretation

## Summary

Interpret and execute multi-stage Docker builds to produce variant container images from a single Dockerfile, then measure and validate their compressed and uncompressed sizes against documented ranges. This skill is essential when verifying that containerized applications meet storage and performance SLAs across different deployment targets (CLI, development, Linux, Windows).

## When to use

Apply this skill when you need to validate that Docker image builds for multiple deployment variants (e.g., cli, dev, linux, windows) meet documented compressed size ranges, or when you must audit storage footprint across a multi-target build pipeline without pre-computed metrics.

## When NOT to use

- Single-stage Dockerfile builds where no variant selection or --target flag is used; use standard docker build and docker inspect instead.
- When documented size ranges are unavailable or untrusted; reconcile sources before comparison.
- When Docker daemon is not available or containerization is not the deployment mechanism; this skill is Docker-specific.

## Inputs

- Dockerfile with multi-stage build configuration (using FROM ... AS <stage> and --target flag syntax)
- Docker daemon with available CPU/memory for build execution
- Documented size range specifications per image variant (e.g., JSON or CSV lookup table)

## Outputs

- Structured verification report (CSV, JSON, or tabular format) with columns: image_name, uncompressed_size_gb, compressed_size_gb, documented_range_gb, pass_fail_status
- Per-variant Docker image artifacts (stored locally or in registry)
- Docker system resource audit (from docker system df output)

## How to apply

Execute the multi-stage Docker build process using `docker build --target <stage_name>` for each variant (runtime-cli, runtime-dev, runtime-linux, runtime-windows). Retrieve uncompressed image size via `docker inspect --format='{{.Size}}'` in bytes, and query compressed on-disk size using `docker system df` or Docker API calls. Convert both byte measurements to gigabytes and compare against documented ranges (e.g., cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB). Generate a structured verification report listing image name, measured size (GB), documented range, and pass/fail status for each variant. The rationale is that multi-stage builds allow selective layer inclusion per target, and size variation across targets indicates whether build optimization is working correctly.

## Related tools

- **Docker** (Build, inspect, and measure container images using docker build --target, docker inspect --format, and docker system df commands)
- **Dockerfile (multi-stage build syntax)** (Source configuration defining multiple build stages (FROM ... AS) and conditional layer inclusion via --target flag) — https://github.com/CSi-Studio/AirdPro
- **AirdPro V5** (Subject application being containerized across multiple variants (cli, dev, linux, windows)) — https://github.com/CSi-Studio/AirdPro

## Examples

```
docker build --target runtime-cli -t airdpro:cli . && docker inspect --format='{{.Size}}' airdpro:cli && docker system df --format 'table {{.Repository}}\t{{.Size}}'
```

## Evaluation signals

- All four image variants (cli, dev, linux, windows) successfully build without errors using --target flag.
- Measured uncompressed sizes (from docker inspect) are within ±5% of expected ranges documented in specification.
- Measured compressed sizes (from docker system df) are within ±10% of documented storage footprint ranges.
- Pass/fail status report shows all variants passing; any failing variant triggers root cause analysis (e.g., unintended layer inclusion, missing cleanup).
- Compressed size is consistently 40–60% of uncompressed size, indicating effective layer de-duplication and compression across variants.

## Limitations

- docker system df reports only locally stored image sizes; registry-side compression may differ due to registry-specific optimization.
- Size measurements are sensitive to Docker build cache state; cold builds (cache invalidation) may report inflated intermediate layer sizes not present in cached builds.
- Multi-stage build target names and stage organization vary by Dockerfile author; automated scanning of --target flags requires parsing Dockerfile syntax.
- Documented size ranges may be outdated if dependency versions (e.g., .NET Framework, Wine, ProteoWizard libraries) are not pinned in Dockerfile; ranges must be re-validated after dependency updates.

## Evidence

- [other] Execute the multi-stage Docker build process via `docker build --target runtime-cli`, `docker build --target runtime-dev`, `docker build --target runtime-linux`, and `docker build --target runtime-windows` to produce all four image variants.: "Execute the multi-stage Docker build process via `docker build --target runtime-cli`, `docker build --target runtime-dev`, `docker build --target runtime-linux`, and `docker build --target"
- [other] Query each built image using `docker inspect --format='{{.Size}}'` to retrieve the uncompressed image size in bytes. Query the compressed size of each image stored on disk using `docker system df`: "Query each built image using `docker inspect --format='{{.Size}}'` to retrieve the uncompressed image size in bytes. Query the compressed size of each image stored on disk using `docker system df`"
- [other] Convert byte sizes to gigabytes and compare each against the documented range (cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB).: "Convert byte sizes to gigabytes and compare each against the documented range (cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB)."
- [other] Generate a structured verification report listing image name, measured size (GB), documented range, and pass/fail status for each variant.: "Generate a structured verification report listing image name, measured size (GB), documented range, and pass/fail status for each variant."
- [readme] AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project.: "AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project."
- [readme] Make sure that your operating system is Windows 7 or above with the .NET framework 4.7.2: "Make sure that your operating system is Windows 7 or above with the .NET framework 4.7.2"
