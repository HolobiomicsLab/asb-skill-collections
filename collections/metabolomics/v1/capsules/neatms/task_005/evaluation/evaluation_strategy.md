# Evaluation Strategy

## Direct Checks

- verify file exists at github:bihealth__NeatMS containing example dataset referenced in cond_full_training configuration
- script_runs: execute NeatMS full model training pipeline on example dataset using default CNN architecture (convolutional base + dense classifier)
- value_in_range: AUC ROC score from trained model is >= 0.9 (metric_auc_threshold)
- output_matches_reference: training and validation loss curves show no divergence indicative of overfitting (consistent with result_no_overfitting_observed); parameter-sensitive to epoch-by-epoch loss trajectory interpretation

## Expert Review

- confirm that reported AUC ROC value of ≥0.9 represents appropriate evaluation on held-out test set (not training set)
- assess whether loss curve stability and metric consistency across epochs substantiate the claim of no overfitting observed
- verify that default CNN architecture (convolutional base + dense classifier) was applied without undocumented modifications
