# Workflow Challenge: `coll_scanpy_workflow`


> Scanpy is a scalable Python toolkit for analyzing single-cell gene expression data, integrating preprocessing, visualization, clustering, trajectory inference, and differential expression testing with the anndata data structure.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Scanpy provides a comprehensive set of computational methods for single-cell analysis, including preprocessing functions for normalization and quality control, graph-based clustering via the Leiden algorithm, embedding techniques such as UMAP and t-SNE, trajectory inference through PAGA, and differential expression testing via rank_genes_groups. The toolkit is designed to handle large datasets efficiently, demonstrated through reproduction of standard workflows on benchmark datasets including PBMC3k and paul15 hematopoiesis data. Testing is performed using pytest with Hatch environment configuration, and the implementation leverages the anndata data structure for organizing and annotating single-cell observations and gene expression matrices.

## Research questions

- Does Scanpy successfully execute a complete single-cell analysis workflow including preprocessing, clustering, and embedding on standard datasets?
- Can preprocessing functions in the scanpy pp module operate on Dask-backed AnnData objects without eagerly loading the entire expression matrix into memory?
- Does Scanpy's rank_genes_groups function with Wilcoxon test produce marker gene rankings that match expected documentation examples when applied to leiden-clustered pbmc3k data?
- How does the PAGA (Partition-based Graph Abstraction) algorithm construct a connectivity matrix from clustered single-cell data, and what is the expected dimensionality of the resulting abstraction?
- Does the Scanpy test suite execute without failures when invoked via the Hatch environment using the standard test command?

## Methods overview

Load pbmc3k dataset as an AnnData object containing ~3,000 cells and ~13,000 genes. Apply depth normalization followed by log1p transformation to stabilize variance and scale expression values. Select ~2,000 highly variable genes to reduce noise and focus on genes with biological signal. Scale gene expression to unit variance and compute PCA for dimensionality reduction. Construct k-nearest neighbor graph using Euclidean distance in PCA space (n_neighbors=15). Detect cell clusters using the Leiden community-detection algorithm on the neighbor graph. Embed cells in 2-D space using UMAP for visualization, preserving local and global structure. Validation: Verify that adata.obs contains 'leiden' column with ≥2 unique cluster labels and adata.obsm contains 'X_umap' with shape (n_cells, 2). References: source article (DOI: 10.1186/s13059-017-1382-0) Load or construct an AnnData object with Dask-backed expression matrix. Execute a pp module function with Dask-compatible parameters. Verify lazy evaluation by confirming operation completes without materializing full matrix. Validate AnnData structure: obs/var dimensions, metadata integrity, and array type consistency. Validation: operation completes successfully with Dask array remaining un-materialized and obs/var dimensions matching expected cell and gene counts. References: source article (DOI: 10.1186/s13059-017-1382-0) Load pre-processed pbmc3k dataset with pre-computed leiden clusters Apply Wilcoxon rank-sum test via tl.rank_genes_groups to identify differentially expressed genes per cluster Extract ranked results using sc.get.rank_genes_groups_df or access adata.uns Filter and sort by log fold-change and adjusted p-value to identify top marker genes Compare against known reference marker gene names and score ranges from Scanpy documentation Validation: Top marker gene names and p-value/fold-change ranges match documented examples References: source article (DOI: 10.1186/s13059-017-1382-0) Load paul15 dataset into an AnnData object using Scanpy's dataset module. Preprocess by computing k-nearest neighbors graph to establish cell–cell connectivity. Partition cells into clusters using Leiden algorithm to define cluster-level groupings. Apply PAGA to abstract the neighborhood graph into a coarse-grained partition-based graph where nodes are clusters and edges represent inter-cluster connectivity. Validation: confirm that adata.uns['paga'] key exists, contains a 'connectivities' sparse matrix, and matrix dimensions equal (n_unique_clusters, n_unique_clusters). References: source article (DOI: 10.1186/s13059-017-1382-0) Clone the scverse/scanpy repository locally and navigate to the repository root directory. Create and activate the Hatch test environment by invoking `hatch test`, which reads hatch.toml and installs dependencies. Execute the full pytest test suite, which reads pytest configuration and runs all test modules in scanpy/tests with matplotlib plot comparison setup active. Capture and parse the test execution output to confirm exit code is 0 and no non-skipped test failures are reported. Validation: confirm test run exits with code 0 and the summary line reports zero failed tests, matching the CI badge passing state reported by the repository. References: source article (DOI: 10.1186/s13059-017-1382-0)

