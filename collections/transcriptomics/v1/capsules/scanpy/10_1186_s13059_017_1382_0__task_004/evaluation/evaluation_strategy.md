# Evaluation Strategy

## Direct Checks

- verify file exists: datasets.paul15 is loadable from scanpy.datasets module
- script_runs: tl.leiden clustering executes without error on loaded datasets.paul15 AnnData object
- script_runs: tl.paga executes without error on clustered AnnData object
- field_present: 'paga' key exists in uns (unstructured annotations) of returned AnnData object
- format_is: connectivity matrix stored at adata.uns['paga'] is a sparse or dense matrix (scipy.sparse or numpy.ndarray)
- value_in_range: shape of connectivity matrix equals (n_clusters, n_clusters) where n_clusters is the number of distinct leiden cluster labels in adata.obs

## Expert Review

- Verify that PAGA graph abstraction connectivity values are semantically meaningful (edges represent partition transitions) by inspecting non-zero entries and comparing against known partition structure
- Confirm that the leiden clustering partitions the cells into expected number of clusters consistent with datasets.paul15 biology
