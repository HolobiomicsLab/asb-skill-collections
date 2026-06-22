---
name: multidimensional-feature-extraction-from-spectra
description: Use when you have preprocessed MS/MS spectral data (normalized peak intensities and m/z values) and need to transform spectra into fixed-dimensional molecular embeddings for candidate matching against a reference database, especially when direct spectral comparison or classical fingerprinting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - Convolutional Neural Network (CNN)
  - ChemEmbed
  - PyTorch
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
---

# multidimensional-feature-extraction-from-spectra

## Summary

Extract multidimensional molecular embedding vectors from mass spectrometry/MS spectral data using a pre-trained Convolutional Neural Network (CNN) model. The skill converts raw normalized peak intensities and m/z values into high-dimensional feature representations suitable for downstream metabolite identification and similarity matching.

## When to use

Apply this skill when you have preprocessed MS/MS spectral data (normalized peak intensities and m/z values) and need to transform spectra into fixed-dimensional molecular embeddings for candidate matching against a reference database, especially when direct spectral comparison or classical fingerprinting methods are insufficient for metabolite identification.

## When NOT to use

- Input spectral data is not normalized or has not been preprocessed (raw, unnormalized peak intensities may produce poor embeddings).
- You have only a small number of spectra (<10–20) and require immediate interpretability of individual features rather than learned representations.
- The target molecules fall outside the chemical space on which the pre-trained CNN model was trained, potentially producing unreliable embeddings.

## Inputs

- Preprocessed MS/MS spectral data (normalized peak intensities and m/z values)
- Pre-trained CNN model file (.pt or equivalent)
- MSP file (with or without SMILES annotations)
- Configuration file (config.yaml) specifying model path and input parameters

## Outputs

- Multidimensional molecular embedding vectors (feature matrix)
- CSV or NumPy format embedding file with one row per spectrum
- Feature matrix with embedding dimensions as columns

## How to apply

Load preprocessed MS/MS spectral data (normalized peak intensities and m/z values) into memory, then initialize a pre-trained CNN model from the ChemEmbed repository. Pass each spectrum sequentially through the CNN to extract multidimensional molecular embedding vectors from the model's learned representations. Aggregate the resulting embeddings into a feature matrix where each row corresponds to one spectrum and each column represents an embedding dimension. Save the aggregated embeddings to an output file in CSV or NumPy format. The CNN architecture learns hierarchical spectral features during training and produces dense vector representations that capture molecular similarity patterns implicit in the spectral data.

## Related tools

- **Convolutional Neural Network (CNN)** (Pre-trained deep learning model that processes mass spectrometry spectral data to extract multidimensional molecular embeddings through learned hierarchical feature representations) — https://github.com/massspecdl/ChemEmbed
- **ChemEmbed** (Framework repository providing the CNN model, data loaders, and inference pipeline for converting normalized MS/MS spectra into embeddings and matching them against reference databases) — https://github.com/massspecdl/ChemEmbed
- **PyTorch** (Deep learning framework used for model implementation and inference)

## Examples

```
python main.py --config config.yaml
```

## Evaluation signals

- Output embedding matrix has the correct shape: number of rows equals number of input spectra, number of columns equals the CNN model's embedding dimensionality.
- No NaN or Inf values present in the embedding matrix; all values are finite floating-point numbers.
- Embeddings from chemically similar spectra (high cosine similarity in reference database) cluster together when visualized in embedding space using dimensionality reduction (t-SNE or UMAP).
- Downstream candidate matching using the embeddings retrieves reference molecules with m/z and fragmentation patterns consistent with the input spectra.
- Embeddings can be successfully saved to the specified output file (CSV or NumPy) and reloaded without data corruption.

## Limitations

- The quality of embeddings depends critically on the pre-trained CNN model; embeddings for out-of-distribution molecules or spectra from novel ionization modes may be unreliable.
- The framework requires normalized MS/MS spectral data as input; poorly preprocessed or noisy raw spectra will degrade embedding quality.
- Computational cost scales linearly with the number of spectra; processing large spectral databases may require GPU acceleration (PyTorch supports CUDA).
- The CNN model is task-specific to the chemical space and MS/MS acquisition parameters on which it was trained; transfer to different instruments or chemical libraries may require model retraining or fine-tuning.

## Evidence

- [other] Load preprocessed MS/MS spectral data (normalized peak intensities and m/z values) into memory: "Load preprocessed MS/MS spectral data (normalized peak intensities and m/z values) into memory."
- [other] Initialize the trained Convolutional Neural Network (CNN) model from the ChemEmbed repository: "Initialize the trained Convolutional Neural Network (CNN) model from the ChemEmbed repository."
- [other] Pass each spectrum through the CNN to extract multidimensional molecular embedding vectors: "Pass each spectrum through the CNN to extract multidimensional molecular embedding vectors."
- [other] Aggregate embeddings into a feature matrix with one row per spectrum and embedding dimension as columns: "Aggregate embeddings into a feature matrix with one row per spectrum and embedding dimension as columns."
- [intro] framework is designed to process mass spectrometry data, perform predictions using a trained Convolutional Neural Network (CNN) model: "framework is designed to process mass spectrometry data, perform predictions using a trained Convolutional Neural Network (CNN) model"
- [readme] Model Prediction: Utilizes a pre-trained CNN model to predict molecular embeddings from spectra data: "Model Prediction: Utilizes a pre-trained CNN model to predict molecular embeddings from spectra data."
