# Workflow Challenge: `coll_squidpy_workflow`


> Squidpy is a Python toolkit for scalable analysis and visualization of spatial molecular data, building on scanpy and anndata to provide streamlined APIs for spatial statistics, feature extraction, and interactive exploration.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Squidpy enables comprehensive analysis of spatial single-cell data through modular and scalable workflows. The toolkit provides core functionality for constructing and analyzing spatial neighbor graphs via spatial_neighbors, computing neighborhood enrichment statistics through nhood_enrichment, and detecting spatially variable genes using sepal. Image analysis capabilities are supported through lazy dask-backed computation in calculate_image_features on the ImageContainer. The package integrates with standard AnnData workflows and supports multiple spatial omics platforms including Visium, Vizgen, and Nanostring through dedicated reader functions. Additionally, Squidpy exposes extensible graph construction mechanisms through GraphBuilder and GraphBuilderCSR base classes, enabling custom implementations such as approximate nearest-neighbor backends while maintaining compatibility with built-in postprocessors and multi-library support.

## Research questions

- Does squidpy.gr.spatial_neighbors correctly construct and store a CSR graph in an AnnData object with expected keys and structure when applied to a bundled example dataset?
- How does the PynndescentKNNBuilder class implement graph construction by subclassing GraphBuilderCSR and integrating pynndescent as its nearest-neighbor backend?
- Does squidpy's nhood_enrichment function correctly compute and store neighborhood enrichment scores in an AnnData object when applied to spatial data with a pre-built neighbor graph?
- Does squidpy.gr.sepal successfully compute spatial statistics and attach gene ranking scores to an AnnData object with the expected field names when applied to spatial transcriptomics datasets?
- Does squidpy's im.calculate_image_features function support lazy computation via dask, and does it correctly materialize computed features into the AnnData object while preserving intermediate computations as dask arrays?

## Methods overview

Install squidpy package and its dependencies (scanpy, anndata, scipy) using pip or environment manager. Load a bundled example dataset from squidpy.datasets (e.g., visium or imc) into an AnnData object. Execute squidpy.gr.spatial_neighbors on the AnnData object to construct the spatial graph using coordinate data. Verify that adjacency and distance matrices are stored as CSR sparse matrices in adata.obsp with correct shape, sparsity, and dtype. Validate diagonal properties: distance matrix has zero diagonal; adjacency matrix diagonal is set according to the set_diag parameter. Validation: confirm that both matrices have identical sparsity structure, shape equals (n_obs, n_obs), and the graph is ready for downstream spatial analysis. References: source article (DOI: 10.1038/s41592-021-01358-2) Install pynndescent and create PynndescentKNNBuilder subclass of GraphBuilderCSR with configurable n_neighs parameter. Instantiate NNDescent model on input coordinates with Euclidean metric and query for k-nearest neighbors. Flatten k×n_obs indices and distances into 1D arrays and construct CSR adjacency matrix (float32) and distance matrix (float64) with matching sparsity patterns. Set diagonal elements: adj diagonal to 1.0 (if set_diag) or existing value, dst diagonal to 0.0. Validation: verify output matrices are CSR format, shapes are (n_obs, n_obs), sparsity patterns match, and diagonals are correctly set. References: source article (DOI: 10.1038/s41592-021-01358-2) Load Visium example dataset containing spatial coordinates and cell-type annotations. Construct spatial neighbor graph using radius-based neighborhood detection on spatial coordinates. Compute neighborhood enrichment by comparing observed co-occurrence of annotated cell types in spatial neighborhoods against shuffled distributions. Store enrichment statistics in AnnData.uns dictionary under 'nhood_enrichment' key. Validation: verify that the enrichment matrix exists in .uns, has expected dimensions [n_categories, n_categories], and contains numeric enrichment scores. References: source article (DOI: 10.1038/s41592-021-01358-2) Load a bundled spatial dataset (slideseqv2 or merfish) via squidpy.datasets into an AnnData container. Execute squidpy.gr.sepal on the loaded AnnData object to compute gene-level spatial enrichment scores and rankings. Extract and inspect output fields from AnnData .var, .uns, and .obsm slots to identify sepal-specific columns and matrices. Validate field names, data types, array dimensions, and absence of unexpected NaN/inf values against squidpy's expected schema. Validation: Confirm that all sepal output fields are present with correct dimensionality and no missing or corrupted values; generate a structured verification report. References: source article (DOI: 10.1038/s41592-021-01358-2) Load spatial coordinates and image file into squidpy.im.ImageContainer and link to AnnData object. Enable dask lazy computation mode in im.calculate_image_features to defer actual pixel-level calculations. Extract image features across specified scales or layers, storing intermediate results as dask arrays in memory. Explicitly collect and materialize dask arrays into AnnData.obsm or AnnData.var slots. Validation: Confirm all requested features are present in the output AnnData object, intermediate computation arrays remained as dask objects before collection, and no data loss occurred during materialization. References: source article (DOI: 10.1038/s41592-021-01358-2)