**Domain:** transcriptomics

**Techniques:** dimensionality-reduction, clustering, batch-correction, normalization, statistical-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata. [evidence_step: task_001] _[grounded: scanpy_system]_
- **(finding)** Scanpy includes preprocessing, visualization, clustering, trajectory inference and differential expression testing. _[grounded: scanpy_system]_
- **(finding)** Scanpy is built in Python. _[grounded: scanpy_system]_
- **(finding)** Before filing an issue, contributors should search the repository to see if someone has already reported the same issue.
- **(finding)** A minimal complete verifiable example should be provided for any bug report.
- **(finding)** Environment information in Scanpy can be obtained via sc.logging.print_versions(). _[grounded: scanpy_system]_
- **(finding)** Code contributions to Scanpy should follow the contribution guide in the main documentation. _[grounded: scanpy_system]_
- **(finding)** The AnnData class is reexported from the anndata module in Scanpy. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides a Neighbors class to represent data as a neighborhood structure, usually a knn graph. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides dataset loading functions including pbmc3k, pbmc68k_reduced, and paul15. _[grounded: scanpy_system]_
- **(finding)** The pp.subsample, tl.louvain, and logging.print_versions functions are deprecated in Scanpy. _[grounded: scanpy_system]_
- **(finding)** Scanpy has experimental preprocessing methods including normalize_pearson_residuals and highly_variable_genes. _[grounded: scanpy_system]_
- **(finding)** The sc.get module provides convenience functions for getting values back in useful formats.
- **(finding)** Scanpy is imported as sc using the command import scanpy as sc. _[grounded: scanpy_system]_
- **(finding)** Additional functionality in Scanpy is available across the broader scverse ecosystem. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides read functions for common file formats including read_10x_h5, read_10x_mtx, and read_visium. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides metrics functions including modularity, confusion_matrix, gearys_c, and morans_i. _[grounded: scanpy_system]_
- **(finding)** The plotting module scanpy.pl largely parallels the tl.* and some of the pp.* functions. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides generic plotting functions including scatter, heatmap, dotplot, violin, and matrixplot. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides plotting classes DotPlot, MatrixPlot, and StackedViolin for fine tuning of visual parameters. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides preprocessing visualization functions for quality control including highest_expr_genes and highly_variable_genes. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides PCA plotting functions including pca, pca_loadings, pca_variance_ratio, and pca_overview. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides embedding plotting functions including tsne, umap, diffmap, draw_graph, spatial, and embedding. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides trajectory and clustering visualization functions including dpt_groups_pseudotime, dpt_timeseries, paga, paga_path, and paga_compare. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides marker gene visualization functions including rank_genes_groups, rank_genes_groups_violin, rank_genes_groups_heatmap, and rank_genes_groups_dotplot. _[grounded: scanpy_system]_
- **(finding)** Scanpy preprocessing includes filtering of highly-variable genes, batch-effect correction, per-cell normalization, and preprocessing recipes. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides basic preprocessing functions including calculate_qc_metrics, filter_cells, filter_genes, highly_variable_genes, log1p, pca, and normalize_total. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides preprocessing recipes including recipe_zheng17, recipe_weinreb17, and recipe_seurat. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides data integration functions including combat and harmony_integrate. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides doublet detection functions including scrublet and scrublet_simulate_doublets. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides a neighbors preprocessing function. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides query functions including biomart_annotations, gene_coordinates, mitochondrial_genes, and enrich. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides a set_figure_params function for setting default matplotlib.rcParams. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides a settings object for configuring Scanpy. _[grounded: scanpy_system]_
- **(finding)** Scanpy settings include Preset and Verbosity enumerations. _[grounded: scanpy_system]_
- **(finding)** Scanpy settings include figdir, cachedir, datasetdir, file_format_figs, and file_format_data for IO. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides a logging.print_header function to print versions of packages that might influence numerical results. _[grounded: scanpy_system]_
- **(finding)** Scanpy tools include embedding methods such as pca, tsne, umap, draw_graph, and diffmap. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides clustering and trajectory inference tools including leiden, dendrogram, dpt, and paga. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides a data integration tool called tl.ingest. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides marker gene tools including rank_genes_groups, filter_rank_genes_groups, and marker_gene_overlap. _[grounded: scanpy_system]_
- **(finding)** Scanpy provides gene scoring tools including score_genes and score_genes_cell_cycle. _[grounded: scanpy_system]_
- **(finding)** Scanpy is a community driven project embedded in the scverse consortium. _[grounded: scanpy_system]_
- **(finding)** The scverse Discourse forum is the place to ask usage questions and for longer form discussions around the project.
- **(finding)** The Scanpy and anndata issue trackers are for reports and discussion of bug reports, documentation issues, and feature requests. _[grounded: scanpy_system]_
- **(finding)** Philipp Angerer is the lead developer of Scanpy since 2023. _[grounded: scanpy_system]_
- **(finding)** Code contributions to Scanpy will be formatted and style checked using Ruff. _[grounded: scanpy_system]_
- **(finding)** To build Scanpy docs, run hatch run docs:build. _[grounded: scanpy_system]_
- **(finding)** Scanpy uses the numpydoc style for writing docstrings. _[grounded: scanpy_system]_
- **(finding)** Scanpy uses pytest for testing. _[grounded: scanpy_system]_
- **(finding)** To run Scanpy tests, run hatch test. _[grounded: scanpy_system]_
- **(finding)** Scanpy follows semantic versioning with major.minor.point version numbering. _[grounded: scanpy_system]_
- **(finding)** Point releases in Scanpy should have no changes beyond bug fixes. _[grounded: scanpy_system]_
- **(finding)** Minor releases in Scanpy can include new features. _[grounded: scanpy_system]_
- **(finding)** Major releases in Scanpy can break old APIs. _[grounded: scanpy_system]_
- **(finding)** Scanpy external module includes exporting functions spring_project and cellbrowser. _[grounded: scanpy_system]_
- **(finding)** Scanpy is no longer accepting new tools into scanpy.external. _[grounded: scanpy_system]_
- **(finding)** Scanpy external plotting module provides phate, trimap, sam, and wishbone_marker_trajectory functions. _[grounded: scanpy_system]_
- **(finding)** Scanpy external preprocessing module provides data integration functions including bbknn, mnn_correct, and scanorama_integrate. _[grounded: scanpy_system]_
- **(finding)** Scanpy can be installed using pip with the command pip install 'scanpy[leiden]'. _[grounded: scanpy_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- virtual environments or conda environments as alternatives to Hatch for development environments

## Steps

### Step `task_001`
- Title: Reproduce the basic clustering and UMAP visualization pipeline on the PBMC3k tutorial dataset
- Task kind: `reproduction`
- Task: Execute the canonical Scanpy tutorial workflow on the pbmc3k dataset: load data, apply standard preprocessing (normalize, log-transform, identify highly variable genes, scale), compute k-nearest neighbors, run Leiden clustering, and compute UMAP embedding. Verify the output AnnData object contains expected cluster annotations and 2-D UMAP coordinates.
- Inputs:
  - pbmc3k dataset from Scanpy built-in datasets
- Expected outputs:
  - AnnData object with leiden cluster annotations in adata.obs['leiden']
  - 2-D UMAP embedding stored in adata.obsm['X_umap']
  - Highly variable genes flagged in adata.var['highly_variable']
- Tools: Scanpy, anndata, Python
- Landmark output files: pbmc3k_normalized.h5ad, pbmc3k_hvg_selected.h5ad, pbmc3k_scaled_pca.h5ad, pbmc3k_neighbors_computed.h5ad, pbmc3k_leiden_clustered.h5ad, pbmc3k_umap_embedded.h5ad
- Primary expected artifact: `pbmc3k_processed.h5ad`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the Dask Array support layer for pp preprocessing functions
- Task kind: `component_reconstruction`
- Task: Execute a Scanpy preprocessing function (pp.normalize_total or pp.pca) on a Dask-backed AnnData object and verify the operation completes without eagerly materializing the full data matrix, confirming valid output structure.
- Inputs:
  - AnnData object with Dask-backed expression matrix (dask.array.Array in adata.X)
  - Scanpy source code and API reference (pp module functions)
- Expected outputs:
  - AnnData object with processed expression data, retaining Dask-backed or sparse structure without full materialization
  - Verification report confirming obs/var structure integrity and memory efficiency
- Tools: Scanpy, anndata, Python, pytest, Hatch
- Landmark output files: dask_adata_input.h5ad, normalized_or_pca_adata.h5ad, memory_profile.log
- Primary expected artifact: `dask_preprocessing_verification_report.txt`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce differential expression results from tl.rank_genes_groups on the pbmc3k_processed dataset
- Task kind: `reproduction`
- Task: Load the pre-processed pbmc3k_processed dataset from Scanpy, identify marker genes per leiden cluster using the Wilcoxon rank-sum test via tl.rank_genes_groups, and validate that the ranked output DataFrame contains expected top marker gene names and score ranges.
- Inputs:
  - Scanpy pbmc3k_processed pre-computed dataset
- Expected outputs:
  - DataFrame of ranked marker genes per leiden cluster with gene names, log fold-change, and adjusted p-values
  - Validation report confirming top marker gene names and score ranges match documentation
- Tools: Scanpy, anndata, Python
- Landmark output files: adata_with_wilcoxon_results.h5ad, marker_genes_per_cluster_top5.csv, validation_report.txt
- Primary expected artifact: `ranked_marker_genes.csv`

### Step `task_004`
- Title: Reconstruct the PAGA trajectory graph on the paul15 hematopoiesis dataset
- Task kind: `component_reconstruction`
- Task: Load the paul15 dataset, compute Leiden clustering as a prerequisite, execute PAGA (partition-based graph abstraction) to construct a coarse-grained neighborhood graph, and verify that the resulting AnnData object contains a 'paga' key in uns with a connectivity matrix of shape (n_clusters, n_clusters).
- Inputs:
  - paul15 dataset from scanpy.datasets
- Expected outputs:
  - AnnData object with 'paga' key in uns containing partition-based graph abstraction results, including a connectivity matrix of shape (n_clusters, n_clusters)
- Tools: Scanpy, anndata, Python
- Landmark output files: adata_with_leiden.h5ad, adata_with_paga.h5ad

### Step `task_005`
- Title: Reproduce the CI workflow by running the pytest test suite via Hatch
- Task kind: `reproduction`
- Task: Execute the Scanpy pytest test suite using the Hatch environment to verify all tests pass with zero non-skipped failures, confirming the codebase meets the CI passing state.
- Inputs:
  - Scanpy repository source code (scverse/scanpy cloned locally)
  - hatch.toml configuration file with predefined test environment
- Expected outputs:
  - Test execution report with exit code 0 and zero non-skipped test failures
  - Console output log from pytest showing all test results and summary statistics
- Tools: Scanpy, pytest, Hatch, git, matplotlib
- Landmark output files: pytest_run.log, test_summary.txt, failed_tests_report.txt

## Final expected outputs

- `AnnData object with processed expression data, retaining Dask-backed or sparse structure without full materialization` (type: file, tolerance: hash)
- `Verification report confirming obs/var structure integrity and memory efficiency` (type: file, tolerance: hash)
- `DataFrame of ranked marker genes per leiden cluster with gene names, log fold-change, and adjusted p-values` (type: file, tolerance: hash)
- `Validation report confirming top marker gene names and score ranges match documentation` (type: file, tolerance: hash)
- `AnnData object with 'paga' key in uns containing partition-based graph abstraction results, including a connectivity matrix of shape (n_clusters, n_clusters)` (type: file, tolerance: hash)
- `Test execution report with exit code 0 and zero non-skipped test failures` (type: file, tolerance: hash)
- `Console output log from pytest showing all test results and summary statistics` (type: file, tolerance: hash)

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
  "workflow_id": "coll_scanpy_workflow",
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
    "AnnData object with processed expression data, retaining Dask-backed or sparse structure without full materialization": "<locator>",
    "Verification report confirming obs/var structure integrity and memory efficiency": "<locator>",
    "DataFrame of ranked marker genes per leiden cluster with gene names, log fold-change, and adjusted p-values": "<locator>",
    "Validation report confirming top marker gene names and score ranges match documentation": "<locator>",
    "AnnData object with 'paga' key in uns containing partition-based graph abstraction results, including a connectivity matrix of shape (n_clusters, n_clusters)": "<locator>",
    "Test execution report with exit code 0 and zero non-skipped test failures": "<locator>",
    "Console output log from pytest showing all test results and summary statistics": "<locator>"
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
