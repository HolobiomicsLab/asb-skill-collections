---
name: expression-matrix-transformation
description: Use when you have loaded raw expression data (linear-scale peptide or
  protein abundance quantification) into pmartR and need to prepare it for statistical
  analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3500
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pmartR
  - R
  - Shiny
  - PMart ShinyApp
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- the bulk of the functionality of the package to be available to the user without
  the need for familiarity with R or the package itself
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pmart_cq
    doi: 10.1021/acs.jproteome.3c00512
    title: PMart
  dedup_kept_from: coll_pmart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.3c00512
  all_source_dois:
  - 10.1021/acs.jproteome.3c00512
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# expression-matrix-transformation

## Summary

Transform raw omics expression data (peptide or protein quantification matrices) from linear scale to log2 scale to stabilize variance and improve statistical modeling of proteomics and metabolomics datasets. This preprocessing step is essential before downstream normalization, filtering, and statistical analysis in multi-omics workflows.

## When to use

Apply this skill when you have loaded raw expression data (linear-scale peptide or protein abundance quantification) into pmartR and need to prepare it for statistical analysis. Log2 transformation is indicated when the data exhibits heteroscedastic variance (variance increases with mean abundance) or when biomolecules span multiple orders of magnitude in abundance, which is typical for proteomics datasets.

## When NOT to use

- Data already in log-space or normalized scale (e.g., log2 counts per million, z-scores)
- Datasets with many zero or below-detection-limit values where log transformation would yield undefined or -Infinity values without prior imputation
- Non-quantitative data such as presence/absence calls or categorical abundance bins

## Inputs

- raw expression matrix (peptide-level or protein-level quantification)
- sample metadata (group assignments, covariates, pairing structure)
- biomolecule metadata (peptide or protein identifiers and annotations)

## Outputs

- log2-transformed expression matrix
- transformed data object suitable for downstream filtering and normalization

## How to apply

Load the raw expression data matrix along with sample metadata and biomolecule metadata into pmartR using the data upload module. Apply log2 transformation as a preprocessing step early in the analysis pipeline, before filtering and normalization steps. The transformation converts each raw abundance value x to log2(x), stabilizing the variance structure across the abundance range and rendering the data more suitable for parametric statistical methods (ANOVA, linear modeling) that assume homoscedastic residuals. This step is particularly important for proteomics data where dynamic range often spans 4–6 orders of magnitude.

## Related tools

- **pmartR** (R package providing data structures and transformation functions for omics data; the backend for expression matrix transformation in the Shiny GUI) — https://github.com/pmartR/pmartR
- **Shiny** (web framework enabling interactive GUI for pmartR transformation workflow without requiring direct R scripting)
- **R** (statistical programming language implementing the log2 transformation and downstream statistical operations)
- **PMart ShinyApp** (Shiny GUI application that wraps pmartR and presents data transformation as part of the interactive analysis pipeline) — https://github.com/pmartR/PMart_ShinyApp

## Evaluation signals

- Verify that all abundance values in the transformed matrix are non-negative (log2 of positive numbers) and that the data type is numeric
- Confirm that the variance of log-transformed data is more homogeneous across the abundance range compared to the raw data (e.g., by plotting residual variance as a function of mean log-abundance)
- Check that metadata (sample identifiers, biomolecule identifiers, group assignments) are preserved and aligned with the transformed expression matrix
- Validate that downstream filtering (by non-missing values and coefficient of variation) produces reasonable retention rates and that statistical tests (ANOVA, G-test) show improved model assumptions (normality, homoscedasticity) compared to untransformed data
- Inspect the distribution of log-transformed values for expected shape (approximately normal if data follows log-normal distribution in raw scale)

## Limitations

- Log2 transformation is undefined for zero or negative abundance values; datasets with many missing or below-detection-limit measurements require prior imputation or filtering
- The transformation assumes that raw abundances follow a log-normal distribution; datasets with other distributional properties may not benefit or may require alternative transformations (e.g., Box–Cox)
- Cannot be reversed without knowing the original scale; the transformation is lossy for variance estimation and effect-size interpretation on the raw scale
- Biomolecules with very low or undetectable abundance across all samples may produce uninformative log-transformed values and are typically removed during subsequent filtering steps

## Evidence

- [intro] Data transformation (raw to log2): "Data transformation (raw to log2)"
- [readme] The normalization and statistical analysis workflow requires transformed data: "Data transformation (raw to log2)
- Group assignment (main effects, covariates, pairing structure)
- Exploratory data analysis.  PCA, missing-variable plots, correlation heatmaps, and more.
-"
- [readme] Data upload precedes transformation in the workflow: "Data upload.  Upload expression data, sample information, and biomolecule metadata.  See the data-requirements section for details.
- Data transformation (raw to log2)"
