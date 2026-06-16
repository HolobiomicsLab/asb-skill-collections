# SciTask Card: Reconstruct the PynndescentKNNBuilder as a GraphBuilderCSR subclass for approximate KNN graph construction

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T17:58:24.733366+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_squidpy/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `modeling`
- DOI: `10.1038/s41592-021-01358-2`
- GitHub: `scverse/squidpy`
- Input from: `task_001`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `multi-omics-integration`, `spatial-metabolomics`
- Techniques: `clustering`, `dimensionality-reduction`, `machine-learning`, `statistical-analysis`

## Research Question
How does the PynndescentKNNBuilder class implement graph construction by subclassing GraphBuilderCSR and integrating pynndescent as its nearest-neighbor backend?

## Connected Finding
Squidpy builds on scanpy and anndata, providing streamlined APIs for feature extraction and spatial statistics that enable scalable analysis of spatial molecular data.

## Task Description
Implement the PynndescentKNNBuilder class by subclassing GraphBuilderCSR with pynndescent as the approximate nearest-neighbor backend, and verify it produces valid CSR sparse adjacency and distance matrices when applied to spatial coordinate data.

## Inputs
- Spatial coordinates as a numpy array of shape (n_obs, n_dims)

## Expected Outputs
- CSR sparse adjacency matrix (adj) of shape (n_obs, n_obs) with float32 dtype and binary indicator values
- CSR sparse distance matrix (dst) of shape (n_obs, n_obs) with float64 dtype containing pairwise Euclidean distances
- Validation report confirming matrix shape, sparsity consistency, diagonal correctness, and CSR format validity

## Expected Output File

- `pynndescent_knn_builder_validation.txt`

## Landmark Outputs

- `adj_matrix.npz`
- `dst_matrix.npz`
- `builder_instantiation_test.log`

## Tools
- Squidpy
- pynndescent
- scipy.sparse
- numpy
- Python
- pytest

## Skills
- nearest-neighbor-graph-construction-pynndescent
- sparse-matrix-csr-format-assembly
- euclidean-distance-computation-approximation
- graph-builder-subclassing-squidpy
- spatial-coordinate-indexing-dense-to-sparse

## Workflow Description
1. Install pynndescent library into the development environment. 2. Create PynndescentKNNBuilder class inheriting from GraphBuilderCSR, implementing the build_graph method to instantiate NNDescent with Euclidean metric on input coordinates. 3. Query the NNDescent model for k-nearest neighbors (with k=n_neighs parameter) and extract indices and distances. 4. Construct CSR sparse matrices for adjacency (adj, using float32 indicator values of 1.0) and distance (dst, using float64 distance values) from the flattened row/column indices and distances. 5. Set diagonal values: adj diagonal to 1.0 if set_diag is True else existing values; dst diagonal to 0.0. 6. Return (adj, dst) tuple from build_graph and implement uns_params method returning n_neighbors and set_diag. 7. Test the builder on sample spatial coordinates and verify adjacency matrix shape matches (n_obs, n_obs), sparsity pattern is consistent between adj and dst, and matrices are in CSR format.

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
- No changelog documenting implementation details, API signatures, or expected behavior of PynndescentKNNBuilder

