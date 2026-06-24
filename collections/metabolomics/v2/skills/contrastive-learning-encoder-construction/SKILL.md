---
name: contrastive-learning-encoder-construction
description: Use when you have mass spectrometry imaging (MSI) data with ion images
  that need low-dimensional representation learning for downstream tasks like co-localized
  ion searching or isotope discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3928
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ResNet18
  - torchvision
  - kornia
  - PyTorch
  techniques:
  - MS-imaging
  license_tier: restricted
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

# contrastive-learning-encoder-construction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Build a shared-weight ResNet18 encoder module that processes pairs of augmented ion images to produce 512-dimensional representation vectors for contrastive learning in mass spectrometry imaging. This skill applies contrastive loss to maximize similarity between augmentations of the same image while avoiding representation collapse.

## When to use

You have mass spectrometry imaging (MSI) data with ion images that need low-dimensional representation learning for downstream tasks like co-localized ion searching or isotope discovery. You want to learn invariant representations by contrasting two augmented views of the same image without supervised labels.

## When NOT to use

- Your ion images are already embedded in a learned low-dimensional space and need only downstream classification or clustering
- You are working with supervised labels and can use a standard classification loss instead of contrastive learning
- Your input data lacks paired augmentations or you cannot generate meaningful augmentations for your ion imaging modality

## Inputs

- Two augmented ion images (tensor pairs from Data Augmentation module)
- Ion image batch with shape [batch_size, channels, height, width]

## Outputs

- Two 512-dimensional representation vectors per image pair (shape: batch_size × 512)
- Encoder module instance with learned or pretrained weights

## How to apply

Define a ResNet18 architecture accepting ion image inputs and outputting 512-dimensional feature vectors. Instantiate a single ResNet18 encoder with shared parameters that will process both augmented ion images sequentially in the forward pass. Configure the encoder to freeze or selectively train convolutional and pooling layers according to your contrastive learning objective (typically freezing early layers for transfer learning). For each input pair of augmented ion images, propagate each through the shared encoder to produce two distinct 512-dimensional representation vectors. Apply projection and prediction modules after the encoder outputs to prevent representation collapse during optimization. Verify output tensor shapes match (batch_size × 512) and check numerical stability of the representation vectors before feeding them to the contrastive loss function.

## Related tools

- **ResNet18** (Backbone convolutional encoder architecture that accepts ion image inputs and outputs fixed 512-dimensional feature vectors through shared parameters across both augmented images)
- **torchvision** (Provides ResNet18 implementation and pretrained weights for transfer learning initialization)
- **kornia** (Provides augmentation operations (color jitter, filtering, Poisson noise, random missing value) applied before encoder input)
- **PyTorch** (Deep learning framework for defining the encoder module, managing shared parameters, and implementing the forward pass with contrastive loss)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Output tensor shapes are exactly [batch_size, 512] for each of the two representation vectors from a single image pair
- Encoder parameters are truly shared: identical forward pass on identical input yields identical output vectors within numerical precision (< 1e-6 difference)
- Representation vectors have bounded norm and no NaN/Inf values after a full training epoch
- Contrastive loss decreases during training, indicating the encoder is learning to maximize similarity between augmentations of the same image
- Projection module prevents representation collapse by maintaining sufficient variance across the batch dimension (checked via singular value decomposition or rank)

## Limitations

- ResNet18 is a relatively shallow architecture; deeper architectures may improve representation quality but increase computational cost for large MSI datasets
- The 512-dimensional bottleneck is fixed by design; changing output dimensionality requires retraining the entire encoder
- Encoder performance depends critically on data augmentation quality (T_COL or T_ISO); poor augmentations yield meaningless contrastive signals
- Shared-weight architecture assumes both augmented images contribute equally to the learned representation; mode-specific augmentation differences (COL vs. ISO) may bias learning toward dominant augmentation types
- No explicit guidance provided on whether to freeze early ResNet18 layers vs. train end-to-end; this choice affects convergence speed and final representation quality

## Evidence

- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image: "Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training"
- [readme] The Data Augmentation module generates two augmented images, where the T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO mode: "The original ion image is first imported into the data augmentation module "T"  to generate two augmented images, where the T_COL including color jitter, filtering, Poisson noise, and random missing"
- [other] The encoder module accepts two augmented ion images and propagates them through a pair of ResNet18-based encoders with shared parameters to output two 512-dimensional representation vectors: "The Encoder module accepts two augmented ion images and propagates them through a pair of ResNet18-based encoders with shared parameters to output two 512-dimensional representation vectors"
