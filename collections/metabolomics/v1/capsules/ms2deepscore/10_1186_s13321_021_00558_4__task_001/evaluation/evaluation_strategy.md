# Evaluation Strategy

## Direct Checks

- file_exists: verify trained MS2DeepScore model (Daylight Tanimoto condition) is accessible from zenodo.org/record/4699356
- file_exists: verify test set containing 3,601 spectra / 500 compounds is accessible from GNPS-derived deposit or supplementary data
- script_runs: execute inference pipeline on all spectrum pairs from the 3,601-spectra test set using the loaded model
- output_matches_reference: RMSE value computed on full test set (no uncertainty filter) is approximately 0.15 (robust to ±0.02 tolerance)
- output_matches_reference: RMSE value computed on test set filtered by interquartile range (IQR < 0.025) is approximately 0.10 (robust to ±0.02 tolerance)
- value_in_range: verify number of spectrum pairs in inference output equals the expected cardinality (3,601 × 3,600 / 2 for unique pairs, or as specified in methods)
- contains_substring: verify inferred predictions are continuous numeric values (Tanimoto scores) in range [0, 1]

## Expert Review

- Confirm that the reported RMSE ~0.15 (no filter) and ~0.10 (IQR < 0.025 filter) are consistent with the numerical outputs and reflect appropriate ground-truth Tanimoto score computation from RDKit Daylight fingerprints
- Assess whether the test set composition (500 unique compounds, 3,601 spectra) and data split strategy ensure no leakage from training data and represent a fair held-out evaluation
- Evaluate whether the uncertainty filtering approach (IQR < 0.025 threshold) is defensible and whether the reported improvement from ~0.15 to ~0.10 RMSE is substantial given the filtering mechanism
