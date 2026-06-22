---
name: contrastive-pair-generation
description: Use when you have raw ion images from MSI data and need to train a contrastive encoder to learn stable, mode-specific representations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# contrastive-pair-generation

## Summary

Generate paired augmented images from a single ion image in mass spectrometry imaging (MSI) to enable contrastive learning. This skill is essential for training representation models that learn meaningful low-dimensional embeddings of ion spatial distributions while avoiding collapsed solutions.

## When to use

Apply this skill when you have raw ion images from MSI data and need to train a contrastive encoder to learn stable, mode-specific representations. Use it specifically when your downstream task is co-localized ion discovery (COL mode) or isotope ion identification (ISO mode), and you want to maximize similarity between augmented views of the same image while preventing representation collapse.

## When NOT to use

- When the input ion image is already a pre-computed 512-dimensional or lower-dimensional representation vector; augmentation is only meaningful on raw or reconstructed spatial images.
- When your analysis goal is descriptive spatial visualization rather than learning transferable representations; augmentation overhead is unnecessary if you only need to visualize raw ion distributions.
- When downstream tasks do not require robustness to intensity variations or missing values (e.g., simple peak intensity comparison without spatial context).

## Inputs

- Raw ion image (2D pixel intensity matrix)
- MSI matrix data with shape [X*Y, P] where X, Y are horizontal/vertical pixel counts and P is ion count
- Mode specification: 'COL' or 'ISO'
- Pixel intensity values for intensity-dependent masking (ISO mode only)

## Outputs

- First augmented ion image (T_COL applied)
- Second augmented ion image (T_COL + T_ISO for ISO mode, or T_COL for COL mode)
- Paired augmented image tuple for contrastive encoder input

## How to apply

Load the raw ion image and extract pixel intensity values. Apply the T_COL augmentation suite (color jitter, filtering, Poisson noise, random missing value) to create the first augmented image. Apply the identical T_COL transformations to create a second augmented image. For ISO mode only, apply an additional intensity-dependent missing-value masking step to the second augmented image, where the probability of a pixel being masked is conditioned on its intensity value. Output both augmented images as a paired tuple for propagation through shared-parameter ResNet18 encoders. The contrastive loss will then maximize similarity between the two views while a stop-gradient operation prevents representation collapse.

## Related tools

- **ResNet18** (Shared-parameter encoder that processes both augmented images in parallel to produce 512-dimensional representation vectors for contrastive loss computation) — https://github.com/gankLei-X/DeepION
- **kornia** (Provides differentiable implementations of color jitter, filtering, and other augmentation transforms in the T_COL and T_ISO pipeline)
- **PyTorch** (Deep learning framework enabling efficient tensor-based augmentation, encoder propagation, and contrastive loss optimization)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode ISO --ion_mode positive --output_file Pos_ISO_result
```

## Evaluation signals

- Both augmented images retain spatial structure (pixel coordinates and local intensity patterns are preserved after augmentation); verify by visual inspection or local autocorrelation comparison.
- T_COL transforms (color jitter, filtering, Poisson noise, random missing value) are applied identically to both images; verify by recording and comparing random seeds or augmentation parameters used for each image.
- For ISO mode, the second augmented image has additional intensity-dependent missing value masking; verify by checking that masked pixels in the second image correlate with low/high intensity regions according to the learned masking function.
- Paired augmented images produce similar 512-dimensional encoder outputs before projection; verify by computing cosine similarity or Euclidean distance between encoder outputs and confirming it is higher than random image pairs.
- Contrastive loss decreases during training and representation collapse is prevented; verify by monitoring that the norm of representation vectors remains stable (neither exploding nor shrinking to zero).

## Limitations

- Intensity-dependent missing value masking (T_ISO) assumes pixel intensity is a meaningful proxy for data quality; if intensity variation is noise rather than signal, the masking may discard valuable spatial information.
- Random missing value and intensity-dependent masking may remove genuine biological signal at certain intensity ranges, potentially biasing learned representations toward mid-range intensities.
- Poisson noise and color jitter are heuristic approximations of real MSI measurement variability; the augmentation may not capture all sources of systematic error in the instrument or preprocessing pipeline.
- The skill requires careful tuning of augmentation hyperparameters (jitter magnitude, filter kernels, noise level, masking probability function); suboptimal choices can lead to uninformative or over-regularized representations.

## Evidence

- [other] T_ISO augmentation extends T_COL by introducing an additional intensity-dependent missing value process specifically for the ISO mode to generate two augmented images from an original ion image.: "T_ISO augmentation extends T_COL (which includes color jitter, filtering, Poisson noise, and random missing value) by introducing an additional intensity-dependent missing value process specifically"
- [readme] Two augmented images are propagated through ResNet18-based encoders to output 512-dimensional representation vectors.: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] Projection and Prediction modules are used to avoid collapsing solutions and ensure meaningful representation learning with contrastive loss.: "Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image and ensure to"
- [readme] T_COL includes color jitter, filtering, Poisson noise, and random missing value, while T_ISO introduces intensity-dependent missing value in ISO mode.: "The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO"
