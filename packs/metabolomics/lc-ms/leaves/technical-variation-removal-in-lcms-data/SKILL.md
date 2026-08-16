---
name: technical-variation-removal-in-lcms-data
description: Use when after merging feature tables from non-targeted LC-MS/MS data and before statistical analysis, when samples were acquired across multiple instrument runs, different days, or instrumental calibration cycles.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - R
  - Jupyter Notebook
  - FBMN-STATS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Batch Correction in Non-Targeted LC-MS/MS Metabolomics

## Summary

Batch correction removes technical variation introduced during LC-MS/MS acquisition from merged feature tables while preserving biological signal. This skill is essential in non-targeted metabolomics workflows to enable valid statistical comparisons across samples acquired in different batches.

## When to use

Apply this skill after merging feature tables from non-targeted LC-MS/MS data and before statistical analysis, when samples were acquired across multiple instrument runs, different days, or instrumental calibration cycles. Batch effects are indicated by systematic clustering of samples by acquisition batch rather than biological condition in exploratory plots.

## When NOT to use

- Input feature table has not yet been merged from individual sample files
- Samples were all acquired in a single batch with no technical replication across instrument runs
- Batch identifiers are not clearly documented or unmappable to individual samples

## Inputs

- Merged feature table from non-targeted LC-MS/MS data (samples × features matrix)
- Experimental metadata file with batch identifiers mapped to each sample

## Outputs

- Batch-corrected feature table (same dimensions as input, CSV or TSV format)
- Quality control plots showing batch effect removal

## How to apply

Load the merged feature table (samples as columns, features as rows) into R or Python along with experimental metadata containing batch identifiers for each sample. Select an appropriate batch correction method such as ComBat or SVA that removes batch-associated technical variation while preserving biological signal. Apply the chosen normalization technique to the feature table, ensuring that the corrected output maintains the same dimensions and sample/feature structure as the input. Export the batch-corrected feature table to CSV or TSV format preserving the original input structure for downstream statistical analysis.

## Related tools

- **R** (Primary computation environment for implementing batch correction methods (ComBat, SVA) on feature tables) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Jupyter Notebook** (Interactive notebook environment for running batch correction workflow reproducibly in R or Python) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **FBMN-STATS** (Dedicated workflow repository containing pre-built notebooks implementing batch correction within the full FBMN-STATS pipeline) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS

## Examples

```
# In R within Jupyter Notebook or Colab:
metadata <- read.csv('sample_metadata.csv', row.names=1)
batch_ids <- metadata$batch
feature_table_corrected <- ComBat(dat=feature_table, batch=batch_ids, par.prior=TRUE)
write.csv(feature_table_corrected, 'batch_corrected_features.csv')
```

## Evaluation signals

- Batch-corrected feature table has identical dimensions to input (same number of samples and features)
- Principal component analysis (PCA) or other unsupervised ordination shows reduced clustering by batch and retention of biological condition separation
- Distribution of feature intensities across samples remains consistent before and after correction (no artificial signal amplification or loss)
- CSV/TSV output file matches original input format and can be directly imported into downstream statistical analysis tools
- Batch identifiers no longer correlate significantly with principal components in corrected data when tested via permutation or linear regression

## Limitations

- Batch correction methods assume systematic (not random) batch effects; small or highly irregular batch effects may be under-corrected
- Over-correction can remove true biological variation if biological conditions are confounded with batch; experimental design should minimize batch-condition confounding
- Methods like ComBat require sufficient samples per batch to estimate batch parameters accurately; severely imbalanced batch designs may fail
- Corrected values may become negative or violate the typical non-negative intensity bounds of MS data; users should verify biological plausibility of corrected intensities

## Evidence

- [other] The FBMN-STATS workflow includes batch correction as a processing step applied to merged feature tables from non-targeted LC-MS/MS data, positioned after data merging and cleanup and before statistical analysis.: "batch correction as a processing step applied to merged feature tables from non-targeted LC-MS/MS data, positioned after data merging and cleanup and before statistical analysis"
- [other] Apply batch correction using an appropriate method (e.g., ComBat, SVA, or similar normalization technique) to remove batch effects while preserving biological signal.: "Apply batch correction using an appropriate method (e.g., ComBat, SVA, or similar normalization technique) to remove batch effects while preserving biological signal"
- [readme] perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks.: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data"
- [other] Load the merged feature table (with samples as columns and features as rows) into R or Python.: "Load the merged feature table (with samples as columns and features as rows) into R or Python"
- [other] Export the batch-corrected feature table to a CSV or TSV file matching the original input structure.: "Export the batch-corrected feature table to a CSV or TSV file matching the original input structure"
