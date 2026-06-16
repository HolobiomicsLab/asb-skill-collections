# SciTask Card: Reconstruct the fgseaMultilevel adaptive multilevel MCMC P-value estimation component under eps=0 exact mode

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T19:18:01.563888+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_fgsea/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-analysis`, `statistical-analysis`, `benchmark-evaluation`
- GitHub: `alserglab/fgsea`
- Input from: `task_001`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `functional-genomics`, `multi-omics-integration`
- Techniques: `enrichment-analysis`, `pathway-analysis`, `statistical-analysis`, `false-discovery-rate-correction`

## Research Question
How does the adaptive multi-level split Monte-Carlo scheme in fgsea adjust P-value precision when the eps parameter is set to zero rather than using a default lower-bound threshold?

## Connected Finding
fgsea implements an adaptive multi-level split Monte-Carlo scheme that enables calculation of arbitrarily low GSEA P-values for gene set collections without a fixed lower-bound constraint.

## Task Description
Run fgsea with adaptive multi-level Monte Carlo scheme (eps=0) on examplePathways and exampleRanks, then compare P-value precision and magnitude against default eps=1e-10 lower-bound estimates to demonstrate improved statistical accuracy.

## Inputs
- examplePathways (list of gene sets from reactome.db)
- exampleRanks (preranked gene-level statistics)

## Expected Outputs
- fgsea results table (default eps=1e-10) with columns: pathway, pval, padj, ES, NES, size
- fgsea results table (eps=0) with same columns and refined P-values
- Comparison table showing pathway, pval_default, pval_eps0, pval_ratio, pval_difference for all pathways
- Visualization (scatter plot or histogram) of log10(pval_ratio) distribution across pathways

## Expected Output File

- `fgsea_pvalue_comparison.csv`

## Landmark Outputs

- `fgsea_default_eps1e10_results.csv`
- `fgsea_eps0_results.csv`
- `pvalue_improvement_summary.csv`
- `pvalue_ratio_distribution.png`

## Tools
- fgsea
- R
- data.table
- ggplot2

## Skills
- gene-set-enrichment-analysis-preranked-gsea
- monte-carlo-p-value-estimation-adaptive
- statistical-precision-comparison-ranked-outputs
- pathway-enrichment-score-interpretation
- genomic-database-identifier-mapping

## Workflow Description
1. Load examplePathways and exampleRanks datasets, set random seed for reproducibility. 2. Run fgsea with default eps=1e-10 parameter and record enrichment scores, raw P-values, and adjusted P-values for all pathways. 3. Run fgsea again with eps=0 to disable the lower-bound estimate and enable adaptive multi-level split Monte Carlo refinement. 4. Construct comparison table joining results from both runs by pathway identifier, computing P-value differences and fold-change ratios. 5. Visualize distribution of P-value changes (log-scale) and identify pathways with greatest precision improvement. 6. Validate that eps=0 run completes without numerical errors and produces valid P-value rankings consistent with default run.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/geseca-spatial-top.png` | figure | False |
| `figures/geseca-vignette-score-toy-example.png` | figure | False |
| `paper.md` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| geo_series | `GSE200250` | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200250 | sider a time course data of Th2 activation from the dataset GSE200250.  First, let prepare the dataset. We load it from Gene Expr |
| geo_series | `GSE116240` | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240 | ges(library(Seurat)) ```  As an example dataset we will use GSE116240 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE1162 |
| geo_series | `GSE14308` | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE14308 | exampleExpressionMatrix` - numeric expression matrix of the GSE14308 dataset. Rows correspond to genes (ENTREZID is used as iden |

## Missing Information
- No changelog or version history available to track changes to fgsea package, affecting reproducibility of exact algorithm implementation state at synthesis date

## Domain Knowledge
- fgsea's adaptive multi-level split Monte Carlo scheme refines P-value estimates by iteratively sampling gene permutations at multiple resolution levels, allowing convergence to arbitrarily small P-values when eps=0 versus the default lower bound of 1e-10.
- The eps parameter controls the P-value lower bound: eps=1e-10 (default) stops refinement at 10^-10; eps=0.0 disables the bound and enables full adaptive refinement until statistical convergence.
- Preranked GSEA ranks genes by a continuous statistic (e.g. t-statistic, log fold-change) without requiring an explicit phenotype contrast, making enrichment scores and P-values sensitive to the magnitude and ordering of gene statistics.
- Enrichment score (ES) measures the maximum signed deviation of cumulative statistic sum from zero; normalized ES (NES) adjusts for gene set size to enable cross-set comparison.
- Multiple testing correction via adjusted P-values (padj) is essential when testing hundreds of pathways; comparing adjusted P-values between eps=1e-10 and eps=0 validates that precision improvement does not inflate false discovery.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: data.table, ggplot2, fgsea results table (default eps=1e-10) with columns: pathway, pval, padj, ES, NES, size, fgsea results table (eps=0) with same columns and refined P-values, Comparison table showing pathway, pval_default, pval_eps0, pval_ratio, pval_difference for all pathways, Visualization (scatter plot or histogram) of log10(pval_ratio) distribution across pathways.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does the adaptive multi-level split Monte-Carlo scheme in fgsea adjust P-value precision when the eps parameter is set to zero rather than using a default lower-bound threshold?: 'P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] fgsea implements an adaptive multi-level split Monte-Carlo scheme that enables calculation of arbitrarily low GSEA P-values for gene set collections without a fixed lower-bound constraint.: 'This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets. P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] examplePathways (list of gene sets from reactome.db): 'data(examplePathways)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] exampleRanks (preranked gene-level statistics): 'data(exampleRanks)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] fgsea results table (default eps=1e-10) with columns: pathway, pval, padj, ES, NES, size: 'head(fgseaRes[order(pval), ])'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] fgsea results table (eps=0) with same columns and refined P-values: 'fgseaRes <- fgsea(pathways = examplePathways, stats = exampleRanks, eps = 0.0, minSize = 15, maxSize = 500)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Comparison table showing pathway, pval_default, pval_eps0, pval_ratio, pval_difference for all pathways: 'fgsea has a default lower bound `eps=1e-10` for estimating P-values. If you need to estimate P-value more accurately, you can set the `eps` argument to zero'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Visualization (scatter plot or histogram) of log10(pval_ratio) distribution across pathways: 'This package allows to quickly and accurately calculate arbitrarily low GSEA P-values'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] fgsea: '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] R: '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] data.table: 'library(data.table)'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] ggplot2: 'library(ggplot2)'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history available to track changes to fgsea package, affecting reproducibility of exact algorithm implementation state at synthesis date: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists in fgsea package: examplePathways (R data object)
- verify file exists in fgsea package: exampleRanks (R data object)
- script_runs: load examplePathways and exampleRanks in R and execute fgsea(examplePathways, exampleRanks, eps=0) without errors
- script_runs: load examplePathways and exampleRanks in R and execute fgsea(examplePathways, exampleRanks, eps=1e-10) without errors
- output_matches_reference: fgsea with eps=0 returns data.frame or list with named column 'pval' (or 'padj') for each pathway
- output_matches_reference: fgsea with eps=1e-10 returns data.frame or list with named column 'pval' (or 'padj') for each pathway
- value_in_range: median or mean P-value from eps=0 run is strictly less than median or mean P-value from eps=1e-10 run across same pathways (robust to ordering; parameter-sensitive to choice of aggregation statistic)
- row_count_equals: both fgsea runs return results for identical set of pathways (same number of rows, same pathway names)

