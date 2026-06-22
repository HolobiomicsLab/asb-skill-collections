---
name: col-mode-augmentation-pipeline-implementation
description: Use when when you have preprocessed mass spectrometry imaging (MSI) ion images and need to generate augmented image pairs for contrastive learning in co-localized ion discovery tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ResNet18
  - Color jitter augmentation
  - Filtering augmentation
  - Poisson noise augmentation
  - Random missing value augmentation
  - Intensity-dependent missing value augmentation
  - kornia
derived_from:
- doi: 10.1021/acs.analchem.3c05002
  title: deepion
evidence_spans:
- Two augmented images are propagated through a pair of ResNet18-based encoders
- T_COL including color jitter, filtering, Poisson noise, and random missing value
- T_ISO introduces an additional process of intensity-dependent missing value in ISO mode
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
---

# COL Mode Augmentation Pipeline Implementation

## Summary

Implementation of the COL (co-localized ions) data augmentation pipeline for ion images in mass spectrometry imaging, which applies four sequential augmentation operations to generate contrastive image pairs for deep learning models. This skill is essential when preparing ion image data for self-supervised representation learning in DeepION.

## When to use

When you have preprocessed mass spectrometry imaging (MSI) ion images and need to generate augmented image pairs for contrastive learning in co-localized ion discovery tasks. Apply this skill specifically when your analysis goal is to learn low-dimensional representations of ion images from different molecules that co-localize spatially, and you require synthetic variation in pixel intensities, spatial features, and noise patterns to prevent model collapse during training.

## When NOT to use

- Input is already a 512-dimensional or lower-dimensional representation vector — skip augmentation and proceed to projection/prediction modules.
- Your analysis goal is isotope ion discovery, not co-localized ion discovery — use ISO mode augmentation instead, which adds intensity-dependent missing value process.
- Ion images have been manually curated or preprocessed with existing augmentations — applying COL pipeline again may introduce redundant or conflicting transformations.

## Inputs

- Original ion image (2D array of pixel intensities)
- Ion image metadata (dimensions, ion mode: positive or negative)

## Outputs

- Two augmented ion images from COL pipeline (each 2D pixel array)
- 512-dimensional representation vectors (via ResNet18 encoder)

## How to apply

Load an original ion image and sequentially apply four augmentation operations in order: (1) color jitter to adjust pixel intensities stochastically, (2) filtering to smooth or enhance spatial features, (3) Poisson noise to simulate photon counting artifacts typical of mass spectrometry detectors, and (4) random missing value process to introduce arbitrary missing pixels at random locations. This sequence creates two distinct augmented versions of the same input image. The rationale is that augmentations must preserve the semantic content (co-localization pattern) while creating sufficient visual variation for the contrastive loss to learn invariant ion image representations. The four operations target different corruption modes observed in real MSI data: intensity fluctuations, edge artifacts, detector noise, and missing measurements.

## Related tools

- **ResNet18** (Encoder that propagates augmented images to output 512-dimensional representation vectors with shared parameters)
- **Color jitter augmentation** (Adjusts pixel intensities stochastically as first operation in COL pipeline)
- **Filtering augmentation** (Smooths or enhances spatial features in ion images as second operation)
- **Poisson noise augmentation** (Simulates photon counting artifacts characteristic of mass spectrometry detectors as third operation)
- **Random missing value augmentation** (Introduces arbitrary missing pixels at random locations as fourth operation in COL pipeline)
- **kornia** (Image transformation and augmentation library used for implementing augmentation operations)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Verify that exactly two distinct augmented images are generated per input ion image, with measurable pixel-level differences due to color jitter, filtering, Poisson noise, and random missing values.
- Confirm that both augmented images retain the spatial structure and co-localization pattern of the original image (visual inspection of ion distribution map should be similar between originals and augmentations).
- Check that the 512-dimensional representation vectors output from ResNet18 encoders have high cosine similarity (contrastive loss is minimized) between the two augmentations of the same image, confirming the model learned invariant representations.
- Validate that missing value locations differ between the two augmented images generated from the same original (random process is working correctly).
- Ensure downstream dimensionality reduction module can successfully reduce 512-dimensional vectors to 20-dimensional output without numerical instability or rank deficiency.

## Limitations

- COL mode augmentation is designed only for co-localized ion discovery; it does not include the intensity-dependent missing value process required for isotope ion analysis (ISO mode).
- The random missing value operation assumes pixels are missing uniformly at random; this may not accurately model systematic detector failures or spatial dead zones in real MSI instruments.
- Poisson noise simulation may not capture all real noise sources in mass spectrometry, such as baseline drift, chemical noise, or isobaric interference.
- The augmentation parameters (jitter magnitude, filter kernel size, Poisson lambda, missing value rate) are not explicitly provided in the README; practitioners must infer or tune them from the source code.
- Augmentation quality depends on preprocessing steps (normalization, baseline subtraction) applied before the pipeline; poorly preprocessed images will produce poor augmentations.

## Evidence

- [readme] T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode: "T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode"
- [readme] The original ion image is first imported into the data augmentation module "T"  to generate two augmented images: "The original ion image is first imported into the data augmentation module "T"  to generate two augmented images"
- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training"
- [readme] The ISO mode introduces an additional process of intensity-dependent missing value in ISO mode: "T_ISO introduces an additional process of intensity-dependent missing value in ISO mode"
