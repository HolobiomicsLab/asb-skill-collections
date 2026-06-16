# SciTask Card: Reproduce GESECA PCA-reduced analysis on GSE200250 and verify score similarity to full-matrix results

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T19:18:01.563888+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_fgsea/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `statistical-analysis`, `visualization`
- GitHub: `alserglab/fgsea`
- Input from: `task_002`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `functional-genomics`, `multi-omics-integration`
- Techniques: `enrichment-analysis`, `pathway-analysis`, `statistical-analysis`, `false-discovery-rate-correction`

## Research Question
Does dimensionality reduction via PCA to 10 dimensions preserve the pathway enrichment results (pathway scores and p-values) obtained from geseca() analysis on the full-dimensional GSE200250 expression matrix?

## Connected Finding
fgsea enables fast and accurate calculation of GSEA P-values for gene set collections, supporting the feasibility of comparing pathway enrichment results across different input dimensionalities.

## Task Description
Apply principal component analysis (PCA) reduction to 10 dimensions on the GSE200250 expression matrix, re-run GESECA analysis on the reduced matrix with center=FALSE, and verify that resulting pathway scores and p-values remain similar to those from the full-matrix analysis.

## Inputs
- GSE200250 microarray dataset from GEO (Th2 activation time course)
- Hallmark gene set collection from MSigDB

## Expected Outputs
- GESECA results table from full matrix analysis (pathway, score, pval, padj, size)
- GESECA results table from reduced (10-PC) matrix analysis (pathway, score, pval, padj, size)
- Scatterplot comparing log10(pval) from full vs reduced matrix, showing Pearson correlation ≥0.95

## Expected Output File

- `pval_comparison_full_vs_reduced.png`

## Landmark Outputs

- `normalized_expression_matrix.rds`
- `pca_reduced_matrix_10d.rds`
- `geseca_full_results.tsv`
- `geseca_reduced_results.tsv`

## Tools
- GEOquery
- limma
- fgsea
- R
- ggplot2
- data.table
- msigdbr

## Skills
- microarray-expression-normalization-log-quantile
- gene-filtering-by-expression-level
- principal-component-analysis-dimensionality-reduction
- gene-set-enrichment-scoring-coregulation
- pathway-activity-correlation-analysis
- statistical-comparison-p-value-conservation

## Workflow Description
1. Load GSE200250 expression matrix from GEO, apply log2 and quantile normalization using limma::normalizeBetweenArrays, filter to top 12,000 genes by mean expression, and subset to Th2 time-course samples. 2. Center gene expression matrix (rows) to zero mean using scale(). 3. Perform standard PCA using base::prcomp() with center=FALSE and extract the first 10 principal components corresponding to linear combinations of cells. 4. Run geseca() on the reduced matrix with minSize=15, maxSize=500, center=FALSE, and capture pathway scores and p-values. 5. Compare gesture results between full and reduced matrices by computing correlation of log10-transformed p-values and plotting log10(pval) from full matrix versus reduced matrix using ggplot2. 6. Validation: confirm that Pearson correlation of log10 p-values between full and reduced results is ≥0.95, indicating negligible information loss from dimensionality reduction.

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
- No changelog or version history available for the fgsea package
- Specific reference implementation or expected outputs for the full-matrix geseca() run on GSE200250 are not provided

