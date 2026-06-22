---
name: mass-spectrometry-domain-specific-language-comprehension
description: Use when you need to translate user-facing mass spectrometry query intent (e.g., 'find all MS2 spectra with a precursor ion at m/z 572.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - SQL
  - massql
  techniques:
  - tandem-MS
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
  - build: coll_massql_cq
    doi: 10.1038/s41592-025-02785-1
    title: MassQL
  dedup_kept_from: coll_massql_cq
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

# mass-spectrometry-domain-specific-language-comprehension

## Summary

Parse, validate, and execute MassQL queries—a SQL-inspired domain-specific language that bakes mass spectrometry assumptions into syntax and semantics to enable succinct, scalable expression of complex mass spectrometry patterns. This skill bridges natural language query intent with structured abstract syntax trees (ASTs) and executable query plans over MS1 and MS2 spectral data.

## When to use

Use this skill when you need to translate user-facing mass spectrometry query intent (e.g., 'find all MS2 spectra with a precursor ion at m/z 572.828 and characteristic isotope patterns') into a machine-executable search plan that respects mass spectrometry constraints (mass tolerance in ppm, scan type, intensity thresholds, precursor matching). Critical when implementing a search interface over spectral repositories or automating batch querying of mzML/mzXML files with mass spectrometry-aware filtering.

## When NOT to use

- Query intent is a simple, low-level scan filter that does not involve mass spectrometry-specific patterns (e.g., 'return all scans with ID > 1000')—use direct spectral indexing instead.
- Input is already a pre-filtered feature table or peak list; MassQL operates on raw/centroided spectra with MS1 and MS2 data, not derived abundance matrices.
- Query requires ad-hoc statistical modeling or machine learning on spectral features beyond mass matching and intensity constraints—use a data analysis framework (scipy, scikit-learn) instead.

## Inputs

- MassQL query string (e.g., 'QUERY scaninfo(MS2DATA) WHERE MS1MZ=100')
- mzML or mzXML spectral data file
- Optional: preloaded MS1 and MS2 DataFrames

## Outputs

- Abstract syntax tree (JSON representation of parsed query structure)
- Results DataFrame or TSV file with matching scans (scan ID, precursor m/z, retention time, intensity, scan type)

## How to apply

Obtain the MassQL reference parser from the mwang87/MassQueryLanguage repository. Tokenize the input MassQL query string into lexical elements (keywords: QUERY, WHERE, AND, MS1DATA, MS2DATA; identifiers: MS1MZ, MS2PREC, TOLERANCEMZ, INTENSITYPERCENT; operators and literals). Build an abstract syntax tree by consuming tokens with recursive descent parsing, capturing query clauses (SELECT/QUERY scaninfo(), WHERE conditions with mass tolerance and intensity constraints), and serialize to JSON. Validate the AST structure by checking that mass tolerance values are positive floats, intensity percentages fall within 0–100%, and scan type specifiers are recognized. Load reference spectra (MS1 and MS2 data frames) from the input mzML file, then traverse the AST to apply filters sequentially (mass window matching, intensity thresholding, precursor constraints), returning results as a TSV or DataFrame. Correctness is confirmed when parsed queries match the reference examples and the final result set contains only spectra satisfying all WHERE constraints.

## Related tools

- **massql** (Python API and command-line utility to parse, validate, and execute MassQL queries on spectral data) — https://github.com/mwang87/MassQueryLanguage
- **SQL** (Inspiration and syntactic model for MassQL grammar and query structure)

## Examples

```
massql test.mzML "QUERY scaninfo(MS2DATA) WHERE MS1MZ=100" --output_file results.tsv
```

## Evaluation signals

- Parsed AST contains expected clauses (QUERY, WHERE) with correct token types (MS1MZ, MS2DATA, TOLERANCEMZ) and no syntax errors.
- Mass tolerance values are positive scalars (e.g., TOLERANCEMZ=0.1 for 0.1 m/z or ppm); intensity percentages are integers in [0, 100].
- Results DataFrame row count is ≤ total input scans and all returned scans have m/z values within the specified tolerance window and intensity above the threshold.
- Parsed query output matches reference examples from the mwang87/MassQueryLanguage repository documentation and test fixtures.
- Round-trip consistency: re-parsing the serialized JSON AST yields an equivalent AST without information loss.

## Limitations

- MassQL is optimized for querying spectra with well-defined precursor masses and intensity patterns; it may not handle unusual or corrupted mzML files (missing MS1/MS2 pairs, malformed metadata) gracefully.
- Performance scales with repository size; querying entire GNPS repositories may require distributed execution (NextFlow workflow) rather than single-process parsing.
- No changelog available in the repository, making it difficult to track API breaking changes or deprecated query syntax across versions.

## Evidence

- [readme] The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion. It is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion. It is inspired by SQL, but it attempts to"
- [readme] Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for: "Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for"
- [readme] Scalable - Easily facilitating the querying of one spectrum all the way up to entire repositories of data: "Scalable - Easily facilitating the querying of one spectrum all the way up to entire repositories of data"
- [other] MassQL is designed as a domain-specific language that expresses mass spectrometry queries by baking mass spectrometry assumptions into the language syntax and semantics: "MassQL is designed as a domain-specific language that expresses mass spectrometry queries by baking mass spectrometry assumptions into the language syntax and semantics"
- [other] Implement a parser (recursive descent or similar) that consumes tokens and builds a structured AST representation. Serialize the AST to JSON format, preserving query components (SELECT clauses, WHERE conditions, mass tolerance, scan type constraints, etc.): "Implement a parser (recursive descent or similar) that consumes tokens and builds a structured AST representation. Serialize the AST to JSON format, preserving query components (SELECT clauses, WHERE"
