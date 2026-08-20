---
name: pytorch-transformer-backbone-instantiation
description: Use when when building a graph-based molecular property prediction model
  that must process both molecular structures (as heterogeneous graphs) and tabular
  metadata (chromatographic column parameters).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_3577
  tools:
  - Graphormer
  - DGL
  - PyTorch
  - RDKit
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
- Graphormer-RT is an extension to the Graphormer package, with documentation, and
  the original code on Github
- import dgl
- import torch
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

# PyTorch Transformer Backbone Instantiation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Initialize a PyTorch Graph Transformer backbone (Graphormer module) with configured hidden dimensions, attention heads, and encoder layers for molecular graph and chromatographic parameter featurization. This skill prepares the core neural architecture before assembling compound embeddings and forward passes for retention-time prediction.

## When to use

When building a graph-based molecular property prediction model that must process both molecular structures (as heterogeneous graphs) and tabular metadata (chromatographic column parameters). Specifically applicable when you have RDKit-generated molecular graphs, DGL graph representations, and numerical/categorical column descriptors (diameter, particle size, pH, temperature, solvent composition) that need joint encoding through a shared transformer backbone.

## When NOT to use

- When molecular structures are already pre-computed as fixed-size vector embeddings (use a simpler feed-forward network instead).
- When chromatographic metadata is sparse or incomplete across most samples (handle via imputation or dataset filtering first).
- When your target is not continuous retention time but categorical chromatographic method classification (requires output head redesign, not backbone instantiation).

## Inputs

- PyTorch model configuration parameters (hidden_dim, num_attention_heads, num_encoder_layers)
- DGL molecular graphs with node/edge attributes (atom types, bond orders, chirality)
- Column metadata: categorical features (company, USP code, solvent names, HPLC type)
- Column metadata: numerical features (length, diameter, particle size, temperature, pH, flow rate, dead time, Tanaka parameters, HSMB parameters)
- Chromatographic gradient vectors: time points (t1, t2, t3) and B-solvent percentages (B1, B2, B3)

## Outputs

- Initialized Graphormer PyTorch module ready for forward pass
- Column-parameter embedding layer (accepts one-hot + normalized features)
- Gradient-slope feature tensor (s1, s2, s3 arrays)
- Composite representation tensor (concatenated molecular + column + gradient embeddings)
- Model checkpoint structure with validated tensor shapes

## How to apply

Initialize the Graphormer module by specifying hidden dimension size, number of attention heads, and encoder layer depth suitable for your molecular graph representation. Configure the DGL graph featurization pipeline to encode molecules as heterogeneous graphs with node attributes (atom types, chirality) and edge attributes (bond orders). Create a separate embedding layer that accepts concatenated column parameters: one-hot encoded categoricals (company, USP, solvent types) plus normalized numericals (length/250, temperature/100, pH/14). Define gradient slope features (s1, s2, s3) from chromatographic time/B-solvent pairs using (B_next − B_prev)/(t_next − t_prev). Assemble the forward pass to concatenate molecular graph embeddings (from DGL encoder), column embeddings, and gradient slopes into a unified representation, then pass through the Graphormer backbone to a final dense output layer. Validate instantiation by checking tensor shape propagation with sample batches (molecular graphs + metadata) to ensure all intermediate tensors have consistent batch/feature dimensions.

## Related tools

- **Graphormer** (Provides the Graph Transformer backbone module with attention-based encoder layers for heterogeneous molecular graph encoding) — https://github.com/microsoft/Graphormer
- **DGL** (Constructs and manages heterogeneous molecular graphs with node/edge attributes (atom types, bond orders) for input to Graphormer) — https://github.com/dmlc/dgl
- **PyTorch** (Provides tensor operations, nn.Module base classes, and computational graph for backbone initialization and forward pass validation) — https://github.com/pytorch/pytorch
- **RDKit** (Generates molecular graphs and extracts chemical features (atom types, chirality, bond orders) for featurization) — https://github.com/rdkit/rdkit

## Examples

