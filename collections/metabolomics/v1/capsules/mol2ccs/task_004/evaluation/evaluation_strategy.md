# Evaluation Strategy

## Direct Checks

- verify that the enveda/ccs-prediction repository contains a trained GNN baseline model checkpoint or weights file
- verify that the repository includes a labeled CCS dataset with documented train/validation/test split definitions
- script runs: verify that a Python script implementing an alternative message-passing GNN variant (GAT or MPNN) can be executed without errors on the repository's dataset
- verify that the alternative GNN implementation accepts the same molecular input format as the original GNN architecture
- verify that the re-trained alternative model produces numerical predictions (CCS values or embeddings) on the test split
- verify that a performance comparison table file exists with at least two rows (original GNN + alternative variant) and at least three columns (architecture name, metric1, metric2)
- value_in_range: verify that reported performance metrics (e.g., MAE, RMSE, R²) for both architectures fall within physically plausible bounds for CCS prediction tasks
- verify that the alternative architecture training log or hyperparameter configuration file is reproducibly specified (no canonical answer for optimal hyperparameters; parameter-sensitive)
- output_matches_reference: if the original paper reports baseline performance on this dataset split, verify that the re-implemented baseline GNN reproduces those reported metrics within ±5% relative error (robust to minor implementation variations)

## Expert Review

- confirm that the alternative message-passing variant (GAT or MPNN) represents a meaningful architectural departure from the original GNN (not merely a hyperparameter tune)
- assess whether differences in performance between the original and alternative architecture are scientifically interpretable and likely due to architectural factors rather than training instability
- evaluate whether the experimental setup (same dataset split, comparable training budget) is fair and whether any confounding factors (e.g., different learning rates, batch sizes) are adequately controlled or disclosed
- judge the statistical significance of performance differences if confidence intervals or multiple runs are provided
