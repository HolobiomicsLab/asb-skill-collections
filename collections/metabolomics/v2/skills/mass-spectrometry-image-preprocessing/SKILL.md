---
name: mass-spectrometry-image-preprocessing
description: Use when you have raw or preprocessed single-channel (2D array) or multi-channel (spectral) ion images from mass spectrometry imaging (MSI) data and need to train a contrastive deep learning model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - ResNet18
  - PyTorch
  - kornia
  - scikit-image or scipy.ndimage
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
  - build: coll_deepion
    doi: 10.1021/acs.analchem.3c05002
    title: deepion
  - build: coll_deepion_cq
    doi: 10.1021/acs.analchem.3c05002
    title: deepion
  dedup_kept_from: coll_deepion_cq
schema_version: 0.2.0
---

# mass-spectrometry-image-preprocessing

## Summary

Augment ion images from mass spectrometry imaging data by applying four stochastic transformations (color jitter, filtering, Poisson noise, random missing value) to generate two contrastive variants for self-supervised deep learning. This skill is essential for preparing MSI data to train representation models that learn robust, low-dimensional embeddings of ion spatial distributions.

## When to use

You have raw or preprocessed single-channel (2D array) or multi-channel (spectral) ion images from mass spectrometry imaging (MSI) data and need to train a contrastive deep learning model. Apply this skill when you aim to learn meaningful low-dimensional representations of ion images for downstream tasks such as co-localized ion discovery or isotope identification, and you operate in COL mode (co-localized ions from different molecules) rather than ISO mode (isotope ions from the same molecule).

## When NOT to use

- Input is already a learned representation vector or feature embedding (apply only to raw or preprocessed spatial images).
- You are working in ISO mode (isotope ions from the same molecule) — use T_ISO augmentation which includes intensity-dependent missing value in addition to the four COL transformations.
- Your MSI data has not been preprocessed into a matrix [X×Y, P] format; preprocessing of raw spectral data must occur first.

## Inputs

- Single-channel 2D ion image array [height × width]
- Multi-channel spectral ion image array [height × width × P] where P is number of ions
- Ion image as numpy array or PyTorch tensor

## Outputs

- Two augmented ion image tensors (pair) for contrastive learning
- Tuple of (augmented_image_1, augmented_image_2)

## How to apply

Load a preprocessed ion image (2D single-channel or multi-channel spectral array). Independently apply four sequential transformations twice to generate two augmented variants: (1) color jitter to modulate intensity values, (2) Gaussian or median filtering to smooth local intensity variations, (3) Poisson noise sampled from a Poisson distribution matched to image intensity (to simulate shot noise in mass spectrometry detection), and (4) random masking of a fraction of pixel values to simulate incomplete or missing detection. Return both augmented images as a tuple. The rationale is that these stochastically-independent variants preserve the underlying ion spatial structure while introducing realistic measurement artifacts and noise characteristics of MSI instruments, enabling the downstream encoder to learn invariant representations that are robust to instrumental variation.

## Related tools

- **ResNet18** (Encoder backbone that processes the pair of augmented images to output 512-dimensional representation vectors for contrastive learning)
- **PyTorch** (Framework for implementing the augmentation pipeline, tensor operations, and training loop)
- **kornia** (Differentiable image processing library used for filtering and spatial transformations in augmentation)
- **scikit-image or scipy.ndimage** (Image filtering (Gaussian or median) operations applied in the augmentation workflow)

## Examples

```
python run.py --input_Matrix ./DATASET/Pos_brain_data_matrix.txt --input_PeakList ./DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Both augmented images retain the same spatial dimensions and are non-identical due to stochastic transformations
- Pixel intensity values in augmented images remain within valid range (non-negative, within sensor dynamic range) after Poisson noise and jitter
- Contrastive loss between the pair of augmented images (passed through shared-parameter encoders) converges during training, indicating meaningful invariant features are learned
- Downstream tasks (co-localized ion discovery or isotope search) achieve higher accuracy or precision when using representations learned from augmented vs. non-augmented data
- Visual inspection confirms that augmented images preserve ion spatial structure and localization patterns while introducing realistic noise and missing-value artifacts

## Limitations

- The hyperparameters for color jitter intensity, filter kernel size, Poisson noise matching factor, and missing-value fraction must be tuned per instrument and ion type; excessive jitter can destroy localization signal.
- Augmentation assumes the underlying ion image spatial structure is stable across the two augmented variants; highly non-stationary or heterogeneous ion distributions may require careful masking thresholds.
- COL mode augmentation (T_COL) does not account for intensity-dependent effects in isotope ions; use T_ISO augmentation instead for ISO mode workflows.
- Performance depends on the quality of input preprocessing (removal of background, normalization); severely degraded or low-SNR input images may not benefit from these augmentations.

## Evidence

- [other] The T_COL augmentation module in COL mode applies four transformations to an input ion image: color jitter, filtering, Poisson noise, and random missing value, generating two augmented images for contrastive learning.: "The T_COL augmentation module in COL mode applies four transformations to an input ion image: color jitter, filtering, Poisson noise, and random missing value, generating two augmented images for"
- [other] 1. Load an input ion image (single-channel 2D array or multi-channel spectral image). 2. Apply color jitter to modulate intensity values across the image. 3. Apply filtering (e.g., Gaussian or median filter) to smooth local intensity variations. 4. Add Poisson noise sampled from a Poisson distribution matched to the image intensity.: "Load an input ion image (single-channel 2D array or multi-channel spectral image). Apply color jitter to modulate intensity values across the image. Apply filtering (e.g., Gaussian or median filter)"
- [intro] The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO mode.: "The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO"
- [intro] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training.: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training."
