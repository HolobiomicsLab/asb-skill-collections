# Evaluation Strategy

## Direct Checks

- verify file exists: enveda/ccs-prediction repository accessible at github.com/enveda/ccs-prediction
- verify file_exists: trained model checkpoint(s) present in repository (e.g., .pt, .pkl, or model directory)
- verify file_exists: CCS dataset or reference to deposited dataset in repository (Zenodo accession, GitHub release, or data/ subdirectory)
- script_runs: execute inference script on held-out test set without errors
- output_matches_reference: computed RMSE value matches reported metric from Engler et al. 2024 (exact value or within tolerance specified in repository documentation)
- output_matches_reference: computed MAE value matches reported metric from Engler et al. 2024 (exact value or within tolerance specified in repository documentation)
- output_matches_reference: computed R² value matches reported metric from Engler et al. 2024 (exact value or within tolerance specified in repository documentation)
- format_is: metric output is a structured record (table, .csv, or JSON) containing at minimum fields for RMSE, MAE, R² and their values

## Expert Review

- verify that reported generalizability metrics (RMSE, MAE, R²) are scientifically appropriate for CCS prediction task and dataset scale
- assess whether reproduced metrics indicate equivalent model generalizability to original reported results (accounting for computational environment differences, random seeds, hardware variations)
- confirm that held-out test set used for reproduction is equivalent in composition and size to the test set described in Engler et al. 2024 methods
