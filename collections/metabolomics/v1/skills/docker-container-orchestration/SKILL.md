---
name: docker-container-orchestration
description: Use when when you have .mzML or .abf LC-HRMS raw data files that require MS-DIAL-based feature detection, chromatogram alignment, and metabolite identification, and you need to ensure reproducibility across local machines, cloud, and HPC systems without manual tool installation and dependency.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_3577
  tools:
  - Docker
  - MSFLO
  - Nextflow
  - MS-DIAL
  - Singularity
  - docker
  - docker-compose
  - TensorFlow Serving
  - nginx
  - TensorFlow 2.3.0
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
- doi: 10.1021/acs.jnatprod.1c00399
  title: ''
evidence_spans:
- Both Docker and Singularity (for high-performance computing) are supported
- containerized workflow MS-DIAL -> MSFLO
- you need docker and docker-compose
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nextflow4msdial
    doi: 10.1021/jasms.4c00364
    title: nextflow4msdial
  - build: coll_npclassifier
    doi: 10.1021/acs.jnatprod.1c00399
    title: npclassifier
  dedup_kept_from: coll_nextflow4msdial
schema_version: 0.2.0
---

# docker-container-orchestration

## Summary

Execute reproducible LC-HRMS metabolomics workflows using Docker containerization of MS-DIAL and MSFLO tools via Nextflow, enabling portable and isolated processing of .mzML mass spectrometry data across heterogeneous computational environments.

## When to use

When you have .mzML or .abf LC-HRMS raw data files that require MS-DIAL-based feature detection, chromatogram alignment, and metabolite identification, and you need to ensure reproducibility across local machines, cloud, and HPC systems without manual tool installation and dependency management.

## When NOT to use

- Input data is already processed into a feature table or peak matrix — use this skill only when starting from raw .mzML or .abf chromatography-mass spectrometry files.
- Your computing environment has strict restrictions on Docker daemon access or does not support container runtimes (in such cases, use the Singularity profile instead).
- You require real-time interactive parameter tuning during processing; Docker containerization assumes pre-configured static parameters in configuration files.

## Inputs

- .mzML files (Liquid Chromatography-High Resolution Mass Spectrometry raw data)
- .abf files (alternative LC-HRMS format)
- MS-DIAL parameter configuration file (msdial_params.txt)
- MS-FLO parameter configuration file (msflo_params.ini)
- MS1 spectral library (ms1_lib.txt)
- MS2 spectral library (ms2_lib.msp)

## Outputs

- Feature detection tables (.tsv files converted from .msdial)
- Aligned data matrices (MS-DIAL aligned features)
- Processed metabolite annotations (MS-FLO results)
- Execution report (execution_report.html)
- Execution timeline (execution_timeline.html)
- Workflow logs (logs/execution.log)

## How to apply

Install Nextflow ≥22.10.0 and Docker, then clone the Nextflow4MS-DIAL repository. Prepare your .mzML metabolomics dataset and place it in the `data/raw_data/` directory. Configure MS-DIAL parameters in `msdial_params.txt` and MS-FLO parameters in `msflo_params.ini` (example files are provided in `functional_test/sample_data/`), and add MS1 and MS2 spectral libraries as `ms1_lib.txt` and `ms2_lib.msp`. Execute the workflow with the Docker profile: `nextflow run main.nf -profile docker`. The containerized MS-DIAL and MSFLO tools run inside isolated Docker images, eliminating version conflicts and platform-specific issues. Monitor execution via `execution_report.html` (runtime and resource usage) and `execution_timeline.html` (process timeline) to verify all pipeline stages complete without error.

## Related tools

- **Nextflow** (Workflow orchestration engine that manages containerized tool execution, resource allocation, and job scheduling across local and distributed computational environments.) — https://www.nextflow.io/
- **MS-DIAL** (Containerized bioinformatics tool for untargeted LC-HRMS metabolomics data processing, including peak detection, deconvolution, and feature alignment.)
- **MSFLO** (Containerized post-processing tool for MS-DIAL output that performs metabolite annotation and library matching.)
- **Docker** (Container runtime that packages MS-DIAL and MSFLO tools with all dependencies into isolated, reproducible execution environments.) — https://docs.docker.com/engine/installation/
- **Singularity** (Alternative container runtime supported by the workflow for high-performance computing environments where Docker is unavailable.) — https://www.sylabs.io/guides/3.0/user-guide/

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log
```

## Evaluation signals

- All workflow stages complete without errors in logs/execution.log; no process reports failure status.
- Expected output files are present and non-empty in the results directory: feature detection tables (converted .tsv files from .msdial), aligned data matrices, and metabolite annotations.
- Execution report (execution_report.html) displays successful completion status, total runtime, and per-process resource utilization within expected ranges.
- Workflow produces consistent feature tables and aligned data across repeated runs with identical input parameters (reproducibility validation).
- Container images for MS-DIAL and MSFLO are successfully pulled and executed without registry or Docker daemon errors (verify in execution logs).

## Limitations

- File names must not contain special characters; only underscores are safe (spaces, dashes, and other symbols cause unexpected errors).
- Input .mzML and .abf files must be converted from other raw mass spectrometry formats using external tools (ProteoWizard msConvert or Reifycs Abf Converter); the workflow does not perform format conversion.
- MS-DIAL and MSFLO tool versions are not explicitly specified in the workflow configuration; no version pinning or compatibility information is provided, which may affect reproducibility across software updates.
- The workflow has been validated only on macOS 13.5.1 (2.6 GHz 6-Core Intel Core i7, 16 GB memory) and Red Hat Enterprise Linux 8.8 (HiPerGator HPC); behavior on other operating systems or resource-constrained environments is untested.
- No explicit discussion of Docker image pull failures, network connectivity issues, or disk space requirements for containerized execution is provided.

## Evidence

- [readme] A reproducible Nextflow workflow for LC-HRMS metabolomics data processing: "A reproducible Nextflow workflow for LC-HRMS metabolomics data processing with MS-DIAL."
- [readme] Containerized MS-DIAL and MSFLO workflow with Docker support: "processing .mzML LC-MS metabolomics data with containerized workflow MS-DIAL -> MSFLO"
- [readme] Docker and Singularity container support: "Both Docker and Singularity (for high-performance computing) are supported"
- [readme] Nextflow version requirement and Java dependency: "Install Java 11 or later. The workflow was developed with Java 11.0.8. Install [Nextflow](https://nf-co.re/usage/installation)."
- [readme] Configuration and library file setup: "Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`. Example configuration files are available in"
- [readme] Execution command with Docker profile: "nextflow run main.nf -profile docker > logs/execution.log"
- [readme] Execution monitoring via report files: "`execution_report.html` summarizes workflow runtime and computational resource usage. `execution_timeline.html` shows the execution timeline for each process."
- [readme] File naming restrictions for workflow execution: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] Platform and hardware testing scope: "It supports macOS and Linux and has been tested successfully on: macOS 13.5.1 with a 2.6 GHz 6-Core Intel Core i7 processor and 16 GB memory. HiPerGator, the University of Florida public research"
- [readme] Input data format requirements: "The workflow accepts `.mzML` and `.abf` files."