## Domain Knowledge
- GESECA score reflects summed squared column sums of the row-centered gene expression submatrix, analogous to explained variance in PCA; higher scores indicate stronger gene co-regulation.
- Row-centered expression matrix is required for GESECA to measure correlation structure; center=FALSE flag is used when the matrix has been pre-centered externally (e.g., after PCA transformation).
- Reverse PCA (rev.pca=TRUE) in Seurat and manual PCA extraction computes principal components as linear combinations of cells (not genes), yielding a feature-loadings matrix where rows are genes and columns are PCs suitable for GESECA input.
- P-value similarity between full and reduced matrices validates that dimensionality reduction preserves pathway co-regulation patterns; high correlation (≥0.95 on log10 scale) confirms 10 PCs capture sufficient biological signal.
- Gene set size filtering (minSize=15, maxSize=500) removes very small pathways prone to noise and very large pathways with weak signal; these thresholds must be consistent across full and reduced analyses for fair comparison.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: GEOquery, limma, ggplot2, data.table, msigdbr, GESECA results table from full matrix analysis (pathway, score, pval, padj, size), GESECA results table from reduced (10-PC) matrix analysis (pathway, score, pval, padj, size), Scatterplot comparing log10(pval) from full vs reduced matrix, showing Pearson correlation ≥0.95.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [methods] Does dimensionality reduction via PCA to 10 dimensions preserve the pathway enrichment results (pathway scores and p-values) obtained from geseca() analysis on the full-dimensional GSE200250 expression matrix?: 'gesecaRes <- geseca(exampleExpressionMatrix, examplePathways, minSize = 15, maxSize = 500)'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] fgsea enables fast and accurate calculation of GSEA P-values for gene set collections, supporting the feasibility of comparing pathway enrichment results across different input dimensionalities.: 'This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] GSE200250 microarray dataset from GEO (Th2 activation time course): 'gse200250 <- getGEO("GSE200250", AnnotGPL = TRUE)[[1]]'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Hallmark gene set collection from MSigDB: 'pathwaysDF <- msigdbr(species="mouse", collection="H")'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] GESECA results table from full matrix analysis (pathway, score, pval, padj, size): 'gesecaRes <- geseca(pathways, exprs(es), minSize = 15, maxSize = 500)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] GESECA results table from reduced (10-PC) matrix analysis (pathway, score, pval, padj, size): 'gesecaResRed <- geseca(pathways, Ered, minSize = 15, maxSize = 500, center=FALSE)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Scatterplot comparing log10(pval) from full vs reduced matrix, showing Pearson correlation ≥0.95: 'ggplot(data=merge(gesecaRes[, list(pathway, logPvalFull=-log10(pval))], gesecaResRed[, list(pathway, logPvalRed=-log10(pval))])) + geom_point(aes(x=logPvalFull, y=logPvalRed))'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] GEOquery: 'library(GEOquery)'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] limma: 'exprs(es) <- normalizeBetweenArrays(log2(exprs(es)), method="quantile")'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] fgsea: 'gesecaResRed <- geseca(pathways, Ered, minSize = 15, maxSize = 500, center=FALSE)'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] R: 'E <- t(base::scale(t(exprs(es)), scale=FALSE))'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] ggplot2: 'ggplot(data=merge(...)) + geom_point(aes(x=logPvalFull, y=logPvalRed))'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] data.table: 'library(data.table)'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] msigdbr: 'pathwaysDF <- msigdbr(species="mouse", collection="H")'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history available for the fgsea package: 'No changelog found.'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] Specific reference implementation or expected outputs for the full-matrix geseca() run on GSE200250 are not provided: '[UNTRUSTED_DOCUMENT]_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that GSE200250 expression matrix can be loaded from GEO using GEOquery
- verify that PCA reduction to 10 dimensions produces a numeric matrix with 10 columns
- verify that geseca() function runs without error on the PCA-reduced matrix with compatible pathway input
- verify that geseca() output on reduced matrix contains pathway scores (NES or similar numeric field)
- verify that geseca() output on reduced matrix contains p-values (padj or pval field)
- verify that pathway scores from reduced-matrix run are within 0.5 absolute units of full-matrix scores (parameter-sensitive; requires establishing baseline full-matrix results first)
- verify that p-values from reduced-matrix run are within 0.05 absolute difference of full-matrix p-values (parameter-sensitive; requires establishing baseline full-matrix results first)

### Expert Review
- evaluate whether score and p-value differences between full-matrix and PCA-reduced runs are biologically acceptable given the dimensionality reduction
- assess whether the choice of 10 PCA dimensions preserves sufficient variance for meaningful pathway inference
- judge whether similarity thresholds (0.5 for scores, 0.05 for p-values) are appropriate benchmarks or require adjustment based on statistical properties of the data

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load GSE200250 microarray data from GEO and extract Th2 time-course samples
2. Apply log2 transformation and quantile normalization to expression matrix
3. Filter genes to top 12,000 by mean expression and remove duplicates/invalid identifiers
4. Center gene expression matrix rows to zero mean and perform standard PCA extraction
5. Retain first 10 principal components (feature loadings: genes × 10 PCs) as reduced expression matrix
6. Run GESECA on full and reduced matrices with identical parameters (minSize=15, maxSize=500, center=FALSE for reduced)
7. Compare pathway p-values between full and reduced results via Pearson correlation of log10-transformed p-values
8. Validation: confirm log10 p-value correlation ≥0.95 to confirm dimensionality reduction preserves pathway scores
9. References: GSE200250 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200250); GSE116240 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240); GSE14308 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE14308)

## Workflow Ports

**Inputs:**

- `geo_dataset_gse200250` — GSE200250 microarray dataset (Th2 activation time course) ← `task_002/geseca_results`
- `hallmark_pathways` — Hallmark gene set collection (mouse, MSigDB)

**Outputs:**

- `geseca_full_results` — GESECA results from full expression matrix
- `geseca_reduced_results` — GESECA results from 10-PC reduced matrix
- `pval_comparison_plot` — Scatterplot comparing p-values (full vs reduced)

**Used:** `urn:asb:port:task_002/geseca_results`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:alserglab__fgsea`
- **Synthesized at:** 2026-06-15T19:26:40+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
