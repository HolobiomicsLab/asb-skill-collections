---
name: batch-effect-variance-quantification
description: Use when after running pycombat batch correction on multi-batch metabolomics feature tables when you need to validate that batch correction has successfully attenuated inter-batch intensity variance without altering the structural integrity (sample and feature counts) of the corrected table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - ThermoRawFileParser
  - pycombat
  - Python
  - pcpfm batch_correct
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- Batch correction is performed using pycombat.
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
---

# batch-effect-variance-quantification

## Summary

Quantify inter-batch intensity variance in metabolomics feature tables before and after batch correction to validate that correction preserves sample/feature dimensions while reducing batch effects. This skill measures the efficacy of batch correction by comparing median inter-batch variance metrics on shared features across batches.

## When to use

Apply this skill after running pycombat batch correction on multi-batch metabolomics feature tables when you need to validate that batch correction has successfully attenuated inter-batch intensity variance without altering the structural integrity (sample and feature counts) of the corrected table. Use it as a post-correction QC step to confirm that the corrected table is suitable for downstream statistical analysis.

## When NOT to use

- Input is already a batch-corrected feature table (redundant application)
- Sample metadata does not contain a batch field or batch assignments are missing/unreliable
- Feature table has very few high-intensity features (subset selection becomes unreliable; may require adjustment of intensity threshold)

## Inputs

- Interpolated feature table (post-imputation, .tsv or similar tabular format with features as rows, samples as columns)
- Sample metadata CSV with batch labels/identifiers

## Outputs

- Dimension check result (sample count and feature count match input)
- Median inter-batch variance for uncorrected table (numeric)
- Median inter-batch variance for corrected table (numeric)
- Variance reduction ratio or comparison (corrected/uncorrected)

## How to apply

Load the interpolated (post-imputation) feature table and sample metadata containing batch labels. Apply pycombat-based batch correction via the pcpfm batch_correct command with the --by_batch parameter specifying the batch metadata field. Verify that the output table has identical dimensions (sample count and feature count) to the input table using a simple shape check. Then, select a subset of high-intensity features and calculate median inter-batch intensity variance separately for the uncorrected and corrected tables by grouping samples by the batch field. The corrected table's median inter-batch variance should be substantially lower than the uncorrected median, demonstrating successful batch effect attenuation. Compare these two variance metrics as the primary validation signal.

## Related tools

- **pycombat** (Batch correction engine applied via --by_batch flag to remove inter-batch intensity variance from multi-batch feature tables)
- **pcpfm batch_correct** (Command-line interface wrapping pycombat batch correction with metadata-driven batch specification) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Python** (Computing environment for loading tables, grouping samples by batch, and calculating variance metrics)

## Examples

```
pcpfm batch_correct --input interpolated_table.tsv --metadata samples.csv --by_batch batch_field --output corrected_table.tsv
```

## Evaluation signals

- Output feature table has identical row count (features) and column count (samples) as input feature table
- Median inter-batch variance calculated on corrected table is lower (typically 20–50% reduction or greater) than median variance on uncorrected table
- Variance reduction is consistent across a representative subset of high-intensity features, not driven by outlier features
- No NaN, Inf, or negative variance values in calculations; all intensity values present before and after correction
- Batch grouping in metadata matches sample annotations in the feature table without missing or misaligned batch assignments

## Limitations

- Variance quantification depends on selection of high-intensity features; thresholds for 'high-intensity' must be chosen a priori and may differ across datasets
- Median inter-batch variance is a summary statistic and may mask heterogeneous correction across different feature classes (e.g., lipids vs. amino acids)
- The skill does not assess whether batch correction introduces bias in biological signal or alters feature covariance structure; it is narrowly focused on batch variance reduction
- Batch correction efficacy may be limited if batch effects are confounded with biological covariates (e.g., phenotype correlated with collection date)

## Evidence

- [other] Batch correction using pycombat is applied to multi-batch interpolated feature tables via the by_batch flag, and the corrected table should retain identical sample and feature dimensions while systematically reducing inter-batch intensity variance for shared features.: "Batch correction using pycombat is applied to multi-batch interpolated feature tables via the by_batch flag, and the corrected table should retain identical sample and feature dimensions while"
- [other] Load the interpolated feature table (post-imputation) and sample metadata containing batch labels. Apply pycombat-based batch correction via the pcpfm batch_correct command with the --by_batch parameter specifying the batch metadata field.: "Load the interpolated feature table (post-imputation) and sample metadata containing batch labels. Apply pycombat-based batch correction via the pcpfm batch_correct command with the --by_batch"
- [other] Verify that the output table has identical dimensions (sample count and feature count) to the input table. Calculate median inter-batch variance for a subset of high-intensity features in both uncorrected and corrected tables using sample grouping by the batch field.: "Verify that the output table has identical dimensions (sample count and feature count) to the input table. Calculate median inter-batch variance for a subset of high-intensity features in both"
- [other] Confirm that corrected table median inter-batch variance is lower than uncorrected median inter-batch variance, demonstrating successful batch effect attenuation.: "Confirm that corrected table median inter-batch variance is lower than uncorrected median inter-batch variance, demonstrating successful batch effect attenuation."
- [readme] data normalization and batch correction: "data normalization and batch correction"
