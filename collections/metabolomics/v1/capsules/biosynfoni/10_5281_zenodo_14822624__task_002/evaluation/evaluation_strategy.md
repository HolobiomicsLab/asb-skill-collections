# Evaluation Strategy

## Direct Checks

- verify file exists at github:lucinamay/biosynfoni or Zenodo deposit 10.5281/zenodo.14822624
- script_runs: biosynfoni package imports without error after installation via pip
- script_runs: fingerprint computation completes on sample molecule(s) from deposited dataset without exception
- file_exists: output fingerprint file (CSV or NumPy .npy/.npz array format) is generated
- file_format_is: output fingerprint file matches declared format (CSV with numeric columns, or NumPy binary array)
- field_present: fingerprint output contains per-molecule identifiers and bit-vector columns/arrays
- row_count_equals or contains_substring: output row count matches or is traceable to number of molecules in input dataset
- value_in_range: fingerprint bit-vector entries are binary (0 or 1) or normalized numeric values, robust to parameter choices

## Expert Review

- Fingerprint bit-vector semantics: do the substructure bits align with documented biosynfoni natural-product chemical feature definitions?
- Fingerprint correctness on reference molecules: if a ground-truth fingerprint or validation set is available in the deposit, does computed output match expected bit patterns?
- Dataset suitability: does the Zenodo dataset contain molecules (SMILES, SDF, or equivalent) appropriate for biosynfoni fingerprinting?
