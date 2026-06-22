---
name: deep-learning-model-loading-and-prediction
description: Use when when you have preprocessed MS/MS spectral data (normalized peak intensities and m/z values) and need to convert each spectrum into a learned molecular embedding vector for downstream matching against a reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Convolutional Neural Network (CNN)
  - PyTorch
  - spectra_inference_dataset_loader.py
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1101/2025.02.07.637102v1
  title: ChemEmbed
evidence_spans:
- perform predictions using a trained Convolutional Neural Network (CNN) model
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemembed_cq
    doi: 10.1101/2025.02.07.637102v1
    title: ChemEmbed
  dedup_kept_from: coll_chemembed_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.02.07.637102v1
  all_source_dois:
  - 10.1101/2025.02.07.637102v1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-model-loading-and-prediction

## Summary

Load a pre-trained Convolutional Neural Network model and apply it to preprocessed mass spectrometry spectra to generate multidimensional molecular embedding vectors. This skill transforms normalized MS/MS peak data into high-dimensional feature representations suitable for metabolite candidate matching.

## When to use

When you have preprocessed MS/MS spectral data (normalized peak intensities and m/z values) and need to convert each spectrum into a learned molecular embedding vector for downstream matching against a reference database. Use this skill immediately after data normalization and before candidate similarity matching.

## When NOT to use

- Input spectra are not preprocessed (raw peak lists or uncalibrated m/z values) — preprocess first using intensity thresholding and normalization.
- No trained CNN model is available for your ionization mode or instrument type — model must be pre-trained on compatible MS/MS data.
- You need interpretable chemical features or molecular fingerprints directly — embeddings are learned latent representations, not human-readable structural features.

## Inputs

- Preprocessed MS/MS spectral data (normalized peak intensities and m/z values)
- Path to trained CNN model file (.pth or equivalent PyTorch format)
- Configuration file (config.yaml) specifying model path and input file type

## Outputs

- Multidimensional molecular embedding vectors (one embedding per spectrum)
- Feature matrix in CSV or NumPy format with shape (num_spectra, embedding_dimension)
- Embeddings ready for cosine similarity matching against reference database

## How to apply

Initialize the trained CNN model from the ChemEmbed repository using the path specified in config.yaml under model_path_positive or model_path_negative (depending on ionization mode). Load each preprocessed spectrum sequentially into memory as a tensor containing normalized peak intensities and m/z values. Pass each spectrum through the forward pass of the CNN to extract a multidimensional embedding vector. Aggregate all embeddings into a feature matrix with one row per spectrum and one column per embedding dimension (typically several hundred dimensions). Save the aggregated embedding matrix to CSV or NumPy format. Verify output dimensions match the expected CNN architecture output size.

## Related tools

- **Convolutional Neural Network (CNN)** (Trained deep learning model that processes normalized MS/MS spectral tensors and outputs multidimensional embedding vectors) — https://github.com/massspecdl/ChemEmbed
- **PyTorch** (Deep learning framework used to load, execute, and manage the pre-trained CNN model) — https://github.com/massspecdl/ChemEmbed
- **spectra_inference_dataset_loader.py** (Custom module to load and batch preprocessed spectra data for CNN inference without SMILES annotations) — https://github.com/massspecdl/ChemEmbed

## Examples

```
python main.py --config config.yaml
```

## Evaluation signals

- Embedding matrix shape is (num_spectra, embedding_dimension), with dimension matching the CNN architecture output layer.
- All embedding values are numeric (float32 or float64) with no NaN or Inf entries.
- Each embedding vector has non-zero magnitude (L2 norm > 0) and exhibits variance across dimensions.
- Downstream cosine similarity matching between predicted embeddings and reference database embeddings produces numeric scores in the range [0, 1].
- Output file can be successfully loaded and has consistent dtypes and row/column counts across runs on the same input.

## Limitations

- The skill requires a pre-trained model; accuracy and generalization depend entirely on the training data and hyperparameters used during model development — no validation of model quality is performed during loading or prediction.
- Embedding predictions are deterministic only if the CNN uses no dropout or stochastic layers during inference; if the model includes dropout, set model.eval() to disable it.
- Input spectra must match the preprocessing and normalization scheme used during CNN training; mismatched preprocessing (e.g., different intensity thresholds or m/z resolution) may degrade embedding quality.
- The README notes that input file type must be set correctly (with_smiles or without_smiles) and that the adduct type must be specified; mismatches between adduct specification and actual spectral data can lead to incorrect candidate matching downstream.

## Evidence

- [other] Initialize the trained Convolutional Neural Network (CNN) model from the ChemEmbed repository. 2. Pass each spectrum through the CNN to extract multidimensional molecular embedding vectors.: "Initialize the trained Convolutional Neural Network (CNN) model from the ChemEmbed repository. 3. Pass each spectrum through the CNN to extract multidimensional molecular embedding vectors."
- [other] Load preprocessed MS/MS spectral data (normalized peak intensities and m/z values) into memory.: "Load preprocessed MS/MS spectral data (normalized peak intensities and m/z values) into memory."
- [other] Aggregate embeddings into a feature matrix with one row per spectrum and embedding dimension as columns.: "Aggregate embeddings into a feature matrix with one row per spectrum and embedding dimension as columns."
- [readme] Model Prediction: Utilizes a pre-trained CNN model to predict molecular embeddings from spectra data.: "Model Prediction: Utilizes a pre-trained CNN model to predict molecular embeddings from spectra data."
- [readme] model_path: Path to the pre-trained CNN model file.: "model_path: Path to the pre-trained CNN model file."
