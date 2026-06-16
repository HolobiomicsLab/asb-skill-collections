# Evaluation Strategy

## Direct Checks

- verify that github:CDLMarkus__QuantyFey repository is accessible and contains a README documenting the external calibration component
- file_exists: calibration-related script or module in the QuantyFey repository (e.g., R script, function definition, or documented algorithm for converting raw MS intensity to concentration)
- contains_substring: README or documentation mentions 'calibration' AND 'intensity' AND 'concentration' (any order, case-insensitive)
- verify that any calibration function or module has documented inputs (raw MS intensity data format) and outputs (quantified concentration format)
- file_format_is: any provided calibration reference data or example (CSV, TSV, RData, or similar structured format)

## Expert Review

- Assess whether the documented calibration algorithm is mathematically sound for converting raw MS intensity to concentration (e.g., linear regression, curve fitting, standard addition method)
- Verify that the calibration component handles multiple MS ionization modes or compound classes correctly, if applicable
- Evaluate whether the calibration step is appropriately separated from drift correction and visualization components as claimed
