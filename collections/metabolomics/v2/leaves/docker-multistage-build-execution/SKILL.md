---
name: docker-multistage-build-execution
description: Use when you need to containerize a C#-based Windows application (like
  AirdPro CLI) for Linux deployment, require Wine and .NET Framework 4.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3786
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - AirdPro V5
  - Docker Desktop for Mac
  - Docker Compose
  - Wine
  - .NET Framework 4.8
  - ProteoWizard
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro V5 is now available at 2023.7
- Docker Desktop for Mac (version 20.10+)
- Docker Compose configuration
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

# docker-multistage-build-execution

## Summary

Execute a Docker multi-stage build pipeline to create containerized runtime images (e.g., airdpro:cli) that bundle compiled C# applications with Wine and .NET Framework dependencies on a Linux base. This skill is essential when deploying Windows-native tools into Linux container environments and needing to verify successful image creation and functionality.

## When to use

Use this skill when you need to containerize a C#-based Windows application (like AirdPro CLI) for Linux deployment, require Wine and .NET Framework 4.8 as runtime dependencies, and want to validate that the final image size and executable behavior meet expectations (6–7 GB range, executable responds to --help).

## When NOT to use

- Input binaries are already built for Linux (native .NET Core/5+) — skip Wine containerization and use native Linux base image instead.
- Target deployment environment is Windows or macOS — use native installers or Docker Desktop rather than Wine-based Linux containers.
- Image size constraints prohibit 6–7 GB footprint — consider lighter alternatives or pre-built public images instead of multi-stage rebuild.

## Inputs

- build-docker.sh build script with --linux-only flag
- Ubuntu 22.04 base image reference
- C# compiled binary (AirdPro CLI executable)
- pwiz_bindings_cli.dll from ProteoWizard
- Dockerfile multi-stage configuration

## Outputs

- Docker image tagged airdpro:cli
- Image size metric (expected 6–7 GB)
- Container instance with executable CLI binary
- Help output verification from --help invocation

## How to apply

Run the build-docker.sh script with the --linux-only flag to initiate the multi-stage Docker build targeting the runtime-cli stage. Monitor the build process as it downloads the Ubuntu 22.04 base image, installs Wine and dependencies, initializes the Wine environment, and installs .NET Framework 4.8. Verify successful image creation by querying Docker for the airdpro:cli image and confirm its size falls within the expected 6–7 GB range using the docker images command. Optionally test image functionality by running a basic container instantiation from airdpro:cli to ensure the compiled AirdPro CLI binary is executable and responds to --help, confirming both build success and runtime readiness.

## Related tools

- **Docker Desktop for Mac** (Container runtime and image builder for executing multi-stage Dockerfile build on local development machine)
- **Wine** (Windows application compatibility layer installed in Docker image to run .NET Framework 4.8 and C# binaries in Linux container)
- **.NET Framework 4.8** (Runtime dependency for C# compiled AirdPro binary, installed and executed through Wine within the container)
- **Docker Compose** (Optional orchestration tool for managing multi-container deployment of built airdpro:cli images)
- **ProteoWizard** (Source library (pwiz_bindings_cli.dll) linked into AirdPro C# application for mass spectrometry file format support)

## Examples

```
./build-docker.sh --linux-only && docker images | grep airdpro:cli && docker run airdpro:cli --help
```

## Evaluation signals

- docker images output confirms airdpro:cli image exists and size is within 6–7 GB range
- Container instantiation completes without Wine or .NET Framework initialization errors
- Invocation of container with --help flag produces CLI usage output (not segmentation fault or missing binary error)
- First run initialization time and performance degradation (expected 20–30% overhead) align with documented Wine behavior
- Multi-stage build log shows successful progression through Ubuntu base, Wine install, .NET Framework 4.8 download/setup, and binary compilation stages

## Limitations

- Wine introduces 20–30% performance degradation compared to native Windows execution; batch processing tasks may require significant runtime overhead.
- First run requires longer initialization time and Wine needs to initialize and download .NET Framework components, taking more than 30 minutes; subsequent runs are faster but initial build and container first-run must account for this overhead.
- Docker image size (6–7 GB) is substantial and may exceed storage or network constraints in resource-limited deployment environments.
- Multi-stage build is specific to Linux target; Windows or macOS deployments require alternative native packaging approaches outside this skill's scope.

## Evidence

- [other] AirdPro is built using Docker with Wine to run the C#-based application in Linux containers, leveraging .NET Framework 4.8 and pwiz_bindings_cli.dll from ProteoWizard: "AirdPro is built using Docker with Wine to run the C#-based application in Linux containers, leveraging .NET Framework 4.8 and pwiz_bindings_cli.dll from ProteoWizard"
- [other] Run the build-docker.sh script with the --linux-only flag to initiate the multi-stage Docker build targeting the runtime-cli stage: "Run the build-docker.sh script with the --linux-only flag to initiate the multi-stage Docker build targeting the runtime-cli stage"
- [other] Verify successful image creation by querying Docker for the airdpro:cli image and confirm its size falls within the expected 6–7 GB range using docker images command: "Verify successful image creation by querying Docker for the airdpro:cli image and confirm its size falls within the expected 6–7 GB range using docker images command"
- [methods] 20-30% performance degradation when running through Wine: "20-30% performance degradation when running through Wine"
- [methods] Wine needs to initialize and download .NET Framework components, taking more than 30 minutes: "Wine needs to initialize and download .NET Framework components, taking more than 30 minutes"
- [readme] AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project: "AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project"
