# SciTask Card: Reproduce limma linear-model fitting on a public microarray dataset via lmFit

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T19:03:19.044971+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_limmavoom/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `statistical-analysis`, `benchmark-evaluation`
- DOI: `10.1093/nar/gkv007`
- GitHub: `bioc/limma`
- Input from: `task_002`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `transcriptomics`
- Subdomains: `differential-expression`, `rna-seq`
- Techniques: `statistical-analysis`, `normalization`, `false-discovery-rate-correction`

## Research Question
Does prepending edgeR's calcNormFactors normalization to the limma voom pipeline alter the ranked list of differentially expressed genes compared to the standard limma-only workflow?

## Connected Finding
Unable to extract a direct finding from the provided section text.

## Task Description
Extend the standard limma RNA-seq pipeline by prepending edgeR's calcNormFactors function to compute TMM normalization factors, pass normalized library sizes to voom, and complete the differential expression workflow. Compare the resulting top table of differentially expressed genes against a limma-only baseline using the same public RNA-seq dataset.

## Inputs
- Raw RNA-seq read count matrix and sample metadata from a public RNA-seq dataset (e.g., GEO, ArrayExpress, or SRA accession); must include treatment group assignments and confounding variables for design matrix construction.

## Expected Outputs
- Top table of differentially expressed genes from TMM-voom-limma pipeline containing gene identifiers, log-fold-changes, average log-expression, t-statistics, p-values, and adjusted p-values (FDR).
- Top table of differentially expressed genes from limma-only baseline (without TMM normalization pre-processing) in identical format for direct comparison.
- Comparison summary table or figure showing overlap of significantly differentially expressed genes (FDR < 0.05) between TMM-voom and limma-only methods, including count of concordant/discordant calls and magnitude of log-fold-change shifts.

## Expected Output File

- `method_comparison_summary.csv`

## Landmark Outputs

- `tmm_normalized_counts.csv`
- `voom_weights.csv`
- `tmm_voom_top_table.csv`
- `limma_only_top_table.csv`
- `method_comparison_overlap.png`

## Tools
- edgeR
- limma
- R
- voom

## Skills
- rna-seq-count-normalization-tmm
- gene-expression-linear-modeling
- differential-expression-empirical-bayes-moderation
- precision-weight-calculation-rna-seq
- method-comparison-differential-calls
- design-matrix-construction-experiments

## Workflow Description
1. Load raw RNA-seq read counts and sample metadata from a public dataset (e.g., GEO accession). 2. Create a DGEList object in edgeR and apply calcNormFactors with TMM method to compute normalization factors and scale library sizes. 3. Extract the TMM-normalized library sizes and pass them to voom along with the design matrix to compute precision weights accounting for mean-variance relationship. 4. Fit a linear model using lmFit on the voom-transformed expression matrix with the design matrix. 5. Apply empirical Bayes moderation using eBayes to stabilize variance estimates across genes. 6. Extract the top differentially expressed genes using topTable with adjusted p-value threshold (e.g., FDR < 0.05). 7. Compare gene rankings, log-fold-changes, and adjusted p-values between the TMM-voom pipeline and limma-only baseline to quantify changes in differential expression calls.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history is documented
- No specific public RNA-seq dataset is identified or referenced in the provided section text
- No prior benchmarking or empirical comparison of edgeR-prepended vs. standard limma workflows is cited

