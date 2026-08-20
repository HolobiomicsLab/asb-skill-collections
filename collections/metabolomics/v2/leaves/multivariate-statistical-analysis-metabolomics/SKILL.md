---
name: multivariate-statistical-analysis-metabolomics
description: Use when when you have preprocessed non-targeted LC-MS/MS feature tables
  (post-merging, cleanup, blank removal, and batch correction) and seek to uncover
  multivariate patterns across samples, discriminate between experimental groups,
  or reduce dimensionality of high-dimensional metabolomic data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2269
  tools:
  - R
  - Jupyter Notebook
  - Google Colab
  - MZmine3
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Multivariate Statistical Analysis of Feature-Based Molecular Networks from Non-Targeted Metabolomics

## Summary

Apply multivariate statistical analysis methods (e.g., PCA, PLS-DA, clustering) to feature tables derived from non-targeted LC-MS/MS data to identify patterns, classify samples, and associate metabolomic signatures with experimental conditions or phenotypes in feature-based molecular networks.

## When to use

When you have preprocessed non-targeted LC-MS/MS feature tables (post-merging, cleanup, blank removal, and batch correction) and seek to uncover multivariate patterns across samples, discriminate between experimental groups, or reduce dimensionality of high-dimensional metabolomic data before downstream interpretation.

## When NOT to use

- Input feature table has not undergone data cleanup, blank removal, or batch correction; apply those preprocessing steps first.
- Sample size is extremely small (n < 3 per group); multivariate methods may overfit or lack statistical power.
- Feature table contains raw, non-log-transformed abundances without appropriate normalization; preprocessing must precede multivariate analysis.

## Inputs

- Preprocessed feature table (TSV, CSV, or Excel format) with features as columns and samples as rows
- Sample metadata or design matrix indicating experimental groups or conditions
- Cleaned, batch-corrected LC-MS/MS feature abundance data

## Outputs

- PCA scores and loadings plots
- PLS-DA classification model and predictions
- Heatmaps of clustered features and samples
- Statistical summary tables (e.g., model performance, feature contributions)
- R objects (.RData) or Python pickled objects for downstream analysis

## How to apply

Load the cleaned and batch-corrected feature table (typically in tabular format with features as columns and samples as rows) into a Jupyter Notebook environment (R or Python) from the FBMN-STATS repository. Execute the multivariate statistical analysis notebook, which automates data scaling, dimensionality reduction (PCA), supervised classification (PLS-DA), and clustering. The notebook applies standard preprocessing steps (e.g., log transformation, normalization) and generates publication-ready visualizations (scores plots, loadings, heatmaps) and statistical outputs (model performance metrics). Verify that all cells run without errors and that output files are generated in the working directory.

## Related tools

- **Jupyter Notebook** (Interactive environment for executing R or Python multivariate statistical analysis workflows on feature tables) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **R** (Statistical computing language used in FBMN-STATS notebooks for PCA, PLS-DA, and clustering analysis) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Google Colab** (Cloud-based alternative environment for running FBMN-STATS notebooks without local R installation) — https://colab.research.google.com/github/Functional-Metabolomics-Lab/FBMN-STATS/blob/main/R/Stats_Untargeted_Metabolomics.ipynb
- **MZmine3** (Preprocessing tool for generating feature tables from raw LC-MS/MS data prior to multivariate analysis)

## Evaluation signals

- All notebook cells execute without errors and complete in reasonable time (<30 min for test datasets MSV000082312 or MSV000085786).
- Output files (plots, tables, model objects) are generated in the working directory and match the structure and content of reference files in the associated Google Drive.
- PCA scores plot shows clear separation or clustering consistent with experimental design; PLS-DA model shows non-trivial cross-validation accuracy (>60% for multi-class, >70% for binary).
- Generated visualizations (heatmaps, loadings plots) are readable and reproducible across independent runs with the same input data.
- Dimensions of output matrices and feature contributions are consistent with input feature table dimensions (e.g., loadings matrix = features × n_components).

## Limitations

- Google Colab runtime automatically disconnects after 90 minutes of idleness or 12 hours of continuous use, requiring notebook re-execution and redownload of results.
- Colab disk space is limited to 77 GB, which may constrain analysis of very large datasets or high-dimensional feature tables.
- Quickstart GNPS (older version) does not generate reformatted output compatible with the notebook; users must use GNPS 2 to ensure correct feature table format.
- When copying notebook code to other environments (e.g., RStudio), GitHub rendering limitations may affect symbol transfer; use Google Colab or locally opened Jupyter for accurate code transfer.
- Package installation in Colab must be performed every session (unlike local Jupyter), which adds runtime overhead.

## Evidence

- [readme] perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data"
- [other] Open and execute the multivariate statistical analysis notebook in Jupyter, ensuring all cells run without errors.: "Open and execute the multivariate statistical analysis notebook in Jupyter, ensuring all cells run without errors."
- [other] Verify that all expected output files are generated and match the reported results stored in the project Google Drive.: "Verify that all expected output files are generated and match the reported results stored in the project Google Drive."
- [readme] Since Colab does not come pre-installed with R packages (or libraries) when running our R Notebook in Colab, we need to install the packages every time we run the notebook: "Since Colab does not come pre-installed with R packages (or libraries) when running our R Notebook in Colab, we need to install the packages every time we run the notebook"
- [readme] Although Colab is easier to use and is all Cloud-based, the main problem with the Colab environment is when you leave the Colab notebook idle for 90 mins or continuously used it for 12 hours, the runtime will automatically disconnect.: "when you leave the Colab notebook idle for 90 mins or continuously used it for 12 hours, the runtime will automatically disconnect"
- [readme] We advise Quickstart GNPS users to switch to the latest GNPS 2 for FBMN-STATS and accessing the Notebooks. The previous version of Quickstart GNPS does not generate the reformatted output needed for Notebook/Web app integration: "The previous version of Quickstart GNPS does not generate the reformatted output needed for Notebook/Web app integration"
