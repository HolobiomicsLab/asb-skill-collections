---
name: intensity-value-aggregation-across-replicates
description: Use when after peak recognition has identified features (m/z and retention time pairs) across one or more MS replicates, and you need to collapse multiple intensity measurements per feature into a single representative value per sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - BreathXplorer
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
---

# intensity-value-aggregation-across-replicates

## Summary

Aggregates mass-spectrometry feature intensities across multiple replicate samples or scan time points, producing normalized intensity values per feature suitable for downstream alignment and statistical analysis. This step standardizes feature representation for comparison across breath samples in high-resolution MS workflows.

## When to use

Apply this skill after peak recognition has identified features (m/z and retention time pairs) across one or more MS replicates, and you need to collapse multiple intensity measurements per feature into a single representative value per sample. Specifically, use it when converting individual scan-level intensities into sample-level feature intensity aggregates for cross-sample alignment.

## When NOT to use

- Input is already a feature table CSV with pre-aggregated intensities — skip to alignment
- Data requires custom intensity aggregation logic not covered by standard peak integration (e.g., intensity ratios, weighted averages)
- Individual scan-level intensities must be preserved for subsequent noise modeling or robust statistics

## Inputs

- FeatureSet object (extracted features from single sample with m/z, scan_time, and per-scan intensity data)
- List of FeatureSet objects (multiple samples/replicates)
- Peak detection results (m/z, retention time, intensity vectors)

## Outputs

- Feature table CSV with aggregated intensities (rows = feature IDs indexed by m/z, columns = samples or time points, values = total/normalized intensity)
- FeatureSet object with aggregated intensity field
- Sample object (aligned features across multiple replicates)

## How to apply

After extracting features from raw mzML/mzXML files using peak recognition (e.g., via the `find_feature` function with Topological or Gaussian algorithm), aggregate intensities by: (1) grouping detected peaks by their m/z value and sample identifier; (2) integrating intensity values across the scan time dimension for each feature to calculate total intensity per feature; (3) optionally filtering features by relative standard deviation (RSD) using quantile-based thresholds (e.g., 10th percentile) to remove low-quality noise; (4) normalizing intensity values to enable comparison across replicates. The aggregated intensities are then structured as a feature table (rows = features, columns = samples or time points) for export to CSV format compatible with downstream feature alignment.

## Related tools

- **BreathXplorer** (Implements feature extraction via `find_feature` function, aggregates intensities during FeatureSet creation, and exports aggregated intensities via `to_csv` method) — https://github.com/wykswr/breathXplorer
- **Python** (Language for implementing feature aggregation logic and data frame operations)

## Examples

```
from breathXplorer import find_feature
fs = find_feature("sample.mzML", False, .8, "Topological", 6)
fs = fs.rsd_control(fs.rsd.quantile(0.1))
fs.to_csv("feature_table.csv")
```

## Evaluation signals

- Feature table CSV contains expected number of rows (features) and columns (samples or time points) with no NaN or inf values
- Aggregated intensity values are positive and within the dynamic range of the MS instrument (no negative or zero-only features)
- RSD filtering (if applied) removes low-variance noise while retaining high-quality features; RSD quantile threshold is consistent with prior knowledge of breath sample complexity
- Sum of aggregated intensities per sample is reasonable and comparable across replicates (no extreme outliers suggesting failed aggregation)
- Downstream feature alignment step successfully merges features with similar m/z across samples, indicating intensity values were properly aggregated and normalized

## Limitations

- Aggregation assumes all scans within a feature's retention time window contribute equally to total intensity; features with irregular peak shapes or noise spikes may produce inflated totals
- RSD-based filtering requires prior knowledge of expected variance; quantile threshold selection is data-dependent and may require manual tuning
- Input file format must be mzML or mzXML; other MS data formats (NetCDF, .raw, .d) are not explicitly supported by BreathXplorer's current implementation
- Aggregation does not account for instrumental drift or batch effects across replicates; normalization is applied post-hoc and may be insufficient for cross-batch comparisons

## Evidence

- [other] Aggregate features by sample identifier and normalize intensity values.: "4. Aggregate features by sample identifier and normalize intensity values."
- [other] Extract feature attributes (m/z, retention time, intensity) for each detected peak.: "3. Extract feature attributes (m/z, retention time, intensity) for each detected peak."
- [readme] fs.intensity  # the total intensity of each feature (calculated by integrating the intensity over scan time): "fs.intensity  # the total intensity of each feature (calculated by integrating the intensity over scan time)"
- [readme] The index of the table is the m/z value of the features, and the 1st column is the total intensity of the feature. The other columns are the intensity of the feature over time: "The index of the table is the m/z value of the features, and the 1st column is the total intensity of the feature. The other columns are the intensity of the feature over time"
- [readme] fs = fs.rsd_control(fs.rsd.quantile(0.1))  # use the 10% quantile of the RSD: "fs = fs.rsd_control(fs.rsd.quantile(0.1))  # use the 10% quantile of the RSD"
