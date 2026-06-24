---
name: batch-effect-detection-and-quantification
description: Use when after merging feature tables from multiple LC-MS/MS analytical
  runs or sample cohorts processed in separate batches, and before applying batch
  correction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - Jupyter Notebook
  - SVA (Surrogate Variable Analysis)
  - SMART
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41596-024-01046-3
  title: FBMN-STATS
- doi: 10.1021/acs.analchem.5c03225
  title: ''
evidence_spans:
- To easily install and run Jupyter Notebook in R
- SMART written in R and R GUI has been developed as user-friendly software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fbmn_stats_cq
    doi: 10.1038/s41596-024-01046-3
    title: FBMN-STATS
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  dedup_kept_from: coll_fbmn_stats_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-024-01046-3
  all_source_dois:
  - 10.1038/s41596-024-01046-3
  - 10.1021/acs.analchem.5c03225
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-effect-detection-and-quantification

## Summary

Identify and quantify batch-associated technical variation in merged non-targeted LC-MS/MS metabolomics feature tables before correction. This skill detects whether batch effects are present and their magnitude, informing the choice of batch correction method and validating correction success.

## When to use

After merging feature tables from multiple LC-MS/MS analytical runs or sample cohorts processed in separate batches, and before applying batch correction. Use this skill when samples have been acquired across different instrument sessions, different days, or different lab conditions, and you need to determine whether batch effects are sufficiently large to warrant correction or to monitor correction efficacy.

## When NOT to use

- Input feature table comes from a single analytical batch or single instrument session with no known batch structure — batch detection requires batch variance to exist.
- Samples are already corrected or pre-processed with batch correction applied — re-detection may confound effects.
- Experimental design lacks batch metadata or sample-to-batch mapping — batch effects cannot be quantified without knowing which samples belong to which batch.

## Inputs

- merged feature table (CSV/TSV format: features × samples)
- experimental metadata with batch assignments
- feature abundance matrix (counts or normalized intensities)

## Outputs

- batch effect magnitude estimates (variance components or effect sizes)
- visualizations stratified by batch (PCA plots, heatmaps, boxplots)
- statistical test results (p-values for batch significance)
- surrogate variable estimates (if using SVA-based methods)

## How to apply

Load the merged feature table (samples as columns, features as rows) and experimental metadata identifying batch identifiers for each sample into R or Python. Apply exploratory visualizations (PCA, heatmaps of sample-to-sample distances) stratified by batch assignment to assess whether samples cluster primarily by batch rather than by biological group. Quantify batch effects using variance decomposition (e.g., permutational MANOVA on batch vs. biological covariates) or batch-effect estimation methods (e.g., SVA surrogate variable estimation). Calculate effect sizes and p-values to determine whether batch variance is significant relative to biological signal. Use these metrics to decide whether batch correction is necessary and to establish a baseline for comparing pre- and post-correction signal recovery.

## Related tools

- **R** (statistical computing environment for variance decomposition, PCA, and batch effect estimation (e.g., SVA, ComBat)) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Jupyter Notebook** (interactive environment for exploratory data analysis, visualization, and batch effect quantification in Python or R) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **SVA (Surrogate Variable Analysis)** (R package for estimating and quantifying batch effects via surrogate variables)

## Evaluation signals

- PCA plots show clear sample clustering by batch assignment (batch effect present) or no batch-driven separation (batch effect absent).
- Permutational MANOVA p-value on batch term is < 0.05 (statistically significant batch effect) or > 0.05 (no significant batch effect).
- Variance partitioning shows batch explains > 10–20% of total variance (clinically/analytically significant).
- Surrogate variable estimates (from SVA) are uncorrelated with biological outcome of interest, indicating batch has been quantified separately from signal.
- Post-correction re-analysis shows reduced batch clustering in PCA and lower batch p-values, confirming correction efficacy.

## Limitations

- Batch detection assumes batch metadata is accurate and complete; missing or mislabeled batch assignments will yield spurious or false-negative results.
- Variance decomposition methods (e.g., MANOVA) assume linear batch effects; non-linear batch structure (e.g., instrument drift) may be underestimated.
- Small sample sizes per batch or highly imbalanced batch designs reduce statistical power to detect batch effects.
- Batch effects confounded with biological grouping (e.g., all samples from disease group in batch 1, controls in batch 2) cannot be reliably separated by detection methods alone.

## Evidence

- [other] FBMN-STATS workflow includes batch correction as a processing step applied to merged feature tables from non-targeted LC-MS/MS data, positioned after data merging and cleanup and before statistical analysis.: "batch correction as a processing step applied to merged feature tables from non-targeted LC-MS/MS data, positioned after data merging and cleanup and before statistical analysis"
- [readme] perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data"
- [other] Identify batch identifiers for each sample from the experimental metadata and apply batch correction using an appropriate method to remove batch effects while preserving biological signal.: "Identify batch identifiers for each sample from the experimental metadata. 3. Apply batch correction using an appropriate method (e.g., ComBat, SVA, or similar normalization technique) to remove"
