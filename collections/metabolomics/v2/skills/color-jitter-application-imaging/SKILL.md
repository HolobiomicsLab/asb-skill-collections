---
name: color-jitter-application-imaging
description: Use when preparing ion image data for representation learning in mass
  spectrometry imaging, specifically when you need to augment raw ion images to generate
  pairs of diverse views for contrastive loss training.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3564
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

# color-jitter-application-imaging

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Color jitter is a data augmentation technique applied to ion images in mass spectrometry imaging to introduce controlled intensity variations across pixel channels, improving model robustness in contrastive learning. It is a component of the T_COL augmentation pipeline used in both COL (co-localized ion) and ISO (isotope ion) modes of DeepION.

## When to use

Apply this skill when preparing ion image data for representation learning in mass spectrometry imaging, specifically when you need to augment raw ion images to generate pairs of diverse views for contrastive loss training. Use it before encoder propagation in either COL mode (co-localized ions from different molecules) or ISO mode (isotope ions from the same molecule).

## When NOT to use

- When ion images have already been normalized or standardized to fixed intensity ranges, as jitter may violate assumptions of downstream intensity-dependent masking steps.
- When the goal is deterministic ion image reconstruction or registration rather than representation learning, as stochastic augmentation introduces irreversible variation.
- When working with single-ion (non-paired) image analysis, as color jitter's primary value derives from generating diverse augmented pairs for contrastive loss.

## Inputs

- Raw ion image (2D spatial array with pixel intensity values, shape [X, Y] where X and Y are pixel coordinates)
- Ion image preprocessed from mass spectrometry imaging matrix data [X*Y, P] flattened and reshaped to [X, Y]

## Outputs

- Color-jittered ion image (same spatial shape [X, Y] with intensity values perturbed within jitter bounds)
- Pair of independently color-jittered images for contrastive learning

## How to apply

Color jitter is applied as the first step in the T_COL augmentation module to a raw ion image before downstream augmentations (filtering, Poisson noise, random missing value). The jitter introduces random, bounded perturbations to pixel intensity values across color channels to simulate realistic imaging variations. In the ISO mode workflow, color jitter is applied identically to both augmented images generated from a single ion image, ensuring that intensity variations are independent across the pair. The jitter magnitude and channel-wise variation bounds should be calibrated to preserve ion spatial structure while increasing view diversity without saturating or zeroing pixel values. Color jitter precedes the intensity-dependent missing-value masking step in ISO mode, allowing intensity-dependent dropout to operate on already-jittered images for more robust isotope ion discovery.

## Related tools

- **kornia** (Image augmentation and computer vision library used to implement color jitter and other augmentations in the T_COL and T_ISO pipelines)
- **ResNet18** (Encoder backbone that receives color-jittered augmented image pairs to output 512-dimensional representation vectors)
- **PyTorch** (Deep learning framework providing tensor operations and differentiable transformations for color jitter implementation)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode ISO --ion_mode positive --output_file Pos_ISO_result
```

## Evaluation signals

- Color-jittered image pair should exhibit independent intensity perturbations: pixel-by-pixel differences between the two jittered views from the same source image should be non-zero and random, not deterministic.
- Jittered pixel values should remain within valid intensity bounds (e.g., [0, 1] or original dynamic range) without clipping or saturation artifacts.
- Spatial structure and ion localization patterns in the jittered image should be qualitatively preserved; visual inspection should confirm that peaks and spatial features remain recognizable.
- Contrastive loss on augmented image pairs should decrease during training, indicating that the encoder learns meaningful representations despite color jitter variation.
- Downstream isotope discovery (ISO mode) or co-localization search (COL mode) metrics (e.g., recall of known isotope pairs, enrichment of co-localized ions) should not degrade when color jitter is enabled, confirming that augmentation aids rather than corrupts signal.

## Limitations

- Color jitter intensity bounds must be tuned empirically for each mass spectrometry imaging dataset; over-aggressive jitter may obscure weak ion signals or create false intensity patterns.
- Color jitter assumes that pixel-wise intensity perturbations are independent across channels and space, which may not reflect realistic instrument noise or chemical variability in heterogeneous tissue.
- The effectiveness of color jitter depends on the dynamic range of the input ion image; images with low signal-to-noise ratio may show degraded representation learning if jitter magnitudes are not carefully balanced.
- Color jitter is applied stochastically at runtime, so identical ion images will produce different augmented pairs across epochs, which may increase training variance if not regularized by adequate batch size and projection/prediction modules.

## Evidence

- [readme] T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value: "The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO"
- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] The original ion image is first imported into the data augmentation module T to generate two augmented images: "The original ion image is first imported into the data augmentation module "T"  to generate two augmented images"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training"
