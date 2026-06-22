---
name: poisson-noise-generation
description: Use when when preparing augmented variants of ion images (single-channel 2D arrays or multi-channel spectral images) for contrastive learning in mass spectrometry imaging tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# poisson-noise-generation

## Summary

Generate synthetic Poisson noise matched to ion image intensity to simulate the shot-noise characteristics of mass spectrometry imaging detectors. This augmentation step is applied during contrastive learning to improve model robustness to realistic detector noise.

## When to use

When preparing augmented variants of ion images (single-channel 2D arrays or multi-channel spectral images) for contrastive learning in mass spectrometry imaging tasks. Apply this skill as part of the T_COL or T_ISO augmentation pipeline in DeepION when you need to generate realistic detector noise that varies with local image intensity, particularly for co-localized ion (COL mode) or isotope (ISO mode) analyses.

## When NOT to use

- Input is already a final learned representation vector (e.g., 512-dimensional encoder output or 20-dimensional reduced embedding) — apply augmentation only to raw or preprocessed ion images.
- The ion image has already undergone Poisson noise addition in a prior preprocessing step — avoid double-noising unless explicitly designing for noise robustness.
- Data are simulated or synthetic Poisson point clouds unrelated to MSI detector output — the intensity-matched sampling assumption may not hold.

## Inputs

- Preprocessed ion image (single-channel 2D array or multi-channel spectral image, shape [height, width] or [height, width, channels])
- Image intensity values as floating-point or integer array

## Outputs

- Noise-augmented ion image with same shape as input, containing pixel values perturbed by Poisson-distributed noise

## How to apply

Sample Poisson noise from a distribution with intensity parameter λ matched to the pixel intensities of the preprocessed ion image. For each pixel, draw a noise sample from Poisson(intensity[pixel]) and add it to the pixel value. This noise generation should be applied independently for each of the two augmented image variants to ensure diversity in the contrastive pair. The intensity-dependent sampling ensures that high-intensity regions (strong ion signals) receive proportionally larger noise than low-intensity regions, mimicking the behavior of photomultiplier tubes and other MSI detectors. Apply this after color jitter and filtering but before random missing value masking to preserve the noise structure.

## Related tools

- **ResNet18** (Encoder that processes augmented ion images (with Poisson noise applied) to extract 512-dimensional representation vectors for contrastive learning)
- **kornia** (Utility library for image transformations and filtering operations applied alongside Poisson noise in the T_COL/T_ISO augmentation pipeline)
- **PyTorch** (Framework for sampling from Poisson distribution and tensor-based image augmentation)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Verify that noise magnitude scales with image intensity: high-intensity pixels receive larger noise amplitude than low-intensity pixels.
- Confirm that the augmented image retains the same spatial and spectral dimensions as the input ion image.
- Check that both augmented image variants (generated independently) differ visibly in noise pattern while preserving overall ion localization patterns.
- Validate that contrastive loss values decrease during training, indicating that the encoder is learning invariance to the Poisson-noise augmentation.
- Confirm that the final 512-dimensional representation vectors from the encoder show high cosine similarity between the two noise-augmented variants of the same ion image.

## Limitations

- Poisson noise sampling assumes ideal shot-noise behavior; real MSI detectors may exhibit additional noise sources (e.g., thermal noise, readout noise) not captured by intensity-matched Poisson sampling.
- The augmentation may blur or distort fine spatial features if noise amplitude is very large relative to signal; tuning the intensity-to-lambda mapping is required for different ion image ranges.
- Random seed control is critical for reproducibility; variations in random state can produce qualitatively different noise-augmented pairs and affect contrastive learning convergence.

## Evidence

- [intro] Poisson noise sampling matched to image intensity: "Add Poisson noise sampled from a Poisson distribution matched to the image intensity."
- [intro] Application in COL mode augmentation pipeline: "The T_COL augmentation module in COL mode applies four transformations to an input ion image: color jitter, filtering, Poisson noise, and random missing value"
- [intro] Dual augmented variants for contrastive learning: "Repeat steps 2–5 independently to generate a second augmented variant."
- [readme] T_COL composition in DeepION: "The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode"
- [readme] Contrastive loss application to augmented pairs: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training."
