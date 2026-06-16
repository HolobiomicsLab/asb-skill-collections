# SciTask Card: Reproduce differential expression results from tl.rank_genes_groups on the pbmc3k_processed dataset

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T17:50:38.861186+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_scanpy/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-analysis`, `statistical-analysis`, `benchmark-evaluation`
- DOI: `10.1186/s13059-017-1382-0`
- GitHub: `scverse/scanpy`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `transcriptomics`
- Subdomains: `rna-seq`, `differential-expression`
- Techniques: `dimensionality-reduction`, `clustering`, `batch-correction`, `normalization`, `statistical-analysis`

## Research Question
Does Scanpy's rank_genes_groups function with Wilcoxon test produce marker gene rankings that match expected documentation examples when applied to leiden-clustered pbmc3k data?

## Connected Finding
Scanpy is a scalable toolkit for analyzing single-cell gene expression data that includes differential expression testing capabilities.

## Task Description
Load the pre-processed pbmc3k_processed dataset from Scanpy, identify marker genes per leiden cluster using the Wilcoxon rank-sum test via tl.rank_genes_groups, and validate that the ranked output DataFrame contains expected top marker gene names and score ranges.

## Inputs
- Scanpy pbmc3k_processed pre-computed dataset

## Expected Outputs
- DataFrame of ranked marker genes per leiden cluster with gene names, log fold-change, and adjusted p-values
- Validation report confirming top marker gene names and score ranges match documentation

## Expected Output File

- `ranked_marker_genes.csv`

## Landmark Outputs

- `adata_with_wilcoxon_results.h5ad`
- `marker_genes_per_cluster_top5.csv`
- `validation_report.txt`

## Tools
- Scanpy
- anndata
- Python

## Skills
- differential-gene-expression-analysis
- marker-gene-identification-by-clustering
- statistical-ranking-wilcoxon-test
- anndata-object-manipulation
- single-cell-rna-seq-interpretation

## Workflow Description
1. Import Scanpy and load the pbmc3k_processed dataset using sc.datasets.pbmc3k_processed(). 2. Verify that leiden cluster assignments are present in adata.obs. 3. Run sc.tl.rank_genes_groups(adata, groupby='leiden', method='wilcoxon') to compute differential gene expression ranks across leiden clusters. 4. Extract the result DataFrame using sc.get.rank_genes_groups_df(adata) or access adata.uns['rank_genes_groups']. 5. Validate that the top-ranked genes per cluster match the documented marker gene names and that log-fold-change and p-value scores fall within expected ranges. 6. Create a summary table of the top 5 marker genes per cluster with their scores.

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
- No changelog found
- Expected top-gene names and score ranges are not specified in the provided discussion section

## Domain Knowledge
- Wilcoxon rank-sum test is a non-parametric test for differential gene expression that does not assume normality, making it suitable for count data.
- Leiden clustering produces community assignments stored in adata.obs; tl.rank_genes_groups requires a groupby column (here 'leiden') to stratify differential expression tests.
- The rank_genes_groups results are stored in adata.uns and include log fold-change (logfoldchanges), p-values (pvals), and adjusted p-values (pvals_adj); accessor functions like sc.get.rank_genes_groups_df reshape these into a user-friendly DataFrame.
- Top marker genes are those with highest absolute log fold-change and lowest adjusted p-values; thresholds vary by application but typically p_adj < 0.05 and |logFC| > 0.25.
- The pbmc3k_processed dataset is a reference peripheral blood mononuclear cell dataset with known cell-type annotation; documented top markers for each cluster are available in Scanpy tutorials and documentation examples.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: DataFrame of ranked marker genes per leiden cluster with gene names, log fold-change, and adjusted p-values, Validation report confirming top marker gene names and score ranges match documentation.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does Scanpy's rank_genes_groups function with Wilcoxon test produce marker gene rankings that match expected documentation examples when applied to leiden-clustered pbmc3k data?: 'It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Scanpy is a scalable toolkit for analyzing single-cell gene expression data that includes differential expression testing capabilities.: 'Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata. It includes preprocessing, visualization, clustering, trajectory inference and differential'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Scanpy pbmc3k_processed pre-computed dataset: 'datasets.pbmc3k_processed'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] DataFrame of ranked marker genes per leiden cluster with gene names, log fold-change, and adjusted p-values: 'get.rank_genes_groups_df'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Validation report confirming top marker gene names and score ranges match documentation: 'rank_genes_groups'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] Scanpy: 'Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] anndata: 'built jointly with anndata'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Python: 'Single-Cell Analysis in Python'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: '_No changelog found._'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] Expected top-gene names and score ranges are not specified in the provided discussion section: 'No substantive content provided in discussion section; only metadata and reference information'

## Evaluation Strategy
### Direct Checks
- verify file exists: pbmc3k_processed dataset accessible from Scanpy data module or deposited repository
- script_runs: Python script loading pbmc3k_processed dataset via scanpy.datasets or equivalent and executing tl.rank_genes_groups with Wilcoxon test on leiden cluster labels
- output_matches_reference: returned DataFrame column names include 'names', 'scores', or equivalent ranked gene identifiers and statistical values
- file_format_is: output is a pandas DataFrame or AnnData object with ranked genes structure
- value_in_range: top gene scores (p-values, log fold changes, or test statistics) fall within documented ranges for Wilcoxon test output, robust to minor numerical precision differences
- contains_substring: output DataFrame or figure legend contains at least 3 of the top marker gene names documented in Scanpy examples for pbmc3k leiden clusters

### Expert Review
- verify that top-ranked genes identified are biologically plausible marker genes for the reported leiden clusters (e.g., known markers for immune cell types in PBMC data)
- confirm that Wilcoxon test ranks and effect sizes align with expected differential expression patterns between clusters as reported in Scanpy documentation examples

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load pre-processed pbmc3k dataset with pre-computed leiden clusters
2. Apply Wilcoxon rank-sum test via tl.rank_genes_groups to identify differentially expressed genes per cluster
3. Extract ranked results using sc.get.rank_genes_groups_df or access adata.uns
4. Filter and sort by log fold-change and adjusted p-value to identify top marker genes
5. Compare against known reference marker gene names and score ranges from Scanpy documentation
6. Validation: Top marker gene names and p-value/fold-change ranges match documented examples
7. References: source article (DOI: 10.1186/s13059-017-1382-0)

## Workflow Ports

**Inputs:**

- `pbmc3k_processed` — Pre-processed PBMC 3K dataset with leiden clusters ← `task_001/processed_adata`

**Outputs:**

- `ranked_genes_df` — DataFrame of ranked marker genes per leiden cluster
- `validation_report` — Validation report of marker gene names and scores

**Used:** `urn:asb:port:task_001/processed_adata`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:scverse__scanpy`
- **Synthesized at:** 2026-06-15T17:57:56+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
