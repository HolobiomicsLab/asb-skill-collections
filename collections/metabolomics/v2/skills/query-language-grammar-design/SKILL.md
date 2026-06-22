---
name: query-language-grammar-design
description: Use when when you need to enable non-programmer mass spectrometry users to express complex spectral search patterns (e.g., isotope patterns, precursor mass constraints, scan-type filters) without writing procedural code.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0361
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SQL
  - MassQL reference implementation
  - massql command-line utility
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

# query-language-grammar-design

## Summary

Design and implement a domain-specific query language grammar that translates user-written queries into structured representations (AST/JSON) suitable for execution against specialized data repositories. This skill bridges high-level query expression with mass spectrometry-specific semantics, enabling users to express complex analytical patterns naturally.

## When to use

When you need to enable non-programmer mass spectrometry users to express complex spectral search patterns (e.g., isotope patterns, precursor mass constraints, scan-type filters) without writing procedural code. Specifically, apply this skill when a community has recurring analytical queries that benefit from baking domain assumptions (mass tolerance, intensity thresholds, scan metadata) directly into query syntax rather than requiring parameter files or API calls.

## When NOT to use

- When queries are already structured in a machine-readable format (e.g., JSON, YAML). Use direct deserialization instead.
- When the analytical task does not require domain-specific assumptions baked into syntax (e.g., generic SQL queries over tabular data).
- When users are comfortable writing procedural code (Python, R) and do not require a natural-language query interface.

## Inputs

- MassQL query string (plain text)
- Formal grammar specification (EBNF or equivalent)
- Reference query examples (text file or repository)
- Mass spectrometry data file (mzML, mzXML, or equivalent) for validation

## Outputs

- Abstract Syntax Tree (AST) in JSON format
- Parsed query representation with clauses (SELECT, WHERE, constraints)
- Validation report (pass/fail against reference queries)
- Query execution plan or intermediate representation

## How to apply

First, extract or design the formal grammar specification (lexical tokens, production rules) from domain literature or reference implementations, identifying mass spectrometry-specific primitives (e.g., MS1MZ, MS2PREC, TOLERANCEMZ, INTENSITYPERCENT). Implement a tokenizer (lexer) to break query strings into keywords, identifiers, operators, and literals, preserving domain semantics. Build a recursive-descent parser that consumes tokens and constructs an Abstract Syntax Tree (AST) capturing SELECT clauses, WHERE conditions, mass tolerance, and scan type constraints. Serialize the AST to JSON, ensuring each clause (e.g., MS1MZ=X:TOLERANCEMZ=0.1) is unambiguously represented. Validate parser output against reference query examples from community repositories or published case studies to confirm structural correctness and semantic fidelity before deployment.

## Related tools

- **MassQL reference implementation** (Provides grammar rules, token types, and AST structure used as the canonical parser design; source for validating custom implementations.) — https://github.com/mwang87/MassQueryLanguage
- **SQL** (Inspires query syntax patterns and logical operator semantics for the domain-specific language.)
- **massql command-line utility** (Executes parsed queries against mzML and related mass spectrometry data files; validates parser output in practice.) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY scaninfo(MS2DATA) WHERE MS1MZ=100', 'input.mzML')
```

## Evaluation signals

- Parser successfully tokenizes all keywords, identifiers, operators, and literals without lexical errors.
- AST structure faithfully represents all SELECT clauses, WHERE conditions, mass tolerance (TOLERANCEMZ), intensity thresholds (INTENSITYPERCENT), and scan type constraints (MS1DATA, MS2DATA) present in input query.
- Serialized JSON AST can be round-tripped (parse → JSON → re-parse) without loss of semantic information.
- Parsed queries execute successfully via the MassQL engine (or equivalent) on reference mzML files and produce expected subset of spectra.
- Output matches reference parser output (from mwang87/MassQueryLanguage) on identical query strings, within schema equivalence.

## Limitations

- Grammar design must incorporate mass spectrometry domain knowledge (isotope patterns, precursor mass relationships, scan metadata) to avoid ambiguity; naive SQL-like syntax will not capture required expressiveness.
- Parser complexity scales with grammar size; recursive descent becomes difficult to maintain and debug beyond ~50 production rules without tool-assisted code generation.
- No changelog or versioning guidance provided in MassQL repository; breaking changes to grammar may require parser redesign and invalidate stored queries.
- Validation against reference queries is only as strong as the reference set; edge cases and malformed queries not in the repository may pass parser but fail at execution time.

## Evidence

- [other] How does the MassQL parser convert query strings into structured representations that capture mass spectrometry-specific patterns and constraints?: "research_question from task_id=task_001"
- [other] MassQL is designed as a domain-specific language that expresses mass spectrometry queries by baking mass spectrometry assumptions into the language syntax and semantics: "MassQL is designed as a domain-specific language that expresses mass spectrometry queries by baking mass spectrometry assumptions into the language syntax and semantics, inspired by SQL but"
- [other] Analyze the reference parser to identify the grammar rules, token types, and AST (abstract syntax tree) structure used to represent MassQL queries.: "Analyze the reference parser to identify the grammar rules, token types, and AST (abstract syntax tree) structure used to represent MassQL queries."
- [other] Implement a tokenizer (lexer) that breaks MassQL query strings into meaningful tokens (keywords, identifiers, operators, literals).: "Implement a tokenizer (lexer) that breaks MassQL query strings into meaningful tokens (keywords, identifiers, operators, literals)."
- [other] Serialize the AST to JSON format, preserving query components (SELECT clauses, WHERE conditions, mass tolerance, scan type constraints, etc.).: "Serialize the AST to JSON format, preserving query components (SELECT clauses, WHERE conditions, mass tolerance, scan type constraints, etc.)."
- [readme] The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion. It is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion. It is inspired by SQL, but it attempts to"
- [readme] Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for: "Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for"
- [other] Validate the parser output against reference query examples from the repository to ensure structural correctness.: "Validate the parser output against reference query examples from the repository to ensure structural correctness."
