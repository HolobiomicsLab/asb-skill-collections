---
name: parameter-sharing-in-siamese-networks
description: Use when when processing paired augmented versions of the same input (e.g., two augmented ion images in COL or ISO mode) and you need to learn meaningful low-dimensional representations via contrastive loss.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3500
  - http://edamontology.org/topic_3520
  tools:
  - ResNet18
  - PyTorch / TensorFlow
  - Contrastive loss function
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

# parameter-sharing-in-siamese-networks

## Summary

Implement a Siamese encoder architecture where two parallel branches share identical weights to process paired augmented inputs and generate matched-dimensional representation vectors. This approach enforces consistent feature extraction across both branches, enabling contrastive learning on augmented ion images in mass spectrometry imaging.

## When to use

When processing paired augmented versions of the same input (e.g., two augmented ion images in COL or ISO mode) and you need to learn meaningful low-dimensional representations via contrastive loss. Parameter sharing is essential to avoid duplicate parameters and ensure that both augmentations are mapped through the same learned feature space, preventing representation collapse during optimization.

## When NOT to use

- When you have non-paired or unpaired inputs and cannot generate reliable augmentations.
- When the two inputs require fundamentally different feature extraction pathways (use separate encoders instead).
- When memory or compute constraints require model reduction; parameter sharing is most beneficial with moderate-to-large architectures.

## Inputs

- Two augmented ion images (e.g., post-T_COL or T_ISO transformation)
- ResNet18 model architecture definition
- Input image shape and number of ions (P)

## Outputs

- Two 512-dimensional representation vectors (one per augmented image)
- Feature maps at intermediate layers (optional, for debugging)

## How to apply

Define a single ResNet18 base model instance using PyTorch or TensorFlow, then configure its final fully connected layer to output 512-dimensional vectors (matching the required representation size). Pass both augmented ion images sequentially through this single encoder instance rather than instantiating two separate models. Verify that each forward pass produces a 512-dimensional output tensor and that gradients flow symmetrically through both branches during backpropagation. The shared weights ensure that identical spatial patterns in either augmented image activate the same learned filters, which is critical for the contrastive loss to maximize similarity between the two augmentations of the same original ion image.

## Related tools

- **ResNet18** (Base convolutional encoder architecture with shared parameters for extracting spatial features from augmented ion images)
- **PyTorch / TensorFlow** (Deep learning framework for implementing the shared-weight encoder and forward passes)
- **Contrastive loss function** (Loss metric that maximizes similarity between the two 512-dimensional vectors from paired augmentations)

## Examples

```
# Instantiate shared ResNet18 encoder, configure for 512-dim output, pass both augmented images sequentially
import torch
from torchvision.models import resnet18

encoder = resnet18(pretrained=False)
encoder.fc = torch.nn.Linear(512, 512)  # Output 512-dim vectors

aug_image_1 = torch.randn(1, 3, 224, 224)
aug_image_2 = torch.randn(1, 3, 224, 224)

rep_1 = encoder(aug_image_1)  # Shape: [1, 512]
rep_2 = encoder(aug_image_2)  # Shape: [1, 512]
# Both forward passes use identical shared weights
```

## Evaluation signals

- Both forward passes through the shared encoder produce output tensors with shape [batch_size, 512].
- Gradient norms are non-zero and symmetric for both branches during backpropagation; no branch receives zero gradients.
- Weight parameters of the encoder are identical before and after processing both augmentations (weights are not duplicated across branches).
- Contrastive loss converges during training, indicating that the shared representation space is learning to map similar augmentations close together.
- Cosine similarity between the two 512-dimensional vectors is high (>0.7 typical) for augmentations of the same ion image after training.

## Limitations

- Parameter sharing assumes that both augmented inputs are semantically equivalent; if augmentations are too dissimilar, the shared encoder may struggle to align them.
- The 512-dimensional bottleneck is fixed in this architecture; different downstream tasks may require different representation sizes.
- Shared parameters reduce model flexibility; if one augmented branch has significantly different noise characteristics, the encoder may not adapt to both equally.
- Stop-gradient operations are required in the projection/prediction modules to prevent representation collapse; parameter sharing alone is insufficient.

## Evidence

- [intro] Parameter sharing ensures consistent feature learning for contrastive loss in ion image representation: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors."
- [readme] Shared encoder applied to sequential augmented image inputs in COL and ISO modes: "The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO"
- [intro] Contrastive loss requires shared feature space to maximize similarity between augmentations: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training."
- [readme] Shared parameters prevent collapse and ensure meaningful representation learning: "Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image"
