---
name: ccs-prediction-model-design
description: Use when you have a dataset of molecules with known or reference CCS values, and you need to construct a trainable model that learns the mapping from molecular structure (encoded as SMILES or feature vectors) to scalar CCS predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0331
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3674
  tools:
  - Transformer (PyTorch)
  - MoLFormer (Pre-trained checkpoint)
  - PyTorch Lightning
  - RDKit
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.5c03492
  title: HyperCCS
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hyperccs_cq
    doi: 10.1021/acs.analchem.5c03492
    title: HyperCCS
  dedup_kept_from: coll_hyperccs_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03492
  all_source_dois:
  - 10.1021/acs.analchem.5c03492
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ccs-prediction-model-design

## Summary

Design and assemble a transformer-based neural network architecture that integrates molecular structure information (SMILES strings, molecular graphs, or feature vectors) to predict Collision Cross Section (CCS) values for molecules. This skill is essential when you have molecular identity data and experimental or reference CCS measurements, and need to build a deep learning model that captures structure–CCS relationships.

## When to use

Use this skill when you have a dataset of molecules with known or reference CCS values, and you need to construct a trainable model that learns the mapping from molecular structure (encoded as SMILES or feature vectors) to scalar CCS predictions. This is appropriate when empirical CCS measurement is expensive or unavailable, and you want to enable high-throughput in silico CCS prediction.

## When NOT to use

- Input data already consists of pre-computed CCS values (no prediction needed) — this skill is for training a predictor, not for processing measured CCS.
- Molecular structures are not available or are incomplete (skill requires valid SMILES or graph representations).
- Task requires real-time CCS prediction on millions of molecules with strict latency constraints — architecture design alone does not guarantee inference speed optimization.

## Inputs

- SMILES strings (molecular structure encodings)
- Molecular feature vectors (ECFP fingerprints, graph embeddings, or pre-computed features)
- Adduct type labels ([M+H]+, [M+Na]+, [M-H]- or other ionization modes)
- Reference or experimental CCS values (training targets)
- Pre-trained transformer checkpoint (e.g., MoLFormer weights from Pretrained MoLFormer/ directory)
- Tokenization vocabulary file (bert_vocab.txt)

## Outputs

- Compiled transformer-based CCS prediction model (PyTorch nn.Module)
- Model checkpoint file (.pt or .pth) containing learned weights
- Forward pass validation report (output shape, predicted CCS range, gradient flow confirmation)
- Predictions CSV file with columns: true_ccs, predicted_ccs, smiles, adducts

## How to apply

Begin by loading the HyperCCS repository and reviewing the transformer encoder specification to understand how molecular inputs (SMILES, molecular graphs, or ECFP fingerprints) are tokenized and embedded. Define the molecular encoder component that processes SMILES strings using a vocabulary (e.g., bert_vocab.txt) and outputs dense embeddings; this typically uses a pre-trained MoLFormer or equivalent transformer backbone. Connect transformer layers (configurable via n_layer, n_head, n_embd parameters) that apply self-attention over the molecular embeddings to capture structure-dependent relationships. Attach a prediction head (a dense layer or small MLP) that maps the final transformer hidden state to a scalar CCS output. Assemble the complete pipeline by connecting encoder → transformer layers → prediction head, then validate the forward pass by loading example molecules and confirming output shape and value ranges match expected CCS scales (typically 50–500 Ų for small organics). Use early or late fusion strategies if integrating multiple molecular representations (e.g., SMILES + ECFP) or conditional features (e.g., adduct type: [M+H]+, [M+Na]+, [M-H]-).

## Related tools

- **Transformer (PyTorch)** (Core architecture component for embedding and attending over molecular structure representations to extract CCS-predictive features) — https://pytorch.org
- **MoLFormer (Pre-trained checkpoint)** (Pre-trained molecular transformer backbone providing initialized weights for the encoder to accelerate convergence and improve CCS prediction accuracy) — https://github.com/NeoNexusX/HyperCCS
- **PyTorch Lightning** (Training framework for managing distributed training, checkpointing, and logging during model fine-tuning)
- **RDKit** (Molecular cheminformatics library for parsing SMILES strings, computing molecular graphs, and generating ECFP fingerprints)

## Examples

```
python main.py --dataset_name FD_M0 --n_head 12 --n_layer 12 --n_embd 768 --batch_size 64 --lr_start 1e-5 --max_epochs 100 --type early --project_name HyperCCS_Attention_fusion
```

## Evaluation signals

- Forward pass produces scalar CCS outputs in expected range (typically 50–500 Ų for most organic molecules); batch shape [batch_size, 1] or [batch_size] is correct.
- Gradient flow validation: backward pass completes without NaN or divergence; all transformer layer parameters receive non-zero gradients.
- Model checkpoint file is correctly saved and can be reloaded; state_dict keys match expected encoder, transformer, and prediction head sublayers.
- Prediction CSV output contains no null values in predicted_ccs column; predicted values lie within training data CCS percentiles (e.g., 1st–99th).
- Comparison of model predictions vs. held-out validation set shows non-zero correlation (Pearson r > 0.5 or Spearman ρ > 0.5 is typical early signal).

## Limitations

- Model architecture assumes SMILES or feature-vector input; if only 3D conformer or experimental spectra are available, preprocessing to SMILES/features is required first.
- CCS predictions depend on the quality and diversity of training data; models trained on limited adduct types or molecular series may not generalize to out-of-distribution structures.
- Fine-tuning requires careful choice of learning rate (default 1e-5), batch size (default 64), and dropout (default 0.1); suboptimal hyperparameter selection can lead to overfitting or divergence.
- Pre-trained MoLFormer checkpoint must be downloaded via git-lfs (git lfs pull); without LFS, checkpoint files will not be available and training will fail.
- Early vs. late fusion strategy must match the project_name parameter (must include 'Attention' string to activate fusion module); incorrect naming will silently disable feature fusion.

## Evidence

- [intro] The model utilizes a transformer-based architecture with molecular structure information for accurate CCS predictions.: "The model utilizes a transformer-based architecture with molecular structure information for accurate CCS predictions."
- [other] Define the transformer encoder component to process molecular structure information (SMILES strings, molecular graphs, or feature vectors as per repository specification).: "Define the transformer encoder component to process molecular structure information (SMILES strings, molecular graphs, or feature vectors as per repository specification)."
- [other] Implement the CCS prediction head that outputs scalar CCS values from the transformer embeddings.: "Implement the CCS prediction head that outputs scalar CCS values from the transformer embeddings."
- [readme] SMILES tokenization for molecular representation; Attention mechanisms for capturing molecular structure; Support for different adduct types ([M+H]+, [M+Na]+, [M-H]-); Early and late fusion options for feature integration: "SMILES tokenization for molecular representation; Attention mechanisms for capturing molecular structure; Support for different adduct types ([M+H]+, [M+Na]+, [M-H]-); Early and late fusion options"
- [other] Validate the model forward pass by loading example molecular structures and confirming output shape and value ranges match expected CCS predictions.: "Validate the model forward pass by loading example molecular structures and confirming output shape and value ranges match expected CCS predictions."
- [readme] --n_head: Number of attention heads (default: 12); --n_layer: Number of transformer layers (default: 12); --n_embd: Embedding dimension (default: 768): "--n_head: Number of attention heads (default: 12); --n_layer: Number of transformer layers (default: 12); --n_embd: Embedding dimension (default: 768)"
- [readme] project_name: Name for the training run  **must have 'Attention' in the string to use the fusion module**: "project_name: Name for the training run  **must have 'Attention' in the string to use the fusion module**"
