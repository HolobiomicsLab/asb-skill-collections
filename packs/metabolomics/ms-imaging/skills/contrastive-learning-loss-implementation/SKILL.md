---
name: contrastive-learning-loss-implementation
description: Use when when you have paired augmented ion images processed through ResNet18 encoders producing 512-dimensional representation vectors, and you need to learn meaningful low-dimensional representations without labeled data by enforcing that augmentations of the same image remain similar while.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ResNet18
  - kornia
  - PyTorch
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Contrastive Learning Loss Implementation

## Summary

Apply contrastive loss to maximize similarity between augmentations of the same ion image while minimizing similarity across different images, using Projection and Prediction modules on 512-dimensional encoder outputs to prevent representation collapse. This skill is essential for training self-supervised representation models on mass spectrometry imaging (MSI) data.

## When to use

When you have paired augmented ion images processed through ResNet18 encoders producing 512-dimensional representation vectors, and you need to learn meaningful low-dimensional representations without labeled data by enforcing that augmentations of the same image remain similar while different images diverge.

## When NOT to use

- Input representation vectors are already collapsed or degenerate (all dimensions identical or near-zero variance)
- You have access to labeled data and supervised learning is feasible; supervised approaches may be more data-efficient
- Ion images have not undergone appropriate augmentation preprocessing (missing color jitter, filtering, Poisson noise, or intensity-dependent missing value)

## Inputs

- 512-dimensional representation vectors from ResNet18 encoder pair
- Augmented ion image pairs with shared parameter encoders
- Batch of augmentation transformations (T_COL or T_ISO)

## Outputs

- Contrastive loss scalar value
- Updated Projection module weights
- Updated Prediction module weights
- Learned low-dimensional representation vectors for downstream tasks

## How to apply

Load the 512-dimensional representation vectors output from paired ResNet18-based encoders for augmented ion image pairs. Apply a Projection module to transform these vectors into a lower-dimensional projection space suitable for contrastive learning. Apply a Prediction module to generate prediction outputs from the projection space, which introduces asymmetry to avoid trivial collapse solutions. Compute contrastive loss between the projections and/or predictions of augmented image pairs, with the loss function maximizing cosine similarity for augmentations of the same ion image while minimizing similarity across different images. Implement a stop-gradient operation on one branch to prevent collapse. Backpropagate the loss through the Projection and Prediction modules to update their learnable parameters, keeping encoder weights frozen or jointly optimized as specified.

## Related tools

- **ResNet18** (Encoder backbone that processes augmented ion images to produce 512-dimensional representation vectors)
- **kornia** (Image augmentation and geometric transformation utilities for generating ion image augmentations)
- **PyTorch** (Deep learning framework for implementing Projection/Prediction modules, computing contrastive loss, and backpropagation)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Contrastive loss decreases monotonically during training iterations, indicating successful optimization
- Cosine similarity between augmentations of the same ion image is higher (closer to 1.0) than between different images
- Stop-gradient operation prevents both branches from converging to trivial constant solutions (verify at least one projection dimension has non-zero variance across the batch)
- Downstream task performance (co-localized ion ranking, isotope discovery) improves when using learned representations vs. raw encoder outputs
- Projection and Prediction module weight norms remain stable and do not diverge during training

## Limitations

- Requires careful selection of augmentation transforms (T_COL for co-localized ions, T_ISO for isotopes); incorrect augmentation strategy can lead to meaningless learned representations
- Success depends on adequate batch size to ensure sufficient negative pairs; very small batches may not provide enough contrastive signal
- Stop-gradient operation is essential; without it or with incorrect placement, the model may collapse to constant outputs that satisfy the loss trivially
- Computational cost scales with the number of ion images and the dimensionality of encoder outputs (512-D); may require GPU acceleration for large MSI datasets

## Evidence

- [intro] 512-dimensional representation vectors output from ResNet18 encoders: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [intro] Projection and Prediction module roles: "Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image"
- [intro] Contrastive loss with stop-gradient: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training"
- [readme] Data augmentation modes for COL and ISO: "T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO mode"
