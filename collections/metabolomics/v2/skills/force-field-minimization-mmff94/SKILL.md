---
name: force-field-minimization-mmff94
description: Use when after RDKit generates multiple 3D conformers from ionized molecular structures using distance-geometry embedding, before filtering with ASE-ANI or submitting to quantum calculations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0321
  edam_topics:
  - http://edamontology.org/topic_0176
  - http://edamontology.org/topic_0154
  tools:
  - Snakemake
  - RDKit
  - ASE-ANI
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
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

# Force-field minimization (MMFF94)

## Summary

Relax 3D molecular conformers toward local energy minima using the Merck Molecular Force Field (MMFF94) or universal force field (UFF), applied post-generation to prepare conformer ensembles for downstream quantum chemical or machine-learning filtering in CCS prediction workflows.

## When to use

After RDKit generates multiple 3D conformers from ionized molecular structures using distance-geometry embedding, before filtering with ASE-ANI or submitting to quantum calculations. Use this skill when conformers are in high-energy, unrealistic geometries that would bias downstream energy-based filtering or CCS prediction.

## When NOT to use

- Input structures contain atoms outside the CHNO set supported by MMFF94 (e.g., halides or transition metals)—use UFF instead.
- Conformers are already at quantum geometry (e.g., DFT-optimized)—minimization would be redundant and computationally wasteful.
- Speed is critical and conformer quality is secondary—skip minimization if ensemble size is >1000 conformers per molecule on limited compute.

## Inputs

- RDKit Mol object with 3D coordinates and multiple conformers (MMCIF, SDF, or MOL format)
- Ionized molecular structures (protonated/deprotonated adducts from Dimorphite-DL)

## Outputs

- SDF or pickle file containing relaxed 3D conformer ensemble with MMFF94-minimized geometries
- Per-conformer final force field energy and convergence status

## How to apply

For each RDKit-generated conformer, apply MMFF94 force field (preferred for drug-like CHNO molecules) or UFF as fallback to minimize geometry toward a local minimum. RDKit's AllChem.MMFFOptimizeMolecule() or UFF minimizer iteratively adjusts atomic coordinates using gradient-based optimization until convergence (typically <0.01 kcal/(mol·Å) RMS gradient). Retain all minimized conformers in the ensemble—do not filter by final energy at this stage, as ASE-ANI will rank them later. Export the relaxed conformer ensemble to SDF or pickle format with all conformers preserved for downstream filtering.

## Related tools

- **RDKit** (Provides AllChem.MMFFOptimizeMolecule() and UFF minimization functions to relax conformer geometries toward local minima using MMFF94 or universal force field.) — https://www.rdkit.org
- **ASE-ANI** (Downstream filtering tool that ranks MMFF94-minimized conformers using neural network potentials; receives relaxed conformer ensemble as input.) — https://github.com/isayev/ASE_ANI
- **Snakemake** (Orchestrates the conformer minimization step as part of the automated CCS prediction workflow on HPC systems.) — https://github.com/DasSusanta/snakemake_ccs

## Examples

```
from rdkit import Chem; from rdkit.Chem import AllChem; mol = Chem.AddHs(Chem.MolFromSmiles('c1ccccc1O')); AllChem.EmbedMolecule(mol, randomSeed=42); AllChem.MMFFOptimizeMolecule(mol); Chem.SDWriter('conformers_minimized.sdf').write(mol)
```

## Evaluation signals

- All conformers in the output ensemble have converged energy (final gradient <0.01 kcal/(mol·Å) RMS or tool's default threshold).
- Output conformer count matches input count—no conformers discarded during minimization.
- Final MMFF94 energies are lower than initial post-embedding energies (positive energy decrease per conformer).
- Minimized conformer geometries pass downstream ASE-ANI filtering and yield physically plausible CCS values within experimental range.
- SDF/pickle file contains all conformers with retained 3D coordinates and no NaN or Inf values in geometry matrices.

## Limitations

- MMFF94 is parameterized only for organic molecules (CHNO atoms); halogenated or metallated compounds require UFF or custom parameterization.
- Force field minimization may trap conformers in local minima; not guaranteed to find global minimum energy structure.
- Computational cost scales with conformer count and molecular size; ensemble of 50–500 conformers per molecule requires significant CPU time.
- README notes ASE-ANI is deprecated—users should migrate to TorchANI for modern neural network–based filtering post-minimization.

## Evidence

- [other] Minimize each conformer's geometry using RDKit's built-in force field (MMFF94 or UFF) to relax structures toward local minima.: "Minimize each conformer's geometry using RDKit's built-in force field (MMFF94 or UFF) to relax structures toward local minima."
- [other] Generate multiple conformers per structure using RDKit's AllChem.EmbedMolecule with specified number of conformers (e.g., 50–500 samples per molecule).: "Generate multiple conformers per structure using RDKit's AllChem.EmbedMolecule with specified number of conformers (e.g., 50–500 samples per molecule)."
- [other] Export the conformer ensemble to SDF or pickle format with all conformers retained for downstream filtering.: "Export the conformer ensemble to SDF or pickle format with all conformers retained for downstream filtering."
- [readme] DEPRECATED and no longer supported, please use TorchANI implementation: "DEPRECATED and no longer supported, please use TorchANI implementation"
- [readme] Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements.: "Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements."
