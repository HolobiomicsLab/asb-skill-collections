---
name: lexer-tokenizer-implementation
description: Use when when you need to parse a domain-specific query language (like MassQL) into an abstract syntax tree (AST), and the query strings must be decomposed into discrete lexical units before syntactic analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - SQL
  - MassQueryLanguage (mwang87/MassQueryLanguage)
  - massql (Python package)
  techniques:
  - mass-spectrometry
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

# lexer-tokenizer-implementation

## Summary

Implement a lexer (tokenizer) that breaks domain-specific query strings into meaningful tokens (keywords, identifiers, operators, literals) as the first stage of parsing. This skill is essential for converting raw query syntax into a token stream that a parser can consume to build structured representations.

## When to use

When you need to parse a domain-specific query language (like MassQL) into an abstract syntax tree (AST), and the query strings must be decomposed into discrete lexical units before syntactic analysis. Use this skill when designing or implementing a query parser where the input is raw text and the first step is to identify and classify meaningful tokens according to the language grammar.

## When NOT to use

- Input is already a pre-tokenized or intermediate representation (e.g., JSON AST, token stream)—skip directly to parsing or validation.
- Query language uses only trivial delimiters (e.g., space-separated fields)—simple string splitting may suffice instead of a full lexer.
- You are working with a well-established query language with existing, maintained tokenizer libraries—prefer the reference implementation over reimplementation.

## Inputs

- Raw MassQL query string (e.g., 'QUERY scaninfo(MS2DATA) WHERE MS1MZ=100')
- Domain-specific language grammar specification (lexical rules, keyword list, operator definitions)

## Outputs

- Sequence of Token objects (token type, value, position/line/column metadata)
- Token stream suitable for parser consumption

## How to apply

Analyze the domain-specific language grammar to identify lexical categories: keywords (e.g., QUERY, WHERE, MS1DATA), identifiers (variable or field names), operators (=, AND, etc.), numeric and string literals, and special symbols. Design token types (enums or classes) for each category. Implement a tokenizer that scans the input query string sequentially, matching character sequences against lexical rules (keywords, regex patterns for numbers/identifiers) and emitting Token objects containing type, value, and position metadata. Use techniques like longest-match and lookahead to resolve ambiguities (e.g., distinguishing keywords from identifiers). Validate the token stream by verifying it contains no unexpected characters and that token sequences respect basic structural constraints (e.g., operators are not adjacent). The output token stream should be complete and unambiguous, ready for consumption by a recursive-descent or other parser.

## Related tools

- **MassQueryLanguage (mwang87/MassQueryLanguage)** (Reference parser implementation and language grammar specification; used to extract lexical rules, token types, and AST structure for MassQL queries) — https://github.com/mwang87/MassQueryLanguage
- **massql (Python package)** (Official Python API for MassQL query execution; tokenizer is internal component accessed via msql_engine.process_query()) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY scaninfo(MS2DATA) WHERE MS1MZ=100', 'test.mzML')
```

## Evaluation signals

- Token stream contains no unrecognized characters; all input is consumed.
- Token sequence respects grammar: keywords are recognized, operators are classified correctly, literals match expected patterns (e.g., numeric vs. string).
- Tokenized output can be successfully parsed by the downstream parser into a valid AST without lexical errors.
- Ambiguous sequences (e.g., 'MS1MZ' vs. keywords) are resolved consistently with the grammar specification.
- Position metadata (line, column) in tokens is accurate and useful for error reporting.

## Limitations

- Tokenizer must be aligned with the exact grammar version in use; grammar changes (e.g., new operators or keywords in MassQL updates) require tokenizer updates.
- No changelog found for MassQL repository, so backward compatibility and lexical rule stability are not formally documented—monitor repository commits for breaking changes.
- Tokenizer design is tightly coupled to the domain; a lexer built for MassQL syntax will not generalize to other query languages without significant modification.

## Evidence

- [other] Grammar extraction and tokenization step: "Implement a tokenizer (lexer) that breaks MassQL query strings into meaningful tokens (keywords, identifiers, operators, literals)."
- [readme] MassQL query syntax and domains: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion."
- [other] Reference implementation availability: "Clone or load the MassQueryLanguage repository from github.com/mwang87/MassQueryLanguage to access the reference parser implementation."
- [other] AST target and validation: "Implement a parser (recursive descent or similar) that consumes tokens and builds a structured AST representation."
- [other] Query component preservation: "Serialize the AST to JSON format, preserving query components (SELECT clauses, WHERE conditions, mass tolerance, scan type constraints, etc.)."
