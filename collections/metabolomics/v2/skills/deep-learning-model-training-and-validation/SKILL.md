---
name: deep-learning-model-training-and-validation
description: Use when you have paired mass-spectrometry spectral data (m/z and intensity arrays) with known molecular fingerprints or InChIKeys, and need to train a supervised deep learning model to predict fingerprints for novel spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - TensorFlow
  - PyTorch
  - scikit-learn
  - PyFingerprint
derived_from:
- doi: 10.1007/s11306-020-01726-7
  title: MetFID
evidence_spans:
- No usage/docs found.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metfid_cq
    doi: 10.1007/s11306-020-01726-7
    title: MetFID
  dedup_kept_from: coll_metfid_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01726-7
  all_source_dois:
  - 10.1007/s11306-020-01726-7
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-model-training-and-validation

## Summary

Train and validate a CNN-based model on labeled mass-spectrometry data to predict compound fingerprints, using appropriate loss functions and monitoring validation performance to prevent overfitting. This skill is essential for building metabolite annotation predictors that map spectral features to molecular fingerprint vectors.

## When to use

You have paired mass-spectrometry spectral data (m/z and intensity arrays) with known molecular fingerprints or InChIKeys, and need to train a supervised deep learning model to predict fingerprints for novel spectra. The trigger is: labeled MS training data is available, a CNN architecture has been designed or selected, and you need to optimize model weights and evaluate generalization performance on held-out test data.

## When NOT to use

- Your MS data is unlabeled or lacks known molecular fingerprints—use unsupervised or transfer-learning approaches instead.
- You have only a small number of spectra (<100)—insufficient to train a deep CNN without severe overfitting; consider simpler models or data augmentation first.
- Your input spectra are already preprocessed into a fixed-size feature vector unrelated to m/z–intensity pairs—the CNN's convolutional assumptions may not apply.

## Inputs

- mass-spectrometry spectral data (m/z and intensity arrays or matrices)
- molecular fingerprint labels or InChIKeys for each spectrum
- training/validation/test split indices or ratios
- CNN architecture specification (layer sizes, activation functions)
- loss function parameters (e.g., class weights, Tanimoto weighting)

## Outputs

- trained CNN model weights (.h5 or checkpoint format)
- model architecture specification (JSON or PyTorch state_dict)
- validation performance metrics (loss curve, accuracy by epoch)
- test set predictions with Tanimoto similarity scores
- hyperparameter log (learning rate, batch size, epochs, optimizer state)

## How to apply

Construct training and validation splits from your labeled MS dataset, ensuring spectra are formatted as matrices or m/z–intensity array pairs compatible with the CNN input layer. Train the CNN using a loss function suited to fingerprint prediction—binary cross-entropy for individual fingerprint bits or Tanimoto-based loss for holistic similarity—with an optimizer such as Adam. Monitor validation loss and accuracy at each epoch to detect overfitting; apply early stopping or learning-rate decay if validation performance plateaus. After training converges, evaluate the final model on a held-out test set and report Tanimoto similarity scores or fingerprint bit-level accuracy. Save trained model weights (e.g., as .h5 format) and log hyperparameters for reproducibility.

## Related tools

- **TensorFlow** (Deep learning framework for building, training, and saving CNN models) — https://www.tensorflow.org/
- **PyTorch** (Alternative deep learning framework for CNN model development and training)
- **scikit-learn** (For train–test split, cross-validation, and evaluation metrics computation)
- **PyFingerprint** (Fingerprint generation and Tanimoto similarity scoring for labels and evaluation) — https://github.com/hcji/PyFingerprint

## Examples

```
python3 main.py
```

## Evaluation signals

- Validation loss decreases monotonically over initial epochs, then stabilizes; test loss remains close to validation loss (no overfitting indicator).
- Tanimoto similarity scores on test spectra fall within the range [0, 1] and match expected metabolite annotation performance (e.g., top candidate scores ≥ 0.5 for known compounds).
- Fingerprint bit-level predictions achieve ≥80% accuracy on held-out test set (or task-specific threshold); per-bit precision and recall are logged.
- Model weights are reproducible when re-trained with identical random seed and hyperparameters; output model file (.h5 or checkpoint) is valid and loadable.
- Input spectra ordering does not affect model learning or test performance (invariant to permutation of training batches).

## Limitations

- CNN performance depends critically on input data quality and preprocessing (normalization, m/z binning); poor spectral alignment or intensity scaling will degrade predictions.
- The choice of loss function (binary cross-entropy vs. Tanimoto) affects learned fingerprints; Tanimoto loss is more chemically interpretable but may be slower to converge.
- Small or imbalanced training sets (over-representation of certain compound classes) can lead to poor generalization; class weighting or stratified splits are required.
- The trained model is specific to the MS instrument, ionization mode, and fragmentation protocol used in training; transfer to new instruments or modes may require retraining or fine-tuning.

## Evidence

- [other] Prepare training and validation splits from labeled MS data with known molecular fingerprints.: "Prepare training and validation splits from labeled MS data with known molecular fingerprints."
- [other] Train the CNN model using a suitable loss function (e.g., binary cross-entropy for fingerprint bits or Tanimoto-based loss) and optimizer, monitoring validation performance.: "Train the CNN model using a suitable loss function (e.g., binary cross-entropy for fingerprint bits or Tanimoto-based loss) and optimizer, monitoring validation performance."
- [other] Evaluate model predictions on a held-out test set and save trained model weights and architecture.: "Evaluate model predictions on a held-out test set and save trained model weights and architecture."
- [readme] The second column represents the `Tanimoto similarity score`. Each table will be ranked in a descending order by score.: "The second column represents the `Tanimoto similarity score`. Each table will be ranked in a descending order by score."
- [readme] Before running the program, you need to have the [PyFingerprint][7], [PubChemPy 1.0.4][1], [Open Babel 3.1.1][2], [tabulate 0.8.9][3] and [Tensorflow][4] installed.: "Before running the program, you need to have the [PyFingerprint][7], [PubChemPy 1.0.4][1], [Open Babel 3.1.1][2], [tabulate 0.8.9][3] and [Tensorflow][4] installed."
