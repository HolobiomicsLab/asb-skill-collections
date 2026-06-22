---
name: molecular-graph-representation-encoding
description: Use when when you have a collection of molecular structures (as InChI strings, SMILES, or RDKit Mol objects) and need to feed them into a pretrained or transfer-learning neural network that expects both molecular graph topology and structural fingerprints as inputs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3364
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3372
  tools:
  - Python
  - torch
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - scikit-learn
  - tqdm
  - rdkit-pypi
  - torch_geometric
  - torch-scatter, torch-sparse, torch-cluster
  - pandas
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
evidence_spans:
- Python 3.9
- torch
- torch-scatter
- torch-sparse
- torch-cluster
- scikit-learn
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_retention_time_gnn_cq
    doi: 10.1021/acs.analchem.3c03177
    title: retention_time_gnn
  - build: coll_rt_transformer_cq
    doi: 10.1093/bioinformatics/btae084
    title: RT-Transformer
  dedup_kept_from: coll_rt_transformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae084
  all_source_dois:
  - 10.1093/bioinformatics/btae084
  - 10.1038/s41467-019-13680-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-graph-representation-encoding

## Summary

Encodes molecular structures as graph representations and fingerprints for input to neural network models predicting molecular properties (e.g., retention time). This skill transforms unstructured chemical data (InChI, SMILES, or molecular objects) into tensor-compatible graph and fingerprint features suitable for graph convolution and transformer architectures.

## When to use

When you have a collection of molecular structures (as InChI strings, SMILES, or RDKit Mol objects) and need to feed them into a pretrained or transfer-learning neural network that expects both molecular graph topology and structural fingerprints as inputs. Specifically apply this skill when preparing data for retention time prediction models like RT-Transformer or when adapting a pretrained model to a new chromatographic dataset.

## When NOT to use

- Input molecules are already pre-encoded as fixed-size numerical feature tables or pre-computed embeddings; re-encoding is redundant.
- The neural network architecture does not use graph convolutions or fingerprint features (e.g., it expects raw SMILES strings to be processed by an embedded tokenizer).
- Molecular structures are missing or malformed (invalid InChI/SMILES); encoding will fail or produce null tensors.

## Inputs

- CSV file with 'InChI' and/or 'SMILES' columns and experimental property values (e.g., 'RT' for retention time)
- RDKit Mol objects or canonical SMILES strings
- Molecular structure dataset (SMRT, PredRet, or user-provided in CSV format with 'InChI' and 'RT' columns)

## Outputs

- PyTorch tensors (node features, edge indices, edge attributes) compatible with torch_geometric
- Batched DataLoader objects for mini-batch training/inference
- Graph representation objects (torch_geometric Data objects) with fingerprint and graph features

## How to apply

Load molecular structures from your dataset (e.g., CSV with 'InChI' or 'SMILES' columns) using RDKit. For each molecule, generate two complementary representations: (1) molecular fingerprints using rdkit-pypi's fingerprint functions (e.g., Morgan fingerprints), and (2) a graph representation capturing atomic connectivity using RDKit's molecular graph API. Convert both representations to PyTorch tensors; use torch_geometric to construct graph objects with node features (atomic properties), edge indices (bonds), and edge attributes. Batch these tensors using torch_geometric's DataLoader for efficient mini-batch training. The rationale is that fingerprints capture global structural patterns while graphs preserve local connectivity, enabling the model to learn both low-level chemical patterns and multi-scale structural relationships relevant to chromatographic behavior.

## Related tools

- **rdkit-pypi** (Generate molecular fingerprints and RDKit Mol objects; parse InChI/SMILES strings into structured molecular graphs) — https://rdkit.org/
- **torch_geometric** (Construct graph tensor representations (node features, edge indices) and batch them for neural network input) — https://pytorch-geometric.readthedocs.io/
- **torch-scatter, torch-sparse, torch-cluster** (Backend operations for efficient graph convolution and aggregation in torch_geometric) — https://pytorch-geometric.readthedocs.io/
- **torch** (Framework for tensor creation, batching, and neural network training/inference) — https://pytorch.org/
- **pandas** (Load and manage tabular datasets (CSV) containing InChI/SMILES and experimental property labels)

## Examples

```
from rdkit import Chem; from torch_geometric.data import DataLoader; molecules = [Chem.MolFromInChI(inchi) for inchi in df['InChI']]; fingerprints = [AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048) for mol in molecules]; graphs = [mol_to_graph(mol) for mol in molecules]; loader = DataLoader([concatenate_features(fp, g) for fp, g in zip(fingerprints, graphs)], batch_size=32)
```

## Evaluation signals

- Verify all molecules in the dataset successfully parse to valid RDKit Mol objects; check for parse errors or null objects using RDKit's validity checks.
- Confirm fingerprint tensors have consistent dimensionality (e.g., 2048-dim Morgan fingerprints) and numeric range [0, 1] or [0, N] depending on fingerprint type.
- Validate graph tensors: node feature tensors have shape [num_atoms, feature_dim], edge indices have shape [2, num_bonds] with valid atomic indices, and edge attributes (if present) match bond count.
- Check DataLoader batches: verify batch sizes match specified batch_size parameter and that graphs are correctly stacked without index collisions across batch elements.
- Confirm output tensors match the input layer dimensionality of the downstream neural network model (e.g., concatenated fingerprint + graph feature size matches the RT-Transformer encoder input).

## Limitations

- Fingerprint methods are lossy; isomeric discrimination depends on fingerprint type and radius. Different fingerprint types (Morgan, RDKit, MACCS) may capture different structural patterns; choice affects model performance.
- Graph representation depends on valid 2D/3D structure; molecules with ambiguous or missing connectivity may fail to parse or produce incorrect graphs.
- Different chromatographic methods may exhibit vastly different retention time distributions for the same molecule; graph encoding alone cannot capture method-specific effects; transfer learning requires adaptation of the prediction head or fine-tuning.
- Large molecular graphs (>100 atoms) may exceed GPU memory during batching; padding or graph pooling strategies may be necessary for scalability.
- Fingerprint generation and graph construction are computationally expensive for large datasets; preprocessing and caching of encoded tensors is recommended to avoid redundant computation.

## Evidence

- [other] generate molecular fingerprints or graph representations using rdkit-pypi and convert to PyTorch tensors with torch_geometric for graph convolution layers: "generate molecular fingerprints or graph representations using rdkit-pypi and convert to PyTorch tensors with torch_geometric for graph convolution layers"
- [readme] The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output: "The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output"
- [readme] Prepare your dataset as a csv file which has 'InChI' and 'RT' columns: "Prepare your dataset as a csv file which has 'InChI' and 'RT' columns"
- [other] Load the SMRT-pretrained RT-Transformer model checkpoint and the PredRet dataset containing molecular structures and retention time annotations: "Load the SMRT-pretrained RT-Transformer model checkpoint and the PredRet dataset containing molecular structures and retention time annotations"
- [intro] Liquid chromatography retention times prediction can assist in metabolite identification, which is a critical task and challenge in non-targeted metabolomics: "Liquid chromatography retention times prediction can assist in metabolite identification, which is a critical task and challenge in non-targeted metabolomics"