```
from graphormer.model_configs import create_graphormer; backbone = create_graphormer(hidden_dim=256, num_attention_heads=8, num_encoder_layers=6); import dgl; g = dgl.graph(([0,1],[1,2])); col_feat = torch.cat([one_hot_company, one_hot_usp, normalized_length, normalized_temp, gradient_slopes]); out = backbone(g, col_feat)
```

## Evaluation signals

- Verify tensor shape consistency: molecular graph batch embeddings (batch_size, hidden_dim) concatenate with column embeddings (batch_size, column_feature_dim) without broadcasting errors.
- Check gradient-slope computation: s1, s2, s3 are finite numerical arrays with no NaN or Inf values; slopes match formula (B_next − B_prev)/(t_next − t_prev).
- Confirm forward pass propagates through Graphormer backbone: input heterogeneous graph with node/edge attributes produces output logits of shape (batch_size, 1) for regression target.
- Validate model instantiation checkpoint: saved .pt file loads without shape-mismatch errors; model state_dict contains expected Graphormer encoder layer parameters and embedding weights.
- Sample-batch validation: instantiate with small toy batch (2–4 molecules, 2–4 column metadata rows) and confirm no dimension errors; output retention-time predictions are non-NaN scalars in plausible range (0–30 min typical for LC).

## Limitations

- Incomplete code blocks in the source article (syntax errors at 'for i i' and mid-function concatenation cuts) require manual completion; recommend consulting the full HopkinsLaboratory/Graphormer-RT repository for production-ready implementations.
- Tanaka parameter cleaning heuristic ('2.7 spp' → 2.7, '2.6 spp' → 2.7) is dataset-specific and may not generalize; verify your column metadata format and adapt replacement logic accordingly.
- Missing values in diameter and pH_B fields are replaced with 0, which may bias learned embeddings for sparsely reported columns; consider masking or per-category imputation instead.
- Additive concentration values are binarized (0/1) regardless of actual concentration range, losing information; preserve raw values if gradient effects are method-dependent.
- Model assumes fixed input dimensions across all chromatographic methods (reverse-phase and HILIC); retraining or fine-tuning required if new HPLC types or solvent combinations appear.

## Evidence

- [other] Initialize a PyTorch Graph Transformer backbone architecture (Graphormer module) with appropriate hidden dimensions, attention heads, and encoder layers.: "Initialize a PyTorch Graph Transformer backbone architecture (Graphormer module) with appropriate hidden dimensions, attention heads, and encoder layers."
- [other] Configure DGL graph featurization pipeline to encode molecules as heterogeneous graphs with node/edge attributes (atom types, bond orders, chirality).: "Configure DGL graph featurization pipeline to encode molecules as heterogeneous graphs with node/edge attributes (atom types, bond orders, chirality)."
- [other] Column parameters are featurized through one-hot encoding of categorical features (company, USP, solvents), normalization of numerical features (length/250, temperature/100, pH/14), and concatenation of integer and float encodings including diameter, particle size, pH, dead time, gradient slopes, Tanaka parameters, and HSMB parameters into a composite feature vector.: "Column parameters are featurized through one-hot encoding of categorical features (company, USP, solvents), normalization of numerical features (length/250, temperature/100, pH/14), and concatenation"
- [other] Define gradient-slope feature computation for B and t parameters (slopes s1, s2, s3 as (B_next − B_prev)/(t_next − t_prev)).: "Define gradient-slope feature computation for B and t parameters (slopes s1, s2, s3 as (B_next − B_prev)/(t_next − t_prev))."
- [other] Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone to final dense output layer for continuous retention-time prediction.: "Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone to"
- [other] Validate model instantiation by checking tensor shapes propagate correctly through forward pass with sample molecular graphs and column-metadata batches.: "Validate model instantiation by checking tensor shapes propagate correctly through forward pass with sample molecular graphs and column-metadata batches."
- [readme] Graphormer is a deep learning package that allows researchers and developers to train custom models for molecule modeling tasks.: "Graphormer is a deep learning package that allows researchers and developers to train custom models for molecule modeling tasks."
- [readme] Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github with additional usage examples.: "Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github with additional usage examples."
