---
name: neural-network-projection-module-design
description: Use when when you have 512-dimensional (or other fixed-size) representation
  vectors output from paired encoders processing augmented versions of the same input
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ResNet18
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

# neural-network-projection-module-design

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Design and implement Projection and Prediction modules that transform high-dimensional encoder outputs into lower-dimensional spaces suitable for contrastive learning while preventing representation collapse. This skill is essential when training self-supervised models on ion images or similar high-dimensional data where trivial solutions (uniform representations) must be actively avoided.

## When to use

When you have 512-dimensional (or other fixed-size) representation vectors output from paired encoders processing augmented versions of the same input (e.g., ion images in mass spectrometry imaging), and you need to apply contrastive loss without having the model collapse to trivial constant solutions. Use this skill as part of the training pipeline after the Encoder module but before computing contrastive loss.

## When NOT to use

- When encoder weights are frozen and you do not need to prevent representation collapse (the modules would have no learnable parameters to update)
- When working with already-collapsed or low-entropy representations where contrastive loss is not applicable
- When the downstream task does not require similarity-based learning or pair-based supervision (e.g., fully supervised classification with single-image labels)

## Inputs

- Two 512-dimensional representation vectors from paired ResNet18 encoders (one vector per augmented ion image pair)
- Augmented ion image pair labels (indicating which two representations came from the same original image)

## Outputs

- Projection space embeddings (lower-dimensional projections of the 512-d vectors)
- Prediction module outputs (asymmetric predictions used for contrastive loss computation)
- Contrastive loss scalar (maximizing similarity within pairs, minimizing across different images)
- Updated Projection and Prediction module weights

## How to apply

After the paired ResNet18 encoders output two 512-dimensional representation vectors from augmented ion image pairs, apply the Projection module to transform these vectors into a lower-dimensional projection space. Then apply the Prediction module to generate prediction outputs from the projected space, introducing asymmetry by stopping gradients on one branch of the contrastive path. Compute contrastive loss between the projections (or predictions) of augmented pairs, maximizing similarity for augmentations of the same ion image while minimizing similarity across different images. Backpropagate this loss through both modules to update their learnable parameters. The asymmetry introduced by the Prediction module and the stop-gradient operation prevent the model from converging to a trivial solution where all representations become identical.

## Related tools

- **ResNet18** (Shared-parameter encoder that outputs 512-dimensional representation vectors from augmented ion images; Projection and Prediction modules operate on these encoder outputs) — https://github.com/gankLei-X/DeepION
- **PyTorch** (Deep learning framework for implementing Projection and Prediction module architectures and contrastive loss backpropagation) — https://github.com/gankLei-X/DeepION

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Verify that contrastive loss decreases during training, indicating the model is learning to maximize similarity between augmentations of the same ion image
- Check that the final 512-dimensional representations do not collapse to a single constant vector or near-zero variance across dimensions
- Confirm that downstream tasks (e.g., co-localized ion searching in COL mode, isotope discovery in ISO mode) benefit from the learned representations with measurable performance improvement
- Validate that the asymmetry introduced by the Prediction module prevents trivial solutions by comparing performance with and without the stop-gradient operation
- Ensure that the learned representations are not identical or nearly identical across different input ion images (inter-image dissimilarity)

## Limitations

- The module design assumes 512-dimensional encoder outputs; adaptation may be required for encoders with different output dimensions
- Performance depends critically on the choice of augmentation strategy (T_COL or T_ISO); inappropriate augmentations may not provide sufficient diversity to prevent collapse
- The contrastive loss optimization requires careful tuning of loss scale and batch composition to balance intra-pair similarity maximization against inter-image dissimilarity
- Stop-gradient operations and the Prediction module introduce asymmetry that is essential but may complicate gradient flow and require longer training schedules
- The approach is designed for paired augmentation scenarios; it may not directly apply to unpaired or multi-view settings without modification

## Evidence

- [readme] Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image: "Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image"
- [other] The Projection and Prediction modules process the 512-dimensional representation vectors output by the ResNet18-based encoders to avoid collapsing solutions while optimizing for maximized similarity between augmentations of the same ion image using contrastive loss.: "The Projection and Prediction modules process the 512-dimensional representation vectors output by the ResNet18-based encoders to avoid collapsing solutions while optimizing for maximized similarity"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training.: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training."
- [other] Apply the Prediction module to generate prediction outputs from the projection space, introducing an asymmetry to avoid trivial solutions.: "Apply the Prediction module to generate prediction outputs from the projection space, introducing an asymmetry to avoid trivial solutions."
- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
