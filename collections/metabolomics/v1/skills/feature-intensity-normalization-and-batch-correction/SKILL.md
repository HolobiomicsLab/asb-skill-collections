---
name: feature-intensity-normalization-and-batch-correction
description: Use when after blank masking and sample dropping, when you have a feature table with intensity values that exhibit systematic variation across sample collection batches or instrument runs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - ThermoRawFileParser
  - Asari
  - khipu
  - pycombat
  - PCPFM (Python-Centric Pipeline for Metabolomics)
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
- convert Thermo .raw to mzML (ThermoRawFileParser)
- process mzML data to feature tables (Asari)
- pre-annotation to group featues to empirical compounds (khipu)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
---

# feature-intensity-normalization-and-batch-correction

## Summary

Normalize LC-MS feature intensities using total ion chromatogram (TIC) scaling on common features, optionally followed by batch-aware correction to remove systematic intensity variation across experimental batches. This skill removes confounding batch effects while preserving biological signal in metabolomics feature tables.

## When to use

Apply this skill after blank masking and sample dropping, when you have a feature table with intensity values that exhibit systematic variation across sample collection batches or instrument runs. Use it when batch identifiers are available in your metadata and you observe batch-driven clustering in exploratory analysis (PCA, t-SNE) despite biological homogeneity within batches. Do NOT apply if samples are from a single batch or instrument run, or if batch information is unavailable.

## When NOT to use

- Input is already a batch-corrected or normalized feature table from a previous processing step
- Samples originate from a single batch or instrument run with no batch metadata
- Feature table contains fewer than 10–20 common features above the percentile threshold (normalization basis becomes unstable)

## Inputs

- Feature intensity table (TSV/CSV format) with features as rows, samples as columns
- Sample metadata CSV with batch identifiers and sample type fields
- Feature detection results (full or preferred feature table from Asari)

## Outputs

- Normalized feature intensity table (TSV format)
- Optionally, batch-corrected feature table if pycombat applied
- Normalization parameters and batch correction model (for reproducibility)

## How to apply

First, normalize feature intensities using TIC-based scaling: identify common features (those present above a specified percentile threshold, typically the 90th percentile) in each sample, compute total intensity of these common features, and scale all features in that sample by the ratio of its TIC to a reference (e.g., median TIC across all samples). This corrects for instrument sensitivity drift and sample loading variation. If multiple batches are present, apply optional batch-aware two-step normalization: first normalize intensities within each batch independently, then apply between-batch normalization using a method such as pycombat (empirical Bayes adjustment) to harmonize intensity distributions across batches while preserving within-batch biological patterns. Use the PCPFM pcpfm normalize command with configurable percentile cutoff (default 90%) for common feature selection.

## Related tools

- **Asari** (Produces full and preferred feature intensity tables that serve as input to normalization) — https://github.com/shuzhao-li/asari
- **pycombat** (Performs empirical Bayes batch correction after TIC normalization)
- **PCPFM (Python-Centric Pipeline for Metabolomics)** (Orchestrates the normalization workflow via pcpfm normalize command with configurable parameters) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics

## Examples

```
pcpfm normalize --experiment_dir ./my_experiment --intensity_table asari_results/preferred_Feature_table.tsv --percentile_cutoff 90 --batch_aware True
```

## Evaluation signals

- Verify that the sum (or median) of TIC across all samples converges to a constant or narrow range after normalization, indicating successful intensity scaling
- Check that common features (above percentile threshold) retain relative rank order across samples before and after normalization, confirming biological signal preservation
- If batch correction applied: PCA plot of corrected table should show reduced batch-driven clustering while preserving within-group (biological) structure
- Inspect the distribution of normalized intensities per feature across samples — should be roughly symmetric after log-transformation, with no extreme outliers
- If known biological contrasts exist (e.g., disease vs. control), validate that effect sizes (fold-change, t-test p-values) on key features do not reverse or collapse after normalization

## Limitations

- TIC normalization assumes that common features (>90th percentile) are not themselves systematically altered by biological condition; if treatment preferentially suppresses or amplifies many high-abundance metabolites, normalization basis may be biased.
- Percentile threshold selection (default 90%) is empirical; datasets with very high or very low feature density may require threshold adjustment to ensure sufficient common features for stable normalization.
- Batch correction via pycombat assumes batch effects are additive on the log-intensity scale; multiplicative or non-linear batch effects may not be fully corrected.
- Pipeline does not currently support GC-MS or other non-LC data types, limiting applicability to untargeted LC-MS metabolomics.
- Missing data imputation (if performed before normalization) can artificially inflate common feature prevalence and bias TIC calculation; order of operations matters.

## Evidence

- [other] Normalize feature intensities using pcpfm normalize with TIC based on common features at specified percentile cutoff (default 90%); optionally apply batch-aware two-step normalization (within-batch then between-batch).: "Normalize feature intensities using pcpfm normalize with TIC based on common features at specified percentile cutoff (default 90%); optionally apply batch-aware two-step normalization (within-batch"
- [intro] data normalization and batch correction: "data normalization and batch correction"
- [readme] The pipeline can ... data normalization and batch correction ... output data in standardized formats (.txt, JSON), ready for downstream analysis: "data normalization and batch correction ... output data in standardized formats (.txt, JSON), ready for downstream analysis"
- [other] optional batch correction using pycombat: "optional batch correction using pycombat"
