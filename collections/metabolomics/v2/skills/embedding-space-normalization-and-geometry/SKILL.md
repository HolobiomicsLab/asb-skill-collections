---
name: embedding-space-normalization-and-geometry
description: Use when when designing a Siamese or multi-branch neural architecture where two or more embedding streams (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - FIDDLE
  - msfiddle
  - PyTorch
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle_cq
schema_version: 0.2.0
---

# embedding-space-normalization-and-geometry

## Summary

Apply L2 normalization to fixed-dimension neural network embeddings and use element-wise geometric operations (e.g., Hadamard product) to combine normalized embedding spaces for downstream prediction tasks. This ensures bounded embedding magnitudes and enables interpretable feature interactions in multi-modal architectures.

## When to use

When designing a Siamese or multi-branch neural architecture where two or more embedding streams (e.g., spectrum embeddings and formula embeddings) must be combined to produce a scalar logit or confidence score, and you need embeddings with controlled magnitude to enable stable element-wise operations and interpretable feature interactions.

## When NOT to use

- Input embeddings are already sparse or categorical without continuous representation; L2 normalization is designed for dense continuous vectors.
- The task requires independent prediction from a single modality (e.g., spectrum-only or formula-only); Siamese geometry is unnecessary when fusion is not the goal.
- Atom counts or spectrum features are missing, incomplete, or inconsistent across the dataset; normalization cannot recover from missing modalities.

## Inputs

- atom-count feature vectors (variable-length discrete feature counts for molecular elements)
- spectrum embeddings (fixed-dimension dense vectors, typically 512 dimensions post-normalization)
- batch of MS/MS spectra with precursor m/z and collision energy metadata

## Outputs

- formula embeddings (512-dimensional L2-normalized vectors)
- rescoring logits (scalar confidence scores per spectrum–formula pair)
- refined formula candidate rankings with confidence scores

## How to apply

Design each embedding branch (e.g., FormulaEncoder) to output fixed-dimension embeddings (e.g., 512 dimensions) with L2 normalization applied at the output layer to constrain the L2 norm to 1.0. In the fusion head (e.g., RescoreHead), compute the element-wise product (Hadamard product, ⊙) of the normalized spectrum embedding z_spec and normalized formula embedding z_form to produce a combined feature vector, then pass this through a final linear layer or pooling operation to generate the scalar logit. L2 normalization ensures that magnitude variations do not dominate the dot-product-like interaction; the element-wise product preserves per-dimension correlation information. Validate the forward pass with synthetic tensors matching expected batch sizes and embedding dimensions to confirm output shapes, normalization bounds (||z|| ≈ 1.0), and logit range.

## Related tools

- **FIDDLE** (Deep learning framework implementing the FormulaEncoder and RescoreHead modules with L2 normalization for molecular formula prediction from MS/MS spectra) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (PyPI package wrapping FIDDLE's Siamese architecture and providing CLI and Python API for batch prediction with normalized embedding inference) — https://github.com/josiehong/msfiddle
- **PyTorch** (Deep learning framework for implementing neural network modules (FormulaEncoder, RescoreHead) with L2 normalization via torch.nn.functional.normalize)

## Examples

```
from torch.nn import Module, Linear, functional as F; embeddings = F.normalize(encoder(atom_counts), p=2, dim=1); logits = (embeddings * formula_embeddings).sum(dim=1, keepdim=True)
```

## Evaluation signals

- Embedding L2 norms are approximately 1.0 (within ±0.01) after normalization for all batch samples.
- Forward pass produces scalar logit outputs with expected batch dimensions (batch_size, 1).
- Element-wise product (Hadamard product) of normalized embeddings has full rank (no dimension collapse) and non-zero gradient flow during backpropagation.
- Ranking of refined formula candidates by rescoring logits matches top-k accuracy benchmarks on held-out validation spectra (e.g., CASMI or NIST datasets).
- Ablation study confirming that removal of L2 normalization increases training instability or reduces top-k accuracy on external benchmarks.

## Limitations

- L2 normalization discards magnitude information; if the magnitude of an embedding carries semantic meaning (e.g., confidence in the spectrum), that signal is lost.
- Element-wise products require embeddings of identical dimension; mismatched dimensions between spectrum and formula embeddings will cause runtime errors.
- Siamese architecture assumes both modalities (spectrum and formula) are present and well-represented; sparse or missing modalities cannot be processed.
- Rescoring logits are not calibrated probabilities; they should not be interpreted as absolute confidence without additional post-hoc calibration.
- The v2.0.0 rescore model replaces the legacy FDRNet class; checkpoints from earlier versions are not compatible and must be retrained.

## Evidence

- [other] Design FormulaEncoder as a neural network layer that accepts atom-count feature vectors and produces 512-dimensional embeddings with L2 normalization.: "Design FormulaEncoder as a neural network layer that accepts atom-count feature vectors and produces 512-dimensional embeddings with L2 normalization"
- [other] RescoreHead computes element-wise product (⊙) of spectrum embedding z_spec and formula embedding z_form to produce a scalar logit output.: "Design RescoreHead as a module that computes element-wise product (⊙) of spectrum embedding z_spec and formula embedding z_form to produce a scalar logit output"
- [other] The v2.0.0 rescore model implements a Siamese architecture that replaces the removed FDRNet class, incorporating a FormulaEncoder to embed atom-count vectors and a RescoreHead that computes element-wise products of spectrum and formula embeddings to generate logits.: "The v2.0.0 rescore model implements a Siamese architecture that replaces the removed FDRNet class, incorporating a FormulaEncoder to embed atom-count vectors and a RescoreHead that computes"
- [other] Validate forward pass with synthetic atom-count and spectrum embedding tensors to confirm output shapes and normalization.: "Validate forward pass with synthetic atom-count and spectrum embedding tensors to confirm output shapes and normalization"
- [readme] Breaking change (v2.0.0): The rescore model has been redesigned (Siamese architecture), see details in CHANGELOG.md.: "Breaking change (v2.0.0): The rescore model has been redesigned (Siamese architecture)"
