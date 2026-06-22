---
name: contrastive-learning-encoder-design
description: Use when when you have mass spectrometry ion image data and need to learn meaningful low-dimensional representations through self-supervised contrastive learning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0769
  tools:
  - ResNet18
  - PyTorch or TensorFlow
  - kornia
  - boly_pytorch
derived_from:
- doi: 10.1021/acs.analchem.3c05002
  title: deepion
evidence_spans:
- Two augmented images are propagated through a pair of ResNet18-based encoders
- Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepion_cq
    doi: 10.1021/acs.analchem.3c05002
    title: deepion
  dedup_kept_from: coll_deepion_cq
schema_version: 0.2.0
---

# contrastive-learning-encoder-design

## Summary

Design and implement a paired ResNet18-based encoder architecture with shared parameters that processes augmented ion images to produce 512-dimensional representation vectors optimized for contrastive learning. This skill is essential when building low-dimensional representations of mass spectrometry imaging (MSI) data where meaningful spatial and spectral patterns must be preserved while avoiding representation collapse.

## When to use

When you have mass spectrometry ion image data and need to learn meaningful low-dimensional representations through self-supervised contrastive learning. Specifically: you have access to two augmented views of the same ion image (generated via distinct augmentation pipelines for COL or ISO modes), you want to maximize similarity between representations of augmented pairs while preventing representation collapse, and you need 512-dimensional intermediate embeddings before further dimensionality reduction to 20-dimensional output vectors.

## When NOT to use

- Ion images are not augmented—contrastive learning requires at least two distinct views of the same input to compute meaningful contrastive loss.
- You need direct spatial localization or class labels—this encoder learns unsupervised representations and does not inherently preserve pixel-level spatial structure.
- ResNet18 backbone is computationally prohibitive—consider lighter architectures if inference latency or memory is critical for your MSI dataset size.

## Inputs

- First augmented ion image (2D tensor, same spatial dimensions as MSI pixel grid)
- Second augmented ion image (2D tensor, same spatial dimensions as MSI pixel grid)
- ResNet18 architecture specification (PyTorch or TensorFlow model definition)

## Outputs

- Two 512-dimensional representation vectors (one per augmented image pair)
- Trained encoder weights with shared parameters
- Intermediate 512-d embeddings suitable for downstream projection and contrastive loss computation

## How to apply

Instantiate a single ResNet18 base model with shared parameters and modify its final fully connected layer to output 512-dimensional vectors instead of the default ImageNet class count. Pass the first augmented ion image through the encoder, then pass the second augmented image through the same encoder instance sequentially to obtain two distinct 512-dimensional representation vectors from identical weights. Connect these encodings to a Projection module and Prediction module that apply non-linear transformations and stop-gradient operations to prevent representation collapse. Train using contrastive loss that maximizes cosine similarity between the two 512-dimensional vectors while the stop-gradient operation prevents trivial solutions. Validate that forward passes consistently produce output tensors of shape [batch_size, 512] with meaningful numerical variation across the batch.

## Related tools

- **ResNet18** (Backbone encoder architecture that processes augmented ion images and outputs 512-dimensional vectors; weights are shared across both augmented image passes.)
- **PyTorch or TensorFlow** (Framework for defining ResNet18 architecture, instantiating shared encoder, and implementing forward passes.)
- **kornia** (Provides image augmentation primitives (color jitter, filtering) used to generate the two augmented views prior to encoder input.)
- **boly_pytorch** (Provides utilities for contrastive learning components including projection and prediction modules.)

## Examples

```
import torch; from torchvision.models import resnet18; encoder = resnet18(pretrained=False); encoder.fc = torch.nn.Linear(512, 512); aug_img1 = torch.randn(1, 3, H, W); aug_img2 = torch.randn(1, 3, H, W); z1 = encoder(aug_img1); z2 = encoder(aug_img2); print(f'Shape z1: {z1.shape}, Shape z2: {z2.shape}')
```

## Evaluation signals

- Output tensor shape is exactly [batch_size, 512] for each augmented image pass, confirming encoder outputs correct dimensionality.
- Cosine similarity between representation vectors of an augmented pair is high (typically > 0.7 after training) and higher than similarity between unrelated ion image pairs, indicating meaningful representations learned.
- Contrastive loss decreases monotonically during training, confirming optimization is reducing divergence between augmented pairs without collapse.
- Stop-gradient operation prevents encoder weights from updating during projection-module backpropagation, ensuring stable learning dynamics.
- Numerical values in 512-d vectors show non-trivial variance across the batch (not constant or near-zero), indicating the encoder is not collapsing to trivial solutions.

## Limitations

- Encoder design does not explicitly preserve spatial locality—learned representations are global and may not retain fine-grained pixel-level ion localization information.
- ResNet18 is relatively shallow; datasets with subtle spectral patterns may benefit from deeper or domain-specific architectures.
- Shared-weight encoder cannot capture asymmetric relationships between the two augmentation pipelines (COL vs. ISO augmentations); if augmentation strategies differ substantially, separate encoders may be more appropriate.
- 512-dimensional intermediate vectors must be further reduced to 20-dimensional outputs by a separate Dimensionality Reduction module for downstream tasks; raw 512-d outputs alone may not be suitable for visualization or clustering.

## Evidence

- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training"
- [other] Configure the encoder to output 512-dimensional vectors by modifying the final fully connected layer: "Configure the encoder to output 512-dimensional vectors by modifying the final fully connected layer"
- [other] Implement parameter sharing by instantiating a single ResNet18 model and passing both augmented images sequentially through the same encoder instance: "Implement parameter sharing by instantiating a single ResNet18 model and passing both augmented images sequentially through the same encoder instance"
- [readme] Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image: "Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image"
