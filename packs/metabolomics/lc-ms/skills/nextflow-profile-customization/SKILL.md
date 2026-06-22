---
name: nextflow-profile-customization
description: Use when you need to execute a Nextflow metabolomics workflow (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Nextflow
  - Singularity
  - Docker
  - MS-DIAL
  - MSFLO
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

# nextflow-profile-customization

## Summary

Customize Nextflow execution profiles to support containerized metabolomics workflows across diverse computational environments (local Docker, HPC with Singularity). This skill enables portable, reproducible LC-HRMS data processing by configuring container runtimes, resource directives, and tool-specific parameters for target execution contexts.

## When to use

You need to execute a Nextflow metabolomics workflow (e.g., MS-DIAL–based LC-HRMS processing) on a new computational environment—such as an HPC cluster with Singularity support or a local macOS/Linux machine with Docker—and existing profiles do not match your resource constraints, container runtime, or job scheduler (e.g., Slurm queue allocation).

## When NOT to use

- Input data is already in feature-table format (e.g., CSV abundance matrix); use this skill only when raw .mzML/.abf spectra must be processed through MS-DIAL.
- Target environment does not support containerization (no Docker or Singularity installation available); Nextflow4MS-DIAL requires container runtime for reproducibility.
- You are running on an unsupported or untested HPC system where Singularity configuration details are unknown and no reference profile (e.g., HiPerGator.config analogue) exists—profile customization may fail without HPC-specific documentation.

## Inputs

- .mzML or .abf raw LC-MS metabolomics data files
- MS-DIAL configuration file (msdial_params.txt)
- MS-FLO configuration file (msflo_params.ini)
- MS1 and MS2 spectral library files (ms1_lib.txt, ms2_lib.msp)
- Nextflow project repository (nextflow.config, conf/*.config files)

## Outputs

- .msdial output files (converted to .tsv for spreadsheet compatibility)
- execution_report.html (workflow runtime and resource usage summary)
- execution_timeline.html (per-process execution timeline)
- logs/execution.log (detailed execution metadata and process logs)
- Validated nextflow.config profile for target environment

## How to apply

1. Identify the target execution context (e.g., HPC cluster with Slurm scheduler, local Docker-capable machine) and its resource limits (CPU, memory, queue names). 2. Review the project's nextflow.config and existing profiles (e.g., conf/base.config, conf/HiPerGator.config) to understand current container directives and resource allocation patterns. 3. Create or extend a profile in nextflow.config with: (a) container enablement (e.g., singularity.enabled = true or docker.enabled = true), (b) process directives specifying container image paths (e.g., process.container = 'singularity://...'), and (c) HPC-specific resource requests (cpus, memory, queue, time limits). 4. Use --max_cpus (not --cpus) to define per-process CPU limits relative to available cluster resources. 5. Test the profile on sample .mzML LC-MS data (or a functional_test profile) by running nextflow run main.nf -profile <profile_name> and inspect execution_report.html and logs for container initialization success, resource utilization, and process completion. 6. Validate that all output .msdial files are produced and that no resource-related errors (e.g., 'Process requirement exceed available CPUs') appear in error logs.

## Related tools

- **Nextflow** (Workflow orchestration engine; manages process execution, parallelization, and container runtime selection across local and HPC environments) — https://www.nextflow.io/
- **Singularity** (Container runtime for HPC environments; executes MS-DIAL and MSFLO processes in isolated, reproducible container images on compute clusters) — https://www.sylabs.io/guides/3.0/user-guide/
- **Docker** (Container runtime for local execution; packages MS-DIAL and MSFLO tools with all dependencies for macOS and Linux workstations) — https://docs.docker.com/engine/installation/
- **MS-DIAL** (Peak detection and metabolite identification tool; processes .mzML LC-HRMS data according to user-defined parameters in msdial_params.txt) — https://github.com/Nextflow4Metabolomics/nextflow4ms-dial
- **MSFLO** (Post-processing and feature annotation tool; refines MS-DIAL output and generates final metabolite abundance tables) — https://github.com/Nextflow4Metabolomics/nextflow4ms-dial

## Examples

```
nextflow run main.nf -profile singularity --max_cpus 20
```

## Evaluation signals

- Container initialization succeeds: execution_report.html and logs confirm 'Singularity [version]' or 'Docker [version]' runtime active with no 'container not found' or 'pull failed' errors.
- Resource allocation matches request: execution_report.html shows actual CPU and memory usage ≤ specified limits; no Slurm errors like 'Process requirement exceed available CPUs' in error.txt.
- All processes complete: execution_timeline.html displays all pipeline steps (MS-DIAL, MSFLO) in green (completed); .msdial/.tsv output files exist in results/ directory with non-zero file size.
- Profile-specific parameters applied: logs/execution.log lists correct queue name, cpus, and memory values for the target profile; container image path matches nextflow.config specification.
- No file-name errors: output files lack special characters (except underscores); no 'file not found' or 'invalid filename' messages in error logs.

## Limitations

- Special characters in input file names (except underscores) cause silent process skipping; users must rename raw .mzML/.abf files before execution.
- CPU limit parameter --max_cpus must be used instead of --cpus in HPC configuration; incorrect parameter name causes resource allocation failures with cryptic Slurm messages.
- Profile customization requires manual HPC environment documentation (queue names, max CPU/memory, job submission system); automated detection not supported.
- Singularity container images must be pre-built or pulled from a compatible registry; Docker-to-Singularity conversion requires additional tools and expertise outside Nextflow.
- HPC scheduler differences (Slurm vs. LSF vs. PBS) necessitate environment-specific profiles; a single profile may not port across institutions.

## Evidence

- [other] Both Docker and Singularity (for high-performance computing) are supported: "Both Docker and Singularity (for high-performance computing) are supported"
- [readme] High-performance computing and Singularity configuration is defined in conf/HiPerGator.config.: "High-performance computing and Singularity configuration is defined in conf/HiPerGator.config."
- [other] Create a Singularity profile in the nextflow.config that specifies the container directive with Singularity syntax (e.g., singularity.enabled = true, process.container = 'singularity://...') and HPC resource directives (queue, cpus, memory).: "Create a Singularity profile in the nextflow.config that specifies the container directive with Singularity syntax (e.g., singularity.enabled = true, process.container = 'singularity://...') and HPC"
- [readme] Use `--max_cpus`, not `--cpus`, in the configuration file to define the CPUs available to each process.: "Use `--max_cpus`, not `--cpus`, in the configuration file to define the CPUs available to each process."
- [readme] To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] nextflow run main.nf -profile docker for local execution and the `singularity` profile for high-performance computing environments: "nextflow run main.nf -profile docker for local execution and the `singularity` profile for high-performance computing environments"
- [readme] execution_report.html summarizes workflow runtime and computational resource usage.: "execution_report.html summarizes workflow runtime and computational resource usage."
