---
name: dotnet-framework-compilation-in-containers
description: Use when you have a C# GUI application targeting .NET Framework 4.8 (Windows-only)
  and need to execute it on macOS or Linux hosts without modifying the source code.
  The application requires compilation from source and GUI display support via X11
  forwarding or headless CLI execution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3431
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - .NET Framework
  - C#
  - ProteoWizard
  - XQuartz
  - Docker Desktop for Mac
  - Docker Engine
  - Wine
  - .NET Framework SDK
  - CSi-Studio/AirdPro
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- .NET Framework 4.8
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

# dotnet-framework-compilation-in-containers

## Summary

Compile .NET Framework 4.8 GUI applications in multi-stage Docker containers to enable Windows-only binaries to run on non-Windows hosts via Wine runtime integration. This skill pairs .NET SDK compilation in a Linux build stage with Wine environment setup and .NET Framework runtime installation in the runtime stage.

## When to use

You have a C# GUI application targeting .NET Framework 4.8 (Windows-only) and need to execute it on macOS or Linux hosts without modifying the source code. The application requires compilation from source and GUI display support via X11 forwarding or headless CLI execution.

## When NOT to use

- Application is already compiled to a native binary (exe, dll) and does not require recompilation from source within the container.
- Application targets modern .NET Core or .NET 5+ and can run natively on Linux without Wine.
- GUI display is not required and Wine overhead is unacceptable for performance-critical CLI-only workloads.

## Inputs

- C# source code repository (e.g., CSi-Studio/AirdPro)
- Project file (.csproj or .sln)
- Dockerfile template with multi-stage build definition
- docker-compose.yml with resource and volume configuration
- Build script (e.g., build-docker.sh)

## Outputs

- Docker image with compiled .NET Framework 4.8 application
- Wine-configured container runtime environment
- Multiple tagged image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev)
- Compiled application binary executable within container

## How to apply

Create a multi-stage Dockerfile with a dedicated build stage that downloads an Ubuntu 22.04 base image, installs the .NET Framework SDK, and compiles the C# application from source. In the runtime stage, install Wine and required Windows compatibility libraries, then install the .NET Framework 4.8 runtime into the Wine prefix. Configure Wine environment variables (WINEPREFIX, DISPLAY) for GUI execution via XQuartz or CLI-only modes. Define separate runtime targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) in the Dockerfile to allow selective builds. Enable Docker BuildKit optimization via `export DOCKER_BUILDKIT=1` and configure resource limits (8GB memory, 4 cores CPU) in docker-compose.yml. Validate by invoking the build script and confirming all target stages compile and the runtime configuration test passes without error.

## Related tools

- **Docker Desktop for Mac** (Container orchestration and multi-stage build execution on macOS hosts) — https://www.docker.com/products/docker-desktop
- **Docker Engine** (Container runtime and build system supporting BuildKit optimization) — https://docs.docker.com/engine/
- **Wine** (Windows runtime environment to execute compiled .NET Framework binaries in Linux containers) — https://www.winehq.org/
- **.NET Framework SDK** (Compiler and build tools for C# source code compilation in the Docker build stage) — https://dotnet.microsoft.com/download/dotnet-framework
- **XQuartz** (X11 display server for GUI rendering on macOS) — https://www.xquartz.org/
- **ProteoWizard** (Source dependency (pwiz_bindings_cli.dll) for AirdPro application functionality) — http://proteowizard.sourceforge.net/
- **CSi-Studio/AirdPro** (Reference C# GUI application demonstrating this compilation skill) — https://github.com/CSi-Studio/AirdPro

## Examples

```
export DOCKER_BUILDKIT=1 && docker build --target runtime-linux --memory=8g --cpus=4 -t airdpro:linux . && docker run --rm -e DISPLAY=host.docker.internal:0 airdpro:linux
```

## Evaluation signals

- All multi-stage Docker build targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) complete without compilation errors.
- Docker configuration test passes: `docker run --rm <image> ./test-config.sh` returns exit code 0.
- Wine prefix is correctly initialized in runtime container: `wine --version` executes and .NET Framework 4.8 is registered in the Wine environment.
- GUI application launches successfully with X11 forwarding: `xhost +local:docker` and `docker run --rm -e DISPLAY=host.docker.internal:0 <gui-image>` displays the AirdPro window.
- CLI variant runs in batch mode without GUI dependency: `docker run --rm <cli-image> airdpro-cli.exe --convert <input> <output>` completes and produces expected Aird output files.

## Limitations

- Wine introduces performance overhead compared to native Windows execution; large-scale batch conversions may be slower than native .NET Framework on Windows.
- GUI rendering requires X11 forwarding setup (XQuartz on macOS, X server on Linux), adding complexity to deployment and making headless-only execution preferable for server environments.
- First multi-stage build is time-intensive (SDK + runtime installation); subsequent builds benefit from layer caching but require explicit `--no-cache` flag to force full recompilation.
- Wine compatibility is version-dependent; edge cases in COM interop, P/Invoke to Windows-specific APIs, or unusual GDI+ usage may cause runtime failures not apparent during compilation.
- Memory and CPU limits (8GB, 4 cores) must be tuned per workload; conversion of very large mass spectrometry files may exceed these resource constraints.

## Evidence

- [other] AirdPro is a C# GUI client written for .NET Framework 4.8 that requires a multi-stage Docker build configuration pairing application compilation with Wine runtime to run Windows applications in Linux containers, enabling execution on non-Windows hosts.: "AirdPro is a C# GUI client written for .NET Framework 4.8 that requires a multi-stage Docker build configuration pairing application compilation with Wine runtime to run Windows applications in Linux"
- [other] Create a multi-stage Dockerfile with a build stage that downloads Ubuntu 22.04 base image, installs .NET Framework SDK, and compiles the AirdPro C# application from source.: "Create a multi-stage Dockerfile with a build stage that downloads Ubuntu 22.04 base image, installs .NET Framework SDK, and compiles the AirdPro C# application from source."
- [other] Add Wine and required Windows compatibility libraries to the runtime stage. Install .NET Framework 4.8 runtime into the Wine environment.: "Add Wine and required Windows compatibility libraries to the runtime stage. Install .NET Framework 4.8 runtime into the Wine environment."
- [other] Define separate runtime targets for Windows native containers, Linux-based Wine execution, CLI-only variant, and development mode.: "Define separate runtime targets for Windows native containers, Linux-based Wine execution, CLI-only variant, and development mode."
- [other] Enable BuildKit optimization and configure resource limits in docker-compose.yml for memory (8GB) and CPU (4 cores).: "Enable BuildKit optimization and configure resource limits in docker-compose.yml for memory (8GB) and CPU (4 cores)."
- [other] confirm all Docker image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) build successfully and run configuration test passes.: "confirm all Docker image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) build successfully and run configuration test passes."
- [readme] AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project.: "AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project."
- [readme] Make sure that your operating system is Windows 7 or above with the .NET framework 4.7.2: "Make sure that your operating system is Windows 7 or above with the .NET framework 4.7.2"
