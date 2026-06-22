---
name: molecular-conformer-preprocessing
description: Use when you have a set of molecular SMILES strings and need to prepare them as inputs to a deep-learning CCS prediction model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0428
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - Python 3
  - RDKit
  - PyTorch
  - PyG
  - pandas
  - NumPy
  - conda
  - pip
  - PyTorch Geometric (PyG)
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1002/cem.70040
  title: PACCS
evidence_spans:
- '[python3](https://www.python.org/)'
- '[RDKit](https://rdkit.org/)'
- '[PyTorch](https://pytorch.org/)'
- '[PyG](https://pytorch-geometric.readthedocs.io/en/latest/)'
- '[pandas](https://pandas.pydata.org/)'
- '[NumPy](https://numpy.org/)'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-conformer-preprocessing

## Summary

Generate and optimize 3D molecular conformers from SMILES strings, then compute voxel-projected area features for use in machine-learning-based collision cross section prediction. This skill prepares molecular geometry and structural descriptors that serve as direct inputs to neural network models.

## When to use

You have a set of molecular SMILES strings and need to prepare them as inputs to a deep-learning CCS prediction model. Specifically, when you require 3D conformer geometries, voxel-projected area features computed across three coordinate planes (xy, xz, yz), and molecular graph representations before training or inference with a PyTorch-based model.

## When NOT to use

- Input molecules already have precomputed 3D conformers from another source and you only need to extract features from fixed geometries — use feature extraction directly instead.
- You are working with 2D molecular structures only and have no need for 3D geometric descriptors or collision cross section prediction.
- The molecular dataset is extremely large (>10^6 molecules) and conformer generation time is prohibitive — consider using pre-generated conformer databases or approximate methods.

## Inputs

- SMILES strings (one per molecule)
- adduct type labels (e.g., [M+H]+, [M-H]-)
- ground-truth CCS values (for training/validation data)

## Outputs

- 3D molecular conformers (RDKit Mol objects with 3D coordinates)
- voxel-projected area feature vectors (averaged across xy, xz, yz planes)
- molecular graph representations (PyG Data objects)
- m/z values (mass-to-charge ratios)
- one-hot encoded adduct type labels
- training, validation, and test datasets (pandas DataFrames with 8:1:1 split)

## How to apply

First, convert SMILES strings to RDKit molecule objects, add explicit hydrogens, and generate 3D conformers using RDKit's ETKDGv3 embedding algorithm with force-field optimization (MMFF) to produce physically realistic geometries. Next, compute voxel-projected area features by distributing points evenly over atomic sphere surfaces using a Fibonacci grid approach, projecting onto three orthogonal coordinate planes, and averaging the results. Simultaneously construct molecular graphs (as PyG Data objects) and compute m/z values. Organize all features and ground-truth CCS labels into a pandas DataFrame, splitting into training (80%), validation (10%), and test (10%) sets. This preprocessing ensures the model receives normalized, geometrically sound molecular descriptors rather than raw SMILES.

## Related tools

- **RDKit** (Generate 3D conformers from SMILES, optimize geometries with MMFF force field, and construct molecular graphs) — https://rdkit.org/
- **PyTorch Geometric (PyG)** (Represent molecules as graph objects (Data) for downstream neural network message passing) — https://pytorch-geometric.readthedocs.io/en/latest/
- **pandas** (Organize preprocessed features, labels, and metadata into DataFrames for training/validation/test split) — https://pandas.pydata.org/
- **NumPy** (Perform numerical operations on voxel-projected area arrays and feature normalization) — https://numpy.org/
- **Python 3** (Orchestrate conformer generation, feature computation, and dataset preparation workflows) — https://www.python.org/

## Examples

```
mol = Chem.MolFromSmiles(smiles); mol = Chem.AddHs(mol); ps = AllChem.ETKDGv3(); ps.randomSeed = -1; AllChem.EmbedMultipleConfs(mol, numConfs=1, params=ps); AllChem.MMFFOptimizeMoleculeConfs(mol)
```

## Evaluation signals

- All SMILES strings successfully convert to RDKit Mol objects with 3D coordinates and no failed embeds (check EmbedMultipleConfs return code).
- Voxel-projected area features are computed for all three orthogonal planes (xy, xz, yz) and averaged to produce a single scalar per molecule.
- Molecular conformer geometries pass energy minimization (MMFF optimization converges and produces no NaN coordinates).
- Training, validation, and test datasets have correct 8:1:1 size ratio and no leakage of molecules between splits.
- All feature vectors and labels align by row in the output DataFrame, with no missing or mismatched entries.

## Limitations

- Conformer generation may fail or produce suboptimal geometries for macrocycles or highly constrained molecules; ETKDGv3 is designed for macrocycles but may still struggle with unusual topologies.
- Voxel-projected area features assume molecular flexibility can be captured by a single conformer; molecules with multiple low-energy conformational states may require ensemble averaging.
- Force-field optimization (MMFF) may not converge for all molecules, particularly those with unusual valence states or nonstandard atom types.
- The method is sensitive to 3D coordinate generation randomness; setting ps.randomSeed = -1 allows variation; reproducibility requires fixed random seeds.

## Evidence

- [readme] Generate 3D conformers of molecules using ETKDGv3 and MMFF optimization: "Generate 3D conformers of molecules... [ETKDGv3](https://www.rdkit.org/docs/source/rdkit.Chem.rdDistGeom.html?highlight=etkdgv3#rdkit.Chem.rdDistGeom.ETKDGv3) returns an EmbedParameters object for"
- [readme] Voxel projected area computation and feature calculation: "Using the Fibonacci grids approach to distribute points evenly over the surfaces of 3D atomic spheres. Projected on three coordinate planes (xy, xz, yz). Averaging."
- [readme] Data preprocessing produces features for model training: "PACCS calculates the projected area with the voxel-based approach, computes the m/z, and constructs the molecular graph."
- [readme] Dataset split for training and evaluation: "The curated dataset is randomly split into the training, validation, and test sets in a ratio of 8:1:1."
- [other] Input organization for model training: "Prepare training, validation, and test datasets using pandas and NumPy, organizing features and corresponding CCS ground-truth labels."
