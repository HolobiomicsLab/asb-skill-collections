# SciTask Card: Reproduce the spatial neighbor graph construction using gr.spatial_neighbors on an example dataset

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T17:58:24.733366+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_squidpy/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `benchmark-evaluation`
- DOI: `10.1038/s41592-021-01358-2`
- GitHub: `scverse/squidpy`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `multi-omics-integration`, `spatial-metabolomics`
- Techniques: `clustering`, `dimensionality-reduction`, `machine-learning`, `statistical-analysis`

## Research Question
Does squidpy.gr.spatial_neighbors correctly construct and store a CSR graph in an AnnData object with expected keys and structure when applied to a bundled example dataset?

## Connected Finding
Squidpy provides streamlined APIs for spatial statistics and interactive exploration, building on anndata as the underlying data structure.

## Task Description
Install squidpy, load a bundled example dataset (e.g., visium or imc), run squidpy.gr.spatial_neighbors to construct a spatial graph, and verify the resulting compressed sparse row (CSR) adjacency and distance matrices are correctly stored in the AnnData object's obsp slots with expected keys and structure.

## Inputs
- squidpy installation (from PyPI, conda, or git) and Python >= 3.11 environment
- Bundled example dataset (e.g., squidpy.datasets.visium or squidpy.datasets.imc)

## Expected Outputs
- AnnData object with spatial graph stored in obsp as CSR matrices with keys 'spatial_neighbors' (adjacency) and 'spatial_distances' (distance matrix)
- Verification report confirming correct matrix shape, sparsity, dtype, and diagonal properties

## Expected Output File

- `adata_spatial_graph.h5ad`

## Landmark Outputs

- `adata_loaded.h5ad`
- `adata_spatial_graph.h5ad`
- `graph_verification.txt`

## Tools
- Squidpy
- scanpy
- anndata
- Python
- pip

## Skills
- spatial-graph-construction-from-coordinates
- sparse-matrix-verification-and-validation
- anndata-object-inspection-and-structure-checking
- adjacency-matrix-sparsity-analysis
- spatial-neighbor-graph-properties-validation

## Workflow Description
1. Install squidpy and its dependencies using pip or a package manager (hatch, uv, or pip). 2. Load a bundled example dataset using squidpy.datasets (e.g., datasets.visium or datasets.imc) into an AnnData object. 3. Call squidpy.gr.spatial_neighbors on the AnnData object to compute spatial graph using coordinate data from obsm. 4. Verify that the resulting adjacency matrix and distance matrix are stored as CSR sparse matrices in adata.obsp with keys such as 'spatial_neighbors' and 'spatial_distances'. 5. Check that both matrices have shape (n_obs, n_obs) matching the observation count, have matching sparsity structure, and satisfy diagonal constraints (diagonal zero for distance, identity or zero for adjacency depending on set_diag parameter).

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/ContainerShow_axis.png` | figure | False |
| `figures/ContainerShow_channel.png` | figure | False |
| `figures/ContainerShow_channelwise.png` | figure | False |
| `figures/ContainerShow_channelwise_segmentation.png` | figure | False |
| `figures/ContainerShow_imshow_kwargs.png` | figure | False |
| `figures/ContainerShow_library_id.png` | figure | False |
| `figures/ContainerShow_scale_mask_circle_crop.png` | figure | False |
| `figures/ContainerShow_segmentation.png` | figure | False |
| `figures/ContainerShow_transpose_channelwise_False_False.png` | figure | False |
| `figures/ContainerShow_transpose_channelwise_False_True.png` | figure | False |
| `figures/ContainerShow_transpose_channelwise_True_False.png` | figure | False |
| `figures/ContainerShow_transpose_channelwise_True_True.png` | figure | False |
| `figures/DetectTissue_detect_tissue_felzenszwalb.png` | figure | False |
| `figures/DetectTissue_detect_tissue_otsu.png` | figure | False |
| `figures/figure1.png` | figure | False |
| `figures/squidpy_horizontal.png` | figure | False |
| `figures/squidpy_vertical.png` | figure | False |
| `figures/test_img.jpg` | figure | False |
| `figures/tissue_hires_image.png` | figure | False |
| `figures/tissue_lowres_image.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog documenting version history, API changes, or deprecations found

