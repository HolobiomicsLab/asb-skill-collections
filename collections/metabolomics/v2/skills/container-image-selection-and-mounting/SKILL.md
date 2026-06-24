---
name: container-image-selection-and-mounting
description: Use when when deploying a Nextflow workflow across multiple execution
  environments (local machines, HPC clusters) where tool versions, dependencies, or
  OS configurations may differ. Choose this skill specifically when you need to process
  LC-HRMS .mzML or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3233
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MSFLO
  - Nextflow
  - Docker
  - Singularity
  - MS-DIAL
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans:
- containerized workflow MS-DIAL -> MSFLO
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nextflow4msdial
    doi: 10.1021/jasms.4c00364
    title: nextflow4msdial
  dedup_kept_from: coll_nextflow4msdial
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00364
  all_source_dois:
  - 10.1021/jasms.4c00364
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# container-image-selection-and-mounting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Select and configure containerized runtime environments (Docker or Singularity) for reproducible execution of bioinformatics workflows across heterogeneous compute platforms. This skill ensures portability and consistent tool behavior in LC-HRMS metabolomics data processing pipelines.

## When to use

When deploying a Nextflow workflow across multiple execution environments (local machines, HPC clusters) where tool versions, dependencies, or OS configurations may differ. Choose this skill specifically when you need to process LC-HRMS .mzML or .abf files through containerized MS-DIAL and MSFLO without manual tool installation, and when reproducibility across macOS, Linux, or HPC systems is a requirement.

## When NOT to use

- Data is already processed into feature tables or annotation matrices — container selection is for raw .mzML/.abf ingestion only.
- Your HPC system does not support Docker or Singularity and requires native tool installation.
- You are running on Windows without WSL2 + Docker Desktop, as the workflow README documents support only for macOS and Linux.

## Inputs

- .mzML LC-MS raw data files
- .abf LC-MS raw data files
- MS-DIAL configuration file (msdial_params.txt)
- MS-FLO configuration file (msflo_params.ini)
- MS1 reference library (.txt)
- MS2 reference library (.msp)

## Outputs

- MS-DIAL feature detection output
- MS-DIAL feature identification output
- MSFLO processed feature tables (.tsv)
- MSFLO annotations
- MSFLO metadata

## How to apply

First, determine your execution environment: local development uses Docker; high-performance computing clusters typically require Singularity. Install the chosen container runtime (Docker via Docker Desktop or Singularity via system package manager). In the Nextflow workflow configuration, select the corresponding profile (`-profile docker` or `-profile singularity`). Verify that containerized MS-DIAL and MSFLO images are available and compatible with your data format (.mzML or .abf). Mount input data directories (raw_data/) and configuration files (msdial_params.txt, msflo_params.ini, MS1/MS2 libraries) into the container at pipeline initialization. The Nextflow runtime automatically stages inputs into the container work directory, executes processes sequentially within the container, and collects outputs from the container's results directory back to the host filesystem.

## Related tools

- **Nextflow** (Orchestrates workflow execution and manages container runtime selection and process staging) — https://www.nextflow.io/
- **Docker** (Local container runtime for reproducible execution on macOS and Linux development machines) — https://docs.docker.com/engine/installation/
- **Singularity** (HPC container runtime for secure, user-namespace-independent execution on shared clusters) — https://www.sylabs.io/guides/3.0/user-guide/
- **MS-DIAL** (Containerized peak detection and feature identification tool executed within selected runtime) — https://github.com/Nextflow4Metabolomics/nextflow4ms-dial
- **MSFLO** (Containerized feature alignment and annotation tool chained after MS-DIAL within pipeline) — https://github.com/Nextflow4Metabolomics/nextflow4ms-dial

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log
```

## Evaluation signals

- Verify container image was successfully pulled and cached locally (check Docker images or Singularity cache directory).
- Confirm input files were mounted and accessible within the container by inspecting Nextflow work directory logs (`.command.log` in process-specific work folders).
- Check that MS-DIAL and MSFLO executed within the container (logs should show container runtime in process metadata).
- Validate that output files (feature tables, .tsv annotations) were collected from container to host results/ directory with correct schema and non-empty content.
- Run `nextflow run main.nf -profile functional_test` and confirm execution completes without container I/O or mount errors.

## Limitations

- MS-DIAL and MSFLO tool versions are fixed at container build time; version updates require rebuilding or pulling new container images.
- High-memory datasets may exhaust container memory limits if not explicitly configured in `conf/base.config` or HPC submission parameters.
- Special characters in input filenames cause unexpected errors and pipeline failures; only underscores are safe in file naming.
- Singularity on HPC systems may require cluster-specific configuration beyond `conf/HiPerGator.config` if using different resource managers (e.g., Slurm, TORQUE).
- Configuration file paths (msdial_params.txt, msflo_params.ini) must match exactly; no automatic path discovery is performed.

## Evidence

- [readme] The workflow includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce.: "The workflow includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce."
- [readme] It supports macOS and Linux and has been tested successfully on macOS 13.5.1 and HiPerGator (Red Hat Enterprise Linux 8.8).: "It supports macOS and Linux and has been tested successfully on: macOS 13.5.1 with a 2.6 GHz 6-Core Intel Core i7 processor and 16 GB memory. HiPerGator, the University of Florida public research"
- [other] Initialize Nextflow with containerization backend selection (Docker or Singularity) and stage .mzML files into work directory.: "Initialize Nextflow ≥22.10.0 runtime environment with containerization backend selection (Docker or Singularity). Stage .mzML input files into Nextflow work directory and validate file format"
- [readme] High-performance computing and Singularity configuration is defined in conf/HiPerGator.config; use docker profile for local execution.: "Docker configuration is defined in conf/base.config. High-performance computing and Singularity configuration is defined in conf/HiPerGator.config. Use the docker profile for local execution and the"
- [readme] Do not use special characters in file names to avoid unexpected errors; only underscores are safe to use.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
