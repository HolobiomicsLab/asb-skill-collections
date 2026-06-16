# Evaluation Strategy

## Direct Checks

- verify file_exists: the output AnnData object saved as .h5ad or .zarr from task execution
- verify field_present: 'obs' attribute of AnnData object contains 'leiden' column with cluster labels
- verify field_present: 'obsm' attribute of AnnData object contains 'X_umap' key with 2-D embedding
- verify format_is: 'X_umap' array has shape (n_obs, 2) where n_obs matches cell count
- verify script_runs: canonical Scanpy workflow script (pp.normalize_total, pp.log1p, pp.highly_variable_genes, pp.scale, pp.neighbors, tl.leiden, tl.umap) executes without error on pbmc3k dataset
- verify value_in_range: leiden cluster labels contain at least 2 distinct clusters (robust to parameter choices, leiden resolution may vary)
- verify contains_substring: UMAP embedding coordinates are numeric and finite (no NaN or inf values)

## Expert Review

- evaluate whether resulting cluster assignments are biologically plausible for PBMC data (expert knowledge of immune cell types required)
- assess whether UMAP embedding shows expected separation between major immune cell populations (requires domain expertise in single-cell immunology)
