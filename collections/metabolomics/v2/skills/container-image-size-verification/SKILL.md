---
name: container-image-size-verification
description: Use when after completing a multi-stage Docker build targeting a compiled
  runtime environment (e.g., airdpro:cli produced from a Wine + .NET Framework 4.8
  + Ubuntu 22.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - AirdPro V5
  - Docker Desktop for Mac
  - Wine
  - .NET Framework 4.8
  - build-docker.sh
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

# container-image-size-verification

## Summary

Verify that a Docker container image built from a multi-stage Dockerfile has been successfully created and falls within expected size constraints (typically 6–7 GB for Wine-based runtime environments). This skill ensures the build process completed correctly before attempting container instantiation or deployment.

## When to use

After completing a multi-stage Docker build targeting a compiled runtime environment (e.g., airdpro:cli produced from a Wine + .NET Framework 4.8 + Ubuntu 22.04 base), verify image existence and size to confirm the build succeeded and produced an artifact within acceptable bounds before running functional tests or deploying to production.

## When NOT to use

- Image build is still in progress or has not yet been invoked; wait for the build process to complete before verification.
- Size constraint documentation is unavailable; verify with maintainers or prior build artifacts before applying this skill.
- Target image is a lightweight base image (e.g., alpine, scratch) where 6–7 GB expectation would be inapplicable.

## Inputs

- Docker daemon with completed multi-stage build
- Target image name string (e.g., 'airdpro:cli')
- Expected image size range (e.g., 6–7 GB)

## Outputs

- Verified Docker image presence and size metadata
- Binary executability confirmation (if functional test run)
- Boolean pass/fail status for size constraint

## How to apply

Query Docker using the `docker images` command to list all images and locate the target image by name (e.g., airdpro:cli). Extract the SIZE column and compare it against the expected range specified in the build documentation (6–7 GB for Wine-based CLI images). If the image size deviates significantly from the expected range, investigate whether the build completed normally or if intermediate layers were accidentally excluded. Once confirmed within range, optionally run a basic container instantiation (`docker run airdpro:cli --help`) to verify that the compiled binary is executable and responsive, signaling correct layer stacking and entry point configuration.

## Related tools

- **Docker Desktop for Mac** (Container runtime and image management; executes docker images query and docker run verification)
- **Wine** (Windows emulation layer integrated into the multi-stage build; contributes significantly to image size (6–7 GB range))
- **.NET Framework 4.8** (Runtime dependency installed in the Wine environment during build; contributes to final image size)
- **build-docker.sh** (Script that initiates the multi-stage Docker build with --linux-only flag; size verification is performed post-completion) — https://github.com/CSi-Studio/AirdPro

## Examples

```
docker images | grep airdpro:cli && docker run airdpro:cli --help
```

## Evaluation signals

- docker images output contains an entry with name='airdpro:cli' (or target image name) and TAG='latest' or versioned tag
- SIZE column for the target image is within the documented range (6–7 GB for Wine-based builds); deviations > 1 GB may indicate missing layers or bloat
- docker run airdpro:cli --help completes without error and outputs usage information, confirming binary executability and correct entry point
- Image creation timestamp is recent (within expected build duration, typically > 30 minutes for initial Wine + .NET Framework setup)
- No error logs or warnings in docker build output related to layer failure, dependency resolution, or disk space exhaustion

## Limitations

- Size range (6–7 GB) is specific to Wine + .NET Framework 4.8 + Ubuntu 22.04 base images; other base images or configurations will have different expected sizes and require updated constraints.
- First build may take significantly longer (> 30 minutes) due to Wine initialization and .NET Framework component downloads; subsequent builds using cached layers will be faster and produce identical image sizes only if no intermediate steps are modified.
- docker images SIZE column reflects compressed storage size; uncompressed in-memory footprint during execution may differ, and size alone does not guarantee runtime stability or performance (e.g., Wine incurs 20–30% performance degradation regardless of image size).
- Functional test (docker run --help) assumes the compiled binary exists at the expected entry point and responds to --help; missing or misconfigured entry point will fail this test despite correct image size.

## Evidence

- [other] Verify successful image creation by querying Docker for the airdpro:cli image and confirm its size falls within the expected 6–7 GB range using docker images command.: "Verify successful image creation by querying Docker for the airdpro:cli image and confirm its size falls within the expected 6–7 GB range using docker images command."
- [other] Optionally test image functionality by running a basic container instantiation from airdpro:cli to ensure the compiled AirdPro CLI binary is executable and responds to --help.: "Optionally test image functionality by running a basic container instantiation from airdpro:cli to ensure the compiled AirdPro CLI binary is executable and responds to --help."
- [methods] Wine needs to initialize and download .NET Framework components, taking more than 30 minutes: "Wine needs to initialize and download .NET Framework components, taking more than 30 minutes"
- [methods] Build all images (first build may take longer): "Build all images (first build may take longer)"
