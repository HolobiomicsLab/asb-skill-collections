---
name: deep-learning-training-convergence-monitoring
description: Use when training a CNN model from scratch on LCMS peak classification
  tasks (or similar image-like batched data) where you need to confirm the model reaches
  target performance (e.g., AUC ROC > 0.9) without overfitting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
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
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create
  a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
- calling the training method (1000 by default). NeatMS does not currently provides
  callback functions to automatically stop the training. Calling the training method
  will simply resume the training
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-training-convergence-monitoring

## Summary

Monitor and diagnose convergence behavior of CNN models during training by comparing training and validation accuracy curves to detect overfitting and determine when to halt training. This skill is essential for validating that a model learns generalizable patterns rather than memorizing training data.

## When to use

Apply this skill when training a CNN model from scratch on LCMS peak classification tasks (or similar image-like batched data) where you need to confirm the model reaches target performance (e.g., AUC ROC > 0.9) without overfitting. Use it after initializing a model and beginning iterative training epochs, especially when the training regime lacks automatic early stopping callbacks.

## When NOT to use

- Input model already has automatic early stopping callbacks enabled; use the callback's built-in monitoring instead.
- Training dataset contains < 500 peaks per class; full model training from scratch is not recommended; use transfer learning instead.
- Validation split was set to 0 or no held-out validation set exists; convergence monitoring requires separate training and validation curves.

## Inputs

- Keras/TensorFlow model training logs (accuracy curves per epoch)
- Validation accuracy curve per epoch
- True positive and false positive rate vectors from get_true_vs_false_positive_df()

## Outputs

- Training vs. validation accuracy comparison (visual or tabular)
- ROC curve plot (FPR vs. TPR)
- AUC ROC score (scalar, target ≥ 0.9)
- Overfitting diagnosis (present/absent)
- Training halt decision (continue/stop)

## How to apply

After calling train_model() with an initial epoch count (e.g., 1000), inspect the returned Keras/TensorFlow training and validation accuracy logs. Plot or tabulate both curves side-by-side to identify convergence patterns: if training accuracy rises substantially while validation accuracy plateaus or diverges, overfitting is occurring and training should be halted immediately. If neither curve shows a plateau (both still improving), resume training by calling train_model() again with additional epochs. Compute the ROC curve and AUC metric using get_true_vs_false_positive_df() data and scikit-learn's auc() function on False Positive Rate vs. True Positive Rate. The skill is successfully applied when training accuracy ≈ validation accuracy and the final AUC ROC meets or exceeds the target threshold (e.g., 0.9), confirming no overfitting and adequate generalization.

## Related tools

- **NeatMS** (Provides train_model() method to resume training, get_true_vs_false_positive_df() to extract ROC curve data, and neural network handler to manage batches and model state) — https://github.com/bihealth/NeatMS
- **TensorFlow/Keras** (Underlying framework returning training and validation accuracy logs; enables resumable training via train_model() calls)
- **scikit-learn** (Computes ROC curve and AUC metric from true and false positive rates)
- **Jupyter Notebook** (Interactive environment for plotting and inspecting training curves in real-time)

## Examples

```
from sklearn.metrics import auc
import matplotlib.pyplot as plt
# After calling train_model(1000):
history = model.history
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.show()
df_roc = experiment.get_true_vs_false_positive_df()
auc_score = auc(df_roc['fpr'], df_roc['tpr'])
print(f'AUC ROC: {auc_score:.3f}')
if auc_score >= 0.9 and abs(history.history['accuracy'][-1] - history.history['val_accuracy'][-1]) < 0.1:
    print('Training successful, no overfitting detected')
```

## Evaluation signals

- Training accuracy and validation accuracy curves are visually similar throughout training (divergence < ~5–10%), confirming no overfitting.
- Final AUC ROC score ≥ 0.9, meeting or exceeding the published target threshold.
- Training curve shows monotonic or near-monotonic increase with no sharp plateau before validation curve plateaus, indicating effective learning.
- Halting condition is triggered when training accuracy reaches ~100% while validation accuracy lags significantly, preventing further model degradation.
- ROC curve passes through expected regions (diagonal baseline for random classifier; concave arc toward top-left for strong classifier).

## Limitations

- NeatMS does not currently provide automatic callback functions to halt training; manual inspection and stopping are required.
- Convergence monitoring assumes a representative training/validation split (0.1 validation split); biased or unrepresentative splits may yield misleading curves.
- Training and validation accuracy curves do not directly reveal class imbalance effects; use normalise_class=True during batch creation if class distributions differ significantly.
- Monitoring requires human judgment to interpret divergence; no formal statistical test for overfitting is embedded in the workflow.
- Model may achieve high AUC ROC but still suffer from local biases in specific sample cohorts not represented in the validation set.

## Evidence

- [other] Monitor training and validation accuracy on the returned Keras/TensorFlow logs; if no plateau is observed, resume training by calling train_model() again with additional epochs.: "Monitor training and validation accuracy on the returned Keras/TensorFlow logs; if no plateau is observed, resume training by calling train_model() again with additional epochs."
- [other] Inspect training and validation accuracy curves to confirm no overfitting (training accuracy ≈ validation accuracy); if training reaches ~100% while validation lags significantly, halt training.: "Inspect training and validation accuracy curves to confirm no overfitting (training accuracy ≈ validation accuracy); if training reaches ~100% while validation lags significantly, halt training."
- [other] Compute ROC curve and AUC using get_true_vs_false_positive_df() data with scikit-learn's auc() function on False Positive Rate vs. True Positive Rate.: "Compute ROC curve and AUC using get_true_vs_false_positive_df() data with scikit-learn's auc() function on False Positive Rate vs. True Positive Rate."
- [methods] NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training: "NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training"
- [other] Does training the NeatMS CNN model from scratch on the provided example dataset under full training conditions produce an AUC ROC score exceeding 0.9 without evidence of overfitting?: "Does training the NeatMS CNN model from scratch on the provided example dataset under full training conditions produce an AUC ROC score exceeding 0.9 without evidence of overfitting?"
