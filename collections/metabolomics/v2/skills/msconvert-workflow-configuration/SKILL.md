---
name: msconvert-workflow-configuration
description: Use when when you need to convert vendor-specific raw mass spectrometry
  files (.raw) to the open mzML format using imzML Writer, and msconvert is not yet
  installed or its location is not recognized by the system.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - msconvert
  - ProteoWizard
  - Python
  - Docker
  - imzML Writer
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.4c06520
  title: imzML Writer
evidence_spans:
- imzML Writer relies on MS convert to convert raw instrument data into the open format
  mzML, requiring a working install.
- imzML Writer relies on MS convert to convert raw instrument data into the open format
  mzML.
- On PC, download the latest msconvert release from ProteoWizard
- 'On PC, this can be installed normally from Proteowizard: https://proteowizard.sourceforge.io/download.html'
- import os import imzml_writer.utils as iw_utils
- iw_utils.mzML_to_imzML_convert(PATH=mzML_path)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_imzml_writer_cq
    doi: 10.1021/acs.analchem.4c06520
    title: imzML Writer
  dedup_kept_from: coll_imzml_writer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06520
  all_source_dois:
  - 10.1021/acs.analchem.4c06520
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msconvert-workflow-configuration

## Summary

Configure and validate msconvert as a dependency for raw vendor mass spectrometry file conversion to mzML format, accounting for platform-specific installation paths (ProteoWizard on Windows, Docker on macOS). This skill ensures the conversion pipeline is correctly initialized before processing raw data files.

## When to use

When you need to convert vendor-specific raw mass spectrometry files (.raw) to the open mzML format using imzML Writer, and msconvert is not yet installed or its location is not recognized by the system. This is a prerequisite step that must complete successfully before raw-to-mzML conversion can proceed.

## When NOT to use

- Input data is already in mzML or imzML format — skip directly to mzML-to-imzML conversion or metadata annotation.
- You are working in an environment where Docker or ProteoWizard cannot be installed (e.g., restricted compute cluster without root access) — seek alternative conversion tools or pre-converted data.
- msconvert is already installed, discoverable in PATH, and has been confirmed working — this skill is redundant; proceed to raw-to-mzML conversion.

## Inputs

- ProteoWizard installer (Windows) or Docker Desktop (macOS)
- System PATH environment variable (Windows) or Docker daemon (macOS)
- imzML Writer GUI or Python environment

## Outputs

- Validated msconvert installation path registered in imzML Writer configuration
- Docker image (chambm/pwiz-skyline-i-agree-to-the-vendor-licenses) available and runnable (macOS)
- Confirmation that raw-to-mzML conversion can proceed

## How to apply

On Windows, download and install ProteoWizard from https://proteowizard.sourceforge.io/download.html, then either add msconvert to the system PATH or manually provide its installation directory path when imzML Writer first prompts for it. On macOS, install Docker Desktop (https://www.docker.com/products/docker-desktop/), then either pre-pull the msconvert Docker image using `docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses` or allow imzML Writer to download it automatically on first use. Verify the configuration by launching the imzML Writer GUI and confirming that the system can locate msconvert (or confirm Docker is running and the image is accessible). The configuration is complete when msconvert is callable without manual path entry or when Docker successfully runs the pwiz-skyline image.

## Related tools

- **msconvert** (Command-line tool that performs the actual binary-to-text conversion of vendor raw files to mzML format; invoked by imzML Writer internally) — https://proteowizard.sourceforge.io/download.html
- **ProteoWizard** (Windows software suite providing msconvert executable; downloaded and installed as a prerequisite on PC platforms) — https://proteowizard.sourceforge.io/download.html
- **Docker** (Containerization platform that runs msconvert via the pwiz-skyline image on macOS; must be installed and running for macOS users) — https://www.docker.com/products/docker-desktop/
- **imzML Writer** (Python package that orchestrates msconvert configuration, prompts for paths or Docker setup, and invokes msconvert via iw_utils.RAW_to_mzML() when configured) — https://github.com/VIU-Metabolomics/imzML_Writer

## Examples

```
docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses && docker run --rm chambm/pwiz-skyline-i-agree-to-the-vendor-licenses msconvert --version
```

## Evaluation signals

- On Windows: `where msconvert` or `Get-Command msconvert` returns a valid file path without error; imzML Writer no longer prompts for msconvert path on startup.
- On macOS: `docker image ls | grep pwiz-skyline` confirms the image is present; `docker run --rm chambm/pwiz-skyline-i-agree-to-the-vendor-licenses msconvert --version` returns version information without timeout or permission error.
- imzML Writer GUI launches without configuration dialogs or errors related to missing msconvert dependency.
- Calling `iw_utils.RAW_to_mzML(raw_data_path)` on a test .raw file completes without FileNotFoundError or executable-not-found exceptions.
- Generated mzML output file(s) contain valid XML structure and expected mass spectra data (verify with XML parser or mzML validator).

## Limitations

- Windows users must manually install ProteoWizard; the installer is not bundled with imzML Writer and requires administrative privileges.
- macOS users must have Docker Desktop running; if Docker daemon is stopped, msconvert invocation will fail silently or timeout.
- Docker image pull on first use may take several minutes depending on network speed; pre-pulling the image is recommended for reproducibility and to avoid delays.
- msconvert invocation defaults to peakPicking settings; non-default centroid/profile modes or vendor-specific parameters cannot be configured at the workflow-configuration stage and must be set during actual raw-to-mzML conversion.
- Configuration is host-specific; moving imzML Writer to a different system or Docker container may require reconfiguration or re-pulling of the Docker image.

## Evidence

- [readme] On PC, this can be installed normally from Proteowizard: https://proteowizard.sourceforge.io/download.html: "On PC, this can be installed normally from Proteowizard: https://proteowizard.sourceforge.io/download.html"
- [readme] imzML Writer will prompt you for the path to msconvert the first time you try to convert raw files (see Docs), or you can add msconvert to the system path if you'd like to run msconvert from the command line.: "imzML Writer will prompt you for the path to msconvert the first time you try to convert raw files (see Docs), or you can add msconvert to the system path"
- [readme] On Mac, you can still run msconvert via a docker image. First, install Docker: https://www.docker.com/products/docker-desktop/: "On Mac, you can still run msconvert via a docker image. First, install Docker: https://www.docker.com/products/docker-desktop/"
- [readme] Similarly, imzML Writer will prompt you to download the docker image the first time you try to call it. If you'd like to do this in advance you can open Terminal.app and run the command: docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses: "imzML Writer will prompt you to download the docker image the first time you try to call it. If you'd like to do this in advance you can open Terminal.app and run the command: docker pull"
- [methods] On Mac, confirm Docker is running and the pwiz-skyline Docker image is downloaded (pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses if needed).: "On Mac, confirm Docker is running and the pwiz-skyline Docker image is downloaded (pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses if needed)"
- [intro] Using imzML Writer depends on msconvert for conversion of raw vendor files to the open format mzML.: "Using imzML Writer depends on msconvert for conversion of raw vendor files to the open format mzML"
