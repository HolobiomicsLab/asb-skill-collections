# Evaluation Strategy

## Direct Checks

- verify file exists at zenodo.org/record/4699356 (fully trained model)
- verify file exists at https://github.com/matchms/ms2deepscore (source code repository)
- verify test set file exists and contains 3601 spectra with structural similarity labels
- script_runs: execute precision-recall computation script with test set and model inputs without errors
- output_matches_reference: precision and recall curves (any of the following formats: PNG/PDF figure, CSV table with threshold, precision, recall columns, or pickle serialized curve object) computed from test set match reported results in article figures within ±0.02 absolute difference in precision/recall values across thresholds
- value_in_range: computed RMSE of MS2DeepScore predictions on test set is between 0.13 and 0.20 (as stated in results section)
- contains_substring: generated precision-recall output documentation clearly labels which scoring method (MS2DeepScore vs. baseline 1 vs. baseline 2) produced each curve

## Expert Review

- assess whether the three scoring methods (MS2DeepScore, baseline 1, baseline 2) are identically configured and fairly compared (same hyperparameters, same data splits, same evaluation protocol)
- judge whether precision and recall curves demonstrate that MS2DeepScore 'clearly outperforms' baselines as claimed—evaluate the magnitude of difference and statistical significance (no canonical answer: depends on domain expectations for 'clear' outperformance)
- evaluate whether the test set (3601 spectra, 500 unique InChIKeys) is sufficiently representative and independent from training/validation to support the claimed generalization
- assess appropriateness of Tanimoto ≥ threshold definition as the ground-truth label for 'structural similarity' and whether this aligns with chemical domain expectations
