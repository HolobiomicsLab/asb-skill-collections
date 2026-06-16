# Evaluation Strategy

## Direct Checks

- verify that the iced module can be imported in Python (>3.7) with script_runs check on 'import iced'
- verify file_exists: normalized contact matrix output file is produced (format: .matrix or .txt or .h5, depending on iced implementation)
- verify that the input contact matrix file (raw, non-normalized) exists and is readable
- verify output_matches_reference: normalized matrix structure contains same dimensions as input matrix (row_count_equals and column dimensionality preserved)
- verify that normalized matrix values are in expected numeric range for Hi-C data (non-negative, floating-point or integer counts)
- verify script_runs: ICE normalization algorithm completes without runtime errors on test contact matrix

## Expert Review

- assess whether the normalization converges to stable solution according to iced algorithm tolerance criteria
- evaluate whether the normalized matrix exhibits expected statistical properties (row and column sum balance, bias removal)
- review whether the choice of iced algorithm parameters (e.g., max_iter, tol, filter_low_counts) is justified for the input matrix characteristics
