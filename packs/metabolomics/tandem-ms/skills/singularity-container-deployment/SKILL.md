---
name: singularity-container-deployment
description: Use when you have a Nextflow workflow (e.g., Nextflow4MS-DIAL) that currently runs under Docker or bare metal, and you need to execute it on an HPC cluster that lacks Docker support or enforces Singularity as the container runtime.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Singularity
  - Nextflow
  - MS-DIAL
  - MSFLO
  - Slurm
  techniques:
  - LC-MS
  - CE-MS
  - tandem-MS
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans:
- Both Docker and Singularity (for high-performance computing) are supported
- Both Docker and Singularity (for high-performance computing) are supported.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# singularity-container-deployment

## Summary

Deploy a Nextflow bioinformatics workflow under Singularity containerization for execution on high-performance computing (HPC) environments. This skill enables portable, reproducible LC-HRMS metabolomics data processing across HPC schedulers (e.g., Slurm) by configuring Singularity profiles, building or pulling container images, and validating end-to-end pipeline execution on HPC resource constraints.

## When to use

You have a Nextflow workflow (e.g., Nextflow4MS-DIAL) that currently runs under Docker or bare metal, and you need to execute it on an HPC cluster that lacks Docker support or enforces Singularity as the container runtime. Singularity is the right choice when your HPC environment already has Singularity installed, you need to respect Slurm or other job scheduler constraints (queue, CPU, memory limits), and you want to avoid rewriting the workflow logic.

## When NOT to use

- Your HPC environment uses Docker natively or does not have Singularity installed — use Docker profiles instead.
- You are running the workflow on a local laptop or desktop with Docker already available — Docker is simpler and faster to iterate on.
- Your input data is already processed or in a pre-computed feature table format — this skill is for raw .mzML or .abf file ingestion and peak detection.

## Inputs

- Nextflow workflow repository (e.g., github:Nextflow4Metabolomics__nextflow4ms-dial)
- Nextflow configuration files (nextflow.config, conf/base.config, HPC-specific configs)
- Docker container images or Docker Hub references for workflow tools (MS-DIAL, MSFLO)
- LC-MS metabolomics data in .mzML or .abf format
- MS-DIAL parameter configuration file (msdial_params.txt)
- MS-FLO parameter configuration file (msflo_params.ini)
- Reference MS1 and MS2 spectral libraries (ms1_lib.txt, ms2_lib.msp)

## Outputs

- Singularity profile configuration (nextflow.config with singularity.enabled=true and HPC directives)
- Singularity container images (built locally or pulled from registry)
- Processed metabolomics data files (.tsv output from MS-DIAL, .msdial results)
- Execution report (execution_report.html, execution_timeline.html)
- Execution log with container metadata and resource usage (logs/execution.log)

## How to apply

First, review the Nextflow configuration files and identify Docker runtime declarations; then create or modify a Singularity profile in `nextflow.config` with directives `singularity.enabled = true` and `process.container = 'singularity://...'` alongside HPC resource allocations (queue, cpus, memory). Build or pull the required Singularity container images (e.g., for MS-DIAL and MSFLO) from a registry or convert existing Docker images using Singularity tools. Execute a test run on sample LC-MS metabolomics data (.mzML format) using `nextflow run main.nf -profile singularity`. Validate that the container initializes correctly, processes complete without resource violations (monitor for Slurm CPU/memory overages), and output files (.msdial → .tsv) are produced as expected. Document the Singularity profile configuration, resource allocation parameters, and execution validation results in a log and report.

## Related tools

- **Nextflow** (Workflow orchestration engine; defines pipeline stages, resource allocation, and container runtime selection via profiles) — https://www.nextflow.io/
- **Singularity** (Container runtime for HPC; executes containerized workflow processes with Slurm scheduler integration and elevated privileges avoided) — https://www.sylabs.io/guides/3.0/user-guide/
- **MS-DIAL** (Core metabolomics data processing tool; performs peak detection and chromatogram alignment on LC-HRMS data, executed inside Singularity container)
- **MSFLO** (Post-processing tool for MS-DIAL outputs; runs downstream analysis in same containerized workflow)
- **Slurm** (Job scheduler on HPC cluster; manages CPU, memory, and queue allocation; Nextflow Singularity profile must respect Slurm constraints via max_cpus and memory directives)

## Examples

```
nextflow run main.nf -profile singularity > logs/execution.log
```

## Evaluation signals

- Singularity profile is present in nextflow.config with `singularity.enabled = true` and `process.container` directives pointing to valid Singularity images.
- Container images successfully build or pull without errors; verify with `singularity inspect <image.sif>`.
- Pipeline executes without Slurm resource errors (no 'Process requirement exceed available CPUs' messages); check logs/execution.log and execution_report.html for resource usage within allocated bounds.
- Output .msdial files are generated and converted to .tsv format in results/ folder; file sizes and row/column counts match expected metabolomics feature table structure.
- Execution timeline and process logs confirm all stages (peak detection, alignment, identification) completed successfully; execution_timeline.html shows no failed processes.

## Limitations

- Singularity container images must be pre-built or available in a registry accessible from the HPC cluster; building large images on login nodes may be prohibitively slow.
- HPC environments vary in Singularity version, module availability, and Slurm configuration; the provided HiPerGator.config example may require adaptation (e.g., different queue names, module load statements).
- Special characters in raw data file names cause pipeline failures; only underscores are safe in file naming conventions.
- The workflow requires sufficient disk space for intermediate files (.mzML→.msdial outputs can be large); quota limits on /scratch or /home may cause silent failures.
- Singularity bind mounts must be configured to allow access to data directories; misconfigured paths result in 'file not found' errors even if files exist on the host.

## Evidence

- [readme] Both Docker and Singularity (for high-performance computing) are supported: "Both Docker and Singularity (for high-performance computing) are supported"
- [other] Create a Singularity profile in the nextflow.config that specifies the container directive with Singularity syntax: "Create a Singularity profile in the nextflow.config that specifies the container directive with Singularity syntax (e.g., singularity.enabled = true, process.container = 'singularity://...')"
- [other] Build or pull the required Singularity container image(s) for MS-DIAL and MSFLO: "Build or pull the required Singularity container image(s) for MS-DIAL and MSFLO from the project's container registry, or convert existing Docker images using Singularity tools."
- [other] Execute a test run of the Nextflow4MS-DIAL pipeline on sample .mzML LC-MS metabolomics data using the Singularity profile via nextflow run with -profile singularity flag.: "Execute a test run of the Nextflow4MS-DIAL pipeline on sample .mzML LC-MS metabolomics data using the Singularity profile via nextflow run with -profile singularity flag."
- [other] HPC resource directives (queue, cpus, memory): "HPC resource directives (queue, cpus, memory)"
- [readme] To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] High-performance computing and Singularity configuration is defined in conf/HiPerGator.config.: "High-performance computing and Singularity configuration is defined in conf/HiPerGator.config."
- [readme] It supports macOS and Linux and has been tested successfully on: ... HiPerGator, the University of Florida public research computing environment, running Red Hat Enterprise Linux 8.8.: "It supports macOS and Linux and has been tested successfully on: ... HiPerGator, the University of Florida public research computing environment, running Red Hat Enterprise Linux 8.8."
