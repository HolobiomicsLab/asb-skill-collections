# Workflow Challenge: `coll_limmavoom_workflow`


> Limma is an R package for analyzing gene expression data through linear models and empirical Bayesian methods, designed to assess differential expression across diverse technologies including microarrays, RNA-seq, and proteomics.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

The limma package provides methods for analyzing comparisons between many RNA targets simultaneously in arbitrarily complex designed experiments. Empirical Bayesian methods estimate hyperparameters of the prior distribution over gene-wise variances, enabling computation of moderated t-statistics and B-statistics that remain stable even when the number of arrays is small. Linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq, and proteomics. The package also provides normalization and background correction functions for microarrays and similar technologies.

## Research questions

- How does limma estimate hyperparameters of the prior distribution over gene-wise variances to compute moderated t-statistics and B-statistics?
- What does the lmFit function in limma produce when applied to a microarray dataset with a specified design matrix?
- Does prepending edgeR's calcNormFactors normalization to the limma voom pipeline alter the ranked list of differentially expressed genes compared to the standard limma-only workflow?

## Methods overview

Load a pre-fitted lmFit object containing gene-wise ordinary least-squares estimates and residual variances Apply empirical Bayes estimation to fit a scaled inverse-chi-squared prior distribution over gene-wise variances Compute moderated t-statistics by shrinking gene variances toward the posterior mean under the fitted prior Calculate B-statistics (log-odds of differential expression) from the moderated t-statistics and estimated prior degrees of freedom Validation: verify that moderated t-statistics show reduced variance and improved power-to-detect compared to ordinary t-statistics, particularly for genes with small sample sizes or low initial variance estimates References: source article (DOI: 10.1093/nar/gkv007) Load microarray expression matrix and sample metadata from a public GEO repository. Construct a design matrix encoding experimental groups, conditions, and any batch or covariate effects. Apply limma's lmFit function to fit row-wise linear models across all genes using the design matrix. Retrieve the MArrayLM object containing coefficient estimates, standard errors, and model diagnostics. Validation: Confirm that the MArrayLM object contains a non-empty coefficients matrix with dimensions matching the number of genes and design matrix columns, and that all standard error estimates are positive and finite. References: source article (DOI: 10.1093/nar/gkv007) Load raw RNA-seq read counts and metadata; construct design matrix from experimental annotations. Apply edgeR's calcNormFactors with TMM method to compute library size scaling factors accounting for composition bias. Execute voom transformation using TMM-normalized library sizes to calculate precision weights for each observation. Fit linear models using lmFit, then apply empirical Bayes variance moderation with eBayes. Extract top differentially expressed genes and quantify concordance with limma-only baseline. Validation: Confirm that TMM-voom and limma-only outputs both pass Benjamini-Hochberg FDR correction at threshold 0.05; report overlap of significant genes and magnitude of log-fold-change differences between methods. References: source article (DOI: 10.1093/nar/gkv007)

**Domain:** transcriptomics

**Techniques:** statistical-analysis, normalization, false-discovery-rate-correction

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Limma is an R package for the analysis of gene expression data. _[grounded: limma]_
- **(finding)** Limma uses linear models for analysing designed experiments and assessment of differential expression. _[grounded: limma]_
- **(finding)** Limma provides the ability to analyse comparisons between many RNA targets simultaneously in complicated designed experiments. _[grounded: limma]_
- **(finding)** Empirical Bayesian methods are used to provide stable results even when the number of arrays is small. _[grounded: comp_empirical_bayes]_
- **(finding)** Normalization and background correction functions are provided for microarrays and similar technologies. _[grounded: comp_normalization]_
- **(finding)** Linear model and differential expression functions apply to microarrays (single-channel or two-color).
- **(finding)** Linear model and differential expression functions apply to quantitative PCR.
- **(finding)** Linear model and differential expression functions apply to RNA-seq.
- **(finding)** Linear model and differential expression functions apply to proteomics.
- **(finding)** Ritchie et al. (2015) demonstrated that limma powers differential expression analyses for RNA-sequencing and microarray studies. _[grounded: limma]_
- **(finding)** Phipson et al. (2016) showed that robust hyperparameter estimation protects against hypervariable genes. _[grounded: comp_robust_hyperparameter]_
- **(finding)** Phipson et al. (2016) showed that robust hyperparameter estimation improves power to detect differential expression. _[grounded: comp_robust_hyperparameter]_
- **(finding)** Law et al. (2014) described voom as unlocking precision weights for linear model analysis of RNA-seq read counts. _[grounded: comp_voom]_
- **(finding)** Law et al. (2016) presented RNA-seq analysis using limma, Glimma, and edgeR as easy as 1-2-3. _[grounded: limma]_
- **(finding)** Law et al. (2020) published a guide to creating design matrices for gene expression experiments.

