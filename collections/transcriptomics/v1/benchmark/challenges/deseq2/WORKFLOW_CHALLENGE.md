# Workflow Challenge: `coll_deseq2_workflow`


> DESeq2 is an R package for detecting differentially expressed genes from RNA-seq count data using negative binomial generalized linear models with data-driven priors on dispersion and log fold changes. The vignette demonstrates standard differential expression workflows and data transformations.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

DESeq2 provides methods for statistical inference of systematic changes in gene expression between conditions using count data from RNA-seq and related assays. The package models count data with negative binomial generalized linear models, incorporating data-driven prior distributions for dispersion estimates and logarithmic fold changes. The vignette explains package usage through typical workflows, including construction of DESeqDataSet objects from various input sources (transcript quantification files via tximport, count matrices, htseq-count files, or SummarizedExperiment objects), differential expression analysis using the DESeq function, and results extraction via the results function which automatically performs independent filtering. Log fold change shrinkage for visualization and ranking is demonstrated using lfcShrink with three estimator types (apeglm, normal, ashr). Data transformations including variance stabilizing transformation (vst) and regularized logarithm (rlog) are described for downstream visualization and clustering applications.

## Research questions

- How many genes in the airway dataset show statistically significant differential expression (adjusted p-value < 0.1) between treated and untreated conditions when analyzed with DESeq2 using the default FDR threshold?
- How do the three shrinkage estimators (apeglm, normal, ashr) in lfcShrink() differ in their shrunken log fold change estimates for the airway dataset treated-vs-untreated contrast?
- How does tximport process transcript-level quantification files from tximportData to produce a gene-level count matrix suitable for DESeqDataSetFromTximport?
- How does the results() function automatically perform independent filtering based on mean normalized counts, and what are the expected outputs when this filtering is applied to DESeq2 results?

## Methods overview

Load airway SummarizedExperiment and construct DESeqDataSet with design ~cell+dex to account for cell type variation while testing dexamethasone treatment effect. Estimate per-gene dispersions using the negative binomial GLM framework, shrinking estimates toward a mean-dispersion trend fitted across all genes. Fit negative binomial GLM for each gene and compute Wald test statistics and p-values for the treatment coefficient. Apply automatic independent filtering based on mean normalized count to optimize the number of genes achieving padj < alpha, where alpha=0.1 (default FDR target). Extract results table with log2 fold changes, standard errors, test statistics, raw p-values, and Benjamini-Hochberg adjusted p-values for treated-vs-untreated contrast. Validation: verify that the count of genes with padj < 0.1 matches the reported value from the vignette and that results table structure includes all required columns (baseMean, log2FoldChange, lfcSE, stat, pvalue, padj). References: source article (DOI: 10.1186/s13059-014-0550-8) Load airway dataset and construct DESeqDataSet with cell and dex design factors. Execute DESeq() to estimate dispersions and fit negative binomial generalized linear models. Extract base results table containing unshrunk log fold changes and p-values for dex effect. Apply lfcShrink with apeglm method (adaptive t-prior, ~5 seconds runtime) to shrink effect sizes. Apply lfcShrink with normal method (adaptive normal prior) for comparison. Apply lfcShrink with ashr method (mixture of normals prior) for additional estimator comparison. Generate MA-plots for each shrunken result to visualize shrinkage strength and effect on visualization. Validation: confirm that each lfcShrink call produces a DESeqResults object with log2FoldChange, lfcSE, and padj columns; verify MA-plots show reduced noise in low-count genes relative to base results; confirm apeglm shrinkage is more conservative than normal prior and ashr produces intermediate shrinkage strength. References: source article (DOI: 10.1186/s13059-014-0550-8) Load sample metadata and assign experimental condition labels (A, B) from tximportData package. Construct file paths to Salmon quantification outputs (quant.sf.gz) and load the tx2gene transcript-to-gene mapping table. Import transcript-level quantifications using tximport() with type='salmon' to aggregate to gene level, producing estimated gene counts and length offsets. Construct a DESeqDataSet from the tximport output (txi list) using DESeqDataSetFromTximport() with sample metadata and design formula. Validation: verify that the assay matrix contains un-normalized integer counts (not scaled by library size) by inspecting the count values and confirming they match expected ranges for RNA-seq data. References: source article (DOI: 10.1186/s13059-014-0550-8) Load airway SummarizedExperiment and construct DESeqDataSet with design ~ cell + dex. Run DESeq() to fit negative binomial GLM and estimate dispersions across all genes. Extract standard results with results(dds, alpha=0.1) to apply automatic independent filtering based on mean normalized count threshold. Separately apply IHW-based filtering using results(dds, filterFun=ihw) to obtain hypothesis-weighted p-value adjustments and FDR control. Tabulate and compare filtered gene counts, adjusted p-value distributions, and NA assignments between standard filtering and IHW approaches. Validation: Verify that the number of genes with padj < 0.1 after standard filtering is at least as many as reported in the vignette summary(res) output, and confirm IHW metadata contains ihwResult object with weights and rejection decisions. References: source article (DOI: 10.1186/s13059-014-0550-8)

