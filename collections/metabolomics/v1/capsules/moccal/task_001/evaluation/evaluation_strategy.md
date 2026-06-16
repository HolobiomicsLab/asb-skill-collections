# Evaluation Strategy

## Direct Checks

- verify that github:HinesLab__MOCCal repository is accessible and contains calibration data templates and example data files
- verify file_exists for calibration template file(s) in the MOCCal repository root or designated calibration/ subdirectory
- verify file_exists for example arrival-time data file(s) in the MOCCal repository
- script_runs: execute MOCCal calibration module with example arrival-time data and calibration template as inputs without errors
- verify output_matches_reference: confirm that CCS values produced by the calibration transform are numeric, non-negative, and within physically plausible range for biomolecules (typically 50–500 Ų)

## Expert Review

- assess whether the calibration transform correctly converts TWIM arrival-time values to CCS values according to the underlying ion-mobility physics (requires domain expertise in mass spectrometry and ion-mobility separation)
- evaluate whether the produced CCS values are consistent with known reference compounds or literature values for the biomolecular classes being calibrated
