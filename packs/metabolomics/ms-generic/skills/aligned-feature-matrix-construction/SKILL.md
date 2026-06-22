---
name: aligned-feature-matrix-construction
description: Use when when you have extracted feature tables from multiple breath samples (mzML/mzXML files) using feature extraction, and you need to identify which features are the same across samples to enable downstream statistical or comparative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - BreathXplorer
  - pandas
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/jasms.4c00152
  title: BreathXplorer
evidence_spans:
- '[![PyPI](https://img.shields.io/pypi/pyversions/breathXplorer)]'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_breathxplorer_cq
    doi: 10.1021/jasms.4c00152
    title: BreathXplorer
  dedup_kept_from: coll_breathxplorer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00152
  all_source_dois:
  - 10.1021/jasms.4c00152
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# aligned-feature-matrix-construction

## Summary

Consolidate per-sample feature tables (each containing m/z, retention time, and intensity measurements) into a single unified aligned feature matrix by matching corresponding features across samples and aggregating their intensities. This skill is essential for multi-sample comparative metabolomics analysis in breath VOC profiling.

## When to use

When you have extracted feature tables from multiple breath samples (mzML/mzXML files) using feature extraction, and you need to identify which features are the same across samples to enable downstream statistical or comparative analysis. Specifically, apply this skill after individual FeatureSet objects have been created and optionally filtered by RSD, but before any cross-sample intensity comparisons or statistical tests.

## When NOT to use

- Input is already a single aligned feature table (e.g., already in aligned-table CSV format) — skip directly to downstream analysis.
- You have only one sample or no need for cross-sample comparison — use individual FeatureSet.to_csv() instead.
- Input feature tables are in formats other than mzML/mzXML or have not been extracted with find_feature() — pre-alignment data munging may be required.

## Inputs

- list of FeatureSet objects (one per sample, each containing m/z, scan_time, intensity, and RSD)
- list of sample names (strings, customizable identifiers for each sample)

## Outputs

- Sample object (contains aligned features, m/z values, sample names, and aggregated intensities)
- aligned feature table CSV file (columns: ID, m/z, then sample-wise total intensities)

## How to apply

Load each per-sample feature table as a FeatureSet object using find_feature() on the raw mzML/mzXML file. Optionally filter each FeatureSet by relative standard deviation (RSD) using rsd_control() to remove noise. Pass the list of FeatureSet objects and corresponding sample names to merge_result(), which aligns features by matching m/z values across samples (similar m/z values from different samples are assumed to be the same feature), consolidates them into a unified feature list with consensus m/z values, and builds a Sample object where rows are aligned features (indexed by m/z) and columns are samples with total intensity values. Export the aligned matrix to CSV using sample.to_csv() with the aligned-table schema (ID, m/z, then one column per sample).

## Related tools

- **BreathXplorer** (Python package providing merge_result() function to align FeatureSet objects into a Sample object, and to_csv() method for exporting aligned feature tables) — https://github.com/wykswr/breathXplorer
- **pandas** (Python library for loading, parsing, and manipulating per-sample feature tables (CSV format) during alignment workflow)

## Examples

```
from breathXplorer import find_feature, merge_result
fss = [find_feature(f, False, .8, "Gaussian", 6) for f in ["sample1.mzML", "sample2.mzML", "sample3.mzML"]]
fss = [fs.rsd_control(fs.rsd.quantile(0.1)) for fs in fss]
sample = merge_result(fss, ["sample1", "sample2", "sample3"])
sample.to_csv("aligned_table.csv")
```

## Evaluation signals

- Output aligned feature table has exactly one row per unique (consensus) m/z value and one column per input sample, plus ID and m/z metadata columns.
- All rows have complete intensity values for all samples (no missing values; zeros are acceptable for features not detected in a sample).
- Sample column order matches the input sample names list and sample.sample_name property.
- Total intensity values in the aligned table are ≥ 0 and correspond to the aggregated feature intensity from the original per-sample tables.
- CSV schema conforms to documented format: ID, m/z, S01_SampleName, S02_SampleName, ... (as shown in README example).

## Limitations

- Feature matching is based on m/z similarity; retention time alignment is mentioned in the task description but the README and code snippets do not show explicit retention-time-based matching parameters, so alignment tolerances and thresholds are not documented.
- If per-sample FeatureSet objects have been heavily filtered by RSD or other criteria, the aligned matrix may lose rare or noisy features and reduce statistical power for low-abundance VOCs.
- The merge_result() function aligns mzML and mzXML files in one call, but mixing formats is 'not recommended' due to consistency concerns, which may introduce subtle alignment artifacts.
- No explicit handling of isotope or adduct variants is shown in the merge_result() documentation, though to_csv() supports adduct=True flag for individual FeatureSet export.

## Evidence

- [readme] The `merge_feature` function takes as input a list of FeatureSet objects, and returns a Sample object. It aligns the features with the similar m/z value from different samples, and calculate the total intensity of each feature in each sample.: "The `merge_feature` function takes as input a list of FeatureSet objects, and returns a Sample object. It aligns the features with the similar m/z value from different samples, and calculate the"
- [other] The aligned feature matrix where rows are unique aligned features and columns are samples, with intensity values populated from the original tables.: "Create an aligned feature matrix where rows are unique aligned features and columns are samples, with intensity values populated from the original tables."
- [readme] Aligned feature table CSV format with ID, m/z, and sample-wise total intensities: The index of the table is the m/z value of the features, and each column is the total intensity of the feature in a sample (experiment of a subject). The name of the column is the sample name.: "The index of the table is the m/z value of the features, and each column is the total intensity of the feature in a sample (experiment of a subject). The name of the column is the sample name."
- [readme] fss = [find_feature(f, False, .8, "Gaussian", 6) for f in ["sample1.mzML", "sample2.mzXML", "sample3.mzML"]]
fss = [fs.rsd_control(fs.rsd.quantile(0.1)) for fs in fss]  # filter out the noise (optional)
sample = merge_result(fss, ["sample1", "sample2", "sample3"]): "fss = [find_feature(f, False, .8, "Gaussian", 6) for f in ["sample1.mzML", "sample2.mzXML", "sample3.mzML"]]
fss = [fs.rsd_control(fs.rsd.quantile(0.1)) for fs in fss]  # filter out the noise"
- [readme] sample.to_csv("aligned_table.csv")  # export the feature table of all samples as csv file: "sample.to_csv("aligned_table.csv")  # export the feature table of all samples as csv file"
