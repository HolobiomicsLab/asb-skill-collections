# Evaluation Strategy

## Direct Checks

- verify file example_counts exists in chromVAR package
- script_runs: execute chromVAR preprocessing chain (filterSamples, filterPeaks, addGCBias, computeExpectations, getBackgroundPeaks) on example_counts without errors
- script_runs: execute computeDeviations with JASPAR motif annotations on preprocessed object without errors
- verify output object is of class chromVARDeviations
- field_present: verify output object contains assay named 'deviations'
- field_present: verify output object contains assay named 'z' (z-scores)
- verify output dimensions match input peak count (after filtering) × sample count
- value_in_range: deviation scores are numeric and finite (no NaN or Inf values)
- value_in_range: z-scores are numeric and finite (no NaN or Inf values)
- robust to parameter choices: output structure consistent across standard chromVAR parameter settings

## Expert Review

- inspect whether deviation scores show reasonable magnitude and distribution for JASPAR motif analysis
- assess whether z-scores reflect expected biological signal (positive deviations for accessible motif sites, negative for closed regions)
- evaluate whether sample and peak filtering steps removed expected proportion of low-quality data
- review whether motif match annotations are properly propagated to output object rowData
