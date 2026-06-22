---
name: small-molecule-3d-structure-preparation
description: Use when when you have ionized adduct structures (SMILES or MOL format) from a prior ionization-state determination step and need to create multiple low-energy 3D conformations before filtering with machine-learning potentials (ASE-ANI) or quantum calculations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0432
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0176
  tools:
  - Snakemake
  - RDKit
  - Dimorphite-DL
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

# small-molecule-3d-structure-preparation

## Summary

Generate and optimize 3D conformer ensembles from ionized molecular structures using RDKit's distance-geometry algorithm and force-field minimization. This skill is essential for preparing small molecules for downstream quantum chemical or neural-network-based energy filtering in high-throughput CCS prediction workflows.

## When to use

When you have ionized adduct structures (SMILES or MOL format) from a prior ionization-state determination step and need to create multiple low-energy 3D conformations before filtering with machine-learning potentials (ASE-ANI) or quantum calculations. Use this skill if your downstream workflow requires conformer ensembles rather than single-point structures.

## When NOT to use

- Input structures are already 3D-optimized at high confidence by prior quantum calculations; re-embedding and minimization would waste computational resources.
- Workflow requires single low-energy conformations only, not ensembles; use simpler single-conformer embedding instead.
- Molecules contain elements outside RDKit's support (e.g., transition metals); alternative tools required.

## Inputs

- ionized adduct structures (SMILES strings or MOL format files)
- conformer count specification (e.g., 50–500 per molecule)
- force-field choice (MMFF94 or UFF)

## Outputs

- 3D conformer ensemble in SDF format
- 3D conformer ensemble in pickle format
- minimized geometries with force-field energies

## How to apply

Load the ionized structures from upstream (e.g., output from Dimorphite-DL) and use RDKit to add explicit hydrogens and embed the molecule in 3D space using the distance-geometry algorithm. Generate a large conformer ensemble (e.g., 50–500 samples per molecule) via RDKit's AllChem.EmbedMolecule. Minimize each conformer's geometry using RDKit's built-in force field (MMFF94 or UFF) to relax structures toward local minima. Export all conformers to SDF or pickle format, retaining the full ensemble for downstream filtering by neural-network potentials or quantum methods. The rationale is that multiple conformers capture conformational diversity and allow subsequent filtering tools to select energetically favorable or ML-screened geometries before expensive quantum calculations.

## Related tools

- **RDKit** (3D coordinate generation, hydrogen addition, conformer embedding via distance-geometry, and force-field minimization (MMFF94/UFF)) — https://www.rdkit.org
- **Dimorphite-DL** (upstream ionization-state determination producing ionized structures that serve as input to this skill) — https://durrantlab.pitt.edu/dimorphite-dl
- **ASE-ANI** (downstream conformer filtering using neural-network potential energy screening) — https://github.com/isayev/ASE_ANI
- **Snakemake** (workflow orchestration and parallelization of conformer generation across multiple molecules on HPC systems) — https://github.com/DasSusanta/snakemake_ccs

## Examples

```
from rdkit import Chem; from rdkit.Chem import AllChem; mol = Chem.MolFromSmiles('C1=CC=C(C=C1)[NH3+]'); mol = Chem.AddHs(mol); AllChem.EmbedMolecule(mol, numConfs=100); AllChem.MMFFOptimizeMoleculeConfs(mol); writer = Chem.SDWriter('conformers.sdf'); [writer.write(mol, i) for i in range(mol.GetNumConformers())]
```

## Evaluation signals

- All conformers per molecule are successfully embedded and have valid 3D coordinates (no NaN or infinite values in coordinate arrays).
- Force-field minimization converges for each conformer, with final energies lower than initial post-embedding energies, indicating geometry relaxation.
- Output SDF/pickle files contain the specified number of conformers per input molecule (e.g., 50–500 samples retained without loss).
- Downstream ASE-ANI or quantum filtering accepts the conformer ensemble without geometry errors or parsing failures.
- Conformer RMSD within each ensemble is > 0.5 Å, confirming conformational diversity; excessive clustering indicates under-exploration.

## Limitations

- RDKit's force-field minimization is local; conformers may be trapped in local minima and not represent true global minimum-energy conformations—reliance on downstream ML or quantum refinement is essential.
- Distance-geometry embedding may fail or produce strained geometries for highly constrained or polycyclic structures; manual intervention or alternative embedding strategies may be required.
- Conformer generation is stochastic; results vary across runs. Users should set a random seed or run multiple replicates to ensure reproducibility.
- ASE-ANI (the recommended downstream filter tool) is deprecated; the README recommends migrating to TorchANI for ongoing support.

## Evidence

- [other] Use RDKit to add hydrogens and generate initial 3D coordinates via distance-geometry algorithm. Generate multiple conformers per structure using RDKit's AllChem.EmbedMolecule with specified number of conformers (e.g., 50–500 samples per molecule).: "Use RDKit to add hydrogens and generate initial 3D coordinates via distance-geometry algorithm. Generate multiple conformers per structure using RDKit's AllChem.EmbedMolecule with specified number of"
- [other] Minimize each conformer's geometry using RDKit's built-in force field (MMFF94 or UFF) to relax structures toward local minima. Export the conformer ensemble to SDF or pickle format with all conformers retained for downstream filtering.: "Minimize each conformer's geometry using RDKit's built-in force field (MMFF94 or UFF) to relax structures toward local minima. Export the conformer ensemble to SDF or pickle format with all"
- [other] RDKit is used in the workflow as the conformation generation tool that operates on ionized adduct structures produced by Dimorphite-DL, generating 3D conformers that are subsequently filtered by ASE-ANI before quantum calculations.: "RDKit is used in the workflow as the conformation generation tool that operates on ionized adduct structures produced by Dimorphite-DL, generating 3D conformers that are subsequently filtered by"
- [other] Load ionized adduct structures (SMILES or MOL format) from the upstream ionization-state determination step.: "Load ionized adduct structures (SMILES or MOL format) from the upstream ionization-state determination step."
- [readme] workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems: "workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems"