**Domain:** transcriptomics

**Techniques:** normalization, statistical-analysis, false-discovery-rate-correction

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The results() function automatically performs independent filtering based on the mean of normalized counts for each gene. [evidence_step: task_004] _[grounded: lfcshrink_function under cond_treated_vs_untreated]_
- **(finding)** DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models. _[grounded: deseq2_system]_
- **(finding)** The DESeq2 estimates of dispersion and logarithmic fold changes incorporate data-driven prior distributions. _[grounded: deseq2_system]_
- **(finding)** DESeq2 should be cited with the reference Love, M.I., Huber, W., Anders, S. (2014) published in Genome Biology volume 15:550. _[grounded: deseq2_system]_
- **(finding)** Other Bioconductor packages with similar aims to DESeq2 include edgeR, limma, DSS, EBSeq, and baySeq. _[grounded: deseq2_system]_
- **(finding)** DESeq2 internally corrects for library size, so transformed or normalized values should not be used as input. _[grounded: deseq2_system]_
- **(finding)** The DESeqDataSet class extends the RangedSummarizedExperiment class. _[grounded: deseqdataset]_
- **(finding)** The design formula in DESeq2 must be specified to express the variables which will be used in modeling. _[grounded: deseq2_system]_
- **(finding)** The variable of interest should be placed at the end of the design formula to benefit from default package settings.
- **(finding)** Tximport is the recommended pipeline for DESeq2 to create gene-level count matrices from transcript abundance estimates. _[grounded: deseq2_system]_
- **(finding)** Tximport can import transcript abundance estimates from Salmon, Sailfish, kallisto, and RSEM. _[grounded: tximport_tool]_
- **(finding)** Using fast transcript abundance quantifiers corrects for potential changes in gene length across samples from differential isoform usage.
- **(finding)** Salmon, Sailfish, and kallisto are substantially faster and require less memory and disk usage compared to alignment-based methods. _[grounded: salmon_tool]_
- **(finding)** Using fast quantifiers allows avoiding discarding fragments that can align to multiple genes with homologous sequence, increasing sensitivity.
- **(finding)** The Salmon software should be used with the --gcBias flag to estimate a correction factor for systematic biases in RNA-seq data. _[grounded: salmon_tool]_
- **(finding)** It is absolutely critical that the columns of the count matrix and rows of the column data are in the same order.
- **(finding)** The featureCounts function in Rsubread can quickly produce count matrices from alignment files. _[grounded: featurecounts_tool]_
- **(finding)** By default, R chooses a reference level for factors based on alphabetical order.
- **(finding)** DESeq2 will not make guesses about which column of the count matrix belongs to which row of the column data. _[grounded: deseq2_system]_
- **(finding)** Technical replicates can be collapsed into single columns using the collapseReplicates function in DESeq2. _[grounded: deseq2_system]_
- **(finding)** The pasilla dataset is from an experiment on Drosophila melanogaster cell cultures investigating RNAi knock-down of the splicing factor pasilla. _[grounded: pasilla_dataset]_
- **(finding)** The results function extracts a results table with log2 fold changes, p values and adjusted p values. _[grounded: results_function]_
- **(finding)** By default, results are for the last variable in the design formula and the last level compared to the reference level. _[grounded: results_function]_
- **(finding)** Log fold change shrinkage is useful for visualization and ranking of genes.
- **(finding)** The apeglm method is the default shrinkage estimator in DESeq2 as of version 1.28.0. _[grounded: deseq2_system]_
- **(finding)** The ashr shrinkage estimator fits a mixture of Normal distributions to form the prior. _[grounded: deseq2_system]_
- **(finding)** The apeglm method has been sped up to take roughly the same time as the normal method, approximately 5 seconds for the pasilla dataset. _[grounded: apeglm_estimator]_
- **(finding)** The pasilla dataset contains approximately 10,000 genes and 7 samples. _[grounded: pasilla_dataset]_
- **(finding)** Setting apeMethod="nbinomC" produces a 10x speedup but returns lfcSE column with NA.
- **(finding)** Batch effects should be corrected for by including known batch variables in the design formula or using functions like svaseq or RUV. _[grounded: deseq2_system]_
- **(finding)** The plotCounts function normalizes counts by estimated size factors and adds a pseudocount of 1/2 for log scale plotting.
- **(finding)** For a log2 fold change of -1, the treatment induces a multiplicative change of 0.5 in gene expression level.
- **(finding)** If all samples in a row have zero counts, baseMean, log2 fold change, p value and adjusted p value will all be set to NA.
- **(finding)** Extreme count outliers detected by Cook's distance cause p value and adjusted p value to be set to NA.
- **(finding)** Low mean normalized count causes only the adjusted p value to be set to NA through independent filtering. _[grounded: independent_filtering]_
- **(finding)** The regionReport package can generate an HTML and PDF summary of DESeq2 results with plots. _[grounded: deseq2_system]_
- **(finding)** The Glimma package can generate interactive MA-plots of DESeq2 output. _[grounded: deseq2_system]_
- **(finding)** The pcaExplorer package can generate PCA plots, boxplots of counts and other summaries from DESeq2 output. _[grounded: deseq2_system]_
- **(finding)** The iSEE package provides functions for creating an interactive Shiny-based graphical user interface for exploring SummarizedExperiment objects.
- **(finding)** The iSEEde package provides additional panels for interactive visualization of differential expression results in iSEE applications. _[grounded: results_function]_
- **(finding)** DEvis is available on CRAN and GitHub for analysis of differential expression data.
- **(finding)** Results can be exported using base R functions write.csv or write.delim. _[grounded: results_function]_
- **(finding)** Multi-factor designs can be analyzed by including additional variables in the design formula.
- **(finding)** DESeq2 can analyze experimental designs with fixed effects including multiple factors, interactions, and continuous variables. _[grounded: deseq2_system]_
- **(finding)** Adding variables to the design can control for additional variation in counts and increase sensitivity for finding differences.
- **(finding)** In experiments with many samples, there will likely be technical variation affecting the observed counts that must be modeled. _[grounded: results_function]_
- **(finding)** Variance stabilizing transformation and rlog are used to remove the dependence of variance on the mean.
- **(finding)** VST and rlog produce transformed data on the log2 scale which has been normalized with respect to library size.
- **(finding)** The rlog function may take too long for experiments with many samples (e.g. 100s), so vst is a faster choice.
- **(finding)** The rlog function requires fitting a shrinkage term for each sample and each gene which takes time.
- **(finding)** Transformation functions vst and rlog have a blind argument for whether transformation should be blind to sample information.
- **(finding)** When blind equals TRUE, vst and rlog functions re-estimate dispersions using only an intercept.
- **(finding)** Blind dispersion estimation should be used to compare samples in a manner unbiased by experimental groups for quality assurance.
- **(finding)** Blind dispersion estimation is not appropriate when expecting many genes will have large differences explainable by experimental design.
- **(finding)** Using blind dispersion estimation can lead to overly shrinking transformed values when design differences are misattributed as noise.
- **(finding)** Setting blind to FALSE uses dispersions already estimated or estimates them using the current design formula.
- **(finding)** Transformation functions vst and rlog return an object of class DESeqTransform, which is a subclass of RangedSummarizedExperiment.
- **(finding)** For approximately 20 samples, rlog may take 30 seconds while vst takes less than 1 second. _[grounded: deseqdataset]_
- **(finding)** Running times for vst and rlog are shorter when using blind=FALSE if the function DESeq has already been run. _[grounded: deseq_function]_
- **(finding)** Pre-filtering low count genes reduces memory size of the dds object and increases speed of count modeling in DESeq2. _[grounded: deseq2_system]_
- **(finding)** Pre-filtering improves visualizations by not plotting features with no information for differential expression.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- edgeR, limma, DSS, EBSeq, baySeq as alternatives to DESeq2
- apeglm, ashr, or normal shrinkage estimators
- vst or rlog for data transformation
- glmGamPoi for faster NB GLM fitting

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- glmGamPoi requires use of test="LRT" and specification of a reduced design
- rlog may be slow for many samples (100s)

