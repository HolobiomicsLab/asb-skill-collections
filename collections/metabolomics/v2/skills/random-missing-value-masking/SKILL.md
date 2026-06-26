---
name: random-missing-value-masking
description: Use when preparing ion image data for contrastive learning in mass spectrometry
  imaging (MSI), specifically when you need to augment single ion images into pairs
  of variants for encoder training in COL mode (co-localized ions) or as a base component
  of ISO mode (isotope ions).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - ResNet18
  - kornia
  - PyTorch
  techniques:
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
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

# random-missing-value-masking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A data augmentation technique that randomly masks a fraction of pixel values in ion images as missing to simulate incomplete detection in mass spectrometry imaging. This augmentation is applied during contrastive learning in DeepION to generate diverse augmented variants that improve representation robustness.

## When to use

Apply this skill when preparing ion image data for contrastive learning in mass spectrometry imaging (MSI), specifically when you need to augment single ion images into pairs of variants for encoder training in COL mode (co-localized ions) or as a base component of ISO mode (isotope ions). Use it to simulate realistic detection incompleteness in MSI data where pixel-level signal dropout occurs.

## When NOT to use

- Input data is already a learned low-dimensional representation (e.g., 20-dimensional embedding from Dimensionality Reduction module) — masking should only be applied to raw or pre-encoded ion images.
- The analysis goal is to preserve signal completeness for quantitative peak detection or absolute intensity measurements — random masking will corrupt intensity-dependent downstream analyses.
- Ion image has been preprocessed into a non-spatial format (e.g., flattened feature vectors) — the augmentation assumes 2D spatial structure.

## Inputs

- Ion image (single-channel or multi-channel 2D array, shape [height, width] or [height, width, channels])
- Raw pixel intensity values (NumPy array or tensor)
- Masking fraction parameter (float, 0 < fraction < 1)
- Random seed or generator state (optional, for reproducibility)

## Outputs

- Masked ion image with randomly zeroed/NaN pixels (same shape as input)
- Mask index map indicating which pixels were set to missing (optional, for debugging)

## How to apply

Within the T_COL augmentation pipeline, after applying color jitter, filtering, and Poisson noise to an input ion image, randomly select a fraction of pixel positions and set their intensity values to a missing/masked state (typically zero or NaN). Repeat this masking independently on each of the two augmented image variants generated for a contrastive pair. The masking probability and fraction should be tunable hyperparameters; the workflow suggests this step simulates incomplete detection inherent in MSI acquisition. Ensure both augmented outputs receive independent random masking to maintain diversity in the contrastive pair while preserving the spatial structure of the underlying ion image.

## Related tools

- **ResNet18** (Encoder that receives the augmented (masked) ion image pairs to produce 512-dimensional representation vectors after random-missing-value masking is applied.)
- **kornia** (Image augmentation and filtering library used within the T_COL pipeline alongside random-missing-value masking for color jitter and filtering operations.)
- **PyTorch** (Tensor computation framework used to implement and orchestrate the random masking operation on GPU for efficient augmentation.)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Verify that masked pixels have value 0 or NaN and are randomly distributed across the image with no spatial bias (histogram or heatmap of masked locations should be uniform).
- Confirm that the masking fraction (proportion of masked pixels / total pixels) matches the input parameter within ±1%.
- Check that two independent masked variants of the same source image differ in their masked pixel locations (masks should not be identical between augmented pairs).
- Validate that the spatial structure of non-masked regions is preserved and contrastive encoder loss converges when receiving masked augmented pairs (encoder should learn invariant representations despite missing pixels).
- Ensure output tensor shape matches input shape and data type is preserved (float32/float64).

## Limitations

- Masking is applied uniformly at random without spatial correlation; real MSI detection failure may exhibit spatial clustering or instrument-specific patterns not captured by uniform random masking.
- Very high masking fractions (>50%) may result in degraded representation learning if too much signal is removed before encoder propagation; optimal masking fraction is a hyperparameter not specified in the article.
- This augmentation assumes pixel-level independence; it does not account for molecular correlations or isotope patterns that might be corrupted by arbitrary pixel dropout.
- README does not specify whether masking uses zero-filling or NaN; both may affect downstream loss computation in contrastive learning depending on encoder handling of missing values.

## Evidence

- [other] The T_COL augmentation module in COL mode applies four transformations to an input ion image: color jitter, filtering, Poisson noise, and random missing value: "The T_COL augmentation module in COL mode applies four transformations to an input ion image: color jitter, filtering, Poisson noise, and random missing value, generating two augmented images for"
- [other] Randomly mask a fraction of pixel values as missing to simulate incomplete detection: "Randomly mask a fraction of pixel values as missing to simulate incomplete detection."
- [other] Repeat steps 2–5 independently to generate a second augmented variant: "Repeat steps 2–5 independently to generate a second augmented variant."
- [readme] The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode: "The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process"
- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
