# Evaluation Strategy

## Direct Checks

- verify that MiMeNet GitHub repository (https://github.com/YDaiLab/MiMeNet) contains executable code for running 10-fold cross-validation experiments
- verify that MiMeNet code implements ten iterations of 10-fold cross-validation as described in methods
- verify that Spearman correlation coefficient calculation is implemented correctly in the codebase (script_runs on validation data)
- verify that well-predicted metabolite threshold is set to 95th percentile of background distribution as stated in methods
- verify that output files or logs from cross-validation contain mean Spearman correlation coefficients for each dataset and model (file_format_is CSV/TSV or JSON with named fields for correlation values)
- value of reported mean Spearman correlation for MiMeNet on IBD (PRISM) dataset is 0.309 (robust to minor numerical precision differences <0.001)
- value of reported mean Spearman correlation for MiMeNet on Cystic Fibrosis dataset is 0.457 (robust to minor numerical precision differences <0.001)
- value of reported mean Spearman correlation for MiMeNet on Soil dataset is 0.264 (robust to minor numerical precision differences <0.001)
- value of reported well-predicted metabolite count for MiMeNet on IBD (PRISM) dataset is 366 (exact match)
- value of reported well-predicted metabolite count for MiMeNet on Cystic Fibrosis dataset is 143 (exact match)
- value of reported well-predicted metabolite count for MiMeNet on Soil dataset is 29 (exact match)
- baseline model correlation and metabolite count outputs match values reported in figures (S6 Fig, S7 Fig) or supplementary tables for Elastic Net/MelonnPan, CCA, and Random Forest
- verify that all three datasets (IBD PRISM, Cystic Fibrosis, Soil) are loaded with correct sample counts and feature dimensions as reported in Methods section

## Expert Review

- assess whether hyperparameter tuning procedure (number/size of hidden layers, L2 regularization penalty) is appropriate and reproducible across the three datasets
- assess whether the choice of Spearman correlation as the performance metric is suitable for the prediction task and comparable across datasets
- assess whether the background distribution generation procedure (shuffling dataset and re-running cross-validation) is statistically sound and whether the 95th percentile threshold for well-predicted metabolites is justified
- assess whether results from ten iterations of 10-fold cross-validation are properly aggregated (mean/standard deviation reported) and whether statistical significance is tested against baselines
- assess biological plausibility: verify that reported mean correlation improvements over baselines are consistent with the nonlinear modeling advantage of neural networks claimed in the paper
