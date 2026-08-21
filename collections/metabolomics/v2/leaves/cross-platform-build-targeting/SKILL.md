---
name: cross-platform-build-targeting
description: Use when you have a Windows-only .NET Framework application that must
  run on non-Windows hosts (macOS or Linux), and you need reproducible, isolated execution
  with support for both interactive GUI and batch CLI workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3173
  tools:
  - C#
  - ProteoWizard
  - XQuartz
  - Docker Desktop for Mac
  - Docker Engine
  - Wine
  - .NET Framework 4.8
  license_tier: open
  provenance_tier: literature
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

# cross-platform-build-targeting

## Summary

Configure multi-stage Docker builds with platform-specific runtime targets to enable a Windows-only .NET Framework 4.8 GUI application (AirdPro) to execute on macOS and Linux hosts. This skill pairs application compilation in a build stage with Wine runtime environments, producing separate optimized image targets for Windows native, Linux GUI via X11, CLI-only batch processing, and development modes.

## When to use

You have a Windows-only .NET Framework application that must run on non-Windows hosts (macOS or Linux), and you need reproducible, isolated execution with support for both interactive GUI and batch CLI workflows. Apply this skill when Docker multi-stage builds and Wine compatibility layers are preferable to native cross-compilation or maintaining separate codebases.

## When NOT to use

- The source application is already natively compiled for Linux, macOS, or uses .NET Core/.NET 5+ (which have native cross-platform support); use native builds instead.
- The application requires hardware features (e.g., GPU acceleration, USB device passthrough) that Wine does not reliably expose.
- Performance-critical scenarios where Wine's emulation overhead (typically 10–30%) is unacceptable; consider native porting or lower-level virtualization.

## Inputs

- C# source code for .NET Framework 4.8 GUI application (AirdPro)
- Dockerfile template with multi-stage build configuration
- docker-compose.yml with resource limits and volume bindings
- Build orchestration script (e.g., build-docker.sh)
- Wine prefix initialization scripts and .NET Framework 4.8 installer

## Outputs

- Docker image tagged runtime-windows (Windows native container target)
- Docker image tagged runtime-linux (Linux with Wine and X11 GUI support)
- Docker image tagged runtime-cli (Linux CLI-only variant)
- Docker image tagged runtime-dev (development mode with debugging tools)
- docker-compose.yml with validated service definitions and resource constraints
- Build log confirming all targets compile without error

## How to apply

Create a multi-stage Dockerfile where the build stage installs the .NET Framework SDK, compiles the C# application from source, and produces application binaries; the runtime stage downloads Ubuntu 22.04, installs Wine and Windows compatibility libraries, initializes a Wine prefix with .NET Framework 4.8 runtime, and configures environment variables (especially DISPLAY for X11 GUI support). Define separate build targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) in the Dockerfile using BuildKit conditional logic or multiple FROM statements. Enable DOCKER_BUILDKIT=1, set resource limits (8GB memory, 4 CPU cores) in docker-compose.yml, and test each target by invoking the build script (e.g., build-docker.sh) to verify compilation and runtime configuration. For GUI execution on macOS/Linux, bind XQuartz socket and set X11 permissions (xhost +local:docker) on the host. Validate by running configuration tests and confirming all targets build without error and execute expected commands.

## Related tools

