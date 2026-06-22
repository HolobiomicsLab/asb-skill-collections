---
name: lexical-analysis-tokenization
description: Use when you have a mass-spectrometry query string written in MassQL (or similar domain-specific SQL-inspired syntax) that must be converted into structured form for execution. The input is raw, unparsed text containing SQL keywords, MS-specific operators (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - MassQL
derived_from:
- doi: 10.1038/s41592-025-02785-1
  title: MassQL
evidence_spans:
- The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massql
    doi: 10.1038/s41592-025-02785-1
    title: MassQL
  dedup_kept_from: coll_massql
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

# lexical-analysis-tokenization

## Summary

Tokenize domain-specific query strings (e.g., MassQL) into a stream of meaningful lexical units (keywords, operators, numeric literals, identifiers) to enable downstream parsing and AST construction. This is the first stage of a compiler/interpreter pipeline for mass-spectrometry-centric query languages.

## When to use

You have a mass-spectrometry query string written in MassQL (or similar domain-specific SQL-inspired syntax) that must be converted into structured form for execution. The input is raw, unparsed text containing SQL keywords, MS-specific operators (e.g., MS1MZ, MS2PREC, TOLERANCEMZ, INTENSITYPERCENT), numeric m/z and intensity thresholds, and logical connectives (AND, OR). Tokenization is necessary before you can build an Abstract Syntax Tree (AST) or validate query semantics.

## When NOT to use

- Input is already a pre-tokenized or parsed representation (e.g., JSON-serialized query object, AST). Skip directly to semantic validation or execution.
- You only need to execute a pre-compiled query; the query text has already been tokenized and validated by an earlier stage of the pipeline.
- Input is free-form natural language prose, not a formal query syntax. Domain-specific tokenization assumes formal grammar; unstructured text requires NLP preprocessing instead.

## Inputs

- MassQL query string (raw text)
- MassQL grammar specification (keywords, operators, token patterns)

## Outputs

- Token stream (sequence of (token_type, token_value, position) tuples)
- Lexical error report (if unrecognized input encountered)

## How to apply

Implement a lexer that scans the input MassQL query string character-by-character, recognizing and classifying tokens according to the MassQL grammar. Group characters into meaningful units: (1) SQL and MS-specific keywords (QUERY, WHERE, MS1DATA, MS2DATA, scaninfo, PREC, MZ); (2) comparison and logical operators (=, AND, +, −); (3) numeric literals (m/z values, tolerance thresholds, intensity percentages); (4) special syntax (parentheses, colons for key-value pairs like TOLERANCEMZ=0.1). Use a whitespace-aware strategy to delimit tokens. Emit a stream of (token_type, token_value) pairs, preserving enough positional information to generate diagnostic error messages if parsing fails later. Validate that all tokens are recognized; if an unrecognized character sequence is encountered, halt with a clear error indicating the location and unexpected input.

## Related tools

- **MassQL** (Domain-specific query language whose syntax defines the lexical grammar (keywords, operators, literals) to be tokenized) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY MS2DATA WHERE MS1MZ=572.828 TOLERANCEMZ=0.1 AND MS2PREC=572.828', 'sample.mzML')
```

## Evaluation signals

- All valid MassQL tokens (SQL keywords like QUERY, WHERE; MS-specific operators like MS1MZ, MS2DATA, TOLERANCEMZ; numeric literals; parentheses) are correctly classified and emitted in order.
- Whitespace and comment regions are properly skipped; output token stream contains no spurious whitespace tokens.
- Compound tokens (e.g., 'MS1MZ=0.1' vs. separate 'MS1MZ' and '=' and '0.1' tokens) are split or grouped according to the grammar specification; test with multi-clause queries (AND chains with nested parentheses).
- Unrecognized input (typos, invalid operators, malformed numeric literals) triggers a lexical error with source location (line, column), enabling user diagnosis.
- Token stream is sufficient to reconstruct a recognizable approximation of the original query (round-trip test): serialize tokens back to text and compare against normalized input.

## Limitations

- Lexical analysis does not validate semantic correctness (e.g., whether MS1MZ tolerance is physically reasonable or whether a referenced filter exists). Semantic checks are deferred to the parser and AST validator.
- Error recovery is minimal: the lexer typically stops at the first unrecognized token. Batch error collection (reporting all lexical issues in one pass) would require more sophisticated tokenization.
- The lexer assumes well-formed input encoding (UTF-8 or ASCII); binary or mixed-encoding query strings may cause silent misclassification.
- No support for comments or query metadata (e.g., /* comment */ syntax) unless explicitly defined in the grammar.

## Evidence

- [other] Implement a lexer to tokenize the input MassQL query string, identifying SQL keywords, MS-specific operators, and numeric literals.: "Implement a lexer to tokenize the input MassQL query string, identifying SQL keywords, MS-specific operators, and numeric literals."
- [readme] MassQL is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry to make querying much more natural for mass spectrometry users.: "MassQL is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry to make querying much more natural for mass spectrometry users."
- [other] Define the MassQL grammar as an extended SQL syntax incorporating mass-spectrometry-specific constructs (e.g., spectrum filters, m/z ranges, intensity thresholds, fragmentation patterns): "Define the MassQL grammar as an extended SQL syntax incorporating mass-spectrometry-specific constructs (e.g., spectrum filters, m/z ranges, intensity thresholds, fragmentation patterns)"
- [other] Serialize the AST to JSON or canonical text format and report parsing success/failure with diagnostic error messages.: "Serialize the AST to JSON or canonical text format and report parsing success/failure with diagnostic error messages."
