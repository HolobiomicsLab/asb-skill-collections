---
name: smiles-sdf-format-handling
description: Use when you have downloaded or obtained a dataset of small molecules with structures encoded as SMILES strings or SDF files (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3391
  tools:
  - torch
  - Python
  - RDKit (rdkit-pypi)
  - PyTorch Geometric (torch_geometric)
  - Python pickle / torch.save
  - RT-Transformer
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
evidence_spans:
- torch
- Python 3.9
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
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

# SMILES/SDF Format Handling

## Summary

Parse and convert molecular structure files in SMILES or SDF format into standardized representations (Morgan fingerprints and graph encodings) suitable for machine learning model ingestion. This skill bridges raw chemical data into featurized inputs for retention time prediction and other molecular property models.

## When to use

You have downloaded or obtained a dataset of small molecules with structures encoded as SMILES strings or SDF files (e.g., the SMRT dataset from METLIN), and need to convert them into dual fingerprint and graph representations for input to a neural network-based molecular property predictor such as RT-Transformer. Apply this skill when your workflow requires both traditional fingerprint features and geometric graph attributes from the same set of chemical structures.

## When NOT to use

- Input structures are already featurized (e.g., pre-computed fingerprint matrices or pre-built graph objects) — skip directly to model training.
- Molecules contain stereochemistry or 3D conformational information that requires explicit 3D coordinate handling beyond SMILES/SDF parsing; use specialized conformer generation tools instead.
- Dataset is already in a model-specific format (e.g., pre-serialized PyTorch Geometric Data objects from a previous run) — load directly rather than re-parsing.

## Inputs

- SMILES strings (plain text or CSV column)
- SDF (Structure Data Format) files
- Molecular structure metadata (e.g., retention time labels, molecule identifiers)

## Outputs

- Morgan fingerprint tensors (binary or count vectors)
- Molecular graph objects (node features, edge indices, edge attributes)
- Serialized representation pairs (pickle or PyTorch tensor files)
- Validated molecule-to-representation mapping (e.g., CSV with molecule ID and file paths)

## How to apply

Load molecular structures from SMILES or SDF format using RDKit's molecule parsing functions. For each molecule, generate Morgan fingerprints using RDKit's fingerprint module to capture local chemical environment information. Simultaneously, convert the molecular structure to a graph representation by extracting atom features (atomic number, valence, chirality) as node attributes and bond types and aromaticity as edge attributes, using RDKit's Chem module paired with PyTorch Geometric for graph encoding. Serialize both representations (fingerprint and graph) to disk in a format compatible with downstream training (e.g., pickle or PyTorch tensor format) to avoid recomputation during model training. Validate that each molecule successfully generates both representations and that graph connectivity matches the original structure.

## Related tools

- **RDKit (rdkit-pypi)** (Parse SMILES/SDF molecular structures and generate Morgan fingerprints and molecular descriptors) — https://www.rdkit.org/
- **PyTorch Geometric (torch_geometric)** (Encode atom and bond features as node and edge attributes in graph format for neural network processing) — https://pytorch-geometric.readthedocs.io/
- **Python pickle / torch.save** (Serialize and persist fingerprint and graph representations to disk for efficient model training)
- **RT-Transformer** (Reference implementation that consumes dual fingerprint and graph inputs for retention time prediction) — https://github.com/01dadada/RT-Transformer

## Evaluation signals

- All molecules in the input dataset successfully parse without RDKit errors; no structures are dropped.
- Morgan fingerprints are generated with consistent dimensionality across all molecules (e.g., all 2048-bit vectors).
- Graph representations have valid node and edge counts that reflect molecular connectivity (number of edges ≥ number of bonds).
- Serialized representation files are readable and deserializable back into the original fingerprint and graph objects without data loss.
- Spot-check: manually verify that a known molecule (e.g., caffeine, aspirin) generates the expected fingerprint hash and graph structure matching its known connectivity.

## Limitations

- SMILES parsing may fail or produce ambiguous structures for malformed or non-standard SMILES strings; input validation and error reporting are essential.
- Morgan fingerprints capture only local 2D topology and cannot encode 3D conformational or stereochemical nuances; for molecules where 3D geometry is critical to retention time, fingerprint-only models may be limited.
- Different chromatographic conditions result in different retention times for the same molecule; fingerprint and graph representations are chemistry-invariant and do not encode experimental conditions, so model transfer across chromatographic methods requires domain adaptation.
- Graph representation quality depends on accurate atom and bond type assignment by RDKit; molecules with unusual valence states or exotic functional groups may be misinterpreted.

## Evidence

- [other] Parse molecular structures (SMILES or SDF format) using RDKit to generate Morgan fingerprints for each molecule.: "Parse molecular structures (SMILES or SDF format) using RDKit to generate Morgan fingerprints for each molecule."
- [other] Convert molecular structures to graph representations using RDKit's Chem.Descriptors and PyTorch Geometric to encode atom and bond features as node and edge attributes.: "Convert molecular structures to graph representations using RDKit's Chem.Descriptors and PyTorch Geometric to encode atom and bond features as node and edge attributes."
- [other] Fingerprints and molecular graphs are derived using rdkit-pypi for molecular representation and torch_geometric for graph processing, with the SMRT dataset sourced from the METLIN small molecule dataset paper: "Fingerprints and molecular graphs are derived using rdkit-pypi for molecular representation and torch_geometric for graph processing"
- [other] Serialize fingerprint and graph representations to disk in a format compatible with downstream model training (e.g., pickle or PyTorch tensor format).: "Serialize fingerprint and graph representations to disk in a format compatible with downstream model training (e.g., pickle or PyTorch tensor format)."
- [readme] The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output.: "The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output."
