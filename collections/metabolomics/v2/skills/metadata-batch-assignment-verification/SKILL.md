---
name: metadata-batch-assignment-verification
description: Use when after data merging and before applying batch correction algorithms (ComBat, SVA, or normalization techniques) to a merged feature table from non-targeted LC-MS/MS metabolomics data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - R
  - Jupyter Notebook
  - Python
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

# metadata-batch-assignment-verification

## Summary

Verification that experimental batch identifiers are correctly assigned to each sample in the metadata prior to batch correction of merged LC-MS/MS feature tables. This skill ensures that batch labels match the actual instrumental run or processing group, preventing incorrect correction and preservation of true batch effects.

## When to use

After data merging and before applying batch correction algorithms (ComBat, SVA, or normalization techniques) to a merged feature table from non-targeted LC-MS/MS metabolomics data. Trigger: you have a merged feature table (samples as columns, features as rows) and experimental metadata, and need to confirm that batch identifiers in the metadata accurately reflect the instrumental or processing batches associated with each sample column.

## When NOT to use

- Batch identifiers are already embedded in the feature table column headers and do not require external metadata verification.
- The analysis is single-batch or does not require batch correction (e.g., all samples processed in one analytical run).
- Metadata has not yet been collected or is incomplete; metadata assembly must occur first.

## Inputs

- merged feature table (CSV/TSV format: samples as columns, features as rows)
- experimental metadata file (CSV/TSV with sample identifiers and batch identifiers)

## Outputs

- verified batch assignment report (confirmation that batch identifiers are present, unique, non-null, and correctly mapped to feature table samples)
- reconciled metadata file (if corrections were needed)

## How to apply

Load both the merged feature table and the experimental metadata into R or Python. Extract the batch identifiers from the metadata and cross-reference them against sample identifiers in the feature table columns. Verify that (1) every sample in the feature table has a corresponding batch assignment in the metadata, (2) batch labels are non-null and consistent (e.g., no mixed formats or typos), and (3) the order and naming of samples in both files match. Check that batches are logically grouped—e.g., samples processed on the same instrument run or within the same time window share the same batch identifier. If discrepancies are found, reconcile them before proceeding to batch correction, as incorrect batch assignment will either fail to remove true technical variation or falsely remove biological signal.

## Related tools

- **R** (Load and verify batch metadata against feature table structure; cross-reference sample identifiers and batch labels) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Jupyter Notebook** (Interactive environment for metadata inspection, validation, and reconciliation before batch correction) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Python** (Programmatic verification of batch assignment integrity (e.g., pandas dataframe alignment checks)) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS

## Examples

```
# R example
metadata <- read.csv('experimental_metadata.csv', row.names=1)
feature_table <- read.csv('merged_feature_table.csv', row.names=1)
all(colnames(feature_table) %in% rownames(metadata))
table(metadata$batch)
```

## Evaluation signals

- All samples in the feature table columns have exactly one non-null batch identifier in the metadata.
- Sample identifiers and order match between the feature table and metadata file (no missing or misaligned rows/columns).
- Batch identifiers are consistent in format (e.g., no mixed 'Batch_1' and 'batch1' spellings) and group samples logically by instrumental run or processing time.
- No sample appears in both the feature table and metadata but with conflicting batch assignments.
- Batch assignments, when plotted or summarized, show expected group sizes and temporal or instrumental patterns consistent with experimental design.

## Limitations

- Verification does not detect whether batch labels correctly reflect the true instrumental or temporal batches if metadata was mislabeled at collection time; it only checks structural consistency.
- Large datasets may require programmatic validation rather than manual inspection; visual spot-checks alone can miss systematic errors.
- If batch identifiers are numeric (e.g., 1, 2, 3) without descriptive labels, it may be difficult to verify correctness without reference to the original experimental logbook.

## Evidence

- [other] task_003 workflow step 2: "Identify batch identifiers for each sample from the experimental metadata."
- [other] task_003 workflow context: "Load the merged feature table (with samples as columns and features as rows) into R or Python."
- [readme] README workflow overview: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data"
- [other] task_003 batch correction context: "Apply batch correction using an appropriate method (e.g., ComBat, SVA, or similar normalization technique) to remove batch effects while preserving biological signal."
