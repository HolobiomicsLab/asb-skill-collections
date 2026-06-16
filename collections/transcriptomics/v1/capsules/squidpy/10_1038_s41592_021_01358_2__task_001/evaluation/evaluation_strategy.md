# Evaluation Strategy

## Direct Checks

- verify that squidpy.gr.spatial_neighbors is callable and accepts a bundled example dataset (e.g., dataset_visium or dataset_imc) as input
- verify that the function returns an AnnData object
- verify that the returned AnnData object contains a 'obsp' (observations pairwise) key after execution
- verify that the CSR graph is stored under the expected key in obsp (e.g., 'spatial_neighbors' or similar), robust to naming conventions documented in function signature
- verify that the CSR graph object has the expected structure (sparse matrix format with shape matching number of observations)
- verify that the CSR graph contains non-zero entries corresponding to spatial neighbor connections

## Expert Review

- assess whether the spatial neighbor graph topology is biologically or geometrically sensible given the input dataset's spatial coordinates
- evaluate whether the connectivity pattern matches expected spatial relationships for the tissue type or imaging modality
