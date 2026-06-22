---
name: siamese-architecture-module-integration
description: Use when when refactoring a mass-spectrometry formula-prediction codebase that has deprecated a monolithic scoring function (FDRNet) and requires a modular, symmetric Siamese design to independently embed spectrum and molecular-formula features before combining them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - FIDDLE
  - PyTorch
  - msfiddle
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

# siamese-architecture-module-integration

## Summary

Reconstruct and integrate a Siamese neural architecture comprising a FormulaEncoder (embedding atom-count vectors into fixed-dimension representations) and a RescoreHead (computing element-wise products of spectrum and formula embeddings to generate confidence logits) into the model_tcn.py codebase. This skill applies when modernizing a legacy formula-prediction rescore pipeline from v1.0.0 to v2.0.0 and replacing removed FDRNet components.

## When to use

When refactoring a mass-spectrometry formula-prediction codebase that has deprecated a monolithic scoring function (FDRNet) and requires a modular, symmetric Siamese design to independently embed spectrum and molecular-formula features before combining them. Specifically use this skill when the task specifies removal of legacy FDRNet references and integration of separate FormulaEncoder and RescoreHead modules into model_tcn.py.

## When NOT to use

- Input atom-count vector is already a pre-computed embedding (use FormulaEncoder only if raw atom counts are provided).
- The model must support asymmetric (non-Siamese) architectures where spectrum and formula encoders differ in structure or dimensionality (this skill assumes symmetric 512-dim embeddings).
- Legacy v1.0.0 model checkpoints that rely on FDRNet are being deployed without version migration (Siamese modules are incompatible with FDRNet-based checkpoints).

## Inputs

- atom-count feature vectors (1D tensor or batch thereof, containing element counts)
- spectrum embeddings (512-dimensional vectors from prior spectrum encoder)
- model_tcn.py source file (with legacy FDRNet references)
- v2.0.0 checkpoint file (fiddle_rescore_orbitrap.pt or fiddle_rescore_qtof.pt)

## Outputs

- FormulaEncoder module (PyTorch nn.Module with L2-normalized 512-dim output)
- RescoreHead module (PyTorch nn.Module computing element-wise product logit)
- updated model_tcn.py with both modules instantiated and FDRNet removed
- scalar logit output per spectrum–formula pair (confidence score for rescoring)

## How to apply

First, design the FormulaEncoder as a PyTorch nn.Module that accepts atom-count feature vectors (e.g., counts of C, H, N, O, S, P, Cl, Br, F, I) and produces 512-dimensional embeddings with L2 normalization applied post-forward pass. Second, design the RescoreHead as a module that takes two 512-dimensional embeddings (z_spec from the spectrum encoder, z_form from the FormulaEncoder) and computes their element-wise product (⊙) to produce a scalar logit output. Third, update model_tcn.py to instantiate both modules and remove all references to the legacy FDRNet class. Fourth, validate the forward pass using synthetic tensors matching expected input shapes (e.g., batch of atom counts, batch of spectrum embeddings) to confirm output logits have correct dimensionality and that L2 normalization is applied correctly. Fifth, verify that model weights load correctly from the v2.0.0 checkpoint without shape mismatches.

## Related tools

- **FIDDLE** (Deep learning framework for formula prediction from MS/MS spectra; v2.0.0 release implements the Siamese rescore architecture with FormulaEncoder and RescoreHead) — https://github.com/JosieHong/FIDDLE
- **PyTorch** (Neural network library used to implement FormulaEncoder and RescoreHead modules as nn.Module subclasses)
- **msfiddle** (PyPI package providing CLI and Python API for FIDDLE inference; loads v2.0.0 rescore checkpoints and applies RescoreHead for confidence scoring) — https://github.com/josiehong/msfiddle

## Examples

```
from fiddle.model_tcn import FormulaEncoder, RescoreHead; encoder = FormulaEncoder(in_dim=10, out_dim=512); head = RescoreHead(in_dim=512); z_spec = torch.randn(8, 512); z_form = encoder(torch.randint(0, 20, (8, 10))); logit = head(z_spec, z_form); assert logit.shape == (8, 1)
```

## Evaluation signals

- FormulaEncoder output tensor has shape [batch_size, 512] with L2-norm ≈ 1.0 per sample (verify via torch.norm(output, p=2, dim=1))
- RescoreHead element-wise product output has shape [batch_size, 1] containing scalar logits
- Forward pass completes without shape mismatch errors on synthetic atom-count tensors (e.g., shape [batch_size, 10] for 10 elements)
- Model checkpoint loads without key errors after removing FDRNet references (verify via torch.load() and state_dict() keys)
- Rescore scores on held-out test spectra (e.g., CASMI 2016, EMBL-MCF 2.0 datasets) match or exceed v1.0.0 baseline performance metrics

## Limitations

- Siamese architecture assumes spectrum and formula embeddings are both 512-dimensional; incompatible with asymmetric designs or different embedding sizes without redesign.
- Element-wise product (⊙) is symmetric and commutative, so it cannot encode directional relationships between spectrum and formula features; alternatives (e.g., concatenation + MLP) may capture richer interactions.
- L2 normalization applied post-forward pass in FormulaEncoder may cause gradient flow inefficiencies; consider in-module normalization if training from scratch.
- No built-in handling for variable-length or sparse atom-count vectors; assumes fixed input dimensionality (typically 10 elements: C, H, N, O, S, P, Cl, Br, F, I).

## Evidence

- [other] The v2.0.0 rescore model implements a Siamese architecture that replaces the removed FDRNet class, incorporating a FormulaEncoder to embed atom-count vectors and a RescoreHead that computes element-wise products of spectrum and formula embeddings to generate logits.: "The v2.0.0 rescore model implements a Siamese architecture that replaces the removed FDRNet class, incorporating a FormulaEncoder to embed atom-count vectors and a RescoreHead that computes"
- [other] Design FormulaEncoder as a neural network layer that accepts atom-count feature vectors and produces 512-dimensional embeddings with L2 normalization.: "Design FormulaEncoder as a neural network layer that accepts atom-count feature vectors and produces 512-dimensional embeddings with L2 normalization"
- [other] Design RescoreHead as a module that computes element-wise product (⊙) of spectrum embedding z_spec and formula embedding z_form to produce a scalar logit output.: "Design RescoreHead as a module that computes element-wise product (⊙) of spectrum embedding z_spec and formula embedding z_form to produce a scalar logit output"
- [other] Integrate both modules into model_tcn.py, ensuring compatibility with the Siamese architecture. Remove references to the legacy FDRNet class and update module imports.: "Integrate both modules into model_tcn.py, ensuring compatibility with the Siamese architecture. Remove references to the legacy FDRNet class"
- [readme] Breaking change (v2.0.0): The rescore model has been redesigned (Siamese architecture), see details in CHANGELOG.md.: "Breaking change (v2.0.0): The rescore model has been redesigned (Siamese architecture)"
