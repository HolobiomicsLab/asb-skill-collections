---
name: cnn-inference-on-spectral-data
description: Use when you have preprocessed MS/MS spectral data (normalized peak intensities and m/z values) in memory or on disk, a trained CNN model checkpoint available, and you need to generate molecular embedding vectors for matching against a reference database of known metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - Convolutional Neural Network (CNN)
  - up_cnn_model.py
  - inference_dataset_loader.py
  - spectra_inference_dataset_loader.py
  - PyTorch
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CNN Inference on Spectral Data

## Summary

Load preprocessed MS/MS spectra and pass them through a trained Convolutional Neural Network to extract multidimensional molecular embedding vectors for each spectrum. This is a core inference step in metabolite identification pipelines that converts raw mass spectrometry measurements into structured feature representations for downstream candidate matching.

## When to use

You have preprocessed MS/MS spectral data (normalized peak intensities and m/z values) in memory or on disk, a trained CNN model checkpoint available, and you need to generate molecular embedding vectors for matching against a reference database of known metabolites. This step is required after data preprocessing and model training but before candidate matching and ranking.

## When NOT to use

- Input spectra are not yet preprocessed (still contain raw, unnormalized peak intensities or missing m/z calibration) — preprocess first using data_processing.py
- You do not have a trained CNN model available — train the model on labeled spectra data before attempting inference
- Your goal is to interpret or validate the learned features directly; CNN embeddings are designed for similarity matching, not human interpretability

## Inputs

- Preprocessed MS/MS spectral data (normalized peak intensities and m/z values)
- Trained CNN model checkpoint file (.pt or equivalent)
- MSP format spectra file (with or without SMILES annotations)
- Configuration file (config.yaml) specifying model_path, input file paths, and parameters

## Outputs

- Multidimensional molecular embedding vectors (one vector per spectrum)
- Embedding feature matrix (CSV or NumPy format)
- Aggregated embeddings ready for candidate matching

## How to apply

Initialize the trained CNN model from disk (e.g., via torch.load or the ChemEmbed cnn_train.up_cnn_model module). Create a data loader using the appropriate inference dataset class (inference_dataset_loader.py for MSP files with SMILES, or spectra_inference_dataset_loader.py for MSP files without SMILES) that batches normalized spectra. Iterate over batches, feeding each spectrum through the CNN in inference mode (model.eval()) to extract embedding vectors. Aggregate the embeddings into a feature matrix with one row per spectrum and embedding dimensions as columns. Save the resulting embeddings matrix to disk in CSV or NumPy format for subsequent cosine similarity matching against the reference database.

## Related tools

- **Convolutional Neural Network (CNN)** (Extracts multidimensional molecular embedding vectors from preprocessed MS/MS spectra during inference) — https://github.com/massspecdl/ChemEmbed
- **up_cnn_model.py** (Custom PyTorch module that defines the trained CNN architecture for spectra-to-embedding inference) — https://github.com/massspecdl/ChemEmbed
- **inference_dataset_loader.py** (Data loader for batching MSP spectra with SMILES annotations for CNN inference) — https://github.com/massspecdl/ChemEmbed
- **spectra_inference_dataset_loader.py** (Data loader for batching MSP spectra without SMILES annotations for CNN inference) — https://github.com/massspecdl/ChemEmbed
- **PyTorch** (Deep learning framework used to load, initialize, and run the trained CNN model in inference mode)

## Examples

```
python main.py --config config.yaml
```

## Evaluation signals

- Embeddings matrix has shape (number_of_spectra, embedding_dimension) with no NaN or infinite values
- All embedding vectors are non-zero and have consistent magnitude (e.g., L2 norm ≈ 1.0 if normalized)
- Cosine similarity scores between embeddings and reference database candidates fall within expected range [−1, 1], with top matches showing similarity > 0.5 for true positives
- Output file successfully saved and is readable; row count matches input spectrum count
- Inference runs without errors in model.eval() mode (gradients disabled, batch normalization frozen)

## Limitations

- CNN embeddings are specific to the training data distribution; performance degrades on spectra from different ionization modes, instruments, or chemical families not well-represented in training
- The method requires a pre-trained model; inference on out-of-distribution data without retraining will produce unreliable embeddings
- MSP files must have consistent formatting (consistent field names, num_peaks count, and peak data structure) or the data loader will fail or silently skip malformed entries
- No changelog or versioning documented; updates to the model or data loader code may break compatibility with embeddings generated by older model checkpoints

## Evidence

- [other] Load preprocessed MS/MS spectral data (normalized peak intensities and m/z values) into memory. Initialize the trained Convolutional Neural Network (CNN) model from the ChemEmbed repository.: "Load preprocessed MS/MS spectral data (normalized peak intensities and m/z values) into memory. 2. Initialize the trained Convolutional Neural Network (CNN) model from the ChemEmbed repository."
- [other] Pass each spectrum through the CNN to extract multidimensional molecular embedding vectors. Aggregate embeddings into a feature matrix with one row per spectrum and embedding dimension as columns. Save embeddings to output file in CSV or NumPy format.: "Pass each spectrum through the CNN to extract multidimensional molecular embedding vectors. 4. Aggregate embeddings into a feature matrix with one row per spectrum and embedding dimension as columns."
- [readme] Model Prediction: Utilizes a pre-trained CNN model to predict molecular embeddings from spectra data.: "Model Prediction: Utilizes a pre-trained CNN model to predict molecular embeddings from spectra data."
- [readme] Handles MSP files both with and without SMILES annotations, controlled via a configuration parameter.: "Supports for Multiple Input Types: Handles MSP files both with and without SMILES annotations, controlled via a configuration parameter."
- [readme] Ensure the cnn_train module is present in your project and contains up_cnn_model.py and spectra_inference_dataset_loader.py.: "Ensure the cnn_train module is present in your project and contains up_cnn_model.py and spectra_inference_dataset_loader.py."
