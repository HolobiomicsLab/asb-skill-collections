---
name: tensor-operation-element-wise-product
description: Use when you have two embedding tensors of identical shape (e.g., both 512-dimensional) and need to produce a fused representation that captures multiplicative interactions between modalities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - FIDDLE
  - PyTorch
  techniques:
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Tensor Operation: Element-wise Product

## Summary

Compute the element-wise (Hadamard) product of two equal-shaped tensors to combine learned representations, commonly used in neural architectures to fuse spectrum and formula embeddings into joint feature vectors.

## When to use

Apply this skill when you have two embedding tensors of identical shape (e.g., both 512-dimensional) and need to produce a fused representation that captures multiplicative interactions between modalities. In FIDDLE's rescore architecture, use element-wise product when combining spectrum embeddings (z_spec) and formula embeddings (z_form) to generate a joint logit for ranking molecular formula candidates.

## When NOT to use

- Input tensors have mismatched shapes or ranks — reshape or broadcast explicitly first.
- One or both input tensors are sparse or contain many zeros — sparse element-wise product may be inefficient; consider dense alternatives.
- You need additive (not multiplicative) fusion — use concatenation or summation instead.

## Inputs

- Spectrum embedding tensor (e.g., shape [batch_size, 512] or [512])
- Formula embedding tensor (e.g., shape [batch_size, 512] or [512], L2-normalized atom-count representation)

## Outputs

- Fused embedding tensor (same shape as inputs, e.g., [batch_size, 512])
- Prediction logit (scalar or shape [batch_size, 1] after optional linear projection)

## How to apply

Define element-wise product as the operation ⊙ where each element of the output tensor is the product of the corresponding elements from the two input tensors: output[i] = z_spec[i] × z_form[i]. In PyTorch, implement this using the `*` operator on tensors or `torch.mul()`. Ensure both input tensors share the same shape and dtype before multiplication. After the element-wise product, optionally apply a final linear projection or scalar logit head to convert the fused embedding into a prediction score. Validate the operation by checking that output shape matches input shape and that values reflect the multiplicative combination (e.g., zero in either input yields zero in output).

## Related tools

- **FIDDLE** (Reference implementation: uses element-wise product in RescoreHead module to combine spectrum and formula embeddings for molecular formula rescoring) — https://github.com/JosieHong/FIDDLE
- **PyTorch** (Tensor computation framework supporting element-wise multiplication via `torch.mul()` or `*` operator)

## Examples

```
import torch; z_spec = torch.randn(8, 512); z_form = torch.randn(8, 512); fused = z_spec * z_form; logit = torch.sum(fused, dim=1, keepdim=True)
```

## Evaluation signals

- Output tensor shape matches input shape exactly (e.g., [batch_size, 512] in, [batch_size, 512] out).
- Element-wise products are computed correctly: spot-check a few elements by hand (e.g., output[0] ≈ z_spec[0] × z_form[0]).
- Zero-preservation: if either input contains zero at index i, output[i] must be zero.
- Downstream logit or loss values are finite and within expected range (not NaN or Inf) after product and projection.
- Forward pass on synthetic tensors (e.g., ones, random normal, known constants) produces expected outputs without shape errors.

## Limitations

- Element-wise product is sensitive to the magnitude of input embeddings; if embeddings are not normalized or scaled appropriately, the product may saturate or vanish.
- No learned weights in the operation itself — the interaction pattern is fixed once embeddings are fixed; consider learned attention or gating if adaptive fusion is needed.
- Binary zeros in either input will zero out the entire corresponding output element, which may lead to loss of information if not carefully managed.

## Evidence

- [other] RescoreHead module that computes element-wise product: "Design RescoreHead as a module that computes element-wise product (⊙) of spectrum embedding z_spec and formula embedding z_form to produce a scalar logit output."
- [other] FormulaEncoder produces 512-dimensional L2-normalized embeddings: "Design FormulaEncoder as a neural network layer that accepts atom-count feature vectors and produces 512-dimensional embeddings with L2 normalization."
- [readme] Siamese architecture context for FIDDLE v2.0.0: "The rescore model has been redesigned (Siamese architecture), see details in [CHANGELOG.md](./CHANGELOG.md)."
- [readme] FIDDLE predicts molecular formulas from MS/MS spectra: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra."
