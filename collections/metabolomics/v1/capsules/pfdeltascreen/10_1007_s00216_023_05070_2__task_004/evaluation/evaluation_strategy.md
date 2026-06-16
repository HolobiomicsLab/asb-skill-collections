# Evaluation Strategy

## Direct Checks

- verify file exists: github:JonZwe__PFAScreen repository is accessible and contains source code for MS2 diagnostic fragment screening module
- file_format_is: input artifact is a valid mzML file (XML-based mass spectrometry data format)
- script_runs: MS2 filter module executes without runtime errors on sample centroided MS2 spectra from mzML input
- output_matches_reference: feature flagging output (list of feature IDs or scan indices) matches expected format with at least one named field identifying flagged features and one field recording diagnostic fragment mass match or mass difference value
- field_present: output contains at least one structured field documenting which diagnostic fragment mass(es) or characteristic mass difference(es) triggered each feature flag
- value_in_range: diagnostic fragment masses or mass differences reported in output fall within plausible PFAS chemical mass range (approximately 50–500 Da for common PFAS diagnostic fragments); robust to minor calibration drift

## Expert Review

- chemical validity of diagnostic fragment masses used in the filter: confirm that selected m/z values correspond to known PFAS diagnostic fragments (e.g., CF2 loss, CF3 ion, perfluorocarbon chain fragments) and that mass tolerance windows are appropriate for high-resolution MS
- appropriateness of mass difference thresholds: verify that characteristic mass differences (e.g., CF2 repeating unit ≈48 Da) are chemically meaningful and correctly parameterized for the instrument resolution
- clinical or regulatory relevance of prioritization: assess whether flagged features align with PFAS compound families of toxicological or regulatory concern
