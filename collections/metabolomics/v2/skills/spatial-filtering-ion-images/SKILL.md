---
name: spatial-filtering-ion-images
description: Use when preparing raw ion image data from mass spectrometry imaging for deep learning-based representation learning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3564
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ResNet18
  - kornia
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
---

# spatial-filtering-ion-images

## Summary

Apply spatial filtering (e.g., Gaussian or morphological filters) to ion images in mass spectrometry imaging as part of data augmentation to reduce noise and smooth pixel intensity variations while preserving ion localization patterns. This preprocessing step is used to generate augmented image pairs for contrastive representation learning in DeepION.

## When to use

Apply this skill when preparing raw ion image data from mass spectrometry imaging for deep learning-based representation learning. Filtering is specifically indicated when: (1) the ion image contains high-frequency noise or acquisition artifacts that would interfere with contrastive loss optimization, (2) you are generating augmented image pairs for either COL (co-localized ion) or ISO (isotope ion) modes in DeepION, or (3) you need to produce consistent, smoothed versions of the same ion image to maximize similarity between augmented pairs while preserving meaningful spatial structure.

## When NOT to use

- Do not apply spatial filtering if the raw ion image has already been smoothed or filtered during mass spectrometry acquisition preprocessing — double-filtering may remove critical localization information.
- Do not use aggressive filtering (large kernel, high blur) if the ion signal spatial resolution is already marginal relative to pixel size — you risk collapsing distinct co-localized or isotope ion patterns into undifferentiable blobs.
- Do not apply filtering in isolation; it must be part of the full T_COL or T_ISO augmentation pipeline (including color jitter, Poisson noise, and missing value augmentation) to avoid bias in the contrastive representation learning.

## Inputs

- Raw ion image matrix (2D pixel array with intensity values)
- Ion image shape parameters (X, Y pixel dimensions)
- Filter type and kernel parameters (e.g., Gaussian kernel size, standard deviation)

## Outputs

- Spatially filtered ion image (2D pixel array, same shape as input)
- Filtered image pair (two identically filtered versions from one raw image for augmentation pipeline)

## How to apply

Integrate spatial filtering as one of four sequential augmentation operations applied to each raw ion image in the Data Augmentation module (T_COL or T_ISO). The filtering step is applied after loading the raw ion image and before or after other augmentations (color jitter, Poisson noise, random missing value). Use a standard spatial filter (e.g., Gaussian blur via kornia library as indicated in the requirements) with kernel size and standard deviation chosen to smooth local pixel neighborhoods without obliterating ion localization boundaries. The same filter parameters must be applied identically to both augmented images generated from a single raw image to maximize their similarity for the contrastive loss objective. Filtering should reduce high-frequency artifacts while preserving the spatial extent of ion signals.

## Related tools

- **kornia** (Provides spatial filtering functions (Gaussian blur, morphological operations) for differentiable augmentation in PyTorch pipeline)
- **ResNet18** (Downstream encoder that processes filtered augmented ion images to extract 512-dimensional representation vectors)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Verify that filtered image retains spatial structure by confirming pixel intensity variance remains > 0 (not collapsed to uniform value) and that ion signal peaks are still localized (not smeared across entire image).
- Confirm that both augmented images from the same raw ion image produce identical or near-identical filtered outputs when the same filter kernel is applied, as required for effective contrastive learning.
- Check that high-frequency noise is reduced by computing local gradient magnitude or power spectrum — filtered image should show lower high-frequency power than raw image.
- Validate that the contrastive loss during training converges and that the learned 512-dimensional representation vectors from ResNet18 encoders show expected downstream task performance (e.g., co-localization or isotope discovery accuracy) compared to unfiltered baselines.
- Inspect visual output of filtered ion images alongside raw ion images to confirm that ion localization patterns are preserved and artifacts are reduced, without over-smoothing critical spatial details.

## Limitations

- Filtering choice and kernel parameters are not explicitly specified in the README or article — practitioners must determine appropriate filter type and hyperparameters empirically for their specific mass spectrometry imaging data domain and ion mass range.
- Aggressive spatial filtering may suppress weak ion signals or fine spatial detail relevant to isotope or co-localization discovery, degrading downstream model performance.
- Filtering is a lossy operation; once applied, fine-scale localization information cannot be recovered. The augmentation strategy assumes that contrastive learning on smoothed pairs is preferable to learning on raw noisy pairs.

## Evidence

- [readme] T_COL including color jitter, filtering, Poisson noise, and random missing value: "The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode"
- [readme] Data augmentation module applies filtering as one of four sequential operations: "The original ion image is first imported into the data augmentation module "T" to generate two augmented images, where the T_COL including color jitter, filtering, Poisson noise, and random missing"
- [readme] Two augmented images propagated through shared ResNet18 encoders after augmentation: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] Contrastive loss ensures similarity between augmented pairs: "Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image"
