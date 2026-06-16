# Evaluation Strategy

## Direct Checks

- file_exists: verify that a cooler test dataset is available in the cooltools package repository (e.g., at cooltools/data/ or similar documented location)
- script_runs: cooltools.coverage command executes without errors on a valid cooler file input
- file_format_is: output file is in bedGraph format or standard tabular format (TSV/CSV with named columns for chrom, start, end, and coverage)
- field_present: output table contains at minimum the fields: chromosome, bin start, bin end, and coverage value
- output_matches_reference: output structure and column ordering match the documented format described in cooltools coverage function docstring or CLI help text
- value_in_range: coverage values are non-negative integers or floats representing valid read counts

## Expert Review

- Assess whether the computed coverage values are biologically plausible given the input cooler file (e.g., coverage distribution is reasonable, no obvious computational artifacts)
- Verify that marginalization/summation logic correctly aggregates contact matrix rows or columns into per-bin coverage without double-counting or systematic bias
