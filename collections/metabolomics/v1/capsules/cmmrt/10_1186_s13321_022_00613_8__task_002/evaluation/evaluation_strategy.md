# Evaluation Strategy

## Direct Checks

- Verify file exists: constantino-garcia/cmmrt repository is accessible and contains model training code or results
- Verify file_exists: SMRT dataset (80,038 experimental retention times from METLIN) is loaded or referenced in inputs
- Verify file_format_is: alvaDesc-generated feature matrices (5,666 descriptors and 2,214 fingerprints) are present in repository or deposited artifact in standard tabular format (CSV/HDF5/NPZ)
- Verify output_matches_reference: model performance metrics (MAE, RMSE, or correlation) for three feature conditions (descriptors only, fingerprints only, combined) are reported numerically and match deposited results or supplementary tables
- Verify value_in_range: fingerprints-only model achieves lower mean absolute error than descriptors-only model (robust to exact metric choice, but requires consistent baseline)
- Verify contains_substring: repository documentation or paper supplementary materials explicitly report performance comparison across all three feature conditions with numerical values

## Expert Review

- Assess whether reported performance differences between fingerprints and descriptors are statistically significant given the reported error bars or confidence intervals
- Evaluate whether the choice of DNN architecture and regularization hyperparameters (cosine annealing, stochastic weight averaging) was applied consistently across all three feature conditions or if architectural differences confound the feature comparison
- Judge whether the experimental design (train/validation/test split, cross-validation strategy, random seed handling) ensures fair comparison across feature types
