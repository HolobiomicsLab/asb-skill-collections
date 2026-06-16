# Evaluation Strategy

## Direct Checks

- file_exists: verify that MassIVE dataset MSV000086542 contains file 20181113_010_autoQC01.raw and is accessible
- script_runs: execute rawrr::readSpectrum(rawfile, scan=9594) on the downloaded raw file without errors
- field_present: verify that spectrum object for scan 9594 contains fields for resolving power, AGC injection time, m/z values, and intensity values
- value_in_range: resolving power reported for scan 9594 equals 30000 (or within ±5% tolerance)
- value_in_range: AGC injection time for scan 9594 equals 2.8 ms (or within ±0.1 ms tolerance)
- output_matches_reference: y-ion signals in scan 9594 spectrum are numeric values, extractable, and comparable to baseline noise level (no canonical answer for 'tens to hundreds above noise' without reference noise floor value provided in article)

## Expert Review

- Assess whether extracted y-ion signals from scan 9594 are qualitatively 'several tens to hundreds above the noise level' by visual inspection of intensity distribution and peak heights relative to baseline
- Verify that resolving power value of 30000 at 200 m/z is consistent with Orbitrap FTMS instrument specifications for Q Exactive HF
- Confirm that AGC injection time of 2.8 ms aligns with reasonable acquisition settings for FTMS analysis
