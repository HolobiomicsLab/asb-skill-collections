---
name: data-format-conversion-csv-tsv
description: Use when after completing data merging, cleanup, and batch correction steps in the FBMN-STATS pipeline, when you have a processed feature quantification table combined with sample metadata in memory (R data frame or Python pandas DataFrame) and need to preserve it for multivariate statistical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3896
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - Jupyter Notebook
  - Python (pandas)
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s41596-024-01046-3
  title: FBMN-STATS
evidence_spans:
- To easily install and run Jupyter Notebook in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fbmn_stats_cq
    doi: 10.1038/s41596-024-01046-3
    title: FBMN-STATS
  dedup_kept_from: coll_fbmn_stats_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-024-01046-3
  all_source_dois:
  - 10.1038/s41596-024-01046-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-format-conversion-csv-tsv

## Summary

Export analysis-ready feature tables and statistical results to CSV or TSV format for downstream bioinformatic and statistical workflows. This skill bridges the FBMN-STATS pipeline output and external analysis tools by converting merged and processed metabolomics data into standardized tabular formats.

## When to use

After completing data merging, cleanup, and batch correction steps in the FBMN-STATS pipeline, when you have a processed feature quantification table combined with sample metadata in memory (R data frame or Python pandas DataFrame) and need to preserve it for multivariate statistical analysis, reproducibility, or cross-platform compatibility.

## When NOT to use

- Input is already in CSV or TSV format and does not require re-export.
- Data format must be retained in a binary or HDF5 structure for interactive or streaming access to large datasets.
- Output will be immediately processed in the same R or Python session; in-memory data structures are more efficient than round-tripping through files.

## Inputs

- Merged feature quantification table (R data frame or pandas DataFrame)
- Combined feature table with sample metadata aligned on sample identifier column
- Data after batch correction step (prior to univariate/multivariate analysis)

## Outputs

- CSV file (comma-separated values format)
- TSV file (tab-separated values format)
- Analysis-ready flat table compatible with statistical software (e.g., for univariate and multivariate statistical analyses)

## How to apply

After the data merging step has aligned the feature quantification table (output from MZmine3 feature detection) with sample metadata via an inner or left join on the sample identifier column, export the resulting analysis-ready data frame to CSV or TSV format. Use R's `write.csv()` or `write.table()` function (with `sep=','` for CSV or `sep='\t'` for TSV) or Python's `pandas.DataFrame.to_csv()` with appropriate delimiter specification. Verify that all rows (samples) and columns (features + metadata) are preserved, no NaN values are introduced unexpectedly, and the file encoding handles special characters in feature or sample names. This ensures the exported file can be imported by downstream statistical analysis tools and maintains the integrity of the merged dataset across platforms.

## Related tools

- **R** (Data frame export via write.csv() or write.table() with delimiter specification) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Jupyter Notebook** (Interactive environment for executing data export and verification in R or Python) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Python (pandas)** (Data frame export via pandas.DataFrame.to_csv() with delimiter and encoding options) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS

## Examples

```
write.csv(merged_data, file='analysis_ready_features_metadata.csv', row.names=FALSE)
```

## Evaluation signals

- File is successfully created and is readable by downstream statistical tools (R, Python, QIIME2, etc.).
- Row count in exported file equals the number of samples in the merged table; column count equals number of features plus metadata columns.
- All sample identifiers and feature names are correctly preserved without truncation or encoding errors.
- No unexpected NaN, NA, or null values introduced during export; compare row/column sums before and after export.
- File opens correctly in a text editor or spreadsheet application and displays expected delimiter separation between fields.

## Limitations

- CSV/TSV formats do not preserve data types (all values stored as strings); downstream tools must re-infer numeric vs. categorical types.
- Large datasets (>100k rows or >1k columns) may be slow to export or difficult to view interactively in spreadsheet applications; consider HDF5 or Parquet for production workflows.
- Special characters in feature or sample names (e.g., whitespace, commas, quotes, non-ASCII symbols) may require escaping or quoting, which can introduce downstream parsing errors if not handled consistently.
- GitHub rendering issues may affect visibility of code examples in Jupyter notebooks; use Google Colab or download notebook locally for accurate code transfer.

## Evidence

- [other] Export the merged analysis-ready table as a CSV or TSV file for downstream statistical analysis.: "Export the merged analysis-ready table as a CSV or TSV file for downstream statistical analysis."
- [readme] Using the notebooks provided here, one can perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks.: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data"
- [readme] To copy code into another environment (e.g., RStudio), please use the respective Google Colab or Jupyter viewed version to ensure all content, including HTML in text cells, is accurately transferred.: "To copy code into another environment (e.g., RStudio), please use the respective Google Colab or Jupyter viewed version"
