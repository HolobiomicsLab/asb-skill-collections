---
name: graph-neural-network-architecture-assembly
description: 'Use when when you have: (1) a collection of molecules represented as molecular graphs (nodes=atoms, edges=bonds with chirality/order attributes); (2) structured metadata describing experimental conditions (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3372
  tools:
  - Graphormer
  - DGL
  - RDKit
  - PyTorch
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
- Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github
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
---

# graph-neural-network-architecture-assembly

## Summary

Assembly and instantiation of a Graph Transformer backbone for molecular property prediction, where heterogeneous molecular graphs (nodes, edges, atom/bond attributes) and structured metadata (column parameters, gradient slopes) are combined into a unified forward pass that outputs continuous predictions. This skill bridges graph encoding, feature featurization, and transformer inference.

## When to use

When you have: (1) a collection of molecules represented as molecular graphs (nodes=atoms, edges=bonds with chirality/order attributes); (2) structured metadata describing experimental conditions (e.g., chromatographic column parameters: diameter, particle size, temperature, pH, solvent composition, gradient slopes); (3) a need to predict a continuous outcome (e.g., retention time) that depends on both molecular structure and experimental context; and (4) access to a pre-trained or custom Graphormer checkpoint. Use this skill to construct the combined encoder–transformer–decoder pipeline that fuses these heterogeneous inputs.

## When NOT to use

- Input molecules are already flattened into fixed-size descriptor vectors or Morgan fingerprints; use standard MLPs or XGBoost instead of graph architectures.
- Experimental metadata is sparse, unstructured, or missing for >20% of samples; imputation and featurization of incomplete column parameters may degrade predictions.
- Target is classification (e.g., retention-time bin) rather than continuous regression; use a classification head and appropriate loss function, not a dense regression layer.

## Inputs

- DGL heterogeneous molecular graphs (nodes with atom-type features, edges with bond-order and chirality attributes)
- RDKit Mol objects or SMILES strings (convertible to DGL graphs)
- Column metadata table with fields: company_name, USP_code, column_length, column_inner_diameter, particle_size, temperature, flow_rate, dead_time, HPLC_type, solvent_A, solvent_B, gradient_times, gradient_B_values, pH_A, pH_B, additive_A, additive_B, Tanaka_parameters, HSMB_parameters
- Graphormer pre-trained checkpoint or initialization parameters (hidden_dim, num_attention_heads, num_encoder_layers)

## Outputs

- PyTorch model instance (nn.Module) ready for forward pass
- Tensor predictions of shape [batch_size, 1] representing continuous retention times or other molecular properties
- Validation report: tensor shape traces through forward pass (e.g., graph embeddings [batch, hidden_dim], column embeddings [batch, column_feature_dim], concatenated [batch, total_dim], final output [batch, 1])

## How to apply

First, initialize a PyTorch Graphormer module with specified hidden dimensions, attention heads, and encoder layers. Second, instantiate a DGL graph featurization pipeline that encodes each molecule as a heterogeneous graph, annotating nodes with atom types and edges with bond orders and chirality flags. Third, construct a column-parameter embedding layer that accepts one-hot encoded categorical features (company, USP, solvent type, HPLC method) and normalized numerical features (column length divided by 250, temperature divided by 100, pH divided by 14, diameter, particle size, dead time, Tanaka/HSMB physicochemical parameters). Fourth, compute gradient-slope features as piecewise slopes s1, s2, s3 from chromatographic B and t parameters via (B_next − B_prev)/(t_next − t_prev). Fifth, assemble the forward pass: concatenate the DGL-encoded molecular graph embeddings, the column-parameter embeddings, and gradient slopes into a composite feature vector, then pass through the Graphormer transformer backbone to a final dense output layer. Finally, validate instantiation by running a forward pass on sample batches (molecular graphs + column metadata) and checking that tensor shapes propagate correctly and output shape matches the prediction target (single continuous value per molecule–column pair).

## Related tools

- **Graphormer** (Graph Transformer backbone: encodes molecular graphs through attention-based message passing and outputs node/graph-level embeddings) — https://github.com/microsoft/Graphormer
- **DGL** (Heterogeneous graph construction and featurization: converts SMILES/Mol objects to node–edge graphs with atom-type and bond-order attributes)
- **RDKit** (Molecule I/O and feature extraction: parses SMILES strings, generates Mol objects, computes molecular properties (used in DGL graph construction))
- **PyTorch** (Neural network framework: defines model layers (embeddings, transformers, dense), handles forward passes, and manages tensor operations)

