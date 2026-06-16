# Evaluation Strategy

## Direct Checks

- verify file_exists: cooler file from public repository (e.g., GitHub open2c/cooltools or Zenodo deposit)
- verify file_exists: eigenvector track input file (bedGraph, bigWig, or text format)
- script_runs: cooltools.digitize invocation with eigenvector track and binning parameters produces output without error
- file_exists: output file from digitize step (binned track artifact)
- script_runs: cooltools.saddle invocation with cooler file and digitized eigenvector input produces output without error
- file_format_is: saddle output file format is NPZ, HDF5, or documented structured format
- field_present: saddle output contains 'saddledata' matrix or equivalent named array
- field_present: saddle output contains 'saddle_strength' scalar or equivalent metric
- value_in_range: saddle_strength value is a finite numeric scalar (not NaN, not inf)
- output_matches_reference: saddle matrix dimensions match expected shape (n_bins × n_bins or similar), robust to parameter choices
- contains_substring: saddle output metadata or log indicates successful completion with no warnings related to NaN handling or bad bin masking

## Expert Review

- verify saddle matrix values are consistent with documented Hi-C contact pattern expectations (diagonal stronger than off-diagonal, symmetric structure)
- verify saddle_strength scalar is within plausible range for the input eigenvector track and cooler contact matrix (no suspiciously large or near-zero values indicating algorithmic failure)
- assess whether output format and structure match the v0.3.0+ changes documented in discussion (saddledata saved without transformation, log/linear scaling applied only at plotting stage)
