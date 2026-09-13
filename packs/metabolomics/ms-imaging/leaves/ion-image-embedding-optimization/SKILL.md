---
name: ion-image-embedding-optimization
description: Use when you have 512-dimensional representation vectors output from
  ResNet18 encoders processing paired augmented ion images, and you need to prevent
  trivial solutions (representation collapse) during contrastive learning—specifically
  when optimizing for maximized similarity between augmentations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3679
  tools:
  - ResNet18
  - kornia
  - PyTorch
  techniques:
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
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

# ion-image-embedding-optimization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill optimizes 512-dimensional ion image representations using contrastive learning with Projection and Prediction modules to prevent representation collapse and learn meaningful embeddings for mass spectrometry imaging. It is applied when training encoder outputs to maximize similarity between augmentations of the same ion image while minimizing cross-image similarity.

## When to use

Apply this skill when you have 512-dimensional representation vectors output from ResNet18 encoders processing paired augmented ion images, and you need to prevent trivial solutions (representation collapse) during contrastive learning—specifically when optimizing for maximized similarity between augmentations of the same ion image while maintaining discriminability across different ion images in mass spectrometry imaging workflows.

## When NOT to use

- Input representations are already collapsed (degenerate case where encoder outputs lack variance across ion images)
- Contrastive learning objective is not appropriate for the downstream task (e.g., if supervised classification or regression on ion images is the true goal)
- Ion image augmentations cannot be reliably generated or differ fundamentally in content rather than noise/intensity variation

## Inputs

- Paired augmented ion image tensors (input to ResNet18 encoders)
- 512-dimensional representation vectors (ResNet18 encoder outputs)
- Augmentation transformation configuration (T_COL or T_ISO mode specification)

## Outputs

- Optimized Projection module weights (learnable parameters)
- Optimized Prediction module weights (learnable parameters)
- Minimized contrastive loss scalar value
- Final learned ion image embeddings (lower-dimensional representations)

## How to apply

Load paired 512-dimensional representation vectors from ResNet18 encoders applied to augmented ion image pairs. Apply the Projection module to transform these vectors into a lower-dimensional projection space suitable for contrastive optimization. Apply the Prediction module to the projection outputs, which introduces asymmetry to prevent trivial collapsed solutions. Compute contrastive loss between the projections/predictions of augmented image pairs, maximizing similarity for the same ion image (using stop-gradient operations) while minimizing similarity across different images. Backpropagate the contrastive loss through the Projection and Prediction modules to update their learnable parameters, either keeping encoder weights frozen or jointly optimizing them. The stop-gradient operation is critical to prevent the optimization from converging to collapsed solutions where all representations become identical.

## Related tools

- **ResNet18** (Encoder architecture that processes augmented ion images and outputs 512-dimensional representation vectors prior to Projection and Prediction module optimization) — https://github.com/gankLei-X/DeepION
- **kornia** (Provides differentiable image augmentation operations (color jitter, filtering, Poisson noise, missing value injection) for T_COL and T_ISO transformation modules)
- **PyTorch** (Deep learning framework for implementing Projection/Prediction modules, contrastive loss computation, and backpropagation optimization (version 1.8.2))

## Examples

```
python run.py --input_Matrix Pos_brain_data_matrix.txt --input_PeakList Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Contrastive loss monotonically decreases across training iterations, indicating successful optimization of Projection and Prediction modules
- Similarity scores between augmentations of the same ion image are substantially higher than similarity scores across different ion images (quantifiable via cosine similarity or other metrics on projection outputs)
- Learned representations exhibit non-zero variance across ion images (detector for collapse—if all embeddings become identical, the skill failed)
- Stop-gradient operation prevents the predictor from collapsing by verifying that prediction branch gradients do not flow to projection outputs
- Downstream task performance (e.g., co-localized ion search in COL mode or isotope discovery in ISO mode) improves compared to non-contrastive baselines

## Limitations

- Encoder weights are either frozen or jointly optimized—joint optimization may destabilize contrastive learning if not carefully balanced
- Augmentation design (T_COL vs. T_ISO) must match the ion image analysis goal; incorrect mode selection will produce embeddings misaligned with downstream tasks
- Requires paired augmented ion images; if augmentation is unreliable or produces semantically different content, contrastive optimization will fail
- The choice of Projection module dimensionality and Prediction module architecture is not explicitly specified in the documentation and may require task-specific tuning

## Evidence

- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image: "Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training"
- [other] Apply the Projection module to transform encoder outputs into a lower-dimensional projection space suitable for contrastive learning. Apply the Prediction module to generate prediction outputs from the projection space, introducing an asymmetry to avoid trivial solutions.: "Apply the Projection module to transform encoder outputs into a lower-dimensional projection space suitable for contrastive learning. Apply the Prediction module to generate prediction outputs from"
- [other] Backpropagate loss through the Projection and Prediction modules to update their learnable parameters while keeping encoder weights frozen or jointly optimized as specified: "Backpropagate loss through the Projection and Prediction modules to update their learnable parameters while keeping encoder weights frozen or jointly optimized as specified"
