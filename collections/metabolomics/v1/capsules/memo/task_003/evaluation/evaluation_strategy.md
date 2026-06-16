# Evaluation Strategy

## Direct Checks

- verify file exists: memo package source code at github:mandelbrot-project/memo
- verify file_format_is: aligned feature table input (CSV or compatible tabular format)
- verify file_format_is: MS2 spectra input (MGF, MSP, or matchms-compatible format)
- script_runs: execute memo_from_aligned() function on provided aligned feature table and MS2 spectra without errors
- output_matches_reference: resulting MemoMatrix object has structure matching unit test expectations from test_memo_from_aligned and test_memo_from_merged_memo (https://github.com/mandelbrot-project/memo)
- field_present: MemoMatrix output contains expected attributes (e.g., matrix data, sample identifiers, feature labels)
- value_in_range: MemoMatrix element values fall within valid numeric range (robust to parameter choices in counting thresholds)
- verify contains_substring: MemoMatrix metadata or documentation string contains reference to MS2 peaks and neutral losses counting
- file_exists: unit test file test_memo_from_aligned in repository at github:mandelbrot-project/memo

## Expert Review

- verify that MemoMatrix fingerprint composition (MS2 peaks and neutral losses) reflects documented counting methodology from changelog v0.1.2
- confirm MemoMatrix dimensionality and sparsity are consistent with expected behavior for sample-feature vectorization
- assess whether MemoMatrix output is suitable for downstream alignment and comparison tasks as per MEMO use case
