# Evaluation Strategy

## Direct Checks

- verify file exists: AnnData object with .uns['fragment_file'] or .obm containing fragment data
- script_runs: pp.add_tile_matrix(adata, counting_strategy='paired_insertion') executes without error on the input AnnData object
- file_format_is: resulting count matrix is stored in adata.X or adata.obm as sparse matrix or dense array
- row_count_equals: count matrix has number of rows equal to number of observations (cells) in input AnnData
- field_present: verify 'tile_matrix' or equivalent matrix key exists in adata.obm after function call
- value_in_range: count matrix contains at least one non-zero entry (sparsity < 100%), robust to different tile sizes and fragment distributions
- output_matches_reference: if reference output matrix exists in repository test data or documentation, byte-for-byte comparison for exact parameter set

## Expert Review

- verify that paired_insertion counting logic correctly counts both read1 and read2 insertions from paired-end fragments, not total fragment count
- assess whether tile matrix dimensions (number of tiles × cells) are biologically reasonable for the input fragment file size and genome coverage
- confirm that non-zero entries in count matrix correspond to tiles with actual fragment coverage and do not represent computational artifacts
