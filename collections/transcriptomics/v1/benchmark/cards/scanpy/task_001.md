# SciTask Card: Reproduce the basic clustering and UMAP visualization pipeline on the PBMC3k tutorial dataset

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T17:50:38.861186+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_scanpy/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `data-analysis`, `visualization`
- DOI: `10.1186/s13059-017-1382-0`
- GitHub: `scverse/scanpy`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `transcriptomics`
- Subdomains: `rna-seq`, `differential-expression`
- Techniques: `dimensionality-reduction`, `clustering`, `batch-correction`, `normalization`, `statistical-analysis`

## Research Question
Does Scanpy successfully execute a complete single-cell analysis workflow including preprocessing, clustering, and embedding on standard datasets?

## Connected Finding
Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata.

## Task Description
Execute the canonical Scanpy tutorial workflow on the pbmc3k dataset: load data, apply standard preprocessing (normalize, log-transform, identify highly variable genes, scale), compute k-nearest neighbors, run Leiden clustering, and compute UMAP embedding. Verify the output AnnData object contains expected cluster annotations and 2-D UMAP coordinates.

## Inputs
- pbmc3k dataset from Scanpy built-in datasets

## Expected Outputs
- AnnData object with leiden cluster annotations in adata.obs['leiden']
- 2-D UMAP embedding stored in adata.obsm['X_umap']
- Highly variable genes flagged in adata.var['highly_variable']

## Expected Output File

- `pbmc3k_processed.h5ad`

## Landmark Outputs

- `pbmc3k_normalized.h5ad`
- `pbmc3k_hvg_selected.h5ad`
- `pbmc3k_scaled_pca.h5ad`
- `pbmc3k_neighbors_computed.h5ad`
- `pbmc3k_leiden_clustered.h5ad`
- `pbmc3k_umap_embedded.h5ad`

## Tools
- Scanpy
- anndata
- Python

## Skills
- single-cell-rna-seq-normalization
- gene-expression-log-transformation
- highly-variable-gene-selection
- dimensionality-reduction-via-pca
- k-nearest-neighbor-graph-construction
- leiden-clustering-of-cells
- umap-embedding-visualization

## Workflow Description
1. Load the pbmc3k dataset using sc.datasets.pbmc3k(). 2. Apply normalize_total normalization to account for sequencing depth differences. 3. Apply log1p transformation to stabilize variance. 4. Identify highly variable genes using pp.highly_variable_genes to reduce dimensionality. 5. Scale gene expression to unit variance using pp.scale. 6. Compute principal component analysis (PCA) using pp.pca with default parameters. 7. Compute k-nearest neighbor graph using pp.neighbors with default parameters (n_neighbors=15). 8. Perform Leiden clustering using tl.leiden to identify cell clusters. 9. Compute 2-D UMAP embedding using tl.umap for visualization. 10. Verify that the output AnnData object contains 'leiden' cluster labels in obs and 'X_umap' coordinates in obsm.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/NKG7.png` | figure | False |
| `figures/Scanpy_Logo.svg` | figure | False |
| `figures/Scanpy_Logo_BrightFG.svg` | figure | False |
| `figures/Scanpy_Logo_RGB.png` | figure | False |
| `figures/cell_types.png` | figure | False |
| `figures/ci_plot-view_attachment-tab.png` | figure | False |
| `figures/ci_plot-view_select-test.png` | figure | False |
| `figures/ci_plot-view_tests-tab.png` | figure | False |
| `figures/expected.png` | figure | False |
| `figures/filter_genes_dispersion.png` | figure | False |
| `figures/louvain.png` | figure | False |
| `figures/paga_paul15.png` | figure | False |
| `figures/paga_planaria.png` | figure | False |
| `figures/spatial-basic-analysis.png` | figure | False |
| `figures/stacked_violin_dotplot_matrixplot.png` | figure | False |
| `figures/timeseries.png` | figure | False |
| `figures/tissue_hires_image.png` | figure | False |
| `figures/tissue_lowres_image.png` | figure | False |
| `figures/tsne_1.3M.png` | figure | False |
| `figures/violin.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version specification provided
- Expected number of clusters or reference cluster assignments for pbmc3k dataset not specified
- Specific Scanpy version and dependency versions (anndata, numpy, scipy) not pinned for reproducibility