**Domain:** bioinformatics

**Techniques:** clustering, dimensionality-reduction, machine-learning, statistical-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images. [evidence_step: task_005] _[grounded: squidpy_system]_
- **(finding)** Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data. _[grounded: squidpy_system]_
- **(finding)** Squidpy requires Python version >= 3.11 to run. _[grounded: squidpy_system]_
- **(finding)** Squidpy can be installed via PyPI using pip install squidpy. _[grounded: squidpy_system]_
- **(finding)** Squidpy can be installed via Conda using conda install -c conda-forge squidpy. _[grounded: squidpy_system]_
- **(finding)** Squidpy can be installed from GitHub using pip install git+https://github.com/scverse/squidpy@main. _[grounded: squidpy_system]_
- **(finding)** Squidpy provides tools to build and analyze the neighborhood graph from spatial coordinates. _[grounded: squidpy_system]_
- **(finding)** Squidpy enables computation of spatial statistics for cell-types and genes. _[grounded: squidpy_system]_
- **(finding)** Squidpy can efficiently store, analyze and visualize large tissue images by leveraging scikit-image. _[grounded: squidpy_system]_
- **(finding)** Squidpy's original napari-plugin has been moved to napari-spatialdata. _[grounded: squidpy_system]_
- **(finding)** The Squidpy interactive module has been removed. _[grounded: squidpy_system]_
- **(finding)** napari-spatialdata is recommended as a replacement for Squidpy's deprecated napari plugin. _[grounded: squidpy_system]_
- **(finding)** Squidpy version 1.0.0 was released on 2021-02-20. _[grounded: squidpy_system]_
- **(finding)** Squidpy version 1.6.2 was released on 2024-11-12. _[grounded: squidpy_system]_
- **(finding)** In version 1.1.1, Squidpy allowed defining cylindrical shells in spatial_neighbors by using the radius argument. _[grounded: squidpy_system]_
- **(finding)** In version 1.2.0, Squidpy added spatial_scatter and spatial_segment functions to statically plot spatial omics data. _[grounded: squidpy_system]_
- **(finding)** Hatch is a Python project manager that manages virtual environments separately for development, testing and building documentation. _[grounded: tool_hatch]_
- **(finding)** Hatch allows running tests locally in different environments, such as different python versions. _[grounded: tool_hatch]_
- **(finding)** Hatch allows running tasks defined in pyproject.toml. _[grounded: tool_hatch]_
- **(finding)** Squidpy uses pre-commit to enforce consistent code-styles. _[grounded: squidpy_system]_
- **(finding)** Squidpy uses pytest for automated testing. _[grounded: squidpy_system]_
- **(finding)** Squidpy uses sphinx with myst extension to allow writing documentation in markdown. _[grounded: squidpy_system]_
- **(finding)** Squidpy documentation uses Numpy-style docstrings through the napoleon extension. _[grounded: squidpy_system]_
- **(finding)** In version 1.3.0, Squidpy added var_by_distance function to calculate distances to anchor points and store results in a design matrix. _[grounded: squidpy_system]_
- **(finding)** In version 1.6.0, mask_graph was added to mask a spatial graph based on shapely.Polygon or shapely.MultiPolygon. _[grounded: squidpy_system]_
- **(finding)** In version 1.6.2, a new function sliding_window was added for creating sliding window assignments. _[grounded: squidpy_system]_
- **(finding)** Squidpy is part of the scverse project and is fiscally sponsored by NumFOCUS. _[grounded: squidpy_system]_
- **(finding)** The manuscript describing Squidpy was published by Palla, Spitzer et al. in Nature Methods in 2022. _[grounded: squidpy_system]_
- **(finding)** Squidpy provides the graph module with functions for spatial neighbor analysis including spatial_neighbors, spatial_neighbors_knn, spatial_neighbors_radius, spatial_neighbors_delaunay, and spatial_neighbors_grid. _[grounded: squidpy_system]_
- **(finding)** Squidpy provides image processing functions including im.process, im.segment, im.calculate_image_features, and im.SegmentationModel. _[grounded: squidpy_system]_
- **(finding)** Squidpy provides plotting functions including pl.spatial_scatter, pl.spatial_segment, pl.nhood_enrichment, pl.centrality_scores, pl.interaction_matrix, pl.ligrec, pl.ripley, pl.co_occurrence, pl.extract, and pl.var_by_distance. _[grounded: squidpy_system]_
- **(finding)** Squidpy provides reading functions for visium, vizgen, and nanostring file formats. _[grounded: squidpy_system]_
- **(finding)** Squidpy provides tools functions including tl.sliding_window and tl.var_by_distance. _[grounded: squidpy_system]_
- **(finding)** Squidpy provides dataset functions for accessing example datasets including four_i, imc, seqfish, merfish, mibitof, slideseqv2, sc_mouse_cortex, and various visium datasets. _[grounded: squidpy_system]_
- **(finding)** Squidpy exposes GraphBuilder and GraphBuilderCSR as base classes for custom graph builders. _[grounded: squidpy_system]_
- **(finding)** In version 1.0.1, Squidpy fixed complex handling in the ligrec function. _[grounded: squidpy_system]_
- **(finding)** In version 1.0.1, Squidpy re-implemented the interaction_matrix function. _[grounded: squidpy_system]_
- **(finding)** In version 1.1.0, Squidpy added the sepal function. _[grounded: squidpy_system]_
- **(finding)** In version 1.1.0, Squidpy replaced moran with spatial_autocorr, which implements both Moran's I and Geary's C. _[grounded: squidpy_system]_
- **(finding)** In version 1.1.0, Squidpy added the option to compute graphs from Delaunay triangulation in spatial_neighbors. _[grounded: squidpy_system]_
- **(finding)** In version 1.1.0, Squidpy added lazy computation using dask for the im module. _[grounded: squidpy_system]_
- **(finding)** In version 1.1.0, Squidpy replaced ripley_k with ripley function. _[grounded: squidpy_system]_
- **(finding)** In version 1.1.0, Squidpy added three new example datasets: merfish, mibitof, and slideseqv2. _[grounded: squidpy_system]_
- **(finding)** In version 1.2.0, Squidpy added read.visium, read.vizgen and read.nanostring functions to read Visium, Vizgen and Nanostring files. _[grounded: squidpy_system]_
- **(finding)** In version 1.2.0, Squidpy added library_key in spatial_neighbors to support building graphs across multiple slides. _[grounded: squidpy_system]_
- **(finding)** In version 1.2.3, Squidpy fixed ligrec from pandas update. _[grounded: squidpy_system]_
- **(finding)** In version 1.3.0, Squidpy added percentile option to spatial_neighbors to filter neighbor graph using percentile of distances threshold. _[grounded: squidpy_system]_
- **(finding)** In version 1.3.1, Squidpy deprecated napari. _[grounded: squidpy_system]_
- **(finding)** In version 1.4.0, Squidpy fixed building graph in knn and delaunay mode. _[grounded: squidpy_system]_
- **(finding)** In version 1.5.0, Squidpy fixed the reading of 10x formatted mtx files. _[grounded: squidpy_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- pynndescent as alternative to scikit-learn NearestNeighbors for kNN graph construction

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- pynndescent must be installed in the same environment as Squidpy

## Steps

### Step `task_001`
- Title: Reproduce the spatial neighbor graph construction using gr.spatial_neighbors on an example dataset
- Task kind: `reproduction`
- Task: Install squidpy, load a bundled example dataset (e.g., visium or imc), run squidpy.gr.spatial_neighbors to construct a spatial graph, and verify the resulting compressed sparse row (CSR) adjacency and distance matrices are correctly stored in the AnnData object's obsp slots with expected keys and structure.
- Inputs:
  - squidpy installation (from PyPI, conda, or git) and Python >= 3.11 environment
  - Bundled example dataset (e.g., squidpy.datasets.visium or squidpy.datasets.imc)
- Expected outputs:
  - AnnData object with spatial graph stored in obsp as CSR matrices with keys 'spatial_neighbors' (adjacency) and 'spatial_distances' (distance matrix)
  - Verification report confirming correct matrix shape, sparsity, dtype, and diagonal properties
- Tools: Squidpy, scanpy, anndata, Python, pip
- Landmark output files: adata_loaded.h5ad, adata_spatial_graph.h5ad, graph_verification.txt
- Primary expected artifact: `adata_spatial_graph.h5ad`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the PynndescentKNNBuilder as a GraphBuilderCSR subclass for approximate KNN graph construction
- Task kind: `component_reconstruction`
- Task: Implement the PynndescentKNNBuilder class by subclassing GraphBuilderCSR with pynndescent as the approximate nearest-neighbor backend, and verify it produces valid CSR sparse adjacency and distance matrices when applied to spatial coordinate data.
- Inputs:
  - Spatial coordinates as a numpy array of shape (n_obs, n_dims)
- Expected outputs:
  - CSR sparse adjacency matrix (adj) of shape (n_obs, n_obs) with float32 dtype and binary indicator values
  - CSR sparse distance matrix (dst) of shape (n_obs, n_obs) with float64 dtype containing pairwise Euclidean distances
  - Validation report confirming matrix shape, sparsity consistency, diagonal correctness, and CSR format validity
- Tools: Squidpy, pynndescent, scipy.sparse, numpy, Python, pytest
- Landmark output files: adj_matrix.npz, dst_matrix.npz, builder_instantiation_test.log
- Primary expected artifact: `pynndescent_knn_builder_validation.txt`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce neighborhood enrichment analysis using gr.nhood_enrichment on the Visium dataset
- Task kind: `reproduction`
- Task: Execute squidpy.gr.nhood_enrichment on Visium spatial transcriptomics data after constructing a spatial neighbor graph, and verify that the enrichment score matrix is stored in the AnnData object at the expected key.
- Inputs:
  - Squidpy Visium example dataset
- Expected outputs:
  - Enrichment score matrix stored in AnnData.uns['nhood_enrichment']
  - NhoodEnrichmentResult object containing enrichment statistics
- Tools: Squidpy, anndata, Python
- Landmark output files: spatial_neighbors_graph.h5ad, nhood_enrichment_matrix.csv, enrichment_scores.png
- Primary expected artifact: `adata_with_nhood_enrichment.h5ad`

### Step `task_004`
- Depends on: `task_001`
- Title: Reproduce the SEPAL spatial variable gene detection using gr.sepal on an example dataset
- Task kind: `reproduction`
- Task: Run squidpy.gr.sepal on a bundled spatial dataset (slideseqv2 or merfish) to compute spatial enrichment and gene rankings, then verify that the resulting scores and gene rankings are correctly attached to the AnnData object under the expected field names.
- Inputs:
  - Bundled spatial omics dataset (slideseqv2 or merfish format)
  - Python environment with Squidpy installed
- Expected outputs:
  - AnnData object with sepal results (gene rankings and spatial enrichment scores) stored in .var, .uns, or .obsm
  - Verification report listing field names, data types, array shapes, and confirmation of successful computation
- Tools: Squidpy, scanpy, anndata, Python
- Landmark output files: adata_loaded.h5ad, sepal_fields_manifest.json, sepal_results_verification.txt
- Primary expected artifact: `sepal_results_verification.txt`

### Step `task_005`
- Depends on: `task_001`
- Title: Analyze lazy dask-backed image processing via im.calculate_image_features on the ImageContainer
- Task kind: `analysis`
- Task: Load a spatially resolved dataset with an associated tissue image into squidpy.im.ImageContainer, compute image features using im.calculate_image_features with dask lazy computation enabled, and verify that feature outputs are materialized into the AnnData object while intermediate computations remain as dask arrays before collection.
- Inputs:
  - AnnData object with spatial coordinates
  - Tissue image file (TIFF, Zarr, or equivalent)
- Expected outputs:
  - AnnData object with computed image features stored in obsm or var slots
  - Verification log or report showing dask array status before and after materialization
- Tools: Squidpy, scanpy, anndata, Python
- Landmark output files: image_container.pkl, feature_names.txt, dask_array_metadata.json, materialized_features.h5ad
- Primary expected artifact: `annotated_adata_with_image_features.h5ad`

## Final expected outputs

- `CSR sparse adjacency matrix (adj) of shape (n_obs, n_obs) with float32 dtype and binary indicator values` (type: file, tolerance: hash)
- `CSR sparse distance matrix (dst) of shape (n_obs, n_obs) with float64 dtype containing pairwise Euclidean distances` (type: file, tolerance: hash)
- `Validation report confirming matrix shape, sparsity consistency, diagonal correctness, and CSR format validity` (type: file, tolerance: hash)
- `Enrichment score matrix stored in AnnData.uns['nhood_enrichment']` (type: file, tolerance: hash)
- `NhoodEnrichmentResult object containing enrichment statistics` (type: file, tolerance: hash)
- `AnnData object with sepal results (gene rankings and spatial enrichment scores) stored in .var, .uns, or .obsm` (type: file, tolerance: hash)
- `Verification report listing field names, data types, array shapes, and confirmation of successful computation` (type: file, tolerance: hash)
- `AnnData object with computed image features stored in obsm or var slots` (type: file, tolerance: hash)
- `Verification log or report showing dask array status before and after materialization` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: open — validity-first.** The deterministic match-rubrics above are demoted to *informational*. The binding evaluator is **SCIENTIFIC_VALIDITY** (below). Any scientifically sound method that addresses the research question is valid, and novel findings or unexplored aspects can score positively — **different is not wrong**.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** implicit

- **Orchestration planning:** static

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_squidpy_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "CSR sparse adjacency matrix (adj) of shape (n_obs, n_obs) with float32 dtype and binary indicator values": "<locator>",
    "CSR sparse distance matrix (dst) of shape (n_obs, n_obs) with float64 dtype containing pairwise Euclidean distances": "<locator>",
    "Validation report confirming matrix shape, sparsity consistency, diagonal correctness, and CSR format validity": "<locator>",
    "Enrichment score matrix stored in AnnData.uns['nhood_enrichment']": "<locator>",
    "NhoodEnrichmentResult object containing enrichment statistics": "<locator>",
    "AnnData object with sepal results (gene rankings and spatial enrichment scores) stored in .var, .uns, or .obsm": "<locator>",
    "Verification report listing field names, data types, array shapes, and confirmation of successful computation": "<locator>",
    "AnnData object with computed image features stored in obsm or var slots": "<locator>",
    "Verification log or report showing dask array status before and after materialization": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
