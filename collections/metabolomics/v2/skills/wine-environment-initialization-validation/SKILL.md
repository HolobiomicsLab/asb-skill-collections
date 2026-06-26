---
name: wine-environment-initialization-validation
description: Use when use this skill after building a Docker image that installs Wine
  and .NET Framework 4.8 on a Ubuntu 22.04 base, but before running production conversion
  tasks or batch jobs with AirdPro.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - AirdPro V5
  - Wine
  - .NET Framework 4.8
  - Docker Desktop for Mac
  - AirdPro V5 / V6
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro V5 is now available at 2023.7
- Wine to run Windows applications in Linux containers
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

# Wine Environment Initialization and Validation

## Summary

Verify that a Wine environment has successfully initialized .NET Framework 4.8 and associated dependencies before executing Windows-based scientific applications (such as AirdPro CLI) in Linux containers. This skill is essential when deploying C#-based proteomics tools via Docker on non-Windows hosts, as Wine initialization is a prerequisite for correct binary execution and can consume >30 minutes.

## When to use

Use this skill after building a Docker image that installs Wine and .NET Framework 4.8 on a Ubuntu 22.04 base, but before running production conversion tasks or batch jobs with AirdPro. Initialization is critical on first-run and after container restart, particularly when the Wine prefix has not yet downloaded and cached .NET Framework components.

## When NOT to use

- Input is a Windows-native AirdPro installation or a pre-initialized Wine container with cached .NET Framework (use direct execution instead of validation).
- You are running GUI-based AirdPro; XQuartz display configuration and GUI rendering validation take precedence over CLI binary validation.
- The deployment target is a production cluster with containerized Wine environments already validated in a prior build stage (skip re-initialization and move directly to task submission).

## Inputs

- Docker container instance from airdpro:cli image
- Ubuntu 22.04 base with Wine environment and .NET Framework 4.8 installed
- AirdPro CLI binary (compiled C# executable)

## Outputs

- Initialized Wine prefix with cached .NET Framework 4.8 components
- Validated AirdPro CLI binary ready for conversion tasks
- Initialization log documenting completion time and performance baseline

## How to apply

After launching a container from the airdpro:cli image, allow Wine to initialize by running a basic container instantiation with a lightweight test command (e.g., `airdpro --help`). Monitor process output and system logs for evidence that Wine has downloaded .NET Framework 4.8 components and completed environment setup. This first-run initialization typically takes >30 minutes and produces 20–30% performance degradation on subsequent invocations. Confirm successful initialization by verifying that the compiled AirdPro CLI binary responds to the help flag and does not throw runtime errors related to missing .NET assemblies (e.g., pwiz_bindings_cli.dll). Document the initialization timestamp to distinguish first-run overhead from steady-state performance baselines.

## Related tools

- **Wine** (Runtime environment that bridges Windows .NET Framework execution in Linux containers; initialization downloads and caches .NET Framework 4.8 components)
- **.NET Framework 4.8** (Dependency runtime for C#-based AirdPro binary; must be installed and initialized within Wine prefix before CLI execution)
- **Docker Desktop for Mac** (Container orchestration and image management; required to build airdpro:cli image and instantiate containers for Wine initialization validation)
- **AirdPro V5 / V6** (CLI application under test; binary execution validates that Wine environment and .NET Framework initialization were successful) — https://github.com/CSi-Studio/AirdPro

## Evaluation signals

- Container successfully executes `airdpro --help` without .NET runtime errors or missing assembly (pwiz_bindings_cli.dll) exceptions
- First-run initialization log shows >30 minutes elapsed time for Wine prefix setup and .NET Framework 4.8 component download; subsequent runs show 20–30% performance degradation relative to Windows native baseline
- Docker image size falls within expected 6–7 GB range (confirming complete .NET Framework and dependency installation)
- Wine prefix directory (/root/.wine or equivalent) contains cached assemblies and .NET configuration after first run (verify via `find /root/.wine -name '*.dll' | grep -i framework`)
- No stderr warnings about missing or broken dependencies when running the test invocation

## Limitations

- Wine initialization requires >30 minutes on first run, making it unsuitable for rapid iterative container testing; plan initialization as a separate, documented step in CI/CD pipelines.
- 20–30% performance degradation vs. Windows native execution is inherent to Wine emulation; this skill validates that degradation is acceptable for the intended workload (batch conversion of proteomics files), not that it eliminates the overhead.
- Wine prefix is tied to a specific container instance or volume mount; re-initializing across multiple containers requires either volume sharing or image rebuilding with cached .wine, adding complexity.
- The skill assumes .NET Framework 4.8 is correctly installed in the Dockerfile; if installation fails silently, validation will detect missing assemblies only at runtime.

## Evidence

- [methods] the first run requires longer initialization time: "the first run requires longer initialization time"
- [methods] Wine needs to initialize and download .NET Framework components, taking more than 30 minutes: "Wine needs to initialize and download .NET Framework components, taking more than 30 minutes"
- [methods] 20-30% performance degradation when running through Wine: "20-30% performance degradation when running through Wine"
- [other] Verify successful image creation by querying Docker for the airdpro:cli image and confirm its size falls within the expected 6–7 GB range using docker images command. Optionally test image functionality by running a basic container instantiation from airdpro:cli to ensure the compiled AirdPro CLI binary is executable and responds to --help.: "Optionally test image functionality by running a basic container instantiation from airdpro:cli to ensure the compiled AirdPro CLI binary is executable and responds to --help"
- [readme] AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project: "AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project"
