---
name: mass-spectrometry-data-querying
description: Use when you have a directory of mzML mass spectrometry files and need to systematically identify and extract scans or peaks matching specific m/z values, retention time windows, intensity thresholds, or spectral fingerprints (e.g., product ion patterns, neutral loss signatures).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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

# mass-spectrometry-data-querying

## Summary

Execute domain-specific queries against collections of mass spectrometry files in mzML format to extract and tabulate spectral features matching user-defined criteria (m/z, retention time, intensity, product ions, neutral losses). This skill bridges SQL-like query expressiveness with mass spectrometry domain assumptions, enabling reproducible extraction of complex spectral patterns from large datasets.

## When to use

You have a directory of mzML mass spectrometry files and need to systematically identify and extract scans or peaks matching specific m/z values, retention time windows, intensity thresholds, or spectral fingerprints (e.g., product ion patterns, neutral loss signatures). Use this skill when manual inspection is infeasible and you require reproducible, parameterizable queries that can be applied uniformly across multiple files.

## When NOT to use

- Input files are not in mzML format (or cannot be converted to mzML) — use MSConvert to pre-convert raw files before applying this skill.
- You need to perform de novo spectral library matching or molecular networking — use specialized tools like GNPS or spectral alignment libraries instead.
- The query patterns you seek are better expressed as statistical comparisons (e.g., case vs. control intensity ratios) rather than deterministic m/z or RT matching — consider statistical proteomics workflows.

## Inputs

- Directory containing .mzML files (mass spectrometry data)
- Query file (JSON, CSV, or XLSX) defining MassQL queries with name and query string fields
- Configuration file (massqlab_config.json) specifying data_directory, queryfile, output_directory, and analysis flags

## Outputs

- ms1_raw_df.csv or ms2_raw_df.csv: tabulated query results with scan metadata
- ms1_analysis_df.csv or ms2_analysis_df.csv: downstream analysis (peak fitting or peak picking results)
- PDF or PNG visualizations: Gaussian fits, scan intensity plots, summary traces, peak area distributions
- Intermediate Feather cache file (if cache_setting enabled) for faster re-querying

## How to apply

Define one or more MassQL queries specifying MS1 or MS2 search criteria (e.g., MS1MZ=207.1418:TOLERANCEPPM=2.5 with RTMIN and RTMAX constraints, or MS2PREC and MS2PROD patterns). Load all mzML files from the target directory using MassQLab's file-discovery mechanism. Parse and validate each query, then apply them sequentially to the loaded mass spectrometry data via the MassQL query engine. The engine matches spectral features against the query predicates and returns matching scan metadata. Tabulate the results into structured DataFrames, then save as CSV files and generate visualization images (Gaussian fits for MS1, scan intensity plots for MS2). Optionally enable downstream analysis (peak fitting for MS1 traces, peak picking for MS2 scans) to quantify peak areas and isotope patterns.

## Related tools

- **MassQL** (Domain-specific query language and reference implementation for expressing and executing mass spectrometry pattern queries) — https://github.com/mwang87/MassQueryLanguage
- **MassQLab** (High-level workflow orchestrator that applies MassQL queries to directories of mzML files, tabulates results, generates visualizations, and enables downstream analysis) — https://github.com/JohnsonDylan/MassQLab

## Examples

```
py src/MassQLab_console.py  # Executes the full pipeline with queries from massqlab_config.json applied to all .mzML files in data_directory, saving CSV and PDF results to MassQLab_Output
```

## Evaluation signals

- Output CSV files contain all expected columns: scan index, m/z, retention time, intensity, and any query-specific metadata (e.g., product ion intensities)
- Number of matched scans is consistent across re-runs on the same input files and query set (deterministic results)
- Visualization PDFs/PNGs show matched peaks at the specified m/z ± tolerance windows and within the defined retention time ranges
- Peak area and Gaussian fit parameters in analysis CSVs are non-negative and physically plausible (e.g., width > 0, area > 0)
- Query execution time scales sublinearly with file count when caching is enabled, indicating proper intermediate storage

## Limitations

- MassQLab processes ALL files in the specified data_directory; no per-file filtering is provided at configuration time.
- Raw-to-mzML conversion (via msconvert) is experimental and may fail silently or produce incomplete conversions; ProteoWizard msconvert is recommended for pre-conversion.
- Query syntax and semantics are specific to MassQL; complex statistical or machine-learning-based filters cannot be expressed natively and require external preprocessing.
- MS1 peak fitting assumes Gaussian lineshape; heavily distorted or overlapped peaks may yield unreliable area estimates.
- Downstream analysis (peak fitting, peak picking) is optional and controlled by the analysis flag; results vary in completeness depending on cache_setting and file availability.

## Evidence

- [readme] MassQLab applies a series of queries (written in the language of MassQL) to a directory containing mass spectrometry data in mzML format: "MassQLab applies a series of queries (written in the language of MassQL) to a directory containing mass spectrometry data in mzML format"
- [readme] Results are tabulated and saved as images and csv files: "Results are tabulated and saved as images and csv files"
- [readme] The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion"
- [other] Load all mzML files from the input directory using MassQLab's file-discovery mechanism. Parse and validate the MassQL query set provided as input. Apply each MassQL query sequentially to the loaded mass spectrometry data using the MassQL query engine. Tabulate query results into structured tables. Save tabulated results as CSV files and generate corresponding visualization images.: "Load all mzML files from the input directory using MassQLab's file-discovery mechanism. Parse and validate the MassQL query set provided as input. Apply each MassQL query sequentially to the loaded"
- [readme] Each query in the file must include the following: name: A unique name for each query (per MS1/MS2 type). query: The MassQL query string itself.: "Each query in the file must include the following: name: A unique name for each query (per MS1/MS2 type). query: The MassQL query string itself."
- [readme] MS1 Outputs: ms1_raw_df.csv, ms1_analysis_df.csv, ms1_RT_analysis_df.csv, ms1_traces.pdf. MS2 Outputs: ms2_raw_df.csv, ms2_analysis_df.csv, ms2_plots.pdf: "Results are saved in MassQLab_Output inside the defined output_directory, organized by timestamp. MS1 Outputs: ms1_raw_df.csv, ms1_analysis_df.csv, ms1_RT_analysis_df.csv, ms1_traces.pdf. MS2"
- [readme] Get MS2 scans with a precursor ion matching m/z 429.3765, retention time between 9.0 and 9.5 minutes, and return intensity of the peak with m/z 85.0281: QUERY scaninfo(MS2DATA) WHERE MS2PREC=429.3765:TOLERANCEPPM=2.5 AND RTMIN=9.0 AND RTMAX=9.5 FILTER MS2PROD=85.0281:TOLERANCEPPM=10: "Get MS2 scans with a precursor ion matching m/z 429.3765, retention time between 9.0 and 9.5 minutes, and return intensity of the peak with m/z 85.0281: QUERY scaninfo(MS2DATA) WHERE"
- [readme] if cache_setting is true, saves an intermediate Feather file to disk and uses it for faster re-querying: "if cache_setting is true, saves an intermediate Feather file to disk and uses it for faster re-querying"
