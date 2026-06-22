---
name: hpc-job-parallelization
description: Use when you have a filtered set of conformers (100s–1000s) from ASE-ANI that each require independent quantum calculations via QUICK, and you have access to HPC resources with multiple cores or nodes. Parallelization is necessary when serial execution would exceed practical time budgets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0176
  tools:
  - QUICK
  - Snakemake
  - ASE-ANI
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- 'QUICK: For quantum calculations'
- Snakemake workflow manager for predicting collisional cross sections
- This repository contains a Snakemake workflow manager for predicting collisional cross sections (CCS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pomics_cq
    doi: 10.1021/jasms.1c00315
    title: POMICS
  dedup_kept_from: coll_pomics_cq
schema_version: 0.2.0
---

# HPC Job Parallelization

## Summary

Distribute independent conformer quantum calculations across HPC cores using a workflow manager to execute multiple QUICK jobs in parallel, reducing wall-clock time for large-scale CCS prediction pipelines. This skill coordinates job submission, resource allocation, and result aggregation on distributed compute infrastructure.

## When to use

You have a filtered set of conformers (100s–1000s) from ASE-ANI that each require independent quantum calculations via QUICK, and you have access to HPC resources with multiple cores or nodes. Parallelization is necessary when serial execution would exceed practical time budgets (e.g., 10+ hours for a single molecule's ensemble).

## When NOT to use

- Conformer set is small (< 10–20) and serial execution on a single CPU is acceptable.
- QUICK jobs have strong inter-job dependencies (e.g., iterative geometry refinement across conformers)—parallelization assumes independence.
- HPC infrastructure is not available or has strict job queue policies that penalize many short jobs; single-node execution may be more efficient.

## Inputs

- Filtered conformer set (xyz or molden format files) from ASE-ANI
- QUICK input specification (quantum method, basis set, molecular geometry per conformer)
- HPC cluster configuration (nodes, cores, walltime, memory allocation)
- Snakemake workflow definition (rules linking conformers to QUICK jobs)

## Outputs

- Aggregated QUICK output table mapping conformer ID to electronic properties (polarizability tensor, dipole moment)
- Individual QUICK output logs (one per conformer)
- Structured ccs.txt or ensemble results file with Boltzmann-averaged CCS values

## How to apply

Use a workflow manager (Snakemake) to define conformer-to-QUICK-job mapping, specify HPC cluster configuration (node count, walltime, memory per task in cluster.yaml), and submit batches of conformer calculations as independent jobs. Snakemake dynamically schedules jobs to available cores, monitors completion, and aggregates results. Configure job submission parameters (e.g., walltime and node specs) in cluster.yaml; ensure each QUICK job receives one conformer's xyz/molden geometry and outputs a structured log. The workflow parallelizes over the conformer set dimension—each conformer is an independent job with no data dependencies between them, enabling linear speedup up to the number of available HPC cores.

## Related tools

- **Snakemake** (Workflow manager that defines conformer-to-job mapping, schedules jobs across HPC resources, monitors task completion, and aggregates results) — https://snakemake.readthedocs.io
- **QUICK** (Quantum chemistry engine executed in parallel; each job receives one conformer and computes electronic properties (polarizability, dipole moment)) — https://github.com/merzlab/QUICK
- **ASE-ANI** (Upstream conformer filtering step that produces the input ensemble for parallelized QUICK calculations) — https://github.com/isayev/ASE_ANI

## Examples

```
bash scheduler.sh
```

## Evaluation signals

- All conformers in the input set have corresponding QUICK output logs with no missing or failed jobs.
- Wall-clock execution time is approximately (total_cpu_time / number_of_parallel_cores), indicating efficient utilization.
- Aggregated results table has one row per conformer with valid electronic properties (polarizability components and dipole moment are non-zero and chemically reasonable).
- Snakemake logs show all jobs transitioned to 'completed' state with exit code 0 and no task retries or timeouts.
- Boltzmann-averaged CCS value falls within the expected range for the molecule class (e.g., 50–400 Ų for small metabolites).

## Limitations

- Parallelization efficiency depends on HPC queue policy and core availability; oversubscribing jobs can lead to contention and slowdown.
- ASE-ANI README notes the tool is deprecated in favor of TorchANI; conformer filtering may require migration to the updated implementation.
- QUICK jobs are tightly coupled to HPC hardware (NVIDIA GPU, CUDA 9.2+ in older versions); portability to non-GPU or different-GPU HPC systems may require code adaptation.
- Memory overhead scales with conformer set size; very large ensembles (10,000+ conformers) may exceed per-node memory limits and require job chunking or workflow redesign.

## Evidence

- [other] Submit each conformer for quantum calculation via QUICK, executing in parallel on available HPC cores.: "Submit each conformer for quantum calculation via QUICK, executing in parallel on available HPC cores."
- [other] The workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems.: "high automation and parallelized computation on high-performance computing (HPC) systems"
- [readme] Configure the walltime, memory requirement, and node specifications in the `cluster.yaml` file.: "Configure the walltime, memory requirement, and node specifications in the `cluster.yaml` file."
- [readme] Snakemake workflow manager for predicting collisional cross sections.: "Snakemake workflow manager for predicting collisional cross sections"
