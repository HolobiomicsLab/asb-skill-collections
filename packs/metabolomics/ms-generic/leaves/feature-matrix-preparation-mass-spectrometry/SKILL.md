---
name: feature-matrix-preparation-mass-spectrometry
description: Use when when you have raw mass spectrometry spectral data (peak intensities across m/z values) and need to feed it into MLP or GNN models for metabolite annotation, or when you need to generate LDA topic labels as auxiliary multi-task learning targets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - LDA (Latent Dirichlet Allocation)
  - Latent Dirichlet Allocation (LDA)
  - scikit-learn
  - RDKit
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btae490
  title: ESP
evidence_spans:
- spectral topic labels obtained using LDA (Latent Dirichlet Allocation)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_esp_cq
    doi: 10.1093/bioinformatics/btae490
    title: ESP
  dedup_kept_from: coll_esp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae490
  all_source_dois:
  - 10.1093/bioinformatics/btae490
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-matrix-preparation-mass-spectrometry

## Summary

Preparation of normalized spectral feature matrices from mass spectrometry data for input to machine learning models in metabolite annotation. This skill transforms raw or binned m/z peak intensities into a structured numerical representation suitable for supervised and multi-task learning on neural network architectures.

## When to use

When you have raw mass spectrometry spectral data (peak intensities across m/z values) and need to feed it into MLP or GNN models for metabolite annotation, or when you need to generate LDA topic labels as auxiliary multi-task learning targets. Use this skill before applying LDA or training neural network predictors on spectral data.

## When NOT to use

- Input is already a preprocessed feature table or tensor in machine-readable format (e.g., .pkl, .pt files); skip directly to model training.
- Your goal is only peak detection or quality control; use a simpler preprocessing pipeline focused on signal-to-noise filtering instead.
- Raw data is in a proprietary vendor format requiring instrument-specific decoding; first convert to open formats (mzML, mzXML) using standard conversion tools.

## Inputs

- Raw mass spectrometry spectral data with peak m/z values and intensities
- Spectrum identifiers (unique IDs for each spectrum)
- Resolution parameter for m/z binning (e.g., 1000 bins) or peak intensity normalization method

## Outputs

- Normalized spectral feature matrix (rows=spectra, columns=m/z bins or normalized features)
- Structured table mapping spectrum identifiers to feature vectors
- Spectral feature matrix suitable for LDA or neural network input

## How to apply

Load the raw spectral data and apply preprocessing: normalize peak intensities (e.g., to unit norm or relative abundance) or bin the m/z values into fixed resolution bins (e.g., 1000 bins across the m/z range) to create a dense feature matrix. Each row represents a spectrum (identified by a spectrum ID), and each column represents a normalized intensity or binned m/z feature. Verify that the resulting matrix has consistent dimensionality across all spectra and that normalization or binning preserves meaningful spectral patterns. The preprocessed feature matrix then serves as input to downstream LDA topic modeling or direct model training. Check that feature distributions are reasonable (no zero-variance columns, values in expected ranges) before proceeding to multi-task learning.

## Related tools

- **Latent Dirichlet Allocation (LDA)** (Downstream application: receives the preprocessed feature matrix to extract spectral topic labels as auxiliary multi-task learning targets for MLP and GNN models.)
- **scikit-learn** (Provides preprocessing utilities (normalization, binning, feature scaling) and may implement LDA for topic modeling.)
- **RDKit** (Supports chemical structure representation and mol object storage (mol_dict.pkl) used alongside spectral features in the ESP pipeline.)

## Evaluation signals

- Feature matrix has consistent dimensionality across all spectra (no missing or ragged rows).
- Normalized feature values fall within expected range (e.g., [0, 1] for unit norm or relative abundance; no NaN or infinite values).
- Spectrum identifier table correctly maps each spectrum ID to its corresponding feature vector row; no duplicates or misalignments.
- LDA applied to the feature matrix produces meaningful and interpretable topic distributions across the spectrum population (verified by domain expert inspection of topic-peak associations).
- Feature matrix retains sufficient variance and signal intensity distribution to support discriminative learning by downstream MLP/GNN models (check via PCA or variance analysis).

## Limitations

- Binning resolution (e.g., 1000 bins) is a hyperparameter that may need tuning; coarse binning loses mass accuracy, while fine binning creates sparse matrices.
- Normalization method (unit norm, relative abundance, etc.) affects downstream LDA and model training; choice must align with spectral intensity interpretation and dataset characteristics.
- Very low-intensity peaks or noise may be retained after normalization, potentially degrading LDA topic quality; consider applying intensity thresholds or signal-to-noise filtering before feature matrix construction.
- Feature matrix preparation does not inherently handle batch effects, instrument drift, or inter-sample variability; additional batch correction or standardization may be required for cross-dataset robustness.

## Evidence

- [other] Load preprocessed spectral feature matrix (normalized peak intensities or binned m/z representation) from the dataset.: "Load preprocessed spectral feature matrix (normalized peak intensities or binned m/z representation) from the dataset."
- [other] Apply LDA (Latent Dirichlet Allocation) to the spectral features, setting the number of topics as a hyperparameter (typically inferred from domain knowledge or cross-validation).: "Apply LDA (Latent Dirichlet Allocation) to the spectral features, setting the number of topics as a hyperparameter"
- [other] Verify label distribution across the dataset and validate that topics capture meaningful spectral patterns before passing labels to MLP and GNN multi-task training.: "Verify label distribution across the dataset and validate that topics capture meaningful spectral patterns before passing labels to MLP and GNN multi-task training."
- [readme] pos_train.csv is the NPLIB1 dataset in csv format. mol_dict.pkl is a dictionary mapping InChiKeys to rdkit mol objects.: "pos_train.csv is the NPLIB1 dataset in csv format. mol_dict.pkl is a dictionary mapping InChiKeys to rdkit mol objects."
- [intro] the MLP and GNN are enhanced by: 1) multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies among spectra peaks.: "multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies among spectra peaks"
