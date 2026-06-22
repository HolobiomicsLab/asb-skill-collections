---
name: batch-correction-quality-assessment
description: Use when after applying pycombat-based batch correction to multi-batch interpolated feature tables in LC-MS metabolomics workflows, when you need to verify that batch effects have been attenuated without loss of data dimensionality or sample information.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ThermoRawFileParser
  - pycombat
  - Python
  - pcpfm
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

# Batch-Correction Quality Assessment

## Summary

Validate that batch correction via pycombat preserves the structural integrity of multi-batch metabolomics feature tables while demonstrating systematic reduction in inter-batch variance. This skill ensures corrected tables retain identical sample and feature dimensions and exhibit lower inter-batch intensity variance for shared features.

## When to use

After applying pycombat-based batch correction to multi-batch interpolated feature tables in LC-MS metabolomics workflows, when you need to verify that batch effects have been attenuated without loss of data dimensionality or sample information.

## When NOT to use

- Input data has not undergone imputation; apply imputation before batch correction.
- Samples lack batch metadata field or batch labels are missing; batch correction requires batch assignment.
- Single-batch study or all samples from one batch; inter-batch variance cannot be meaningfully assessed.

## Inputs

- Interpolated feature table (post-imputation) in TSV or tabular format
- Batch-corrected feature table output from pycombat via pcpfm batch_correct
- Sample metadata CSV with batch labels and sample identifiers

## Outputs

- Validation report confirming matching sample and feature counts
- Median inter-batch variance metrics for uncorrected vs. corrected tables
- Comparison demonstrating inter-batch variance reduction

## How to apply

Load the batch-corrected feature table and the corresponding uncorrected (post-imputation) table alongside sample metadata containing batch labels. Verify output table dimensions match input dimensions exactly (identical sample and feature counts). Calculate median inter-batch intensity variance for a subset of high-intensity features in both the uncorrected and corrected tables by grouping samples according to the batch metadata field. Confirm that corrected table median inter-batch variance is measurably lower than uncorrected median inter-batch variance, demonstrating successful batch effect attenuation. This comparison validates both the preservation of data structure and the effectiveness of batch correction.

## Related tools

- **pycombat** (Performs batch correction on multi-batch feature tables via parametric ComBat algorithm)
- **pcpfm** (Orchestrates batch correction pipeline step via batch_correct command with --by_batch parameter) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Python** (Used to load tables, calculate inter-batch variance statistics, and generate validation comparisons)

## Evaluation signals

- Output table has identical sample count to input table (no rows dropped or added)
- Output table has identical feature count to input table (no features dropped or added)
- Median inter-batch variance for high-intensity shared features is lower in corrected table than uncorrected table
- Batch variance reduction is consistent across multiple sampled high-intensity features
- No systematic loss of signal intensity or introduction of negative values in corrected table

## Limitations

- pycombat assumes parametric distributions of batch effects; may not perform optimally if batch effects are highly nonlinear or sample-dependent.
- Variance reduction assessment requires sufficient sample replication within each batch; batches with very few samples may yield unreliable inter-batch variance estimates.
- Quality of batch correction depends on proper batch label assignment in metadata; mislabeled or ambiguous batch assignments will compromise validation.
- Shared features used for variance comparison must be present across all batches; features unique to single batches cannot be assessed for inter-batch effects.

## Evidence

- [other] Does batch correction via pycombat preserve the structural integrity (sample and feature count) of multi-batch metabolomics feature tables while reducing inter-batch variance?: "Does batch correction via pycombat preserve the structural integrity (sample and feature count) of multi-batch metabolomics feature tables while reducing inter-batch variance?"
- [other] Batch correction using pycombat is applied to multi-batch interpolated feature tables via the by_batch flag, and the corrected table should retain identical sample and feature dimensions while systematically reducing inter-batch intensity variance for shared features.: "Batch correction using pycombat is applied to multi-batch interpolated feature tables via the by_batch flag, and the corrected table should retain identical sample and feature dimensions while"
- [other] Apply pycombat-based batch correction via the pcpfm batch_correct command with the --by_batch parameter specifying the batch metadata field.: "Apply pycombat-based batch correction via the pcpfm batch_correct command with the --by_batch parameter specifying the batch metadata field."
- [other] Verify that the output table has identical dimensions (sample count and feature count) to the input table. Calculate median inter-batch variance for a subset of high-intensity features in both uncorrected and corrected tables using sample grouping by the batch field.: "Verify that the output table has identical dimensions (sample count and feature count) to the input table. Calculate median inter-batch variance for a subset of high-intensity features in both"
- [readme] data normalization and batch correction: "data normalization and batch correction"
