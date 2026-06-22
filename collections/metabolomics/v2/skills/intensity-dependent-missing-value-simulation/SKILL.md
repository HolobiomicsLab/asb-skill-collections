---
name: intensity-dependent-missing-value-simulation
description: Use when augmenting mass spectrometry ion images in ISO mode (isotope ions from the same molecule) and you need to simulate intensity-dependent data loss that reflects real detector behavior where lower-intensity pixels are more likely to be missed or undetected.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ResNet18
  - Random missing value augmentation
  - Intensity-dependent missing value augmentation
  - kornia
  - PyTorch
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

# intensity-dependent-missing-value-simulation

## Summary

A data augmentation technique that selectively removes pixels from ion images based on their intensity levels, applied exclusively in ISO mode of the DeepION pipeline to simulate realistic photon-counting and detector artifacts in mass spectrometry imaging. This augmentation preserves the relationship between pixel intensity and missingness, which is critical for learning robust representations of isotope ions.

## When to use

Apply this skill when augmenting mass spectrometry ion images in ISO mode (isotope ions from the same molecule) and you need to simulate intensity-dependent data loss that reflects real detector behavior where lower-intensity pixels are more likely to be missed or undetected. Use it as a component of the T_ISO augmentation pipeline when preparing training data for contrastive learning of ion image representations.

## When NOT to use

- Input is a COL mode augmentation task (co-localized ions)—use only random missing value, not intensity-dependent removal.
- Ion image data lacks physical intensity variation or represents pre-processed binary/normalized data where intensity-missingness correlation is not meaningful.
- Downstream task requires complete pixel coverage or cannot tolerate systematic bias toward missing low-intensity pixels.

## Inputs

- Ion image matrix (2D array of pixel intensities)
- COL-mode augmented ion image (post color jitter, filtering, Poisson noise, random missing value)
- Intensity distribution metadata (to determine removal probability function)

## Outputs

- ISO-mode augmented ion image with intensity-dependent missing values
- Two augmented variants for contrastive learning (pair of images with selective pixel removal)

## How to apply

Execute this augmentation after all COL mode operations (color jitter, filtering, Poisson noise, and random missing value) have been applied to the ion image. Apply an intensity-dependent missing value process that selectively removes pixels based on their intensity levels—pixels with lower intensities should have higher removal probability than high-intensity pixels, modeling the physical reality that weak signal pixels are more prone to detection failure in mass spectrometry imaging. This process should be applied independently to each of the two augmented images propagated through the ResNet18 encoders to maximize diversity while maintaining the contrastive learning signal. The augmented images are then encoded into 512-dimensional representation vectors for downstream similarity maximization via contrastive loss.

## Related tools

- **ResNet18** (Encoder module that receives the augmented ISO-mode image pair and outputs 512-dimensional representation vectors for contrastive loss computation)
- **kornia** (Augmentation library dependency (version 0.4.1) used to implement filtering and other geometric augmentations in the pipeline)
- **PyTorch** (Deep learning framework (version 1.8.2) for tensor operations, contrastive loss computation, and model training)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode ISO --ion_mode positive --output_file Pos_ISO_result
```

## Evaluation signals

- Verify that the augmented ISO-mode image contains fewer non-zero pixels than the input, with a concentration of missing values among low-intensity regions (histogram of non-missing pixel intensities should shift toward higher values relative to input).
- Confirm that the intensity-dependent removal is applied stochastically—repeated augmentation of the same image should produce different missing-value patterns while maintaining the same intensity bias.
- Check that contrastive loss between the two ISO-mode augmented images converges during training, indicating that the encoder successfully learns to maximize similarity between augmentations despite intensity-dependent missing values.
- Validate that the final 512-dimensional representation vectors from both augmented images have high cosine similarity (typically > 0.7) before dimensionality reduction, confirming the augmentation preserves semantic structure.
- Ensure that ISO mode augmentations produce lower downstream co-localization false-discovery rates compared to COL mode alone when evaluated on known isotope-ion pairs from the training dataset.

## Limitations

- The skill assumes a monotonic relationship between pixel intensity and detection probability; it may not generalize to ion images with complex instrumental artifacts or non-linear detector response curves.
- Optimal intensity-dependent removal probability function is not specified in the article; practitioners must calibrate the intensity threshold and removal rate empirically for their specific mass spectrometry instrument and sample type.
- The augmentation is designed for the ISO mode (isotope ions); applying it to COL mode (co-localized ions) is explicitly contraindicated and may degrade model performance by introducing unnecessary intensity bias.
- Performance depends critically on the quality of input peak data and preprocessing; if the MSI matrix is already heavily filtered or intensity-normalized, the intensity-dependent mechanism may become ineffective.

## Evidence

- [readme] T_ISO introduces an additional process of intensity-dependent missing value in ISO mode: "T_ISO introduces an additional process of intensity-dependent missing value in ISO mode"
- [other] ISO mode includes all COL operations plus an additional intensity-dependent missing value process: "The ISO mode includes all COL operations plus an additional intensity-dependent missing value process."
- [other] For ISO mode: execute all COL mode augmentations, then apply intensity-dependent missing value process that selectively removes pixels based on their intensity levels: "For ISO mode: execute all COL mode augmentations, then apply intensity-dependent missing value process that selectively removes pixels based on their intensity levels."
- [readme] two modes of DeepION, denoted as COL and ISO are designed for the cases of regular co-localized ions from different molecules and isotope ions from a same molecule respectively: "two modes of DeepION, denoted as "COL" and "ISO" are designed for the cases of regular co-localized ions from different molecules and isotope ions from a same molecule respectively"
- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