## Steps

### Step `task_001`
- Title: Reconstruct voom precision-weight computation for RNA-seq count data
- Task kind: `component_reconstruction`
- Task: Fit the empirical Bayes prior distribution over gene-wise variances using a pre-fitted lmFit object, then compute moderated t-statistics and B-statistics for differential expression inference. Output moderated test statistics and posterior odds ratios.
- Inputs:
  - Pre-fitted lmFit object from a public GEO microarray or RNA-seq dataset
- Expected outputs:
  - Table of differential expression results containing gene identifiers, log-fold changes, moderated t-statistics, adjusted p-values, and B-statistics
- Tools: limma, R
- Landmark output files: ebayes_fit.rds, moderated_tstats.csv, ebayes_results.csv
- Primary expected artifact: `ebayes_results.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct empirical Bayes moderated t-statistic computation via limma's eBayes
- Task kind: `component_reconstruction`
- Task: Fit a linear model to a publicly deposited microarray dataset using limma's lmFit function with a specified design matrix, producing a MArrayLM object containing coefficient estimates and standard errors for subsequent empirical Bayes shrinkage analysis.
- Inputs:
  - Microarray expression matrix and phenotype metadata from a public GEO accession
- Expected outputs:
  - MArrayLM fitted-model object containing coefficient estimates, standard errors, and design matrix information
- Tools: limma, R
- Landmark output files: design_matrix.csv, lmfit_coefficients.csv
- Primary expected artifact: `fitted_model.RData`

### Step `task_003`
- Depends on: `task_002`
- Title: Reproduce limma linear-model fitting on a public microarray dataset via lmFit
- Task kind: `reproduction`
- Task: Extend the standard limma RNA-seq pipeline by prepending edgeR's calcNormFactors function to compute TMM normalization factors, pass normalized library sizes to voom, and complete the differential expression workflow. Compare the resulting top table of differentially expressed genes against a limma-only baseline using the same public RNA-seq dataset.
- Inputs:
  - Raw RNA-seq read count matrix and sample metadata from a public RNA-seq dataset (e.g., GEO, ArrayExpress, or SRA accession); must include treatment group assignments and confounding variables for design matrix construction.
- Expected outputs:
  - Top table of differentially expressed genes from TMM-voom-limma pipeline containing gene identifiers, log-fold-changes, average log-expression, t-statistics, p-values, and adjusted p-values (FDR).
  - Top table of differentially expressed genes from limma-only baseline (without TMM normalization pre-processing) in identical format for direct comparison.
  - Comparison summary table or figure showing overlap of significantly differentially expressed genes (FDR < 0.05) between TMM-voom and limma-only methods, including count of concordant/discordant calls and magnitude of log-fold-change shifts.
- Tools: edgeR, limma, R, voom
- Landmark output files: tmm_normalized_counts.csv, voom_weights.csv, tmm_voom_top_table.csv, limma_only_top_table.csv, method_comparison_overlap.png
- Primary expected artifact: `method_comparison_summary.csv`

## Final expected outputs

- `Top table of differentially expressed genes from TMM-voom-limma pipeline containing gene identifiers, log-fold-changes, average log-expression, t-statistics, p-values, and adjusted p-values (FDR).` (type: file, tolerance: hash)
- `Top table of differentially expressed genes from limma-only baseline (without TMM normalization pre-processing) in identical format for direct comparison.` (type: file, tolerance: hash)
- `Comparison summary table or figure showing overlap of significantly differentially expressed genes (FDR < 0.05) between TMM-voom and limma-only methods, including count of concordant/discordant calls and magnitude of log-fold-change shifts.` (type: file, tolerance: hash)

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
  "workflow_id": "coll_limmavoom_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003"
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
    }
  },
  "final_outputs": {
    "Top table of differentially expressed genes from TMM-voom-limma pipeline containing gene identifiers, log-fold-changes, average log-expression, t-statistics, p-values, and adjusted p-values (FDR).": "<locator>",
    "Top table of differentially expressed genes from limma-only baseline (without TMM normalization pre-processing) in identical format for direct comparison.": "<locator>",
    "Comparison summary table or figure showing overlap of significantly differentially expressed genes (FDR < 0.05) between TMM-voom and limma-only methods, including count of concordant/discordant calls and magnitude of log-fold-change shifts.": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
