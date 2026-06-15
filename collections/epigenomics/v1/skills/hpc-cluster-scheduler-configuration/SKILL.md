---
name: hpc-cluster-scheduler-configuration
description: Use when when installing HiC-Pro on a shared HPC cluster or multi-node computing environment where job submission must be routed through a scheduler rather than running locally.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0314
  edam_topics:
  - http://edamontology.org/topic_0218
  tools:
  - MultiQC 1.8
  - bowtie2
  - samtools (>=1.9)
  - R
  - TORQUE
  - SGE
  - SLURM
  - LSF
  - HiC-Pro
derived_from:
- doi: 10.1186/s13059-015-0831-x
  title: hicpro
evidence_spans:
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected
- samtools (>=1.9) can be automatically installed if not detected
- R (http://www.r-project.org/) with the following packages
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hicpro
    doi: 10.1186/s13059-015-0831-x
    title: hicpro
  dedup_kept_from: coll_hicpro
schema_version: 0.2.0
---

# HPC Cluster Scheduler Configuration

## Summary

Configure HiC-Pro to submit jobs to a specific cluster scheduler (TORQUE, SGE, SLURM, or LSF) by editing the installation configuration file with the appropriate CLUSTER_SYS parameter. This skill ensures that the pipeline can distribute computationally intensive steps across a high-performance computing infrastructure.

## When to use

When installing HiC-Pro on a shared HPC cluster or multi-node computing environment where job submission must be routed through a scheduler rather than running locally. Specifically, when the target system uses one of the supported schedulers (TORQUE, SGE, SLURM, or LSF) and you need HiC-Pro's sequential workflow steps to execute in parallel across cluster nodes.

## When NOT to use

- Input data is already pre-aligned BAM files or normalized contact matrices—this skill configures the execution environment, not the analysis itself.
- The target system does not use a supported scheduler (TORQUE, SGE, SLURM, LSF)—use local/laptop installation instead.
- You are installing HiC-Pro on a single machine without cluster access and intend to run the pipeline sequentially on that machine.

## Inputs

- config-install.txt template file (with CLUSTER_SYS placeholder)
- HiC-Pro source archive

## Outputs

- config-system.txt (read-only configuration file with locked CLUSTER_SYS parameter)
- HiC-Pro installation configured for target scheduler

## How to apply

During HiC-Pro installation, identify the scheduler used by your HPC environment (TORQUE, SGE, SLURM, or LSF). Edit the config-install.txt file before running 'make configure' and 'make install', setting the CLUSTER_SYS parameter to the correct scheduler name. The installation process reads this configuration and generates a system-specific config-system.txt file that locks in the scheduler choice. The pipeline will subsequently use this configuration to format and submit job scripts appropriately for your cluster's resource manager, enabling each workflow step to run independently on cluster nodes rather than sequentially on a single machine.

## Related tools

- **TORQUE** (PBS job scheduler option for cluster submission)
- **SGE** (Sun Grid Engine scheduler option for cluster submission)
- **SLURM** (SLURM Workload Manager scheduler option for cluster submission)
- **LSF** (IBM Platform Load Sharing Facility scheduler option for cluster submission)
- **HiC-Pro** (Hi-C processing pipeline whose installation and job submission behavior is configured by this skill) — https://github.com/nservant/HiC-Pro

## Examples

```
echo 'CLUSTER_SYS=SLURM' >> config-install.txt && make configure && make install
```

## Evaluation signals

- Verify that config-system.txt exists and contains the correct CLUSTER_SYS entry matching the target scheduler name (TORQUE, SGE, SLURM, or LSF).
- Confirm that config-system.txt is marked read-only (e.g., chmod 444) to prevent accidental user modification during pipeline execution.
- Test that HiC-Pro's job submission commands correctly format scheduler directives (e.g., #PBS, #$ , #SBATCH, or #BSUB) when running a workflow step that requires cluster submission.
- Verify installation completion by running 'HiC-Pro -h' and checking that no scheduler configuration errors are reported.
- Submit a test job via HiC-Pro and confirm it appears in the cluster scheduler's queue with appropriate directives for the configured scheduler.

## Limitations

- Only four schedulers are supported (TORQUE, SGE, SLURM, LSF); other schedulers require manual configuration or local execution.
- The CLUSTER_SYS parameter is set at installation time and locked into the config-system.txt file; changing schedulers requires reinstallation.
- HiC-Pro's sequential workflow design means some steps still run locally; only specific computationally intensive steps benefit from cluster submission.
- Configuration does not automatically tune scheduler parameters (e.g., node count, memory per job, wall time) — users must specify these in separate job configuration files or command-line arguments.

## Evidence

- [readme] CLUSTER_SYS parameter definition: "CLUSTER_SYS   | Scheduler to use for cluster submission. Must be TORQUE, SGE, SLURM or LSF"
- [readme] Configuration file editing workflow: "Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH"
- [other] Generated configuration file locking mechanism: "Compile all detected or user-specified paths and system parameters into a structured config-system.txt file with entries for each dependency path and cluster scheduler type. Lock the generated"
- [readme] Installation command syntax: "make configure
make install"
- [readme] Pipeline scalability design: "The pipeline is flexible, scalable and optimized. It can operate either on a single laptop or on a computational cluster."
