---
name: retention-time-mz-alignment-matching
description: Use when you have extracted feature tables (m/z, intensity, retention time) from multiple breath samples (mzML or mzXML files) via feature extraction, and need to identify which features represent the same volatile organic compound (VOC) across samples to enable cross-sample intensity comparisons.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0218
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

# retention-time-mz-alignment-matching

## Summary

Align features across multiple breath samples by matching features with similar retention time and m/z values, consolidating them into a unified feature matrix. This step transforms per-sample feature tables into a single aligned feature table suitable for comparative analysis.

## When to use

You have extracted feature tables (m/z, intensity, retention time) from multiple breath samples (mzML or mzXML files) via feature extraction, and need to identify which features represent the same volatile organic compound (VOC) across samples to enable cross-sample intensity comparisons and downstream statistical analysis.

## When NOT to use

- Input is already an aligned feature table (CSV with multi-sample intensities) — skip alignment and proceed directly to analysis.
- You have only a single sample — alignment requires two or more FeatureSet objects to identify corresponding features.
- Features have not been quality-filtered (e.g., by RSD) — consider applying RSD control to remove noise before alignment to improve alignment accuracy.

## Inputs

- List of FeatureSet objects (one per sample, output from find_feature function)
- List of sample name strings (customizable identifiers for each FeatureSet)

## Outputs

- Sample object (contains aligned features across all samples)
- Aligned feature table CSV file with schema: ID | m/z | sample1_intensity | sample2_intensity | ... | sampleN_intensity

## How to apply

Apply the `merge_result` function from BreathXplorer to a list of FeatureSet objects, providing sample names as identifiers. The function aligns features by matching m/z and retention time values across samples using built-in alignment criteria (specific tolerances are not explicitly stated in the README but are handled internally). The result is a Sample object where each row represents a unique aligned feature (identified by consensus m/z and retention time) and each column represents a sample's total intensity for that feature. Export the aligned Sample object to CSV format using the `.to_csv()` method, which produces a table with columns: ID, m/z, and one intensity column per sample (named by the provided sample identifiers). Optionally enable adduct inference by passing `adduct=True` to enrich the aligned table.

## Related tools

- **BreathXplorer** (Performs feature alignment via merge_result function, which consolidates per-sample feature tables into unified aligned feature matrix) — https://github.com/wykswr/breathXplorer
- **Python pandas** (Underlying data structure for loading, parsing, and manipulating feature tables (FeatureSet and Sample objects are pandas-based))

## Examples

```
from breathXplorer import find_feature, merge_result
fss = [find_feature(f, False, .8, "Topological", 6) for f in ["sample1.mzML", "sample2.mzML", "sample3.mzML"]]
fss = [fs.rsd_control(fs.rsd.quantile(0.1)) for fs in fss]
sample = merge_result(fss, ["sample1", "sample2", "sample3"])
sample.to_csv("aligned_table.csv")
```

## Evaluation signals

- Aligned feature table CSV contains one row per unique aligned feature and one column per input sample, with no missing or malformed column headers.
- Total number of aligned features is less than or equal to the maximum number of features in any single input sample (consolidation occurred).
- m/z values in the aligned table fall within the range of the input m/z values, and intensity values are non-negative integers matching the per-sample input intensities.
- Sample names in the aligned table column headers match the provided sample name list exactly and in the correct order.
- All features present in the input FeatureSet objects are represented in the aligned table; no features are lost during alignment.

## Limitations

- Alignment tolerances for retention time and m/z matching are not explicitly documented in the README; behavior depends on internal BreathXplorer defaults and may require empirical validation.
- The function assumes that input FeatureSet objects were extracted from breath samples generated under comparable HRMS conditions; mismatched instrumentation or acquisition parameters may produce poor alignment.
- No mechanism is documented for manual curation or validation of aligned feature assignments; all matched features are consolidated without user intervention.
- The aligned table loses per-feature retention time information (if different across samples) beyond the consensus value; fine-grained temporal variation is not retained.

## Evidence

- [readme] The `merge_result` function takes as input a list of FeatureSet objects, and returns a Sample object. It aligns the features with the similar m/z value from different samples, and calculate the total intensity of each feature in each sample.: "The `merge_result` function takes as input a list of FeatureSet objects, and returns a Sample object. It aligns the features with the similar m/z value from different samples, and calculate the total"
- [other] BreathXplorer includes a feature alignment workflow step that consumes per-sample feature tables and produces an aligned feature table in CSV format: "BreathXplorer includes a feature alignment workflow step that consumes per-sample feature tables and produces an aligned feature table in CSV format, as documented in the file format specifications"
- [readme] The index of the table is the m/z value of the features, and each column is the total intensity of the feature in a sample (experiment of a subject). The name of the column is the sample name.: "The index of the table is the m/z value of the features, and each column is the total intensity of the feature in a sample"
- [other] Apply feature matching across samples using retention time and m/z alignment criteria to identify corresponding features.: "Apply feature matching across samples using retention time and m/z alignment criteria to identify corresponding features."
- [readme] sample = merge_result(fss, ["sample1", "sample2", "sample3"]): "sample = merge_result(fss, ["sample1", "sample2", "sample3"])"
