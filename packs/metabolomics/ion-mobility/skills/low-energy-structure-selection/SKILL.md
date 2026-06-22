---
name: low-energy-structure-selection
description: Use when after generating an ensemble of 3D conformers via RDKit conformation sampling, when you need to reduce the conformer set size before expensive quantum-chemical calculations (e.g., QUICK).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  tools:
  - ASE-ANI
  - RDKit
  - Snakemake
  - QUICK
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- 'ASE-ANI: For conformation filtering'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Low-Energy Structure Selection

## Summary

Select and rank molecular conformers by computed single-point energies using a neural network potential, retaining the lowest-energy subset for downstream quantum-chemical calculations. This filtering step reduces computational cost while preserving conformational diversity relevant to collision cross section prediction.

## When to use

After generating an ensemble of 3D conformers via RDKit conformation sampling, when you need to reduce the conformer set size before expensive quantum-chemical calculations (e.g., QUICK). Use this skill when conformers are provided in SDF or XYZ format and you have access to a GPU-accelerated neural network potential.

## When NOT to use

- Input conformers contain elements outside CHNO (e.g., halogens, transition metals); ANI-1x/ANI-1ccx do not support them.
- No GPU available or compute capability < 5.0; ASE-ANI requires modern NVIDIA GPU and CUDA 9.2.
- Conformers are already filtered or ranked by a prior method; applying this skill would introduce redundant energy computation.
- Goal is to retain all conformational diversity; energy-based selection may discard rare but structurally important conformers.

## Inputs

- RDKit-generated conformer ensemble (SDF or XYZ format)
- ASE-ANI potential model weights (ANI-1x or ANI-1ccx)
- List or count of conformers to retain (N or energy threshold)

## Outputs

- Ranked conformer set with computed energies
- Filtered low-energy conformer ensemble (SDF or XYZ)
- Energy scores per conformer (eV)

## How to apply

Initialize the ASE-ANI neural network potential (ANI-1x or ANI-1ccx, supporting CHNO elements) and compute single-point energy for each RDKit-generated conformer using the Atomic Simulation Environment (ASE) interface. Rank conformers by computed energy and apply an energy threshold or retain the top N lowest-energy conformers—the exact cutoff depends on balancing computational cost against conformational sampling needs for CCS ensemble averaging. Export the filtered conformer set in XYZ or SDF format compatible with downstream quantum-chemical software. The rationale is that ASE-ANI provides fast, DFT-accurate energies at force-field cost, making it suitable for pre-filtering before more expensive single-point or property calculations.

## Related tools

- **ASE-ANI** (Neural network potential for fast, DFT-accurate single-point energy computation and conformer ranking) — https://github.com/isayev/ASE_ANI
- **RDKit** (Source of conformer ensemble generation upstream of this filtering step) — https://www.rdkit.org
- **Snakemake** (Workflow orchestration for parallelized ASE-ANI energy calculations on HPC systems) — https://github.com/DasSusanta/snakemake_ccs
- **QUICK** (Downstream quantum-chemical software consuming filtered conformer set for CCS calculations)

## Evaluation signals

- Energy values are computed and ranked in ascending order; check that minimum energy is lower than initial ensemble mean.
- Filtered conformer count matches the specified threshold (top N or energy cutoff); verify no conformers are lost or duplicated.
- Energy spread across retained conformers reflects chemical diversity (e.g., rotamers, ring flips); anomalously narrow energy range may indicate over-aggressive filtering.
- Exported conformer file format (SDF/XYZ) is readable by downstream QUICK software and preserves 3D coordinates.
- ASE-ANI computation completes without GPU memory errors or unsupported-element warnings; log files confirm all conformers were processed.

## Limitations

- ASE-ANI is deprecated (per README); users should migrate to TorchANI for ongoing support and newer element coverage (CHNOSFCl).
- Restricted to CHNO elements; any conformer containing halogens, metals, or other elements will fail or be skipped.
- GPU and CUDA 9.2 are required; no CPU fallback is available. Works only on Ubuntu Linux variants with NVIDIA GPU (compute capability ≥ 5.0).
- Energy ranking alone does not guarantee biological or experimental relevance; lowest-energy conformers may not dominate solution-phase ensembles due to entropy and solvation effects not captured by gas-phase neural network potentials.
- Python 3.6 binary compatibility is outdated; modern Python environments may require conda/mamba setup with specific version pinning.

## Evidence

- [other] Initialize ASE-ANI potential and compute single-point energy for each conformer. Rank conformers by energy and select the lowest-energy subset (retain top N conformers or apply an energy threshold).: "Initialize ASE-ANI potential and compute single-point energy for each conformer. Rank conformers by energy and select the lowest-energy subset (retain top N conformers or apply an energy threshold)."
- [other] Load conformer structures generated by RDKit in a standard molecular format (e.g., SDF or XYZ). ... Export filtered conformer set in a format compatible with downstream quantum-chemical software (QUICK).: "Load conformer structures generated by RDKit in a standard molecular format (e.g., SDF or XYZ). ... Export filtered conformer set in a format compatible with downstream quantum-chemical software"
- [intro] ASE-ANI: For conformation filtering. Available at: [https://github.com/isayev/ASE_ANI]: "ASE-ANI: For conformation filtering. Available at: [https://github.com/isayev/ASE_ANI]"
- [readme] This is a prototype interface for ANI-1x and ANI-1ccx neural network potentials for The Atomic Simulation Environment (ASE). Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements.: "Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements."
- [readme] DEPRECATED and no longer supported, please use [TorchANI](https://github.com/aiqm/torchani) implementation: "DEPRECATED and no longer supported, please use [TorchANI] implementation"
- [readme] Modern NVIDIA GPU, [compute capability 5.0](https://developer.nvidia.com/cuda-gpus) of newer. [CUDA 9.2](https://developer.nvidia.com/cuda-downloads): "Modern NVIDIA GPU, [compute capability 5.0] of newer. [CUDA 9.2]"
- [intro] workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems: "high automation and parallelized computation on high-performance computing (HPC) systems"
