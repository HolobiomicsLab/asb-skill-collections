# Evaluation Strategy

## Direct Checks

- verify that inputs directory or github:jhhung__PS2MS repository contains at least one SMILES string file or dataset (file_exists and format_is: text/CSV/JSON with SMILES column)
- verify that the implementation script or module exists in the repository and is executable (file_exists and script_runs: run encoding step on sample SMILES without errors)
- verify that the encoded output is a structured artifact with consistent dimensionality across multiple input molecules (output_matches_reference: row_count_equals and field_present for feature vectors of expected size)
- verify that encoded feature vectors are numerical arrays or tensors with no NaN or infinite values in the output (value_in_range: all feature values are finite numbers)

## Expert Review

- assess whether the chosen featurization method (e.g., graph convolution, fingerprint, molecular descriptor encoding) is appropriate for NPS chemical structure representation and consistent with stated deep learning model input requirements
- confirm that the encoded feature dimensionality matches the input layer of the PS2MS model architecture as described in methods
- evaluate whether the encoding preserves chemically relevant information (chirality, aromaticity, functional groups) necessary for discriminating NPS structures
