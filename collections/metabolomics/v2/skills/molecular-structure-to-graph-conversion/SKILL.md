---
name: molecular-structure-to-graph-conversion
description: Use when when you have validated RDKit molecule objects from chemical databases (PubChem, HMDB) and need to generate graph-structured features for machine learning models that consume molecular topology as input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0379
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  tools:
  - RDKit 2020.03.4
  - RDKit
  - numpy
  - pandas
  - scikit-learn
derived_from:
- doi: 10.1007/s10489-022-04351-0
  title: Mass Spectrum Transformer
evidence_spans:
- RDKit == 2020.03.4
- numpy == 1.19.1
- implicit in data.csv loading requirement
- scikit-learn == 0.23.2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnn_rt_cq
    doi: 10.1021/acs.analchem.0c04071
    title: GNN-RT
  - build: coll_mass_spectrum_transformer_cq
    doi: 10.1007/s10489-022-04351-0
    title: Mass Spectrum Transformer
  dedup_kept_from: coll_mass_spectrum_transformer_cq
schema_version: 0.2.0
---

# molecular-structure-to-graph-conversion

## Summary

Convert RDKit molecule objects derived from PubChem/HMDB IDs into graph-based feature representations (node and edge tensors) suitable for neural network training. This skill bridges molecular structure validation and downstream multimodal feature alignment by extracting topology and connectivity information.

## When to use

When you have validated RDKit molecule objects from chemical databases (PubChem, HMDB) and need to generate graph-structured features for machine learning models that consume molecular topology as input. Use this skill if your training pipeline requires node-edge tensor representations alongside other modalities (fingerprints, descriptors).

## When NOT to use

- Input molecule structures are already represented as pre-computed adjacency matrices or graph embeddings.
- Your analysis goal requires only 1D molecular summaries (fingerprints, descriptors) and does not need topology information.
- Molecule objects are invalid or cannot be parsed by RDKit (structural integrity check has failed).

## Inputs

- RDKit molecule objects (validated molecular structures)
- PubChem or HMDB molecule identifiers (as strings or integers)
- data.csv (CSV file containing molecule IDs and metadata)

## Outputs

- Node feature tensors (atom-level properties and embeddings)
- Edge feature tensors (bond-level connectivity and properties)
- Aligned graph tensor pair suitable for GNN input
- Serialized graph features (HDF5 or pickle format)

## How to apply

After loading and validating molecule IDs from data.csv and converting each to a RDKit molecule object, extract node features (atom properties) and edge features (bond connectivity) from the molecular structure graph. Use RDKit's graph traversal and property accessor methods to construct adjacency and feature matrices. Stack the resulting node and edge tensors into aligned numpy arrays that preserve molecule identity and can be serialized (HDF5 or pickle) alongside other modality tensors. Verify that tensor dimensions match the number of atoms and bonds in each molecule and that sparse representations (if used) preserve graph connectivity.

## Related tools

- **RDKit** (Molecular structure parsing, graph construction, and feature extraction from validated molecule objects)
- **numpy** (Tensor creation, stacking, and alignment of node-edge feature matrices into aligned multimodal arrays)
- **pandas** (Loading and indexing molecule metadata from data.csv for batch processing)

## Examples

```
# In data_prep.py: mol = Chem.MolFromSmiles(smiles); nodes, edges = extract_graph_features(mol); graph_tensor = np.stack([nodes, edges])
```

## Evaluation signals

- Node tensor shape matches total atom count per molecule; edge tensor shape matches total bond count.
- All nodes are assigned valid atom features (atomic number, charge, hybridization); all edges reference valid atom pairs.
- Graph connectivity is preserved: edge indices refer to valid node indices and reflect the molecular structure.
- Tensor dimensions and dtypes are consistent across the batch and serializable without loss of precision.
- Downstream GNN model accepts graph tensors without reshape errors and produces valid node/graph-level embeddings.

## Limitations

- RDKit version pinned to 2020.03.4; newer versions may change graph API or feature definitions.
- Molecules with unusual valence states or incomplete structure records may fail graph construction or produce sparse/malformed tensors.
- No handling documented for molecules with disconnected components; multi-component graphs may require custom handling.
- Graph representation is static and does not encode conformational or stereochemical variations beyond 2D connectivity.

## Evidence

- [other] Convert each molecule ID to a RDKit molecule object and validate structural integrity.: "Convert each molecule ID to a RDKit molecule object and validate structural integrity."
- [other] Generate graph-based features (node and edge tensors) from molecular structures using RDKit.: "Generate graph-based features (node and edge tensors) from molecular structures using RDKit."
- [other] Stack graph, fingerprint, and descriptor modalities into aligned multimodal feature tensors using numpy.: "Stack graph, fingerprint, and descriptor modalities into aligned multimodal feature tensors using numpy."
- [readme] the process of multimodal dataset production is in data_prep.py: "the process of multimodal dataset production is in data_prep.py"
