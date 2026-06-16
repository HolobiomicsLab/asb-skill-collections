# Evaluation Strategy

## Direct Checks

- verify that the BAM repository (HassounLab/BAM) is accessible and contains executable pipeline code
- verify that a validation dataset is deposited and accessible (e.g., via GitHub repository, Zenodo, or supplementary materials)
- verify that the pipeline script runs without errors on the validation dataset using the repository codebase
- verify that pipeline execution produces output files in expected format (e.g., CSV, JSON, or structured results table)
- value of reported validation metric (annotation accuracy or coverage) matches the metric value produced by pipeline execution on validation dataset — exact match required
- verify output file contains required fields for validation metrics (e.g., accuracy, coverage, sensitivity, specificity columns or equivalent)

## Expert Review

- assess whether the pipeline execution faithfully implements the biotransformation-based annotation method as described in the article methods
- assess whether the reproduced validation metrics are scientifically reasonable and consistent with method design
- assess whether any discrepancies between reported and reproduced metrics can be explained by documentation, parameter defaults, or known environment differences
