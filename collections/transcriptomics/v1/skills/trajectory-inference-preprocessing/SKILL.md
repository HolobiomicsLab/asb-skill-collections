---
name: trajectory-inference-preprocessing
description: Use when you have raw or normalized single-cell RNA-seq expression data stored in an AnnData object (`.h5ad` format) and your analysis goal is to infer developmental or differentiation trajectories.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3291
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3308
  tools:
  - Python
  - Scanpy
  - anndata
  - PAGA
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
- Single-Cell Analysis in Python
- type annotations on function parameters
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_scanpy
    doi: 10.1186/s13059-017-1382-0
    title: scanpy
  dedup_kept_from: coll_scanpy
schema_version: 0.2.0
---

# trajectory-inference-preprocessing

## Summary

Prepare clustered single-cell gene expression data for trajectory inference by constructing a k-nearest neighbor graph and applying Leiden clustering. This preprocessing step abstracts the high-dimensional cell-to-cell neighborhood structure into a coarse-grained partition graph suitable for downstream trajectory algorithms like PAGA.

## When to use

Apply this skill when you have raw or normalized single-cell RNA-seq expression data stored in an AnnData object (`.h5ad` format) and your analysis goal is to infer developmental or differentiation trajectories. Use it specifically when you need to move from individual cell resolution to cluster-level abstraction before running partition-based graph abstraction (PAGA) or other trajectory methods that operate on clustered data.

## When NOT to use

- The input data has not been normalized or contains confounding batch effects that have not been corrected; trajectory inference requires comparable gene expression levels across cells.
- You already have manual cell type annotations and do not need unsupervised clustering; Leiden clustering may contradict existing biological labels.
- Your single-cell dataset has extremely low depth (< 500 UMI per cell on average) or sparse sampling of the developmental process, as the kNN graph and clustering will not reliably capture continuous transitions.

## Inputs

- AnnData object (.h5ad) with normalized or log-transformed gene expression matrix in `.X`
- PCA representation (typically pre-computed in `.obsm['X_pca']`)
- Raw or preprocessed expression counts

## Outputs

- AnnData object with k-nearest neighbor graph (connectivities and distances matrices in `.obsp`)
- AnnData object with Leiden cluster assignments in `.obs['leiden']`
- Neighborhood graph ready for partition-based abstraction

## How to apply

Load your expression matrix into an AnnData object and compute the principal component analysis (PCA) representation using default scanpy preprocessing. Next, construct a k-nearest neighbor (kNN) graph using `sc.pp.neighbors()` with default parameters (n_neighbors=15, use_rep='X_pca'), which captures local cell-to-cell connectivity in reduced dimensionality space. Apply `sc.tl.leiden()` to partition cells into discrete clusters, which balances community detection sensitivity with computational tractability. The resulting clusters become nodes in the downstream trajectory graph. Verify that the neighbors graph (stored in `adata.obsp['distances']` and `adata.obsp['connectivities']`) has been computed and that cluster assignments exist in `adata.obs['leiden']` before proceeding to trajectory inference methods.

## Related tools

- **Scanpy** (Core toolkit providing sc.pp.neighbors(), sc.tl.leiden(), and trajectory inference functions including sc.tl.paga()) — https://github.com/scverse/scanpy
- **anndata** (Data container for single-cell gene expression data; stores expression matrix, neighborhood graph, and cluster annotations) — https://github.com/scverse/anndata
- **Python** (Programming environment for executing scanpy workflows and data manipulation)
- **PAGA** (Downstream trajectory inference method that consumes the kNN-clustered data from this preprocessing step to compute partition-based graph abstraction) — https://github.com/theislab/paga

## Examples

```
import scanpy as sc; adata = sc.datasets.paul15(); sc.pp.neighbors(adata, n_neighbors=15, use_rep='X_pca'); sc.tl.leiden(adata); print(adata.obsp['connectivities'].shape, adata.obs['leiden'].nunique())
```

## Evaluation signals

- adata.obsp['connectivities'] and adata.obsp['distances'] exist and have shape (n_cells, n_cells); confirm non-zero entries correspond to k=15 nearest neighbors per cell.
- adata.obs['leiden'] contains discrete cluster labels with no missing values; verify number of clusters is biologically reasonable (typically 5–20 for hematopoiesis datasets like paul15).
- adata.obsm['X_pca'] is present and has dimensionality matching the number of PCs retained (default ~50); confirm explained variance ratio shows expected drop-off.
- No cells have zero degree in the kNN graph (i.e., all cells have at least 15 neighbors); check that k=15 is not larger than the total number of cells minus 1.
- Leiden clustering is reproducible across runs with the same random seed; verify cluster stability by inspecting silhouette scores or comparing cluster composition to known cell type markers.

## Limitations

- The choice of k=15 neighbors is a default that may not suit all datasets; small cell populations or datasets with extreme local density gradients may require manual tuning of n_neighbors.
- Leiden clustering is stochastic; results depend on the random seed. Different seeds may yield slightly different cluster memberships, affecting downstream trajectory inference.
- PCA-based neighborhood computation assumes that the first ~50 principal components capture biologically meaningful structure; datasets with strong technical confounders or batch effects may require batch correction before this step.
- The method assumes cells are sampled densely enough along the trajectory to form a continuous kNN manifold; very sparse or discontinuous cell sampling may fragment the neighborhood graph into disconnected components.

## Evidence

- [other] Scanpy is a scalable toolkit for analyzing single-cell gene expression data that includes trajectory inference capabilities, which encompasses methods like PAGA for constructing partition-based graph abstractions from clustered data.: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data that includes trajectory inference capabilities"
- [other] Compute k-nearest neighbors graph using sc.pp.neighbors with default parameters (n_neighbors=15, use_rep='X_pca').: "Compute k-nearest neighbors graph using sc.pp.neighbors with default parameters (n_neighbors=15, use_rep='X_pca')"
- [other] Run Leiden clustering via sc.tl.leiden to partition cells into clusters.: "Run Leiden clustering via sc.tl.leiden to partition cells into clusters"
- [intro] It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
- [other] Verify that adata.uns['paga'] exists and contains a 'connectivities' matrix with dimensions matching n_clusters × n_clusters.: "Verify that adata.uns['paga'] exists and contains a 'connectivities' matrix with dimensions matching n_clusters × n_clusters"
