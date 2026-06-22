---
name: mass-spectrometry-result-tabulation
description: Use when after executing a MassQL query against mzML mass spectrometry data files and obtaining tabulated results (DataFrame or equivalent in-memory table), apply this skill to persist those results in both human-readable CSV format and visual image form for archival, sharing, and downstream.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MassQL
  - MassQLab
  - pandas
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-result-tabulation

## Summary

Convert mass spectrometry query results from in-memory tabulated form into persistent dual-format output (CSV and image visualization). This skill bridges MassQL query execution and downstream analysis by serializing structured results and generating publication-ready visualizations.

## When to use

After executing a MassQL query against mzML mass spectrometry data files and obtaining tabulated results (DataFrame or equivalent in-memory table), apply this skill to persist those results in both human-readable CSV format and visual image form for archival, sharing, and downstream statistical analysis.

## When NOT to use

- Raw, unprocessed spectra from mzML files—this skill operates on already-tabulated query results, not on raw binary or XML spectrum data.
- Pre-existing CSV or image files that do not require re-serialization—use this skill only when converting fresh in-memory results.
- Intermediate Feather or cache files used for performance optimization—these are separate from final publication outputs.

## Inputs

- Tabulated query results (pandas DataFrame or equivalent structured table in memory)
- Result structure metadata (query type: MS1 or MS2; analysis type: raw, fitted traces, cluster plots)
- Output directory path (string)

## Outputs

- CSV file containing tabulated results with metadata columns
- Image file(s) in PNG or PDF format visualizing results (plot type depends on result structure)

## How to apply

Load the tabulated query results (produced by MassQL query execution) into memory. Serialize the results table to CSV format using a standard CSV writer such as pandas.DataFrame.to_csv(), preserving all columns and metadata. Simultaneously generate a visualization image from the tabulated results—the plot type and layout are determined by result structure (e.g., MS1 Gaussian-fitted traces, MS2 scan intensity plots, or peak area bar charts). Write both the CSV file and image file(s) to the designated output directory, ensuring both files are created with correct formatting and non-zero file size before confirming success.

## Related tools

- **MassQL** (Query engine that produces the tabulated result DataFrames fed to this serialization skill) — https://github.com/mwang87/MassQueryLanguage
- **MassQLab** (End-to-end workflow implementation that applies MassQL queries and invokes this tabulation and export step) — https://github.com/JohnsonDylan/MassQLab
- **pandas** (Python library used to serialize DataFrame results to CSV via to_csv() method)

## Examples

```
results_df = msql_engine.process_query(input_query, input_filename); results_df.to_csv('ms1_raw_df.csv'); import matplotlib.pyplot as plt; plt.plot(results_df['rt'], results_df['intensity']); plt.savefig('ms1_consolidated_traces.png')
```

## Evaluation signals

- Both CSV and image files exist in the output directory with non-zero file sizes.
- CSV file contains all result columns from the in-memory table with correct data types and row counts matching the input DataFrame.
- Image file renders without corruption and contains visual elements matching the result structure (e.g., Gaussian curve overlays for MS1 fitted traces, peak intensity lines for MS2 scans).
- Output filenames follow MassQLab conventions (e.g., ms1_raw_df.csv, ms1_consolidated_traces.png, ms2_plots.pdf) and are timestamped or query-indexed.
- File encoding and format metadata are correct (UTF-8 for CSV, standard PNG/PDF headers for images).

## Limitations

- Plot type and layout must be pre-determined by the result structure; the skill does not infer visualization strategy from arbitrary tabular data.
- Large result tables may produce slow rendering or memory pressure during image generation; no built-in pagination or tiling for very large datasets.
- Image visualization fidelity depends on the completeness of result metadata (e.g., MS1 retention time, intensity values, Gaussian fit parameters); sparse or missing metadata may produce incomplete or misleading plots.
- No automatic format negotiation; if both PDF and PNG outputs are required, separate export calls are needed.

## Evidence

- [readme] Results are tabulated and saved as images and csv files: "Results are tabulated and saved as images and csv files"
- [other] CSV format serialization and image visualization generation process: "Serialize results table to CSV format using a CSV writer (e.g. pandas.DataFrame.to_csv or equivalent). 3. Generate visualization image(s) from the tabulated results (format and plot type determined"
- [other] Verification criteria for successful output: "Verify both CSV and image files are written to the designated output directory with correct format and non-zero size."
- [other] Input to the serialization step: "Load tabulated query results (in memory or from intermediate format produced by MassQL query execution)."
- [readme] Output file organization in MassQLab: "ms1_raw_df.csv: Raw query results + metadata"
