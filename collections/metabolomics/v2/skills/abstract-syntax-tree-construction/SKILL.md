---
name: abstract-syntax-tree-construction
description: Use when you have a tokenized sequence of domain-specific language tokens
  and need to construct a hierarchical, unambiguous representation that can be validated
  against language design principles (expressiveness, precision, scalability, readability)
  and passed to downstream execution engines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - SQL
  - ANTLR
  - PLY (Python Lex-Yacc)
  - MassQL reference implementation
  techniques:
  - mass-spectrometry
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# abstract-syntax-tree-construction

## Summary

Parse domain-specific query language strings into structured abstract syntax tree (AST) representations that capture the hierarchical syntax and semantics of the query. This skill is essential when implementing a domain-specific language (DSL) interpreter that needs to transform human-readable query expressions into machine-processable intermediate representations for validation and execution.

## When to use

Apply this skill when you have a tokenized sequence of domain-specific language tokens and need to construct a hierarchical, unambiguous representation that can be validated against language design principles (expressiveness, precision, scalability, readability) and passed to downstream execution engines. Specifically, use this when building a parser for SQL-inspired query syntax extended with domain-specific assumptions (e.g., mass spectrometry-specific filters like mass-to-charge ratio, retention time, intensity thresholds).

## When NOT to use

- Input query is already in a pre-parsed, canonical intermediate format (JSON, protobuf) — proceed directly to validation or execution.
- Query syntax is unambiguous, fully deterministic, and requires no hierarchical decomposition — a simple state machine or regex-based matcher may suffice.
- The domain-specific language has no formal grammar definition or the grammar is under active revision — defer AST construction until the grammar is stabilized.

## Inputs

- tokenized query string (sequence of lexical tokens from domain-specific query language)
- formal grammar definition (BNF or EBNF describing syntax and operator precedence)
- mass spectrometry query expressions (MS1MZ, MS2DATA, retention time, intensity filters, tolerance parameters)

## Outputs

- abstract syntax tree (AST) or query object representation
- canonical serialization (JSON or Python pickle) of the parse tree
- structured query object ready for execution or analysis

## How to apply

Begin by defining a formal grammar capturing the domain-specific language syntax and mass spectrometry-specific operators (e.g., MS1MZ, MS2DATA, tolerance parameters, intensity matching clauses). Construct a tokenizer that lexically analyzes input query strings into recognized tokens (keywords, literals, operators). Build a recursive descent parser or use a parser generator (ANTLR, PLY) that consumes the token sequence and produces a structured AST or query object. At each parse step, validate that clauses respect domain constraints (e.g., retention time and mass-to-charge filters are semantically coherent). Return the AST in a canonical, serializable format (JSON or pickled Python object) suitable for downstream query validation and execution across single spectra or entire data repositories.

## Related tools

- **ANTLR** (Parser generator for constructing recursive descent parsers from formal grammars; generates lexer and parser from DSL grammar specification)
- **PLY (Python Lex-Yacc)** (Python-based parser generator for tokenization and AST construction from domain-specific query syntax)
- **MassQL reference implementation** (Reference Python API demonstrating tokenization, parsing, and AST construction for SQL-inspired mass spectrometry queries; includes msql_engine.process_query() for query execution) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY scaninfo(MS2DATA) WHERE MS1MZ=100', 'input_file.mzML')
```

## Evaluation signals

- AST structure reflects the syntactic hierarchy and operator precedence of the query language; nested clauses are correctly subordinated (e.g., WHERE predicates are children of QUERY nodes).
- All terminals in the parse tree are valid tokens from the domain; no spurious or unrecognized tokens remain.
- Roundtrip property: serializing the AST back to query syntax and re-parsing should produce an isomorphic tree.
- Query validation passes: the AST respects domain constraints (e.g., mass-to-charge filters have valid numeric ranges, tolerance parameters are positive, intensity match clauses are semantically coherent).
- Downstream execution engines (query engines) can traverse the AST without ambiguity to generate results; no missing or malformed subtrees.

## Limitations

- Parser construction requires a stable, complete formal grammar; incomplete or ambiguous grammar specifications lead to parse conflicts and incorrect AST structures.
- Performance degrades for deeply nested queries (e.g., complex boolean expressions with many AND/OR clauses) or very long token streams; recursive descent parsers may hit stack limits.
- Error recovery and diagnostic messaging depend on parser implementation; generic parser generators may produce unhelpful error messages for domain experts unfamiliar with parsing concepts.
- Domain-specific assumptions (e.g., mass spectrometry filter semantics) must be encoded in the grammar or as post-parse validation; the parser alone cannot enforce domain correctness without explicit constraints.

## Evidence

- [other] Construct a parser (e.g., using recursive descent or parser generator such as ANTLR or PLY) that consumes tokens and produces a structured abstract syntax tree (AST) or query object representation.: "Construct a parser (e.g., using recursive descent or parser generator such as ANTLR or PLY) that consumes tokens and produces a structured abstract syntax tree (AST) or query object representation."
- [other] Validate the parse tree against MassQL design principles: expressiveness (captures complex MS patterns), scalability (handles single spectrum to repository queries), and readability (natural MS semantics).: "Validate the parse tree against MassQL design principles: expressiveness (captures complex MS patterns), scalability (handles single spectrum to repository queries), and readability (natural MS"
- [other] Return the parse tree in a canonical format (e.g., JSON or pickled Python object) for downstream query execution or analysis.: "Return the parse tree in a canonical format (e.g., JSON or pickled Python object) for downstream query execution or analysis."
- [readme] MassQL is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry to make querying much more natural for mass spectrometry users.: "MassQL is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry to make querying much more natural for mass spectrometry users."
- [readme] Language Grammar, Reference Implementation Python API, Command line Utility to execute: "Language Grammar, Reference Implementation Python API, Command line Utility to execute"
