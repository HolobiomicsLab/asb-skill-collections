---
name: overfitting-detection-and-prevention
description: Use when when training a fresh CNN model from scratch on labeled LCMS data (e.g., MS1 peak classification in NeatMS), particularly when aiming for a specific performance target (e.g., AUC ROC > 0.9) and you need to avoid wasting compute time on redundant epochs or degrading validation performance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
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
  techniques:
  - LC-MS
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

# overfitting-detection-and-prevention

## Summary

Monitor training and validation accuracy curves during neural network model training to detect overfitting and determine when to halt training. This skill ensures that a CNN model generalizes well to unseen data by comparing training performance against validation performance throughout the training process.

## When to use

When training a fresh CNN model from scratch on labeled LCMS data (e.g., MS1 peak classification in NeatMS), particularly when aiming for a specific performance target (e.g., AUC ROC > 0.9) and you need to avoid wasting compute time on redundant epochs or degrading validation performance.

## When NOT to use

- Input already consists of a pre-trained model with a fixed architecture and locked weights (e.g., transfer learning from an existing NeatMS model); in that case, focus on monitoring validation performance for task-specific overfitting rather than stopping training outright.
- Dataset is very small (<500 labeled peaks per class); overfitting will be inevitable; instead prioritize regularization (e.g., normalise_class=True, data augmentation) before monitoring.
- Validation split is not clearly defined or validation batches are contaminated with training data; any comparison of training vs. validation accuracy will be meaningless.

## Inputs

- Keras/TensorFlow model (freshly initialized or partially trained)
- Training batches (80% of labeled peak examples, normalized or unnormalized)
- Validation batches (10% of labeled peak examples, separate from training)
- Epoch count (integer; typically 1000 as default)

## Outputs

- Keras/TensorFlow training logs (accuracy metrics per epoch)
- Decision to halt training (boolean; True if overfitting detected)
- Final trained model state (saved at best validation checkpoint or manually halted point)

## How to apply

After initializing a CNN model with create_model(lr=0.00001, optimizer='Adam') and calling train_model(1000) with an initial epoch count, monitor the Keras/TensorFlow training logs to inspect both training and validation accuracy curves side-by-side. If no plateau is observed after the initial epoch block, resume training by calling train_model() again with additional epochs, but halt immediately if training accuracy approaches ~100% while validation accuracy lags significantly behind (a divergence indicating overfitting). The rationale is that when the model memorizes training data (high training accuracy) but fails to generalize (stalled or declining validation accuracy), further training will only degrade its utility on held-out test data.

## Related tools

- **NeatMS** (Provides create_model(), train_model(), and batch creation methods; logs training/validation accuracy metrics from Keras/TensorFlow backend) — https://github.com/bihealth/NeatMS
- **TensorFlow** (Underlying framework that generates and returns training/validation accuracy logs during model.fit() / train_model() calls)
- **Keras** (High-level API for model definition and training; produces accuracy curves and callbacks for monitoring)
- **Jupyter Notebook** (Interactive environment for real-time visualization and inspection of training/validation accuracy curves)

## Examples

```
# Train model with incremental monitoring
model = neatms_handler.create_model(lr=0.00001, optimizer='Adam')
logs = neatms_handler.train_model(1000)
# Inspect logs; if no plateau, resume training
logs_resumed = neatms_handler.train_model(500)  # Additional epochs
# Compare training_acc vs validation_acc; halt if divergence detected
```

## Evaluation signals

- Training and validation accuracy curves are plotted and visually inspected; they should remain closely aligned throughout training (e.g., within 5–10% of each other).
- No significant gap emerges between training accuracy (~100%) and validation accuracy (e.g., <80%); if such a gap appears, training must be halted immediately.
- Validation accuracy reaches a plateau or begins to decline in later epochs; training should stop at or before the epoch of best validation performance.
- Final model checkpoint (saved at best validation epoch) achieves the target AUC ROC score (e.g., >0.9) when evaluated on a held-out test set (10% of data).
- Training logs show smooth, monotonic improvement in both training and validation metrics without sudden spikes or collapse in validation performance.

## Limitations

- NeatMS does not currently provide automatic callback functions (e.g., EarlyStopping) to halt training; practitioners must manually monitor logs and call train_model() incrementally or externally implement stopping criteria.
- Overfitting detection relies on visual or manual comparison of training vs. validation accuracy; no built-in threshold or automated decision rule is provided.
- If validation_split is set too small (e.g., <10%), validation accuracy estimates may be noisy, making overfitting detection unreliable.
- The default learning rate (lr=0.00001) and optimizer choice (Adam) are fixed in create_model(); poorly tuned hyperparameters may lead to slow convergence or unstable training curves that complicate overfitting assessment.
- Class imbalance (when normalise_class=False) can bias training accuracy upward and mask overfitting in the minority class.

## Evidence

- [other] Inspect training and validation accuracy curves to confirm no overfitting (training accuracy ≈ validation accuracy); if training reaches ~100% while validation lags significantly, halt training.: "Inspect training and validation accuracy curves to confirm no overfitting (training accuracy ≈ validation accuracy); if training reaches ~100% while validation lags significantly, halt training."
- [other] Monitor training and validation accuracy on the returned Keras/TensorFlow logs; if no plateau is observed, resume training by calling train_model() again with additional epochs.: "Monitor training and validation accuracy on the returned Keras/TensorFlow logs; if no plateau is observed, resume training by calling train_model() again with additional epochs."
- [methods] NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training: "NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training"
- [methods] When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class).: "When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class)."
