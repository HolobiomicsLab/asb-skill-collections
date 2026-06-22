---
name: r-statistical-computing
description: Use when you have a merged and batch-corrected non-targeted LC-MS/MS feature table with sample metadata and need to perform statistical testing to identify significant features, compare groups (e.g., disease vs. control), or explore multivariate patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3407
  tools:
  - R
  - Jupyter Notebook
  - Google Colab
  - FBMN-STATS
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

# r-statistical-computing

## Summary

Execute statistical hypothesis testing and multivariate analysis workflows on non-targeted LC-MS/MS metabolomics feature tables using R in a Jupyter Notebook environment. This skill applies univariate and multivariate statistical methods (e.g., t-tests, ANOVA, PCA) to detect significant metabolomic features and derive biological insights from high-dimensional mass spectrometry data.

## When to use

You have a merged and batch-corrected non-targeted LC-MS/MS feature table with sample metadata and need to perform statistical testing to identify significant features, compare groups (e.g., disease vs. control), or explore multivariate patterns. Use this skill after data cleanup and blank removal steps are complete and you have a quantitative feature abundance matrix ready for hypothesis testing.

## When NOT to use

- Input data is already a pre-computed statistical results table (p-values already assigned) — use visualization/interpretation skills instead.
- Feature table has not been cleaned, batch-corrected, or had blanks removed — perform preprocessing steps first.
- Data originates from targeted LC-MS/MS or other instrumental platforms not explicitly supported by the FBMN-STATS workflow.

## Inputs

- Non-targeted LC-MS/MS feature abundance table (CSV or tab-delimited format with features × samples)
- Sample metadata file with group/phenotype assignments
- Test dataset (MSV000082312 or MSV000085786 from MASSIVE, or user-provided equivalent format)

## Outputs

- Univariate statistical test results (p-values, fold-changes, q-values per feature)
- Multivariate analysis outputs (PCA scores, loadings, clustering dendrograms)
- Filtered feature lists (significant features passing statistical thresholds)
- Result visualizations (plots, heatmaps, volcano plots)
- Log files and summary tables documenting analysis parameters and results

## How to apply

Launch the FBMN-STATS R Jupyter Notebook (Stats_Untargeted_Metabolomics.ipynb) either locally via Jupyter Notebook with R kernel or in Google Colab. Load your cleaned feature table (typically a tab-delimited or CSV matrix with features as rows and samples as columns) along with sample metadata file containing group assignments. Execute the notebook cells sequentially to perform data merging, univariate statistical analysis (hypothesis tests on individual features), and multivariate statistical analysis (PCA, clustering). The workflow applies statistical thresholds (e.g., p-values for significance filtering) and generates result files including statistical test outputs, plots, and filtered feature lists. Verify outputs match the reference results by checking file format, presence of expected columns (feature ID, p-value, fold-change), and consistency of statistical summaries.

## Related tools

- **Jupyter Notebook** (Interactive notebook environment for executing R statistical analysis cells sequentially on metabolomics data) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **R** (Statistical computing language executing hypothesis tests, PCA, clustering, and other multivariate methods on feature tables) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Google Colab** (Cloud-based alternative for running R notebooks without local installation; useful for smaller datasets) — https://colab.research.google.com/github/Functional-Metabolomics-Lab/FBMN-STATS/blob/main/R/Stats_Untargeted_Metabolomics.ipynb
- **FBMN-STATS** (Repository containing pre-built Jupyter notebooks and R scripts for univariate and multivariate statistical analysis of non-targeted metabolomics data) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS

## Evaluation signals

- Output result files exist and match the structure and format of reference files in the FBMN-STATS Google Drive (file names, columns, data types).
- Statistical test columns (p-value, q-value, fold-change) are numerically valid (p-values ∈ [0,1], no NaN/Inf values in expected columns).
- Feature count in filtered output is consistent with applied significance thresholds (e.g., features with p < 0.05 or q < 0.1 are retained).
- Multivariate plots (PCA, dendrograms, heatmaps) show expected separation or clustering patterns consistent with sample group assignments.
- Output file content alignment: spot-check a sample of feature IDs, p-values, and effect sizes against intermediate summary statistics to confirm computation accuracy.

## Limitations

- Package installation in Google Colab occurs every session (not persistent), extending runtime; direct Jupyter Notebook is faster for repeated analyses.
- Google Colab runtime disconnects after 90 minutes of inactivity or 12 hours continuous use, requiring notebook restart and loss of session variables; larger datasets may exceed the 77 GB disk limit.
- GitHub rendering of Jupyter notebooks may display incompletely due to file size or complex outputs; use Google Colab or local Jupyter Notebook view for accurate code copying.
- Older Quickstart GNPS (not GNPS 2) does not generate reformatted outputs compatible with the notebook workflow, leading to incorrect feature table integration.
- Workflow is designed for non-targeted LC-MS/MS data after MZmine3 feature detection and FBMN preprocessing; applicability to other mass spectrometry modalities or pre-processing pipelines is not guaranteed.

## Evidence

- [readme] perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks."
- [other] Run the univariate statistical analysis notebook in Jupyter Notebook with R kernel, executing all cells in sequence: "Run the univariate statistical analysis notebook in Jupyter Notebook with R kernel, executing all cells in sequence to perform statistical hypothesis testing on the metabolomic features."
- [readme] To easily install and run Jupyter Notebook in R, follow the steps in the document: "To easily install and run Jupyter Notebook in R, [follow the steps in the document according to your preferred OS]"
- [other] Statistical analysis methods can be applied to feature-based molecular networks from non-targeted LC-MS/MS metabolomics data: "Statistical analysis methods can be applied to feature-based molecular networks from non-targeted LC-MS/MS metabolomics data"
- [readme] Colab environment is all Cloud-based... runtime will automatically disconnect... you will lose all your variables, installed packages, and files: "when you leave the Colab notebook idle for 90 mins or continuously used it for 12 hours, the runtime will automatically disconnect. This means you will lose all your variables, installed packages,"
- [readme] Unlike Jupyter Notebook, it is not possible to access the files from your local computer in a Google Colab space: "Unlike Jupyter Notebook, it is not possible to access the files from your local computer in a Google Colab space as it is cloud-based."
- [readme] Quickstart GNPS users to switch to the latest GNPS 2... previous version does not generate the reformatted output needed: "We advise Quickstart GNPS users to switch to the latest GNPS 2 for FBMN-STATS and accessing the Notebooks. The previous version of Quickstart GNPS does not generate the reformatted output needed for"
