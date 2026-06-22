---
name: conformer-generation-rdkit
description: Use when when you have ionized adduct structures (SMILES or MOL format) from an ionization-state determination step and need to create an ensemble of relaxed 3D geometries for each molecule prior to expensive conformation filtering (e.g., ASE-ANI or quantum methods).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0482
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0176
  tools:
  - Snakemake
  - RDKit
  - Dimorphite-DL
  - ASE-ANI
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- Snakemake workflow manager for predicting collisional cross sections
- This repository contains a Snakemake workflow manager for predicting collisional cross sections (CCS)
- 'RDKit: For conformation generation'
- 'RDKit: For conformation generation. Available at: https://www.rdkit.org'
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

# conformer-generation-rdkit

## Summary

Generate and minimize 3D conformer ensembles from ionized molecular structures using RDKit's distance-geometry algorithm and force-field optimization. This skill produces multiple low-energy 3D geometries per molecule that serve as input for downstream high-level quantum or machine-learning filtering in CCS prediction workflows.

## When to use

When you have ionized adduct structures (SMILES or MOL format) from an ionization-state determination step and need to create an ensemble of relaxed 3D geometries for each molecule prior to expensive conformation filtering (e.g., ASE-ANI or quantum methods). Use this skill if your downstream analysis requires multiple conformers per molecule to account for conformational diversity.

## When NOT to use

- Input structures are already fully optimized 3D geometries from quantum calculations (re-minimizing with a force field will introduce systematic bias).
- Molecules contain elements outside RDKit's supported set (C, H, N, O, S, P, F, Cl, Br, I); use alternative conformer generators for exotic chemistries.
- Conformational diversity is not needed (e.g., if only one low-energy conformation per molecule is sufficient for your downstream step).

## Inputs

- Ionized adduct structures (SMILES strings or MOL files)
- Configuration parameters: number of conformers per molecule (e.g., 50–500), force field choice (MMFF94 or UFF), random seed (for reproducibility)

## Outputs

- 3D conformer ensemble (SDF or pickle format) with all conformers retained
- Per-conformer geometries and MMFF94/UFF minimized energies

## How to apply

Load ionized adduct structures in SMILES or MOL format. Use RDKit to add hydrogens and generate initial 3D coordinates via the distance-geometry algorithm (AllChem.EmbedMolecule). Generate 50–500 conformers per molecule depending on molecular size and sampling requirements. Minimize each conformer's geometry using RDKit's built-in force field (MMFF94 or UFF) to drive structures toward local minima. Export the complete conformer ensemble to SDF or pickle format, retaining all conformers for downstream filtering by higher-level methods (ASE-ANI, QUICK). The rationale is that diverse low-energy starting geometries improve the chances of sampling the global minimum during subsequent quantum or ML-based refinement.

## Related tools

- **RDKit** (Generates initial 3D coordinates via distance-geometry, creates conformer ensembles via AllChem.EmbedMolecule, and minimizes geometries using MMFF94/UFF force fields.) — https://www.rdkit.org
- **Dimorphite-DL** (Upstream tool that produces ionized adduct structures (SMILES) consumed by this conformer generation step.) — https://durrantlab.pitt.edu/dimorphite-dl
- **ASE-ANI** (Downstream tool that filters the generated conformer ensemble using neural-network potentials before quantum calculations.) — https://github.com/isayev/ASE_ANI
- **Snakemake** (Workflow orchestration framework that automates and parallelizes RDKit conformer generation across multiple molecules on HPC systems.) — https://github.com/DasSusanta/snakemake_ccs

## Examples

```
from rdkit import Chem; from rdkit.Chem import AllChem; mol = Chem.MolFromSmiles('CC(C)C[C@H](NC(=O)[C@H](CC(=O)N)NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@H](CO)NC(=O)[C@H](Cc1c[nH]cn1)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](CCC(=O)N)NC(=O)[C@H](CC(=O)O)NC(=O)[C@H](Cc1ccc(O)cc1)NC(=O)[C@H](Cc1ccccc1)NC(=O)CNC(=O)[C@H](N)Cc1ccc(O)cc1)C(=O)N[C@@H](Cc1ccccc1)C(=O)N[C@@H](CO)C(=O)N[C@@H](Cc1c[nH]cn1)C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H](CCC(=O)N)C(=O)N[C@@H](CC(=O)O)C(=O)N[C@@H](Cc1ccc(O)cc1)C(=O)N[C@@H](Cc1ccccc1)C(=O)N'); AllChem.EmbedMolecule(mol, numConfs=100); AllChem.MMFFOptimizeMoleculeConfs(mol); writer = Chem.SDWriter('conformers.sdf'); [writer.write(mol, confId=i) for i in range(mol.GetNumConformers())]; writer.close()
```

## Evaluation signals

- All output conformers have valid 3D coordinates and no steric clashes (check bond distances and van der Waals overlaps).
- Force-field minimized energies decrease or plateau across conformers, indicating convergence of geometry optimization.
- Conformer count per molecule matches the requested ensemble size (e.g., 50–500 without dropouts or failures).
- Output SDF/pickle files are readable and contain all conformers without truncation or corruption.
- Downstream ASE-ANI filtering or quantum calculations accept the generated conformers without geometry errors or parsing failures.

## Limitations

- RDKit's distance-geometry and force-field methods are heuristic; they may miss global minima or rare conformations that are important for some molecules.
- MMFF94/UFF are fast but approximate; force-field minimized geometries may deviate significantly from higher-level (quantum or ML-based) optima.
- Conformer generation is stochastic (unless random seed is fixed); repeated runs may yield slightly different ensemble compositions.
- The README notes ASE-ANI is deprecated; users should consider TorchANI as the successor tool for downstream filtering.

## Evidence

- [other] Use RDKit to add hydrogens and generate initial 3D coordinates via distance-geometry algorithm: "Use RDKit to add hydrogens and generate initial 3D coordinates via distance-geometry algorithm."
- [other] Generate multiple conformers per structure using RDKit's AllChem.EmbedMolecule with specified number of conformers (e.g., 50–500 samples per molecule): "Generate multiple conformers per structure using RDKit's AllChem.EmbedMolecule with specified number of conformers (e.g., 50–500 samples per molecule)."
- [other] Minimize each conformer's geometry using RDKit's built-in force field (MMFF94 or UFF) to relax structures toward local minima: "Minimize each conformer's geometry using RDKit's built-in force field (MMFF94 or UFF) to relax structures toward local minima."
- [other] Export the conformer ensemble to SDF or pickle format with all conformers retained for downstream filtering: "Export the conformer ensemble to SDF or pickle format with all conformers retained for downstream filtering."
- [other] RDKit is used in the workflow as the conformation generation tool that operates on ionized adduct structures produced by Dimorphite-DL: "RDKit is used in the workflow as the conformation generation tool that operates on ionized adduct structures produced by Dimorphite-DL"
- [readme] DEPRECATED and no longer supported, please use TorchANI implementation: "DEPRECATED and no longer supported, please use TorchANI implementation"
