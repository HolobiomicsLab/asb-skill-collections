# Evaluation Strategy

## Direct Checks

- Verify file exists: github:bihealth__NeatMS repository is accessible and contains the NeatMS package source code
- Verify script runs: execute get_true_vs_false_positive_df() function from NeatMS package on default model outputs under cond_full_training condition without errors
- Verify output_matches_reference: returned data frame contains columns for True Positive Rate and False Positive Rate at minimum
- Value in range: True Positive Rate at threshold 0.01 equals 1.0 (100% High_quality retained), robust to floating-point representation
- Value in range: False Positive Rate at threshold 0.01 is approximately 0.44 (44% false positive), parameter-sensitive to threshold specification
- Verify contains_substring: output data frame row at threshold 0.01 shows Low_quality proportion of approximately 0.80 (80%), robust to minor rounding differences

## Expert Review

- Verify that the metric_threshold_001_true label (100% High_quality retained) is correctly interpreted as the True Positive Rate value and aligns with the classification task definition
- Verify that the metric_threshold_001_false label (44% false positive, 80% Low_quality, specific Noise proportion) correctly describes the False Positive Rate composition and that the 80% Low_quality figure represents the conditional distribution among false positives
- Assess whether threshold 0.01 is a reasonable and appropriate decision boundary for the NeatMS neural network classifier given the training objectives
