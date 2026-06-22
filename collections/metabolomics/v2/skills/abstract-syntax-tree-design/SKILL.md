---
name: abstract-syntax-tree-design
description: Use when when you have a domain-specific query language (such as MassQL for mass spectrometry) and need to convert query strings into structured representations that preserve domain constraints (e.g., mass tolerance, scan type, intensity thresholds).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0081
  tools:
  - SQL
  - MassQL
  - massql Python API
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

# abstract-syntax-tree-design

## Summary

Design and implement an abstract syntax tree (AST) representation for a domain-specific language, capturing hierarchical query structure with typed nodes that preserve semantics and constraints specific to the problem domain. This skill is essential when converting textual queries into structured, machine-interpretable forms that enable validation, optimization, and execution.

## When to use

When you have a domain-specific query language (such as MassQL for mass spectrometry) and need to convert query strings into structured representations that preserve domain constraints (e.g., mass tolerance, scan type, intensity thresholds). Apply this skill when the query language has formal grammar rules and you need to enable downstream operations like validation, serialization, or query execution.

## When NOT to use

- When the query language lacks a formal grammar specification or the syntax is highly ambiguous and context-dependent
- When your use case only requires regex-based pattern matching or simple string parsing without semantic structure preservation
- When the query input is already in a structured format (XML, JSON, Prolog) requiring only deserialization rather than parsing

## Inputs

- Query string (text) in domain-specific language syntax
- Formal grammar specification (lexical and production rules)
- Reference query examples for validation

## Outputs

- Abstract syntax tree (AST) with typed nodes
- JSON serialization of AST preserving query structure and domain constraints
- Validation report indicating structural correctness

## How to apply

First, extract or design the formal grammar specification for your domain-specific language, identifying lexical rules (token types: keywords, identifiers, operators, literals) and production rules (clause structure). Implement a tokenizer to break query strings into meaningful tokens, then implement a parser (recursive descent or equivalent) that consumes tokens according to the grammar and builds an AST by creating typed nodes for each syntactic element (SELECT clauses, WHERE conditions, constraints). For MassQL specifically, preserve mass spectrometry-specific nodes such as MS1MZ, MS2PREC, TOLERANCEMZ, and INTENSITYPERCENT as first-class AST elements. Serialize the resulting AST to JSON format, preserving all query components and their hierarchical relationships. Validate the AST output against reference query examples from the language specification to ensure structural correctness and that domain constraints are properly captured.

## Related tools

- **MassQL** (Reference domain-specific language implementation for mass spectrometry query parsing; provides grammar rules, reference parser, and validation examples) — https://github.com/mwang87/MassQueryLanguage
- **massql Python API** (Reference implementation of MassQL parser and AST construction; used to analyze grammar rules and AST structure design patterns) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY MS2DATA WHERE MS1MZ=100', 'input_file.mzML')
```

## Evaluation signals

- AST nodes correspond 1:1 to grammar production rules; validate by checking node types against grammar specification
- JSON serialization round-trips without loss: deserialize JSON AST, regenerate query, re-parse, and verify output AST matches original
- All domain-specific constraints are captured as AST node attributes or child nodes (e.g., TOLERANCEMZ, INTENSITYPERCENT, scan type); verify by comparing parsed constraints against reference query examples
- Parser correctly handles edge cases: nested clauses, optional parameters, multiple AND/OR conditions; test against reference query suite from language documentation
- Structural validation passes: all leaf nodes are tokens, all internal nodes have expected child counts per grammar rules

## Limitations

- AST design is tightly coupled to grammar specification; grammar changes require AST schema redesign and parser modification
- Serialization to JSON assumes all AST node attributes are JSON-representable; non-primitive types (e.g., custom objects, circular references) require custom encoding
- Parser performance scales linearly with query string length; complex nested queries may incur overhead; no mention of optimization for large-scale query batches
- The skill assumes formal grammar is already defined; design of the grammar itself (expressing mass spectrometry semantics) is a separate, non-trivial task

## Evidence

- [other] Design or extract the formal grammar specification (lexical rules, production rules) for MassQL query syntax.: "Design or extract the formal grammar specification (lexical rules, production rules) for MassQL query syntax."
- [other] Implement a tokenizer (lexer) that breaks MassQL query strings into meaningful tokens (keywords, identifiers, operators, literals).: "Implement a tokenizer (lexer) that breaks MassQL query strings into meaningful tokens (keywords, identifiers, operators, literals)."
- [other] Implement a parser (recursive descent or similar) that consumes tokens and builds a structured AST representation.: "Implement a parser (recursive descent or similar) that consumes tokens and builds a structured AST representation."
- [other] Serialize the AST to JSON format, preserving query components (SELECT clauses, WHERE conditions, mass tolerance, scan type constraints, etc.).: "Serialize the AST to JSON format, preserving query components (SELECT clauses, WHERE conditions, mass tolerance, scan type constraints, etc.)."
- [intro] MassQL is designed as a domain-specific language that expresses mass spectrometry queries by baking mass spectrometry assumptions into the language syntax and semantics, inspired by SQL but specialized for mass spectrometry use cases.: "domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion. It is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry"
- [readme] Language Grammar and Reference Implementation Python API are core components of the MassQL repository.: "This contains several parts: 1. Language Grammar 2. Reference Implementation Python API"
