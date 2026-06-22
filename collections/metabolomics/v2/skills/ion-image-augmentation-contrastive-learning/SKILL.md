---
name: ion-image-augmentation-contrastive-learning
description: Use when when you have preprocessed mass spectrometry ion images (single-channel 2D arrays or multi-channel spectral images) and need to train a self-supervised encoder to learn low-dimensional representations for downstream tasks such as co-localized ion discovery (COL mode) or isotope ion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - ResNet18
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

# ion-image-augmentation-contrastive-learning

## Summary

Apply stochastic augmentation transformations to single ion images to generate paired augmented variants for contrastive representation learning in mass spectrometry imaging. This skill ensures that the encoder learns invariant ion image representations robust to instrumental and detection variability.

## When to use

When you have preprocessed mass spectrometry ion images (single-channel 2D arrays or multi-channel spectral images) and need to train a self-supervised encoder to learn low-dimensional representations for downstream tasks such as co-localized ion discovery (COL mode) or isotope ion clustering (ISO mode). Use this skill when contrastive loss optimization requires pairs of independent augmentations from the same ion image to maximize representation similarity.

## When NOT to use

- The input is already a low-dimensional representation vector or feature embedding — augmentation should be applied only to raw or preprocessed ion images, not derived features.
- The ion image is from a single isotope or single m/z channel in ISO mode where intensity-dependent missing value augmentation is required instead of random masking.
- The analysis goal does not require contrastive learning or self-supervised representation learning — if supervised labels are available, alternative augmentation strategies may be more appropriate.

## Inputs

- Single ion image (2D numpy array or tensor, single-channel or multi-channel spectral image)
- Image intensity range (for matched Poisson noise sampling)
- Augmentation hyperparameters (jitter magnitude, filter kernel size, masking fraction)

## Outputs

- Pair of augmented ion images (two 2D arrays/tensors of identical shape to input)
- Tuple or tensor pair (augmented_image_1, augmented_image_2) ready for encoder input

## How to apply

Load a single preprocessed ion image and independently apply a sequence of four stochastic transformations to generate two augmented variants. For COL mode, apply: (1) color jitter to modulate pixel intensity values; (2) spatial or intensity filtering (Gaussian or median) to smooth local variations; (3) Poisson noise sampled from a distribution matched to the image intensity to simulate shot noise; (4) random masking of a fraction of pixels as missing values to simulate incomplete ion detection. Repeat steps 1–4 independently to create a second augmented image. Return both augmented images as a paired tuple for propagation through shared-parameter ResNet18 encoders. The independence of the two augmentations ensures the encoder learns invariances rather than memorizing the original image.

## Related tools

- **ResNet18** (Shared-parameter encoder that receives paired augmented images and outputs 512-dimensional representation vectors for contrastive loss computation) — https://github.com/gankLei-X/DeepION
- **kornia** (Differentiable image transformation library used to implement spatial filtering and intensity augmentations)
- **boly_pytorch** (PyTorch utility package for contrastive loss and stop-gradient operations)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Both augmented images have identical spatial shape and dtype as the input ion image; pixel values remain within valid intensity range after all transformations.
- The two augmented variants are statistically independent: applying the same augmentation sequence twice to the same input produces different outputs, confirming stochasticity of color jitter, Poisson noise, and random masking.
- After encoding through shared ResNet18 encoders, the cosine similarity between the two 512-dimensional representation vectors is higher than random image pairs, indicating contrastive loss is reducing representation distance between augmentations from the same ion image.
- Pixels marked as missing values in the augmented images are consistently masked (e.g., set to 0 or NaN) in both output tensors with approximately equal frequency (masking fraction matches the specified parameter).
- Poisson noise samples exhibit variance proportional to pixel intensity, consistent with Poisson noise properties; low-intensity pixels show less variance than high-intensity pixels in repeated augmentation cycles.

## Limitations

- Augmentation hyperparameters (jitter magnitude, filter kernel, masking fraction, Poisson intensity scaling) must be tuned per dataset; no universal defaults are specified in the article. Suboptimal choices can degrade representation quality.
- Random masking may obscure fine spatial structure in low-resolution ion images; excessive masking fraction can make augmented images too sparse for encoder learning.
- Poisson noise calibration depends on accurate estimation of ion image intensity range; miscalibration results in noise that does not reflect true instrumental shot noise, reducing biological relevance of learned representations.
- In ISO mode, the standard T_COL augmentation must be supplemented with intensity-dependent missing value augmentation; applying T_COL alone to isotope pairs misses the isotope-specific augmentation strategy.

## Evidence

- [other] The T_COL augmentation module in COL mode applies four transformations to an input ion image: color jitter, filtering, Poisson noise, and random missing value, generating two augmented images for contrastive learning.: "The T_COL augmentation module in COL mode applies four transformations to an input ion image: color jitter, filtering, Poisson noise, and random missing value, generating two augmented images for"
- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO mode.: "The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training.: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training."
- [other] Repeat steps 2–5 independently to generate a second augmented variant.: "Repeat steps 2–5 independently to generate a second augmented variant."
