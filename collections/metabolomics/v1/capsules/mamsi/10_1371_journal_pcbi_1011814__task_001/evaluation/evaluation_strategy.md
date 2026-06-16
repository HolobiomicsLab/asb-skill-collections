# Evaluation Strategy

## Direct Checks

- verify that kopeckylukas/py-mamsi repository is accessible and contains MB-PLS pipeline implementation
- verify that kopeckylukas/py-mamsi-tutorials repository contains AddNeuroMed or MY Diabetes sample dataset files
- script_runs: execute full MAMSI pipeline (MB-PLS model fitting, MB-VIP feature selection, cross-validation) on sample dataset without errors
- output_matches_reference: model performance metrics (AUC, accuracy, sensitivity, specificity) are numeric values in valid range [0.0, 1.0]
- output_matches_reference: cross-validation fold count and latent variable estimates are positive integers
- file_exists: pipeline produces a significant features list file (CSV or table format)
- file_format_is: significant features output contains at least columns for feature identifier, VIP score, and p-value
- value_in_range: MB-VIP scores are numeric and non-negative, robust to dataset-specific scaling

## Expert Review

- assess whether reported model performance metrics (AUC, accuracy) are scientifically reasonable for metabolomics classification on the specific dataset
- assess whether selected statistically significant features (after MB-VIP and permutation testing) align with known metabolic biomarkers or plausible biological signals for the phenotype
- assess whether cross-validation strategy (k-fold count, metric choice) is appropriate for the sample size and data characteristics of AddNeuroMed or MY Diabetes dataset
