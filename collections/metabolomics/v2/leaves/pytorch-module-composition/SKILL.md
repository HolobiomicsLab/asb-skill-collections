---
name: pytorch-module-composition
description: Use when when you need to extract both local spatial patterns and global
  long-range dependencies from sequential or spectral data (e.g., 1H NMR spectra),
  and neither CNNs nor Transformers alone are sufficient.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - Python
  - PyTorch+cu118
  - Anaconda
  - PyTorch
  - FlavorFormer
  techniques:
  - NMR
  license_tier: restricted
derived_from:
- doi: 10.1016/j.microc.2025.115372
  title: FlavorFormer
evidence_spans:
- Python 3.13.2 and Pytorch (version 2.7.0+cu118)
- Install [Anaconda](https://www.anaconda.com/).
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_flavorformer_cq
    doi: 10.1016/j.microc.2025.115372
    title: FlavorFormer
  dedup_kept_from: coll_flavorformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.microc.2025.115372
  all_source_dois:
  - 10.1016/j.microc.2025.115372
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# PyTorch Module Composition

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Combine independent PyTorch neural network modules (e.g., CNN feature extractors, Transformer encoders) into a unified architecture with explicit feature fusion points. This skill enables hybrid architectures that merge complementary processing paradigms to handle complex scientific data.

## When to use

When you need to extract both local spatial patterns and global long-range dependencies from sequential or spectral data (e.g., 1H NMR spectra), and neither CNNs nor Transformers alone are sufficient. Use this skill to fuse a CNN's local receptive fields with a Transformer's attention-based global context modeling.

## When NOT to use

- Input is already a hand-crafted feature table or manually engineered descriptor set; use a simpler feedforward network instead.
- Spectral data is purely local (e.g., narrow peaks with no long-range correlations); a CNN-only model will likely suffice.
- Computational budget is severely constrained; Transformer self-attention scales quadratically with sequence length, so very long spectra may be impractical without dimensionality reduction.

## Inputs

- 1H NMR spectral tensors (shape: batch × sequence_length × spectral_features)
- PyTorch nn.Module subclasses (CNN layers, Transformer encoder blocks)

## Outputs

- Unified PyTorch nn.Module combining CNN and Transformer
- Encoded feature representations (shape: batch × embedding_dim)
- Intermediate feature maps at fusion points for debugging

## How to apply

First, define a CNN feature extractor using stacked convolutional layers to capture local patterns in the input spectra (e.g., 1H NMR). Second, implement a multi-head Transformer encoder block to model global dependencies across the spectral sequence. Third, determine feature fusion points where CNN outputs are passed as input to the Transformer (or vice versa), ensuring tensor shapes and embedding dimensions are compatible. Fourth, integrate both components into a single parent module with a forward() method that orchestrates the data flow through CNN → Transformer → output. Finally, verify the composed module accepts raw spectral tensors (e.g., 1H NMR arrays) and outputs encoded representations (fixed-dimension feature vectors) that are compatible with downstream prediction heads (e.g., bi-encoder, cross-encoder).

## Related tools

- **PyTorch** (Core framework for defining, composing, and training neural network modules; provides nn.Module base class and functional building blocks) — https://pytorch.org
- **FlavorFormer** (Reference implementation of hybrid CNN-Transformer composition for 1H NMR compound identification; demonstrates feature fusion and encoder head integration) — https://github.com/yfWang01/FlavorFormer

## Examples

```
# Pseudocode: compose CNN + Transformer for 1H NMR
import torch.nn as nn
cnn_extractor = nn.Sequential(nn.Conv1d(1, 64, 5), nn.ReLU(), nn.Conv1d(64, 128, 5), nn.AdaptiveAvgPool1d(256))
transformer_encoder = nn.TransformerEncoder(nn.TransformerEncoderLayer(d_model=128, nhead=8), num_layers=2)
class HybridModel(nn.Module):
  def forward(self, spectra):
    local_feat = self.cnn_extractor(spectra)  # (batch, 128, 256)
    local_feat = local_feat.permute(2, 0, 1)  # (seq, batch, emb)
    global_feat = self.transformer_encoder(local_feat)
    return global_feat.permute(1, 0, 2).mean(1)  # (batch, 128)
```

## Evaluation signals

- The composed module's forward() method accepts raw 1H NMR spectral tensors and returns encoded feature vectors without shape errors or broadcasting failures.
- Intermediate tensor shapes at each fusion point match expected dimensions (CNN output embedding_dim == Transformer input embedding_dim).
- Output from the composed module has fixed dimensionality (batch × embedding_dim) suitable for downstream bi-encoder or cross-encoder heads.
- Gradient flow through both CNN and Transformer components during backpropagation (check with torch.autograd.grad() or loss.backward() + parameter.grad inspection).
- Ablation: removing either CNN or Transformer component degrades performance on held-out compound identification task, confirming both contribute to predictions.

## Limitations

- Feature fusion points must be manually specified; incorrect dimensionality matching will cause runtime errors. No automatic shape inference across module boundaries.
- Transformer self-attention is quadratic in sequence length; very long 1H NMR spectra (>1000 frequency points) may exceed GPU memory without prior dimensionality reduction (e.g., binning, PCA).
- No built-in mechanism for learning optimal fusion weights; equal concatenation or sum fusion may not be optimal; consider learnable gating or weighted combination layers.
- Composed module increases total parameters compared to CNN or Transformer alone, requiring larger training datasets to avoid overfitting.

## Evidence

- [other] Define a CNN feature extractor using convolutional layers to capture local patterns in 1H NMR spectra: "Define a CNN feature extractor using convolutional layers to capture local patterns in 1H NMR spectra."
- [other] Implement a multi-head Transformer encoder block to model global dependencies across the spectral sequence: "Implement a multi-head Transformer encoder block to model global dependencies across the spectral sequence."
- [other] Integrate CNN and Transformer components into a unified hybrid encoder module with appropriate feature fusion points: "Integrate the CNN and Transformer components into a unified hybrid encoder module with appropriate feature fusion points."
- [other] Verify the module accepts 1H NMR spectral tensors and outputs encoded representations compatible with downstream bi-encoder and cross-encoder heads: "Verify the module accepts 1H NMR spectral tensors and outputs encoded representations compatible with downstream bi-encoder and cross-encoder heads."
- [intro] Hybrid CNN and Transformer architecture to capture local features and global dependencies from 1H NMR spectra: "incorporating a hybrid CNN and Transformer architecture to capture both local features and global dependencies from 1H NMR spectra"
