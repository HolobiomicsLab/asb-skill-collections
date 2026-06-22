---
name: representation-collapse-prevention
description: Use when training a contrastive learning model on ion image data (mass spectrometry imaging) where augmented pairs of the same ion image must maximize similarity while different images minimize similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0091
  tools:
  - ResNet18
  - PyTorch
  - kornia
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

# representation-collapse-prevention

## Summary

This skill prevents trivial (collapsed) solutions during contrastive learning of ion image representations by introducing an asymmetric Projection–Prediction module architecture that discourages the encoder from learning constant representations. It is essential when optimizing 512-dimensional encoder outputs under contrastive loss to preserve meaningful variation in learned ion image embeddings.

## When to use

Apply this skill when training a contrastive learning model on ion image data (mass spectrometry imaging) where augmented pairs of the same ion image must maximize similarity while different images minimize similarity. Use it specifically when the encoder outputs 512-dimensional vectors and you are optimizing with contrastive loss; without this mechanism, the encoder may converge to a constant representation (collapse) that trivially satisfies the loss function.

## When NOT to use

- When the input is already a collapsed representation (constant vector across all samples) — prevention is only meaningful during training.
- When using supervised contrastive objectives with hard labels instead of augmentation pairs — the asymmetry design assumes unsupervised learning from augmentations.
- When the encoder output dimensionality is significantly lower than 512 or when downstream tasks require maximally compact embeddings — additional projection may be unnecessary.

## Inputs

- 512-dimensional representation vectors from paired ResNet18-based encoders
- Augmented ion image pairs with known correspondence labels
- Contrastive loss function and hyperparameters (temperature, batch size)

## Outputs

- Learned Projection module parameters
- Learned Prediction module parameters
- Optimized 512-dimensional representation vectors that preserve meaningful variation across different ion images

## How to apply

Implement a two-module pipeline following the DeepION architecture: (1) After the ResNet18-based encoder outputs 512-dimensional representation vectors, apply a Projection module to transform these vectors into a lower-dimensional projection space suitable for contrastive learning. (2) Apply a Prediction module on top of the projections to introduce asymmetry between the two encoder branches, preventing trivial constant solutions. (3) Compute contrastive loss between projections/predictions of augmented image pairs, maximizing similarity for the same ion image while minimizing similarity across different images. (4) Use a stop-gradient operation on one branch to further prevent collapse. (5) Backpropagate the loss through both modules while keeping encoder weights frozen or jointly optimized as specified. The asymmetry between branches and the stop-gradient operation are critical: they prevent the encoder from learning degenerate constant representations.

## Related tools

- **ResNet18** (Encoder network that outputs 512-dimensional representation vectors for augmented ion image pairs) — https://github.com/gankLei-X/DeepION
- **PyTorch** (Deep learning framework for implementing Projection and Prediction modules and contrastive loss optimization)
- **kornia** (Computer vision library for augmentation operations applied before encoder input)

## Examples

```
python run.py --input_Matrix .../Pos_brain_data_matrix.txt --input_PeakList .../Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Verify that the loss decreases during training and converges without plateauing at a constant value, indicating the encoder is not learning a collapsed solution.
- Check that 512-dimensional vectors output by the encoder exhibit non-zero variance across different ion images and augmentations; compute the standard deviation per dimension and confirm it is non-negligible.
- Confirm that augmented pairs of the same ion image produce similar projections (high cosine similarity), while projections from different ion images are dissimilar (low cosine similarity), validating the contrastive objective.
- Validate that removing the Prediction module or stop-gradient operation causes loss to plateau or representations to collapse, demonstrating the necessity of the asymmetric design.
- Inspect the learned projection space dimensionality and verify it is reduced from 512 to a lower dimension as specified in the architecture, confirming the module applied a transformation.

## Limitations

- The approach requires careful tuning of the contrastive loss temperature and batch size; inappropriate hyperparameters can still lead to collapse despite the asymmetric architecture.
- The method is specifically designed for ion image data with augmentation-based learning; applicability to other domains or supervised contrastive objectives requires validation.
- The 512-dimensional encoder output is fixed by the ResNet18 architecture; if input image resolution or encoder depth changes, the representation dimensionality may differ and module design must be adjusted.
- The stop-gradient operation introduces a hard asymmetry between branches that may reduce the information flow in one direction; joint optimization of both branches without stop-gradient may be more efficient in some settings.

## Evidence

- [other] The Projection and Prediction modules process the 512-dimensional representation vectors output by the ResNet18-based encoders to avoid collapsing solutions while optimizing for maximized similarity between augmentations of the same ion image using contrastive loss.: "Projection and Prediction modules process the 512-dimensional representation vectors output by the ResNet18-based encoders to avoid collapsing solutions"
- [readme] Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image and ensure to learn the meaningful representation vectors. A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training.: "Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image and ensure to"
- [other] Apply the Projection module to transform encoder outputs into a lower-dimensional projection space suitable for contrastive learning. Apply the Prediction module to generate prediction outputs from the projection space, introducing an asymmetry to avoid trivial solutions.: "Apply the Projection module to transform encoder outputs into a lower-dimensional projection space suitable for contrastive learning. Apply the Prediction module to generate prediction outputs from"
- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors.: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
