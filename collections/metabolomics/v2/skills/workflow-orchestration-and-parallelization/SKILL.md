---
name: workflow-orchestration-and-parallelization
description: Use when when you have a multi-step computational chemistry or molecular modeling pipeline (3+ sequential or parallel stages) that must process many molecules, each requiring repeated tool invocations with different parameters, and you need reproducibility, fault tolerance, and the ability to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0176
  tools:
  - Snakemake
  - Dimorphite-DL
  - ASE-ANI
  - QUICK
  - RDKit
  - hpccs
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- Snakemake workflow manager for predicting collisional cross sections
- This repository contains a Snakemake workflow manager for predicting collisional cross sections (CCS)
- 'Dimorphite-DL: For ionization state determination'
- 'ASE-ANI: For conformation filtering'
- 'QUICK: For quantum calculations'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.1c00315
  all_source_dois:
  - 10.1021/jasms.1c00315
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# workflow-orchestration-and-parallelization

## Summary

Use Snakemake to orchestrate multi-stage computational chemistry pipelines with automatic parallelization across HPC nodes, enabling efficient end-to-end prediction of molecular properties (e.g., collisional cross sections) from SMILES input through ionization, conformation generation, filtering, and quantum calculations.

## When to use

When you have a multi-step computational chemistry or molecular modeling pipeline (3+ sequential or parallel stages) that must process many molecules, each requiring repeated tool invocations with different parameters, and you need reproducibility, fault tolerance, and the ability to distribute work across HPC clusters or multi-core workstations without manually scheduling each job.

## When NOT to use

- Input is a single molecule or handful of structures; overhead of HPC job submission outweighs parallelization benefit.
- Workflow is a simple linear sequence with no branching or fan-out; simpler shell scripts or Python loops are sufficient.
- Real-time or interactive iteration is required; Snakemake batch submission adds latency unsuitable for exploratory analysis.
- Software dependencies cannot be installed or containerized; Snakemake requires all tools accessible via paths or environment modules.

## Inputs

- SMILES input file (one structure per line)
- paths.json (software installation paths: Dimorphite-DL, RDKit, ASE-ANI, QUICK, hpccs)
- arguments.json (workflow parameters: ionization pH, conformation count, energy cutoff, quantum method)
- cluster.yaml (HPC resource specifications: walltime, memory, nodes per stage)

## Outputs

- ccs.txt (Boltzmann-averaged CCS values per input molecule and adduct)
- Intermediate SMILES variants (ionized, multi-adduct)
- Conformer ensemble files (RDKit geometry outputs)
- Filtered conformer subset (ASE-ANI low-energy structures)
- Quantum calculation outputs (QUICK molecular properties)
- Snakemake DAG and execution logs (workflow provenance)

## How to apply

Define the workflow as a Snakefile with explicit input→rule→output dependencies for each pipeline stage (e.g., SMILES → ionization state determination → conformation generation → energy filtering → quantum calculations → CCS prediction). Use Snakemake's wildcard expansion to parallelize across molecules and adduct types automatically. Configure a cluster.yaml file specifying walltime, memory, and node requirements per rule, then invoke the workflow via a scheduler script (e.g., bash scheduler.sh) to submit jobs to the HPC queue. Snakemake tracks file outputs and re-runs only failed or out-of-date stages, avoiding redundant computation. Specify tool paths and arguments in JSON configuration files (paths.json, arguments.json) to decouple workflow logic from environment details.

## Related tools

- **Snakemake** (Workflow orchestration engine: parses Snakefile rules, resolves dependencies, parallelizes jobs across molecules/adducts, submits to HPC scheduler) — https://snakemake.github.io
- **Dimorphite-DL** (First workflow stage: predicts protonated and deprotonated ionization states for each SMILES at specified pH) — https://durrantlab.pitt.edu/dimorphite-dl
- **RDKit** (Second stage: generates 3D conformer ensembles for each ionized molecule variant) — https://www.rdkit.org
- **ASE-ANI** (Third stage: filters conformer ensemble using ANI neural network potentials to retain low-energy structures) — https://github.com/isayev/ASE_ANI
- **QUICK** (Fourth stage: performs quantum mechanical calculations (semi-empirical or DFT) on filtered conformers to compute molecular properties) — https://github.com/merzlab/QUICK
- **hpccs** (Fifth stage: computes collision cross section from quantum outputs; final aggregation step) — https://github.com/cepid-cces/hpccs

