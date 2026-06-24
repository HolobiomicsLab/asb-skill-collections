---
name: large-scale-database-construction
description: Use when you have a collection of molecular structures (as SMILES or
  SDF files) and need to generate pre-computed CCS values for fast retrieval in downstream
  mass spectrometry workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2258
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
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# large-scale-database-construction

## Summary

Construct searchable, indexed collision cross section (CCS) databases from molecular structures by applying the PACCS projected-area-based prediction method to molecular conformers in batch, aggregating results into a structured table, and exporting as a retrievable file format (CSV or HDF5). This skill enables rapid deployment of CCS lookup tables for mass spectrometry applications without manual computation.

## When to use

You have a collection of molecular structures (as SMILES or SDF files) and need to generate pre-computed CCS values for fast retrieval in downstream mass spectrometry workflows. Use this skill when you require a static, indexed database rather than real-time prediction, or when you must validate CCS predictions across a large, diverse chemical space for benchmarking or method comparison.

## When NOT to use

- Input molecules already have experimental CCS measurements — use validation/comparison workflows instead of generation.
- Structures are highly unusual (extreme molecular weight, macrocycles with unoptimized geometry) — conformer generation may fail or produce invalid 3D coordinates.
- Real-time, single-molecule prediction is required — pre-computed database lookup is slower than on-demand inference for isolated queries.

## Inputs

- Pandas DataFrame with SMILES strings or SDF file paths
- Molecular structures in SMILES or SDF format
- Adduct type annotations (e.g., +H, +Na, -H)

## Outputs

- Indexed CCS database in CSV or HDF5 format
- Table with columns: molecular ID, CCS value, conformer metadata
- Searchable lookup table with numeric CCS predictions

## How to apply

Begin by preparing input molecular structures as a pandas DataFrame with SMILES or SDF columns. Use RDKit to generate 3D conformers from each structure via ETKDGv3 embedding and MMFF optimization. Apply the PACCS voxel projected-area method (from VoxelProjectedArea.py) to compute CCS values for each conformer, feeding the projected area, molecular graph representation, adduct type encoding, and m/z into the trained PACCS PyTorch model. Aggregate predictions into a pandas DataFrame with molecular identifiers, CCS values, and conformer metadata as separate columns. Export the structured table to CSV or HDF5 format with an index column (e.g., SMILES or compound ID) to enable rapid random-access retrieval. Validation: confirm the output file exists, verify all expected columns are present and non-null, ensure CCS values fall within physically plausible ranges (typically 50–300 Ų for small molecules), and spot-check a sample of rows against expected conformer metadata.

## Related tools

- **RDKit** (Generate 3D molecular conformers via ETKDGv3 embedding and MMFF optimization; construct molecular graph representations) — https://rdkit.org/
- **pandas** (Aggregate CCS predictions with molecular identifiers into a structured DataFrame; organize predictions with index columns for retrieval) — https://pandas.pydata.org/
- **PyTorch** (Load and execute the trained PACCS neural network model for CCS prediction from voxel projected area and molecular graph inputs) — https://pytorch.org/
- **PyG (PyTorch Geometric)** (Represent and process molecular graphs as graph neural network inputs during CCS prediction) — https://pytorch-geometric.readthedocs.io/en/latest/
- **PACCS** (Compute voxel projected area, encode adduct type, calculate m/z, and predict CCS values for each molecular conformer) — https://github.com/yuxuanliao/PACCS
- **Jupyter Notebook** (Execute the database generation workflow interactively; provided example notebook (database generation.ipynb) implements the full pipeline) — https://github.com/yuxuanliao/PACCS

## Evaluation signals

- Output file exists and is readable (CSV or HDF5 format validates against expected schema)
- All rows in the output table contain non-null numeric CCS values; no rows with NaN or infinity
- Column count matches expected structure: molecular ID, CCS value, and conformer metadata are all present
- CCS values fall within physically plausible range (spot-check: typical small molecules 50–300 Ų; validate against external test set if available)
- Index column is unique and matches input molecular identifiers; random-access retrieval by ID returns correct row without error

## Limitations

- Conformer generation via ETKDGv3 and MMFF may fail for highly constrained or macrocyclic structures, resulting in omitted entries in the database.
- PACCS CCS predictions are trained on curated datasets; performance on chemically divergent molecules or adducts outside the training distribution is not guaranteed.
- Voxel projected-area method assumes isotropic molecular geometry; highly flexible or highly charged species may have reduced accuracy.
- Database export to CSV or HDF5 requires sufficient disk space for large chemical libraries (millions of molecules); HDF5 is recommended for very large databases.

## Evidence

- [intro] PACCS supports users to generate large-scale and searchable CCS databases using the open-source Jupyter Notebook: "PACCS supports users to generate large-scale and searchable CCS databases using the open-source Jupyter Notebook"
- [other] Prepare input molecular structures in a supported format (e.g., SMILES or SDF) as a pandas DataFrame: "Prepare input molecular structures in a supported format (e.g., SMILES or SDF) as a pandas DataFrame"
- [other] Apply the PACCS projected-area-based CCS prediction method to compute collision cross sections for each conformer: "Apply the PACCS projected-area-based CCS prediction method to compute collision cross sections for each conformer"
- [other] Aggregate and organize predictions with molecular identifiers using pandas into a searchable table structure: "Aggregate and organize predictions with molecular identifiers using pandas into a searchable table structure"
- [other] Export the CCS database as a structured file (CSV or HDF5 format) with index columns for rapid retrieval: "Export the CCS database as a structured file (CSV or HDF5 format) with index columns for rapid retrieval"
- [other] verify database file exists, contains expected columns (molecular ID, CCS value, conformer metadata), and all rows are populated with numeric CCS predictions: "verify database file exists, contains expected columns (molecular ID, CCS value, conformer metadata), and all rows are populated with numeric CCS predictions"
- [readme] The example code for generating large-scale CCS databases by PACCS is included in the [database generation.ipynb](database%20generation/database%20generation.ipynb). By directly running [database generation.ipynb](database%20generation/database%20generation.ipynb), users can easily customize and generate their large-scale CCS databases: "users can easily customize and generate their large-scale CCS databases by PACCS based on their practical needs"
