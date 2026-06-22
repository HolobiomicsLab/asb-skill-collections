---
name: percentile-feature-filtering-for-normalization
description: Use when you have a raw or pre-processed LC-MS feature table with multiple samples and need to normalize for inter-sample intensity biases before downstream statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Python/pandas
  - PCPFM (PythonCentricPipelineForMetabolomics)
  - Asari
  - pycombat
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

# percentile-feature-filtering-for-normalization

## Summary

Filter metabolomics feature tables to retain only common features present across a minimum percentile of samples, then use this filtered feature set to compute per-sample normalization factors (median or mean TIC) for inter-sample intensity correction. This reduces noise from rare features and stabilizes normalization in untargeted LC-MS metabolomics workflows.

## When to use

Apply this skill when you have a raw or pre-processed LC-MS feature table with multiple samples and need to normalize for inter-sample intensity biases before downstream statistical analysis. Use it specifically when you want to exclude infrequent features (which may be noise or sample-specific artifacts) from the normalization factor calculation, ensuring that normalization is driven by robust, commonly-detected metabolites rather than outlier or rare features.

## When NOT to use

- Input is already a normalized or batch-corrected feature table; re-normalizing may introduce spurious scaling artifacts.
- Sample count is very small (n < 5–10) such that percentile-based filtering removes nearly all features or becomes unstable.
- Feature table is already filtered to a curated set of target compounds; percentile filtering may remove intentionally-selected compounds.

## Inputs

- feature table (TSV/CSV: rows=features, columns=samples, values=ion intensities)
- sample metadata (CSV: including sample type, batch identifier if applicable)
- percentile threshold parameter (0–100; commonly 80–95%)

## Outputs

- normalized feature table (same dimensions as input, intensity values scaled)
- normalization factor vector (per-sample scaling coefficients used)
- log or metadata documenting which features were retained for normalization

## How to apply

Load the feature table (rows = features, columns = samples) and sample metadata using pandas. Define a percentile threshold (e.g., 90%) and identify features present in at least that percentile of samples, excluding zero intensities from presence calculations. Calculate per-sample TIC as the sum of intensities across only the filtered feature set. Compute the normalization factor for each sample as either the median or mean TIC value across all samples divided by that sample's TIC. If batch information is available in metadata, apply normalization independently within each batch before inter-batch normalization. Multiply all feature intensities in the original (unfiltered) table by the corresponding per-sample normalization factor. Save the normalized feature table to the feature_tables subdirectory with a descriptive moniker reflecting the normalization method and parameters applied.

## Related tools

- **Python/pandas** (Load, filter, and manipulate feature tables and metadata; compute per-sample TIC and normalization factors)
- **PCPFM (PythonCentricPipelineForMetabolomics)** (End-to-end LC-MS preprocessing pipeline that integrates this normalization filter as a configurable step before downstream analysis) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Asari** (Generates the initial feature table from mzML files; outputs are then normalized using this percentile-filter approach) — https://github.com/shuzhao-li/asari
- **pycombat** (Applied after normalization for batch correction when samples span multiple analytical batches)

## Examples

```
# Pseudocode example grounded in the workflow description:
import pandas as pd
feature_table = pd.read_csv('feature_table.tsv', sep='\t', index_col=0)
percentile_threshold = 90
features_in_percentile = (feature_table > 0).sum(axis=1) >= (percentile_threshold / 100 * feature_table.shape[1])
filtered_features = feature_table[features_in_percentile]
per_sample_tic = filtered_features.sum(axis=0)
median_tic = per_sample_tic.median()
norm_factors = median_tic / per_sample_tic
normalized_table = feature_table.multiply(norm_factors, axis=1)
normalized_table.to_csv('normalized_feature_table.tsv', sep='\t')
```

## Evaluation signals

- Verify that the filtered feature set contains exactly those features present in ≥ percentile_threshold of samples (spot-check a few features at the threshold boundary).
- Check that per-sample TIC values computed from filtered features are reasonable (no negative, zero, or extreme outlier values; within expected LC-MS intensity ranges).
- Confirm that normalized feature table has same dimensions (rows, columns) as input and that all intensities are positive and reasonably scaled (global median or mean TIC across samples should be ~1.0 after normalization).
- Validate that samples with high TIC receive downscaling (normalization factor < 1) and samples with low TIC receive upscaling (normalization factor > 1), consistent with the intention to correct inter-sample biases.
- If batch-aware normalization was applied, confirm that within-batch normalization occurred before inter-batch normalization by inspecting sample-level TIC homogeneity within and across batches.

## Limitations

- Percentile threshold is user-defined and not automatically optimized; inappropriate thresholds (too low, too high) may retain noise or discard genuine rare metabolites.
- Does not account for biochemical differences between sample types (e.g., disease vs. control); all samples contribute equally to the normalization reference, which may mask true biological differences if one group has systematically different TIC profiles.
- Median or mean TIC selection can yield different results in skewed distributions; the paper does not provide guidance on choosing between them for specific experimental designs.
- The approach assumes that the filtered feature set is representative of global metabolite abundance; if the percentile threshold is very stringent, normalization may be driven by a non-representative subset of abundant compounds.
- No explicit support for QC sample handling within this step; QC samples should be pre-filtered (marked and excluded) before normalization to avoid skewing the normalization reference.

## Evidence

- [other] Filter features to retain only those present in at least the specified percentile of samples (e.g., 90%), excluding zeros from presence calculations.: "Filter features to retain only those present in at least the specified percentile of samples (e.g., 90%), excluding zeros from presence calculations."
- [other] Calculate the per-sample TIC (sum of intensities across filtered features) for each sample.: "Calculate the per-sample TIC (sum of intensities across filtered features) for each sample."
- [other] Compute the normalization factor for each sample as either the median or mean TIC value across all samples, divided by that sample's TIC.: "Compute the normalization factor for each sample as either the median or mean TIC value across all samples, divided by that sample's TIC."
- [other] with options for batch-aware normalization where each batch is normalized independently before inter-batch normalization.: "with options for batch-aware normalization where each batch is normalized independently before inter-batch normalization."
- [readme] data normalization and batch correction: "data normalization and batch correction"
- [other] Drop infrequent features based on feature retention percentile: "Drop infrequent features based on feature retention percentile"
