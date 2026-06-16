# Evaluation Strategy

## Direct Checks

- verify that Zenodo deposit 10.5281/zenodo.14822624 is accessible and contains downloadable biosynfoni fingerprint dataset files
- verify file_format_is: all fingerprint vectors are in a standard serializable format (e.g., NumPy binary, HDF5, CSV, or pickle) that can be loaded by a computational agent
- verify script_runs: a Python script can successfully load all fingerprint vectors from the deposited dataset without errors
- verify that summary statistics table contains at least the following named fields: position_index, bit_frequency (or analogous), sparsity_metric, and vector_count
- verify that pairwise Tanimoto similarity distribution plot contains axes labeled with similarity range and frequency/density, with title or caption identifying it as Tanimoto similarity
- verify row_count_equals: summary statistics table has one row per fingerprint position (or one row per summary statistic computed across all vectors, depending on output schema chosen)
- verify output_matches_reference: computed bit-frequency values are consistent across repeated loads (robust to parameter choices in bit-frequency calculation)
- verify that all expected_outputs files exist in the task output directory with correct extensions (.csv, .json, .png, .pdf, or .npz as appropriate)

## Expert Review

- Confirm that the choice of Tanimoto similarity metric is appropriate for the fingerprint representation and that pairwise distance computation is correctly implemented
- Confirm that sparsity metric definition (e.g., fraction of zero bits, entropy-based measure) is justified and consistent with biosynfoni fingerprint design
- Confirm that summary statistics are computed over the full population of fingerprints in the release and are not inadvertently filtered or subsampled
- Confirm that visualization and tabular outputs are scientifically interpretable and support inferences about fingerprint bit informativeness and vector similarity landscape