## Evaluation signals

- Forward pass completes without shape-mismatch or device-placement errors; sample batch (e.g., 32 molecules + 32 column metadata rows) produces output shape [32, 1].
- Molecular graph embeddings have expected dimensionality (hidden_dim, e.g., 768); column parameter embeddings match featurization output size (≥30 features post-concatenation); gradient slopes are scalar values in [−2, 2] (typical normalized gradient range).
- Model parameters are on the correct device (CPU or CUDA); gradients flow through all components (graph encoder → transformer → output layer) when loss.backward() is called.
- Column metadata is correctly one-hot encoded (categorical dimensions sum to 1 per category) and numerical features are normalized to approximate range [0, 1] (e.g., pH ∈ [0, 0.14] after division by 14).
- Predictions are within physically plausible range for retention times (e.g., 0–100 min for typical LC methods); no NaN or inf values in output or gradient tensors.

## Limitations

- Incomplete or truncated code in source material (two code blocks end mid-function with syntax errors 'for i i' and truncated int_encodings concatenation); full featurization pipeline must be manually completed or sourced from HopkinsLaboratory/Graphormer-RT repository.
- Categorical feature encoding (company, USP, solvent type) is dataset-specific; one-hot vocabulary must be learned from training data or predefined; unseen categories will fail unless handled with OOV (out-of-vocabulary) placeholders.
- Numerical feature normalization thresholds (length/250, temperature/100, pH/14) are assumed fixed; if experimental ranges differ significantly (e.g., ultra-high-pressure HPLC >400 bar), normalization may saturate or produce outliers.
- Missing values in column metadata (empty strings for diameter, pH_B) are replaced with 0; this assumes 0 is semantically meaningful (e.g., no additive present) and may introduce bias if data is missing at random.
- Tanaka and HSMB physicochemical parameters contain string artifacts ('2.7 spp', '2.6 spp'); string-to-numeric conversion is required and non-standard values are coerced to defaults, risking silent data loss.
- Model requires pre-trained Graphormer weights or careful initialization; training from scratch requires substantial labeled data and tuning of learning rate, warmup schedule, and weight decay.

## Evidence

- [other] Column parameters are featurized through one-hot encoding of categorical features (company, USP, solvents), normalization of numerical features (length/250, temperature/100, pH/14), and concatenation of integer and float encodings: "Column parameters are featurized through one-hot encoding of categorical features (company, USP, solvents), normalization of numerical features (length/250, temperature/100, pH/14), and concatenation"
- [other] Initialize a PyTorch Graph Transformer backbone architecture (Graphormer module) with appropriate hidden dimensions, attention heads, and encoder layers: "Initialize a PyTorch Graph Transformer backbone architecture (Graphormer module) with appropriate hidden dimensions, attention heads, and encoder layers."
- [other] Configure DGL graph featurization pipeline to encode molecules as heterogeneous graphs with node/edge attributes (atom types, bond orders, chirality): "Configure DGL graph featurization pipeline to encode molecules as heterogeneous graphs with node/edge attributes (atom types, bond orders, chirality)."
- [other] Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone to final dense output layer for continuous retention-time prediction: "Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone to"
- [other] Validate model instantiation by checking tensor shapes propagate correctly through forward pass with sample molecular graphs and column-metadata batches: "Validate model instantiation by checking tensor shapes propagate correctly through forward pass with sample molecular graphs and column-metadata batches."
- [results] def featurize_column(column_params, index): company = one_hot_company(column_params[0]) USP = one_hot_USP(column_params[1]) length = float(column_params[2]) / 250: "def featurize_column(column_params, index):
    company = one_hot_company(column_params[0])
    USP = one_hot_USP(column_params[1])
    length = float(column_params[2]) / 250"
- [readme] Supports interface and datasets of PyG, DGL, OGB, and OCP. Supports fairseq backbone.: "Supports interface and datasets of PyG, DGL, OGB, and OCP.
* Supports fairseq backbone."
