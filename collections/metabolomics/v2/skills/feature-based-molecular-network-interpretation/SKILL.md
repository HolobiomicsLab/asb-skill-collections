---
name: feature-based-molecular-network-interpretation
description: Use when you have a feature-based molecular network generated from non-targeted LC-MS/MS metabolomics data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - Jupyter Notebook
  - MZmine3
  - GNPS FBMN
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

# feature-based-molecular-network-interpretation

## Summary

Interpret feature-based molecular networks (FBMNs) generated from non-targeted LC-MS/MS data by applying statistical analysis workflows (data merging, cleanup, blank removal, batch correction, and univariate/multivariate tests) to identify significant metabolic features and their relationships. This skill enables reproducible extraction of biological insights from FBMN structure and feature abundance patterns.

## When to use

You have a feature-based molecular network generated from non-targeted LC-MS/MS metabolomics data (e.g., from MZmine3 or GNPS FBMN workflow) and need to validate which network features are statistically significant across sample groups, remove technical artifacts (blanks, batch effects), and perform hypothesis testing on metabolic features to support biological interpretation.

## When NOT to use

- Input is targeted metabolomics data with a priori selected metabolites (use targeted statistical methods instead)
- Feature table has already been extensively preprocessed and validated by another pipeline (avoid redundant cleanup steps)
- Network nodes lack mass accuracy or retention-time information needed for chemical annotation (limits biological interpretation)

## Inputs

- Feature abundance table (numeric matrix: rows=features, columns=samples)
- Sample metadata file (sample_id, group assignment, batch/plate identifier)
- Feature annotations (optional: compound names, mass-to-charge, retention time)
- Feature-based molecular network file (nodes and edges, typically from GNPS FBMN task)

## Outputs

- Cleaned and batch-corrected feature abundance matrix
- Univariate statistical results (p-values, fold-changes, effect sizes per feature)
- Multivariate analysis outputs (PCA/PLS-DA scores and loadings, clustering dendrograms)
- Quality control plots (blank removal diagnostics, batch effect visualization)
- Annotated network file with statistical significance overlaid on nodes
- Summary tables of significant features and their biological interpretation

## How to apply

Execute the FBMN-STATS Jupyter notebooks in sequence: (1) load feature abundance tables and metadata into the notebook environment; (2) perform data merging to combine replicate measurements and align with sample metadata; (3) apply blank removal by filtering features below a sample/blank ratio threshold to exclude contamination; (4) conduct batch correction to remove systematic technical variation across runs or plates; (5) perform univariate statistical analysis (e.g., fold-change, t-tests, ANOVA) to identify features significantly different between groups; (6) apply multivariate statistical analysis (e.g., PCA, PLS-DA, hierarchical clustering) to discover multivariate patterns and feature co-variation within the network. Validate results against reference output files stored in the project Google Drive to ensure reproducibility.

## Related tools

- **Jupyter Notebook** (Interactive computational environment for executing multivariate statistical analysis workflows on feature tables and FBMN results) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **R** (Statistical programming language executing univariate and multivariate analysis functions (PCA, PLS-DA, t-tests, ANOVA) within Jupyter notebooks) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **MZmine3** (LC-MS/MS data processing tool that generates the initial feature abundance tables consumed by FBMN-STATS notebooks)
- **GNPS FBMN** (Web workflow that generates feature-based molecular networks from MZmine3 feature lists; output networks are interpreted using FBMN-STATS statistical analysis) — https://gnps.ucsd.edu/ProteoSAFe/
- **Google Colab** (Cloud-based Jupyter environment for running FBMN-STATS notebooks without local R/Jupyter installation) — https://colab.research.google.com/

## Evaluation signals

- All expected output files are generated and present in the working directory after notebook execution completes without errors
- Output files (statistical results tables, plots, cleaned feature matrices) match reference files in the project Google Drive folder within numerical precision tolerances
- Blank removal reduces feature counts from input to output by a detectable margin; sample/blank intensity ratios confirm contamination filtering is active
- Batch-corrected feature abundance matrix shows reduced batch-wise clustering in PCA score plots compared to pre-correction data
- Univariate p-values and fold-changes are reported for ≥80% of input features; significant features (p < 0.05) are identified and annotated with biological group assignment

## Limitations

- Colab runtime disconnects automatically after 90 minutes of idleness or 12 hours of continuous use, requiring re-execution of the entire notebook and loss of intermediate variables
- Colab disk space is limited to 77 GB per user; large datasets or long-running notebooks may exceed memory or storage constraints
- GitHub rendering of Jupyter notebooks may be incomplete due to file size; notebooks must be downloaded and opened locally or accessed via Google Colab links for accurate viewing
- Quickstart GNPS (legacy version) generates reformatted output incompatible with FBMN-STATS notebooks; users must switch to GNPS 2 to avoid incorrect feature table ingestion
- Statistical power depends on sample size and effect magnitude; small sample counts or low fold-changes may fail to reach significance thresholds even for biologically relevant features

## Evidence

- [readme] perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks"
- [intro] Statistical analysis methods can be applied to feature-based molecular networks from non-targeted LC-MS/MS metabolomics data: "Statistical analysis methods can be applied to feature-based molecular networks from non-targeted LC-MS/MS metabolomics data"
- [readme] To use this notebook with your data in Colab, first, save a copy to your Google Drive by selecting File → Save a copy in Drive: "save a copy to your Google Drive by selecting File → Save a copy in Drive"
- [other] Verify that all expected output files are generated and match the reported results stored in the project Google Drive: "all expected output files are generated and match the reported results stored in the project Google Drive"
- [readme] The previous version of Quickstart GNPS does not generate the reformatted output needed for Notebook/Web app integration, leading to incorrect feature tables: "The previous version of Quickstart GNPS does not generate the reformatted output needed for Notebook/Web app integration, leading to incorrect feature tables"
