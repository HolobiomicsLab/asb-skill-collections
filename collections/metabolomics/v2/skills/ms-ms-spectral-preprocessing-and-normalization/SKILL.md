---
name: ms-ms-spectral-preprocessing-and-normalization
description: Use when you have a labelled dataset of raw MS/MS spectra annotated as 'relevant' (compounds of interest) or 'other' (reference standards or non-target compounds) and need to prepare them for supervised classifier training.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3474
  tools:
  - AnnoMe
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1093/bioadv/vbag111
  title: AnnoMe
evidence_spans:
- This is a package for the classification of MS/MS spectra of novel compounds
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_annome_cq
    doi: 10.1093/bioadv/vbag111
    title: AnnoMe
  dedup_kept_from: coll_annome_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbag111
  all_source_dois:
  - 10.1093/bioadv/vbag111
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS/MS spectral preprocessing and normalization

## Summary

Prepare raw MS/MS spectral data for machine learning classification by applying built-in normalization and feature extraction procedures. This skill is essential to standardize spectral intensities and extract discriminative features before training binary classifiers to distinguish compounds of interest from other compounds.

## When to use

Apply this skill when you have a labelled dataset of raw MS/MS spectra annotated as 'relevant' (compounds of interest) or 'other' (reference standards or non-target compounds) and need to prepare them for supervised classifier training. Use it as the first step before splitting data into training and validation subsets.

## When NOT to use

- Input spectra are already processed and embedded (e.g., MS2DeepScore embeddings); skip to classifier training.
- Data are already in a normalized feature table format; proceed directly to train/validation splitting.
- Spectra lack quality metadata or annotation labels; preprocessing cannot proceed without ground truth labels.

## Inputs

- Labelled MS/MS spectral dataset (MGF or vendor format) with spectra annotated as 'relevant' or 'other'
- Reference standards MS/MS spectra
- MS/MS spectra from repositories (e.g., GNPS, MassBank)

## Outputs

- Normalized and feature-extracted MS/MS spectral matrix (numeric format suitable for classifier training)
- Preprocessed training subset
- Preprocessed validation subset

## How to apply

Load the labelled MS/MS spectral dataset (in MGF or equivalent format) into AnnoMe and invoke its built-in normalization and feature extraction routines. Normalization standardizes peak intensities across spectra to remove instrumental and concentration-dependent variation. Feature extraction transforms raw m/z and intensity pairs into a uniform numerical representation suitable for machine learning. Apply these preprocessing steps uniformly to both 'relevant' and 'other' class spectra before partitioning into training and validation subsets, ensuring that the training classifier receives consistently formatted input.

## Related tools

- **AnnoMe** (Provides built-in normalization and feature extraction routines for MS/MS spectra; orchestrates the complete preprocessing pipeline before classifier training) — https://github.com/chrboku/AnnoMe

## Examples

```
uv run annome_classificationgui  # Load labelled MGF file, invoke built-in normalization and feature extraction, then proceed to train/validation split and classifier training.
```

## Evaluation signals

- Verify all spectra in the output matrix have consistent dimensionality (same number of features)
- Check that normalized intensities fall within expected bounds (e.g., [0, 1] or [0, 100]) across all spectra
- Confirm that 'relevant' and 'other' class labels are preserved through preprocessing and correctly mapped to rows
- Validate that preprocessing reduces within-class variance while preserving between-class separation (e.g., via PCA visualization or Fisher's discriminant ratio)
- Ensure that train/validation splits maintain the same class balance ratios as the full preprocessed dataset

## Limitations

- Classification of MS/MS spectra into substance classes is non-trivial and most often unsuccessful, especially when the training dataset is highly imbalanced; preprocessing alone cannot resolve this fundamental challenge.
- The MS2DeepScore embedding generation step (most computationally expensive phase) requires 4+ hours on standard laptops and may fail on less powerful hardware; preprocessing should be performed once and embeddings cached to disk.
- Preprocessing quality depends critically on the composition and labelling accuracy of the input dataset; mislabelled or biased training data will propagate through normalization into downstream classifier performance.

## Evidence

- [other] The normalization and feature extraction step in the workflow ensures uniform representation before classifier training.: "Preprocess spectra using AnnoMe's built-in normalization and feature extraction."
- [readme] AnnoMe explicitly implements preprocessing as part of its binary classification pipeline.: "This is a package for the classification of MS/MS spectra of novel compounds into either "relevant" or "other" compounds."
- [readme] Training classifiers requires initial preprocessing of large heterogeneous MS/MS spectral datasets.: "the classifiers first need to be trained on a large set of MS/MS spectra of compounds of interest (e.g., obtained from reference standards) and others (e.g., obtained from reference standards of"
- [other] The preprocessing step must be applied before partitioning the dataset for model training.: "Split dataset into training and validation subsets."
