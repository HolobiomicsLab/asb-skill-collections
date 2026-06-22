---
name: infoence-loss-composition
description: Use when when training embeddings from MS/MS spectra data where you need both discriminative power (to distinguish similar spectra) and reconstruction accuracy (to preserve peak and metadata information).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PyTorch
  - Transformer architecture
  - CLERMS
derived_from:
- doi: 10.1021/acs.analchem.3c00260
  title: CLERMS
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_clerms_cq
    doi: 10.1021/acs.analchem.3c00260
    title: CLERMS
  dedup_kept_from: coll_clerms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c00260
  all_source_dois:
  - 10.1021/acs.analchem.3c00260
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Compose InfoNCE and MSE Loss for Embedding Training

## Summary

Combine InfoNCE contrastive loss and MSE reconstruction loss into a weighted composite loss function for training embeddings from MS/MS spectra peak information and metadata. This hybrid approach balances contrastive learning (discriminative separation) with reconstruction fidelity in a transformer-based embedding architecture.

## When to use

When training embeddings from MS/MS spectra data where you need both discriminative power (to distinguish similar spectra) and reconstruction accuracy (to preserve peak and metadata information). Specifically when peak-information embeddings and metadata embeddings must be jointly optimized with temperature-scaled contrast and reconstruction objectives.

## When NOT to use

- Input embeddings are already fixed (pre-trained, frozen) — no gradients to optimize.
- Only reconstruction accuracy matters and discriminative power is irrelevant — use MSE loss alone.
- Peak and metadata modalities are uncorrelated or orthogonal; InfoNCE will fail to find meaningful positives.

## Inputs

- Peak-information embeddings (batch × embedding_dim tensor)
- Metadata embeddings (batch × embedding_dim tensor)
- Positive pair indices or masks (batch-level correspondences)
- Temperature scaling coefficient (scalar, typically 0.1–1.0)
- Loss weight parameters (α, β for InfoNCE and MSE balancing)

## Outputs

- Composite loss value (scalar tensor)
- Gradient flow enabling backpropagation through both loss terms
- Per-sample InfoNCE and MSE loss components (for monitoring)

## How to apply

Define two loss components: (1) InfoNCE contrastive loss operating on peak-information and metadata embeddings with temperature scaling to maximize agreement between modalities while repelling negatives; (2) MSE reconstruction loss to enforce faithful reconstruction of embeddings. Implement the composite loss as a weighted sum of both terms, where weights are configurable hyperparameters. Wrap in a PyTorch module and validate gradient flow through both branches on synthetic embedding tensors of shape matching your spectra batch size. The temperature parameter in InfoNCE controls the peakedness of the similarity distribution—lower values sharpen contrasts, higher values soften them; adjust based on convergence behavior and embedding space geometry.

## Related tools

- **PyTorch** (Deep learning framework for implementing composite loss module, tensor operations, and gradient computation)
- **Transformer architecture** (Host architecture for sinusoidal embedder that produces peak-information and metadata embeddings fed into composite loss)
- **CLERMS** (Reference implementation combining sinusoidal embedder and composite loss for MS/MS spectra representation learning) — https://github.com/HaldamirS/CLERMS

## Evaluation signals

- Gradient flow: verify ∇loss w.r.t. embedding parameters is non-zero and finite for both InfoNCE and MSE terms; check backward() executes without NaN or overflow.
- Loss component breakdown: InfoNCE should decrease as embeddings become more aligned across modalities; MSE should decrease as reconstruction fidelity improves; composite loss should be a weighted sum matching the configured weights.
- Embedding space geometry: cosine similarity between positive peak-metadata pairs should increase over training epochs; negative pairs should decrease; verify using histogram of pairwise similarities.
- Convergence stability: loss should decrease monotonically (with noise) over training batches; no sudden spikes or divergence; training loss should be comparable to validation loss (no overfitting to single batch).
- Ablation check: disable InfoNCE (α=0) and verify only MSE loss remains; disable MSE (β=0) and verify only contrastive loss remains; confirm composite loss matches manual weighted sum.

## Limitations

- Temperature scaling parameter is sensitive; poor choice can lead to trivial solutions (all embeddings collapse to single point if τ too high) or numerical instability (log-sum-exp underflow if τ too low).
- Balance between InfoNCE and MSE is problem-dependent; no principled way to set α and β without grid search or validation tuning; unbalanced weights can cause one objective to dominate.
- Requires well-aligned positive pairs (peak-metadata correspondences); if ground truth pairings are noisy or incomplete, InfoNCE will learn misleading alignments.
- Composite loss assumes both modalities are meaningfully embeddable to the same dimensionality; highly heterogeneous data (e.g., sparse peaks vs. dense metadata) may require separate embedding spaces or dimension-specific losses.
- No changelog provided in repository; unclear which versions of PyTorch, GNPS datasets, or preprocessing steps were validated together.

## Evidence

- [other] CLERMS uses a novel composite loss function that combines InfoNCE loss and MSE loss to obtain good embeddings from peak information and metadata using a sinusoidal embedder within a transformer-based architecture.: "The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss has been proposed for the obtaining of good embedding from the peak"
- [other] Workflow steps for implementing the composite loss include defining InfoNCE with temperature scaling, defining MSE reconstruction loss, implementing weighted sum, wrapping in PyTorch module, and validating gradient flow.: "1. Define the InfoNCE contrastive loss function operating on peak-information and metadata embeddings with temperature scaling. 2. Define the MSE reconstruction loss function for embedding"
- [readme] CLERMS is designed for MS/MS spectra representation learning using contrastive learning and transformer architecture.: "CLERMS is a novel contrastive learning-based method for the representation of MS/MS spectra, which is based on transformer architecture."
- [readme] Data preprocessing and structural similarity calculation are required before model training with the composite loss.: "To get the structural similarity for the model training, we calculate the score from the input data."
