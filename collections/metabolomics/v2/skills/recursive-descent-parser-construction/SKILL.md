---
name: recursive-descent-parser-construction
description: Use when you have a formal grammar specification for a domain-specific language (or can extract one from reference implementations) and need to convert user-written query strings into structured, machine-processable representations (ASTs or JSON) that preserve domain-specific semantics—such as mass.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SQL
  - MassQueryLanguage
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# recursive-descent-parser-construction

## Summary

Implement a recursive descent parser that tokenizes and builds an abstract syntax tree (AST) from a domain-specific query language, converting unstructured query strings into structured representations. This skill is essential when designing domain-specific languages (DSLs) like MassQL that must capture complex patterns and constraints while maintaining readability and precision.

## When to use

You have a formal grammar specification for a domain-specific language (or can extract one from reference implementations) and need to convert user-written query strings into structured, machine-processable representations (ASTs or JSON) that preserve domain-specific semantics—such as mass spectrometry tolerances, scan type constraints, or m/z value patterns. Use this skill when the query language must express complex patterns that are natural in the domain but would be verbose or ambiguous in generic SQL or JSON.

## When NOT to use

- The input is already a structured representation (XML, JSON, AST)—parse only unstructured query strings.
- The query language has no formal grammar or reference implementation—grammar definition must precede parser construction.
- You are implementing a general-purpose programming language compiler—recursive descent is suitable for DSLs but may not scale to complex operator precedence or large production rule sets without additional techniques.

## Inputs

- Query string in domain-specific language syntax (e.g., MassQL query as text)
- Formal grammar specification (lexical rules and production rules)
- Reference parser implementation or language documentation

## Outputs

- Abstract syntax tree (AST) as in-memory object
- AST serialized to JSON format preserving query components
- Validation report against reference examples

## How to apply

First, extract or design the formal grammar specification by analyzing a reference parser implementation (e.g., from the MassQueryLanguage GitHub repository), documenting lexical rules (token types: keywords, identifiers, operators, literals) and production rules (clause structures, expressions, constraints). Implement a tokenizer (lexer) that breaks input query strings into meaningful tokens using pattern matching or state machines. Then implement a recursive descent parser that consumes tokens in sequence, building an AST by matching production rules recursively—each grammar rule becomes a parser function that either succeeds (returning a node) or fails (triggering backtracking or error handling). Serialize the resulting AST to JSON, preserving domain-specific query components (SELECT clauses, WHERE conditions, mass tolerance parameters, scan type filters). Finally, validate the parser against a suite of reference query examples from the domain community to ensure structural correctness and semantic fidelity.

## Related tools

- **MassQueryLanguage** (Reference implementation providing grammar rules, token types, and AST structure patterns for recursive descent parser design) — https://github.com/mwang87/MassQueryLanguage
- **massql Python API** (Reference Python implementation demonstrating tokenization and AST construction via msql_engine.process_query()) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
```python
from massql import msql_engine

input_query = "QUERY MS2DATA WHERE MS1MZ=572.828 TOLERANCEMZ=0.1 AND MS2PREC=572.828"
results_df = msql_engine.process_query(input_query, input_filename)
```
```

## Evaluation signals

- Parser successfully tokenizes all reference query examples without errors or exceptions.
- AST structure matches expected grammar production rules (e.g., SELECT clauses, WHERE conditions, parameter specifications are distinct AST nodes).
- JSON serialization preserves all domain-specific query components (mass tolerance values, scan type constraints, m/z patterns) without loss or mutation.
- Parser correctly rejects malformed queries (syntax errors, missing required clauses) and reports meaningful error locations.
- Round-trip validation: re-parsing serialized JSON produces an AST structurally identical to the original.

## Limitations

- Recursive descent parsing can suffer from left recursion without refactoring; the grammar must be left-factored or rewritten to avoid infinite loops.
- No changelog in the MassQueryLanguage repository, so grammar changes or parser updates may not be formally documented; rely on reference implementation and test suite for ground truth.
- Scaling to very large query strings or deeply nested expressions may cause stack overflow if recursion depth is unbounded; monitor recursion depth and consider iterative or memoized approaches for production use.
- Parser design assumes the grammar is unambiguous; ambiguous grammars require conflict resolution (e.g., shift/reduce decisions in LR parsing) beyond the scope of simple recursive descent.

## Evidence

- [other] Grammar extraction and parser implementation workflow: "Analyze the reference parser to identify the grammar rules, token types, and AST (abstract syntax tree) structure used to represent MassQL queries. Design or extract the formal grammar specification"
- [other] Tokenization step: "Implement a tokenizer (lexer) that breaks MassQL query strings into meaningful tokens (keywords, identifiers, operators, literals)."
- [other] Recursive descent parser construction: "Implement a parser (recursive descent or similar) that consumes tokens and builds a structured AST representation."
- [other] AST serialization and validation: "Serialize the AST to JSON format, preserving query components (SELECT clauses, WHERE conditions, mass tolerance, scan type constraints, etc.). Validate the parser output against reference query"
- [readme] Domain-specific language design rationale: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion. It is inspired by SQL, but it attempts to"
