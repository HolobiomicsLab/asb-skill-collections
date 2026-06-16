# Evaluation Strategy

## Direct Checks

- verify file_exists: PR #61 commit or merged code in iomega/ms2query repository on GitHub
- verify file_format_is: spectrum processing module as .py Python source file(s)
- verify contains_substring: processing module contains function definitions for spectrum normalisation and/or filtering operations
- verify script_runs: spectrum processing functions execute without error on sample spectrum input (no canonical answer for which sample spectra, requires multiple defensible test cases)
- verify output_matches_reference: processed spectrum output format (peaks, intensities, metadata) is consistent with documented spectrum data structure in codebase
- verify field_present: processed spectrum output includes normalized/filtered peak list and intensity array fields
- verify value_in_range: processed spectrum intensity values fall within chemically plausible range (0–1 for normalized, or 0–max_intensity for non-normalized; no canonical answer, parameter-sensitive to normalization choice)

## Expert Review

- assess whether spectrum normalisation method (if present) is appropriate for MS/MS spectral matching workflows
- assess whether spectrum filtering logic (peak removal, noise threshold) follows standard MS/MS preprocessing practices
- assess whether cleaned spectrum output is fit-for-purpose for downstream library matching operations
- assess consistency of preprocessing step definitions against any published MS2Query method descriptions or prior versions
