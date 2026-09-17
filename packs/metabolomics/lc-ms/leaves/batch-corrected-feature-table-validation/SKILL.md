---
name: batch-corrected-feature-table-validation
description: Use when after applying batch correction (e.g., ComBat, SVA) to a merged
  feature table from non-targeted LC-MS/MS metabolomics data and before proceeding
  to univariate or multivariate statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3391
  tools:
  - R
  - Jupyter Notebook
  - Google Colab
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

# batch-corrected-feature-table-validation

## Summary

Validate that batch correction has successfully removed technical batch effects from merged LC-MS/MS metabolomics feature tables while preserving biological signal. This skill ensures the batch-corrected output is suitable for downstream statistical analysis by confirming effect removal and data integrity.

## When to use

After applying batch correction (e.g., ComBat, SVA) to a merged feature table from non-targeted LC-MS/MS metabolomics data and before proceeding to univariate or multivariate statistical analysis. Use this skill when you need to verify that batch-associated technical variation has been removed without artifactually inflating or suppressing biological differences between experimental groups.

## When NOT to use

- Input feature table has not yet been merged from individual sample runs — apply data merging first.
- Batch identifiers are unknown or not recorded in metadata — batch correction cannot be applied or validated without this information.
- Dataset contains only a single batch — batch correction is unnecessary and validation is not applicable.

## Inputs

- Merged feature table (CSV/TSV: samples as columns, features as rows)
- Batch identifiers for each sample (from experimental metadata)
- Original pre-correction feature table (for comparison)

## Outputs

- Batch-corrected feature table (CSV/TSV, matching original structure)
- Validation report with PCA/dimensionality reduction plots
- Batch effect quantification metrics (e.g., variance explained by batch before/after)

## How to apply

Load the batch-corrected feature table (samples as columns, features as rows) alongside the original batch identifiers and experimental metadata into R or Python. Visually inspect principal component analysis (PCA) or other dimensionality reduction plots to confirm that samples no longer cluster by batch but instead reflect biological grouping. Quantitatively assess batch effect removal by computing a batch effect metric (e.g., silhouette score, variance partition analysis) comparing pre- and post-correction tables; batch effect contribution should be substantially reduced. Verify data structure integrity: check for negative values (which may signal over-correction), confirm no features were inadvertently removed, and validate that sample and feature counts remain constant. If batch effects persist or biological signal is compromised, re-evaluate the batch correction method or its parameters before proceeding to statistical analysis.

## Related tools

- **R** (Primary environment for batch correction validation, exploratory data analysis, and statistical assessment using ComBat, SVA, or custom variance partitioning scripts.) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Jupyter Notebook** (Interactive computational environment for loading, processing, and visualizing batch-corrected feature tables with code cells and embedded plots.) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Google Colab** (Cloud-based Jupyter environment for running batch validation notebooks without local installation; supports R and Python kernels.) — https://colab.research.google.com/github/Functional-Metabolomics-Lab/FBMN-STATS/blob/main/R/Stats_Untargeted_Metabolomics.ipynb

## Examples

```
# R example: validate batch-corrected feature table using PCA and variance partitioning
prcomp(t(batch_corrected_table), scale = TRUE) %>% plot(); # PCA visualization
require(variancePartition); fitVP <- fitExtractVarPartModel(batch_corrected_table, ~ batch + phenotype, metadata); plotVarPart(fitVP); # Quantify batch vs. biological variance
```

## Evaluation signals

- PCA plots show samples clustering by experimental group/phenotype rather than by batch after correction; before-correction plots show batch-driven clustering.
- Batch effect quantification metric (e.g., variance explained by batch factor) is substantially lower in corrected vs. original table (target: >50% reduction).
- Feature table dimensions (rows = features, columns = samples) and value distributions remain consistent pre- and post-correction; no features are missing or duplicated.
- Corrected feature table contains no aberrant negative values; value ranges remain within expected bounds for the analytical method (e.g., MS intensity scale).
- Batch-corrected table passes structural validation: matches input column/row count, produces readable output in CSV/TSV format, and loads without parsing errors into downstream statistical tools.

## Limitations

- Batch correction efficacy depends on accurate batch labeling in metadata; mislabeled or partially labeled batches will compromise validation and downstream analysis.
- Over-correction using aggressive batch correction methods may artificially remove weak biological signals or introduce spurious patterns; visual and quantitative inspection is essential.
- Validation of batch effect removal is primarily visual (PCA) or heuristic (variance partitioning); no universally accepted statistical test for 'sufficient' batch removal is provided in the article.
- If batch and biological effect are confounded (e.g., all samples from treatment A run in batch 1, all controls in batch 2), batch correction cannot reliably separate them and may distort true biological differences.

## Evidence

- [other] Applied batch correction using ComBat, SVA, or similar normalization method to remove batch effects while preserving biological signal.: "Apply batch correction using an appropriate method (e.g., ComBat, SVA, or similar normalization technique) to remove batch effects while preserving biological signal."
- [readme] Batch correction is a processing step in the FBMN-STATS workflow for non-targeted LC-MS/MS metabolomics.: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data"
- [other] Feature table structure is maintained (samples as columns, features as rows) before and after batch correction.: "Load the merged feature table (with samples as columns and features as rows) into R or Python. Identify batch identifiers for each sample from the experimental metadata."
- [other] Batch correction is positioned after data merging and cleanup and before statistical analysis in the workflow.: "The FBMN-STATS workflow includes batch correction as a processing step applied to merged feature tables from non-targeted LC-MS/MS data, positioned after data merging and cleanup and before"
