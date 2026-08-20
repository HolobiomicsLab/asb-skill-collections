---
name: tensor-shape-validation-through-forward-pass
description: Use when after assembling a Graphormer backbone with DGL molecular graph
  encoders, column-parameter embedding layers, and gradient-slope feature concatenation,
  but before training on the full dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_3336
  tools:
  - Graphormer
  - DGL
  - PyTorch
  - RDKit
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
- Graphormer-RT is an extension to the Graphormer package, with documentation, and
  the original code on Github
- import dgl
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphormer_rt_cq
    doi: 10.1021/acs.analchem.4c05859
    title: Graphormer-RT
  dedup_kept_from: coll_graphormer_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05859
  all_source_dois:
  - 10.1021/acs.analchem.4c05859
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tensor-shape-validation-through-forward-pass

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify correct tensor dimensionality propagation through a Graph Transformer model by executing a forward pass on sample molecular graphs and column-metadata batches, catching shape mismatches before full training. This guards against silent broadcasting errors and dimensional inconsistencies in heterogeneous graph encodings and multi-modal feature fusion.

## When to use

After assembling a Graphormer backbone with DGL molecular graph encoders, column-parameter embedding layers, and gradient-slope feature concatenation, but before training on the full dataset. Use this skill whenever you combine embeddings from multiple modalities (graph structure, categorical metadata, normalized numerical features) and must ensure the final output layer receives correctly shaped tensors.

## When NOT to use

- Model architecture is already deployed and tested in production — use continuous monitoring instead.
- Input is a pre-computed feature table (e.g., .npz or .csv) with no Graph Transformer model yet defined.
- Sample molecular graph or column metadata is unavailable or incomplete — collect representative data first.

## Inputs

- Instantiated Graphormer PyTorch model with configured attention heads, hidden dimensions, and encoder layers
- DGL molecular graph with node attributes (atom types) and edge attributes (bond orders, chirality)
- Column-metadata vector: concatenated one-hot encodings (company, USP, solvents) and normalized numerical features (length/250, temperature/100, pH/14, diameter, particle size, pH_A, pH_B, dead time, gradient slopes s1, s2, s3, Tanaka/HSMB parameters)

## Outputs

- Boolean validation result (pass/fail) indicating whether all intermediate tensor shapes conform to model architecture
- Scalar tensor output shape (torch.Size([1]) for single-molecule batch or [batch_size] for multi-molecule batch)
- Error log (if any) listing shape mismatches at DGL encoder, column-embedding, or concatenation stages

## How to apply

Instantiate the model with all layers configured (Graphormer module, DGL graph featurization pipeline, column-parameter embedding layer for one-hot encoded categoricals and normalized numericals, and gradient-slope computation). Create a minimal batch with a sample molecular graph (e.g., a single molecule converted to DGL heterogeneous graph with atom types, bond orders, chirality) and a corresponding column-metadata vector (one-hot company/USP/solvent encodings concatenated with normalized length/250, temperature/100, pH/14 values, plus diameter, particle size, dead time, Tanaka/HSMB parameters, and gradient slopes s1/s2/s3). Execute a single forward pass and inspect tensor shapes at three critical junctions: (1) after DGL graph encoder outputs molecular embeddings, (2) after column-parameter embedding layer outputs concatenated metadata features, (3) after concatenating molecular embeddings with column embeddings and gradient slopes. Confirm final output shape matches the target (1,) for continuous retention-time regression. Use assertions or print statements to halt if any intermediate shape deviates from expected dimensions.

## Related tools

- **Graphormer** (Provides Graph Transformer backbone architecture (attention heads, encoder layers, hidden dimensions) that processes concatenated molecular and column embeddings into scalar retention-time predictions.) — https://github.com/microsoft/Graphormer
- **DGL** (Constructs heterogeneous molecular graphs with node/edge attributes (atom types, bond orders, chirality) and encodes them into graph embeddings prior to concatenation.) — https://github.com/dmlc/dgl
- **PyTorch** (Provides tensor operations, shape introspection (.shape, .size()), and forward-pass execution framework for model validation.) — https://github.com/pytorch/pytorch
- **RDKit** (Converts SMILES strings to molecular objects that DGL uses to construct graph representations with atomic and bond features.) — https://github.com/rdkit/rdkit

## Examples

```
import torch; model = GraphormerRT(hidden_dim=256, num_heads=8, num_layers=6); sample_graph = dgl.graph(([0,1,2],[1,2,0])); col_metadata = torch.cat([torch.zeros(8), torch.tensor([2.5, 0.3, 6.8, 25.0, 5.0, 0.01, 0.15, 0.05])]); out = model(sample_graph, col_metadata); assert out.shape == torch.Size([1]), f'Expected shape [1], got {out.shape}'
```

## Evaluation signals

- All intermediate tensor shapes match expected dimensions: DGL graph encoder outputs [batch_size, hidden_dim], column-embedding layer outputs [batch_size, column_feature_dim], concatenated feature tensor outputs [batch_size, hidden_dim + column_feature_dim + gradient_slope_dim].
- Final output tensor has shape [batch_size] or [batch_size, 1] suitable for scalar retention-time regression (no shape broadcasts or dimension squeezing errors).
- Forward pass completes without RuntimeError or ValueError related to tensor shape mismatches, non-broadcastable dimensions, or attribute access failures.
- Gradient computation (backward pass) succeeds and produces valid gradients for all model parameters, confirming the computational graph is well-formed.
- Repeated forward passes with different batch sizes and column-metadata compositions produce consistent output shapes, indicating the validation is robust to input variability.

## Limitations

- Validation on a single small batch does not guarantee correct behavior on the full training dataset, especially if the dataset contains outlier column parameters (e.g., unusual pH or gradient slopes) that could cause numerical instabilities downstream.
- Shape validation does not detect semantic errors in feature normalization (e.g., length/250, temperature/100, pH/14 applied incorrectly) — auditing normalization logic separately is necessary.
- The sample molecular graph must be representative of the training distribution; a single SMILES string or overly simple molecule may not exercise all graph encoder pathways (e.g., uncommon bond types, large rings, stereochemistry variants).
- Incomplete code blocks in the source material (noted as 'for i i' syntax error and truncated int_encodings concatenation) mean some column-featurization steps may not be fully specified; practitioners must reconcile these gaps before validation.

## Evidence

- [other] Validate model instantiation by checking tensor shapes propagate correctly through forward pass with sample molecular graphs and column-metadata batches.: "Validate model instantiation by checking tensor shapes propagate correctly through forward pass with sample molecular graphs and column-metadata batches."
- [other] Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone to final dense output layer for continuous retention-time prediction.: "Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone to"
- [other] Configure DGL graph featurization pipeline to encode molecules as heterogeneous graphs with node/edge attributes (atom types, bond orders, chirality).: "Configure DGL graph featurization pipeline to encode molecules as heterogeneous graphs with node/edge attributes (atom types, bond orders, chirality)."
- [other] Create column-parameter embedding layer that accepts one-hot encoded categorical features (company, USP, solvent composition) and normalized numerical features (length/250, temperature/100, pH/14).: "Create column-parameter embedding layer that accepts one-hot encoded categorical features (company, USP, solvent composition) and normalized numerical features (length/250, temperature/100, pH/14)."
- [other] Initialize a PyTorch Graph Transformer backbone architecture (Graphormer module) with appropriate hidden dimensions, attention heads, and encoder layers.: "Initialize a PyTorch Graph Transformer backbone architecture (Graphormer module) with appropriate hidden dimensions, attention heads, and encoder layers."
