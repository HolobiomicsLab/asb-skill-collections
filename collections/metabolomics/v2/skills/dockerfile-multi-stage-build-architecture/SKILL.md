---
name: dockerfile-multi-stage-build-architecture
description: Use when when you need to containerize a Windows-only .NET Framework
  GUI application (such as AirdPro V5/V6 written in C# for .NET Framework 4.8) for
  execution on macOS or Linux hosts, and you want to avoid shipping compile-time tooling
  (SDK) in the production image.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - C#
  - ProteoWizard
  - XQuartz
  - Docker Desktop for Mac
  - Docker Engine
  - Wine
  - .NET Framework 4.8
  techniques:
  - mass-spectrometry
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dockerfile-multi-stage-build-architecture

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Design and implement a multi-stage Docker build configuration that separates application compilation from runtime environment setup, enabling Windows-only .NET Framework applications (e.g., AirdPro) to execute on non-Windows hosts via Wine compatibility layer. This approach reduces final image size, isolates build dependencies, and supports multiple runtime targets (native Windows, Linux+Wine, CLI-only, development).

## When to use

When you need to containerize a Windows-only .NET Framework GUI application (such as AirdPro V5/V6 written in C# for .NET Framework 4.8) for execution on macOS or Linux hosts, and you want to avoid shipping compile-time tooling (SDK) in the production image. Multi-stage builds are the correct choice when the application cannot be natively compiled for Linux and requires Wine runtime emulation.

## When NOT to use

- Application is already compiled to native Linux binaries or supports native .NET Core/5+; use single-stage build instead.
- Target application is small and compile dependencies are minimal; overhead of multi-stage may not justify added complexity.
- Wine runtime is not compatible with the specific Windows libraries required by the application (e.g., proprietary COM objects, kernel drivers).

## Inputs

- C# source code repository (e.g., CSi-Studio/AirdPro)
- Base OS image specification (Ubuntu 22.04 recommended)
- Application dependencies list (.NET Framework 4.8, Wine, ProteoWizard pwiz_bindings_cli.dll)
- docker-compose.yml template with resource and environment specifications

## Outputs

- Multi-stage Dockerfile with named build targets
- Docker images: runtime-windows, runtime-linux, runtime-cli, runtime-dev
- docker-compose.yml with BuildKit directives and resource limits
- Build verification report (all targets compiled, configuration test passed)

## How to apply

Create a Dockerfile with at least two named stages: a build stage that downloads a base OS image (Ubuntu 22.04), installs .NET Framework SDK and required build tools, and compiles the C# source code; and a runtime stage that installs Wine and Windows compatibility libraries, injects the compiled binaries, and initializes the Wine prefix with .NET Framework 4.8 runtime installed into the prefix. Configure separate build targets (via `--target` flag) for different execution modes: `runtime-windows` for native Windows containers, `runtime-linux` for CLI/GUI via Wine, `runtime-cli` for batch processing without GUI overhead, and `runtime-dev` for interactive development. Enable Docker BuildKit (`export DOCKER_BUILDKIT=1`) to optimize layer caching and reduce rebuild times. Define resource limits in docker-compose.yml (e.g., memory: 8GB, cpus: 4) to prevent out-of-memory errors during large-scale conversions. Validate success by running `build-docker.sh` and confirming all four target stages build without error and the configuration test passes.

## Related tools

- **Docker Desktop for Mac** (Container build and execution environment; required for BuildKit and multi-stage image orchestration on macOS) — https://www.docker.com/products/docker-desktop
- **Docker Engine** (Container runtime and build system; executes Dockerfile instructions and manages layer caching) — https://docs.docker.com/engine/
- **Wine** (Windows compatibility layer and runtime environment; enables execution of Windows .NET Framework binaries in Linux containers) — https://www.winehq.org/
- **.NET Framework 4.8** (Runtime library for compiled AirdPro C# GUI application; must be installed into Wine prefix for bytecode execution)
- **XQuartz** (X11 display server for macOS; enables GUI rendering from Wine environment in containers running on macOS hosts) — https://www.xquartz.org/
- **ProteoWizard** (Mass spectrometry data library; pwiz_bindings_cli.dll dependency compiled into AirdPro for vendor file format support) — https://proteowizard.sourceforge.io/

## Examples

```
export DOCKER_BUILDKIT=1 && docker build --target=runtime-linux -t airdpro:latest . && docker-compose up -d airdpro-service && docker run --rm airdpro:latest --test
```

## Evaluation signals

- All four Docker build targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) complete without compile or runtime errors; validate with `docker build --target=<target-name> .`
- Configuration test passes: `docker run --rm airdpro:runtime-linux --test` exits with status 0 and reports health check OK
- Final runtime image size is ≤50% of build stage image size, confirming build dependencies (SDK) were not shipped to production
- GUI application launches and renders without errors when invoked via Wine in container with XQuartz X11 forwarding enabled; CLI variant executes batch conversion tasks without requiring display
- Memory consumption during large-scale multi-file conversion stays within defined resource limits (8GB max); verify via `docker stats` or health check monitoring

## Limitations

- Wine emulation introduces runtime overhead (~10–50% slower than native execution) and may not support all Windows GUI features (some proprietary controls, advanced DirectX rendering); suitable for CPU-bound batch conversion but may impact interactive responsiveness.
- GUI rendering on non-Windows hosts requires additional setup (XQuartz on macOS, VNC/X11 forwarding on Linux); CLI variant recommended for headless / batch environments.
- First build is significantly longer (~15–30 min) due to .NET Framework SDK download and compilation; subsequent builds cache build stage layers but any source code change triggers recompilation.
- Multi-stage builds require Docker BuildKit support (not available in legacy Docker daemon); older Docker versions or certain CI/CD platforms may not support `--target` flag.
- Wine prefix initialization and .NET Framework runtime installation must complete successfully at container startup; failures may not be obvious without health check validation; confirm via `docker inspect --format='{{.State.Health.Status}}'`.

## Evidence

- [other] What is the multi-stage Docker build architecture that enables AirdPro, a Windows-only .NET Framework 4.8 GUI application, to execute on non-Windows hosts?: "AirdPro is a C# GUI client written for .NET Framework 4.8 that requires a multi-stage Docker build configuration pairing application compilation with Wine runtime to run Windows applications in Linux"
- [other] How to build multi-stage Dockerfile: "Create a multi-stage Dockerfile with a build stage that downloads Ubuntu 22.04 base image, installs .NET Framework SDK, and compiles the AirdPro C# application from source. 2. Add Wine and required"
- [other] Runtime targets and BuildKit optimization: "Define separate runtime targets for Windows native containers, Linux-based Wine execution, CLI-only variant, and development mode. 6. Enable BuildKit optimization and configure resource limits in"
- [readme] AirdPro application details: "AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project."
- [readme] System requirements: "Make sure that your operating system is Windows 7 or above with the .NET framework 4.7.2"
