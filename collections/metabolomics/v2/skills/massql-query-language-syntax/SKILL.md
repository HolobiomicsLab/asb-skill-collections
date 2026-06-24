---
name: massql-query-language-syntax
description: Use when you need to search for specific mass spectrometry patterns (e.g.,
  precursor ion m/z, product ion presence, retention time windows, intensity constraints,
  neutral loss patterns) across one or more mzML files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MassQL
  - MassQLab
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1002/rcm.10132
  title: MassQLab
evidence_spans:
- MassQLab applies a series of queries (written in the language of MassQL)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MassQL Query Language Syntax

## Summary

MassQL is a domain-specific language designed for succinct, mass-spectrometry-centric querying of MS1 and MS2 spectral data. It abstracts common mass spectrometry patterns (precursor/product ion filtering, retention time ranges, intensity thresholds, neutral losses) into readable query syntax, enabling users to express complex spectral searches without ambiguity.

## When to use

Use this skill when you need to search for specific mass spectrometry patterns (e.g., precursor ion m/z, product ion presence, retention time windows, intensity constraints, neutral loss patterns) across one or more mzML files. This is appropriate when your analysis goal is to identify and tabulate scans matching defined criteria rather than to perform statistical modeling or unsupervised feature discovery.

## When NOT to use

- When you need to perform statistical inference, hypothesis testing, or multiple-comparison correction—MassQL returns raw matches, not p-values or adjusted statistics.
- When your input data is already in a processed feature table or peak list without raw spectrum-level information—MassQL operates on MS1/MS2 scan data.
- When you need unsupervised discovery of novel patterns or clustering—MassQL is a targeted query engine, not a feature-extraction or machine-learning framework.

## Inputs

- mzML mass spectrometry file (single file or directory of files)
- MassQL query string (e.g., 'QUERY scaninfo(MS2DATA) WHERE MS2PREC=429.3765:TOLERANCEPPM=2.5')
- Optional: pre-loaded MS1 dataframe and MS2 dataframe (to bypass file I/O)

## Outputs

- Pandas DataFrame with query results (columns: scan number, retention time, m/z, intensity, and query metadata)
- Optional: TSV/CSV file with tabulated results
- Optional: visualization images (PNG, PDF) of matched spectra

## How to apply

Construct a MassQL query string following the domain-specific syntax: begin with QUERY and specify the data type (MS1DATA or MS2DATA); use WHERE clauses to filter by m/z (MS1MZ, MS2PREC, MS2PROD, MS2NL) with tolerance parameters (TOLERANCEPPM or TOLERANCEMZ); add retention time constraints (RTMIN, RTMAX); optionally use FILTER clauses to extract specific peak intensities; and execute the query via the Python API (`msql_engine.process_query(input_query, input_filename)`) or CLI (`massql test.mzML "QUERY..."`). The query engine parses the string, applies it to loaded MS1/MS2 data frames, and returns a tabulated results dataframe. Verify correctness by checking that returned scan numbers, m/z values, and intensities match expected ranges and that the result schema includes expected columns (e.g., scaninfo, retention time, precursor m/z).

## Related tools

- **MassQL** (Query language engine and reference implementation; provides Python API and CLI for executing queries against MS1/MS2 data) — https://github.com/mwang87/MassQueryLanguage
- **MassQLab** (Application layer that orchestrates batch MassQL query execution across mzML file directories, handles result tabulation and visualization) — https://github.com/JohnsonDylan/MassQLab

## Examples

```
massql test.mzML "QUERY scaninfo(MS2DATA) WHERE MS2PREC=429.3765:TOLERANCEPPM=2.5 AND RTMIN=9.0 AND RTMAX=9.5 FILTER MS2PROD=85.0281:TOLERANCEPPM=10" --output_file results.tsv
```

## Evaluation signals

- Returned DataFrame row count matches the expected number of scans satisfying the WHERE/FILTER criteria (verify by spot-checking a few scan numbers and m/z values against raw mzML).
- All returned precursor or product m/z values fall within the specified tolerance window (e.g., TOLERANCEPPM=2.5 means ±2.5 ppm of the target m/z).
- Retention time (RT) values of returned rows fall within specified RTMIN and RTMAX boundaries (if specified).
- Intensity columns (if filtered via FILTER clause) contain non-null values matching the target peak m/z within the query's tolerance.
- No rows are returned when the query specifies a highly restrictive m/z value or RT window that should yield zero matches in the input file.

## Limitations

- MassQL processes all files in a directory without selective filtering; selective file processing requires pre-filtering the directory or post-filtering results.
- Raw-to-mzML conversion (via msconvert) is experimental; use ProteoWizard msconvert separately for production workflows.
- Query execution time scales linearly with the number of scans and files; very large repositories may benefit from distributed execution (NextFlow workflow mentioned but not detailed in README).
- Caching (via Feather format) is optional and must be explicitly enabled in configuration; repeated queries without caching will re-parse and re-scan the mzML data.

## Evidence

- [readme] The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion.: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion."
- [readme] it attempts to bake in assumptions of mass spectrometry to make querying much more natural for mass spectrometry users.: "it attempts to bake in assumptions of mass spectrometry to make querying much more natural for mass spectrometry users."
- [readme] results_df = msql_engine.process_query(input_query, input_filename): "results_df = msql_engine.process_query(input_query, input_filename)"
- [readme] MassQLab applies a series of queries (written in the language of MassQL) to a directory containing mass spectrometry data in mzML format.: "MassQLab applies a series of queries (written in the language of MassQL) to a directory containing mass spectrometry data in mzML format."
- [readme] Get MS2 scans with a precursor ion matching m/z 429.3765, retention time between 9.0 and 9.5 minutes, and return intensity of the peak with m/z 85.0281: "Get MS2 scans with a precursor ion matching m/z 429.3765, retention time between 9.0 and 9.5 minutes, and return intensity of the peak with m/z 85.0281"
- [readme] Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for. Precision - Exactly prescribe how to find data without ambiguity.: "Expressiveness - Capture complex mass spectrometry patterns; Precision - Exactly prescribe how to find data without ambiguity"
