---
name: poisson-noise-injection-spectral
description: Use when augmenting mass spectrometry ion images for contrastive learning,
  specifically when you need to simulate the natural Poisson noise that arises from
  photon-counting detectors in mass spectrometry imaging experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
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

# Poisson Noise Injection for Spectral Augmentation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Poisson noise injection is a data augmentation technique applied to ion images in mass spectrometry imaging to simulate realistic photon-counting noise and improve model robustness to intensity-dependent noise artifacts. It is used as part of the T_COL augmentation pipeline in DeepION to generate contrastive image pairs for self-supervised representation learning.

## When to use

Apply this skill when augmenting mass spectrometry ion images for contrastive learning, specifically when you need to simulate the natural Poisson noise that arises from photon-counting detectors in mass spectrometry imaging experiments. Use it as part of a multi-step augmentation pipeline (alongside color jitter, filtering, and random missing values) to create two augmented image variants from a single raw ion image for contrastive loss optimization.

## When NOT to use

- Input is already a pre-processed feature table or low-dimensional representation (e.g., 20-dimensional vector O) — apply Poisson noise only to raw or semi-processed ion images.
- When intensity values are already heavily corrupted or normalized to a non-physical scale (e.g., log-transformed or standardized to zero mean) — Poisson sampling assumes intensity values represent photon counts.
- If the detector model for your MSI instrument is known to use non-Poisson noise characteristics (e.g., Gaussian readout noise or multiplicative noise) — verify the detector type before applying.

## Inputs

- Raw ion image (2D pixel intensity matrix, shape [X*Y, P] where X, Y are pixel coordinates and P is number of ions)
- Pixel intensity values (numeric array, non-negative real values)

## Outputs

- Poisson-noise-augmented ion image (2D pixel intensity matrix, same shape as input)
- Two augmented image variants (paired for contrastive learning)

## How to apply

Poisson noise injection is applied within the T_COL augmentation module by adding noise drawn from a Poisson distribution to pixel intensity values of the ion image. The process operates on intensity-dependent photon counts: for each pixel with intensity I, sample from Poisson(I) and use the result as the augmented intensity. This simulates detector noise inherent to mass spectrometry imaging. Apply this transformation to both augmented images identically during the data augmentation step, before encoder propagation. The rationale is that MSI detectors exhibit photon-counting noise proportional to signal intensity; training on artificially noisy variants improves the model's invariance to this natural noise source and strengthens learned representations for downstream isotope or co-localization discovery tasks.

## Related tools

- **kornia** (Image augmentation and transformation library used to implement photon-counting noise injection and other augmentations in the T_COL pipeline)
- **PyTorch** (Deep learning framework for tensor operations, Poisson sampling, and gradient computation during training)
- **ResNet18** (Encoder architecture that receives the Poisson-augmented image pair to extract 512-dimensional representations for contrastive learning)

## Examples

```
python run.py --input_Matrix .../Pos_brain_data_matrix.txt --input_PeakList .../Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Augmented image pixel intensity histograms should show variance proportional to original intensity values (approximate Poisson variance ≈ mean).
- Two augmented images derived from the same raw image should exhibit different Poisson noise realizations but identical overall intensity structure and spatial patterns.
- Downstream contrastive loss should converge and produce meaningful 512-dimensional representation vectors that cluster isotope ion images or co-localized ion pairs appropriately.
- Comparison of learned representations with and without Poisson augmentation should show improved robustness to intensity perturbations and better generalization to held-out test ion images.
- Visual inspection: augmented images should appear noisy but recognizable compared to raw inputs, without artificial artifacts or extreme outliers.

## Limitations

- Poisson noise sampling assumes pixel intensities are proportional to photon counts; if MSI data is already heavily preprocessed (e.g., normalized or log-transformed), Poisson noise may not reflect true detector characteristics.
- Poisson noise is appropriate for counting statistics at moderate-to-high signal levels; at very low intensities (single-digit photon counts), discrete effects may not be well-captured by continuous Poisson approximation.
- Requires raw or near-raw ion image data; integration with other augmentations (color jitter, filtering, random missing values) in the T_COL pipeline may interact in ways that reduce noise realism if applied in wrong order.
- No explicit guidance in the article on Poisson noise magnitude tuning or whether noise scale should be data-dependent; practitioners should validate choice against real detector noise profiles for their specific MSI instrument.

## Evidence

- [readme] T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value: "T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode"
- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] The original ion image is first imported into the data augmentation module to generate two augmented images: "The original ion image is first imported into the data augmentation module to generate two augmented images"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing"
- [intro] T_ISO augmentation extends T_COL (which includes color jitter, filtering, Poisson noise, and random missing value) by introducing an additional intensity-dependent missing value process: "T_COL (which includes color jitter, filtering, Poisson noise, and random missing value)"
