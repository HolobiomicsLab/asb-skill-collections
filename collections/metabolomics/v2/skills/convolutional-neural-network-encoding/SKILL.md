---
name: convolutional-neural-network-encoding
description: Use when you have pairs of augmented ion images from mass spectrometry imaging data and need to generate low-dimensional representation vectors that maximize similarity between augmentations of the same image while avoiding representation collapse.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3173
  tools:
  - ResNet18
  - PyTorch
  - torchvision
derived_from:
- doi: 10.1021/acs.analchem.3c05002
  title: deepion
evidence_spans:
- Two augmented images are propagated through a pair of ResNet18-based encoders
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepion
    doi: 10.1021/acs.analchem.3c05002
    title: deepion
  dedup_kept_from: coll_deepion
schema_version: 0.2.0
---

# convolutional-neural-network-encoding

## Summary

Use a shared-weight ResNet18 encoder to transform pairs of augmented ion images into fixed 512-dimensional representation vectors for contrastive learning. This skill is essential when building self-supervised embeddings of mass spectrometry imaging (MSI) data that preserve spatial and intensity relationships across augmented views.

## When to use

Apply this skill when you have pairs of augmented ion images from mass spectrometry imaging data and need to generate low-dimensional representation vectors that maximize similarity between augmentations of the same image while avoiding representation collapse. Use it as the core encoding stage in a contrastive learning pipeline for co-localized ion or isotope discovery tasks.

## When NOT to use

- Input data is already a pre-computed 512-dimensional feature matrix or embedding table; skip directly to downstream projection or dimensionality reduction.
- Augmented image pairs are not available or augmentation pipeline has not been applied; apply data augmentation (COL or ISO mode) before encoding.
- You require per-pixel or spatial feature maps rather than global image representations; use intermediate convolutional activations instead of the final 512-D output.

## Inputs

- augmented ion image tensor pair (batch_size × channels × height × width)
- ResNet18 architecture configuration (input dimensions, output feature dimension = 512)

## Outputs

- two 512-dimensional representation vector tensors (batch_size × 512 each)
- encoder module with learned convolutional and pooling weights

## How to apply

Instantiate a ResNet18 architecture configured to accept ion image tensors and output 512-dimensional feature vectors. Use a single ResNet18 instance with shared parameters to process both augmented images sequentially, ensuring that the same learned weights constrain both encodings. Configure selective layer training or freezing based on your contrastive learning objective (e.g., freeze earlier convolutional blocks if using transfer learning from natural images). Pass each augmented ion image through the shared encoder in the forward pass to produce two distinct 512-dimensional vectors. Validate output tensor shapes match [batch_size, 512] and check for numerical stability (no NaNs, reasonable ranges for representation norms). The shared-weight design forces the encoder to learn invariances that hold across the augmentation transformations (color jitter, Poisson noise, filtering, missing values), enabling the downstream projection and prediction modules to distinguish true signal from augmentation artifacts via contrastive loss.

## Related tools

- **ResNet18** (Shared-weight convolutional encoder that processes augmented ion images and outputs 512-dimensional feature vectors)
- **PyTorch** (Deep learning framework for implementing and training the ResNet18 encoder module)
- **torchvision** (Provides ResNet18 pre-trained architecture definitions and convolutional building blocks)

## Examples

```
from torchvision.models import resnet18; import torch; encoder = resnet18(pretrained=False); encoder.fc = torch.nn.Linear(512, 512); z1 = encoder(img_aug_1); z2 = encoder(img_aug_2)
```

## Evaluation signals

- Output tensor shape is exactly [batch_size, 512] for both augmented image encodings with no singleton dimensions or rank mismatches.
- Representation vectors are numerically stable: no NaNs, no Inf values, and L2 norms fall within expected range (e.g., 5–50 for typical initialization and early training).
- Contrastive loss decreases during training, indicating that the encoder is learning to maximize cosine similarity between augmentations of the same image.
- The two 512-D vectors from the same original image produce higher cosine similarity than vectors from different images (contrastive signal is working).
- Gradient flow through the encoder is non-zero during backpropagation; frozen layers produce zero gradients, trainable layers produce non-zero gradients as configured.

## Limitations

- ResNet18 was originally trained on natural images (ImageNet); transfer to ion images may require careful layer freezing and learning rate tuning to avoid catastrophic forgetting of general features.
- The fixed 512-dimensional output may not capture fine-grained spatial details if the original ion images are high-resolution; intermediate feature maps can be extracted if needed.
- Shared-weight encoding assumes both augmented images have the same semantic content; if augmentation strategies are too aggressive (e.g., excessive missing values), the encoder may fail to learn meaningful invariances.
- The skill requires paired augmented data; preprocessing must guarantee that two augmented versions of each ion image are available in aligned order during training.

## Evidence

- [other] The Encoder module accepts two augmented ion images and propagates them through a pair of ResNet18-based encoders with shared parameters to output two 512-dimensional representation vectors.: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [other] The task workflow explicitly requires defining ResNet18 architecture configured for ion images, instantiating a shared-parameter encoder, and configuring selective layer training per the contrastive objective.: "Define a ResNet18 architecture configured to accept ion image inputs and output 512-dimensional feature vectors. Instantiate a parameter-sharing encoder module consisting of a single ResNet18"
- [other] Validation of output tensor shape and numerical stability is a mandatory step before integration with downstream projection modules.: "Verify output tensor shapes (batch_size × 512) and numerical stability of the representation vectors."
- [readme] DeepION uses contrastive loss to enforce similarity between augmentations while the projection and prediction modules prevent collapse.: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training"
- [readme] The encoder receives the output of the data augmentation module, which generates augmented images with mode-specific transformations.: "The original ion image is first imported into the data augmentation module "T" to generate two augmented images"
