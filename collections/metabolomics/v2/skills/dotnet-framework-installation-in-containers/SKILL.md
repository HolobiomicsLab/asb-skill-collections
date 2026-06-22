---
name: dotnet-framework-installation-in-containers
description: Use when you need to containerize a C# application (e.g., AirdPro) that targets .NET Framework 4.8 and must run on Linux hosts via Docker, but the application was originally built for Windows. Use this skill when you are building multi-stage Docker images from a Ubuntu 22.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - AirdPro V5
  - .NET Framework 4.8
  - Docker
  - Wine
  - AirdPro V5/V6
  - ProteoWizard
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro V5 is now available at 2023.7
- .NET Framework 4.8 installed and run through Wine
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
---

# dotnet-framework-installation-in-containers

## Summary

Install and configure .NET Framework 4.8 within a Wine-enabled Linux container to run C#-based Windows applications like AirdPro in containerized environments. This skill bridges Windows/.NET dependencies with cross-platform container deployment.

## When to use

You need to containerize a C# application (e.g., AirdPro) that targets .NET Framework 4.8 and must run on Linux hosts via Docker, but the application was originally built for Windows. Use this skill when you are building multi-stage Docker images from a Ubuntu 22.04 base and must support Windows/.NET binaries without access to native .NET on Linux.

## When NOT to use

- The application is already a .NET Core or .NET 5+ application targeting Linux — use native .NET packages instead.
- Windows-native only features (e.g., COM interop, Win32 APIs beyond Wine's scope) are required and cannot be abstracted.
- Performance-critical workloads where 20–30% degradation through Wine emulation is unacceptable.

## Inputs

- Ubuntu 22.04 base container image
- Wine runtime package
- Wine dependencies (graphics libraries, DXVK, vcrun2015, etc.)
- .NET Framework 4.8 installer (.exe or redistributable)

## Outputs

- Docker image layer with initialized Wine prefix and .NET Framework 4.8 installed
- Functional Windows/.NET runtime environment within Linux container
- Verified container capable of executing C# binaries (e.g., airdpro:cli image)

## How to apply

In the Dockerfile, after installing Wine and its dependencies in a Ubuntu 22.04 base image, initialize the Wine environment (which sets up the Windows prefix) and then install .NET Framework 4.8 through Wine. The installation will download and configure the .NET Framework components, which may take more than 30 minutes on first run. Verify the installation by confirming the framework binaries are present in the Wine prefix and test that a sample C# executable or DLL (e.g., pwiz_bindings_cli.dll) can be invoked through Wine. Expect 20–30% performance degradation when running .NET applications through Wine due to emulation overhead.

## Related tools

- **Docker** (Container orchestration and image build system for multi-stage builds targeting Wine+.NET Framework environments)
- **Wine** (Windows compatibility layer that provides the Win32 API and runtime to execute .NET Framework applications on Linux)
- **.NET Framework 4.8** (Target runtime framework installed and executed through Wine to support C# applications like AirdPro)
- **AirdPro V5/V6** (Example C# application deployed in containerized form using this skill) — https://github.com/CSi-Studio/AirdPro
- **ProteoWizard** (Source library (pwiz_bindings_cli.dll) that AirdPro depends on and must be executable within the .NET Framework container)

## Evaluation signals

- Docker image builds successfully and reaches the runtime-cli or equivalent stage without .NET Framework installation errors.
- Final image size is within expected range (6–7 GB for AirdPro:cli), confirming all components were installed.
- Container instantiation completes and the C# binary responds to test invocations (e.g., `--help` flag for AirdPro CLI), indicating .NET Framework is functional.
- Wine prefix is initialized (presence of ~/.wine/drive_c directory in container) and contains Framework registry entries confirming Framework 4.8 registration.
- Performance profiling shows 20–30% overhead relative to native Windows execution, confirming expected degradation from Wine emulation.

## Limitations

- First-run initialization requires >30 minutes to download and install .NET Framework components; subsequent builds may cache layers to reduce latency.
- Wine introduces 20–30% performance degradation; compute-intensive workloads (large file conversions in AirdPro) may require optimization or resource tuning.
- Some advanced Win32 features and COM interop patterns may not work correctly through Wine; test application-specific functionality before production deployment.
- Container image size becomes large (6–7 GB) due to Wine, .NET Framework, and supporting libraries, impacting storage and image pull times.

## Evidence

- [other] The document describes that AirdPro is built using Docker with Wine to run the C#-based application in Linux containers, leveraging .NET Framework 4.8: "AirdPro is built using Docker with Wine to run the C#-based application in Linux containers, leveraging .NET Framework 4.8"
- [methods] Wine needs to initialize and download .NET Framework components, taking more than 30 minutes: "Wine needs to initialize and download .NET Framework components, taking more than 30 minutes"
- [methods] 20-30% performance degradation when running through Wine: "20-30% performance degradation when running through Wine"
- [other] Monitor the build process as it downloads the Ubuntu 22.04 base image, installs Wine and dependencies, initializes the Wine environment, and installs .NET Framework 4.8: "downloads the Ubuntu 22.04 base image, installs Wine and dependencies, initializes the Wine environment, and installs .NET Framework 4.8"
- [other] Verify successful image creation by querying Docker for the airdpro:cli image and confirm its size falls within the expected 6–7 GB range: "confirm its size falls within the expected 6–7 GB range using docker images command"