## Domain Knowledge
- GraphBuilderCSR is a base class that requires implementing build_graph to return a tuple (adj, dst) where both are CSR sparse matrices of matching sparsity structure with shape (n_obs, n_obs).
- The adjacency matrix (adj) uses float32 dtype and acts as a boolean indicator (1.0 for present edges, 0.0 for absent), while the distance matrix (dst) uses float64 and encodes edge-associated numeric values such as Euclidean distances.
- NNDescent performs approximate k-nearest-neighbor search in Euclidean space and returns indices and distances; these must be reshaped and flattened into row/column coordinate pairs for sparse matrix construction.
- The diagonal of adj should be set to 1.0 only when set_diag=True (convention for including self-loops); the diagonal of dst should always be 0.0 by convention, since distance from a point to itself is zero.
- CSR (Compressed Sparse Row) format is required for Squidpy's postprocessor pipeline and multi-library combination, ensuring efficient sparse operations and compatibility with Squidpy's graph manipulation utilities.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: pynndescent, pytest, CSR sparse adjacency matrix (adj) of shape (n_obs, n_obs) with float32 dtype and binary indicator values, Validation report confirming matrix shape, sparsity consistency, diagonal correctness, and CSR format validity.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does the PynndescentKNNBuilder class implement graph construction by subclassing GraphBuilderCSR and integrating pynndescent as its nearest-neighbor backend?: 'Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Squidpy builds on scanpy and anndata, providing streamlined APIs for feature extraction and spatial statistics that enable scalable analysis of spatial molecular data.: 'It builds on scanpy and anndata, providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Spatial coordinates as a numpy array of shape (n_obs, n_dims): 'Build it like any other builder: import squidpy as sq; sq.gr.spatial_neighbors_from_builder(adata, PynndescentKNNBuilder(n_neighs=6))'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] CSR sparse adjacency matrix (adj) of shape (n_obs, n_obs) with float32 dtype and binary indicator values: 'adj = csr_matrix((np.ones_like(row_indices, dtype=np.float32), (row_indices, col_indices)), shape=(n_obs, n_obs))'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] CSR sparse distance matrix (dst) of shape (n_obs, n_obs) with float64 dtype containing pairwise Euclidean distances: 'dst = csr_matrix((dists, (row_indices, col_indices)), shape=(n_obs, n_obs))'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Validation report confirming matrix shape, sparsity consistency, diagonal correctness, and CSR format validity: 'adj.setdiag(1.0 if self.set_diag else adj.diagonal()); dst.setdiag(0.0)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] pynndescent: 'The [pynndescent](https://github.com/lmcinnes/pynndescent) library provides an approximate nearest-neighbor search backend'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] scipy.sparse: 'csr_matrix objects and should reuse Squidpy's CSR-specific postprocessors'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] numpy: 'np.repeat(np.arange(n_obs), self.n_neighs); np.ones_like(row_indices, dtype=np.float32)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] Python: 'Spatial Single Cell Analysis in Python'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] pytest: 'This package uses [pytest][] for automated testing.'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting implementation details, API signatures, or expected behavior of PynndescentKNNBuilder: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file exists in squidpy repository containing PynndescentKNNBuilder class definition
- verify PynndescentKNNBuilder class inherits from GraphBuilderCSR
- verify script runs: instantiate PynndescentKNNBuilder with spatial coordinate array input and invoke build_graph method
- verify output is scipy.sparse CSR matrix with non-zero structure
- verify CSR matrix has shape matching (n_samples, n_samples) where n_samples is the input coordinate count

### Expert Review
- assess whether pynndescent backend is correctly integrated for nearest-neighbor computation
- review whether CSR sparse graph connectivity is semantically valid for spatial neighborhood structure

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Install pynndescent and create PynndescentKNNBuilder subclass of GraphBuilderCSR with configurable n_neighs parameter.
2. Instantiate NNDescent model on input coordinates with Euclidean metric and query for k-nearest neighbors.
3. Flatten k×n_obs indices and distances into 1D arrays and construct CSR adjacency matrix (float32) and distance matrix (float64) with matching sparsity patterns.
4. Set diagonal elements: adj diagonal to 1.0 (if set_diag) or existing value, dst diagonal to 0.0.
5. Validation: verify output matrices are CSR format, shapes are (n_obs, n_obs), sparsity patterns match, and diagonals are correctly set.
6. References: source article (DOI: 10.1038/s41592-021-01358-2)

## Workflow Ports

**Inputs:**

- `spatial_coords` — Spatial coordinates as numpy array ← `task_001/adata_with_graph`

**Outputs:**

- `adj_matrix` — CSR sparse adjacency matrix
- `dst_matrix` — CSR sparse distance matrix
- `validation_report` — Matrix validity and format check report

**Used:** `urn:asb:port:task_001/adata_with_graph`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:scverse__squidpy`
- **Synthesized at:** 2026-06-15T18:06:28+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
