# Evaluation Strategy

## Direct Checks

- verify that samgoldman97/mist-cf repository is accessible and contains executable code for the MIST-CF model
- verify file_exists: a benchmark MS/MS dataset file (check repository for standard naming: e.g., test_data.csv, benchmark.mgf, or similar) used for evaluation
- script_runs: execute MIST-CF end-to-end inference pipeline on the benchmark dataset without errors
- verify file_exists: output ranking file (e.g., predictions.csv or rankings.json) containing top-k formula and adduct assignments
- value_in_range: top-1 accuracy for chemical formula assignment is reported as a percentage between 0–100
- value_in_range: top-k accuracy for adduct assignment is reported as a percentage between 0–100 for reported k values
- output_matches_reference: reported top-k accuracies match values published in paper tables or figures (exact numeric match, robust to rounding to 1 decimal place)
- verify field_present: output ranking includes both formula predictions and adduct type predictions (e.g., [M+H]+, [M+Na]+, etc.)
- verify that SIRIUS baseline results are retrievable or reproducible from same benchmark dataset for direct comparison

## Expert Review

- assess whether the benchmark MS/MS dataset is appropriate and representative for chemical formula inference (standard metabolomics or natural products data)
- evaluate whether the comparison to SIRIUS is fair: identical input data, same evaluation metric (top-k accuracy), and same chemical formula search space
- judge whether reported ranking performance improvements over SIRIUS are statistically significant and practically meaningful
- assess the quality of formula and adduct assignments: whether top-ranked predictions are chemically plausible and consistent with known mass spectrometry fragmentation patterns
