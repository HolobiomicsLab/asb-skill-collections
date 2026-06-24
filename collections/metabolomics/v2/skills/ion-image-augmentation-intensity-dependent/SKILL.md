---
name: ion-image-augmentation-intensity-dependent
description: Use when training a contrastive encoder on mass spectrometry imaging
  (MSI) data in ISO mode (isotope ions from the same molecule).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ResNet18
  - kornia
  - PyTorch
  techniques:
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.3c05002
  title: deepion
evidence_spans:
- Two augmented images are propagated through a pair of ResNet18-based encoders
- Two augmented images are propagated through a pair of ResNet18-based encoders that
  shared parameters
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

# Ion-Image Augmentation with Intensity-Dependent Missing Values

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

T_ISO augmentation extends base color jitter, filtering, and Poisson noise transformations by adding intensity-dependent missing-value masking to generate contrastive image pairs for isotope ion images in mass spectrometry imaging. This skill is essential when training representation models on isotope ion data where missing-value patterns should correlate with pixel intensity rather than occur uniformly.

## When to use

Apply this skill when training a contrastive encoder on mass spectrometry imaging (MSI) data in ISO mode (isotope ions from the same molecule). Use it specifically to generate two augmented image pairs from a single raw ion image when the downstream encoder requires contrastive learning with intensity-aware data augmentation.

## When NOT to use

- Input is already a feature table or pre-computed representation vector (skip to downstream projection module)
- Working in COL mode (co-localized ions); use base T_COL augmentation without intensity-dependent masking instead
- Raw MSI data is unpreprocessed or contains invalid/missing calibration information; preprocess first

## Inputs

- raw ion image (2D pixel array with intensity values)
- MSI matrix data [X*Y, P] where X, Y are pixel coordinates and P is ion count
- MSI peak data [P, 1] listing P ions

## Outputs

- augmented image pair (two 2D pixel arrays)
- 512-dimensional representation vector (after encoder propagation)

## How to apply

Load a preprocessed MSI ion image (raw pixel intensities). Apply T_COL augmentations (color jitter, filtering, Poisson noise, random missing value) to generate a first augmented image. Apply identical T_COL augmentations to create a second augmented image. On the second augmented image only, apply intensity-dependent missing-value masking, where the probability of masking each pixel is conditioned on that pixel's intensity value (e.g., higher-intensity pixels may have different masking probability than low-intensity pixels). Return both augmented images as a pair for propagation through shared-parameter ResNet18 encoders. The rationale is that isotope ions exhibit intensity-correlated spatial patterns; conditioning missing-value augmentation on intensity preserves this relationship while still creating meaningful contrastive pairs.

## Related tools

- **ResNet18** (Encoder backbone that receives both augmented image pairs and outputs 512-dimensional representation vectors with shared parameters between image pair)
- **kornia** (Image processing library used for color jitter, filtering, and geometric transformations in T_COL augmentation pipeline)
- **PyTorch** (Deep learning framework for implementing augmentation pipeline, encoder, and contrastive loss computation)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode ISO --ion_mode positive --output_file Pos_ISO_result
```

## Evaluation signals

- Verify that both augmented images are generated and have identical spatial dimensions to input
- Confirm that second augmented image has intensity-dependent masking applied (pixels with same intensity should have similar masking probability; masking probability should vary across intensity range)
- Check that first augmented image contains only T_COL augmentations (color jitter, filtering, Poisson noise, uniform random missing value) without intensity-dependent masking
- Validate that encoder produces 512-dimensional vectors with contrastive similarity maximized between the pair (via stop-gradient loss computation)
- Inspect that missing-value patterns in second image show correlation with underlying pixel intensity distribution (higher/lower intensity regions should exhibit predictable masking patterns)

## Limitations

- Intensity-dependent masking rationale is tailored to isotope ions (ISO mode); application to co-localized ions (COL mode) may degrade performance
- Missing-value function design (intensity → masking probability mapping) is not explicitly specified in source material; practitioner must infer or tune empirically
- Requires preprocessed MSI data with validated intensity calibration; noisy or poorly calibrated raw data may yield uninformative augmentations
- Contrastive learning assumes sufficient variation in ion image intensity; uniformly low-intensity images may not benefit from this approach

## Evidence

- [other] T_ISO augmentation extends T_COL (which includes color jitter, filtering, Poisson noise, and random missing value) by introducing an additional intensity-dependent missing value process specifically for the ISO mode to generate two augmented images from an original ion image.: "T_ISO augmentation extends T_COL (which includes color jitter, filtering, Poisson noise, and random missing value) by introducing an additional intensity-dependent missing value process specifically"
- [readme] the T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO mode.: "the T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO"
- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training.: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training"
- [readme] isotope ions from a same molecule: "isotope ions from a same molecule respectively"
