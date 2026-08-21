---
name: pytorch-graph-serialization
description: Use when you have constructed molecular graphs with atom features (atomic
  number, degree, formal charge, hybridization) and bond features (bond type, aromaticity)
  from SMILES or MOL files using RDKit, and need to feed them into a PyTorch-based
  GNN training pipeline without memory overhead or I/O.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0209
  tools:
  - PyTorch
  - Python
  - RDKit
  - Python pickle module
  - HDF5 (h5py)
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c04071
  title: GNN-RT
evidence_spans:
- conda install pytorch
- Anaconda for python 3.6
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnn_rt_cq
    doi: 10.1021/acs.analchem.0c04071
    title: GNN-RT
  dedup_kept_from: coll_gnn_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c04071
  all_source_dois:
  - 10.1021/acs.analchem.0c04071
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# PyTorch Graph Serialization for GNN Input

## Summary

Serialize molecular graph representations into PyTorch-compatible formats (pickle or HDF5) to enable efficient consumption by Graph Neural Network training pipelines. This skill bridges the gap between RDKit molecular graph construction and PyTorch DataLoader ingestion for retention time prediction models.

## When to use

You have constructed molecular graphs with atom features (atomic number, degree, formal charge, hybridization) and bond features (bond type, aromaticity) from SMILES or MOL files using RDKit, and need to feed them into a PyTorch-based GNN training pipeline without memory overhead or I/O bottlenecks during model training and transfer learning phases.

## When NOT to use

- Input is already in PyTorch Tensor or graph object format (Data or HeteroData from PyG)
- Molecular graphs are extremely large (>10 million atoms per structure) and serialization overhead exceeds memory savings
- Training pipeline expects streaming/online data augmentation rather than pre-serialized static batches

## Inputs

- Molecular graphs with node-edge representations (constructed via RDKit)
- Atom feature arrays (atomic number, degree, formal charge, hybridization)
- Bond feature arrays (bond type, aromaticity)
- SMILES or MOL format structure files from in-house database

## Outputs

- Serialized molecular graphs in pickle format
- Serialized molecular graphs in HDF5 format
- PyTorch-compatible graph batches ready for DataLoader consumption

## How to apply

After converting molecular structures into node-edge representations using RDKit's graph construction methods, serialize the molecular graphs into pickle or HDF5 format to create a format compatible with PyTorch's DataLoader. The serialized graphs should retain all atom and bond feature attributes computed during the RDKit preprocessing stage. Store serialized graphs in a structured directory (e.g., the 'data' directory) that the PyTorch training pipeline can discover and batch-load during Train.py and Transferlearning.py execution. Verify serialization by confirming file sizes are reasonable relative to the number of molecules and that DataLoader can iterate over batches without deserialization errors.

## Related tools

- **RDKit** (Construct molecular graphs with atom/bond features before serialization) — https://www.rdkit.org/
- **PyTorch** (Load and batch-iterate over serialized graphs via DataLoader) — https://pytorch.org/
- **Python pickle module** (Serialize graph objects into binary format)
- **HDF5 (h5py)** (Alternative serialization format for large-scale graph storage)

## Examples

```
python Preprocess.py  # converts SMILES/MOL files to serialized molecular graphs in data/ directory for consumption by PyTorch DataLoader in Train.py
```

## Evaluation signals

- Serialized files are created and readable by Python pickle or h5py without errors
- PyTorch DataLoader successfully iterates over batches of deserialized graphs without shape or type mismatches
- Graph features (atom features, bond features) are preserved after deserialization and match the original RDKit-constructed representations
- Training pipeline (Train.py, Transferlearning.py) runs without I/O bottlenecks or out-of-memory errors when loading batches
- File sizes scale linearly with the number of molecules and average molecular complexity

## Limitations

- Serialization format choice (pickle vs HDF5) affects compatibility across Python versions and platforms; pickle is Python-specific
- Large molecular datasets may require substantial disk space; pre-serialization requires estimating storage and I/O bandwidth
- Graph serialization assumes fixed schema; heterogeneous graph structures or variable feature dimensions may require custom serialization logic
- No changelog or versioning support noted in repository, making it unclear how serialized graphs from older versions interact with updated GNN-RT code

## Evidence

- [other] Serialize the molecular graphs into a format compatible with PyTorch's DataLoader (e.g., pickle or HDF5) for consumption by the GNN training pipeline.: "Serialize the molecular graphs into a format compatible with PyTorch's DataLoader (e.g., pickle or HDF5)"
- [other] Construct molecular graphs by converting each structure into a node-edge representation with atom features (atomic number, degree, formal charge, hybridization) and bond features (bond type, aromaticity) using RDKit's graph construction methods.: "Construct molecular graphs by converting each structure into a node-edge representation with atom features (atomic number, degree, formal charge, hybridization) and bond features (bond type,"
- [readme] It takes molecular graph as the input, and the predicted retention time as the output.: "It takes molecular graph as the input, and the predicted retention time as the output."
- [readme] put your spectra files in to data directory and run [Preprocess.py], [Train.py] and [Transferlearning.py]: "put your spectra files in to data directory and run [Preprocess.py], [Train.py] and [Transferlearning.py]"
