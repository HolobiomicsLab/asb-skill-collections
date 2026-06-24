---
name: tic-based-intensity-scaling
description: Use when after feature detection when you have a metabolomics feature
  table with intensity values across multiple samples and observe evidence of inter-sample
  intensity bias (e.g., batch effects, variable ionization efficiency, or instrument
  drift).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0092
  tools:
  - Python
  - pandas
  - Asari
  - pycombat
  techniques:
  - LC-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# TIC-based intensity scaling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Normalize LC-MS metabolomics feature tables by correcting inter-sample intensity biases using total ion current (TIC) computed from high-frequency features. This addresses systematic variation in ionization efficiency and instrument response across samples, ensuring fair downstream statistical comparison.

## When to use

Apply this skill after feature detection when you have a metabolomics feature table with intensity values across multiple samples and observe evidence of inter-sample intensity bias (e.g., batch effects, variable ionization efficiency, or instrument drift). The skill is especially appropriate when samples have been processed in a single batch or when you need sample-level normalization before batch correction.

## When NOT to use

- Input is already a batch-corrected feature table (applying TIC normalization post-correction may reintroduce batch effects).
- Fewer than ~10–20 samples per group or batch; TIC estimation becomes unstable with very small cohorts.
- Feature table contains many features with dropout or missingness >50%; the percentile filter may retain too few features, yielding unreliable TIC estimates.

## Inputs

- LC-MS feature intensity table (tsv, csv, or pandas DataFrame; rows=features, columns=samples)
- Sample metadata file (csv; must include sample identifiers and optionally batch labels)

## Outputs

- Normalized LC-MS feature intensity table (same format and structure as input, with scaled intensities)
- Normalization factors per sample (optional metadata record for QC and reproducibility)

## How to apply

Load the feature table and sample metadata using Python/pandas. Filter features to retain only those present in at least a specified percentile of samples (e.g., 90th percentile), excluding zeros from presence calculations—this step selects a robust, common feature set less prone to biological or technical dropout. Calculate the per-sample TIC by summing intensities across the filtered feature set for each sample. Compute the normalization factor for each sample as the median (or mean) TIC across all samples, divided by that individual sample's TIC; this factor accounts for the scale of ionization for that sample relative to the cohort average. Multiply all feature intensities in the original (unfiltered) feature table by the corresponding per-sample normalization factor. Optionally apply batch-aware normalization where each batch is normalized independently before inter-batch normalization. Save the normalized feature table to the feature_tables subdirectory with a descriptive moniker indicating the normalization method applied.

## Related tools

- **Python** (Language and runtime for feature filtering, TIC calculation, and intensity scaling operations) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **pandas** (Library for loading, filtering, and manipulating feature tables and sample metadata)
- **Asari** (Upstream feature detection tool that generates the input feature table for normalization) — https://github.com/shuzhao-li-lab/asari
- **pycombat** (Downstream batch correction tool often applied after TIC normalization for multi-batch studies)

## Examples

```
# Load table, filter to 90th percentile of presence, compute per-sample TIC, and scale
import pandas as pd
feature_table = pd.read_csv('feature_table.tsv', sep='\t', index_col=0)
percentile_threshold = 0.9
features_present = (feature_table > 0).sum(axis=1) / feature_table.shape[1]
filtered_features = features_present[features_present >= percentile_threshold].index
tic_per_sample = feature_table.loc[filtered_features].sum(axis=0)
median_tic = tic_per_sample.median()
norm_factors = median_tic / tic_per_sample
normalized_table = feature_table.mul(norm_factors, axis=1)
normalized_table.to_csv('feature_table_tic_normalized.tsv', sep='\t')
```

## Evaluation signals

- Verify that the percentile filter retains a consistent, non-empty feature subset across all samples (typically 50–95% of original features for a 90th percentile threshold).
- Check that per-sample normalization factors are positive, close to 1 in median, and show expected variance (e.g., CV < 20–30% for well-controlled experiments).
- Confirm that total feature intensities (summed across all features) are now similar across samples post-normalization, especially within-batch or within-sample-type groups.
- Inspect PCA or other unsupervised clustering on the normalized table; inter-sample intensity biases should be visually reduced compared to the unnormalized table.
- Verify that the normalized feature table has the same dimensions (rows and columns) as the input, with no missing or NaN values introduced by the scaling operation.

## Limitations

- TIC normalization assumes that the majority of detected features are stable across samples; if true biological differences dominate or if many features are truly absent in some samples, TIC may conflate biology with technical bias.
- The choice of percentile threshold (e.g., 90th vs. 80th) is somewhat arbitrary; results are sensitive to this parameter, especially for small cohorts or datasets with large numbers of rare or sparse features.
- Batch-aware normalization (separate per-batch TIC calculation) requires accurate batch labels in the sample metadata; mislabeled batches will propagate errors.
- This skill does not address non-linear or multiplicative batch effects; if batch effects are non-linear or sample-type dependent, downstream batch correction (e.g., pycombat) or more sophisticated approaches may be needed.
- No internal spike-in standards for QC support is implemented; normalized tables lack an absolute external reference to validate the magnitude of correction applied.

## Evidence

- [other] Filter features to retain only those present in at least the specified percentile of samples (e.g., 90%), excluding zeros from presence calculations.: "Filter features to retain only those present in at least the specified percentile of samples (e.g., 90%), excluding zeros from presence calculations."
- [other] Calculate the per-sample TIC (sum of intensities across filtered features) for each sample.: "Calculate the per-sample TIC (sum of intensities across filtered features) for each sample."
- [other] Compute the normalization factor for each sample as either the median or mean TIC value across all samples, divided by that sample's TIC.: "Compute the normalization factor for each sample as either the median or mean TIC value across all samples, divided by that sample's TIC."
- [other] Multiply all feature intensities in the original table by the corresponding per-sample normalization factor.: "Multiply all feature intensities in the original table by the corresponding per-sample normalization factor."
- [other] with options for batch-aware normalization where each batch is normalized independently before inter-batch normalization: "with options for batch-aware normalization where each batch is normalized independently before inter-batch normalization."
- [readme] data normalization and batch correction: "data normalization and batch correction"
- [readme] This feature table can then be optionally blank masked, normalized, batch corrected, annotated or otherwise curated: "This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM"
