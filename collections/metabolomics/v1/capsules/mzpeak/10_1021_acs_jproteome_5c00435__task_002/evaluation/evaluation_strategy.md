# Evaluation Strategy

## Direct Checks

- verify file exists at github:mobiusklein__mzpeak_prototyping/python/ subdirectory
- script_runs: execute Python loader script from python/ subdirectory without errors
- file_format_is: output artifact is valid Parquet file or pandas DataFrame serialized to standard format (pickle, CSV, or Parquet)
- field_present: output table contains at least one column representing m/z values
- field_present: output table contains at least one column representing intensity values
- row_count_equals: output table has row_count > 0 (non-empty spectrum data)
- output_matches_reference: if reference mzPeak file and expected output are available in repository, verify loaded DataFrame schema and row count match reference specification

## Expert Review

- Verify that loaded spectrum data types (m/z and intensity) are appropriate for mass spectrometry (numeric, not truncated or corrupted)
- Confirm that tabular structure correctly represents the logical hierarchy of mzPeak format (e.g., spectra, scans, peaks are correctly denested or indexed)
- Assess whether pyarrow library integration follows Arrow memory model semantics correctly (zero-copy semantics, column-store layout)
