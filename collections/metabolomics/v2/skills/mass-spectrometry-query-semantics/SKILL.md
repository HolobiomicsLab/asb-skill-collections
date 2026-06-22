---
name: mass-spectrometry-query-semantics
description: Use when when you need to express complex mass spectrometry search patterns (e.g., isotope envelope detection, neutral loss patterns, intensity relationships across m/z ranges) in a human-readable format that can be executed against spectral data files (mzML, mzXML) or spectral repositories.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SQL
  - MassQL (reference implementation)
derived_from:
- doi: 10.1038/s41592-025-02785-1
  title: MassQL
evidence_spans:
- It is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massql
    doi: 10.1038/s41592-025-02785-1
    title: MassQL
  - build: coll_massql_2_cq
    doi: 10.1038/s41592-025-02785-1
    title: MassQL
  dedup_kept_from: coll_massql_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02785-1
  all_source_dois:
  - 10.1038/s41592-025-02785-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-query-semantics

## Summary

Parse and validate SQL-inspired domain-specific language queries into structured representations for mass spectrometry data search. MassQL embeds mass spectrometry assumptions (mass-to-charge ratio, retention time, intensity filtering) into query syntax to enable natural, succinct expression of complex MS patterns across single spectra to entire repositories.

## When to use

When you need to express complex mass spectrometry search patterns (e.g., isotope envelope detection, neutral loss patterns, intensity relationships across m/z ranges) in a human-readable format that can be executed against spectral data files (mzML, mzXML) or spectral repositories. Use this skill when SQL-like filtering alone is insufficient because the query logic must encode domain assumptions about retention time, mass accuracy tolerance, or intensity matching thresholds specific to MS data.

## When NOT to use

- Input data is already a feature table or processed abundance matrix without raw spectral scan information.
- Query logic requires operations not expressible in mass spectrometry domain (e.g., arbitrary relational joins across unrelated datasets).
- Spectral data is in a format other than mzML/mzXML without prior conversion.

## Inputs

- MassQL query string (e.g., 'QUERY MS2DATA WHERE MS1MZ=100')
- Mass spectrometry data file in mzML or mzXML format
- Optional: pre-loaded pandas DataFrame pair (ms1_df, ms2_df) from spectral data

## Outputs

- Abstract syntax tree (AST) or canonical JSON representation of parsed query
- Results DataFrame or TSV file containing matching scans with scan metadata and intensity values

## How to apply

Construct a MassQL query string using SQL-inspired syntax with mass spectrometry parameters (MS1MZ, MS2DATA, TOLERANCE, INTENSITYPERCENT, etc.). Invoke the MassQL parser/engine to tokenize the query string into recognized MS-specific tokens, then construct an abstract syntax tree (AST) or canonical JSON representation. Validate that the parse tree captures expressiveness (complex MS patterns), precision (unambiguous filter semantics), and scalability (handles from single spectrum to repository scale). Execute the parsed query against input spectral data (provided as mzML file or pre-loaded pandas DataFrames) to retrieve matching scan records. Return results as a structured table (TSV or DataFrame) containing scan metadata and intensity values meeting the query criteria.

## Related tools

- **MassQL (reference implementation)** (Domain-specific language parser and query engine for mass spectrometry data; provides Python API, CLI tool, and web API for query execution) — https://github.com/mwang87/MassQueryLanguage
- **SQL** (Syntactic inspiration and design paradigm for query expression in MassQL)

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY MS2DATA WHERE MS1MZ=100', 'sample.mzML')
```

## Evaluation signals

- Parse succeeds without syntax error and produces valid JSON or AST representation with all query clauses (QUERY, WHERE, AND operators) correctly mapped.
- Returned results satisfy the specified filtering criteria: m/z values within stated TOLERANCE, intensity percentages meet INTENSITYPERCENT thresholds, retention time ranges (if specified) are respected.
- Results are consistent across different execution paths (file-based load vs. pre-loaded DataFrame produce identical outputs).
- Query execution scales appropriately: single-spectrum queries return quickly; repository-scale queries complete without memory overflow or timeout.
- Intermediate JSON representation is readable and preserves semantic meaning: parameter names, filter operators, and logical conjunctions (AND) are preserved and unambiguous.

## Limitations

- No formal changelog documented; version compatibility and breaking changes are not explicitly tracked.
- Query expressiveness is bounded by the predefined MS-specific parameter set (MS1MZ, MS2DATA, TOLERANCE, etc.); custom domain logic outside these parameters cannot be encoded directly.
- Scalability to very large repositories (tested up to repository scale in principle) requires external workflow integration (NextFlow, ProteoSAFe) not provided in the core API.
- Mass accuracy tolerance (e.g., ppm or Da) must be specified manually per query; no automatic calibration or adaptive tolerance is performed.

## Evidence

- [readme] Domain-specific language design goal and SQL inspiration: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion. It is inspired by SQL, but it attempts to"
- [readme] Core design principles including expressiveness and scalability: "Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for. Scalable - Easily facilitating the querying of one spectrum all the way up to entire"
- [other] Parser construction workflow: "Construct a parser (e.g., using recursive descent or parser generator such as ANTLR or PLY) that consumes tokens and produces a structured abstract syntax tree (AST) or query object representation"
- [readme] Python API usage pattern: "results_df = msql_engine.process_query(input_query, input_filename, ms1_df=ms1_df, ms2_df=ms2_df)"
- [readme] Natural language design goal for MS users: "Relatively Natural - MassQL should be relatively easy to read and write and even use to communicate ideas about mass spectrometry"
