---
name: domain-specific-language-parsing
description: 'Use when when you have SQL-inspired query strings that encode domain-specific assumptions and need to validate, transform, or execute them against data repositories. Specifically: input is human-readable DSL text containing mass spectrometry-specific clauses (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SQL
  - MassQL reference implementation (Python API)
  - massql command-line utility
  - ANTLR / PLY parser generators
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# domain-specific-language-parsing

## Summary

Parse domain-specific query languages (DSLs) inspired by SQL into structured representations (AST or query objects) for downstream execution. This skill is essential when a scientific community needs a succinct, natural way to express domain-specific patterns (e.g., mass spectrometry search criteria) without writing imperative code.

## When to use

When you have SQL-inspired query strings that encode domain-specific assumptions and need to validate, transform, or execute them against data repositories. Specifically: input is human-readable DSL text containing mass spectrometry-specific clauses (e.g., 'MS1MZ', 'TOLERANCE', 'INTENSITY') and you need to extract structured criteria for filtering spectra or scan data.

## When NOT to use

- Input is already a structured query object or intermediate representation (AST/JSON); skip parsing and move directly to execution.
- Domain patterns are simple enough to express in existing general-purpose query languages (SQL, MongoDB queries); DSL parsing adds unnecessary complexity.
- Query strings do not conform to the documented domain grammar; parsing will fail or produce misleading results.

## Inputs

- query string (text) conforming to domain-specific language syntax
- domain grammar specification (tokens, operators, clauses)
- mass spectrometry data file (mzML format, optional for validation)

## Outputs

- abstract syntax tree (AST) or query object representation
- canonical intermediate representation (JSON or Python object)
- parse validation report (success/failure with error locations)

## How to apply

Define a lexical grammar that recognizes domain-specific tokens (e.g., MS1MZ, MS2DATA, TOLERANCE, INTENSITYPERCENT for mass spectrometry). Build a tokenizer to convert input query strings into a sequence of recognized tokens. Construct a parser (using recursive descent, ANTLR, or PLY) that consumes tokens and produces an abstract syntax tree (AST) or query object. Validate the parse tree against design principles: expressiveness (captures complex patterns the domain community wants to search for), precision (unambiguous filter semantics), scalability (handles single objects to entire repositories), and readability (natural domain semantics). Return the canonical parse tree (JSON or pickled Python object) for downstream query execution.

## Related tools

- **MassQL reference implementation (Python API)** (Execute parsed MassQL queries against mzML or other mass spectrometry data files; primary use via msql_engine.process_query()) — https://github.com/mwang87/MassQueryLanguage
- **massql command-line utility** (Parse and execute MassQL query strings from shell; e.g., 'massql test.mzML "QUERY scaninfo(MS2DATA)" --output_file results.tsv') — https://github.com/mwang87/MassQueryLanguage
- **ANTLR / PLY parser generators** (Optional tools for constructing tokenizers and recursive-descent or LALR parsers from formal grammars; not required if hand-coded)

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY scaninfo(MS2DATA) WHERE MS1MZ=100', 'test.mzML')
```

## Evaluation signals

- Parse succeeds without error on all valid queries conforming to the documented grammar; parse fails with clear error location on invalid syntax.
- AST structure preserves all clauses and filters; no loss of information from input query to output representation.
- Round-trip test: serialize parsed AST back to query string and re-parse; result is structurally identical or logically equivalent.
- Query object supports downstream execution: filter predicates (e.g., MS1MZ=100, TOLERANCE=0.1) are accurately reconstructed and applied to spectrum data.
- Performance: tokenization + parsing completes in <100 ms for typical query strings (<500 chars); scales to repository queries without excessive memory or latency.

## Limitations

- Grammar must be explicitly defined for the target domain; parser is domain-specific and not portable without grammar redefinition.
- Ambiguous grammars or operator precedence conflicts may require iterative refinement; lookahead or precedence declarations may be necessary.
- No changelog available in the repository at the time of review, so backward compatibility and deprecation practices are unclear.
- Error recovery in parser is minimal; a single syntax error may cause the entire query to fail rather than producing partial results.
- Mass spectrometry-specific assumptions baked into the DSL (e.g., retention time, intensity intensity percent ranges) may not generalize to other instrumental modalities without DSL extension.

## Evidence

- [intro] SQL-inspired syntax with mass spectrometry assumptions for domain-specific language design: "It is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry"
- [other] Structured output from parsing for downstream execution: "Return the parse tree in a canonical format (e.g., JSON or pickled Python object) for downstream query execution or analysis."
- [readme] Core design principles: expressiveness, precision, scalability, and readability: "1. Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for
1. Precision - Exactly prescribe how to find data without ambiguity
2. Scalable - Easily"
- [other] Tokenizer and parser construction workflow: "Build a tokenizer that lexically analyzes input MassQL query strings into a sequence of recognized tokens. 3. Construct a parser (e.g., using recursive descent or parser generator such as ANTLR or"
- [readme] Domain-specific language motivation and applicability: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion."
