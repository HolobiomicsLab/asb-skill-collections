---
name: lexical-tokenization-and-grammar-design
description: Use when you need to enable users to express complex domain-specific queries in a natural, succinct syntax—particularly when SQL patterns are familiar but must be augmented with domain assumptions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SQL
  - ANTLR
  - PLY (Python Lex-Yacc)
  - MassQL Reference Implementation
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
---

# Lexical Tokenization and Grammar Design

## Summary

Design and implement a domain-specific language (DSL) grammar and tokenizer to parse structured query strings into an intermediate representation (AST or query object). This skill is essential when building query interfaces for specialized scientific domains where SQL-inspired syntax must be adapted with domain-specific assumptions and semantics.

## When to use

Apply this skill when you need to enable users to express complex domain-specific queries in a natural, succinct syntax—particularly when SQL patterns are familiar but must be augmented with domain assumptions (e.g., mass spectrometry-specific filters like mass-to-charge ratio, retention time, intensity thresholds). Use it as a prerequisite step before query execution or validation.

## When NOT to use

- Input is already a parsed AST or structured query object—skip directly to query execution or validation.
- Domain does not benefit from natural-language-like syntax (e.g., already using programmatic APIs or low-level binary formats).
- Query complexity is minimal and does not justify DSL overhead; use parameter-based filtering instead.

## Inputs

- DSL grammar specification (textual or formal definition)
- Query string in DSL syntax (e.g., 'QUERY MS2DATA WHERE MS1MZ=100')
- Lexicon and token type definitions

## Outputs

- Token stream (sequence of recognized lexical units)
- Abstract syntax tree (AST) or query object representation
- Canonical intermediate format (JSON, Python object, or equivalent)

## How to apply

First, define the DSL grammar and lexical tokens based on SQL-inspired syntax extended with domain-specific assumptions (e.g., for mass spectrometry: MS1MZ, MS2DATA, TOLERANCEMZ, INTENSITYPERCENT filters). Build a tokenizer that lexically analyzes input query strings into a recognized token sequence, handling operators, keywords, and domain-specific syntax. Construct a parser (recursive descent, ANTLR, PLY, or similar) that consumes tokens and produces a structured abstract syntax tree (AST) or query object representation. Validate the parse tree against DSL design principles: expressiveness (captures complex domain patterns), precision (unambiguous specification), scalability (single item to repository queries), and readability (natural domain semantics). Return the canonical parse tree (JSON, pickled Python object, or similar) for downstream execution or analysis.

## Related tools

- **ANTLR** (Parser generator for lexing and parsing DSL grammars into ASTs)
- **PLY (Python Lex-Yacc)** (Python-based lexer and parser generator for tokenization and grammar parsing)
- **MassQL Reference Implementation** (Concrete example of DSL tokenization, grammar, and parser for mass spectrometry queries) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY MS2DATA WHERE MS1MZ=100', 'input.mzML')
```

## Evaluation signals

- Token stream contains no unrecognized tokens and covers the entire input query without gaps.
- AST structure conforms to the DSL grammar specification and contains all relevant domain-specific clauses (e.g., MS1MZ, MS2DATA, WHERE filters for MassQL).
- Parse tree is deterministic and reproducible for identical input queries.
- Canonical output can be serialized and deserialized without loss of information.
- Query semantics preserve domain-specific precision: filters (e.g., tolerance thresholds, intensity percentages) and their parameters are correctly parsed and accessible in the output structure.

## Limitations

- DSL grammar design and tokenizer implementation require upfront domain expertise and careful specification to avoid ambiguity.
- Parser generation tools (ANTLR, PLY) introduce toolchain dependencies and potential version compatibility issues.
- Complex or recursive domain patterns may require iterative grammar refinement; initial designs often need revision after user feedback.
- Performance scalability depends on tokenizer and parser efficiency; very large query strings or deeply nested expressions may incur latency.
- No validation of semantic correctness at parse time; malformed domain-specific values (e.g., invalid mass ranges, nonsensical intensity thresholds) pass through tokenization/parsing and require downstream validation.

## Evidence

- [other] Define grammar and lexical tokens.: "Define the MassQL grammar and lexical tokens based on SQL-inspired syntax with mass spectrometry-specific assumptions (e.g., mass, retention time, intensity filters)."
- [other] Tokenizer lexically analyzes input.: "Build a tokenizer that lexically analyzes input MassQL query strings into a sequence of recognized tokens."
- [other] Parser produces AST or query object.: "Construct a parser (e.g., using recursive descent or parser generator such as ANTLR or PLY) that consumes tokens and produces a structured abstract syntax tree (AST) or query object representation."
- [other] DSL design principles: expressiveness, scalability, readability.: "Validate the parse tree against MassQL design principles: expressiveness (captures complex MS patterns), scalability (handles single spectrum to repository queries), and readability (natural MS"
- [readme] MassQL is SQL-inspired with mass spectrometry assumptions.: "It is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry to make querying much more natural for mass spectrometry users."
- [readme] MassQL design principles include precision.: "Precision - Exactly prescribe how to find data without ambiguity"
