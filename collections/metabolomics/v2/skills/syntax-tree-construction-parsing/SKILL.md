---
name: syntax-tree-construction-parsing
description: Use when you have a domain-specific language (DSL) grammar specification and raw query strings that must be converted into structured intermediate representations for validation, transformation, or execution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0091
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
---

# syntax-tree-construction-parsing

## Summary

Convert a domain-specific query language string into an Abstract Syntax Tree (AST) via lexical tokenization and recursive descent or LALR parsing, validating syntactic and semantic constraints. This skill is essential for implementing expressive, unambiguous query languages that map human-readable syntax to structured, machine-executable representations.

## When to use

Apply this skill when you have a domain-specific language (DSL) grammar specification and raw query strings that must be converted into structured intermediate representations for validation, transformation, or execution. Specifically, use it when the query syntax combines SQL-inspired constructs with domain-specific operators (e.g., m/z ranges, intensity thresholds, fragmentation patterns in mass spectrometry) that require both syntactic parsing and semantic constraint enforcement.

## When NOT to use

- Input is already a parsed AST or intermediate representation; skip directly to AST validation or execution.
- The query syntax is simple enough to use string-based pattern matching or regex; full parser construction adds unnecessary complexity.
- Domain constraints and semantics are better handled post-parse by a separate validation layer; defer semantic checking if the grammar is purely syntactic.

## Inputs

- Raw query string in domain-specific language (e.g., MassQL query text)
- Grammar specification defining syntax rules and domain-specific operators
- Token definitions for lexer (keywords, operators, literals)

## Outputs

- Abstract Syntax Tree (AST) object representing the parsed query structure
- Serialized AST (JSON or canonical text format)
- Parsing diagnostic report (success/failure with error messages and positions)

## How to apply

First, define the complete grammar incorporating domain-specific constructs (e.g., spectrum filters, m/z ranges, intensity thresholds) aligned with design principles of expressiveness, precision, scalability, and natural readability. Implement a lexer that tokenizes the input query string, identifying SQL keywords, domain-specific operators, and numeric literals with their positions. Build a parser (recursive descent or LALR) that consumes the token stream and constructs an AST, enforcing both syntactic rules and semantic constraints (e.g., valid parameter ranges, type consistency). Validate the resulting AST against design criteria: confirm that complex domain patterns can be expressed unambiguously, that queries scale appropriately from single-item to repository-scale searches, and that human readability is maintained. Finally, serialize the AST to a canonical format (JSON or text) and generate diagnostic error messages (with line and column information) for any parsing failures.

## Related tools

- **MassQL** (Domain-specific query language for mass spectrometry; defines the grammar and design principles (expressiveness, precision, scalability, natural readability) that guide parser implementation.) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY scaninfo(MS2DATA) WHERE MS1MZ=100', input_filename='sample.mzML')
```

## Evaluation signals

- AST structure correctly represents all query clauses (SELECT, WHERE, AND conditions) with proper nesting and operator precedence.
- Lexer successfully tokenizes all valid domain-specific operators (e.g., MS1MZ, TOLERANCEMZ, INTENSITYPERCENT, MS2PREC in MassQL) without loss of numeric precision or operator semantics.
- Parser rejects syntactically invalid queries with diagnostic error messages citing line and column positions.
- Validated AST can be serialized to JSON and deserialized back to an equivalent structure without loss of information.
- Complex mass spectrometry patterns (e.g., multi-ion filters with intensity ratios and tolerance thresholds) parse unambiguously with no grammatical ambiguity.

## Limitations

- Parser performance may degrade on very large or deeply nested queries; scalability should be tested on realistic query complexity.
- Error recovery and partial parsing are not guaranteed; a single syntax error may prevent any output beyond the first failure point.
- The grammar must be maintained in sync with domain requirements; changes to expressiveness or precision constraints require grammar and parser updates.
- Semantic validation (e.g., enforcing valid m/z ranges, intensity bounds, or file format compatibility) is deferred to post-parse validation; the parser alone cannot guarantee semantic correctness.

## Evidence

- [intro] Design principle: Expressiveness - Capture complex mass spectrometry patterns: "Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for"
- [intro] Design principle: Precision - unambiguous specification: "Precision - Exactly prescribe how to find data without ambiguity"
- [other] Parsing workflow: lexer, parser, AST construction, validation: "Implement a lexer to tokenize the input MassQL query string, identifying SQL keywords, MS-specific operators, and numeric literals. 3. Implement a parser using recursive descent or LALR parsing to"
- [other] AST validation and serialization: "Validate the AST against the design criteria: confirm that complex MS patterns can be expressed unambiguously, that queries scale from single spectra to repository-scale searches, and that syntax"
- [readme] MassQL design: SQL-inspired with mass-spectrometry-specific constructs: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion. It is inspired by SQL, but it attempts to"
- [intro] Design principle: Relatively Natural - human readability: "Relatively Natural - MassQL should be relatively easy to read and write and even use to communicate ideas about mass spectrometry"
