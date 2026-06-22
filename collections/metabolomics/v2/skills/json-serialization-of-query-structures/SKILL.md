---
name: json-serialization-of-query-structures
description: Use when you have parsed a MassQL query string into an AST representation and need to store, validate, transmit, or integrate the query structure with other tools or systems.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SQL
  - MassQL Reference Parser
  - massql Python API
  - massql Command Line Tool
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
---

# json-serialization-of-query-structures

## Summary

Convert domain-specific query language abstract syntax trees (ASTs) into JSON format to preserve structured query components (SELECT clauses, WHERE conditions, constraints) in a machine-readable and interoperable form. This enables downstream processing, visualization, validation, and integration of mass spectrometry queries across pipelines.

## When to use

Apply this skill when you have parsed a MassQL query string into an AST representation and need to store, validate, transmit, or integrate the query structure with other tools or systems. Use it whenever you need the query to be independently inspectable, versioned, or transformed by downstream agents without reparsing the original query string.

## When NOT to use

- Query string is already in JSON form or does not require interoperability with other tools.
- Query structure is simple enough that raw AST objects or internal representations suffice for downstream processing.
- Application requires lossy compression or does not need to preserve full query semantics for validation or reconstruction.

## Inputs

- Parsed AST (abstract syntax tree) from MassQL query parser
- Query component metadata (SELECT clause targets, WHERE condition predicates, constraint values)

## Outputs

- JSON-serialized query representation with nested structure
- Query structure document preserving mass spectrometry constraints and operators

## How to apply

After building an AST from tokenized MassQL query syntax, recursively serialize the tree into a JSON object that preserves all query components: SELECT clauses (e.g. scaninfo, MS2DATA), WHERE condition filters (e.g. MS1MZ, TOLERANCEMZ, INTENSITYPERCENT), logical operators (AND, OR), mass tolerance parameters, and scan type constraints. Map each AST node to a JSON object with fields for node type, operator/keyword, operands, and nested conditions. Validate the JSON output against reference query examples from the MassQueryLanguage repository to ensure structural correctness and that all mass spectrometry-specific parameters (mass/m-z values, tolerance thresholds, intensity percentages) are accurately represented. The JSON form should be human-readable and reconstruct the original query semantics without loss of information.

## Related tools

- **MassQL Reference Parser** (Parses MassQL query strings into AST prior to JSON serialization; reference for validating serialized output against canonical query semantics) — https://github.com/mwang87/MassQueryLanguage
- **massql Python API** (Provides process_query() method that consumes queries and can be extended to emit JSON-serialized intermediate representations) — https://github.com/mwang87/MassQueryLanguage
- **massql Command Line Tool** (CLI interface for query execution; can be chained with JSON serialization for pipeline integration) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine; import json; results_df = msql_engine.process_query('QUERY MS2DATA WHERE MS1MZ=100', 'test.mzML'); query_json = json.dumps({'SELECT': 'MS2DATA', 'WHERE': {'MS1MZ': 100}}, indent=2)
```

## Evaluation signals

- JSON output is valid and parseable; no syntax errors or truncation.
- All AST nodes are represented in the JSON structure with no information loss (e.g., all mass tolerance values, scan type constraints, and WHERE operators are present).
- JSON-serialized query can be round-tripped: deserialize to JSON, reconstruct query string, re-parse, and produce equivalent AST to original.
- Mass spectrometry-specific parameters (MS1MZ, TOLERANCEMZ, INTENSITYPERCENT, MS2PREC) are correctly mapped to JSON field names and values matching reference query examples.
- Query structure matches expected schema for SELECT, WHERE, AND/OR operators, and constraint parameters when validated against reference examples from the MassQueryLanguage documentation.

## Limitations

- Serialization only captures query structure; does not include execution results or performance metrics. Downstream tools must re-parse and execute the JSON-serialized query to obtain spectrum results.
- JSON output may grow large for complex queries with deeply nested AND/OR conditions; no built-in compression is specified in the reference implementation.
- Serialization assumes a stable, well-defined grammar; changes to MassQL syntax or addition of new constraint types require schema migration of existing JSON-serialized queries.
- No changelog documented for the MassQL specification; breaking changes to serialization format are not formally tracked.

## Evidence

- [other] The workflow specifies that serialization to JSON is a key step in parsing and representation.: "Serialize the AST to JSON format, preserving query components (SELECT clauses, WHERE conditions, mass tolerance, scan type constraints, etc.)."
- [other] The reference implementation is the canonical source for AST structure and validation.: "Analyze the reference parser to identify the grammar rules, token types, and AST (abstract syntax tree) structure used to represent MassQL queries."
- [intro] MassQL is designed to bake mass spectrometry assumptions into syntax and semantics.: "It is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry"
- [other] Validation against reference examples ensures correctness of the serialization.: "Validate the parser output against reference query examples from the repository to ensure structural correctness."
- [readme] The repository provides a reference implementation with documented grammar and structure.: "This is the repository to define the language and reference implementation. This contains several parts: 1. Language Grammar 2. Reference Implementation Python API"
