# Evaluation Strategy

## Direct Checks

- verify file 'tests/tests_data/ftms/ESI_NEG_SRFA.d' exists
- verify file 'tests/tests_data/ftms/SRFA.ref' exists
- verify output structured record contains field 'calibration_points_count' with integer value
- verify output structured record contains field 'calibration_coefficients' with numeric array
- verify output structured record contains field 'residuals' with numeric array or single value
- verify script_runs without exception when loading DS-001 spectrum and DS-002 reference file
- verify calibration_points_count is exactly the number of matched m/z values from SRFA.ref
- verify when matched_count < 5, PPM window is widened (robust to parameter choices, parameter-sensitive on window increment threshold)

## Expert Review

- assess whether calibration coefficients are physically reasonable for the mass spectrometry instrument type (FTMS)
- assess whether residuals indicate acceptable fit quality after fallback to wider PPM window
- assess whether the conditional logic correctly triggers window widening at the threshold of fewer than 5 matched reference points
- assess whether calibration results are consistent with standard SRFA calibration practices in mass spectrometry
