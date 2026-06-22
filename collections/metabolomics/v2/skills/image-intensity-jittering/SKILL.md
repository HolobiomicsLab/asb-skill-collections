---
name: image-intensity-jittering
description: Use when when preparing ion images (single-channel 2D arrays or multi-channel spectral images) from mass spectrometry imaging for contrastive learning in DeepION's COL or ISO modes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05002
  all_source_dois:
  - 10.1021/acs.analchem.3c05002
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# image-intensity-jittering

## Summary

Apply color jitter augmentation to ion images in mass spectrometry imaging to modulate pixel intensity values, generating varied augmented versions for contrastive learning. This technique helps prevent representation collapse and improves the robustness of learned embeddings.

## When to use

When preparing ion images (single-channel 2D arrays or multi-channel spectral images) from mass spectrometry imaging for contrastive learning in DeepION's COL or ISO modes. Use this skill when you need to create multiple augmented views of the same ion image to maximize similarity between augmentations in a self-supervised contrastive framework.

## When NOT to use

- Input data is already a low-dimensional representation vector (e.g., 512-D or 20-D embeddings from DeepION) — apply jittering only to raw or preprocessed ion images before encoding.
- Ion images have already undergone intensity normalization or standardization incompatible with pixel-level perturbations — verify preprocessing steps first.
- The analysis goal is not contrastive learning or self-supervised representation learning — color jitter is specifically designed to create useful negative pairs for contrastive loss.

## Inputs

- Single-channel 2D ion image array (X×Y pixel matrix)
- Multi-channel spectral image (X×Y×P, where P is number of ions)

## Outputs

- Jittered ion image (same shape as input, with modulated intensity values)
- Second independently jittered variant of the input image

## How to apply

Apply color jitter as the first transformation in the T_COL (COL mode) or T_ISO (ISO mode) augmentation pipeline. Color jitter modulates intensity values across the entire ion image by randomly perturbing pixel intensities within a reasonable range. This operation is applied independently to generate two separate augmented variants from a single input image. The jittered images are then fed sequentially through filtering, Poisson noise injection, and random missing value masking before being propagated through shared-parameter ResNet18 encoders. The rationale is that intensity perturbations that preserve spatial structure and relative ion intensity relationships enable the encoder to learn invariant representations robust to instrumental noise and detection variability in mass spectrometry imaging.

## Related tools

- **ResNet18** (Encoder that receives both jittered image variants to output 512-dimensional representation vectors) — https://github.com/gankLei-X/DeepION
- **kornia** (Library for image augmentation operations (likely used for color jitter implementation))

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Verify that the output image tensor has the same shape and data type as the input (2D or 3D array preserved).
- Confirm that pixel intensity values remain within physically meaningful ranges for ion images (no underflow to negative or overflow beyond instrument dynamic range).
- Check that two independent calls to the jitter function on the same input produce different outputs (stochasticity verified).
- Validate that spatial structure and relative ion localization patterns are preserved — jitter should perturb intensity, not shuffle pixel locations.
- Ensure that downstream contrastive loss converges and learned representations show improved clustering or co-localization prediction compared to unaggmented baselines.

## Limitations

- Color jitter alone does not account for instrument-specific noise characteristics — it must be combined with Poisson noise injection to model realistic mass spectrometry imaging noise.
- The magnitude of jitter is not specified in the article; practitioners must tune the intensity perturbation range empirically to balance augmentation strength without destroying chemical information.
- Intensity jittering may degrade performance on datasets where absolute ion intensity values carry diagnostic significance, requiring careful validation on domain-specific ion images.
- The technique assumes ion images have continuous or near-continuous intensity distributions; highly discrete or binary ion images may not benefit from intensity perturbation.

## Evidence

- [other] Color jitter as first transformation step: "Apply color jitter to modulate intensity values across the image."
- [other] Part of T_COL augmentation pipeline: "The T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode"
- [other] Independent generation of two augmented variants: "Repeat steps 2–5 independently to generate a second augmented variant."
- [other] Purpose in contrastive learning framework: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
