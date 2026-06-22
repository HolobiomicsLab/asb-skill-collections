---
name: ion-current-calculation-and-aggregation
description: Use when when raw LC-MS feature tables exhibit inter-sample intensity variation due to instrument sensitivity drift, sample ionization efficiency differences, or loading differences, and you need to normalize intensities to a common reference scale before downstream statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Asari
  - PCPFM (PythonCentricPipelineForMetabolomics)
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

# ion-current-calculation-and-aggregation

## Summary

Compute per-sample total ion current (TIC) by summing feature intensities across a percentile-filtered feature set, then derive per-sample normalization factors as the ratio of global TIC median (or mean) to each sample's TIC. This enables intensity bias correction in untargeted LC-MS metabolomics datasets.

## When to use

When raw LC-MS feature tables exhibit inter-sample intensity variation due to instrument sensitivity drift, sample ionization efficiency differences, or loading differences, and you need to normalize intensities to a common reference scale before downstream statistical analysis. Apply this skill after feature detection but before batch correction or statistical testing, especially when samples were processed in multiple batches or acquired over extended instrument runs.

## When NOT to use

- Input is already a normalized or batch-corrected feature table—applying this skill would create double normalization and distort relative intensities.
- Feature table contains negative or zero-only intensities in the majority of samples—TIC calculation would be uninformative.
- Sample sizes are extremely small (< 5 samples) and a percentile threshold would filter out nearly all features, leaving insufficient features for robust TIC calculation.

## Inputs

- Feature intensity table (pandas DataFrame or TSV format with samples as columns, features as rows)
- Sample metadata (CSV or DataFrame containing batch assignments, if batch-aware normalization is desired)
- Percentile threshold (e.g., 90) for feature retention

## Outputs

- Normalized feature intensity table (TSV format, same structure as input, saved to feature_tables subdirectory)
- Per-sample normalization factors (optional; useful for QC and documentation)

## How to apply

Load the feature table and sample metadata into a pandas DataFrame. Filter the feature table to retain only features present in at least the specified percentile of samples (e.g., 90th percentile), excluding zero intensities from presence calculations—this ensures normalization uses only common, reliable features. For each sample, calculate its TIC by summing intensities across the filtered feature set. Then compute a global reference TIC (median or mean across all samples) and calculate each sample's normalization factor as reference_TIC / sample_TIC. Finally, multiply all intensities in the original (unfiltered) feature table by the corresponding normalization factor. For batch-aware normalization, apply these steps independently to each batch before performing inter-batch normalization. Save the normalized table to the feature_tables output directory with a new moniker.

## Related tools

- **Python** (Primary language for loading, filtering, and computing TIC and normalization factors using pandas and NumPy)
- **Asari** (Upstream tool that generates the initial feature table from mzML data; output fed into this normalization skill) — https://github.com/shuzhao-li/asari
- **PCPFM (PythonCentricPipelineForMetabolomics)** (End-to-end pipeline that orchestrates feature detection, normalization, batch correction, and annotation; this skill is a sub-step in the pipeline's data normalization stage) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics

## Examples

```
# Load feature table and metadata; filter features by 90th percentile presence; calculate per-sample TIC; compute normalization factors; apply to full table
import pandas as pd
feature_table = pd.read_csv('feature_table.tsv', sep='\t', index_col=0)
metadata = pd.read_csv('metadata.csv', index_col=0)
percentile_threshold = 90
features_present = (feature_table > 0).sum(axis=1) / len(feature_table.columns) * 100
filtered_features = feature_table[features_present >= percentile_threshold]
tic_per_sample = filtered_features.sum(axis=0)
tic_reference = tic_per_sample.median()
normalization_factors = tic_reference / tic_per_sample
normalized_table = feature_table.multiply(normalization_factors, axis=1)
normalized_table.to_csv('feature_tables/normalized_feature_table.tsv', sep='\t')
```

## Evaluation signals

- Verify that filtered feature set contains exactly the expected number of features (those present in ≥ percentile threshold of samples), and that feature count is > 0 and substantially less than the original feature count.
- Check that per-sample TIC values are all positive and roughly similar in magnitude (normalized TIC should cluster tightly around 1.0 for the global reference, with minimal outliers beyond 0.5–2.0 range).
- Confirm that the sum of normalized intensities across all features per sample is approximately constant (equal to reference TIC) for each sample.
- Validate that feature intensity distributions (e.g., median, interquartile range) are comparable across samples post-normalization, whereas pre-normalization they may show systematic bias correlated with batch or acquisition order.
- Ensure the normalized feature table has identical dimensions (features × samples) and row/column order as the input table, with all positive values preserved.

## Limitations

- Relies on assumption that a substantial fraction of features are common across samples; if many features are sparse or sample-specific, the percentile-filtered feature set may be small and normalization factors unstable.
- Does not account for feature-level ion suppression or differential ionization efficiency; uses only total signal. Features with extreme m/z or retention time may have systematically biased intensities post-normalization.
- Percentile threshold (e.g., 90%) is user-specified; inappropriate thresholds (too high or too low) can lead to feature loss or inclusion of noisy rare features, affecting normalization accuracy.
- Batch-aware normalization requires accurate batch assignments in metadata; mislabeled batches will propagate errors.
- Not suitable for data with strong spike-in standards or isotope-labeled internal controls, which should be excluded from TIC calculation but the skill does not automatically detect them.

## Evidence

- [other] Filter features by a percentile threshold to include only common features, then calculates per-sample TIC (sum of intensities across filtered features) for each sample.: "Filter features to retain only those present in at least the specified percentile of samples (e.g., 90%), excluding zeros from presence calculations. 3. Calculate the per-sample TIC (sum of"
- [other] Compute normalization factors as ratio of global TIC to per-sample TIC, with mean or median option.: "Compute the normalization factor for each sample as either the median or mean TIC value across all samples, divided by that sample's TIC."
- [other] Batch-aware normalization option normalizes each batch independently.: "with options for batch-aware normalization where each batch is normalized independently before inter-batch normalization"
- [readme] Normalization is part of the data normalization and batch correction workflow step.: "data normalization and batch correction"
- [readme] Apply normalization before downstream statistical analysis.: "Outputs are intended to be immediately usable for downstream analysis (e.g. MetaboAnalyst or common tools in R, Python etc.)"
