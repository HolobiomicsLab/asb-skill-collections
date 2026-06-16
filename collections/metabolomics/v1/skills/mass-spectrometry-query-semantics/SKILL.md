---
name: mass-spectrometry-query-semantics
description: Use when when you need to enable users to express complex mass spectrometry search patterns (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - MassQL
derived_from:
- doi: 10.1038/s41592-025-02660-z
  title: massql
evidence_spans:
- The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massql
    doi: 10.1038/s41592-025-02660-z
    title: massql
  dedup_kept_from: coll_massql
schema_version: 0.2.0
---

# mass-spectrometry-query-semantics

## Summary

Design and implement a domain-specific query language (DSL) parser that translates mass-spectrometry-centric query strings into structured, unambiguous representations while preserving natural language readability. This skill bridges SQL-inspired syntax with MS-specific constructs (m/z ranges, intensity thresholds, fragmentation patterns) to enable precise, scalable querying across single spectra and repository-scale datasets.

## When to use

When you need to enable users to express complex mass spectrometry search patterns (e.g., isotope clusters, neutral losses, fragment ion ladders, precursor-product relationships) in a human-readable form that can be executed unambiguously against both local spectra files (mzML, mzXML) and large spectral repositories without manual translation to procedural code.

## When NOT to use

- Input is already a procedural code (C++, Python) that directly specifies spectrum filtering logic—use this skill only when raw MS data and human-readable query intent must be bridged.
- Query is purely generic SQL with no mass-spectrometry domain semantics (e.g., simple SELECT * FROM table WHERE id=5)—use standard SQL parsers instead.
- Data is already a pre-computed feature table or processed result matrix (e.g., abundance table, aligned LC-MS features)—this skill applies to raw or lightly processed spectra.

## Inputs

- MassQL query string (text)
- Optional: mass spectrometry data file (mzML, mzXML) or dataframe with MS1 and MS2 scans

## Outputs

- Abstract Syntax Tree (AST) in JSON or canonical text format
- Parsed query representation suitable for execution
- Parsing success/failure report with diagnostic error messages
- Results dataframe (scaninfo, ion matches, or spectra filtered by query constraints)

## How to apply

First, define a formal grammar extending SQL syntax with MS-specific operators and clauses (QUERY, WHERE, MS1DATA, MS2DATA, MS1MZ, MS2PREC, ATOLERANCEMZ, INTENSITYPERCENT, fragmentation pattern predicates). Implement a lexer to tokenize the input string into SQL keywords, MS domain tokens, and numeric literals. Use recursive descent or LALR parsing to build an Abstract Syntax Tree (AST) that enforces syntactic constraints and MS semantic rules (e.g., m/z tolerance must be non-negative, intensity thresholds must be 0–100 for percentages). Validate the AST against the four design principles: confirm that complex MS patterns are expressible without ambiguity, that queries scale from single spectra to repositories, that syntax remains readable, and that all MS-specific constructs are semantically valid. Serialize the validated AST to JSON or canonical text, and report parsing success with diagnostic error messages for invalid syntax or out-of-range parameters.

## Related tools

- **MassQL** (Domain-specific query language and reference implementation for parsing and executing mass spectrometry queries) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY MS2DATA WHERE MS1MZ=100 ATOLERANCEMZ=0.1', 'sample.mzML')
```

## Evaluation signals

- AST structure correctly reflects all MS-specific operators (MS1MZ, MS2PREC, ATOLERANCEMZ, INTENSITYPERCENT, INTENSITYMATCH, fragmentation patterns) with no loss of semantic information.
- Parsed query executes identically on a single spectrum and on an entire repository without requiring syntax changes, confirming scalability principle is satisfied.
- Complex MS patterns (e.g., isotope clusters with m/z spacing ±2 and intensity ratios, neutral loss ladders) can be expressed in a single, human-readable query without nested procedural constructs.
- All numeric parameters (tolerance ranges, intensity thresholds) are validated to be within valid MS ranges (e.g., 0–100 for intensity percentages, non-negative for m/z tolerance) and parsed query reports errors for out-of-range values.
- Parsed query can be serialized to JSON and round-tripped back to query string without loss of semantics or redundant parentheses/whitespace.

## Limitations

- Parser requires well-formed MassQL syntax; malformed queries produce diagnostic error messages but do not attempt error recovery or query repair.
- Expressiveness is bounded by the grammar; novel MS patterns not anticipated at language design time cannot be queried without extending the grammar and re-implementing the parser.
- Precision depends on exact specification of tolerance windows, intensity thresholds, and fragmentation rules; ambiguous or under-specified queries may match unintended spectra.
- No explicit changelog documented in the repository; version compatibility and breaking syntax changes are not systematically tracked.

## Evidence

- [readme] The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion.: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion."
- [intro] Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for: "Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for"
- [intro] Precision - Exactly prescribe how to find data without ambiguity: "Precision - Exactly prescribe how to find data without ambiguity"
- [intro] Scalable - Easily facilitating the querying of one spectrum all the way up to entire repositories of data: "Scalable - Easily facilitating the querying of one spectrum all the way up to entire repositories of data"
- [readme] Relatively Natural - MassQL should be relatively easy to read and write and even use to communicate ideas about mass spectrometry: "Relatively Natural - MassQL should be relatively easy to read and write and even use to communicate ideas about mass spectrometry"
- [other] Define the MassQL grammar as an extended SQL syntax incorporating mass-spectrometry-specific constructs (e.g., spectrum filters, m/z ranges, intensity thresholds, fragmentation patterns): "Define the MassQL grammar as an extended SQL syntax incorporating mass-spectrometry-specific constructs (e.g., spectrum filters, m/z ranges, intensity thresholds, fragmentation patterns)"
- [other] Implement a lexer to tokenize the input MassQL query string, identifying SQL keywords, MS-specific operators, and numeric literals.: "Implement a lexer to tokenize the input MassQL query string, identifying SQL keywords, MS-specific operators, and numeric literals."
- [other] Implement a parser using recursive descent or LALR parsing to build an Abstract Syntax Tree (AST) from the token stream, enforcing syntactic and semantic constraints.: "Implement a parser using recursive descent or LALR parsing to build an Abstract Syntax Tree (AST) from the token stream, enforcing syntactic and semantic constraints."
- [other] Serialize the AST to JSON or canonical text format and report parsing success/failure with diagnostic error messages.: "Serialize the AST to JSON or canonical text format and report parsing success/failure with diagnostic error messages."
