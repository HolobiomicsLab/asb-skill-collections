# Evaluation Strategy

## Direct Checks

- verify file exists in github:bihealth__NeatMS repository: example mzML input file
- verify file exists in github:bihealth__NeatMS repository: example feature-table input file
- script_runs: NeatMS default preprocessing applied to example inputs without errors
- verify output file format_is: peak matrix (array, table, or matrix format)
- verify peak matrix shape matches documented result_matrix_shape artifact — first 40 and last 40 values (robust to representation format)
- verify peak matrix binary dimension (rows vs. columns) matches documented result_matrix_shape — exact byte-for-byte or exact value comparison

## Expert Review

- peak matrix values and distributions are consistent with expected LC-MS preprocessing behavior (noise filtering, normalization if applied)
- first and last 40 row/column values are scientifically plausible given input mzML and feature-table characteristics
