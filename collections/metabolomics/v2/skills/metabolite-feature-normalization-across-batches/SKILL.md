---
name: metabolite-feature-normalization-across-batches
description: Use when after data merging and cleanup (blank removal) and before univariate or multivariate statistical analysis, when your merged feature table (samples as columns, metabolite features as rows) contains samples processed in different MS batches or instrumental runs that may introduce systematic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - Jupyter Notebook
  - Google Colab
  - FBMN-STATS web app
  techniques:
  - LC-MS
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

# metabolite-feature-normalization-across-batches

## Summary

Removes batch-associated technical variation from merged LC-MS/MS metabolomics feature tables while preserving biological signal, using statistical batch correction methods. This step is critical in the FBMN-STATS workflow to ensure fair downstream statistical comparisons when samples were processed across multiple instrumental runs or MS batches.

## When to use

Apply this skill after data merging and cleanup (blank removal) and before univariate or multivariate statistical analysis, when your merged feature table (samples as columns, metabolite features as rows) contains samples processed in different MS batches or instrumental runs that may introduce systematic technical bias unrelated to your biological question.

## When NOT to use

- If your feature table has not yet been merged from individual sample files or has not undergone blank removal and cleanup.
- If all samples were processed in a single batch with no known batch variable or instrumental heterogeneity.
- If batch is confounded with your primary biological variable of interest (e.g., all diseased samples in batch 1, all healthy in batch 2), as batch correction may remove genuine biological signal.

## Inputs

- Merged metabolomics feature table (TSV or CSV: samples × features, with feature intensity or abundance values)
- Experimental metadata table with batch identifier for each sample

## Outputs

- Batch-corrected feature table (TSV or CSV: samples × features, matching original input structure)
- Quality control metrics or diagnostic plots showing batch effect removal

## How to apply

Load the merged feature table (CSV or TSV format with samples as columns and features as rows) into R or Python alongside experimental metadata containing batch identifiers for each sample. Identify and flag which samples belong to each batch. Apply a batch correction method such as ComBat or SVA to normalize feature intensities across batches, removing batch-associated variance while preserving the biological signal of interest. The corrected feature table should maintain the original data structure (samples as columns, features as rows) and be exported to CSV/TSV for downstream statistical analysis. Rationale: batch effects are unintended systematic variation from instrumental drift, reagent lots, or run date differences; removing them ensures that observed differences in statistical analysis reflect true biological variation rather than technical artifacts.

## Related tools

- **R** (Host language for implementing batch correction using packages such as ComBat or SVA) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS/blob/main/R/Stats_Untargeted_Metabolomics.ipynb
- **Jupyter Notebook** (Interactive environment for executing batch correction pipelines in R or Python) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Google Colab** (Cloud-based Jupyter environment for running batch correction without local installation) — https://colab.research.google.com/github/Functional-Metabolomics-Lab/FBMN-STATS/blob/main/R/Stats_Untargeted_Metabolomics.ipynb
- **FBMN-STATS web app** (Streamlit-hosted implementation of batch correction for smaller datasets without code) — https://fbmn-stats.streamlit.app/

## Evaluation signals

- Batch identifiers are correctly mapped to all samples and no batch assignments are missing or misclassified.
- Feature intensity distributions show reduced systematic differences between batches in PCA or distribution plots before and after correction.
- Biological replicate samples cluster together after batch correction, while distinct biological groups remain separated.
- Feature table maintains original dimensions (same number of samples and features) and no features or samples are inadvertently removed.
- Corrected feature values remain within expected intensity ranges for metabolomics data and show no obvious artifacts (e.g., negative intensities if the original data were non-negative).

## Limitations

- Batch correction assumes that batch and biological effects are separable; severe confounding between batch and phenotype can lead to loss of biological signal.
- Different batch correction methods (ComBat, SVA, etc.) may yield different results; method choice should be justified and validated via cross-validation or independent datasets.
- Effectiveness depends on having sufficient samples per batch and adequate representation of biological variation within each batch; small, imbalanced batch designs may lead to overcorrection.
- Batch correction is most reliable when batch information is known and accurately recorded in metadata; unknown or misclassified batches will reduce performance.

## Evidence

- [other] The FBMN-STATS workflow includes batch correction as a processing step applied to merged feature tables from non-targeted LC-MS/MS data, positioned after data merging and cleanup and before statistical analysis.: "The FBMN-STATS workflow includes batch correction as a processing step applied to merged feature tables from non-targeted LC-MS/MS data, positioned after data merging and cleanup and before"
- [other] Load the merged feature table (with samples as columns and features as rows) into R or Python. Identify batch identifiers for each sample from the experimental metadata. Apply batch correction using an appropriate method (e.g., ComBat, SVA, or similar normalization technique) to remove batch effects while preserving biological signal.: "Load the merged feature table (with samples as columns and features as rows) into R or Python. Identify batch identifiers for each sample from the experimental metadata. Apply batch correction using"
- [readme] perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks."
- [other] Export the batch-corrected feature table to a CSV or TSV file matching the original input structure.: "Export the batch-corrected feature table to a CSV or TSV file matching the original input structure."
