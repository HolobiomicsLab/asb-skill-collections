# Evaluation Strategy

## Direct Checks

- verify that createTargetList() function exists in the TARDIS package source code
- verify file_exists: a targets.xlsx or targets.csv example file is present in the package repository or supplementary materials
- verify that the function accepts polarity as a filtering parameter (by examining function signature and documentation)
- verify that output is a data.frame (or tibble) with columns: compound ID, compound Name, m/z, RT, and polarity — robust to column order
- verify that the data.frame row count matches the input file after polarity filtering is applied (exact row count comparison)
- verify that all expected columns are present in output data.frame (field_present check for each of: ID, Name, m/z, RT, polarity)
- script_runs: the createTargetList() function executes without error when provided a well-formed targets file and valid polarity parameter
- verify output data.frame contains only rows matching the specified polarity filter (no off-polarity rows remain) — exact filtering verification

## Expert Review

- Assess whether the polarity filtering logic correctly implements the intended chemical/analytical principle (positive vs. negative ionization mode selection)
- Review whether m/z and RT columns are preserved at appropriate precision and units for downstream peak detection use
- Evaluate whether the column selection and ordering match the expected input format documented in the TARDIS methods (Methods section or README)
