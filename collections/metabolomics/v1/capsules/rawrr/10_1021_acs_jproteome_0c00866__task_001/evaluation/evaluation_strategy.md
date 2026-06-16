# Evaluation Strategy

## Direct Checks

- file_exists: verify that 20181113_010_autoQC01.raw is accessible from MassIVE dataset MSV000086542
- script_runs: execute rawrr::readSpectrum() on the deposited file to extract spectral data for iRT peptide precursors
- script_runs: execute rawrr::readChromatogram() with mass tolerance and iRT m/z values to retrieve extracted ion chromatograms
- format_is: verify that readChromatogram output is a rawrrChromatogram object containing fitted intensity traces with retention time annotations
- script_runs: fit linear regression model rtFittedAPEX ~ iRTscore using extracted retention times from chromatogram peaks
- value_in_range: R-squared value from regression model equals 0.9999 (or within ±0.0001, robust to numerical precision in floating-point computation)

## Expert Review

- Verify that iRT peptide m/z values and expected retention times used in the analysis are correct for the iRT standard mixture
- Assess whether retention time extraction method (maximum of fitted intensity traces) is appropriate for the reported R-squared claim
- Evaluate whether R-squared = 0.9999 is consistent with reported claim of 'highly linear RT behavior' and represents a meaningful fit quality for LC-MS calibration
