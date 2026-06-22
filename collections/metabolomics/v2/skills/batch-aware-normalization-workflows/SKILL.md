---
name: batch-aware-normalization-workflows
description: Use when your LC-MS feature table exhibits intensity variations across samples that correlate with technical batches (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pycombat
  - Python/pandas
  - Asari
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm_cq
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-aware-normalization-workflows

## Summary

A normalization strategy for LC-MS metabolomics feature tables that corrects inter-sample intensity biases while accounting for batch structure, computing per-sample normalization factors independently within each batch before applying inter-batch normalization. This prevents batch effects from inflating or deflating normalization factors across the entire dataset.

## When to use

Your LC-MS feature table exhibits intensity variations across samples that correlate with technical batches (e.g., samples run on different days, instruments, or in separate MS acquisitions), and you need to normalize feature intensities while preserving true biological differences within and between batches. Use this when batch effects are suspected or documented in your sample metadata.

## When NOT to use

- Your samples do not have documented or suspected batch structure — use simple global normalization instead.
- Your feature table is already normalized by the feature detection software (e.g., Asari output marked as pre-normalized).
- Batch assignments are missing or unreliable for >5% of samples — address batch metadata quality first.

## Inputs

- feature table (TSV or CSV with samples as columns, features as rows, intensity values)
- sample metadata (CSV with sample identifiers and batch assignments)
- percentile threshold parameter (e.g., 0.90 for 90th percentile)

## Outputs

- batch-aware normalized feature table (TSV with same dimensions as input, intensity values rescaled)
- per-sample normalization factors (optional; useful for quality assessment)

## How to apply

First, load the feature table and sample metadata using Python/pandas, ensuring batch assignments are present in metadata. Filter the feature table to retain only features present in at least a specified percentile of samples (e.g., 90%), excluding zeros from presence counts—this removes rare or noisy features that would distort normalization factors. Calculate the per-sample TIC (total ion current, sum of intensities) across the filtered feature set for each sample. Within each batch independently, compute batch-specific median or mean TIC values, then calculate per-sample normalization factors as batch_reference_TIC / sample_TIC for that batch. Apply these factors to all features in the original (unfiltered) table. Finally, perform optional inter-batch normalization by computing global reference TIC across batches and adjusting batch-level medians/means relative to this global reference. Save the normalized feature table with a descriptive moniker (e.g., '_TIC_normalized_batch_aware') to the feature_tables subdirectory.

## Related tools

- **pycombat** (downstream batch correction after TIC normalization; harmonizes batch-specific distributions post-normalization)
- **Python/pandas** (core toolkit for loading feature tables, filtering features by percentile, computing TIC statistics, and applying per-sample normalization factors)
- **Asari** (upstream feature detection that produces the feature table input; may output pre-normalized features requiring re-normalization for batch awareness) — https://github.com/shuzhao-li/asari

## Examples

```
# Load feature table and metadata, filter to 90th percentile, compute batch-aware TIC normalization
import pandas as pd
feature_table = pd.read_csv('feature_table.tsv', sep='\t', index_col=0)
metadata = pd.read_csv('sample_metadata.csv', index_col=0)
for batch in metadata['batch'].unique():
    batch_samples = metadata[metadata['batch'] == batch].index
    batch_features = feature_table[batch_samples].loc[(feature_table[batch_samples] > 0).sum(axis=1) >= len(batch_samples) * 0.9]
    batch_tic = batch_features.sum(axis=0)
    norm_factors = batch_tic.median() / batch_tic
    feature_table.loc[:, batch_samples] = feature_table.loc[:, batch_samples].mul(norm_factors, axis=1)
feature_table.to_csv('feature_table_TIC_normalized_batch_aware.tsv', sep='\t')
```

## Evaluation signals

- Check that filtered feature set retains >80% of total original feature count and that percentile threshold is applied consistently across all samples.
- Verify that per-sample normalization factors are all positive, typically in range [0.5, 2.0], with batch-specific medians/means roughly equal across batches post-normalization.
- Confirm that samples within the same batch exhibit similar normalized TIC distributions before inter-batch normalization; inter-batch distributions should be more uniform after global normalization.
- Validate that feature intensity ranks and fold-changes between biological groups are preserved relative to unnormalized data (spot-check 5–10 known biomarkers or spike-in controls).
- Ensure output feature table has identical dimensions and feature/sample names as input; no rows or columns should be dropped.

## Limitations

- If batches are severely imbalanced (e.g., one batch contains <5% of samples), batch-specific TIC medians may be unstable; consider merging small batches or using robust statistics.
- Percentile-based feature filtering can be sensitive to the choice of threshold; features rare in one batch but common in another may be incorrectly excluded or retained.
- The method assumes that the relationship between TIC and true ion quantity is linear and consistent across batches; non-linear instrument drift or detector saturation could compromise correction.
- No automatic detection of batch structure from data; batch assignments must be manually curated in metadata.
- Inter-batch normalization step is optional in the workflow; omitting it preserves batch-level variation, which may or may not be desired depending on downstream analysis goals.

## Evidence

- [other] Filter features by a percentile threshold to include only common features, then calculates per-sample normalization factors using median or mean TIC (total ion current) from the filtered feature set, with options for batch-aware normalization where each batch is normalized independently before inter-batch normalization.: "Filter features by a percentile threshold to include only common features, then calculates per-sample normalization factors using median or mean TIC (total ion current) from the filtered feature set,"
- [other] Calculate the per-sample TIC (sum of intensities across filtered features) for each sample. Compute the normalization factor for each sample as either the median or mean TIC value across all samples, divided by that sample's TIC.: "Calculate the per-sample TIC (sum of intensities across filtered features) for each sample. Compute the normalization factor for each sample as either the median or mean TIC value across all samples,"
- [intro] Batch correction is performed using pycombat: "Batch correction is performed using pycombat"
- [intro] optionally blank masked, normalized, batch corrected, annotated or otherwise curated: "optionally blank masked, normalized, batch corrected, annotated or otherwise curated"
