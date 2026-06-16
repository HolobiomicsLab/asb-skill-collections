# Evaluation Strategy

## Direct Checks

- verify file exists: locate unaligned MS2 spectra input file(s) in mandelbrot-project/memo or mandelbrot-project/memo_publication_examples repositories
- script_runs: execute memo_from_unaligned() function from memo package on input spectra without errors
- file_format_is: confirm output MemoMatrix object is serializable to standard Python pickle or HDF5 format
- field_present: verify returned MemoMatrix contains 'memo_matrix' attribute as core data structure
- row_count_equals or value_in_range: validate row count (samples) and column count (m/z features or neutral losses) are consistent with input file cardinality; no canonical answer without seeing test fixture
- contains_substring: verify unit test references in changelog (test for memo_from_unaligned) exist in repository test suite and pass
- output_matches_reference: compare generated MemoMatrix dimensions and sparsity pattern against expected outputs from repo test files, robust to minor floating-point precision differences

## Expert Review

- examine whether MemoMatrix correctly represents MS2 peak and neutral loss counting as documented ('occurrence of MS2 peaks and neutral losses in each sample is counted')
- validate that fingerprint alignment/comparison semantics are preserved in output matrix structure
- confirm matrix values fall within expected range for occurrence counts (non-negative integers or normalized frequencies)
