# Evaluation Strategy

## Direct Checks

- file_exists: verify that deposited model file (zenodo.org/record/4699356) is accessible and contains trained weights
- file_exists: verify that GitHub repository (https://github.com/matchms/ms2deepscore) contains Monte-Carlo Dropout implementation and inference scripts
- script_runs: execute Monte-Carlo Dropout ensemble inference (N=100 predictions) on test set (3601 spectra) using deposited model and verify script completes without error
- output_matches_reference: verify computed per-Tanimoto-bin RMSE values (without IQR filtering) match reported values from article figures/tables to within parameter-sensitive tolerance (robust to minor numerical precision variations across platforms)
- output_matches_reference: verify computed per-Tanimoto-bin RMSE values (with IQR < 0.025 filtering) match reported values from article figures/tables to within parameter-sensitive tolerance
- value_in_range: RMSE reduction in low Tanimoto bin (< 0.4) after IQR < 0.025 filtering is positive and exceeds baseline noise floor (no canonical answer; multiple defensible filtering thresholds exist)
- value_in_range: RMSE reduction in high Tanimoto bin (> 0.7) after IQR < 0.025 filtering is positive and exceeds baseline noise floor (no canonical answer; multiple defensible filtering thresholds exist)

## Expert Review

- Assess whether reported RMSE drops are statistically significant and meaningful given test set size and score distribution across Tanimoto bins
- Evaluate whether IQR < 0.025 filtering threshold is appropriate and whether alternative uncertainty quantiles would be more defensible
- Verify that Monte-Carlo Dropout with N=100 samples provides adequate convergence of uncertainty estimates and whether reported ensemble size is justified
- Judge whether per-bin RMSE metrics are computed correctly (e.g., bin boundaries, sample counts per bin, treatment of boundary cases)
- Review whether the reported RMSE improvements are practically meaningful for metabolomic workflows (e.g., impact on spectral matching accuracy, network analysis quality)
