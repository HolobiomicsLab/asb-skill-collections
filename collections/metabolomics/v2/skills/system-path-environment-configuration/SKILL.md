---
name: system-path-environment-configuration
description: 'Use when when setting up imzML Writer for the first time on a new machine, or when raw vendor mass spectrometry file conversion fails with ''msconvert not found'' or Docker image unavailable errors. Specifically: on Windows/PC systems before invoking RAW_to_mzML conversion;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - ProteoWizard
  - Python
  - msconvert
  - Docker
  - chambm/pwiz-skyline-i-agree-to-the-vendor-licenses
  - imzML Writer
derived_from:
- doi: 10.1021/acs.analchem.4c06520
  title: imzML Writer
evidence_spans:
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# system-path-environment-configuration

## Summary

Configure system PATH environment variables and platform-specific dependencies (msconvert on Windows via ProteoWizard, Docker image on macOS) to enable imzML Writer's raw-to-mzML conversion pipeline. This skill ensures that external command-line tools and containerized services are discoverable and executable by the Python application at runtime.

## When to use

When setting up imzML Writer for the first time on a new machine, or when raw vendor mass spectrometry file conversion fails with 'msconvert not found' or Docker image unavailable errors. Specifically: on Windows/PC systems before invoking RAW_to_mzML conversion; on macOS before first Docker-based msconvert call; when users report conversion failures due to missing tool paths.

## When NOT to use

- Input data is already in mzML or imzML format (skip to mzML_to_imzML_convert or metadata annotation steps instead)
- User is running imzML Writer in a pre-configured Docker container where msconvert and dependencies are already embedded
- System lacks write permissions to install ProteoWizard or Docker (administrative access is required)

## Inputs

- System environment (PATH, Docker daemon state)
- ProteoWizard installation directory (PC only)
- Docker Desktop installation and configuration (macOS only)

## Outputs

- Valid system PATH entry pointing to msconvert executable (PC)
- Docker daemon running with pwiz-skyline image available (macOS)
- Confirmation that iw_utils.RAW_to_mzML() can locate and invoke msconvert

## How to apply

On PC: download and install ProteoWizard from https://proteowizard.sourceforge.io/download.html, which bundles msconvert; either add the msconvert installation directory to the system PATH environment variable, or allow imzML Writer to prompt for the msconvert path on first use and store it internally. On Mac: install Docker Desktop from https://www.docker.com/products/docker-desktop/, ensure the Docker GUI is running, and pre-pull the Docker image (docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses) or let imzML Writer download it on first conversion attempt. Verify accessibility by testing msconvert --version on PC or confirming Docker image presence via 'docker images' on Mac before running RAW_to_mzML conversion.

## Related tools

- **msconvert** (Command-line tool invoked by imzML Writer to convert raw vendor mass spectrometry files to mzML format; must be locatable via system PATH or Docker) — https://proteowizard.sourceforge.io/download.html
- **ProteoWizard** (Installer bundle for msconvert on Windows/PC; provides the msconvert executable and supporting libraries) — https://proteowizard.sourceforge.io/download.html
- **Docker** (Container runtime on macOS; downloads and executes the chambm/pwiz-skyline image to run msconvert without native ProteoWizard installation) — https://www.docker.com/products/docker-desktop/
- **chambm/pwiz-skyline-i-agree-to-the-vendor-licenses** (Docker image containing msconvert and vendor library dependencies for macOS; pulled on demand or pre-cached) — https://hub.docker.com/r/chambm/pwiz-skyline-i-agree-to-the-vendor-licenses
- **imzML Writer** (Python application that depends on this configuration; prompts for msconvert path on first use if not found in PATH) — https://github.com/VIU-Metabolomics/imzML_Writer

## Examples

```
# PC: add msconvert to PATH, then verify
echo %PATH% | find "msconvert"
# macOS: pre-pull Docker image
docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses
# Then launch imzML Writer; it will auto-detect dependencies
import imzml_writer.imzML_Writer as iw; iw.gui()
```

## Evaluation signals

- On PC: `msconvert --version` returns version info and help text (not 'command not found')
- On macOS: `docker images` lists 'chambm/pwiz-skyline-i-agree-to-the-vendor-licenses' with a recent pull timestamp
- imzML Writer GUI launches without environment-related errors and does not prompt for msconvert path on subsequent uses
- Calling iw_utils.RAW_to_mzML(raw_data_path) completes without 'msconvert executable not found' or Docker connection errors
- Generated mzML output file(s) contain valid XML structure and match expected byte size for the input .raw file

## Limitations

- On PC, ProteoWizard installation requires administrative privileges and may not be available in all institutional environments (air-gapped networks, locked-down corporate systems)
- On macOS, Docker Desktop requires system resources (memory, disk); pulling the pwiz-skyline image is ~2–3 GB and requires internet access; first-time pull may take several minutes
- macOS users must have Docker daemon running before attempting conversion; if Docker is stopped, imzML Writer will hang or fail silently
- PATH configuration is shell-specific (bash, zsh, etc.) and may not persist across terminal sessions if not added to .bashrc/.zshrc
- Vendor library licenses bundled in the Docker image require acceptance; users may be prompted or required to acknowledge licensing terms on first pull

## Evidence

- [readme] On PC, this can be installed normally from Proteowizard: https://proteowizard.sourceforge.io/download.html: "On PC, this can be installed normally from Proteowizard: https://proteowizard.sourceforge.io/download.html"
- [readme] On Mac, you can still run msconvert via a docker image. First, install Docker: https://www.docker.com/products/docker-desktop/: "On Mac, you can still run msconvert via a docker image. First, install Docker: https://www.docker.com/products/docker-desktop/"
- [readme] imzML Writer will prompt you for the path to msconvert the first time you try to convert raw files (see Docs), or you can add msconvert to the system path: "imzML Writer will prompt you for the path to msconvert the first time you try to convert raw files (see Docs), or you can add msconvert to the system path"
- [methods] it will prompt you to download the docker image for msconvert from hub.docker.com/r/chambm/pwiz-skyline-i-agree-to-the-vendor-licenses: "it will prompt you to download the docker image for msconvert from hub.docker.com/r/chambm/pwiz-skyline-i-agree-to-the-vendor-licenses"
- [other] on Mac, msconvert runs via a Docker image (chambm/pwiz-skyline-i-agree-to-the-vendor-licenses) that is downloaded on demand: "on Mac, msconvert runs via a Docker image (chambm/pwiz-skyline-i-agree-to-the-vendor-licenses) that is downloaded on demand"
- [other] on PC, confirm msconvert is in the system PATH or locate its install directory; on Mac, confirm Docker is running and the pwiz-skyline Docker image is downloaded: "on PC, confirm msconvert is in the system PATH or locate its install directory; on Mac, confirm Docker is running and the pwiz-skyline Docker image is downloaded"
