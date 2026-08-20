---
name: query-result-serialization-to-csv
description: Use when after executing a MassQL query against mzML mass spectrometry
  files and obtaining a tabulated result DataFrame in memory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - MassQL
  - MassQLab
  - pandas
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1002/rcm.10132
  title: MassQLab
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massqlab_cq
    doi: 10.1002/rcm.10132
    title: MassQLab
  dedup_kept_from: coll_massqlab_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.10132
  all_source_dois:
  - 10.1002/rcm.10132
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# query-result-serialization-to-csv

## Summary

Serialize tabulated mass spectrometry query results to persistent storage in both CSV and image formats. This skill captures the critical export step that converts in-memory result tables (produced by MassQL query execution) into reusable CSV files and visualization images for downstream analysis and reporting.

## When to use

After executing a MassQL query against mzML mass spectrometry files and obtaining a tabulated result DataFrame in memory. The skill is needed when results must be persisted to disk in both machine-readable (CSV) and human-readable (visualization) forms for archival, sharing, or integration into downstream analysis pipelines.

## When NOT to use

- Results are only needed for immediate interactive exploration (e.g., within a Jupyter notebook) and do not need to be archived or shared.
- Input is already a persisted CSV or image file—re-serialization is redundant.
- Query results are empty or malformed (serialization will succeed but produce invalid or zero-byte outputs).

## Inputs

- tabulated query results (pandas DataFrame or equivalent in-memory table)
- output directory path (string)
- result structure metadata (to determine visualization type)

## Outputs

- CSV file containing raw query results and metadata (e.g., ms1_raw_df.csv or ms2_raw_df.csv)
- visualization image file (PNG or PDF format, e.g., ms1_traces.pdf, ms2_plots.pdf)

## How to apply

Load the tabulated query results (either directly from MassQL query execution output or from an intermediate format such as a Feather cache). Serialize the result table to CSV format using a CSV writer utility (e.g., pandas.DataFrame.to_csv()). Simultaneously generate a visualization image from the tabulated results—plot type and format are determined by the result structure and query type (MS1 vs MS2). Write both the CSV file and visualization image(s) to the designated output directory. Finally, verify that both files are written to disk with correct format and non-zero size before marking the export step as complete.

## Related tools

- **MassQL** (Executes domain-specific queries on mass spectrometry data; produces tabulated result DataFrames that serve as input to this serialization skill.) — https://github.com/mwang87/MassQueryLanguage
- **MassQLab** (Orchestrates end-to-end workflow including MassQL query execution and result serialization to CSV and image outputs.) — https://github.com/JohnsonDylan/MassQLab
- **pandas** (Provides DataFrame.to_csv() method for CSV serialization.)

## Examples

```
results_df = msql_engine.process_query(input_query, input_filename); results_df.to_csv('ms1_raw_df.csv'); # followed by visualization image generation and write to output_directory
```

## Evaluation signals

- CSV file exists in the output directory and is readable by a CSV parser (pandas.read_csv, etc.); schema includes expected column names (e.g., scan number, m/z, retention time, intensity).
- Image file exists in the output directory with correct raster format (PNG) or vector format (PDF); file size is greater than zero bytes.
- Row count in CSV matches the number of rows in the in-memory result table before serialization (no silent data loss).
- Output directory contains exactly two files per query result: one CSV and one or more visualization image(s).
- Result table schema is preserved: no columns are dropped, no row reordering occurs during CSV write.

## Limitations

- Very large result tables (millions of rows) may cause memory or I/O bottlenecks during CSV serialization.
- Visualization image generation depends on result structure heuristics; malformed or unexpected result schemas may produce invalid or illegible plots.
- CSV serialization does not preserve native Python data types (e.g., datetime objects are converted to strings); downstream consumers must reparse type information.
- Output directory permissions must allow file creation; serialization will fail silently or raise I/O exceptions if write access is denied.
- No built-in deduplication or compression of results; identical queries executed multiple times will produce duplicate files in the output directory unless manually managed.

## Evidence

- [other] MassQLab exports tabulated query results through a two-format serialization mechanism: results are saved as both images and CSV files.: "MassQLab exports tabulated query results through a two-format serialization mechanism: results are saved as both images and CSV files."
- [other] Load tabulated query results (in memory or from intermediate format produced by MassQL query execution). Serialize results table to CSV format using a CSV writer (e.g. pandas.DataFrame.to_csv or equivalent). Generate visualization image(s) from the tabulated results (format and plot type determined by result structure). Save visualization(s) as image file(s) (PNG or equivalent raster format). Verify both CSV and image files are written to the designated output directory with correct format and non-zero size.: "Load tabulated query results (in memory or from intermediate format produced by MassQL query execution). Serialize results table to CSV format using a CSV writer (e.g. pandas.DataFrame.to_csv or"
- [readme] Results are tabulated and saved as images and csv files: "Results are tabulated and saved as images and csv files"
- [readme] Results are saved in `MassQLab_Output` inside the defined `output_directory` (`data_directory` is used by default), organized by timestamp. **MS1 Outputs** - `ms1_raw_df.csv`: Raw query results + metadata: "Results are saved in `MassQLab_Output` inside the defined `output_directory` (`data_directory` is used by default), organized by timestamp. **MS1 Outputs** - `ms1_raw_df.csv`: Raw query results +"
