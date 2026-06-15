---
name: poisson-noise-injection-for-imaging
description: Use when augmenting mass spectrometry ion images for contrastive learning, particularly when the model must generalize across different detector conditions or signal-to-noise ratios.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - ResNet18
  - Poisson noise augmentation
  - kornia
  - boly_pytorch
derived_from:
- doi: 10.1021/acs.analchem.3c05002
  title: deepion
evidence_spans:
- Two augmented images are propagated through a pair of ResNet18-based encoders
- T_COL including color jitter, filtering, Poisson noise, and random missing value
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepion
    doi: 10.1021/acs.analchem.3c05002
    title: deepion
  dedup_kept_from: coll_deepion
schema_version: 0.2.0
---

# poisson-noise-injection-for-imaging

## Summary

Poisson noise injection is a data augmentation technique that adds photon counting artifacts to ion images in mass spectrometry imaging (MSI) to simulate realistic detector noise. It is applied as part of the DeepION data augmentation pipeline to improve the robustness of deep learning models for ion image representation learning.

## When to use

Apply this skill when augmenting mass spectrometry ion images for contrastive learning, particularly when the model must generalize across different detector conditions or signal-to-noise ratios. Use it as part of the COL or ISO mode augmentation pipeline in DeepION when training encoders to learn noise-invariant ion image representations.

## When NOT to use

- When the input ion images have already been heavily noise-filtered or denoised by preprocessing — re-adding Poisson noise may conflict with prior signal enhancement steps.
- When downstream analysis requires pixel-level intensity quantification or absolute peak intensity measurements, as Poisson noise injection will corrupt those values.
- When working with ion images that are already heavily corrupted or have very low signal-to-noise ratio before augmentation.

## Inputs

- Ion image (2D or 3D array of pixel intensities from mass spectrometry imaging)
- Pixel intensity values (floating point or integer counts)

## Outputs

- Augmented ion image with Poisson noise artifacts
- Noisy pixel intensities simulating photon-counting detection

## How to apply

Poisson noise is injected into ion images after color jitter and filtering operations within the data augmentation module T. The noise is sampled from a Poisson distribution with rate parameter λ derived from the original pixel intensities, simulating photon-counting statistics characteristic of mass spectrometry detectors. The augmented image with injected Poisson noise is then passed to a ResNet18 encoder alongside an unaugmented or differently augmented version of the same image. The contrastive loss maximizes similarity between augmented pairs from the same image while the stop-gradient operation prevents representation collapse. This operation is applied consistently during training to both COL mode (co-localized ions) and ISO mode (isotope ions) augmentation branches.

## Related tools

- **ResNet18** (Encoder that processes augmented ion images with injected Poisson noise to output 512-dimensional representation vectors) — https://github.com/gankLei-X/DeepION
- **kornia** (PyTorch library providing differentiable image augmentation operations for Poisson noise and other transformations)
- **boly_pytorch** (PyTorch utility package supporting augmentation pipeline implementation)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Verify that augmented images contain visibly noisy artifacts compared to the original, with intensity variations proportional to the square root of original pixel values (characteristic of Poisson noise).
- Confirm that contrastive loss between augmented image pairs from the same source decreases during training, indicating the encoder learns to map noisy augmentations to similar 512-dimensional vectors.
- Check that the model trained with Poisson noise injection shows improved generalization on test ion images with different noise characteristics compared to models trained without this augmentation.
- Validate that the stop-gradient operation prevents representation collapse by ensuring that representation vectors maintain non-zero variance and do not converge to a single point in the 512-dimensional space.
- Inspect output 20-dimensional vectors from the dimensionality reduction module to confirm they preserve discriminative information despite noise injection during training.

## Limitations

- Poisson noise injection assumes detector noise follows Poisson statistics; real mass spectrometry detectors may have different noise distributions (Gaussian, read noise, multiplicative noise) that are not captured by this model.
- The skill is applied uniformly across all pixels without accounting for spatial correlations in noise or detector characteristics that may vary across the image sensor.
- Intensity-dependent missing value process in ISO mode is applied after Poisson noise, creating a two-stage corruption that may not fully reflect realistic MSI acquisition artifacts.
- The augmentation is optimized for the specific MSI data formats and preprocessing pipeline described in DeepION (matrix shape [X*Y, P]); applicability to other MSI platforms or preprocessing workflows is not established.

## Evidence

- [other] The COL mode augmentation applies four operations to ion images: color jitter, filtering, Poisson noise, and random missing value.: "T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode"
- [readme] Poisson noise is one of the standard augmentations in the data augmentation module that operates on ion images before encoder processing.: "The original ion image is first imported into the data augmentation module "T" to generate two augmented images, where the T_COL including color jitter, filtering, Poisson noise, and random missing"
- [readme] Augmented images are processed through ResNet18 encoders that output representation vectors used in contrastive learning with a stop-gradient operation.: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [other] A contrastive loss is employed to maximize similarity between augmentations from the same image.: "The model employs contrastive loss to maximize similarity between augmentations of the same image"
- [readme] The skill is applied within a framework designed for mass spectrometry imaging representation learning.: "DeepION is a deep learning-based low-dimensional representation model of ion images for mass spectrometry imaging"
