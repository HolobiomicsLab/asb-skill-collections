---
name: transformer-encoder-architecture-design
description: Use when when you need to learn chemical-rational embeddings of tandem
  MS/MS spectra for library matching or molecular property prediction, and you want
  to leverage self-supervised learning through masking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Anaconda
  - Git
  - PyTorch 2.2
  - Anaconda (Python 3.12)
  - MSBERT (reference implementation)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c02426
  title: MSBERT
evidence_spans:
- '[Anaconda](https://www.anaconda.com) for Python 3.12'
- Install [Git](https://git-scm.com/downloads)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msbert_cq
    doi: 10.1021/acs.analchem.4c02426
    title: MSBERT
  dedup_kept_from: coll_msbert_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c02426
  all_source_dois:
  - 10.1021/acs.analchem.4c02426
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# transformer-encoder-architecture-design

## Summary

Design and implement a transformer encoder backbone in PyTorch to process tandem mass spectra with configurable attention heads and hidden dimensions. This architecture forms the foundation for mask-based contrastive pretraining of mass spectrometry embeddings.

## When to use

When you need to learn chemical-rational embeddings of tandem MS/MS spectra for library matching or molecular property prediction, and you want to leverage self-supervised learning through masking. Apply this skill before implementing the masking augmentation and contrastive loss, as the encoder backbone is the core learnable component that will be trained to map spectra into a meaningful embedding space.

## When NOT to use

- Input spectra are not tokenized or binned into discrete m/z-intensity pairs — preprocess raw spectra first
- You have only a handful of MS/MS spectra (<100) — the transformer will overfit without sufficient contrastive pairs
- Your task requires interpretability of which m/z peaks drive predictions — transformer attention may be harder to interpret than rule-based or simpler feature-based models

## Inputs

- Tokenized tandem mass spectra (batch of integer sequences, shape [batch_size, sequence_length])
- Hyperparameter configuration: vocab_size, hidden_dim, num_heads, intermediate_dim, dropout_rate, max_position_embeddings

## Outputs

- Transformer encoder model (PyTorch nn.Module)
- Embedding vectors from encoded spectra (shape [batch_size, hidden_dim])
- Verified forward-pass tensor transformations demonstrating correct shape flow

## How to apply

Implement a transformer encoder in PyTorch 2.2 with configurable hyperparameters: vocabulary size (number of possible m/z intensity bins, e.g., 100002 for MSBERT), embedding dimension (e.g., 512), number of attention heads (e.g., 6), and feed-forward hidden dimension (e.g., 16). The encoder takes tokenized tandem mass spectra as input and produces fixed-size embedding vectors. Configure the architecture to accept both original and randomly masked versions of the same spectrum during training, so that the model learns invariant representations. Verify correct tensor shape transformations through the forward pass: input shape [batch_size, sequence_length] → output shape [batch_size, embedding_dim]. The encoder should output embeddings suitable for cosine similarity computation between paired spectra.

## Related tools

- **PyTorch 2.2** (Framework for implementing the transformer encoder architecture, autograd, and tensor operations) — https://pytorch.org/
- **Anaconda (Python 3.12)** (Environment manager for dependency isolation and reproducible Python setup) — https://www.anaconda.com
- **Git** (Version control for cloning the MSBERT repository and accessing the reference implementation) — https://git-scm.com/downloads
- **MSBERT (reference implementation)** (Reference transformer encoder and training pipeline for tandem mass spectra embedding) — https://github.com/zhanghailiangcsu/MSBERT

## Examples

```
model = MSBERT(100002, 512, 6, 16, 0, 100, 3); model.load_state_dict(torch.load('model/MSBERT.pkl')); demo_arr = ModelEmbed(model, demo_data, 16)
```

## Evaluation signals

- Forward pass produces embeddings with correct shape [batch_size, hidden_dim] and no NaN or Inf values
- Identical masking seed produces identical embeddings from original and masked spectrum pairs before contrastive loss training
- Embeddings can be compared via cosine similarity to produce scores in [−1, 1]; library matching achieves top-1 accuracy ≥0.78 on Orbitrap test set after full training
- Attention weights across heads sum approximately to 1.0 per token, indicating proper softmax normalization
- Model weight gradients flow through all layers during backprop, verified via torch.autograd.grad or loss.backward() + inspection of model.parameters()

## Limitations

- Hyperparameter sensitivity: attention heads, hidden dimensions, and dropout rate must be tuned for your specific spectrum vocabulary size and dataset size; poor choices may lead to underfitting or overfitting.
- Vocabulary size is fixed at model creation; tokenized spectra with m/z values outside the vocabulary range will fail. The MSBERT paper uses 100002 bins for GNPS; your dataset may require different binning.
- Computational cost scales with sequence length (number of m/z peaks per spectrum) and batch size; longer spectra or larger batches require more GPU memory and training time.
- No built-in handling of missing or null spectra; input data must be complete and pre-normalized before encoder input.

## Evidence

- [readme] MSBERT used the transformer encoder as the backbone and take advantage of the randomness of the mask to construct positive samples for contrastive learning.: "MSBERT used the transformer encoder as the backbone and take advantage of the randomness of the mask to construct positive samples for contrastive learning."
- [intro] Implement the transformer-encoder backbone architecture in PyTorch 2.2 with configurable attention heads and hidden dimensions.: "Implement the transformer-encoder backbone architecture in PyTorch 2.2 with configurable attention heads and hidden dimensions."
- [intro] Verify the encoder and masking module are correctly wired to the contrastive loss computation by validating tensor shape transformations through the forward pass.: "Verify the encoder and masking module are correctly wired to the contrastive loss computation by validating tensor shape transformations through the forward pass."
- [readme] model = MSBERT(100002, 512, 6, 16, 0,100,3): "model = MSBERT(100002, 512, 6, 16, 0,100,3)"
- [readme] MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset.: "MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset."
