---
name: molecular-structure-conformer-generation
description: Use when you have 2D molecular structures (SMILES or SDF format) and need to create 3D conformer geometries as input to subsequent computational chemistry workflows, such as CCS prediction, molecular graph construction, or voxel-based property calculations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0176
  - http://edamontology.org/topic_3314
  tools:
  - Python 3
  - pandas
  - NumPy
  - RDKit
  - PyTorch
  - PyG
  - Jupyter Notebook
  - conda
  - pip
  - ETKDGv3
  - EmbedMultipleConfs
  - MMFFOptimizeMoleculeConfs
  techniques:
  - ion-mobility-MS
  - NMR
derived_from:
- doi: 10.1002/cem.70040
  title: PACCS
evidence_spans:
- '[python3](https://www.python.org/)'
- '[pandas](https://pandas.pydata.org/)'
- '[NumPy](https://numpy.org/)'
- '[RDKit](https://rdkit.org/)'
- '[PyTorch](https://pytorch.org/)'
- '[PyG](https://pytorch-geometric.readthedocs.io/en/latest/)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_paccs_cq
    doi: 10.1002/cem.70040
    title: PACCS
  dedup_kept_from: coll_paccs_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/cem.70040
  all_source_dois:
  - 10.1002/cem.70040
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-conformer-generation

## Summary

Generate optimized 3D conformers from molecular SMILES or SDF inputs using RDKit's ETKDGv3 embedding and MMFF force field optimization. This is a prerequisite data-preparation step for physics-based molecular property prediction, including collision cross section (CCS) calculations.

## When to use

You have 2D molecular structures (SMILES or SDF format) and need to create 3D conformer geometries as input to subsequent computational chemistry workflows, such as CCS prediction, molecular graph construction, or voxel-based property calculations. Start this step when input data lacks 3D coordinates or when you need to generate multiple conformations per molecule for ensemble-based predictions.

## When NOT to use

- Input molecules already contain experimentally determined 3D structures (e.g., from X-ray crystallography or NMR); use those coordinates directly.
- You require multiple conformers per molecule for explicit ensemble averaging; the single-conformer workflow (numConfs=1) is not suitable.
- Input is already a pre-computed conformer library or conformer database; skip to CCS calculation or graph construction.

## Inputs

- SMILES strings (one per molecule)
- SDF molecular structure files
- pandas DataFrame with SMILES column

## Outputs

- RDKit Mol objects with embedded 3D conformers
- Optimized conformer geometries (coordinates in Ångströms)
- Conformer IDs and MMFF optimization status codes

## How to apply

Load each molecule from SMILES using RDKit's MolFromSmiles() and add hydrogens with AddHs(). Configure ETKDGv3 parameters (randomSeed=-1, maxAttempts=1, numThreads=0, useRandomCoords=True) to control embedding reproducibility and conformer diversity. Call EmbedMultipleConfs() to generate the desired number of 3D conformations (typically 1 per molecule for CCS pipelines). Immediately optimize all generated conformers using MMFFOptimizeMoleculeConfs() with a force field (MMFF) to relax geometries to local minima. Verify success by confirming all returned conformers have valid 3D coordinates and optimization converged. Store optimized conformers in memory or serialize to SDF for downstream processing.

## Related tools

- **RDKit** (Performs 2D-to-3D coordinate embedding, conformer generation, hydrogen addition, and MMFF force field optimization) — https://rdkit.org/
- **ETKDGv3** (RDKit's distance geometry embedding algorithm optimized for macrocycles; configured with randomSeed and maxAttempts parameters to control conformer generation behavior) — https://www.rdkit.org/docs/source/rdkit.Chem.rdDistGeom.html
- **EmbedMultipleConfs** (RDKit function that generates multiple 3D conformations per molecule with specified parameters) — https://www.rdkit.org/docs/source/rdkit.Chem.rdDistGeom.html
- **MMFFOptimizeMoleculeConfs** (RDKit force field optimizer that refines all generated conformers to local energy minima using MMFF94 potential) — https://www.rdkit.org/docs/source/rdkit.Chem.rdForceFieldHelpers.html
- **Python 3** (Programming environment for RDKit scripting and conformer processing) — https://www.python.org/

## Examples

```
mol = Chem.MolFromSmiles('CCO'); mol = Chem.AddHs(mol); ps = AllChem.ETKDGv3(); ps.randomSeed = -1; AllChem.EmbedMultipleConfs(mol, numConfs=1, params=ps); AllChem.MMFFOptimizeMoleculeConfs(mol, numThreads=0)
```

## Evaluation signals

- All conformers possess valid 3D atomic coordinates (no NaN or inf values); dimensionality is (N_atoms, 3).
- MMFFOptimizeMoleculeConfs() returns optimization status code 0 (convergence) for all or ≥95% of conformers.
- Conformer structure remains chemically valid: bond connectivity unchanged, no atom collisions (inter-atomic distances > 0.8 Å), valence satisfied.
- Voxel-projected area calculations or subsequent CCS predictions execute without geometry errors; no singular covariance matrices or degenerate coordinate systems.
- Output conformer count matches numConfs parameter; each conformer has a unique ID (confId) in RDKit object.

## Limitations

- ETKDGv3 is optimized for macrocycles but may fail on highly strained or exotic cage scaffolds; fallback to alternative distance geometry methods may be required.
- Single-conformer generation (numConfs=1) with randomSeed=-1 produces non-reproducible results across runs; set randomSeed to a fixed integer if reproducibility is critical.
- MMFF94 force field has limited coverage of organometallics, some heteroatoms, and highly unusual bonding; molecules outside its parameterization may converge to unrealistic geometries.
- Conformer generation does not account for solvent effects, pH, or protonation state changes; input SMILES must be pre-prepared with correct protonation.
- Generated conformers are local energy minima, not global minima; ensemble-based CCS prediction requires multiple high-quality conformers per molecule, necessitating numConfs >> 1 and post-hoc selection or averaging.

## Evidence

- [readme] Generate 3D conformers of molecules using ETKDGv3, EmbedMultipleConfs, and MMFFOptimizeMoleculeConfs: "Generate 3D conformers of molecules. mol = Chem.MolFromSmiles(smiles) mol = Chem.AddHs(mol) ps = AllChem.ETKDGv3() ps.randomSeed = -1 ps.maxAttempts = 1 ps.numThreads = 0 ps.useRandomCoords = True re"
- [readme] ETKDGv3 returns an EmbedParameters object for the ETKDG method - version 3 (macrocycles): "ETKDGv3 returns an EmbedParameters object for the ETKDG method - version 3 (macrocycles)."
- [readme] EmbedMultipleConfs generates the 3D conformers of molecules: "EmbedMultipleConfs generates the 3D conformers of molecules."
- [readme] MMFFOptimizeMoleculeConfs optimizes the 3D conformers of molecules: "MMFFOptimizeMoleculeConfs optimizes the 3D conformers of molecules."
- [other] Use RDKit to generate molecular conformers from input structures: "Use RDKit to generate molecular conformers from input structures."
- [other] PACCS operates directly from molecular conformers to enable database generation: "PACCS is a Projected Area-based CCS prediction method that operates directly from molecular conformers to enable database generation"
