---
name: wine-windows-runtime-configuration
description: Use when you have a Windows-only C# GUI application (e.g., AirdPro) built for .NET Framework 4.8 that needs to run on non-Windows hosts (macOS or Linux), and you are using a multi-stage Docker build where the runtime stage includes Wine and Windows compatibility libraries.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Wine
  - C#
  - ProteoWizard
  - XQuartz
  - .NET Framework 4.8
  - Docker Engine
  - winetricks
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- Wine to run Windows applications in Linux containers
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
---

# wine-windows-runtime-configuration

## Summary

Configure Wine runtime environment to execute Windows-only .NET Framework 4.8 GUI applications in Linux containers on macOS/Linux hosts. This skill enables platform-agnostic deployment of compiled C# applications by initializing Wine prefix, installing .NET Framework runtime into the Wine environment, and setting environment variables for both GUI and CLI execution paths.

## When to use

You have a Windows-only C# GUI application (e.g., AirdPro) built for .NET Framework 4.8 that needs to run on non-Windows hosts (macOS or Linux), and you are using a multi-stage Docker build where the runtime stage includes Wine and Windows compatibility libraries. Apply this skill after the application compilation stage and before testing execution.

## When NOT to use

- The application is already a native Linux/macOS binary or uses cross-platform .NET (e.g., .NET 6+) — use native containerization instead.
- Wine prefix initialization and .NET Framework runtime installation succeed but the application still fails to locate vendor libraries (e.g., ProteoWizard DLLs) — this indicates a dependency resolution issue outside Wine configuration; check library paths and DLL registration.
- You are targeting Windows native containers — Wine is unnecessary; use the Windows Server base image and native .NET Framework runtime.

## Inputs

- Multi-stage Dockerfile with build stage completed (compiled C# application binaries present)
- Ubuntu 22.04 (or equivalent Linux) runtime base image
- Wine installation package and Windows compatibility libraries list
- .NET Framework 4.8 installer or winetricks definitions

## Outputs

- Docker runtime image with Wine prefix initialized and .NET Framework 4.8 installed
- Configured environment variables (WINEPREFIX, DISPLAY, WINEARCH) embedded in image or entrypoint
- Separate entrypoint scripts for GUI and CLI execution modes
- Persistent Wine prefix directory (e.g., mounted volume or image layer)

## How to apply

In the Docker runtime stage, install Wine and required Windows compatibility libraries (e.g., via `apt-get` on Ubuntu 22.04), then download and install the .NET Framework 4.8 runtime into the Wine environment using Wine's winetricks or manual installation. Initialize the Wine prefix (the WINEPREFIX environment variable should point to a persistent directory, typically /root/.wine or a mounted volume). Configure environment variables including WINEPREFIX, DISPLAY (for GUI forwarding via XQuartz on macOS or X11 on Linux), and WINEARCH (typically win64). Define separate entrypoint scripts or CMD directives for GUI execution (which requires X11 socket forwarding) and CLI-only execution (which may not require display). The rationale is that Wine requires explicit prefix initialization and environment setup to locate the Windows runtime, registry, and system libraries; without these, the Windows application cannot locate .NET Framework dependencies or display resources.

## Related tools

- **Wine** (Runtime layer for executing Windows applications and .NET Framework in Linux containers) — https://www.winehq.org/
- **.NET Framework 4.8** (Windows runtime that must be installed into Wine prefix to support AirdPro C# application execution)
- **Docker Engine** (Container orchestration and multi-stage build execution to assemble build and runtime stages)
- **XQuartz** (X11 server on macOS required to forward GUI display from Wine runtime inside Docker container)
- **winetricks** (Optional utility to automate .NET Framework and Windows dependency installation into Wine prefix)

## Evaluation signals

- Wine prefix directory exists and is writable at WINEPREFIX path; `ls -la $WINEPREFIX` returns drive_c, system.reg, and user.reg files.
- .NET Framework 4.8 runtime is installed in Wine prefix; `wine --version` and `wine cmd /c wmic os get osversion` execute without error.
- Environment variables WINEPREFIX, DISPLAY, and WINEARCH are set correctly in container; `docker inspect <image>` shows Env field contains these variables.
- GUI entrypoint can connect to X11 display; running the entrypoint with X11 forwarding (e.g., docker run -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix) produces no socket connection errors in Wine logs.
- CLI entrypoint executes without DISPLAY; `docker run --rm <image> cli-entrypoint.sh` completes without 'DISPLAY not set' or similar GUI-related errors.

## Limitations

- Wine runtime incurs non-negligible CPU and memory overhead compared to native binaries; AirdPro Docker configuration specifies memory limit of 8GB and 4 CPU cores as practical minimum.
- GUI forwarding requires X11 server availability on the host (XQuartz on macOS, X11 on Linux) and network-accessible socket; network-isolated or headless environments cannot use GUI mode.
- .NET Framework 4.8 installation into Wine is a slow, one-time operation during image build; initial Docker build may take significantly longer than native Linux applications.
- Wine does not guarantee 100% Windows API compatibility; vendor libraries (e.g., ProteoWizard pwiz_bindings_cli.dll) may have undocumented dependencies or edge cases that fail under Wine emulation.
- Persistent data (Wine registry, user profiles, application state) must be managed via Docker volumes to survive container restart; without volume mounts, all runtime state is ephemeral.

## Evidence

- [other] AirdPro is a C# GUI client written for .NET Framework 4.8 that requires a multi-stage Docker build configuration pairing application compilation with Wine runtime to run Windows applications in Linux containers, enabling execution on non-Windows hosts.: "C# GUI client written for .NET Framework 4.8 that requires a multi-stage Docker build configuration pairing application compilation with Wine runtime to run Windows applications in Linux containers"
- [other] Add Wine and required Windows compatibility libraries to the runtime stage. 3. Install .NET Framework 4.8 runtime into the Wine environment. 4. Configure Wine prefix initialization and environment variables for GUI and CLI execution paths.: "Add Wine and required Windows compatibility libraries to the runtime stage. Install .NET Framework 4.8 runtime into the Wine environment. Configure Wine prefix initialization and environment"
- [methods] Wine to run Windows applications in Linux containers: "Wine to run Windows applications in Linux containers"
- [methods] Download and install Docker Desktop for Mac: "Download and install Docker Desktop for Mac"
- [methods] Install XQuartz using Homebrew: "Install XQuartz using Homebrew"
- [methods] Check 'Allow connections from network clients' in Security tab: "Check 'Allow connections from network clients' in Security tab"
- [methods] Set memory and CPU limits in docker-compose.yml: "Set memory and CPU limits in docker-compose.yml"
- [readme] Make sure that your operating system is Windows 7 or above with the .NET framework 4.7.2: "Make sure that your operating system is Windows 7 or above with the .NET framework 4.7.2"
