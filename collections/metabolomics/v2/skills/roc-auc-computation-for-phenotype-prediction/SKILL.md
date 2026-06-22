---
name: roc-auc-computation-for-phenotype-prediction
description: Use when you have constructed consensus-clustered microbe and metabolite modules from microbiome-metabolome interaction data and wish to test whether these module-level features have clinically predictive value for a binary phenotype (e.g., disease vs. healthy).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3809
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3518
  - http://edamontology.org/topic_2885
  tools:
  - Elastic Net
  - MiMeNet
  - TensorFlow or PyTorch
  - scikit-learn
  - Seaborn
  - Python
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- we benchmarked MiMeNet against other general regression models, i.e., Random Forest (RF), multivariate Elastic Net, and canonical correlation analysis (CCA) models
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome abundance features (green) are used to train a neural network to predict metabolite abundance features (blue).
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- MelonnPan and NED models were obtained from their respective GitHub repositories and executed using default parameters as according to their tutorials. Random Forest, multivariate Elastic Net, and
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet_cq
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet_cq
schema_version: 0.2.0
---

# ROC-AUC computation for phenotype prediction

## Summary

Trains binary neural network classifiers on derived microbe-metabolite module features to predict disease phenotype (IBD status), evaluating discriminative performance using area-under-ROC-curve (AUC) as the primary metric across multiple random iterations to assess robustness.

## When to use

You have constructed consensus-clustered microbe and metabolite modules from microbiome-metabolome interaction data and wish to test whether these module-level features have clinically predictive value for a binary phenotype (e.g., disease vs. healthy). Use this skill when you want to move from exploratory network discovery to quantitative phenotype prediction and need a robust, iteration-based AUC estimate to compare prediction performance across different input transformations or model architectures.

## When NOT to use

- Input phenotype is continuous (not binary); use regression metrics (e.g., Pearson correlation, RMSE) instead of ROC-AUC.
- Module features have not yet been constructed or validated; apply this skill only after consensus clustering has produced stable, interpretable microbe-metabolite modules.
- Sample size is very small (<30 total) or class imbalance is extreme (>95:5); ROC-AUC may be misleading; consider stratified resampling or alternative metrics.

## Inputs

- Module feature matrix (samples × module features, normalized feature values)
- Binary phenotype labels (samples × 1, class assignment per sample)
- Optionally, two parallel input transformations (e.g., CLR and relative abundance module features)

## Outputs

- AUC scores from 100 iterations (distribution of performance metrics)
- Mean and variance of AUC across iterations per condition
- Comparison table of AUC between input transformations or model variants

## How to apply

Train a 3-layer binary neural network classifier (32 nodes per layer) on module feature values (derived from consensus-clustered microbes and metabolites) to predict binary phenotype labels (e.g., IBD vs. control). Perform 100 independent training runs with random initialization to generate a distribution of AUC scores rather than a single point estimate. Compute area-under-ROC-curve (AUC) for each run on a held-out test set (the IBD PRISM cohort or equivalent), recording the mean and variance across all 100 iterations. This iteration-based evaluation guards against initialization sensitivity and allows fair comparison: compute AUC separately for each input transformation (e.g., CLR vs. relative abundance) or model variant and document the magnitude of improvement.

## Related tools

- **TensorFlow or PyTorch** (Neural network framework for training 3-layer binary classifier on module features)
- **scikit-learn** (Provides ROC curve computation and AUC metric calculation from predicted probabilities and true labels)

## Examples

```
python -c "from sklearn.metrics import roc_auc_score; import numpy as np; auc_scores = [roc_auc_score(y_test, y_pred_proba[:, 1]) for _ in range(100)]; print(f'Mean AUC: {np.mean(auc_scores):.3f} ± {np.std(auc_scores):.3f}')"
```

## Evaluation signals

- AUC values range between 0.5 (random chance) and 1.0 (perfect discrimination); mean AUC should be meaningfully above 0.5 if modules capture phenotype signal.
- Variance across 100 iterations should be low (tight distribution) to indicate robust, reproducible prediction; high variance suggests unstable features or insufficient training data.
- AUC improvement magnitude (e.g., CLR vs. relative abundance) should be documented; if improvement is <5% absolute, practical significance is questionable.
- Mean AUC should be consistent on external validation cohort if one is provided (e.g., IBD external cohort); large drop in AUC on external data indicates overfitting.
- Receiver-operating-characteristic curve should show clear separation from the diagonal (no-discrimination line); visual inspection of ROC plots across iterations confirms consistency.

## Limitations

- AUC does not account for class imbalance; if phenotype prevalence is skewed, consider computing precision-recall AUC or sensitivity/specificity trade-off metrics alongside ROC-AUC.
- Module features must be properly normalized and stable; if consensus clustering produces few or highly correlated modules, AUC may be inflated or uninformative.
- Single-iteration AUC estimates (without the 100-iteration framework) can be sensitive to random weight initialization; the paper's 100-iteration protocol is necessary for robustness.
- AUC reflects discriminative capacity but does not guarantee biological interpretability of individual module associations; modules should be validated for functional coherence independently of AUC.
- External validation on completely independent cohorts was not performed in all datasets; generalization to new populations is not guaranteed.

## Evidence

- [methods] Train binary neural network classifiers (3-layer, 32 nodes per layer) on CLR and RA module feature values to predict IBD status; evaluate on IBD (PRISM) using 100 iterations with area-under-ROC-curve (AUC) metric.: "Train binary neural network classifiers (3-layer, 32 nodes per layer) on CLR and RA module feature values to predict IBD status; evaluate on IBD (PRISM) using 100 iterations with area-under-ROC-curve"
- [methods] Compare counts of well-predicted metabolites and AUC scores between CLR and RA, documenting the magnitude of improvement for CLR.: "Compare counts of well-predicted metabolites and AUC scores between CLR and RA, documenting the magnitude of improvement for CLR."
- [results] MiMeNet then trains multiple network models using 10-fold cross-validation: "MiMeNet then trains multiple network models using 10-fold cross-validation"
- [results] the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites"
- [results] constructs a module-based interaction network: "constructs a module-based interaction network"