## Steps

### Step `task_001`
- Title: Reproduce the count of genes with adjusted p-value < 0.1 in the airway dataset DESeq2 analysis
- Task kind: `reproduction`
- Task: Run DESeq2's standard differential expression pipeline on the airway dataset to test for treated-vs-untreated differences, applying the default FDR threshold (alpha=0.1), and produce a results table with log2 fold changes and adjusted p-values.
- Inputs:
  - airway SummarizedExperiment object from Bioconductor airway package
- Expected outputs:
  - Results table with columns: baseMean, log2FoldChange, lfcSE, stat, pvalue, padj for treated-vs-untreated contrast
  - Count of genes with adjusted p-value < 0.1
- Tools: DESeq2
- Landmark output files: dds_object.RData, results_table_raw.csv, results_table_ordered_by_padj.csv
- Primary expected artifact: `deseq_results.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce LFC shrinkage results for apeglm, normal, and ashr estimators on the airway dataset
- Task kind: `reproduction`
- Task: Apply lfcShrink() with three shrinkage estimators (apeglm, normal, ashr) to DESeq2 results from the airway dataset and produce shrunken log fold change tables for the treated-vs-untreated contrast.
- Inputs:
  - airway SummarizedExperiment dataset
  - DESeqDataSet object after DESeq() analysis
- Expected outputs:
  - Shrunken LFC results table from apeglm estimator
  - Shrunken LFC results table from normal estimator
  - Shrunken LFC results table from ashr estimator
  - Comparative MA-plots for three shrinkage estimators
- Tools: DESeq2
- Landmark output files: results_base.csv, resLFC_apeglm.csv, resNorm_normal.csv, resAsh_ashr.csv, ma_plots_comparison.png
- Primary expected artifact: `shrunken_lfc_comparison_results.RData`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct the tximport-based count matrix ingestion step for DESeq2 using tximportData
- Task kind: `component_reconstruction`
- Task: Import transcript-level quantification files from tximportData package using tximport to produce a gene-level count matrix, then construct a DESeqDataSet suitable for differential expression analysis. Verify that the resulting matrix contains un-normalized estimated gene counts.
- Inputs:
  - Sample metadata table from tximportData package (samples.txt with run IDs, population, center, and condition information)
  - Salmon quant.sf.gz quantification files for each sample
  - Transcript-to-gene mapping table (tx2gene.gencode.v27.csv)
- Expected outputs:
  - Gene-level count matrix (txi list object) containing un-normalized estimated gene counts, transcript lengths, and abundance-weighted library size offsets
  - DESeqDataSet object (ddsTxi) with gene-level counts, sample metadata, and design formula ready for differential expression analysis
- Tools: tximport, DESeq2, Salmon, tximportData, readr
- Landmark output files: samples_metadata_table.txt, txi_list.rds, dds_object.rds

### Step `task_004`
- Title: Reproduce the ~10x speedup of apeglm's nbinomC fast mode on the pasilla dataset
- Task kind: `reproduction`
- Task: Apply independent filtering and IHW-based p-value adjustment to DESeq2 results from the airway dataset, reproducing the automatic filtering behavior of results() and separately applying Independent Hypothesis Weighting, then verify that filtered gene counts and adjusted p-value outputs match expected behavior.
- Inputs:
  - airway SummarizedExperiment dataset from Bioconductor airway package
- Expected outputs:
  - Results table with log2 fold changes, p-values, and adjusted p-values after automatic independent filtering (default alpha=0.1)
  - Results table with IHW-adjusted p-values and metadata containing ihwResult object
  - Summary statistics comparing gene counts retained after standard filtering vs. IHW filtering
- Tools: DESeq2, IHW
- Landmark output files: results_standard_alpha01.csv, results_ihw_adjusted.csv, filter_summary_stats.txt
- Primary expected artifact: `filtering_comparison_summary.csv`

## Final expected outputs

- `Shrunken LFC results table from apeglm estimator` (type: file, tolerance: hash)
- `Shrunken LFC results table from normal estimator` (type: file, tolerance: hash)
- `Shrunken LFC results table from ashr estimator` (type: file, tolerance: hash)
- `Comparative MA-plots for three shrinkage estimators` (type: file, tolerance: hash)
- `Gene-level count matrix (txi list object) containing un-normalized estimated gene counts, transcript lengths, and abundance-weighted library size offsets` (type: file, tolerance: hash)
- `DESeqDataSet object (ddsTxi) with gene-level counts, sample metadata, and design formula ready for differential expression analysis` (type: file, tolerance: hash)
- `Results table with log2 fold changes, p-values, and adjusted p-values after automatic independent filtering (default alpha=0.1)` (type: file, tolerance: hash)
- `Results table with IHW-adjusted p-values and metadata containing ihwResult object` (type: file, tolerance: hash)
- `Summary statistics comparing gene counts retained after standard filtering vs. IHW filtering` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** concrete

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
  "workflow_id": "coll_deseq2_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004"
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
    }
  },
  "final_outputs": {
    "Shrunken LFC results table from apeglm estimator": "<locator>",
    "Shrunken LFC results table from normal estimator": "<locator>",
    "Shrunken LFC results table from ashr estimator": "<locator>",
    "Comparative MA-plots for three shrinkage estimators": "<locator>",
    "Gene-level count matrix (txi list object) containing un-normalized estimated gene counts, transcript lengths, and abundance-weighted library size offsets": "<locator>",
    "DESeqDataSet object (ddsTxi) with gene-level counts, sample metadata, and design formula ready for differential expression analysis": "<locator>",
    "Results table with log2 fold changes, p-values, and adjusted p-values after automatic independent filtering (default alpha=0.1)": "<locator>",
    "Results table with IHW-adjusted p-values and metadata containing ihwResult object": "<locator>",
    "Summary statistics comparing gene counts retained after standard filtering vs. IHW filtering": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
