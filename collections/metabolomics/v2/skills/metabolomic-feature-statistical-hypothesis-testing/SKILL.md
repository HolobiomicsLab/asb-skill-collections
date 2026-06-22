---
name: metabolomic-feature-statistical-hypothesis-testing
description: Use when when you have a normalized and batch-corrected feature abundance matrix from non-targeted LC-MS/MS metabolomics (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0080
  tools:
  - R
  - Jupyter Notebook
  - FBMN-STATS
  - Google Colab
derived_from:
- doi: 10.1038/s41596-024-01046-3
  title: FBMN-STATS
evidence_spans:
- To easily install and run Jupyter Notebook in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fbmn_stats_cq
    doi: 10.1038/s41596-024-01046-3
    title: FBMN-STATS
  dedup_kept_from: coll_fbmn_stats_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-024-01046-3
  all_source_dois:
  - 10.1038/s41596-024-01046-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-feature-statistical-hypothesis-testing

## Summary

Execute univariate statistical hypothesis testing on metabolomic features extracted from non-targeted LC-MS/MS data to identify statistically significant metabolites across experimental conditions. This skill applies parametric and non-parametric tests to feature intensity matrices after data cleanup, batch correction, and blank removal to produce p-values and effect estimates for downstream interpretation.

## When to use

When you have a normalized and batch-corrected feature abundance matrix from non-targeted LC-MS/MS metabolomics (e.g., after MZmine3 processing and feature-based molecular networking), and you need to test whether individual metabolomic features differ significantly between experimental groups or treatments. Use this skill as the first statistical step after data merging, cleanup, blank removal, and batch correction—before multivariate analysis or network interpretation.

## When NOT to use

- Input feature table has not undergone data cleanup, blank removal, or batch correction—apply those preprocessing steps first.
- Sample size is extremely small (n < 3 per group), making hypothesis testing unreliable; use exploratory or descriptive methods instead.
- Experiment uses a paired or repeated-measures design without modifications to the standard notebook; consult the documentation for paired-test variants.

## Inputs

- Cleaned and batch-corrected feature abundance matrix (CSV or TSF format)
- Sample metadata with experimental group/treatment assignments
- Non-targeted LC-MS/MS feature table from MZmine3 or equivalent
- Blank-removed and normalized intensity values

## Outputs

- Univariate statistical test results table (p-values, adjusted p-values, effect sizes per feature)
- Summary statistics and hypothesis test reports
- Filtered feature lists meeting statistical significance thresholds
- Visualization plots (e.g., volcano plots, Q-Q plots)

## How to apply

Load the cleaned and batch-corrected feature table (rows=metabolomic features, columns=samples) into a Jupyter Notebook with R kernel. Execute the univariate statistical analysis notebook from the FBMN-STATS repository, which applies statistical hypothesis tests (e.g., t-tests, ANOVA, or non-parametric equivalents depending on data distribution and group structure) to each feature independently, computing p-values and effect sizes. The notebook automates test selection, multiple-testing correction, and tabulation of results. Compare generated output files (e.g., result tables with p-values, log-fold-changes, and adjusted significance thresholds) against reference files deposited in the project Google Drive to verify correct execution and data format compatibility.

## Related tools

- **Jupyter Notebook** (Execution environment for running the univariate statistical analysis notebook with R kernel) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **R** (Programming language for statistical hypothesis testing, p-value computation, and multiple-testing correction) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **FBMN-STATS** (Repository providing the pre-built univariate statistical analysis notebook and reference test datasets) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Google Colab** (Cloud-based alternative execution environment for running the R notebook without local installation) — https://colab.research.google.com/github/Functional-Metabolomics-Lab/FBMN-STATS/blob/main/R/Stats_Untargeted_Metabolomics.ipynb

## Evaluation signals

- Output result files exist and match the reference files in the FBMN-STATS Google Drive repository (checking file existence, format, and content alignment).
- P-value distributions are reasonable (e.g., no unexpected clustering at 0 or 1; histogram shows expected shape under null hypothesis).
- Multiple-testing correction (e.g., Benjamini-Hochberg FDR) is applied and adjusted p-values are ≥ raw p-values.
- Effect sizes (e.g., log-fold-changes or standardized differences) are reported alongside p-values for each feature.
- Statistical test choices are appropriate for data structure (e.g., parametric tests for normally distributed features, non-parametric for skewed distributions).

## Limitations

- The notebook assumes features have been pre-filtered for quality and that input data are in the specific format generated by MZmine3 or GNPS 2; older Quickstart GNPS output may not be compatible.
- Univariate testing ignores correlation structure among metabolomic features; multivariate analysis is required to capture network-level effects.
- P-value results are sensitive to missing data handling, normalization method, and batch correction procedure applied before this step; errors in upstream preprocessing will propagate.
- Google Colab runtime has a 90-minute idle timeout and 12-hour continuous-use limit; longer or interactive sessions require local Jupyter Notebook installation.
- Large datasets may exceed Google Colab's 77 GB disk space or memory limits, necessitating local execution or data subsetting.

## Evidence

- [other] univariate statistical analysis workflow can be applied to non-targeted LC-MS/MS metabolomics data: "Result files from executing the notebook analysis are available in the project Google Drive, confirming that the univariate statistical analysis workflow can be applied to non-targeted LC-MS/MS"
- [readme] sequence of data processing and hypothesis testing steps: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data"
- [other] notebook execution and result verification procedure: "Run the univariate statistical analysis notebook in Jupyter Notebook with R kernel, executing all cells in sequence to perform statistical hypothesis testing on the metabolomic features. 4. Verify"
- [readme] cloud-based execution alternative: "To execute our R notebook in Colab: ... While Colab offers a Jupyter Notebook environment, it differs in file loading and output file generation."
- [readme] Colab session and storage limitations: "when you leave the Colab notebook idle for 90 mins or continuously used it for 12 hours, the runtime will automatically disconnect. Another limitation is disk space of 77 GB for the user."
