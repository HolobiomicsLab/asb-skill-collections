---
name: docker-container-orchestration
description: Use when your analysis requires msconvert or another ProteoWizard tool
  on macOS, but native installation is infeasible or licensing-restricted. You need
  to convert vendor raw mass spectrometry files (.raw) to the open mzML format without
  installing ProteoWizard directly on your system.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_3577
  tools:
  - ProteoWizard
  - Docker
  - Python
  - msconvert
  - imzML Writer
  - chambm/pwiz-skyline-i-agree-to-the-vendor-licenses
  - MSFLO
  - Nextflow
  - MS-DIAL
  - Singularity
  - docker
  - docker-compose
  - TensorFlow Serving
  - nginx
  - TensorFlow 2.3.0
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.4c06520
  title: imzML Writer
- doi: 10.1021/jasms.4c00364
  title: ''
- doi: 10.1021/acs.jnatprod.1c00399
  title: ''
evidence_spans:
- On PC, download the latest msconvert release from ProteoWizard
- 'On PC, this can be installed normally from Proteowizard: https://proteowizard.sourceforge.io/download.html'
- On Mac, download Docker and open up the GUI dashboard. The first time you go to
  convert raw files, it will prompt you to download the docker image for msconvert
- On Mac, you can still run msconvert via a docker image. First, install Docker
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
  - build: coll_nextflow4msdial
    doi: 10.1021/jasms.4c00364
    title: nextflow4msdial
  - build: coll_npclassifier
    doi: 10.1021/acs.jnatprod.1c00399
    title: npclassifier
  dedup_kept_from: coll_imzml_writer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06520
  all_source_dois:
  - 10.1021/acs.analchem.4c06520
  - 10.1021/jasms.4c00364
  - 10.1021/acs.jnatprod.1c00399
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# docker-container-orchestration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Run platform-dependent bioinformatics tools (like msconvert) inside containerized Docker environments to ensure reproducibility and avoid native OS dependencies. This skill is essential when the target tool has restrictive licensing or vendor-specific requirements that complicate native installation.

## When to use

Your analysis requires msconvert or another ProteoWizard tool on macOS, but native installation is infeasible or licensing-restricted. You need to convert vendor raw mass spectrometry files (.raw) to the open mzML format without installing ProteoWizard directly on your system.

## When NOT to use

- msconvert is already natively installed and working on your system (native execution is simpler and faster than containerization).
- You are working on Windows/PC where ProteoWizard can be installed directly from the ProteoWizard repository without Docker.
- Your raw files are already in open formats (mzML or imzML) and do not require conversion.

## Inputs

- Directory containing vendor .raw mass spectrometry files
- Docker installation and Docker daemon running
- Raw file path string passed to iw_utils.RAW_to_mzML()

## Outputs

- mzML format files converted from vendor raw data
- Docker container execution logs and conversion status

## How to apply

First, verify Docker is installed and running on your system. Pull the pre-built Docker image containing msconvert: `docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses`. When imzML Writer invokes raw-to-mzML conversion (via `iw_utils.RAW_to_mzML(raw_data_path)`), the framework automatically detects the Docker environment and routes the msconvert call through the containerized image instead of seeking a native binary. The container receives the raw file path, applies default peak-picking settings, and writes mzML output back to the host filesystem. Monitor conversion progress in the GUI or logs; verify the mzML file is generated with correct XML structure and file naming.

## Related tools

- **Docker** (Container runtime that downloads, manages, and executes the pwiz-skyline Docker image containing msconvert and its dependencies) — https://www.docker.com/products/docker-desktop/
- **msconvert** (ProteoWizard utility that runs inside the Docker container to convert vendor raw mass spectrometry files to mzML format with peak-picking) — https://proteowizard.sourceforge.io/download.html
- **imzML Writer** (Python framework that detects Docker availability on macOS and orchestrates Docker-containerized msconvert calls for RAW to mzML conversion) — https://github.com/VIU-Metabolomics/imzML_Writer
- **chambm/pwiz-skyline-i-agree-to-the-vendor-licenses** (Pre-built Docker image hosted on Docker Hub containing msconvert and ProteoWizard libraries with vendor license agreements pre-accepted) — https://hub.docker.com/r/chambm/pwiz-skyline-i-agree-to-the-vendor-licenses

## Examples

```
docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses; import imzml_writer.imzML_Writer as iw; iw.gui()
```

## Evaluation signals

- Docker image is successfully pulled and appears in `docker images` output with tag chambm/pwiz-skyline-i-agree-to-the-vendor-licenses.
- mzML output files are generated in the expected directory with correct naming (matching input .raw filenames with .mzML extension).
- mzML files have valid XML structure (verified by opening with XML parser or imzML-compatible software).
- Conversion completion is logged without Docker runtime errors or permission failures.
- File size of mzML output is consistent with input raw file size and expected centroid/profile mode data volume.

## Limitations

- Docker must be running and the container image must be downloaded; initial setup adds latency compared to native tool installation.
- On macOS, Docker Desktop requires additional system resources (CPU, memory, disk) to maintain a running container; some systems may experience performance degradation.
- Vendor license agreements embedded in the Docker image apply automatically; users implicitly accept them by pulling and running the image.
- File path handling between host and container must be explicitly mapped; incorrect mount paths will cause conversion to fail silently or report 'file not found' errors.
- The image is maintained by a third party (chambm); updates or deprecation are outside imzML Writer's control.

## Evidence

- [readme] On Mac, you can still run msconvert via a docker image. First, install Docker: https://www.docker.com/products/docker-desktop/: "On Mac, you can still run msconvert via a docker image. First, install Docker"
- [readme] Similarly, imzML Writer will prompt you to download the docker image the first time you try to call it. If you'd like to do this in advance you can open `Terminal.app` and run the command: docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses: "imzML Writer will prompt you to download the docker image the first time you try to call it. If you'd like to do this in advance you can open Terminal.app and run the command: docker pull"
- [methods] on Mac, msconvert runs via a Docker image (chambm/pwiz-skyline-i-agree-to-the-vendor-licenses) that is downloaded on demand: "on Mac, msconvert runs via a Docker image (chambm/pwiz-skyline-i-agree-to-the-vendor-licenses) that is downloaded on demand"
- [methods] Invoke iw_utils.RAW_to_mzML(raw_data_path) on the directory containing the .raw file, which internally calls msconvert with default peakPicking settings to convert vendor raw data to mzML format.: "Invoke iw_utils.RAW_to_mzML(raw_data_path) on the directory containing the .raw file, which internally calls msconvert with default peakPicking settings"
