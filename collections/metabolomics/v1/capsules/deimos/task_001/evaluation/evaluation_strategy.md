# Evaluation Strategy

## Direct Checks

- verify file 'example_tune_pos.h5' exists in repository or MassIVE deposit
- verify file 'example_tune_neg.h5' exists in repository or MassIVE deposit (for negative ion mode)
- script_runs: DEIMoS CCS calibration routine executes without errors on tunemix example data for positive ion mode
- script_runs: DEIMoS CCS calibration routine executes without errors on tunemix example data for negative ion mode
- value_in_range: r-squared value for positive ion mode calibration is ≥0.99997
- value_in_range: r-squared value for negative ion mode calibration is ≥0.99997
- output_matches_reference: reported r-squared values from user guide match computed values (byte-for-byte match of at least 5 significant figures)

## Expert Review

- verify that tunemix calibration data is appropriate for CCS fitting and meets quality thresholds documented in user guide
- assess whether r-squared ≥0.99997 represents adequate calibration fit quality for the intended application
