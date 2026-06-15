---
name: mass-spectrometry-image-preprocessing
description: Use when when preparing raw mass spectrometry imaging (MSI) ion images for deep learning–based representation learning, especially when you need to generate augmented image pairs that preserve domain-specific artifacts (photon counting noise, missing pixels) while varying appearance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - ResNet18
  - Color jitter augmentation
  - Filtering augmentation
  - Poisson noise augmentation
  - Random missing value augmentation
  - Intensity-dependent missing value augmentation
  - kornia
  - boly_pytorch
derived_from:
- doi: 10.1021/acs.analchem.3c05002
  title: deepion
evidence_spans:
- Two augmented images are propagated through a pair of ResNet18-based encoders
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

# mass-spectrometry-image-preprocessing

## Summary

Augment mass spectrometry ion images through mode-specific pipelines (COL for co-localized ions, ISO for isotope ions) that apply color jitter, filtering, Poisson noise, and intensity-dependent missing value processes to generate paired augmented images for contrastive representation learning.

## When to use

When preparing raw mass spectrometry imaging (MSI) ion images for deep learning–based representation learning, especially when you need to generate augmented image pairs that preserve domain-specific artifacts (photon counting noise, missing pixels) while varying appearance. Use COL mode for co-localized ions from different molecules; switch to ISO mode when handling isotope ions from the same molecule, which requires the additional intensity-dependent missing value process.

## When NOT to use

- Input is already a pre-computed 512-dimensional or lower-dimensional representation vector; preprocessing is redundant.
- Ion images have already been augmented by a different pipeline and you are about to apply augmentation a second time (risk of cascading noise corruption).
- Data are not from mass spectrometry imaging experiments (e.g., optical microscopy, histopathology images without ion-specific artifacts) — the Poisson noise and intensity-dependent missing value processes are specific to MSI detector physics.

## Inputs

- Original ion image (2D grayscale or single-channel intensity map from MSI)
- MSI matrix data [X*Y, P] where X, Y are pixel coordinates and P is the number of ions
- Mode selection: 'COL' or 'ISO' (string parameter)

## Outputs

- Two augmented ion images per input (4 total images when both COL and ISO are applied)
- 512-dimensional representation vectors (output from ResNet18 encoders)
- 20-dimensional reduced representation vectors (from dimensionality reduction module)

## How to apply

Load the original ion image and route it through the appropriate augmentation pipeline (T_COL or T_ISO). For COL mode: sequentially apply color jitter to adjust pixel intensities, apply filtering to smooth or enhance spatial features, add Poisson noise to simulate photon-counting artifacts typical of mass spectrometry detectors, and introduce random missing values at arbitrary pixel locations. For ISO mode: execute all COL operations, then apply an intensity-dependent missing value process that selectively removes pixels based on their intensity levels (lower-intensity pixels are more likely to be missing, reflecting the physical reality of isotope detection). Both pipelines output two augmented images per input, which are then passed to paired ResNet18-based encoders to generate contrastive loss optimization. The rationale is that augmentations must preserve the spatial structure and intensity relationships of the ion images while introducing realistic variations, ensuring the learned 512-dimensional representation vectors capture invariant ion localization patterns rather than pixel-level noise.

## Related tools

- **ResNet18** (Paired parameter-shared encoders that propagate augmented images to 512-dimensional representation vectors)
- **Color jitter augmentation** (Adjusts pixel intensities in both COL and ISO modes to simulate detector gain variation)
- **Filtering augmentation** (Applies spatial smoothing or feature enhancement to both COL and ISO augmented images)
- **Poisson noise augmentation** (Simulates photon-counting artifacts in both COL and ISO modes to reflect realistic MSI detector behavior)
- **Random missing value augmentation** (Introduces random pixel dropout at arbitrary locations in both COL and ISO modes)
- **Intensity-dependent missing value augmentation** (Selectively removes pixels based on intensity in ISO mode only; models isotope-specific detection characteristics)
- **kornia** (PyTorch library providing geometric and photometric image augmentation operations)
- **boly_pytorch** (Supporting package for contrastive loss computation and model training)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Output image count: exactly 2 augmented images per input image per mode (verify pair generation before encoder stage).
- Poisson noise statistics: augmented images exhibit mean-variance relationship consistent with Poisson process (variance ≈ intensity) in high-intensity regions.
- Missing value patterns: random missing value mode produces uniformly distributed dropout; intensity-dependent mode produces higher dropout in low-intensity pixels (ISO only).
- Representation vector dimensions: encoder outputs are exactly 512-dimensional; final outputs after dimensionality reduction are exactly 20-dimensional.
- Contrastive loss convergence: similarity between representation vectors from the two augmentations of the same image should increase during training; dissimilarity between representations from different images should increase (measured via contrastive loss metric).

## Limitations

- Augmentation parameters (color jitter strength, noise level, missing value percentage, intensity-dependent threshold) are not explicitly parameterized in the README; tuning for different ion image resolutions or SNR regimes may require empirical validation.
- The skill assumes preprocessed MSI matrix data with shape [X*Y, P]; raw instrument output (e.g., imzML, Analyze format) must be converted to this format beforehand.
- Intensity-dependent missing value process in ISO mode is designed specifically for isotope ions; applying it to non-isotopic co-localized ion images (COL mode) would be physically inconsistent.
- Python version is restricted to 3.5, 3.6, or 3.7; compatibility with modern Python ≥3.8 is not documented.

## Evidence

- [other] The COL mode augmentation applies four operations to ion images: color jitter, filtering, Poisson noise, and random missing value. The ISO mode includes all COL operations plus an additional intensity-dependent missing value process.: "T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO mode"
- [readme] Both augmentation pipelines feed into paired ResNet18 encoders that output 512-dimensional vectors for contrastive learning.: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] The data augmentation module generates two augmented images from each original ion image.: "The original ion image is first imported into the data augmentation module "T"  to generate two augmented images"
- [readme] COL mode is for co-localized ions from different molecules; ISO mode is for isotope ions from the same molecule.: "two modes of DeepION, denoted as "COL" and "ISO" are designed for the cases of regular co-localized ions from different molecules and isotope ions from a same molecule respectively"
- [readme] The final dimensionality reduction step produces a 20-dimensional vector for downstream tasks.: "This module is applied to further reduce the dimensionality of ion image representation to a 20-dimensional vector O for downstream tasks"
