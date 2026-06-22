---
name: neural-network-layer-design-and-implementation
description: Use when when replacing deprecated model components (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0611
  - http://edamontology.org/topic_3957
  tools:
  - FIDDLE
  - PyTorch
  - msfiddle
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

# neural-network-layer-design-and-implementation

## Summary

Design and implement custom neural network modules (such as FormulaEncoder and RescoreHead) that transform domain-specific input vectors into fixed-dimension embeddings and combine multiple embeddings to produce scalar logits. This skill is essential when adapting deep learning architectures to novel molecular mass spectrometry tasks where off-the-shelf layers do not capture the required input-output relationships.

## When to use

When replacing deprecated model components (e.g., FDRNet) with a new Siamese architecture, you have domain-specific input vectors (atom-count features, spectrum embeddings) that must be transformed into fixed-dimension representations, and you need to combine embeddings from multiple modalities (formula and spectrum) to produce a single confidence score or logit. Concrete trigger: task requires element-wise product of spectrum and formula embeddings to generate predictions, or you need L2-normalized embedding outputs from atom-count feature vectors.

## When NOT to use

- Input embeddings are already aligned in a single shared space and do not require separate encoder modules—directly use element-wise operations without custom layer design.
- Output is a dense prediction matrix or multi-class probability distribution rather than a scalar logit—use standard classification heads instead.
- Atom-count vectors have irregular length and cannot be pre-padded to fixed dimension—apply sequence models (RNN/Transformer) instead of fixed-size feedforward layers.

## Inputs

- atom-count feature vectors (dense tensors of shape [batch_size, num_atom_types])
- spectrum embeddings (512-dimensional L2-normalized tensors of shape [batch_size, 512])
- PyTorch model configuration file (.yml) specifying layer dimensions and hyperparameters

## Outputs

- FormulaEncoder: 512-dimensional L2-normalized formula embeddings (shape [batch_size, 512])
- RescoreHead: scalar logits or confidence scores (shape [batch_size, 1] or [batch_size])
- Updated model_tcn.py with integrated Siamese architecture

## How to apply

1. **Define FormulaEncoder** as a neural network module that accepts variable-length atom-count feature vectors and outputs fixed 512-dimensional embeddings with L2 normalization applied post-inference to ensure unit norm; use fully connected layers with appropriate activation functions (e.g., ReLU) and optional dropout for regularization. 2. **Define RescoreHead** as a module that takes pre-computed spectrum and formula embeddings (both 512-dimensional, L2-normalized), computes their element-wise product (⊙), and passes the result through a final fully connected layer to produce a scalar logit. 3. **Integrate both modules into model_tcn.py** by importing them as separate classes and instantiating them within the main model's constructor; ensure forward pass is called in the correct order (FormulaEncoder → product computation → RescoreHead). 4. **Remove legacy imports and references** to the old FDRNet class and update module initialization to match the new Siamese architecture. 5. **Validate forward pass** with synthetic atom-count tensors (e.g., shape [batch_size, num_atoms]) and spectrum embedding tensors (e.g., shape [batch_size, 512]) to confirm output shapes (scalar logits) and verify L2 normalization is applied correctly.

## Related tools

- **FIDDLE** (Deep learning framework for predicting molecular formulas from MS/MS spectra; provides the Siamese rescore architecture context and v2.0.0 redesign requiring custom layer implementation.) — https://github.com/JosieHong/FIDDLE
- **PyTorch** (Deep learning library for implementing FormulaEncoder and RescoreHead modules using torch.nn.Module inheritance and tensor operations (element-wise product, L2 normalization).)
- **msfiddle** (Python API and CLI package that wraps FIDDLE models including the redesigned rescore architecture; accepts MGF input spectra and applies the integrated custom modules.) — https://github.com/josiehong/msfiddle

## Examples

```
```python
from torch import nn
import torch.nn.functional as F

class FormulaEncoder(nn.Module):
    def __init__(self, input_dim=20, output_dim=512):
        super().__init__()
        self.fc = nn.Linear(input_dim, output_dim)
    def forward(self, atom_counts):
        x = self.fc(atom_counts)
        return F.normalize(x, p=2, dim=1)

class RescoreHead(nn.Module):
    def __init__(self, embedding_dim=512):
        super().__init__()
        self.logit_layer = nn.Linear(embedding_dim, 1)
    def forward(self, z_spec, z_form):
        product = z_spec * z_form
        return self.logit_layer(product)

encoder = FormulaEncoder()
head = RescoreHead()
atom_counts = torch.randn(8, 20)
z_form = encoder(atom_counts)
z_spec = torch.randn(8, 512)
z_spec = F.normalize(z_spec, p=2, dim=1)
logits = head(z_spec, z_form)
```
```

## Evaluation signals

- FormulaEncoder output shape is [batch_size, 512] and L2 norm of each embedding row is 1.0 (within floating-point tolerance ~1e-5).
- RescoreHead element-wise product operation correctly combines spectrum and formula embeddings: verify output logit reflects multiplicative interaction of both modalities.
- Forward pass runs without shape mismatch errors and produces scalar logits (not multi-dimensional tensors) from atom-count input vectors.
- Integration test: synthetic atom-count tensor [8, 20] (8 batch, 20 atom types) produces output [8, 1], matching expected logit shape.
- Model checkpoint loads successfully and inference on validation spectra (e.g., caffeine Orbitrap spectrum) produces confidence scores in expected range [0, ~1] after sigmoid or softmax.

## Limitations

- FormulaEncoder requires fixed atom-count vector dimension; variable-length or sparse atom counts require padding or embedding lookup strategies not described in the task.
- L2 normalization in FormulaEncoder assumes embeddings should lie on a unit hypersphere; if downstream operations require unbounded logits, normalization may constrain model capacity.
- Element-wise product in RescoreHead is symmetric and commutative; if asymmetric fusion of spectrum and formula information is required (e.g., attention), this design may be suboptimal.
- No mention of regularization (e.g., dropout, weight decay) in the task specification; overfitting risk on small validation sets if hyperparameters are not tuned.

## Evidence

- [other] Design FormulaEncoder as a neural network layer that accepts atom-count feature vectors and produces 512-dimensional embeddings with L2 normalization.: "Design FormulaEncoder as a neural network layer that accepts atom-count feature vectors and produces 512-dimensional embeddings with L2 normalization."
- [other] Design RescoreHead as a module that computes element-wise product (⊙) of spectrum embedding z_spec and formula embedding z_form to produce a scalar logit output.: "Design RescoreHead as a module that computes element-wise product (⊙) of spectrum embedding z_spec and formula embedding z_form to produce a scalar logit output."
- [readme] The rescore model has been redesigned (Siamese architecture), see details in CHANGELOG.md: "The rescore model has been redesigned (Siamese architecture)"
- [other] Integrate both modules into model_tcn.py, ensuring compatibility with the Siamese architecture.: "Integrate both modules into model_tcn.py, ensuring compatibility with the Siamese architecture."
- [other] Validate forward pass with synthetic atom-count and spectrum embedding tensors to confirm output shapes and normalization.: "Validate forward pass with synthetic atom-count and spectrum embedding tensors to confirm output shapes and normalization."
