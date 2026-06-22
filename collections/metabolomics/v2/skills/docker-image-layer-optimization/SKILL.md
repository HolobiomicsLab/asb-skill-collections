---
name: docker-image-layer-optimization
description: Use when you are building a Docker image for a .NET Framework 4.8 application (like AirdPro) that must run on both Windows native containers and Linux+Wine environments, and you need to reduce build time and image size while maintaining separate targets for GUI, CLI, and development modes.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Docker Desktop for Mac
  - Docker Engine
  - C#
  - ProteoWizard
  - XQuartz
  - Wine
  - .NET Framework 4.8
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- Docker Desktop for Mac (version 20.10+)
- this project enables AirdPro to run on macOS through Docker + Wine technology.
- Docker Engine or Docker Desktop
- AirdPro is written in C#
- pwiz_bindings_cli.dll from the ProteoWizard project
- based on pwiz_bindings_cli.dll from the ProteoWizard project.
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
---

# docker-image-layer-optimization

## Summary

Optimize multi-stage Docker builds for Windows .NET Framework applications running under Wine on Linux by structuring build and runtime stages to minimize layer bloat, enable BuildKit caching, and reduce final image size. This skill is essential when deploying GUI or CLI applications that require both compilation and runtime dependencies across heterogeneous host platforms.

## When to use

You are building a Docker image for a .NET Framework 4.8 application (like AirdPro) that must run on both Windows native containers and Linux+Wine environments, and you need to reduce build time and image size while maintaining separate targets for GUI, CLI, and development modes. Apply this skill when you have a multi-stage Dockerfile with a build stage (compilation) and a runtime stage (Wine + .NET Framework 4.8 runtime) and you want to leverage BuildKit optimization and resource constraints.

## When NOT to use

- Your application is already compiled as a single binary (.exe) and does not require in-container compilation; use a single-stage Dockerfile instead.
- You are targeting only Windows natively and do not need Wine or Linux runtime support; standard .NET Framework Docker images are simpler.
- Your build is I/O-bound on the host filesystem and BuildKit caching overhead would exceed the benefit; consider pre-compiling locally.

## Inputs

- Dockerfile with multi-stage build definition (build stage + runtime stage(s))
- C# application source code (.cs files)
- docker-compose.yml with resource limits and build configuration
- Build script (e.g., build-docker.sh) to orchestrate the build process

## Outputs

- Optimized Docker images for multiple targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev)
- Cached build layers eligible for reuse in subsequent builds
- Configuration test report confirming all targets built successfully

## How to apply

Structure your Dockerfile into separate build and runtime stages: the build stage installs .NET Framework SDK and compiles the C# application from source on an Ubuntu 22.04 base; the runtime stage adds Wine, Windows compatibility libraries, .NET Framework 4.8 runtime, and Wine prefix initialization. Enable DOCKER_BUILDKIT=1 before building to activate layer caching. Define multiple build targets (e.g., runtime-windows, runtime-linux, runtime-cli, runtime-dev) to allow selective image construction without rebuilding unnecessary layers. Configure memory (8 GB) and CPU (4 cores) limits in docker-compose.yml to prevent resource exhaustion during large multi-stage builds. Use --no-cache only when debugging; otherwise rely on BuildKit's layer caching to speed up incremental builds. Test all target stages by invoking the build script (build-docker.sh) and verify that each target compiles without error and the configuration test passes.

## Related tools

- **Docker Desktop for Mac** (Container runtime and build orchestration; required version 20.10+ to support BuildKit and resource limits configuration)
- **Docker Engine** (Alternative container runtime for Linux hosts; enables BuildKit optimization via DOCKER_BUILDKIT=1)
- **Wine** (Windows application compatibility layer installed in runtime stage to execute .NET Framework applications on Linux)
- **.NET Framework 4.8** (SDK installed in build stage for compilation; runtime installed in Wine prefix for execution)
- **C#** (Language of the AirdPro application source code compiled during the build stage)
- **ProteoWizard** (Provides pwiz_bindings_cli.dll dependency used by AirdPro at runtime)
- **XQuartz** (GUI display support for running AirdPro GUI variant on macOS via X11 forwarding)

## Examples

```
export DOCKER_BUILDKIT=1 && docker build --target runtime-linux -t airdpro:runtime-linux . && docker run --rm -e DISPLAY=host.docker.internal:0 airdpro:runtime-linux /opt/airdpro/AirdPro
```

## Evaluation signals

- All Docker image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) build without compilation or runtime errors.
- Configuration test (docker run ... && check health status) reports successful initialization for each target.
- Layer cache is reused across consecutive builds: compare docker build output for cache hits on non-modified layers (e.g., 'Using cache' messages).
- Final image sizes for each target are smaller than a non-optimized monolithic build by at least 10–20% (verify via docker images and docker history).
- Memory and CPU usage during build stays within configured limits (8 GB memory, 4 cores) and does not trigger OOM or throttling events.

## Limitations

- First build may take substantially longer than subsequent builds due to initial layer creation; plan accordingly.
- Wine prefix initialization and .NET Framework 4.8 runtime installation add significant size and startup latency to the runtime stage; not suitable for resource-constrained or serverless environments.
- BuildKit optimization requires DOCKER_BUILDKIT=1 environment variable; older Docker versions or CI/CD systems may not support it.
- GUI execution (AirdPro-gui target) requires X11 forwarding and XQuartz on macOS; headless/CLI targets are more portable.

## Evidence

- [other] multi-stage Docker build configuration pairing application compilation with Wine runtime to run Windows applications in Linux containers: "multi-stage Docker build configuration pairing application compilation with Wine runtime to run Windows applications in Linux containers, enabling execution on non-Windows hosts"
- [other] Create a multi-stage Dockerfile with a build stage that downloads Ubuntu 22.04 base image, installs .NET Framework SDK, and compiles the AirdPro C# application from source.: "Create a multi-stage Dockerfile with a build stage that downloads Ubuntu 22.04 base image, installs .NET Framework SDK, and compiles the AirdPro C# application from source"
- [other] Add Wine and required Windows compatibility libraries to the runtime stage. Install .NET Framework 4.8 runtime into the Wine environment.: "Add Wine and required Windows compatibility libraries to the runtime stage. Install .NET Framework 4.8 runtime into the Wine environment."
- [other] Define separate runtime targets for Windows native containers, Linux-based Wine execution, CLI-only variant, and development mode.: "Define separate runtime targets for Windows native containers, Linux-based Wine execution, CLI-only variant, and development mode."
- [other] Enable BuildKit optimization and configure resource limits in docker-compose.yml for memory (8GB) and CPU (4 cores).: "Enable BuildKit optimization and configure resource limits in docker-compose.yml for memory (8GB) and CPU (4 cores)"
- [other] Test the multi-stage build by invoking build-docker.sh script to verify all target stages compile without error. Validation: confirm all Docker image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) build successfully and run configuration test passes.: "Test the multi-stage build by invoking build-docker.sh script to verify all target stages compile without error. Validation: confirm all Docker image targets (runtime-windows, runtime-linux,"
- [other] AirdPro is a C# GUI client written for .NET Framework 4.8 that requires a multi-stage Docker build: "AirdPro is a C# GUI client written for .NET Framework 4.8 that requires a multi-stage Docker build"
- [methods] Download and install Docker Desktop for Mac: "Download and install Docker Desktop for Mac"
