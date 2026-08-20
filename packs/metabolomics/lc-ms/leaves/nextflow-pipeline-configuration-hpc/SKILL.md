---
name: nextflow-pipeline-configuration-hpc
description: Use when your analysis target is an HPC environment (e.g., Slurm-managed cluster, university research computing center) where Singularity is available but Docker is restricted or unavailable; your workflow is already packaged in Docker but needs portability to HPC;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3520
  tools:
  - Nextflow
  - Singularity
  - MS-DIAL
  - MSFLO
  - Nextflow4MS-DIAL
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans:
- '[![Nextflow](https://img.shields.io/badge/nextflow-%E2%89%A522.10.0-brightgreen.svg)](https://www.nextflow.io/)'
- nextflow4ms-dial
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

# Configure Nextflow pipeline for high-performance computing with Singularity containerization

## Summary

This skill enables deployment of Nextflow bioinformatics workflows on HPC systems by configuring Singularity container runtime and resource directives (queue, CPU, memory) in place of Docker. It is essential when executing metabolomics or other data-intensive pipelines on institutional computing clusters where Singularity is the standard container runtime.

## When to use

Your analysis target is an HPC environment (e.g., Slurm-managed cluster, university research computing center) where Singularity is available but Docker is restricted or unavailable; your workflow is already packaged in Docker but needs portability to HPC; you need reproducible, containerized execution across local, Docker, and HPC backends with a single codebase.

## When NOT to use

- Your HPC system uses Docker natively; Singularity is not installed or unavailable.
- The workflow is not containerized; Docker images are not available or maintainable.
- Your analysis runs on local machines or cloud platforms with native Docker support; HPC deployment is not required.
- Workflow execution requires GPUs or specialized hardware not described in the Nextflow config; custom resource directives beyond standard queue/cpus/memory are needed.

## Inputs

- Nextflow workflow script (main.nf or equivalent)
- Nextflow configuration files with Docker declarations (conf/*.config)
- Docker container image registry (project-specific or public)
- HPC system credentials and queue information (job scheduler type, resource limits)
- Sample input data in workflow-native format (e.g., .mzML LC-MS files for metabolomics)
- Workflow-specific parameter files (e.g., msdial_params.txt, msflo_params.ini for MS-DIAL pipelines)

## Outputs

- HPC-compatible Nextflow configuration profile (singularity profile in nextflow.config)
- Singularity container image(s) (converted or pulled from registry)
- Execution report with HPC resource usage (execution_report.html)
- Process timeline log (execution_timeline.html)
- Standard output and error logs (execution.log, error.txt)
- Pipeline output artifacts in expected format (e.g., .tsv feature tables for metabolomics)

## How to apply

Review the Nextflow configuration files (typically conf/base.config and HPC-specific configs) to identify Docker runtime declarations. Create or update a Singularity profile in nextflow.config by setting singularity.enabled = true and specifying container directives with Singularity syntax (e.g., process.container = 'singularity://...'). Define HPC resource allocations (queue name, cpus, memory) in the same profile; use --max_cpus to set per-process CPU limits, not --cpus. Build or pull Singularity container images corresponding to each Docker image in the workflow (e.g., MS-DIAL, MSFLO for metabolomics pipelines). Execute a test run on sample data using the -profile singularity flag and validate that container initialization completes, processes log without errors, and output files are generated with expected content (e.g., .tsv metabolite tables from .mzML input).

## Related tools

- **Nextflow** (Workflow orchestration and execution engine; interprets Singularity profile and manages process submission to HPC scheduler) — https://www.nextflow.io/
- **Singularity** (Container runtime for HPC systems; loads and executes containerized processes in isolation with host filesystem access) — https://www.sylabs.io/guides/3.0/user-guide/
- **MS-DIAL** (Metabolomics peak detection and alignment tool; containerized process in the workflow for .mzML LC-MS data processing)
- **MSFLO** (Metabolite identification and quantification tool; downstream containerized process following MS-DIAL in metabolomics pipeline)
- **Nextflow4MS-DIAL** (Reference implementation of Singularity-HPC configuration for metabolomics; serves as template for HPC profile adaptation) — https://github.com/Nextflow4Metabolomics/nextflow4ms-dial

## Examples

```
nextflow run main.nf -profile singularity > logs/execution.log
```

## Evaluation signals

- Singularity profile successfully parses in nextflow.config without syntax errors; nextflow config shows singularity.enabled = true and container directives resolved.
- Test pipeline execution completes with exit code 0; execution_report.html and execution_timeline.html are generated without missing stages.
- Container initialization logs (visible in execution.log) show successful Singularity image pull/bind and process execution inside container, not on host.
- Output files match expected schema and content: for metabolomics, .tsv feature tables contain expected columns (m/z, retention time, intensity, etc.) with non-empty rows.
- HPC resource allocation is respected: execution_report.html shows CPU and memory usage align with queue limits set via --max_cpus; no Slurm errors like 'Process requirement exceed available CPUs'.

## Limitations

- Singularity container images must be pre-built or available in a registry; converting existing Docker images using Singularity tools adds a prerequisite step.
- HPC scheduler configuration is system-specific (e.g., Slurm vs. PBS); the conf/HiPerGator.config template may not transfer directly to other institutions without queue name and resource limit adjustments.
- Special characters in input file names can cause unexpected errors; file naming conventions (e.g., underscores only) must be enforced upstream.
- Per-process CPU allocation via --max_cpus must not exceed total CPUs requested from the scheduler; misconfiguration leads to Slurm queueing failures.
- The workflow depends on availability of MS1 and MS2 spectral libraries (ms1_lib.txt, ms2_lib.msp) and MS-DIAL/MSFLO parameter files; missing or misconfigured parameter files produce silent failures or invalid quantification.

## Evidence

- [readme] Both Docker and Singularity (for high-performance computing) are supported: "Both Docker and Singularity (for high-performance computing) are supported"
- [other] HPC resource directives and Singularity syntax for profile creation: "Create a Singularity profile in the nextflow.config that specifies the container directive with Singularity syntax (e.g., singularity.enabled = true, process.container = 'singularity://...') and HPC"
- [other] Container image build or pull workflow for metabolomics tools: "Build or pull the required Singularity container image(s) for MS-DIAL and MSFLO from the project's container registry, or convert existing Docker images using Singularity tools."
- [other] Test execution and validation approach for Singularity profile: "Execute a test run of the Nextflow4MS-DIAL pipeline on sample .mzML LC-MS metabolomics data using the Singularity profile via nextflow run with -profile singularity flag."
- [readme] HPC CPU allocation troubleshooting guidance: "Use `--max_cpus`, not `--cpus`, in the configuration file to define the CPUs available to each process."
- [readme] HPC testing and deployment context for Nextflow4MS-DIAL: "It supports macOS and Linux and has been tested successfully on: macOS 13.5.1 with a 2.6 GHz 6-Core Intel Core i7 processor and 16 GB memory. HiPerGator, the University of Florida public research"
- [readme] Configuration file organization for HPC and Singularity settings: "High-performance computing and Singularity configuration is defined in `conf/HiPerGator.config`."
