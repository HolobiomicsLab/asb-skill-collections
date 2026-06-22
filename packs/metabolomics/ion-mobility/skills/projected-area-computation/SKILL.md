---
name: projected-area-computation
description: Use when you have 3D optimized molecular conformers (RDKit mol objects or SDF files) and need to extract shape-based features for collision cross section prediction, graph neural network input, or conformer comparison.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0250
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0081
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
  - VoxelProjectedArea.py
  - MZ.py
  - MolecularRepresentations.py
  techniques:
  - ion-mobility-MS
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

# projected-area-computation

## Summary

Compute voxel-projected area features from 3D molecular conformers using Fibonacci grid sampling and coordinate plane projections. This is a critical input featurization step for deep-learning CCS prediction, where projected area encodes molecular shape and cross-sectional geometry.

## When to use

You have 3D optimized molecular conformers (RDKit mol objects or SDF files) and need to extract shape-based features for collision cross section prediction, graph neural network input, or conformer comparison. Use this when the input molecules have already been embedded to 3D coordinates and force-field optimized, and you are preparing data for PACCS model training or inference.

## When NOT to use

- Input is a 2D SMILES or mol graph without 3D coordinates — conformer generation and optimization must precede this skill.
- Molecules are already represented as pre-computed feature tensors or neural embeddings — projected area computation is redundant.
- Use case requires all-atoms surface area or solvent-accessible surface area instead of projected area — different geometric models.

## Inputs

- RDKit mol object with 3D conformer embedded and force-field optimized
- Molecular conformer in SDF format
- SMILES string (must be converted to 3D conformer first via ETKDGv3 + MMFF optimization)

## Outputs

- Scalar projected area value (float, in Ų units)
- Projected area vector [area_xy, area_xz, area_yz] before averaging
- Feature tensor ready for concatenation with m/z, graph, and adduct encoding

## How to apply

Load each molecular conformer and apply the voxel projected area algorithm: (1) distribute points evenly over 3D atomic van der Waals surfaces using Fibonacci grid sampling; (2) project these point clouds orthogonally onto three coordinate planes (xy, xz, yz); (3) compute the occupied area on each plane; (4) average the three plane areas to obtain a single scalar projected area value per conformer. The method is implemented in VoxelProjectedArea.py and operates directly on RDKit mol objects. This scalar feature is then combined with m/z (from MZ.py), molecular graph encoding (from MolecularRepresentations.py), and adduct one-hot encoding to form the complete input tensor for the PACCS neural network.

## Related tools

- **RDKit** (Load and manipulate 3D molecular conformers; provide mol objects and atomic coordinate access for voxel distribution and projection) — https://rdkit.org/
- **VoxelProjectedArea.py** (Core implementation of Fibonacci grid sampling, plane projection, and area aggregation; called for each conformer) — https://github.com/yuxuanliao/PACCS
- **NumPy** (Numerical computation of Fibonacci grid points, orthogonal projections onto xy/xz/yz planes, and area averaging) — https://numpy.org/
- **MZ.py** (Sibling module to compute mass-to-charge ratio; projected area is concatenated with m/z for model input) — https://github.com/yuxuanliao/PACCS
- **MolecularRepresentations.py** (Sibling module to construct molecular graph; projected area is concatenated with graph encoding for model input) — https://github.com/yuxuanliao/PACCS

## Examples

```
from PACCS.VoxelProjectedArea import compute_projected_area
from rdkit import Chem
from rdkit.Chem import AllChem

mol = Chem.MolFromSmiles('CCO')
mol = Chem.AddHs(mol)
ps = AllChem.ETKDGv3()
AllChem.EmbedMultipleConfs(mol, numConfs=1, params=ps)
AllChem.MMFFOptimizeMoleculeConfs(mol, numThreads=0)
projected_area = compute_projected_area(mol, confId=0)
```

## Evaluation signals

- Projected area scalar is a positive float > 0; typical range ~50–500 Ų for organic molecules.
- Three intermediate plane areas (xy, xz, yz) are computed and their average equals the final scalar output.
- Projected area remains invariant under conformer reorientation (rotation and translation do not change geometric projection).
- Conformer with larger van der Waals radius or more extended shape yields larger projected area than compact conformer of same molecule.
- Output tensor can be successfully concatenated with m/z and graph features without shape mismatch (scalar appends to feature vector).

## Limitations

- Accuracy depends on accurate 3D conformer generation and force-field optimization beforehand; garbage-in-garbage-out.
- Fibonacci grid resolution (number of surface points sampled per atom) is a hidden hyperparameter; insufficient sampling may undersample concave or intricate surfaces.
- Projected area is orientation-invariant but does not capture directional anisotropy or asymmetry in shape; symmetric molecules with different 3D shapes may yield identical projected areas.
- Method assumes van der Waals radii are accurately defined in RDKit; anomalous or heavy-metal atoms may have poor or absent radii.
- Single conformer per molecule loses ensemble effects; if multiple conformers exist, projected area should be computed per conformer and aggregated or selected carefully.

## Evidence

- [readme] PACCS calculates the projected area with the voxel-based approach: "PACCS calculates the projected area with the voxel-based approach, computes the m/z, and constructs the molecular graph."
- [readme] Using Fibonacci grids and projection on three coordinate planes: "Using the Fibonacci grids approach to distribute points evenly over the surfaces of 3D atomic spheres. Projected on three coordinate planes (xy, xz, yz). Averaging."
- [readme] PACCS is a Projected Area-based CCS prediction method: "We developed a Projected Area-based CCS prediction method (PACCS) directly from molecular conformers."
- [readme] Voxel projected area features are core inputs to the deep-learning model: "The predicted CCS values of molecules are obtained by feeding the voxel projected area, molecular graph, one-hot encoding of adduct type, and m/z into the already trained PACCS model"
- [readme] Conformers must be 3D-embedded and force-field optimized first: "MMFFOptimizeMoleculeConfs optimizes the 3D conformers of molecules."