- **Docker Desktop for Mac** (Container runtime and multi-stage build orchestration on macOS hosts; version 20.10+ required) — https://www.docker.com/products/docker-desktop
- **Docker Engine** (Container runtime for Linux hosts; builds and executes multi-stage Docker images) — https://docs.docker.com/engine/
- **Wine** (Compatibility layer in runtime stage to execute Windows binaries and .NET Framework on Linux; initialized with prefix and environment configuration) — https://www.winehq.org/
- **.NET Framework 4.8** (Runtime installed in Wine prefix to execute the compiled C# application (AirdPro))
- **XQuartz** (X11 server on macOS for forwarding GUI display from Docker container to host desktop)
- **ProteoWizard** (msConvert library (pwiz_bindings_cli.dll) linked by AirdPro for vendor file format conversion) — https://proteowizard.sourceforge.io/
- **C#** (Source language of AirdPro application; compiled in build stage)

## Examples

```
export DOCKER_BUILDKIT=1 && docker build --target=runtime-linux -t airdpro:linux . && docker run --rm -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix airdpro:linux wine /app/AirdPro.exe
```

## Evaluation signals

- All four Docker image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) build without compilation errors; docker build --target=<target> completes successfully.
- Docker image introspection confirms Wine is installed, .NET Framework 4.8 runtime is present in the Wine prefix, and environment variables (WINEARCH, WINEPREFIX, DISPLAY) are correctly set: `docker inspect <image_id> --format='{{json .Config.Env}}'`
- Configuration test passes when executed: container successfully invokes the compiled application binary and reports expected version/help output.
- GUI target runs without X11/DISPLAY errors when XQuartz is configured on macOS (xhost +local:docker) and container is launched with -e DISPLAY=host.docker.internal:0 and socket binding.
- Resource limits are enforced: docker stats shows memory usage ≤ 8GB and CPU count ≤ 4 cores when running the container; no OOM kills or throttling occur during typical batch conversion workloads.

## Limitations

- Wine emulation introduces performance overhead (typically 10–30%) compared to native execution; not suitable for real-time or latency-sensitive operations.
- Wine does not reliably support all Windows system calls, COM interfaces, or graphics features; complex GUI elements (e.g., WinForms with custom rendering) may render incorrectly or not at all.
- X11 forwarding for GUI requires XQuartz (macOS) or Xvfb/similar (Linux headless) to be pre-configured on the host; network X11 forwarding has security and performance implications.
- The multi-stage build significantly increases Docker image size (~2–5 GB) due to SDK, compilation artifacts, Wine, and .NET Framework runtime; initial build time can exceed 10–30 minutes.
- Wine prefix initialization is one-time; changes to .NET Framework settings or Windows registry modifications inside the container do not persist unless volumes are properly bound or the image is rebased.

## Evidence

- [other] AirdPro is a C# GUI client written for .NET Framework 4.8 that requires a multi-stage Docker build configuration pairing application compilation with Wine runtime to run Windows applications in Linux containers, enabling execution on non-Windows hosts.: "C# GUI client written for .NET Framework 4.8 that requires a multi-stage Docker build configuration pairing application compilation with Wine runtime to run Windows applications in Linux containers"
- [other] Create a multi-stage Dockerfile with a build stage that downloads Ubuntu 22.04 base image, installs .NET Framework SDK, and compiles the AirdPro C# application from source.: "multi-stage Dockerfile with a build stage that downloads Ubuntu 22.04 base image, installs .NET Framework SDK, and compiles the AirdPro C# application from source"
- [other] Add Wine and required Windows compatibility libraries to the runtime stage. Install .NET Framework 4.8 runtime into the Wine environment.: "Add Wine and required Windows compatibility libraries to the runtime stage. Install .NET Framework 4.8 runtime into the Wine environment."
- [other] Define separate runtime targets for Windows native containers, Linux-based Wine execution, CLI-only variant, and development mode.: "Define separate runtime targets for Windows native containers, Linux-based Wine execution, CLI-only variant, and development mode."
- [other] Enable BuildKit optimization and configure resource limits in docker-compose.yml for memory (8GB) and CPU (4 cores).: "Enable BuildKit optimization and configure resource limits in docker-compose.yml for memory (8GB) and CPU (4 cores)."
- [other] Test the multi-stage build by invoking build-docker.sh script to verify all target stages compile without error. Validation: confirm all Docker image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) build successfully and run configuration test passes.: "invoking build-docker.sh script to verify all target stages compile without error. Validation: confirm all Docker image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) build"
- [methods] Download and install Docker Desktop for Mac: "Download and install Docker Desktop for Mac"
- [methods] Install XQuartz using Homebrew: "Install XQuartz using Homebrew"
- [methods] Check 'Allow connections from network clients' in Security tab: "Check 'Allow connections from network clients' in Security tab"
- [readme] AirdPro is a GUI client for conversion from vendor files to Aird files: "AirdPro is a GUI client for conversion from vendor files to Aird files"
- [readme] AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project.: "written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project"
