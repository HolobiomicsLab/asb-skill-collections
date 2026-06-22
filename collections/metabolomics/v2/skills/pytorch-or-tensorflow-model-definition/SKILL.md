---
name: pytorch-or-tensorflow-model-definition
description: Use when when you have molecular structure inputs (SMILES strings, molecular graphs, or feature vectors) and need to predict a continuous molecular property (e.g., CCS values, retention time, ionization efficiency).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3363
  edam_topics:
  - http://edamontology.org/topic_3298
  - http://edamontology.org/topic_3336
  tools:
  - MoLFormer
  - PyTorch
  - PyTorch Lightning
  - transformers (Hugging Face)
  - RDKit
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pytorch-or-tensorflow-model-definition

## Summary

Define and assemble a transformer-based deep learning model for molecular property prediction, integrating molecular structure encoders, attention mechanisms, and prediction heads into a complete architecture. This skill enables construction of multimodal models that process SMILES strings and molecular features to output scalar predictions like Collision Cross Section (CCS) values.

## When to use

When you have molecular structure inputs (SMILES strings, molecular graphs, or feature vectors) and need to predict a continuous molecular property (e.g., CCS values, retention time, ionization efficiency). Specifically applicable when the prediction task requires capturing long-range dependencies in molecular structure through attention mechanisms, and when pre-trained molecular encoders (e.g., MoLFormer) are available for initialization.

## When NOT to use

- Input molecules are already pre-computed as fixed-size numerical feature matrices without structural information (use a simple dense neural network instead)
- Task is classification (e.g., compound class prediction) rather than continuous property regression
- Computational budget does not permit transformer-scale models (>100M parameters); consider simpler architectures like random forests or linear models

## Inputs

- SMILES strings (molecular representations)
- Molecular feature vectors (ECFP fingerprints, adduct types)
- Pre-trained transformer checkpoint (e.g., MoLFormer weights)
- Vocabulary file (bert_vocab.txt for tokenization)
- Hyperparameter configuration (JSON or command-line arguments)

## Outputs

- Compiled PyTorch/TensorFlow model object
- Model architecture definition (serialized as checkpoint)
- Forward pass validation log (input/output shapes, value ranges)
- CCS prediction tensor (batch_size × 1 scalar values)

## How to apply

Load a pre-trained transformer encoder (e.g., MoLFormer checkpoint) and define a molecular tokenizer (e.g., SMILES-based vocabulary via bert_vocab.txt). Construct a transformer encoder block with configurable attention heads (--n_head, typically 12), layers (--n_layer, typically 12), and embedding dimension (--n_embd, typically 768). Integrate molecular feature fusion (early or late fusion via --type parameter) to combine SMILES embeddings with auxiliary features like ECFP fingerprints (--ecfp_num, typically 1024) and adduct type embeddings (--adduct_num, typically 3). Attach a prediction head (dense layers with dropout --d_dropout, typically 0.1) that maps transformer outputs to scalar CCS values. Validate the model by performing a forward pass on example molecules and confirming output shapes match the expected batch size and scalar prediction format.

## Related tools

- **MoLFormer** (Pre-trained molecular transformer encoder for SMILES tokenization and structure embedding)
- **PyTorch** (Deep learning framework for model definition, forward pass, and training)
- **PyTorch Lightning** (Training loop management and checkpointing for transformer model training)
- **transformers (Hugging Face)** (Pre-built transformer layer implementations and tokenization utilities)
- **RDKit** (Molecular structure parsing and ECFP fingerprint generation for feature fusion)

## Examples

```
python main.py --dataset_name FD_M0 --data_root ./data/FD_M0 --n_head 12 --n_layer 12 --n_embd 768 --ecfp_num 1024 --type early --batch_size 64 --max_epochs 100 --device cuda
```

## Evaluation signals

- Model forward pass produces output tensor of shape (batch_size, 1) with CCS values in expected range (200–400 Ų typical for small molecules)
- Attention mechanism weights sum to 1.0 across the sequence dimension (softmax constraint verified)
- Gradient flow check: backward pass completes without NaN/Inf values and gradients propagate to all trainable parameters
- Model parameter count matches expected size (e.g., 12 layers × 12 heads × 768 embedding dim + prediction head ≈ 100M+ parameters for full transformer)
- Prediction output is invariant to padding tokens and only reflects non-masked molecular features

## Limitations

- Model requires GPU memory proportional to transformer size; fine-tuning with batch_size > 64 may exceed typical VRAM on consumer hardware
- SMILES tokenization is lossy and context-dependent; unusual chirality or aromaticity patterns may not be fully captured by fixed vocabulary (bert_vocab.txt)
- Early vs. late fusion (--type parameter) choice requires validation on the target dataset; no universal rule determines which is optimal
- Prediction accuracy degrades for molecules with chemical scaffolds or adduct types not seen during pre-training; domain adaptation or fine-tuning is required
- Apex installation (NVIDIA mixed precision) is optional but may fail on non-NVIDIA GPUs or older CUDA versions (≤10.0); CPU-only training is significantly slower

## Evidence

- [intro] The model utilizes a transformer-based architecture with molecular structure information for accurate CCS predictions.: "The model utilizes a transformer-based architecture with molecular structure information for accurate CCS predictions."
- [readme] SMILES tokenization for molecular representation, Attention mechanisms for capturing molecular structure, Support for different adduct types ([M+H]+, [M+Na]+, [M-H]-), Early and late fusion options for feature integration: "The model uses a transformer-based architecture with: SMILES tokenization for molecular representation, Attention mechanisms for capturing molecular structure, Support for different adduct types"
- [readme] Model Architecture Parameters: --n_head: Number of attention heads (default: 12), --n_layer: Number of transformer layers (default: 12), --n_embd: Embedding dimension (default: 768), --adduct_num: Number of adduct types (default: 3), --ecfp_num: ECFP fingerprint size (default: 1024), --type: Fusion type ('early' or 'later') for feature integration: "Model Architecture Parameters: --n_head: Number of attention heads (default: 12), --n_layer: Number of transformer layers (default: 12), --n_embd: Embedding dimension (default: 768), --adduct_num:"
- [other] Define the transformer encoder component to process molecular structure information (SMILES strings, molecular graphs, or feature vectors as per repository specification).: "Define the transformer encoder component to process molecular structure information (SMILES strings, molecular graphs, or feature vectors as per repository specification)."
- [other] Implement the CCS prediction head that outputs scalar CCS values from the transformer embeddings.: "Implement the CCS prediction head that outputs scalar CCS values from the transformer embeddings."
