---
name: query-result-tabulation
description: Use when after executing MassQL queries against mzML mass spectrometry files when you need to organize heterogeneous scan-level results (MS1 and MS2 data) into consistent tabular schemas for batch analysis, statistical comparison across files/queries, or visual summary generation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MassQLab
  - MassQL
derived_from:
- doi: 10.1002/rcm.10132
  title: MassQLab
evidence_spans:
- github.com__JohnsonDylan__MassQLab
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

# Query Result Tabulation

## Summary

Convert unstructured mass spectrometry query results into structured tabular formats (CSV, images) suitable for downstream analysis and interpretation. This skill transforms raw MassQL query outputs into organized data frames with metadata, enabling systematic peak analysis, retention time statistics, and cross-file comparisons.

## When to use

Apply this skill after executing MassQL queries against mzML mass spectrometry files when you need to organize heterogeneous scan-level results (MS1 and MS2 data) into consistent tabular schemas for batch analysis, statistical comparison across files/queries, or visual summary generation. Use it specifically when raw query results need to be enriched with metadata and prepared for downstream analysis such as peak fitting, clustering, or intensity-based comparisons.

## When NOT to use

- Input is already a feature matrix or pre-aggregated abundance table (tabulation is for raw scan-level query results)
- MassQL queries have not yet been executed or no query results are available
- Output schema must conform to a pre-specified format incompatible with separate MS1/MS2 tables or timestamp-based directory organization

## Inputs

- MassQL query result objects (scan-level data from MS1DATA and MS2DATA queries)
- mzML file paths and metadata (file names, scan counts)
- Query definitions (query name, query string, query type: MS1 or MS2)
- Configuration parameters (output directory path, analysis flag, cache setting)

## Outputs

- ms1_raw_df.csv — raw MS1 query results with scan metadata
- ms1_analysis_df.csv — MS1 peak fitting analysis and Gaussian parameters
- ms1_RT_analysis_df.csv — retention time statistics vs. query RT window
- ms2_raw_df.csv — raw MS2 query results with precursor and product ion data
- ms2_analysis_df.csv — MS2 peak picking and intensity analysis
- ms1_traces.pdf — Gaussian peak fits per query/file combination
- ms2_plots.pdf — MS2 scan intensities with MS1 linkage lines
- ms2_summary_plots.pdf — top scan per query
- ms2_cluster_plots.pdf — MS2 analysis clustered by energy level or group

## How to apply

After MassQL queries return raw scan-level data, aggregate the results into separate data frames for MS1 and MS2 scans, each including query metadata (query name, file source, scan identifiers, m/z values, retention times, and intensity measurements). For MS1 results, compute auxiliary columns such as retention time statistics relative to the query RT window and prepare data for Gaussian peak fitting. For MS2 results, preserve precursor m/z, product ion m/z, and neutral loss information alongside scan-level total intensities. Export both raw and analysis-enriched tables as CSV files, indexed by timestamp and organized into separate MS1 and MS2 output directories. Simultaneously generate corresponding visualization PDFs (traces, summary plots, cluster plots) to enable rapid quality assessment and cross-query/cross-file pattern recognition.

## Related tools

- **MassQL** (Domain-specific query language used to define which mass spectrometry scans and features to extract before tabulation) — https://github.com/mwang87/MassQueryLanguage
- **MassQLab** (Workflow orchestrator that applies MassQL queries to mzML directories and invokes tabulation and visualization on results) — https://github.com/JohnsonDylan/MassQLab

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query(input_query, input_filename); results_df.to_csv('ms2_raw_df.csv', index=False)
```

## Evaluation signals

- All query results are present in output CSVs with no missing rows relative to MassQL query execution logs
- CSV files contain expected column names and data types (e.g., MS1MZ as float, scan as int, retention_time as float)
- MS1 and MS2 results are in separate tables with no cross-contamination (MS2-specific fields absent from MS1 table)
- Generated PDF plots contain data points that correspond to CSV rows (e.g., scatter plot points match raw_df row count)
- Output directory structure matches timestamp-based naming convention with subdirectories for MS1 and MS2 results

## Limitations

- MassQLab processes ALL files in the specified data_directory indiscriminately; selective file filtering must be done upstream
- Output organization by timestamp can lead to orphaned or hard-to-trace results if multiple runs are executed in rapid succession
- Peak fitting analysis (Gaussian fits for MS1) assumes unimodal or separable peak shapes; may fail or produce misleading results for co-eluting features
- MS2 clustering by energy level requires explicit energy metadata in mzML headers; missing or malformed metadata will degrade cluster plots

## Evidence

- [intro] Results are tabulated and saved as images and csv files: "Results are tabulated and saved as images and csv files"
- [other] Tabulate query results into structured tables and save as CSV/images: "4. Tabulate query results into structured tables. 5. Save tabulated results as CSV files and generate corresponding visualization images."
- [readme] MS1 and MS2 output tables with analysis and metadata: "ms1_raw_df.csv: Raw query results + metadata; ms1_analysis_df.csv: Peak fitting analysis; ms2_raw_df.csv: Raw query results + metadata; ms2_analysis_df.csv: Peak picking analysis"
- [readme] Retention time analysis computed relative to query window: "ms1_RT_analysis_df.csv: RT stats vs. query RT"
- [readme] Configuration determines whether downstream analysis is performed: "analysis: Whether to run downstream analysis on results returned from the MassQL queries (true or false)."
