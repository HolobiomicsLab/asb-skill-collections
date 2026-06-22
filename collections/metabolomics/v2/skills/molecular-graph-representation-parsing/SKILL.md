---
name: molecular-graph-representation-parsing
description: Use when you have molecular identifiers (SMILES strings or molecular structure files) that need to be converted into node-edge graph tensors for input to message passing neural network models like chemprop or chemprop-IR.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0092
  tools:
  - chemprop
  - chemprop-IR
derived_from:
- doi: 10.1021/acs.jcim.1c00055
  title: Chemprop-IR
evidence_spans:
- extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations for Property Prediction]
- The `chemprop-IR` architecture is an extension of `chemprop`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemprop_ir
    doi: 10.1021/acs.jcim.1c00055
    title: Chemprop-IR
  dedup_kept_from: coll_chemprop_ir
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.1c00055
  all_source_dois:
  - 10.1021/acs.jcim.1c00055
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-graph-representation-parsing

## Summary

Parse molecular inputs (SMILES strings or graph structures) into standardized graph representations compatible with message passing neural networks. This skill bridges chemical notation and computational graph formats required for chemprop and chemprop-IR model ingestion.

## When to use

You have molecular identifiers (SMILES strings or molecular structure files) that need to be converted into node-edge graph tensors for input to message passing neural network models like chemprop or chemprop-IR. Use this skill when preparing raw chemical data for forward passes through MPNN architectures.

## When NOT to use

- Input is already a feature table or pre-computed molecular descriptor vector — use only when raw chemical structures must be converted to graph format.
- Target model does not accept graph-based inputs — this skill is specific to message passing neural networks and related graph neural architectures.
- Molecular structures are malformed, contain invalid atom symbols, or cannot be parsed by the underlying chemprop chemistry library.

## Inputs

- SMILES strings
- molecular structure files
- molecule objects from chemistry libraries (rdkit, etc.)

## Outputs

- node feature tensors (atom representations)
- edge adjacency matrices (bond connectivity)
- graph tensor bundles compatible with MPNN input layers

## How to apply

Load the chemprop codebase and locate the molecular graph parsing utilities, typically in the feature extraction or preprocessing modules. Parse SMILES strings or molecular structure inputs using the chemprop graph construction logic, which converts molecules into node features (atom types, bond orders, aromaticity) and edge adjacency matrices. Validate that the resulting graph tensors match the expected dimensionality and data types defined in the model architecture (e.g., atom feature vectors and bond index tensors). Test parsing on a small set of representative molecules before applying to full datasets. Verify that atom and bond features are correctly encoded and that the graph structure preserves molecular topology.

## Related tools

- **chemprop** (Provides the base molecular graph parsing and feature extraction module used to convert SMILES/structure inputs into node-edge tensors for MPNN ingestion) — https://github.com/chemprop/chemprop
- **chemprop-IR** (Extends chemprop's graph parsing with additional spectral feature layers; inherits and builds upon base molecular graph representation parsing) — https://github.com/chemprop/chemprop

## Evaluation signals

- Parsed graph tensors have consistent dimensionality across a batch of diverse molecular structures (varying atom counts, bond orders, aromaticity patterns)
- Node features are correctly indexed and match the chemical properties of input atoms (e.g., carbon, nitrogen, oxygen atoms encoded with correct bond multiplicities)
- Edge adjacency matrices preserve molecular connectivity — graph structure is isomorphic to the original molecule after round-trip serialization
- Feature data types match model input specification (e.g., float32 for atom features, int32 for bond indices; no NaN or inf values)
- Forward pass executes without shape mismatch errors when parsed tensors are fed to the MPNN model's input layer

## Limitations

- Parser fidelity depends on the chemistry library's (rdkit) ability to canonicalize and represent the input molecules; exotic or non-standard chemical structures may parse incorrectly or be rejected
- SMILES strings must be valid and unambiguous; canonical SMILES formats are recommended to ensure consistent graph construction across multiple parses of the same molecule
- Graph tensor dimensionality is fixed based on the maximum atom/bond feature vocabulary size in the model; molecules with novel atom types or bond orders outside the training vocabulary may be misrepresented

## Evidence

- [other] Parse molecular input handling (SMILES/graph parsing): "Parse the feature extraction implementation to understand the named spectral features and their construction logic. Implement or instantiate the spectral feature extraction module with molecular"
- [other] Graph representation and tensor production: "Test the feature extraction on a small set of example molecules to verify that feature tensors are produced in the correct shape and format."
- [other] Feature dimensionality and data type validation: "Validate that the extracted features match the expected dimensionality and data types defined in the chemprop-IR architecture."
- [other] Forward pass on molecular graph inputs: "Execute a forward pass on a sample molecular input (SMILES or graph representation) to verify model compilation and parameter flow."
- [intro] chemprop-IR as extension of chemprop: "The `chemprop-IR` architecture is an extension of `chemprop` described in the paper"
