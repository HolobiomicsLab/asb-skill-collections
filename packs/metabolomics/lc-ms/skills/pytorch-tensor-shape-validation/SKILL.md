---
name: pytorch-tensor-shape-validation
description: Use when after implementing a transformer encoder backbone with masking mechanisms in PyTorch, before training on mass spectra data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - PyTorch 2.2
  - PyTorch
  - Python
  - Anaconda
  - Git
  - Python 3.12
  - MSBERT
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.4c02426
  title: MSBERT
evidence_spans:
- '[Pytorch](https://pytorch.org/) 2.2'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pytorch-tensor-shape-validation

## Summary

Verify correct tensor shape transformations through the forward pass of a PyTorch model to ensure encoder and masking modules are correctly wired to contrastive loss computation. This skill detects dimensional mismatches and data flow errors early in model development.

## When to use

After implementing a transformer encoder backbone with masking mechanisms in PyTorch, before training on mass spectra data. Use this skill when integrating multiple neural network components (encoder, masking, contrastive loss) to catch shape incompatibilities that would otherwise cause runtime errors during the first training epoch.

## When NOT to use

- Model architecture is already trained and in production; use this during development, not post-deployment.
- Input is already a confirmed, tested feature embedding; this skill is for pre-training validation, not inference.
- Tensor shapes are externally guaranteed by framework (e.g., using strict type hints or compiled graphs that reject mismatches).

## Inputs

- PyTorch model with transformer encoder backbone
- Batch of tandem mass spectra (as tensors)
- Model configuration (attention heads, hidden dimensions, masking probability)

## Outputs

- Validated tensor shape trace through encoder
- Confirmed embedding dimensions for contrastive loss input
- Shape mismatch report (if any)

## How to apply

Construct a small batch of representative input tensors (e.g., a few tandem mass spectra samples) and trace them through the full forward pass: original spectra → transformer encoder → embedding output, and separately through the masked spectra pathway. Record the shape at each stage (batch size, sequence length, embedding dimension). Verify that both pathways produce identically-shaped embeddings suitable for contrastive loss computation (e.g., both outputs should have shape [batch_size, embedding_dim]). Use PyTorch's `.shape` attribute and print statements or assertions to document expected vs. actual dimensions. This validation should occur before training loop integration to avoid wasting compute on divergent tensor flows.

## Related tools

- **PyTorch 2.2** (Primary framework for tensor manipulation, forward pass execution, and shape introspection via .shape attribute and debugging utilities) — https://pytorch.org/
- **Python 3.12** (Language runtime for test scripts and debugging logic)
- **MSBERT** (Reference implementation containing transformer encoder, masking module, and contrastive loss integration to validate against) — https://github.com/zhanghailiangcsu/MSBERT

## Examples

```
import torch; from model.MSBERTModel import MSBERT; model = MSBERT(100002, 512, 6, 16, 0, 100, 3); test_batch = torch.randint(0, 100002, (16, 256)); out_orig = model(test_batch); out_masked = model(test_batch); assert out_orig.shape == out_masked.shape == torch.Size([16, 512]), f'Shape mismatch: {out_orig.shape} vs {out_masked.shape}'
```

## Evaluation signals

- Both masked and unmasked spectra produce embeddings with identical shapes (batch_size × embedding_dim)
- Embedding dimension matches the configured hidden size (e.g., 512 for MSBERT) across all samples
- No shape-related exceptions are raised during forward pass execution on a test batch
- Contrastive loss function accepts both embedding tensors without shape mismatch errors
- Tensor flow diagram (printed shapes at each layer) shows no unexpected dimension reductions or expansions

## Limitations

- Shape validation does not verify numerical correctness or semantic quality of embeddings; it only checks dimensional compatibility.
- Does not catch issues related to batch normalization or dropout behavior that may emerge only during distributed training.
- Validation on small test batches may not expose shape bugs that appear with larger batch sizes or edge cases (e.g., very long spectra sequences).

## Evidence

- [intro] Verify the encoder and masking module are correctly wired to the contrastive loss computation by validating tensor shape transformations through the forward pass.: "Verify the encoder and masking module are correctly wired to the contrastive loss computation by validating tensor shape transformations through the forward pass."
- [intro] MSBERT employed a transformer encoder backbone and leverages the randomness of masking to construct positive samples for contrastive learning during training on the GNPS dataset.: "MSBERT employs a transformer encoder backbone and leverages the randomness of masking to construct positive samples for contrastive learning"
- [intro] Implement the transformer-encoder backbone architecture in PyTorch 2.2 with configurable attention heads and hidden dimensions.: "Implement the transformer-encoder backbone architecture in PyTorch 2.2 with configurable attention heads and hidden dimensions."
- [readme] MSBERT used the transformer encoder as the backbone and take advantage of the randomness of the mask to construct positive samples for contrastive learning.: "MSBERT used the transformer encoder as the backbone and take advantage of the randomness of the mask to construct positive samples for contrastive learning."
