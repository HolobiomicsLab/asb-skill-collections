---
name: mass-spectrometry-peak-classification
description: Use when you have raw mzML files and feature tables (CSV format from mzMine or XCMS) from untargeted LCMS experiments and need to distinguish true metabolite peaks from false positives introduced by the peak-picking algorithm.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - NeatMS
  - Python
  - TensorFlow
  - Keras
  - scikit-learn
  - pandas
  - NumPy
  - Jupyter Notebook
  - TensorFlow/Keras
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
- calling the training method (1000 by default). NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training
- from keras.optimizers import SGD, Adam
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neatms
    doi: 10.1021/acs.analchem.1c02220
    title: neatms
  dedup_kept_from: coll_neatms
schema_version: 0.2.0
---

# mass-spectrometry-peak-classification

## Summary

Automated classification of MS1 peaks as true or false positives using neural network models trained on labelled LCMS data. This skill enables filtering of spurious detections reported by standard peak-picking pipelines (mzMine, XCMS) to improve signal quality in untargeted metabolomics.

## When to use

You have raw mzML files and feature tables (CSV format from mzMine or XCMS) from untargeted LCMS experiments and need to distinguish true metabolite peaks from false positives introduced by the peak-picking algorithm. You have either (a) ≥500 labelled peaks per class for full model training, or (b) a few hundred manually annotated peaks and an existing pre-trained model for transfer learning.

## When NOT to use

- Input is already a curated, manually validated feature table with high confidence peaks.
- You have fewer than 500 labelled peaks per class and no pre-trained model available for transfer learning.
- You are working with targeted LCMS or data from non-standard peak-picking tools where NeatMS training data does not apply.

## Inputs

- raw mzML files (mass spectrometry data)
- feature table (CSV format from mzMine or XCMS peak detector)
- labelled peak annotations (for training: ≥500 peaks per class; for transfer learning: few hundred peaks)
- pre-trained neural network model (optional, .h5 format for transfer learning)

## Outputs

- trained CNN model (.h5 format)
- probability predictions per peak (0.0–1.0)
- ROC curve and AUC score (≥0.9 target)
- threshold-dependent True Positive Rate, False Positive Rate, and false positive subclass breakdown (Low_quality, Noise) at user-specified thresholds
- filtered peak list with classification labels (High_quality, Low_quality, Noise)

## How to apply

Load raw mzML files and feature table into a NeatMS Experiment object specifying the input type (mzmine or xcms). Create a Neural Network Handler with default parameters (matrice_size=120, margin=1, min_scan_num=5) and call create_batches(validation_split=0.1, normalise_class=False) to generate 80:10:10 training/test/validation splits. For full training, initialize a fresh CNN with create_model(lr=0.00001, optimizer='Adam') and train via train_model(1000); monitor training/validation accuracy curves to detect overfitting (training accuracy ≈ validation accuracy). Alternatively, for transfer learning, load a pre-trained .h5 model and fine-tune on your labelled subset. Extract probability predictions for each peak, compute ROC and AUC using scikit-learn on the True Positive Rate vs. False Positive Rate, and inspect threshold-dependent metrics (e.g., TPR and FPR at threshold 0.01) to validate model performance.

## Related tools

- **NeatMS** (Core framework providing Experiment, Neural Network Handler, batch creation, model training, and threshold-based peak classification) — https://github.com/bihealth/NeatMS
- **TensorFlow/Keras** (Neural network model definition, training, and inference backend)
- **scikit-learn** (ROC curve and AUC computation from true/false positive rates)
- **pandas** (Feature table loading and threshold-dependent metric extraction)
- **NumPy** (Numerical operations on peak matrices and batch generation)
- **Jupyter Notebook** (Interactive development and visualization of training curves and ROC plots)

## Examples

```
from neatms import Experiment, NeuralNetworkHandler
from sklearn.metrics import auc, roc_curve

exp = Experiment(input_type='mzmine', raw_path='./data/', feature_table_path='./features.csv')
nn_handler = NeuralNetworkHandler(matrice_size=120, margin=1, min_scan_num=5)
nn_handler.create_batches(validation_split=0.1, normalise_class=False)
nn_handler.create_model(lr=0.00001, optimizer='Adam')
nn_handler.train_model(epochs=1000)
df_probs = nn_handler.get_true_vs_false_positive_df(label='High_quality')
roc_auc = auc(df_probs['FPR'], df_probs['TPR'])
print(f'AUC ROC: {roc_auc:.3f}')
```

## Evaluation signals

- AUC ROC score on held-out test set ≥ 0.9, indicating strong discriminative power between true and false positives.
- Training accuracy ≈ validation accuracy with no large divergence, confirming absence of overfitting.
- At threshold 0.01: True Positive Rate = 1.0 (100% retention of high-quality peaks) and False Positive Rate ≈ 0.44 (44% of false positives removed).
- Consistency between probability distribution of labelled peaks and expected class ratios (High_quality, Low_quality, Noise).
- Reproducibility: same raw mzML + feature table + model produces identical probability predictions and threshold metrics across runs.

## Limitations

- NeatMS does not provide automatic early stopping callbacks; practitioners must manually inspect training curves and call train_model() iteratively to avoid overfitting.
- Full model training requires ≥500 labelled peaks per class, which is labour-intensive; transfer learning is recommended for smaller datasets but requires a relevant pre-trained model.
- Model performance depends on the representativeness of the training dataset; if the LCMS instrument, ionization mode, or metabolite class distribution differs significantly from training data, retraining may be necessary.
- The default matrice_size (120) and margin (1) parameters may require tuning for non-standard m/z ranges or peak widths; no automated hyperparameter optimization is provided in the core package.

## Evidence

- [readme] NeatMS enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: "**NeatMS** enables automated filtering of false positive MS<sup>1</sup> peaks reported by commonly used LCMS data processing pipelines."
- [methods] NeatMS relies on neural network based classification to distinguish true from false positive peaks.: "NeatMS relies on neural network based classification to distinguish true from false positive peaks in untargeted LCMS data."
- [methods] Load data via Experiment object with mzmine or xcms format specification.: "In order to create an experiment object, we need to set 3 parameters: The path to the raw data folder, The path to the feature table (.csv) or the feature tables folder, The peak detection"
- [other] Create batches with validation split 0.1 and default neural network parameters.: "Create a Neural Network Handler with default parameters (matrice_size=120, margin=1, min_scan_num=5) and call create_batches(validation_split=0.1, normalise_class=False) to generate training, test,"
- [other] Monitor training/validation accuracy to confirm no overfitting before using the model for prediction.: "Inspect training and validation accuracy curves to confirm no overfitting (training accuracy ≈ validation accuracy); if training reaches ~100% while validation lags significantly, halt training."
- [other] Extract threshold-dependent TPR/FPR metrics from trained model predictions.: "Call nn_handler.get_true_vs_false_positive_df(label='High_quality') to compute the threshold-dependent recall table across probability thresholds from 0.00 to 0.99."
- [methods] Minimum training set size for full model training.: "When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class)."
- [methods] No automatic training termination; manual inspection required.: "NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training"
