---
name: collision-cross-section-prediction
description: Use when you have molecular structures (SMILES or SDF format) and need to predict their collision cross sections for ion mobility mass spectrometry workflows, particularly when generating large-scale searchable CCS databases for compound identification and characterization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0154
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
  - PyG (PyTorch Geometric)
  - PACCS (github.com/yuxuanliao/PACCS)
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
  - build: coll_ccs_predictor_2_0_cq
    doi: 10.1021/acs.analchem.2c03491
    title: CCS Predictor 2.0
  - build: coll_mol2ccs_cq
    doi: 10.1186/s13321-024-00899-w
    title: mol2ccs
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

# collision-cross-section-prediction

## Summary

Predict collision cross section (CCS) values for molecular ions using a voxel projected area-based deep learning method (PACCS) applied to 3D molecular conformers. This skill enables rapid CCS database generation for mass spectrometry applications without experimental measurement.

## When to use

Use this skill when you have molecular structures (SMILES or SDF format) and need to predict their collision cross sections for ion mobility mass spectrometry workflows, particularly when generating large-scale searchable CCS databases for compound identification and characterization.

## When NOT to use

- Input is already experimental CCS measurements—use this for prediction only, not validation
- Molecular structures contain unparameterized elements or unusual bonding not covered by MMFF force field
- You need site-specific or conformer-dependent CCS predictions for multiple rotamers (PACCS generates one CCS per conformer; averaging across multiple conformers is required for comparison to experimental drift tube mobility data)

## Inputs

- SMILES strings or SDF molecular structures
- Adduct type annotations (e.g., [M+H]+, [M+Na]+)
- Pre-trained PACCS model weights (PyTorch checkpoint)

## Outputs

- Predicted CCS values (numeric, in units of Ų or Å²)
- Searchable CCS database (CSV or HDF5 format with molecular ID, CCS value, conformer metadata)
- Validation report confirming expected columns and numeric population

## How to apply

First, generate 3D conformers for input molecules using RDKit's ETKDGv3 embedding and MMFF optimization. Compute voxel-projected areas by distributing Fibonacci grid points over atomic spheres and projecting onto three coordinate planes (xy, xz, yz), then average the projections. Construct molecular graphs and one-hot encode adduct type. Feed the voxel projected area, molecular graph representation, adduct encoding, and computed m/z values into the pre-trained PACCS deep learning model (PyTorch/PyG) to obtain predicted CCS values. Aggregate predictions with molecular identifiers into a pandas DataFrame and export as CSV or HDF5 for rapid retrieval and validation.

## Related tools

- **RDKit** (Generate 3D molecular conformers using ETKDGv3 and MMFF optimization; construct molecular graphs) — https://rdkit.org/
- **PyTorch** (Backend for PACCS deep learning model inference) — https://pytorch.org/
- **PyG (PyTorch Geometric)** (Graph neural network representation for molecular structure encoding) — https://pytorch-geometric.readthedocs.io/en/latest/
- **pandas** (Aggregate and organize predicted CCS values with molecular identifiers into searchable table structure) — https://pandas.pydata.org/
- **NumPy** (Numerical computation for voxel projection and averaging) — https://numpy.org/
- **Jupyter Notebook** (Interactive execution environment for model training, CCS prediction, and database generation workflows) — https://jupyter.org/
- **PACCS (github.com/yuxuanliao/PACCS)** (Implements projected area-based CCS prediction method with VoxelProjectedArea.py, MZ.py, MolecularRepresentations.py, and Prediction.py modules) — https://github.com/yuxuanliao/PACCS

## Examples

```
from PACCS.Prediction import PACCS_predict; PACCS_predict(input_path='molecules.csv', model_path='PACCS_model.pt', output_path='predicted_CCS.csv')
```

## Evaluation signals

- Output CCS database file exists and contains expected columns: molecular ID, CCS value (numeric), conformer metadata, adduct type
- All rows in output table are populated with numeric CCS predictions; no NaN or null values in CCS column
- CCS values fall within expected physical range for the molecular weight and charge state (typically 100–300 Ų for small molecules in positive-ion mode)
- Predicted CCS values for test molecules show correlation with external experimental CCS datasets when available (e.g., compare against the provided external test set)
- Reproducibility check: re-running prediction on same input with same random seed produces identical CCS values

## Limitations

- PACCS relies on MMFF force field parameterization; molecules with non-standard or missing atom types may fail conformer generation or optimization
- Single conformer per input SMILES is generated by default; aggregation across multiple conformers needed to match experimental data from drift tube instruments that measure conformer ensembles
- Model predictions are only as good as the training dataset; external test set performance may degrade for adduct types or chemical families not well-represented in training data
- No changelog available in the repository to track model version changes or retraining history

## Evidence

- [readme] We developed a Projected Area-based CCS prediction method (PACCS) directly from molecular conformers: "We developed a Projected Area-based CCS prediction method (PACCS) directly from molecular conformers"
- [readme] PACCS supports users to generate large-scale and searchable CCS databases using the open-source Jupyter Notebook: "PACCS supports users to generate large-scale and searchable CCS databases using the open-source Jupyter Notebook"
- [readme] Using the Fibonacci grids approach to distribute points evenly over the surfaces of 3D atomic spheres. Projected on three coordinate planes (xy, xz, yz). Averaging.: "Using the Fibonacci grids approach to distribute points evenly over the surfaces of 3D atomic spheres. Projected on three coordinate planes (xy, xz, yz). Averaging."
- [readme] EmbedMultipleConfs generates the 3D conformers of molecules. MMFFOptimizeMoleculeConfs optimizes the 3D conformers of molecules.: "EmbedMultipleConfs generates the 3D conformers of molecules. MMFFOptimizeMoleculeConfs optimizes the 3D conformers of molecules."
- [readme] The predicted CCS values of molecules are obtained by feeding the voxel projected area, molecular graph, one-hot encoding of adduct type, and m/z into the already trained PACCS model: "The predicted CCS values of molecules are obtained by feeding the voxel projected area, molecular graph, one-hot encoding of adduct type, and m/z into the already trained PACCS model"
- [other] Prepare input molecular structures in a supported format (e.g., SMILES or SDF) as a pandas DataFrame: "Prepare input molecular structures in a supported format (e.g., SMILES or SDF) as a pandas DataFrame"
- [other] Aggregate and organize predictions with molecular identifiers using pandas into a searchable table structure. Export the CCS database as a structured file (CSV or HDF5 format): "Aggregate and organize predictions with molecular identifiers using pandas into a searchable table structure. Export the CCS database as a structured file (CSV or HDF5 format)"
- [other] verify database file exists, contains expected columns (molecular ID, CCS value, conformer metadata), and all rows are populated with numeric CCS predictions: "verify database file exists, contains expected columns (molecular ID, CCS value, conformer metadata), and all rows are populated with numeric CCS predictions"
