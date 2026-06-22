---
name: docker-container-runtime-execution-and-monitoring
description: Use when you have a vendor mass spectrometry raw file (e.g., .raw format) that requires conversion to Aird format using AirdPro CLI, and you are running on macOS or Linux.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Docker Desktop for Mac
  - AirdPro V5
  - AirdPro V6
  - ProteoWizard
  - Wine
  - .NET Framework 4.8
  - AirdPro V5 / V6
  - XQuartz
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- Docker Desktop for Mac (version 20.10+)
- AirdPro V5 is now available at 2023.7
- AirdPro V6 is now available at 2024.4
- pwiz_bindings_cli.dll from the ProteoWizard project
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

# docker-container-runtime-execution-and-monitoring

## Summary

Execute a containerized application (e.g. AirdPro CLI) within a Docker container with mounted input/output volumes, monitor initialization overhead and runtime behavior, and verify output file integrity. This skill is essential when deploying Windows/.NET applications on macOS/Linux via Wine emulation, where first-run setup can exceed 30 minutes.

## When to use

You have a vendor mass spectrometry raw file (e.g., .raw format) that requires conversion to Aird format using AirdPro CLI, and you are running on macOS or Linux. Docker Desktop and Wine initialization have not yet been performed, or you need to document the initialization and runtime behavior of the containerized conversion pipeline.

## When NOT to use

- Input file is already in Aird format (.aird + .json pair) — skip conversion.
- You are running AirdPro on native Windows with .NET Framework 4.7.2+ already installed — use the GUI or direct CLI executable instead of Docker/Wine.
- The vendor file format is not supported by ProteoWizard MSConvert (AirdPro's underlying library) — consult the supported format list before attempting conversion.

## Inputs

- Vendor mass spectrometry raw file (e.g., .raw format from Thermo, Agilent, or Waters)
- Docker image: airdpro:cli (pre-built or built from CSi-Studio/AirdPro repository)
- Host directory path for input vendor files
- Host directory path for output Aird files

## Outputs

- Aird data file (.aird suffix)
- Aird index file (.json suffix with same base name as .aird file)
- Container execution log with timestamps for Wine initialization and .NET Framework download
- Runtime duration (wall-clock time from run-cli.sh invocation to completion)

## How to apply

Launch the airdpro:cli Docker container with volume mounts pointing to input vendor raw data and a designated output directory. Execute the run-cli.sh script within the container against the sample vendor file. On first run, Wine will initialize and download .NET Framework 4.8 components—this process is documented to take more than 30 minutes; monitor and record the wall-clock time and log output. Once conversion completes, verify output file existence, measure its size, and check the file format signature (Aird files should have .aird and accompanying .json index files in the same directory with matching base names). Confirm that no conversion errors appear in the container logs and that the output directory contains the expected Aird data and index files.

## Related tools

- **Docker Desktop for Mac** (Container runtime and orchestration for macOS; required to build, manage, and execute the airdpro:cli image with mounted volumes)
- **Wine** (Windows application emulator running inside the Linux container; initializes on first run to enable .NET Framework 4.8 execution; introduces 20–30% performance degradation)
- **.NET Framework 4.8** (Runtime for AirdPro C# application; downloaded and cached by Wine during first-run initialization (>30 minutes))
- **AirdPro V5 / V6** (CLI application executed within the container to convert vendor mass spectrometry files to Aird format) — https://github.com/CSi-Studio/AirdPro
- **ProteoWizard** (Underlying library (pwiz_bindings_cli.dll) providing vendor file format support for AirdPro conversion)
- **XQuartz** (Optional; provides X11 display server for GUI version on macOS if display forwarding is needed)

## Examples

```
docker run --rm -v /path/to/vendor/files:/input -v /path/to/output:/output airdpro:cli /bin/bash -c '/home/airdpro/run-cli.sh /input/sample.raw /output'
```

## Evaluation signals

- Output .aird file exists in the mounted output directory with non-zero file size
- Corresponding .json index file exists in the same directory with matching base name (e.g., sample.aird and sample.json)
- Container log shows 'Wine initialization' message(s) followed by .NET Framework component downloads on first run; subsequent runs skip this phase
- First-run execution duration is >30 minutes (as documented); subsequent runs complete significantly faster
- No error or exception messages in container stderr/stdout related to file I/O, format parsing, or .NET runtime failures

## Limitations

- First-run initialization requires >30 minutes due to Wine and .NET Framework 4.8 setup; this overhead is unavoidable on fresh container instances.
- 20–30% performance degradation is incurred by Wine emulation layer compared to native Windows/.NET execution.
- Only vendor file formats supported by ProteoWizard MSConvert can be converted; unsupported formats will fail silently or with cryptic Wine/DLL errors.
- Volume mount permissions and path encoding on the host must be correctly configured, or the container cannot read input files or write output files.
- The airdpro:cli image build may take longer on first build due to dependency installation and Wine setup within the container.

## Evidence

- [other] AirdPro converts vendor mass spectrometry files to Aird format; first-run execution requires Wine to initialize and download .NET Framework components, a process documented to take more than 30 minutes.: "AirdPro converts vendor mass spectrometry files to Aird format; first-run execution requires Wine to initialize and download .NET Framework components, a process documented to take more than 30"
- [other] Launch the airdpro:cli container with volume mounts for input vendor raw data and output directory. Trigger Wine initialization by executing run-cli.sh against a sample vendor mass spectrometry raw file (e.g., .raw format). Monitor and record the first-run Wine startup and .NET Framework component download time.: "Launch the airdpro:cli container with volume mounts for input vendor raw data and output directory. Trigger Wine initialization by executing run-cli.sh against a sample vendor mass spectrometry raw"
- [other] Verify that the Aird conversion process completes and produces a named output Aird file in the mounted output directory. Confirm file integrity by checking file existence, size, and format signature.: "Verify that the Aird conversion process completes and produces a named output Aird file in the mounted output directory. Confirm file integrity by checking file existence, size, and format signature."
- [readme] Aird Index File and Aird Data File show be stored in the same directory with the same file name but with different suffix: "Aird Index File and Aird Data File show be stored in the same directory with the same file name but with different suffix"
- [readme] Docker Desktop for Mac (version 20.10+); Wine to run Windows applications in Linux containers; .NET Framework 4.8 installed and run through Wine: "Docker Desktop for Mac (version 20.10+); Wine to run Windows applications in Linux containers; .NET Framework 4.8 installed and run through Wine"
- [readme] 20-30% performance degradation when running through Wine: "20-30% performance degradation when running through Wine"