## Examples

```
conda activate snakemake && bash scheduler.sh
```

## Evaluation signals

- Snakemake DAG completes without errors; all expected output files (ccs.txt, logs) are generated with valid content.
- Job submission and scheduling align with cluster.yaml specs: walltime, memory, and node counts match submitted jobs.
- Reproducibility check: re-running the workflow with same input and config produces identical output files (bit-for-bit or numerically equivalent CCS values).
- Parallelization efficiency: monitor job queue; workflow should spawn parallel tasks for independent molecules and adducts, reducing wall-clock time relative to sequential execution.
- Intermediate file consistency: inspect conformer counts, energy distributions, and quantum calculation convergence at each stage to confirm tools executed correctly and data flowed as expected.

## Limitations

- ASE-ANI is deprecated and no longer actively supported; repository recommends migration to TorchANI. Performance on molecules outside CHNO element set (e.g., with S, F, Cl) requires alternative neural network models.
- ASE-ANI binary compatibility limited to Python 3.6, CUDA 9.2, and Ubuntu Linux with NVIDIA GPUs; deployment on newer GPU architectures or non-Linux systems requires recompilation or use of TorchANI alternative.
- Workflow assumes all software dependencies are pre-installed and paths specified in paths.json are correct; missing or misconfigured tools fail silently or produce cryptic errors.
- Conformation generation and quantum calculation runtimes scale rapidly with molecule size and flexibility; large-scale applications on thousands of heavy molecules may exceed HPC queue limits or wall-clock time budgets.
- Snakemake DAG resolution requires all input files and configuration to be specified upfront; dynamic or streaming workflows (e.g., responding to user input mid-run) are not supported.

## Evidence

- [intro] workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems: "workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems"
- [intro] Snakemake workflow manager for predicting collisional cross sections: "Snakemake workflow manager for predicting collisional cross sections (CCS) using simplified molecular-input line-entry system (SMILES) structures"
- [other] The workflow integrates four sequential computational steps: Dimorphite-DL for ionization state determination, RDKit for conformation generation, ASE-ANI for conformation filtering, and QUICK for quantum calculations.: "The workflow integrates four sequential computational steps: Dimorphite-DL for ionization state determination, RDKit for conformation generation, ASE-ANI for conformation filtering, and QUICK for"
- [readme] 1. Specify the paths to the installed software in the `paths.json` file. 2. Configure the walltime, memory requirement, and node specifications in the `cluster.yaml` file. 3. Provide all the necessary arguments in the `arguments.json` file. 4. To run the workflow, execute the following command: bash scheduler.sh: "Specify the paths to the installed software in the `paths.json` file. 2. Configure the walltime, memory requirement, and node specifications in the `cluster.yaml` file. 3. Provide all the necessary"
- [readme] DEPRECATED and no longer supported, please use TorchANI implementation: "DEPRECATED and no longer supported, please use [TorchANI](https://github.com/aiqm/torchani) implementation"
- [readme] Works only under Ubuntu variants of Linux with a NVIDIA GPU: "Works only under Ubuntu variants of Linux with a NVIDIA GPU"
- [readme] After successful job completion, the workflow will generate a `ccs.txt` file in the `ensemble` (or `ensemble_fast`) folder. The `ccs.txt` file contains the Boltzmann average CCS values computed using this workflow.: "After successful job completion, the workflow will generate a `ccs.txt` file in the `ensemble` (or `ensemble_fast`) folder. The `ccs.txt` file contains the Boltzmann average CCS values computed using"
