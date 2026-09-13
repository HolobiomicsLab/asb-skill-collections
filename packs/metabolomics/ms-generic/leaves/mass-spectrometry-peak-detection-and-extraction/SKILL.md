---
name: mass-spectrometry-peak-detection-and-extraction
description: Use when you have raw high-resolution mass-spectrometry data in mzML
  or mzXML format from breath analysis and need to identify individual volatile organic
  compounds before sample-to-sample alignment or comparative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - BreathXplorer
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-peak-detection-and-extraction

## Summary

Detect and extract volatile organic compound (VOC) features from high-resolution mass-spectrometry breath data by identifying significant peaks across the mass-to-charge (m/z) ratio range and computing their feature attributes (m/z, retention time, intensity). This is the foundational step that converts raw mzML/mzXML data into a feature table suitable for downstream alignment and statistical analysis.

## When to use

Apply this skill when you have raw high-resolution mass-spectrometry data in mzML or mzXML format from breath analysis and need to identify individual volatile organic compounds before sample-to-sample alignment or comparative analysis. Use it as the first processing step in breath-metabolomics workflows where noise filtering and feature quality control are required.

## When NOT to use

- Input is already a feature-aligned table (use feature alignment instead).
- Data format is not mzML or mzXML (BreathXplorer does not support other formats).
- You need only raw spectral visualization without feature extraction (use a spectrum viewer instead).

## Inputs

- mzML-format mass-spectrometry file
- mzXML-format mass-spectrometry file

## Outputs

- FeatureSet object (Python) containing extracted m/z values, intensity, scan_time, and RSD metrics
- Feature table CSV with columns: ID, m/z, intensity (total), and time-indexed intensity columns

## How to apply

Load raw mzML/mzXML breath MS data into BreathXplorer's `find_feature` function, specifying a quality threshold (e.g., 0.8) and peak-detection algorithm (Topological or Gaussian). The function applies peak recognition to identify significant signals and extracts m/z, retention time, and intensity for each detected peak. Filter the resulting FeatureSet using relative standard deviation (RSD) to remove noise lacking consistent intensity across breath peaks—either by specifying an RSD cutoff or using a quantile (e.g., 10th percentile of RSD) to retain only high-confidence features. Export the filtered feature table to CSV format with rows as m/z features and columns as scan-time intensity values, ready for alignment or statistical downstream processing.

## Related tools

- **BreathXplorer** (Implements peak recognition, feature extraction, and RSD filtering for breath MS data; provides find_feature function and FeatureSet object for feature management and CSV export) — https://github.com/wykswr/breathXplorer

## Examples

```
from breathXplorer import find_feature
fs = find_feature("sample.mzML", False, .8, "Topological", 6)
fs = fs.rsd_control(fs.rsd.quantile(0.1))
fs.to_csv("feature_table.csv")
```

## Evaluation signals

- FeatureSet object contains non-empty m/z, intensity, and scan_time arrays with matching lengths.
- Extracted feature count is reasonable for breath VOC analysis (typically dozens to hundreds of features, not thousands or zero).
- RSD values are computed and can be filtered; filtered FeatureSet has fewer features than unfiltered, with RSD below threshold.
- Exported CSV has correct structure: ID column, m/z column, total intensity column, and time-indexed intensity columns with numeric values.
- No NaN or infinite values in intensity columns after RSD filtering; all m/z values are positive and within expected mass range (typically 40–500 m/z for breath VOCs).

## Limitations

- Only supports mzML and mzXML input formats; other MS data formats (NetCDF, raw vendor files) are not supported.
- RSD filtering requires a-priori choice of threshold or quantile; inappropriate thresholds may over-filter (losing real features) or under-filter (retaining noise).
- Peak recognition sensitivity depends on algorithm choice (Topological vs. Gaussian) and quality parameter; Gaussian algorithm requires prior knowledge of breath count per experiment, which may not always be available.
- Feature extraction does not distinguish between true VOC signals and instrument noise; post-hoc RSD filtering is essential but may fail for low-abundance or highly variable features.

## Evidence

- [readme] Feature extraction is used to find the volatile organic compound (VOC) in the breath sample. The feature extraction is performed using the `find_feature` function. The function takes the path to an mzMl/mzXML file as input, and returns an object containing the extracted feature table: "Feature extraction is used to find the volatile organic compound (VOC) in the breath sample. The feature extraction is performed using the `find_feature` function. The function takes the path to an"
- [readme] fs = find_feature("sample.mzML", False, .8, "Topological", 6)

The `False` indicates that the input file is not a line spectrum, and the `.8` controls the quality of the extracted features, higher value means higher quality. The `"Topological"` indicates the algorithm used for feature extraction, the other option is `"Gaussian"`.: "The `.8` controls the quality of the extracted features, higher value means higher quality. The `"Topological"` indicates the algorithm used for feature extraction, the other option is `"Gaussian"`."
- [readme] In practice, the relative standard deviation (RSD) can be used to filter out the noise which doesn't have a consistent intensity with breath peaks: fs = fs.rsd_control(.1) # use specific RSD value: "the relative standard deviation (RSD) can be used to filter out the noise which doesn't have a consistent intensity with breath peaks"
- [other] Apply peak recognition to identify significant signals across the mass-to-charge ratio range. 3. Extract feature attributes (m/z, retention time, intensity) for each detected peak. 4. Aggregate features by sample identifier and normalize intensity values. 5. Export the feature table as a CSV file with rows as samples and columns as m/z features: "Extract feature attributes (m/z, retention time, intensity) for each detected peak. Aggregate features by sample identifier and normalize intensity values. Export the feature table as a CSV file"
- [readme] The index of the table is the m/z value of the features, and the 1st column is the total intensity of the feature. The other columns are the intensity of the feature over time, the time is the name of the corresponding column.: "The index of the table is the m/z value of the features, and the 1st column is the total intensity of the feature. The other columns are the intensity of the feature over time"
