# Evaluation Strategy

## Direct Checks

- verify that inputs include a valid NetCDF file from PNNLMetV20191015.MSL dataset or a file path to DS-004
- verify that the CoreMS pipeline executes without runtime errors when called with ReadAndiNetCDF, GC_RI_Calibration, and LowResMassSpectralMatch modules
- verify that expected_outputs CSV file exists and file_format_is CSV
- verify that CSV contains at least the following fields: compound_name (or equivalent identifier), retention_index_score, spectral_match_score
- verify that row_count_equals is greater than zero (at least one compound identified)
- verify that values in retention_index_score and spectral_match_score fields are in_range [0.0, 1.0] or [0, 100] depending on normalization (no canonical answer without pipeline documentation)
- verify that script_runs successfully: the pipeline execution command completes with exit code 0

## Expert Review

- assess whether retention-index scores are biochemically plausible for GC-MS separation (expert domain knowledge of gas chromatography required)
- assess whether spectral match scores align with expected mass spectral matching quality for the PNNLMetV20191015.MSL reference library (requires MS chemometrics expertise)
- evaluate whether identified compound assignments are consistent with known standards or reference spectra in the PNNL library
