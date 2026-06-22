---
name: hyperparameter-tuning-learning-rate-optimizer-selection
description: Use when when training a fresh NeatMS CNN model from scratch on LCMS peak classification and you need to determine which optimizer (Adam vs. SGD) and learning rate will produce an AUC ROC > 0.9 without overfitting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02220
  all_source_dois:
  - 10.1021/acs.analchem.1c02220
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hyperparameter-tuning-learning-rate-optimizer-selection

## Summary

Systematic selection and tuning of neural network learning rate and optimizer (Adam, SGD) for CNN-based LCMS peak classification. This skill optimizes model convergence speed and generalization to achieve target performance (AUC ROC > 0.9) without overfitting.

## When to use

When training a fresh NeatMS CNN model from scratch on LCMS peak classification and you need to determine which optimizer (Adam vs. SGD) and learning rate will produce an AUC ROC > 0.9 without overfitting. Apply this skill before committing to a full training run (1000+ epochs) to avoid wasted computation on poor hyperparameter choices.

## When NOT to use

- If using transfer learning on a pre-trained NeatMS model rather than training from scratch—fine-tuning typically requires fewer hyperparameter variations and smaller learning rates.
- If the labeled dataset contains fewer than ~500 peaks per class—NeatMS recommends at least 500 peaks per class for full model training; insufficient data makes hyperparameter tuning unreliable.
- If you have already identified and validated optimal hyperparameters in a prior study on similar LCMS data—reusing published values avoids redundant tuning.

## Inputs

- mzML raw mass spectrometry files
- feature table (CSV format from mzMine or XCMS)
- labeled training/validation/test batches (output from NeatMS create_batches method)
- candidate hyperparameter grid (learning_rate values, optimizer choices)

## Outputs

- trained CNN model with optimized learning_rate and optimizer parameters
- Keras/TensorFlow training and validation accuracy logs
- ROC curve data (False Positive Rate vs. True Positive Rate)
- AUC ROC score
- recommendation of best-performing hyperparameter set

## How to apply

Create a Neural Network Handler and generate training/validation/test batches (80:10:10 split, validation_split=0.1, normalise_class=False) from your labeled peak dataset. Initialize multiple CNN models with candidate hyperparameters: test learning rates in the range 0.00001 to 0.0001 with both Adam and SGD optimizers via create_model(lr=<candidate_lr>, optimizer=<'Adam'|'SGD'>). Train each configuration for an initial 1000 epochs using train_model(1000), monitoring Keras/TensorFlow logs for training and validation accuracy curves. Select the configuration where validation accuracy tracks closely with training accuracy (no plateau or divergence), indicating no overfitting. Once a promising set is identified, resume training with additional epochs by calling train_model() again. Compute ROC curve and AUC using get_true_vs_false_positive_df() with scikit-learn's auc() function; halt training if training accuracy reaches ~100% while validation lags significantly, or if AUC ROC achieves >0.9.

## Related tools

- **NeatMS** (Core framework providing create_model(), train_model(), create_batches(), and get_true_vs_false_positive_df() methods for CNN training, batch generation, and ROC computation) — https://github.com/bihealth/NeatMS
- **TensorFlow/Keras** (Neural network backend for model creation, training, and logging of accuracy curves)
- **scikit-learn** (Computation of ROC curve and AUC score from predicted and true labels)
- **Python** (Programming language for orchestrating hyperparameter sweeps and model training)
- **Jupyter Notebook** (Interactive environment for monitoring training curves and comparing hyperparameter configurations)

## Examples

```
from neatms import NeatMS, NeuralNetworkHandler
handler = NeuralNetworkHandler()
handler.create_batches(validation_split=0.1, normalise_class=False)
model = handler.create_model(lr=0.00001, optimizer='Adam')
model.train_model(1000)
df = handler.get_true_vs_false_positive_df()
from sklearn.metrics import auc
auc_score = auc(df['fpr'], df['tpr'])
```

## Evaluation signals

- Validation accuracy tracks closely with training accuracy across epochs (gap < ~5–10%), indicating no overfitting.
- Training does not reach ~100% accuracy while validation plateaus significantly below—a sign of overfitting and poor hyperparameter choice.
- Achieved AUC ROC score on held-out test set exceeds 0.9, meeting the target performance threshold.
- Learning curves show monotonic improvement or gradual plateau rather than oscillation or divergence, indicating stable convergence.
- Comparison of multiple optimizer/learning-rate pairs reveals a clear best configuration with higher AUC and better generalization than alternatives.

## Limitations

- NeatMS does not currently provide automatic early stopping callback functions; you must manually monitor logs and call train_model() to resume or halt training.
- Hyperparameter tuning requires a labeled training dataset with a minimum of ~500 peaks per class; smaller or imbalanced datasets will yield unreliable results.
- The recommended learning rate range (0.00001 to 0.0001) was empirically determined for the NeatMS CNN architecture and may not transfer to substantially different network designs.
- Tuning is performed on a specific representative subset of LCMS data; hyperparameters optimized on one dataset may require re-tuning for significantly different sample types or acquisition protocols.

## Evidence

- [other] Initialize a fresh CNN model using create_model(lr=0.00001, optimizer='Adam') with default hyperparameters and train via train_model(1000): "Initialize a fresh CNN model using create_model(lr=0.00001, optimizer='Adam') with default hyperparameters and train via train_model(1000) for an initial epoch count."
- [other] Monitor training and validation accuracy on the returned Keras/TensorFlow logs; if no plateau is observed, resume training by calling train_model() again: "Monitor training and validation accuracy on the returned Keras/TensorFlow logs; if no plateau is observed, resume training by calling train_model() again with additional epochs."
- [other] Inspect training and validation accuracy curves to confirm no overfitting (training accuracy ≈ validation accuracy); if training reaches ~100% while validation lags significantly, halt training.: "Inspect training and validation accuracy curves to confirm no overfitting (training accuracy ≈ validation accuracy); if training reaches ~100% while validation lags significantly, halt training."
- [methods] When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class).: "When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class)."
- [methods] from keras.optimizers import SGD, Adam: "from keras.optimizers import SGD, Adam"
- [readme] NeatMS relies on neural network based classification: "NeatMS relies on neural network based classification."
