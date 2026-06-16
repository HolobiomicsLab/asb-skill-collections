# Evaluation Strategy

## Direct Checks

- verify file exists in constantino-garcia/cmmrt repository containing trained cond_meta_learning_10mol model or checkpoint
- verify script_runs: execute meta-learning model inference pipeline on a held-out test set of molecules with known retention times
- verify output_matches_reference: mean absolute error (MAE) and median absolute error (MdAE) from 10-molecule calibration set match or fall within reported competitive range against baseline projections
- value_in_range: number of calibration molecules used in cond_meta_learning_10mol evaluation equals 10
- file_format_is: model weights and hyperparameters are stored in standard format (HDF5, pickle, PT, or documented custom format)
- contains_substring: repository documentation or paper supplementary materials explicitly reference 'cond_meta_learning_10mol' or equivalent model identifier

## Expert Review

- assess whether reported error rates (MAE, MdAE) from 10-molecule meta-learning projection are statistically competitive with baseline projection approaches (e.g., linear regression, PLS, other meta-learning variants) when accounting for method differences and dataset characteristics
- evaluate appropriateness of the 10-molecule calibration set selection: whether molecules are representative of chemical diversity and retention time range needed for reliable projection
- judge whether comparison against baseline projections is fair and controlled (same training data, same test molecules, same evaluation metric definitions)
