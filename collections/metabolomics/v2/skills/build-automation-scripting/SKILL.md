---
name: build-automation-scripting
description: Use when when you have a Windows-only .NET Framework 4.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - C#
  - ProteoWizard
  - XQuartz
  - Docker Desktop for Mac
  - Docker Engine
  - Wine
  - .NET Framework 4.8
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro is written in C#
- pwiz_bindings_cli.dll from the ProteoWizard project
- based on pwiz_bindings_cli.dll from the ProteoWizard project.
- XQuartz (for GUI display support)
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

# build-automation-scripting

## Summary

Automate multi-stage Docker builds for cross-platform deployment of Windows-only .NET Framework applications using BuildKit optimization and resource-constrained orchestration. This skill enables reproducible, CI/CD-ready containerization of GUI and CLI variants with Wine runtime integration for non-Windows host execution.

## When to use

When you have a Windows-only .NET Framework 4.8 application (GUI or CLI) that must run on macOS or Linux hosts, and you need a reproducible, version-controlled build pipeline that generates separate runtime targets (native Windows, Linux+Wine, CLI-only, development) without manual compilation steps on each target OS.

## When NOT to use

- Input application is already compiled to x86_64 Linux binaries or native .NET Core — use containerization without Wine or multi-stage builds.
- Target deployment is Windows-only — native Windows binary or simpler Docker image for Windows containers is more efficient.
- Build resource constraints on the CI/CD host are < 2GB memory or single-core — the 8GB/4-core requirement will cause OOM or timeout failures.

## Inputs

- .NET Framework 4.8 C# source code
- Dockerfile with multi-stage configuration
- docker-compose.yml with resource limits and service definitions
- build-docker.sh automation script
- ProteoWizard dependencies (pwiz_bindings_cli.dll)
- Wine configuration templates (if pre-built)

## Outputs

- Docker image (runtime-windows target)
- Docker image (runtime-linux target with Wine integration)
- Docker image (runtime-cli target, headless)
- Docker image (runtime-dev target, debug-enabled)
- docker-compose environment file
- Build validation log confirming all stages compiled without error

## How to apply

Create a multi-stage Dockerfile that decouples the build stage (Ubuntu 22.04 base, .NET Framework SDK, C# compilation from source) from runtime stages (Wine+Windows compatibility libraries, .NET Framework 4.8 runtime, GUI/CLI environment configuration). Enable DOCKER_BUILDKIT=1 for optimization and define resource limits (8GB memory, 4 cores CPU) in docker-compose.yml. Configure Wine prefix initialization and separate build targets using Docker build stages: runtime-windows (native Windows execution), runtime-linux (Wine-based Linux execution), runtime-cli (headless CLI variant), and runtime-dev (development mode with debug symbols). Execute the build-docker.sh script to compile all targets. Validate that each Docker image target builds without error and the configuration test passes (typically via health check validation or container startup verification).

## Related tools

- **Docker Desktop for Mac** (Container runtime and build orchestration environment for multi-stage builds on macOS) — https://www.docker.com/products/docker-desktop
- **Docker Engine** (Container runtime for building and executing multi-stage Docker images on Linux hosts) — https://docs.docker.com/engine/
- **Wine** (Windows compatibility layer providing runtime environment for .NET Framework 4.8 and Windows GUI in Linux containers) — https://www.winehq.org/
- **.NET Framework 4.8** (Target runtime library compiled into Docker image runtime stage for executing AirdPro C# GUI and CLI binaries)
- **ProteoWizard** (Dependency library (pwiz_bindings_cli.dll) providing vendor format file I/O for AirdPro conversion logic) — https://github.com/CSi-Studio/AirdPro
- **XQuartz** (X11 server for forwarding GUI display from Wine-based containers to macOS host)

## Examples

```
export DOCKER_BUILDKIT=1; ./build-docker.sh; docker run --rm -v airdpro-data:/data airdpro:runtime-linux config-test
```

## Evaluation signals

- All four Docker image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) build successfully with no compilation errors in the build-docker.sh output log.
- Configuration test passes: `docker run --rm <image> config-test` or equivalent health check returns exit code 0.
- Docker image size for runtime-linux target is < 2GB (Wine + .NET Framework overhead is typical; significant deviation indicates bloat or missing layer optimization).
- Container starts without 'OutOfMemory' or resource allocation failures when docker-compose.yml memory limit (8GB) and CPU limit (4 cores) are applied via `docker inspect` or `docker stats`.
- GUI variant runs without Wine or X11 socket errors when invoked with `xhost +local:docker` and DISPLAY forwarding enabled; CLI variant executes without X11 dependency.

## Limitations

- Multi-stage builds increase total build time (first build may take 20+ minutes) due to .NET Framework SDK download, compilation, and Wine environment setup in container.
- Wine runtime introduces a ~5–10% performance overhead compared to native Windows execution; CPU-intensive conversions may be slower than native .NET Framework 4.8 on Windows.
- GUI rendering via Wine + X11 forwarding to macOS (via XQuartz) may encounter display glitches or color space mismatches; headless CLI variant is more reliable for batch processing.
- ProteoWizard vendor format support depends on pwiz_bindings_cli.dll version and Wine's ability to load Windows DLLs; format support matrix does not expand beyond what ProteoWizard upstream supports.
- BuildKit optimization requires DOCKER_BUILDKIT=1 environment variable; older Docker versions or CI/CD systems may not support this feature, requiring fallback to classic build mode.

## Evidence

- [other] AirdPro is a C# GUI client written for .NET Framework 4.8 that requires a multi-stage Docker build configuration pairing application compilation with Wine runtime to run Windows applications in Linux containers.: "AirdPro is a C# GUI client written for .NET Framework 4.8 that requires a multi-stage Docker build configuration pairing application compilation with Wine runtime to run Windows applications in Linux"
- [other] 1. Create a multi-stage Dockerfile with a build stage that downloads Ubuntu 22.04 base image, installs .NET Framework SDK, and compiles the AirdPro C# application from source. 2. Add Wine and required Windows compatibility libraries to the runtime stage.: "Create a multi-stage Dockerfile with a build stage that downloads Ubuntu 22.04 base image, installs .NET Framework SDK, and compiles the AirdPro C# application from source. 2. Add Wine and required"
- [other] Define separate runtime targets for Windows native containers, Linux-based Wine execution, CLI-only variant, and development mode.: "Define separate runtime targets for Windows native containers, Linux-based Wine execution, CLI-only variant, and development mode."
- [other] Enable BuildKit optimization and configure resource limits in docker-compose.yml for memory (8GB) and CPU (4 cores).: "Enable BuildKit optimization and configure resource limits in docker-compose.yml for memory (8GB) and CPU (4 cores)."
- [other] Test the multi-stage build by invoking build-docker.sh script to verify all target stages compile without error. Validation: confirm all Docker image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) build successfully and run configuration test passes.: "Test the multi-stage build by invoking build-docker.sh script to verify all target stages compile without error. Validation: confirm all Docker image targets build successfully and run configuration"
- [readme] AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project.: "AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project."
- [readme] By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format.: "By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format."
