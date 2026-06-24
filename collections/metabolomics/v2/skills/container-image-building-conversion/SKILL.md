---
name: container-image-building-conversion
description: Use when your Nextflow metabolomics workflow has been validated with
  Docker locally, but you need to deploy it on an HPC cluster that mandates Singularity
  containerization (e.g., Red Hat Enterprise Linux 8.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Singularity
  - Docker
  - Nextflow
  - MS-DIAL
  - MSFLO
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nextflow4msdial_cq
    doi: 10.1021/jasms.4c00364
    title: nextflow4msdial
  dedup_kept_from: coll_nextflow4msdial_cq
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

# Container Image Building and Conversion

## Summary

Build or convert container images (Docker↔Singularity) to enable pipeline portability across execution environments—from local Docker-capable workstations to high-performance computing clusters that require Singularity for resource isolation and compliance.

## When to use

Your Nextflow metabolomics workflow has been validated with Docker locally, but you need to deploy it on an HPC cluster that mandates Singularity containerization (e.g., Red Hat Enterprise Linux 8.x), or you want to avoid repeated image pulls by pre-building Singularity images from existing Docker definitions in the project's container registry.

## When NOT to use

- Workflow is being executed only on a local macOS or Linux workstation where Docker is already available and HPC deployment is not planned.
- HPC environment does not support Singularity and has no container runtime installed (use native or module-based installations instead).
- Input images are proprietary and cannot be redistributed or converted; check license restrictions before pulling or converting.

## Inputs

- Docker image URI (e.g., quay.io/ms-dial:latest)
- Existing Docker images in project registry
- Singularity definition file (.def) or recipe
- Nextflow configuration file (nextflow.config)
- Sample .mzML or .abf LC-MS data files for validation

## Outputs

- Singularity image file (.sif)
- Container execution logs and validation report
- Updated or new Singularity profile in nextflow.config
- Processed metabolomics output (.tsv, .msdial files)

## How to apply

Identify the Docker image definitions or references in the Nextflow workflow configuration (e.g., process.container directives in nextflow.config). For each image, either pull the pre-built Singularity image from a registry or convert an existing Docker image using Singularity tools (e.g., singularity pull docker://image_uri or singularity build output.sif Singularity.def). Validate container initialization by checking that all MS-DIAL, MSFLO, and dependency binaries are present and executable inside the image. Stage the Singularity image files (.sif) on the HPC system in a shared location accessible to the Nextflow execution profile. Test the Singularity profile configuration (singularity.enabled = true, process.container = 'singularity://path/to/image.sif') with a sample .mzML dataset to confirm process execution, correct resource allocation (queue, cpus, memory), and successful metabolomics data processing completion.

## Related tools

- **Singularity** (Container runtime for HPC environments; builds and executes .sif images converted from or equivalent to Docker definitions) — https://www.sylabs.io/guides/3.0/user-guide/
- **Docker** (Source container platform; Docker images are pulled or converted to Singularity format for HPC portability) — https://docs.docker.com/engine/installation/
- **Nextflow** (Workflow orchestrator; reads container directives from nextflow.config and executes processes within Singularity runtime when profile is activated) — https://www.nextflow.io/
- **MS-DIAL** (Containerized metabolomics analysis tool for peak detection and feature quantification; image must be built/converted and available to Singularity runtime)
- **MSFLO** (Containerized post-processing tool for MS-DIAL output; image must be built/converted and available to Singularity runtime)

## Examples

```
singularity build ms-dial.sif docker://ms-dial:latest; nextflow run main.nf -profile singularity -resume
```

## Evaluation signals

- Singularity image file (.sif) is created, present on HPC filesystem, and readable by the Nextflow execution user.
- Container initialization completes without errors; MS-DIAL and MSFLO executables and libraries are present inside the image (verified via `singularity exec image.sif which msdial` or equivalent).
- Nextflow execution log shows successful container binding, correct process invocation (e.g., 'Executing process > process_name [XX%]'), and no container-related timeouts or permission errors.
- Processing pipeline produces expected output files (.tsv, .msdial) with data schemas and row/column counts consistent with prior Docker execution on identical input.
- HPC resource allocation (queue, cpus, memory) is respected; no SLURM/scheduler errors such as 'Process requirement exceed available CPUs'.

## Limitations

- Singularity image conversion from Docker may fail if the Docker image contains features unsupported by Singularity (e.g., certain mount types, user namespaces); manual recipe rewriting may be required.
- HPC environments may not allow privileged image building; use `singularity pull` to fetch pre-built images or request administrative assistance for `singularity build`.
- File name handling: do not use special characters in input data file names (e.g., spaces, hyphens in intermediate filenames); underscores are safe. Special characters may cause Singularity binding or process execution failures.
- Performance may differ between Docker and Singularity due to I/O overhead and network filesystem latency on HPC; benchmark on representative datasets before committing to production.

## Evidence

- [readme] Docker and Singularity support for HPC: "Both Docker and Singularity (for high-performance computing) are supported"
- [other] Singularity profile configuration and container image requirements: "Create a Singularity profile in the nextflow.config that specifies the container directive with Singularity syntax (e.g., singularity.enabled = true, process.container = 'singularity://...')"
- [other] Docker-to-Singularity conversion workflow: "Build or pull the required Singularity container image(s) for MS-DIAL and MSFLO from the project's container registry, or convert existing Docker images using Singularity tools"
- [other] Validation of container execution with metabolomics data: "Execute a test run of the Nextflow4MS-DIAL pipeline on sample .mzML LC-MS metabolomics data using the Singularity profile via nextflow run with -profile singularity flag"
- [readme] HPC deployment context for Singularity: "It supports macOS and Linux and has been tested successfully on: HiPerGator, the University of Florida public research computing environment, running Red Hat Enterprise Linux 8.8"
- [readme] File naming constraint for container execution: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
