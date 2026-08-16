---
name: deep-learning-architecture-implementation
description: Use when you have two augmented versions of the same ion image (from mass spectrometry imaging data) and need to extract learnable 512-dimensional feature representations using a shared-weight encoder for contrastive loss optimization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ResNet18
  - PyTorch
  - torchvision
  techniques:
  - MS-imaging
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05002
  all_source_dois:
  - 10.1021/acs.analchem.3c05002
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-architecture-implementation

## Summary

Implement a ResNet18-based encoder module with shared parameters that processes pairs of augmented ion images and outputs 512-dimensional representation vectors for contrastive learning in mass spectrometry imaging. This skill is essential for building the feature extraction backbone of self-supervised representation learning models designed to discover co-localized or isotope ions.

## When to use

Apply this skill when you have two augmented versions of the same ion image (from mass spectrometry imaging data) and need to extract learnable 512-dimensional feature representations using a shared-weight encoder for contrastive loss optimization. Use it in the feature extraction stage of a self-supervised learning pipeline where you seek to maximize similarity between augmentations of the same image while avoiding representation collapse.

## When NOT to use

- Ion image data has already been reduced to a final 20-dimensional representation—use the Dimensionality Reduction module instead.
- Input images are not derived from a shared augmentation pair—the contrastive learning objective requires both augmentations of the same source image.
- Your goal is final ion matching or downstream classification—this skill outputs intermediate representations; pair it with Projection, Prediction, and Dimensionality Reduction modules for end-to-end predictions.

## Inputs

- Two augmented ion images (derived from the same original ion image via the Data Augmentation module)
- Original MSI ion image data (2D spatial intensity matrix of shape X×Y, where X and Y are pixel dimensions)
- ResNet18 model architecture (pre-initialized or random weights)

## Outputs

- Two 512-dimensional representation vectors (shape: batch_size × 512) corresponding to the two augmented inputs
- Learned or frozen ResNet18 encoder weights (if training)

## How to apply

Define a ResNet18 architecture configured to accept ion image inputs (grayscale 2D spatial data from MSI) and configure it to output 512-dimensional feature vectors by modifying the final fully connected layer. Instantiate a single ResNet18 instance (parameter sharing) that will process both augmented images sequentially or in parallel. Configure training of convolutional and pooling layers according to your contrastive objective—typically by freezing early layers if pre-trained, or training end-to-end if training from scratch. Implement the forward pass to accept a batch of two augmented ion images and propagate each independently through the shared ResNet18 encoder, producing two distinct 512-dimensional representation vectors (shape: batch_size × 512). Verify output tensor shapes match (batch_size × 512) and check numerical stability of the representation vectors (no NaN, no exploding/vanishing gradients) before passing to the Projection and Prediction modules.

## Related tools

- **ResNet18** (Shared-parameter encoder backbone that accepts ion images and outputs 512-dimensional feature vectors for contrastive learning)
- **PyTorch** (Deep learning framework for implementing and training the ResNet18 encoder module)
- **torchvision** (Provides pre-built ResNet18 architecture and utilities for model instantiation)

## Evaluation signals

- Output tensor shape is exactly (batch_size, 512) for both representation vectors; no shape mismatches downstream.
- Representation vectors contain no NaN or infinite values and have reasonable numerical magnitude (e.g., L2 norm in expected range, not saturated at 0 or unbounded).
- Contrastive loss decreases over training iterations and converges, indicating that the encoder is learning to maximize similarity between augmentations of the same image.
- Gradient flow through the encoder is stable (no exploding/vanishing gradients) when backpropagating the contrastive loss.
- Visual inspection: learned representations cluster augmentations of the same ion image close together in embedding space while pushing augmentations of different ions apart (e.g., via t-SNE or UMAP visualization after Dimensionality Reduction).

## Limitations

- ResNet18 is relatively shallow; deeper architectures (ResNet50, ResNet101) may capture more complex ion image features but require more training data and compute.
- Shared-weight architecture means both augmented images are processed identically; if augmentations are too aggressive or too subtle, contrastive learning may fail to learn meaningful distinctions.
- Output is a 512-dimensional vector, which is still high-dimensional; subsequent Projection and Dimensionality Reduction modules are required to avoid representation collapse and to produce interpretable final representations.
- The encoder assumes grayscale 2D ion images; multi-channel or 3D imaging data would require architectural modification.
- Python 3.5–3.7 and PyTorch 1.8.2 are specified requirements; compatibility with modern PyTorch versions (2.x) is not documented.

## Evidence

- [intro] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [other] Define a ResNet18 architecture configured to accept ion image inputs and output 512-dimensional feature vectors: "Define a ResNet18 architecture configured to accept ion image inputs and output 512-dimensional feature vectors"
- [other] Implement the forward pass to accept two augmented ion images as input and propagate each through the shared ResNet18 encoder to produce two distinct 512-dimensional representation vectors: "Implement the forward pass to accept two augmented ion images as input and propagate each through the shared ResNet18 encoder to produce two distinct 512-dimensional representation vectors"
- [other] Verify output tensor shapes (batch_size × 512) and numerical stability of the representation vectors: "Verify output tensor shapes (batch_size × 512) and numerical stability of the representation vectors"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training"
