---
name: molecular-descriptor-indexing
description: Use when when you have a collection of molecular structures (SMILES or SDF format) and need to generate a queryable database of collision cross section values for high-throughput mass spectrometry workflows, or when you want to organize pre-computed CCS predictions with conformer metadata into a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3370
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
  - PACCS
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

# molecular-descriptor-indexing

## Summary

Build searchable, large-scale CCS (collision cross section) databases by computing projected-area-based molecular descriptors from conformers and organizing them with molecular identifiers into indexed, retrieval-optimized structures (CSV/HDF5). This skill enables rapid lookup and validation of predicted collision cross sections for mass spectrometry applications.

## When to use

When you have a collection of molecular structures (SMILES or SDF format) and need to generate a queryable database of collision cross section values for high-throughput mass spectrometry workflows, or when you want to organize pre-computed CCS predictions with conformer metadata into a structure that supports fast retrieval by molecular ID.

## When NOT to use

- Input structures are already 2D or lack stereochemistry information — PACCS requires valid 3D conformers with optimized geometry.
- You need CCS values for species not represented in the training dataset (e.g., post-translational modifications outside the training adduct set) — performance degrades on out-of-domain molecules.
- Database already exists and is populated — this skill generates a new database; use retrieval/query skills instead.

## Inputs

- Molecular structures as SMILES strings or SDF file
- pandas DataFrame with column(s) containing SMILES and adduct type
- Trained PACCS PyTorch model checkpoint

## Outputs

- Searchable CCS database (CSV or HDF5 file)
- Table with columns: molecular ID, CCS value, conformer metadata, m/z
- Indexed structure enabling key-based retrieval by molecular identifier

## How to apply

Load molecular structures into a pandas DataFrame and generate 3D conformers using RDKit's ETKDGv3 and EmbedMultipleConfs methods. Apply the PACCS projected-area-based CCS prediction method (which computes voxel projected areas on xy, xz, and yz planes and feeds them into a trained deep learning model) to each conformer to obtain numeric CCS values. Aggregate predictions with molecular identifiers, conformer metadata, and m/z values using pandas, ensuring all rows contain populated numeric CCS predictions. Export the resulting table to CSV or HDF5 format with indexed columns (molecular ID, CCS value, conformer metadata) to enable rapid key-based retrieval. Validation: verify the output file exists, contains the expected columns with no nulls in numeric fields, and spot-check a sample of CCS values for plausibility against the external test set.

## Related tools

- **RDKit** (Generate 3D molecular conformers from SMILES using ETKDGv3 and EmbedMultipleConfs; optimize conformer geometry with MMFF force field) — https://rdkit.org/
- **pandas** (Load input structures, aggregate CCS predictions with molecular IDs and metadata, and export indexed tables) — https://pandas.pydata.org/
- **PyTorch** (Load and execute the trained PACCS deep learning model for CCS prediction from voxel projected areas and molecular graphs) — https://pytorch.org/
- **PyG (PyTorch Geometric)** (Construct and represent molecular graphs as input features to the PACCS neural network) — https://pytorch-geometric.readthedocs.io/en/latest/
- **Jupyter Notebook** (Interactive execution environment for database generation; PACCS repository provides example notebook (database generation.ipynb) to customize and generate large-scale CCS databases) — https://github.com/yuxuanliao/PACCS
- **PACCS** (Core method: computes voxel projected area (Fibonacci grids on three coordinate planes), encodes adduct and m/z, and predicts CCS values via trained model) — https://github.com/yuxuanliao/PACCS

## Examples

```
from PACCS.Prediction import PACCS_predict; PACCS_predict(input_path='molecules.csv', model_path='trained_model.pth', output_path='CCS_database.csv')
```

## Evaluation signals

- Output file exists and is readable as a valid CSV or HDF5 with correct schema (columns: molecular_id, CCS, conformer_metadata, m/z)
- All rows contain numeric CCS predictions; no null or NaN values in prediction columns
- Molecular identifiers are unique and correctly indexed for fast retrieval by key
- Spot-check: sample CCS values fall within expected physical range and align with curated or external test set for structurally similar molecules
- Index keys enable O(1) or O(log n) lookup by molecular ID, confirmed by querying the database with a known molecular identifier

## Limitations

- PACCS performance is limited to molecules and adduct types represented in the training set; prediction accuracy degrades for novel chemical scaffolds or unencountered adducts.
- 3D conformer generation via RDKit's ETKDGv3 may fail for highly strained or complex macrocyclic molecules; single conformer per molecule is used by default in the README example, potentially underrepresenting conformational heterogeneity.
- CCS prediction accuracy depends on the quality of the input molecular structure (valence, aromaticity, stereochemistry); invalid SMILES will cause pipeline failure.
- No changelog provided in the repository; version tracking and reproducibility across different PACCS repository snapshots is unclear.

## Evidence

- [readme] PACCS supports users to generate large-scale and searchable CCS databases using the open-source Jupyter Notebook: "PACCS supports users to generate large-scale and searchable CCS databases using the open-source Jupyter Notebook"
- [other] Aggregate and organize predictions with molecular identifiers using pandas into a searchable table structure; export the CCS database as a structured file (CSV or HDF5 format) with index columns for rapid retrieval.: "Aggregate and organize predictions with molecular identifiers using pandas into a searchable table structure. 6. Export the CCS database as a structured file (CSV or HDF5 format) with index columns"
- [readme] PACCS calculates the projected area with the voxel-based approach, computes the m/z, and constructs the molecular graph.: "PACCS calculates the projected area with the voxel-based approach, computes the m/z, and constructs the molecular graph"
- [readme] Using the Fibonacci grids approach to distribute points evenly over the surfaces of 3D atomic spheres. Projected on three coordinate planes (xy, xz, yz). Averaging.: "Using the Fibonacci grids approach to distribute points evenly over the surfaces of 3D atomic spheres. Projected on three coordinate planes (xy, xz, yz). Averaging."
- [other] verification: verify database file exists, contains expected columns (molecular ID, CCS value, conformer metadata), and all rows are populated with numeric CCS predictions: "verify database file exists, contains expected columns (molecular ID, CCS value, conformer metadata), and all rows are populated with numeric CCS predictions"
