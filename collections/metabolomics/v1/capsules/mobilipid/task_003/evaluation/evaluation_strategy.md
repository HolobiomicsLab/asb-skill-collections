# Evaluation Strategy

## Direct Checks

- verify file exists: github:FelinaHildebrand__MobiLipid/MobiLipid_correction.Rmd or analogous R Markdown file in the repository root
- verify file_format_is: R Markdown (.Rmd) contains executable code chunks for CCS bias correction
- verify script_runs: execute the CCS correction code chunk(s) on the bias assessment output without errors
- verify output_matches_reference: corrected CCS table has same number of rows as input bias assessment output
- verify field_present: output table contains columns for original CCS values, correction factor, and corrected CCS values
- verify value_in_range: all correction factors are numeric and non-zero (parameter-sensitive to lipid class and instrument tuning)
- verify format_is: output table is CSV, TSV, or data.frame-serialized format (any of the following acceptable)

## Expert Review

- inspect corrected CCS values against the DT CCS N2 library for U13C labeled lipids: verify corrections reduce bias relative to reference standards (requires chemistry/lipidomics domain judgment)
- assess whether correction magnitude is appropriate for the detected lipid classes in the input bias assessment (parameter-sensitive to instrument platform and MS acquisition settings)
- confirm that correction methodology preserves the rank order and relative spacing of CCS values across the lipid class distribution