## Domain Knowledge
- Library size normalization corrects for sequencing depth variation across cells, essential before downstream analysis.
- Log transformation (log1p) reduces the dominance of highly-expressed genes and approximates normality of count-based expression data.
- Highly variable genes capture biological signal by excluding genes with low variance that are likely technical noise.
- The Leiden algorithm is a community-detection method superior to Louvain for modularity optimization in cell clustering.
- UMAP is a non-linear dimensionality reduction technique that preserves both local and global structure better than t-SNE for large datasets.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: AnnData object with leiden cluster annotations in adata.obs['leiden'], 2-D UMAP embedding stored in adata.obsm['X_umap'].

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does Scanpy successfully execute a complete single-cell analysis workflow including preprocessing, clustering, and embedding on standard datasets?: 'It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata.: 'Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] pbmc3k dataset from Scanpy built-in datasets: 'datasets.pbmc3k'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] AnnData object with leiden cluster annotations in adata.obs['leiden']: 'tl.leiden'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] 2-D UMAP embedding stored in adata.obsm['X_umap']: 'tl.umap'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Highly variable genes flagged in adata.var['highly_variable']: 'pp.highly_variable_genes'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Scanpy: 'Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] anndata: 'built jointly with anndata'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] Python: 'Single-Cell Analysis in Python'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version specification provided: '_No changelog found._'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] Expected number of clusters or reference cluster assignments for pbmc3k dataset not specified: '_No changelog found._'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] Specific Scanpy version and dependency versions (anndata, numpy, scipy) not pinned for reproducibility: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file_exists: the output AnnData object saved as .h5ad or .zarr from task execution
- verify field_present: 'obs' attribute of AnnData object contains 'leiden' column with cluster labels
- verify field_present: 'obsm' attribute of AnnData object contains 'X_umap' key with 2-D embedding
- verify format_is: 'X_umap' array has shape (n_obs, 2) where n_obs matches cell count
- verify script_runs: canonical Scanpy workflow script (pp.normalize_total, pp.log1p, pp.highly_variable_genes, pp.scale, pp.neighbors, tl.leiden, tl.umap) executes without error on pbmc3k dataset
- verify value_in_range: leiden cluster labels contain at least 2 distinct clusters (robust to parameter choices, leiden resolution may vary)
- verify contains_substring: UMAP embedding coordinates are numeric and finite (no NaN or inf values)

### Expert Review
- evaluate whether resulting cluster assignments are biologically plausible for PBMC data (expert knowledge of immune cell types required)
- assess whether UMAP embedding shows expected separation between major immune cell populations (requires domain expertise in single-cell immunology)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load pbmc3k dataset as an AnnData object containing ~3,000 cells and ~13,000 genes.
2. Apply depth normalization followed by log1p transformation to stabilize variance and scale expression values.
3. Select ~2,000 highly variable genes to reduce noise and focus on genes with biological signal.
4. Scale gene expression to unit variance and compute PCA for dimensionality reduction.
5. Construct k-nearest neighbor graph using Euclidean distance in PCA space (n_neighbors=15).
6. Detect cell clusters using the Leiden community-detection algorithm on the neighbor graph.
7. Embed cells in 2-D space using UMAP for visualization, preserving local and global structure.
8. Validation: Verify that adata.obs contains 'leiden' column with ≥2 unique cluster labels and adata.obsm contains 'X_umap' with shape (n_cells, 2).
9. References: source article (DOI: 10.1186/s13059-017-1382-0)

## Workflow Ports

**Inputs:**

- `pbmc3k_dataset` — pbmc3k raw count matrix

**Outputs:**

- `processed_adata` — Processed AnnData object with clusters and UMAP
- `leiden_clusters` — Leiden cluster labels
- `umap_embedding` — 2-D UMAP coordinates

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:scverse__scanpy`
- **Synthesized at:** 2026-06-15T17:57:56+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
