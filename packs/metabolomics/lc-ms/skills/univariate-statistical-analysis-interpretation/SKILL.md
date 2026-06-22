---
name: univariate-statistical-analysis-interpretation
description: Use when you have a preprocessed feature table from non-targeted LC-MS/MS metabolomics data (after data merging, cleanup, blank removal, and batch correction) and need to test whether individual metabolomic features show statistically significant differences between experimental groups or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - Jupyter Notebook
  - Google Colab
  - GNPS2 Web App
  - Streamlit App
  techniques:
  - LC-MS
  - tandem-MS
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

# univariate-statistical-analysis-interpretation

## Summary

Execute statistical hypothesis testing on metabolomic features extracted from non-targeted LC-MS/MS data using Jupyter notebooks with R kernels to identify significantly altered metabolites across sample groups. This skill applies univariate statistical methods to feature tables derived from feature-based molecular networks, producing ranked results with p-values and effect sizes suitable for prioritizing candidates for downstream multivariate or network-level analysis.

## When to use

Apply this skill when you have a preprocessed feature table from non-targeted LC-MS/MS metabolomics data (after data merging, cleanup, blank removal, and batch correction) and need to test whether individual metabolomic features show statistically significant differences between experimental groups or conditions. Specifically use it when your goal is to identify univariate significance of individual features before or in parallel with multivariate analysis of feature-based molecular networks.

## When NOT to use

- Input data is not yet cleaned—data merging, blank removal, batch correction must be completed beforehand; this skill assumes a fully preprocessed feature table.
- You aim only to visualize molecular network topology without statistical hypothesis testing; use network analysis skills instead.
- Feature table is already collapsed or aggregated at the pathway or compound class level; univariate analysis operates on individual features.

## Inputs

- Preprocessed feature table (matrix format: samples × features with intensity values)
- Sample metadata (group assignments, batch indicators, covariates)
- Feature identifiers (m/z, retention time, or feature ID)
- Reference results files (from Google Drive) for validation

## Outputs

- Statistical test results table (feature ID, p-value, adjusted p-value, fold-change or effect size)
- Ranked feature list by significance
- Summary statistics and diagnostic plots
- Output files matching reference format in project Google Drive

## How to apply

Clone the FBMN-STATS repository and open the univariate statistical analysis Jupyter notebook with an R kernel. Load your preprocessed feature table (e.g., from test datasets MSV000082312 or MSV000085786) in the format required by the notebook—typically a matrix of feature intensities with samples as rows and features as columns, plus associated metadata (sample group assignments, batch indicators). Execute all notebook cells in sequence; the workflow performs statistical hypothesis testing (e.g., t-tests, ANOVA, or appropriate non-parametric equivalents) on each feature to generate p-values and effect size estimates. Verify output against reference result files deposited in the project Google Drive to confirm correct file format, presence of key columns (feature ID, p-value, adjusted p-value, fold-change or effect size), and logical value ranges (p-values in [0,1], fold-changes numeric). The notebook structure ensures reproducibility and standardized output naming conventions.

## Related tools

- **Jupyter Notebook** (Interactive computational environment for executing R-kernel univariate statistical analysis on feature tables with cell-by-cell reproducibility and integrated documentation.) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **R** (Statistical computing language in which univariate tests (t-tests, ANOVA, Wilcoxon, etc.) and effect size calculations are implemented within the notebook.) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Google Colab** (Cloud-based alternative execution environment for running the R notebooks without local installation; supports both direct Jupyter and Google Colab workflows.) — https://colab.research.google.com/github/Functional-Metabolomics-Lab/FBMN-STATS/blob/main/R/Stats_Untargeted_Metabolomics.ipynb
- **GNPS2 Web App** (Hosted web interface implementation of the FBMN-STATS notebook for running univariate statistical analysis without local installation, suitable for smaller datasets.) — https://fbmn-statsguide.gnps2.org/
- **Streamlit App** (Alternative cloud-hosted web application for executing the statistical analysis workflow on smaller datasets without installation.) — https://fbmn-stats.streamlit.app/

## Evaluation signals

- Output files exist and match reference file names and structure from the project Google Drive (e.g., feature table with columns: feature ID, p-value, adjusted p-value, effect size).
- All p-values are numeric, fall within [0, 1], and adjusted p-values are ≥ original p-values (monotonicity check).
- Feature counts in output match input feature table; no features unexpectedly dropped or duplicated.
- Results show biologically plausible effect sizes (fold-changes typically in range observed in metabolomic studies, e.g., |log2 FC| often < 5 for most metabolites) and p-value distributions (e.g., histogram of raw p-values shows enrichment near 0 if true signals exist).
- Notebook runs without errors and all cells execute in sequence; intermediate diagnostic plots (e.g., QQ plots, histograms of p-values) are generated and visually consistent with statistical assumptions (normality, equal variance when applicable).

## Limitations

- Google Colab runtime will automatically disconnect after 90 minutes of idle time or 12 hours of continuous use, requiring rerun of the entire notebook; local Jupyter Notebook avoids this but requires software installation.
- Colab has a 77 GB disk space limit per user; larger datasets may exceed available storage or require data streaming strategies not addressed in the notebook.
- GNPS Quickstart version (legacy) does not generate reformatted output compatible with the notebook; users must switch to GNPS 2 to ensure correct feature table format.
- Code transfer from GitHub rendering to other environments (e.g., RStudio) may lose HTML formatting or symbols due to GitHub display limitations; direct use of Google Colab or locally-opened Jupyter files is recommended for code copying.
- Notebook assumes standard univariate test applicability; users must validate that test assumptions (e.g., normality, homogeneity of variance) hold for their specific metabolomic feature distributions; non-parametric alternatives may be needed for heavily skewed or zero-inflated features.

## Evidence

- [other] Univariate statistical analysis workflow reproducibility and output validation: "Run the univariate statistical analysis notebook in Jupyter Notebook with R kernel, executing all cells in sequence to perform statistical hypothesis testing on the metabolomic features. Verify that"
- [readme] Core workflow steps and data pipeline context: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks"
- [readme] Test datasets and execution environment: "MASSIVE Datasets from which all the files were selected for MZmine3: MSV000082312 and MSV000085786"
- [readme] Cloud execution alternative and file handling: "All the output files will be stored under the working directory. You need to download all the result files from the directory at the end of your session as they are only saved in the Cloud and not in"
- [readme] Colab runtime and storage limitations: "when you leave the Colab notebook idle for 90 mins or continuously used it for 12 hours, the runtime will automatically disconnect. Another limitation is disk space of 77 GB for the user."
- [readme] GNPS version compatibility requirement: "We advise Quickstart GNPS users to switch to the latest GNPS 2 for FBMN-STATS and accessing the Notebooks. The previous version of Quickstart GNPS does not generate the reformatted output needed for"
