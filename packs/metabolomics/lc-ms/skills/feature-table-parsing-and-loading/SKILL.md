---
name: feature-table-parsing-and-loading
description: Use when you have extracted volatile organic compound (VOC) features from individual breath samples (mzML or mzXML files) and wish to consolidate multiple per-sample feature tables into a single aligned feature table, or you need to programmatically access feature metadata (m/z, intensity, scan.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - breathXplorer
  - pandas
  techniques:
  - LC-MS
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

# feature-table-parsing-and-loading

## Summary

Load and parse per-sample feature tables in CSV format to extract feature identifiers, retention time, m/z values, and intensity measurements for downstream alignment or analysis. This is the foundational step that converts raw mass spectrometry feature tables into structured data objects.

## When to use

You have extracted volatile organic compound (VOC) features from individual breath samples (mzML or mzXML files) and wish to consolidate multiple per-sample feature tables into a single aligned feature table, or you need to programmatically access feature metadata (m/z, intensity, scan time) for quality control, filtering, or integration.

## When NOT to use

- Input is already an aligned feature table (sample-level aggregation); use directly without parsing individual per-sample tables.
- Feature tables are in a non-CSV format (e.g., MGF, netCDF, proprietary binary); convert or use format-specific parsers first.
- You only need MS/MS spectra metadata; use dedicated MGF parsing instead.

## Inputs

- per-sample feature table CSV file(s) (index=m/z, columns=intensity_total + time_points)
- mzML or mzXML file paths (for extraction via find_feature)

## Outputs

- FeatureSet object (contains fs.mz, fs.intensity, fs.scan_time, fs.rsd attributes)
- parsed feature metadata (m/z, retention time, intensity vectors)
- optionally, filtered FeatureSet after RSD-based quality control

## How to apply

Load each per-sample feature table CSV using Python pandas, where the index is the m/z value, the first column contains total feature intensity, and subsequent columns contain intensity values at discrete scan times. Extract the feature identifiers, m/z values, total intensity, and time-resolved intensity measurements from each table. Apply optional quality control filters (e.g., relative standard deviation quantile thresholds) to remove noise features before consolidation. Parse the FeatureSet object attributes (fs.mz, fs.intensity, fs.scan_time, fs.rsd) to access aligned feature data. If aligning across samples, pass the list of parsed FeatureSet objects to the merge_result function, which applies m/z-based matching criteria to identify corresponding features across samples.

## Related tools

- **breathXplorer** (Python package providing find_feature and merge_result functions to extract and parse per-sample feature tables into FeatureSet and Sample objects) — https://github.com/wykswr/breathXplorer
- **pandas** (underlying library for CSV reading and DataFrame manipulation within BreathXplorer's FeatureSet parsing)

## Examples

```
from breathXplorer import find_feature
fs = find_feature("sample.mzML", False, .8, "Topological", 6)
fs = fs.rsd_control(fs.rsd.quantile(0.1))
fs.to_csv("feature_table.csv")
```

## Evaluation signals

- Parsed FeatureSet object contains non-empty fs.mz, fs.intensity, and fs.scan_time arrays with matching dimensionality.
- Feature table CSV conforms to schema: index column is m/z, first data column is total intensity, subsequent columns are time-resolved intensities with numeric column names representing scan times.
- RSD values (fs.rsd) are numeric and within expected range [0, 1] for feature quality assessment; filtering at fs.rsd.quantile(0.1) removes low-quality noise while retaining consistent breath peaks.
- After parsing multiple samples and calling merge_result, aligned feature table contains matching m/z values across samples with corresponding intensity values in a sample-indexed matrix.
- Exported CSV file (fs.to_csv or sample.to_csv) reproduces the feature and intensity data without data loss or format corruption.

## Limitations

- Feature table CSV must strictly follow BreathXplorer's schema (index=m/z, columns=intensity + time points); non-conformant CSVs will fail to parse or produce spurious results.
- Parsing assumes m/z values are unique row identifiers; duplicate m/z entries will be silently dropped by pandas indexing, leading to feature loss.
- The RSD-based quality control filter (fs.rsd_control) requires prior computation of relative standard deviation; this step is optional but recommended to remove noise. Incorrect quantile selection (e.g., too permissive) can retain artifacts.
- Feature alignment via merge_result applies m/z-based matching only; retention time drift across samples is not explicitly corrected during parsing, potentially causing misalignment if chromatographic variation is high.

## Evidence

- [other] Load per-sample feature tables (CSV format) using Python pandas. Parse each table to extract feature identifiers, retention time, m/z values, and intensity measurements.: "Load per-sample feature tables (CSV format) using Python pandas. 2. Parse each table to extract feature identifiers, retention time, m/z values, and intensity measurements."
- [readme] The index of the table is the m/z value of the features, and the 1st column is the total intensity of the feature. The other columns are the intensity of the feature over time, the time is the name of the corresponding column.: "The index of the table is the m/z value of the features, and the 1st column is the total intensity of the feature. The other columns are the intensity of the feature over time"
- [readme] The fs is a FeatureSet object, it contains the following information: fs.mz, fs.scan_time, fs.intensity, len(fs), fs[96.7654], fs.rsd.: "The fs is a FeatureSet object, it contains the following information: fs.mz  # m/z values of the extracted features
fs.scan_time  # scan time of the experiment
fs.intensity"
- [readme] In practice, the relative standard deviation (RSD) can be used to filter out the noise which doesn't have a consistent intensity with breath peaks.: "In practice, the relative standard deviation (RSD) can be used to filter out the noise which doesn't have a consistent intensity with breath peaks"
- [readme] The fss is a list of FeatureSet objects, the merge_result aligns those FeatureSet objects. The first statement creates a list of FeatureSet objects.: "The first statement creates a list of FeatureSet objects. One thing very cool is the function can deal with different file formats in one line of code"
