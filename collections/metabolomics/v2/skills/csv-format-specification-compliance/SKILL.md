---
name: csv-format-specification-compliance
description: 'Use when after feature extraction or feature alignment when you have FeatureSet or Sample objects that must be exported as CSV files for sharing, archival, or downstream analysis. Specifically: (1) when exporting single-sample feature tables from find_feature() output;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3703
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - BreathXplorer
  - Python pandas
  techniques:
  - tandem-MS
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

# CSV format specification compliance

## Summary

Validate and format feature tables and aligned feature matrices to conform to BreathXplorer's documented CSV schemas, ensuring downstream compatibility with feature alignment and export workflows. This skill bridges raw feature extraction outputs with specification-compliant tabular formats required for multi-sample analysis.

## When to use

Apply this skill after feature extraction or feature alignment when you have FeatureSet or Sample objects that must be exported as CSV files for sharing, archival, or downstream analysis. Specifically: (1) when exporting single-sample feature tables from find_feature() output; (2) when exporting aligned multi-sample feature matrices from merge_result() output; (3) when preparing feature tables with optional adduct and isotope annotations for publication or data repositories.

## When NOT to use

- Input is already a validated CSV file in BreathXplorer format — proceed directly to downstream analysis or merging.
- Input is mzML/mzXML raw mass spectrometry data — first run feature extraction (find_feature) to generate a FeatureSet, then export.
- Output target is MGF format for MS/MS spectra — use the MS/MS spectra export utility (to_mgf) instead of CSV export.

## Inputs

- FeatureSet object (from find_feature())
- Sample object (from merge_result())
- Output file path (string)

## Outputs

- Feature table CSV file (ID, m/z, intensity, time-indexed columns)
- Aligned feature table CSV file (ID, m/z, sample-indexed columns with intensities)
- Feature table CSV with adduct annotations (optional)
- Feature table CSV with isotope annotations (optional)

## How to apply

Validate the feature table schema before export: confirm the table has ID (feature index), m/z (mass-to-charge ratio), and intensity columns. For single-sample feature tables, add time-indexed columns (scan_time values) with per-feature intensity values at each timepoint. For aligned feature tables, verify each column corresponds to a sample name, rows correspond to unique aligned features, and cells contain total feature intensities per sample. Apply optional adduct and isotope inference using built-in methods if chemical annotation is required. Call to_csv() with the output path and boolean flags (adduct=True/False, isotope=True/False) to write the formatted table. Verify the output file is readable, has no missing values in required columns, and column/row counts match the input object's feature and sample cardinality.

## Related tools

- **BreathXplorer** (Provides FeatureSet and Sample objects with to_csv() method for specification-compliant export; defines aligned and single-sample CSV schemas) — https://github.com/wykswr/breathXplorer
- **Python pandas** (Underlying library for CSV formatting, validation, and I/O operations)

## Examples

```
fs.to_csv("feature_table.csv", adduct=True, isotope=True)
sample.to_csv("aligned_table.csv")
```

## Evaluation signals

- Output CSV file parses without errors in pandas (pd.read_csv) and contains expected columns: ID, m/z, intensity, and sample/time columns.
- Row count matches the number of unique features in the input object (len(FeatureSet) or len(Sample)).
- Column count matches expected schema: single-sample tables have 3 required + N time columns; aligned tables have 2 required + M sample columns.
- No null or missing values in required columns (ID, m/z, intensity); optional adduct/isotope columns may be sparse.
- m/z values are numeric and within biological mass range (typically 50–500 m/z for volatile organic compounds); intensity values are non-negative.
- Sample names in aligned table headers match the input sample_name list; feature ID indices are sequential starting from 0.

## Limitations

- CSV export does not retain scan_time metadata from the original FeatureSet; time information is preserved only as column headers in single-sample tables.
- Adduct and isotope inference are optional annotations; their accuracy depends on mass accuracy and feature distribution; not all features will be confidently annotated.
- The aligned feature table assumes successful retention time and m/z alignment across samples; misalignment upstream will propagate into the CSV output.
- Large feature sets (>10,000 features) may produce very wide CSV files when exported as aligned tables with many samples; consider data matrix representation (HDF5, NetCDF) for very large cohorts.

## Evidence

- [readme] The index of the table is the m/z value of the features, and the 1st column is the total intensity of the feature. The other columns are the intensity of the feature over time, the time is the name of the corresponding column.: "The index of the table is the m/z value of the features, and the 1st column is the total intensity of the feature. The other columns are the intensity of the feature over time"
- [readme] The index of the table is the m/z value of the features, and each column is the total intensity of the feature in a sample (experiment of a subject). The name of the column is the sample name.: "each column is the total intensity of the feature in a sample (experiment of a subject). The name of the column is the sample name."
- [readme] FeatureSet object can be exported as csv file using the `to_csv` method: fs.to_csv("feature_table.csv"): "FeatureSet object can be exported as csv file using the `to_csv` method"
- [readme] BreathXplorer can infer the adducts and isotope of the features, to enable this function: fs.to_csv("feature_table.csv", adduct=True, isotope=True): "BreathXplorer can infer the adducts and isotope of the features, to enable this function"
- [readme] The single or aligned feature table can be exported as csv file. The related MS/MS spectra can be exported in an mgf file.: "The single or aligned feature table can be exported as csv file"
- [other] 6. Format the output table to conform to BreathXplorer's aligned-table CSV schema (feature ID, retention time, m/z, sample intensities).: "Format the output table to conform to BreathXplorer's aligned-table CSV schema (feature ID, retention time, m/z, sample intensities)"
