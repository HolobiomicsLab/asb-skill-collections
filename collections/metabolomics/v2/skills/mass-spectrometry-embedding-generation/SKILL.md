---
name: mass-spectrometry-embedding-generation
description: Use when when you have preprocessed MS/MS spectral data (normalized peak intensities and m/z values) and need to convert individual spectra into fixed-dimensional vector representations for similarity-based metabolite matching or comparative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Convolutional Neural Network (CNN)
  - PyTorch
  - ChemEmbed
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

# mass-spectrometry-embedding-generation

## Summary

Extract multidimensional molecular embedding vectors from preprocessed MS/MS spectra using a trained Convolutional Neural Network (CNN) model. These embeddings serve as feature representations for downstream metabolite identification and candidate matching against reference databases.

## When to use

When you have preprocessed MS/MS spectral data (normalized peak intensities and m/z values) and need to convert individual spectra into fixed-dimensional vector representations for similarity-based metabolite matching or comparative analysis. Specifically useful when working with MS/MS data formatted as MSP files (with or without SMILES annotations) within the ChemEmbed pipeline.

## When NOT to use

- Input spectra are already in the form of pre-computed embedding vectors or feature tables; re-embedding will introduce redundant transformation.
- The CNN model has not been trained or validated on the chemical space or ionization mode (positive/negative) of your input spectra; model mismatch will produce unreliable embeddings.
- MS/MS data is not preprocessed (raw, unnormalized peak intensities); the CNN expects normalized spectral intensities and will produce poor-quality embeddings on raw input.

## Inputs

- Preprocessed MS/MS spectral data (DataFrame or array with normalized peak intensities and m/z values)
- Trained CNN model file (PyTorch or compatible format)
- MSP file (with or without SMILES annotations)
- Configuration file (config.yaml) containing model_path, input file paths, and parameters

## Outputs

- Molecular embedding vectors (multidimensional arrays, one per spectrum)
- Aggregated feature matrix (CSV or NumPy format with shape: num_spectra × embedding_dimension)
- Saved embeddings file path for downstream candidate matching

## How to apply

Load preprocessed MS/MS spectral data containing normalized peak intensities and m/z values into memory. Initialize the trained CNN model from the ChemEmbed repository using the model_path parameter specified in config.yaml. Pass each spectrum sequentially through the CNN to extract multidimensional molecular embedding vectors (one embedding vector per input spectrum). Aggregate all extracted embeddings into a feature matrix with one row per spectrum and embedding dimensions as columns. Save the resulting embedding matrix to an output file in CSV or NumPy format. The CNN processes spectral peak data as input and produces dense vector representations suitable for cosine similarity matching against a reference database of known metabolites.

## Related tools

- **Convolutional Neural Network (CNN)** (Trained deep learning model that processes spectral peak data and outputs multidimensional embedding vectors for each spectrum) — https://github.com/massspecdl/ChemEmbed
- **PyTorch** (Deep learning framework used for CNN model loading and inference during embedding generation)
- **ChemEmbed** (End-to-end framework orchestrating data preprocessing, CNN-based embedding generation, and candidate matching) — https://github.com/massspecdl/ChemEmbed

## Examples

```
python main.py --config config.yaml
```

## Evaluation signals

- Embedding matrix dimensions match expected shape: num_spectra rows × model embedding_dimension columns (e.g., 100 spectra × 256 dimensions).
- No NaN or Inf values in output embeddings; all values are finite floating-point numbers within a reasonable range (e.g., -10 to +10).
- Spectra from the same or similar compounds produce embeddings with high cosine similarity (>0.7); spectra from unrelated compounds produce low similarity (<0.3).
- Output file (CSV or NumPy) is successfully saved and can be loaded back without corruption; file size is proportional to num_spectra × embedding_dimension.
- Downstream candidate matching step (cosine similarity comparison against reference database) produces top-N candidates with interpretable rankings and non-trivial similarity scores.

## Limitations

- CNN model performance is constrained by the chemical diversity and MS/MS data distribution used during training; spectra from chemically distinct domains or acquired under different ionization conditions may produce poor embeddings.
- MSP files without SMILES annotations are processed without structural information; embeddings rely solely on spectral peak patterns and may be less discriminative for isomeric or isobaric compounds.
- Embedding dimensionality and quality are fixed by the pre-trained model architecture; users cannot adjust embedding dimension or fine-tune the CNN without access to training code and data.
- No explicit mechanism to handle missing peaks, very low-intensity noise, or spectra with fewer peaks than the model expects; preprocessing must ensure all spectra meet minimum quality thresholds.

## Evidence

- [other] Load preprocessed MS/MS spectral data (normalized peak intensities and m/z values) into memory. Initialize the trained Convolutional Neural Network (CNN) model from the ChemEmbed repository. Pass each spectrum through the CNN to extract multidimensional molecular embedding vectors.: "Load preprocessed MS/MS spectral data (normalized peak intensities and m/z values) into memory. 2. Initialize the trained Convolutional Neural Network (CNN) model from the ChemEmbed repository. 3."
- [other] Aggregate embeddings into a feature matrix with one row per spectrum and embedding dimension as columns. Save embeddings to output file in CSV or NumPy format.: "Aggregate embeddings into a feature matrix with one row per spectrum and embedding dimension as columns. 5. Save embeddings to output file in CSV or NumPy format."
- [intro] The framework is designed to perform predictions using a trained Convolutional Neural Network (CNN) model that processes mass spectrometry data as input to the pipeline.: "The framework is designed to perform predictions using a trained Convolutional Neural Network (CNN) model that processes mass spectrometry data as input to the pipeline."
- [readme] Utilizes a pre-trained CNN model to predict molecular embeddings from spectra data.: "Utilizes a pre-trained CNN model to predict molecular embeddings from spectra data."
- [readme] Handles MSP files both with and without SMILES annotations, controlled via a configuration parameter.: "Handles MSP files both with and without SMILES annotations, controlled via a configuration parameter."
