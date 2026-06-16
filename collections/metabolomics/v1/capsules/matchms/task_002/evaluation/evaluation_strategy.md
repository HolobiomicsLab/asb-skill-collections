# Evaluation Strategy

## Direct Checks

- verify file exists in matchms GitHub repository (input artifact path)
- verify input file format is one of: MGF, MSP, mzML (file_format_is)
- verify output is a spectrum collection object or file in a structured format (file_exists and format_is)
- verify script runs without errors when executing peak-filtering workflow on input spectral data (script_runs)
- verify output spectrum count is less than or equal to input spectrum count (value_in_range, robust to parameter choices)
- verify filtered spectrum peaks have been reduced or modified compared to input spectra (output differs from input, parameter-sensitive to filter parameters)

## Expert Review

- assess whether peak-filtering parameters applied are appropriate for the spectral data type and scientific use case
- evaluate whether filtered spectra retain sufficient peak information for downstream similarity comparisons or analysis
- verify that filtering does not introduce artifacts or remove biologically/chemically relevant peaks