### Expert Review
- Assess whether reported P-values from eps=0 run are substantively more precise (lower variance, finer granularity) than eps=1e-10 lower-bound estimates, as claimed for adaptive multi-level split scheme
- Evaluate whether precision improvement is consistent across pathways of different sizes and effect magnitudes, or only in specific subsets
- Judge whether the comparison demonstrates the correctness and practical benefit of the adaptive multi-level split Monte Carlo implementation versus the fixed eps truncation

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load example gene set collection (examplePathways) and preranked gene statistics (exampleRanks) into R environment with reproducible random seed.
2. Execute fgsea function with default eps=1e-10 lower bound, recording enrichment scores, raw P-values, adjusted P-values, and effect sizes (ES, NES) for all pathways.
3. Re-execute fgsea with eps=0 to activate unrestricted adaptive multi-level Monte Carlo P-value refinement for the same input data.
4. Construct merged comparison table indexed by pathway, computing pairwise differences and log-scale ratios of P-values from both runs.
5. Visualize distribution of P-value improvements across pathways and verify ranking consistency between methods.
6. Validation: confirm that eps=0 execution completes without error, produces valid numeric P-values for all pathways, and demonstrates lower (more precise) P-value estimates for top-ranked pathways relative to default run.
7. References: GSE200250 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200250); GSE116240 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240); GSE14308 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE14308)

## Workflow Ports

**Inputs:**

- `examplePathways` — Gene set list from reactome ← `task_001/fgsea_result_table`
- `exampleRanks` — Preranked gene statistics

**Outputs:**

- `fgsea_default_results` — FGSEA results with default eps=1e-10
- `fgsea_eps0_results` — FGSEA results with eps=0
- `pvalue_comparison_table` — Side-by-side P-value comparison by pathway
- `precision_improvement_plot` — Visualization of P-value refinement magnitude

**Used:** `urn:asb:port:task_001/fgsea_result_table`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:alserglab__fgsea`
- **Synthesized at:** 2026-06-15T19:26:40+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