## Domain Knowledge
- Squidpy's spatial_neighbors function returns two CSR matrices (adj for adjacency, dst for distance) with matching sparsity structure and shape (n_obs, n_obs).
- The adjacency matrix encodes edge presence (typically 1.0 for present edges) and respects the set_diag parameter; the distance matrix stores edge values (e.g., Euclidean length) with zero diagonal by convention.
- CSR (Compressed Sparse Row) format is memory-efficient for large sparse graphs and is the standard output storage in AnnData.obsp slots.
- The resulting graph is stored in AnnData.obsp with keys like 'spatial_neighbors' (adjacency) and 'spatial_distances' (distances), allowing seamless integration with downstream analysis.
- Graph construction respects multi-library scenarios (when library_key is provided) by combining per-library results into a unified sparse matrix.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Verification report confirming correct matrix shape, sparsity, dtype, and diagonal properties.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does squidpy.gr.spatial_neighbors correctly construct and store a CSR graph in an AnnData object with expected keys and structure when applied to a bundled example dataset?: 'Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data. It builds on scanpy and anndata, providing streamlined APIs for feature extraction, spatial statistics'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Squidpy provides streamlined APIs for spatial statistics and interactive exploration, building on anndata as the underlying data structure.: 'providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] squidpy installation (from PyPI, conda, or git) and Python >= 3.11 environment: 'Squidpy requires Python version >= 3.11 to run. Install Squidpy by running:: pip install squidpy'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Bundled example dataset (e.g., squidpy.datasets.visium or squidpy.datasets.imc): 'datasets.visium, datasets.imc'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] AnnData object with spatial graph stored in obsp as CSR matrices with keys 'spatial_neighbors' (adjacency) and 'spatial_distances' (distance matrix): 'adj and dst are square sparse matrices of shape (n_obs, n_obs) with matching sparsity structure'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Verification report confirming correct matrix shape, sparsity, dtype, and diagonal properties: 'dst should have a zero diagonal, and adj should only have a non-zero diagonal when set_diag=True'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Squidpy: 'Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data.'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] scanpy: 'It builds on scanpy and anndata'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] anndata: 'It builds on scanpy and anndata'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] Python: 'Spatial Single Cell Analysis in Python'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] pip: 'pip install squidpy'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting version history, API changes, or deprecations found: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that squidpy.gr.spatial_neighbors is callable and accepts a bundled example dataset (e.g., dataset_visium or dataset_imc) as input
- verify that the function returns an AnnData object
- verify that the returned AnnData object contains a 'obsp' (observations pairwise) key after execution
- verify that the CSR graph is stored under the expected key in obsp (e.g., 'spatial_neighbors' or similar), robust to naming conventions documented in function signature
- verify that the CSR graph object has the expected structure (sparse matrix format with shape matching number of observations)
- verify that the CSR graph contains non-zero entries corresponding to spatial neighbor connections

### Expert Review
- assess whether the spatial neighbor graph topology is biologically or geometrically sensible given the input dataset's spatial coordinates
- evaluate whether the connectivity pattern matches expected spatial relationships for the tissue type or imaging modality

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Install squidpy package and its dependencies (scanpy, anndata, scipy) using pip or environment manager.
2. Load a bundled example dataset from squidpy.datasets (e.g., visium or imc) into an AnnData object.
3. Execute squidpy.gr.spatial_neighbors on the AnnData object to construct the spatial graph using coordinate data.
4. Verify that adjacency and distance matrices are stored as CSR sparse matrices in adata.obsp with correct shape, sparsity, and dtype.
5. Validate diagonal properties: distance matrix has zero diagonal; adjacency matrix diagonal is set according to the set_diag parameter.
6. Validation: confirm that both matrices have identical sparsity structure, shape equals (n_obs, n_obs), and the graph is ready for downstream spatial analysis.
7. References: source article (DOI: 10.1038/s41592-021-01358-2)

## Workflow Ports

**Inputs:**

- `squidpy_install` — squidpy installation (from PyPI, conda, or git)
- `example_dataset` — Bundled example dataset (squidpy.datasets.visium or squidpy.datasets.imc)

**Outputs:**

- `adata_with_graph` — AnnData object with spatial graph in obsp
- `verification_report` — Verification report of graph structure and properties

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:scverse__squidpy`
- **Synthesized at:** 2026-06-15T18:06:28+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
