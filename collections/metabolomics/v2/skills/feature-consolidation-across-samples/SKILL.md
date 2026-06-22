---
name: feature-consolidation-across-samples
description: Use when you have extracted multiple per-sample feature tables (in CSV format, each with feature ID, m/z, intensity, and retention time columns) and need to identify which features are the same compound detected across different breath samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - BreathXplorer
  - Python pandas
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

# feature-consolidation-across-samples

## Summary

Consolidate per-sample feature tables into a unified aligned feature table by matching features across samples using retention time and m/z alignment criteria, then producing a matrix where rows represent unique aligned features and columns represent individual samples. This skill is essential for comparative breath metabolomics analysis where features detected in different breath samples must be cross-referenced to enable downstream statistical or clustering analysis.

## When to use

Apply this skill when you have extracted multiple per-sample feature tables (in CSV format, each with feature ID, m/z, intensity, and retention time columns) and need to identify which features are the same compound detected across different breath samples. This is required before performing sample-level statistical comparisons or building a feature-by-sample abundance matrix for multivariate analysis.

## When NOT to use

- Input is already a single aligned feature table across all samples
- Per-sample feature tables lack m/z or retention time information needed for cross-sample matching
- Samples are from fundamentally different instruments or methods with incompatible m/z/retention time scales

## Inputs

- per-sample feature tables (CSV format)
- list of FeatureSet objects (from find_feature function)
- sample names (list of strings)

## Outputs

- aligned feature table (CSV format)
- Sample object (containing mz, sample_name, and aligned intensities)

## How to apply

Load each per-sample feature table using Python pandas and extract feature identifiers, retention time, m/z values, and intensity measurements. Apply feature matching across samples using retention time and m/z alignment criteria (typically using tolerances appropriate to your instrument's mass resolution and chromatographic reproducibility) to identify corresponding features across samples. Consolidate matched features into a unified feature list, computing consensus retention time and m/z values for each matched group. Create an aligned feature matrix where rows are unique aligned features, columns are sample names, and cells contain the total intensity of each feature in each sample. Format the output to conform to the aligned-table CSV schema: feature ID, m/z, retention time (optional), and one column per sample with intensity values. Write the aligned feature table to a CSV file using the `to_csv()` method.

## Related tools

- **BreathXplorer** (provides merge_result() function to align FeatureSet objects and consolidate per-sample features into a Sample object; exports aligned feature table via to_csv()) — https://github.com/wykswr/breathXplorer
- **Python pandas** (used to load, parse, and manipulate per-sample feature tables in CSV format)

## Examples

```
from breathXplorer import merge_result, find_feature
fss = [find_feature(f, False, .8, "Gaussian", 6) for f in ["sample1.mzML", "sample2.mzXML", "sample3.mzML"]]
fss = [fs.rsd_control(fs.rsd.quantile(0.1)) for fs in fss]
sample = merge_result(fss, ["sample1", "sample2", "sample3"])
sample.to_csv("aligned_table.csv")
```

## Evaluation signals

- Output aligned feature table conforms to schema: feature ID, m/z, and one intensity column per input sample (no missing columns)
- Number of aligned features is less than or equal to the maximum number of features in any single input sample (no spurious duplicates)
- All intensity values in aligned table are non-negative numbers; cells corresponding to features absent in a given sample contain 0 or are handled consistently
- Consensus m/z values for aligned features fall within the expected m/z tolerance range of pairwise matches (e.g., within ±5–10 ppm depending on instrument)
- Sample names in output column headers match the input sample name list exactly and in the same order

## Limitations

- Feature matching relies on m/z and retention time tolerances; if these are set too stringently, true matches may be missed; if too loosely, unrelated features may be incorrectly merged
- Consensus m/z and retention time calculations assume that matched features represent the same compound; systematic shifts in retention time across samples (e.g., due to column aging or temperature drift) may degrade alignment quality
- Output schema does not include retention time by default in the example provided; users must manually include it if needed for downstream analysis
- The `merge_result()` function can handle mixed file formats (mzML, mzXML) in a single call, but documentation discourages this due to data consistency concerns

## Evidence

- [other] Feature alignment workflow step that consumes per-sample feature tables and produces an aligned feature table in CSV format: "BreathXplorer includes a feature alignment workflow step that consumes per-sample feature tables and produces an aligned feature table in CSV format, as documented in the file format specifications"
- [other] Workflow: load, parse, match, consolidate, create matrix, format output, write CSV: "1. Load per-sample feature tables (CSV format) using Python pandas. 2. Parse each table to extract feature identifiers, retention time, m/z values, and intensity measurements. 3. Apply feature"
- [readme] Aligned feature table CSV schema with feature ID, m/z, and sample columns: "| ID | m/z     | S01_Before | S02_Before | S03_Before |
|----|---------|------------|------------|------------|"
- [readme] merge_result function takes list of FeatureSet objects and returns Sample object with aligned features: "The `merge_result` function takes as input a list of FeatureSet objects, and returns a Sample object. It aligns the features with the similar m/z value from different samples, and calculate the total"
- [readme] Python code example using merge_result with sample names: "sample = merge_result(fss, ["sample1", "sample2", "sample3"])"
- [readme] Sample object export via to_csv method: "sample.to_csv("aligned_table.csv")  # export the feature table of all samples as csv file"
