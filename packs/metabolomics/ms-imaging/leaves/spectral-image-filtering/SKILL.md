---
name: spectral-image-filtering
description: Use when when generating augmented variants of single-channel or multi-channel
  ion images for contrastive learning in mass spectrometry imaging analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3564
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ResNet18
  - kornia
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

# spectral-image-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply spatial filtering to ion images in mass spectrometry imaging (MSI) to smooth local intensity variations while preserving spatial structure for contrastive representation learning. This is a component of the T_COL data augmentation pipeline in DeepION for generating augmented ion image pairs.

## When to use

When generating augmented variants of single-channel or multi-channel ion images for contrastive learning in mass spectrometry imaging analysis. Use this skill as part of COL mode augmentation when you have preprocessed MSI data (2D ion intensity arrays) and need to create two independent augmented versions from a single input image to train representation encoders.

## When NOT to use

- Input ion images are already heavily smoothed or have been preprocessed with aggressive filtering — additional filtering may remove important spatial detail or ion localization signal.
- Analysis requires preservation of raw spectral resolution or peak fine structure — spatial filtering blurs intensity transitions and may obscure isotope or fragment ion distributions.
- Input is a feature vector or dimensionality-reduced representation rather than a raw 2D spatial image.

## Inputs

- single-channel 2D ion image array (X*Y pixel coordinates)
- multi-channel spectral ion image (X*Y*P, where P is number of ions)
- preprocessed MSI matrix with shape [X*Y, P]

## Outputs

- filtered ion image (same shape as input)
- smoothed intensity matrix suitable for downstream noise injection

## How to apply

Apply filtering (e.g., Gaussian or median filter) to modulate local intensity variations in the ion image after color jitter and before Poisson noise injection. The filtering step reduces pixel-level noise and smooths spatial gradients, making the augmented images more robust to fine-grained intensity fluctuations while preserving ion localization patterns. This filtering is applied independently to each of the two augmented variants generated from the same input, ensuring diversity in the augmentation pipeline. The choice between Gaussian (linear smoothing) and median (edge-preserving) filtering depends on whether you prioritize smooth gradients or preservation of sharp ion localization boundaries.

## Related tools

- **kornia** (spatial filtering library for image augmentation in deep learning)
- **ResNet18** (encoder that receives filtered augmented images to learn representations)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Verify output image shape matches input shape; no spatial dimensions should be lost or cropped.
- Check that intensity values remain within valid range (e.g., [0, max_intensity]); filtering should not introduce out-of-range artifacts.
- Confirm that two independently filtered variants from the same input show different spatial smoothing patterns, indicating independent augmentation application.
- Visual inspection: filtered image should show reduced pixel-level noise while ion spatial localization patterns remain recognizable compared to original.
- Downstream contrastive loss should show convergence when pairs of filtered images are passed through shared ResNet18 encoders, indicating meaningful augmentation.

## Limitations

- Aggressive filtering may over-smooth ion localization boundaries and reduce discriminative signal for rare or co-localized ions.
- Filter kernel size and type (Gaussian vs. median) are hyperparameters that require tuning; no universal setting is specified in the article for different MSI instrument types or spatial resolutions.
- Filtering is applied uniformly across all pixels; intensity-dependent or adaptive filtering is not mentioned in COL mode (though ISO mode introduces intensity-dependent missing value separately).
- The filtering step is not separately validated in isolation; its contribution to contrastive learning is evaluated only as part of the full four-step T_COL augmentation pipeline.

## Evidence

- [readme] color jitter, filtering, Poisson noise, and random missing value: "The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode"
- [other] filtering for smoothing: "Apply filtering (e.g., Gaussian or median filter) to smooth local intensity variations"
- [other] two augmented variants independently: "Repeat steps 2–5 independently to generate a second augmented variant"
- [readme] contrastive learning pipeline: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