## Domain Knowledge
- TMM (trimmed mean of M-values) normalization removes composition bias in RNA-seq by adjusting library sizes based on gene-wise log-fold-changes; limma-voom accepts pre-computed normalized library sizes to improve precision weight estimation.
- Empirical Bayes moderation in limma borrows information across genes to stabilize variance estimates, which becomes especially important when sample sizes are small or gene-wise variances are heterogeneous.
- Voom transforms RNA-seq counts to log2-counts-per-million and computes precision weights that account for the mean-variance relationship, converting count data to a form suitable for linear modeling.
- Differential expression results (gene rankings, log-fold-changes, p-values) can shift between pipelines if normalization assumptions differ; comparison must account for both statistical significance (adjusted p-value) and effect size (log-fold-change magnitude).
- FDR-adjusted p-values (e.g., Benjamini-Hochberg correction) control false discovery rate across multiple gene tests; standard threshold is FDR < 0.05 for significance in exploratory differential expression studies.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Top table of differentially expressed genes from limma-only baseline (without TMM normalization pre-processing) in identical format for direct comparison., Comparison summary table or figure showing overlap of significantly differentially expressed genes (FDR < 0.05) between TMM-voom and limma-only methods, including count of concordant/discordant calls and magnitude of log-fold-change shifts..

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [other] Does prepending edgeR's calcNormFactors normalization to the limma voom pipeline alter the ranked list of differentially expressed genes compared to the standard limma-only workflow?: 'No verbatim evidence available in provided text'
- `ev_002` from `agent2_synthesis` (agent2_traced): [other] Unable to extract a direct finding from the provided section text.: 'No examples found.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Raw RNA-seq read count matrix and sample metadata from a public RNA-seq dataset (e.g., GEO, ArrayExpress, or SRA accession); must include treatment group assignments and confounding variables for design matrix construction.: 'The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Top table of differentially expressed genes from TMM-voom-limma pipeline containing gene identifiers, log-fold-changes, average log-expression, t-statistics, p-values, and adjusted p-values (FDR).: 'linear models for analysing designed experiments and the assessment of differential expression'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Top table of differentially expressed genes from limma-only baseline (without TMM normalization pre-processing) in identical format for direct comparison.: 'the assessment of differential expression'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Comparison summary table or figure showing overlap of significantly differentially expressed genes (FDR < 0.05) between TMM-voom and limma-only methods, including count of concordant/discordant calls and magnitude of log-fold-change shifts.: 'Limma is an R package for the analysis of gene expression data'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] edgeR: 'calcNormFactors [TMM normalization]'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] limma: 'Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] R: 'Limma is an R package'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] voom: 'Voom: precision weights unlock linear model analysis tools for RNA-seq read counts'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history is documented: '_No changelog found._'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No specific public RNA-seq dataset is identified or referenced in the provided section text: '[entire section provides only metadata; no dataset specification appears]'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No prior benchmarking or empirical comparison of edgeR-prepended vs. standard limma workflows is cited: '[section text does not contain any such comparison]'

## Evaluation Strategy
### Direct Checks
- verify that edgeR package is available in the computational environment (script_runs check: attempt to load edgeR library)
- verify that limma package is available and loadable from github:bioc__limma (script_runs check: load limma library)
- verify that a public RNA-seq dataset can be retrieved and loaded (file_exists check for dataset artifact or accession identifier)
- verify that calcNormFactors function from edgeR executes without error on the input dataset (script_runs check)
- verify that voom function accepts TMM-normalized library sizes as input and produces a voom object (script_runs check: output_matches_reference structure)
- verify that the extended pipeline (edgeR calcNormFactors → voom → limma workflow) completes and produces a top-table output file (file_exists and format_is checks)
- verify that the baseline limma-only pipeline (without edgeR prepend) also completes on the same dataset and produces a comparable top-table (file_exists and format_is checks)
- verify that both top-tables have identical or near-identical structure (row_count_equals and field_present checks for gene identifiers, log-fold-change, adjusted p-values)
- robust comparison: calculate rank correlation (Spearman or similar) between log-fold-change columns of extended vs. baseline pipelines, value in range [−1, 1]

### Expert Review
- Assess whether observed differences in top-table rankings (gene order, adjusted p-value thresholds) are biologically meaningful or expected given TMM normalization theory
- Evaluate whether the choice of public RNA-seq dataset is representative (e.g., sample size, sequencing depth, biological context) for a fair comparison
- Judge whether the comparison accounts for known behavior of TMM normalization vs. other limma defaults in this context
- Review whether the prepended edgeR step introduces any violations of limma's statistical assumptions or downstream function requirements

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load raw RNA-seq read counts and metadata; construct design matrix from experimental annotations.
2. Apply edgeR's calcNormFactors with TMM method to compute library size scaling factors accounting for composition bias.
3. Execute voom transformation using TMM-normalized library sizes to calculate precision weights for each observation.
4. Fit linear models using lmFit, then apply empirical Bayes variance moderation with eBayes.
5. Extract top differentially expressed genes and quantify concordance with limma-only baseline.
6. Validation: Confirm that TMM-voom and limma-only outputs both pass Benjamini-Hochberg FDR correction at threshold 0.05; report overlap of significant genes and magnitude of log-fold-change differences between methods.
7. References: source article (DOI: 10.1093/nar/gkv007)

## Workflow Ports

**Inputs:**

- `rna_seq_counts` — Raw RNA-seq read count matrix and sample metadata ← `task_002/fitted_model`

**Outputs:**

- `tmm_voom_top_table` — Top table from TMM-voom-limma differential expression analysis
- `limma_only_top_table` — Top table from limma-only baseline differential expression analysis
- `method_comparison` — Comparison summary of gene rankings and significance between methods

**Used:** `urn:asb:port:task_002/fitted_model`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:bioc__limma`
- **Synthesized at:** 2026-06-15T19:07:10+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
