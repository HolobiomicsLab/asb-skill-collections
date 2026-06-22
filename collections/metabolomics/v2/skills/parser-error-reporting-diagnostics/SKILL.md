---
name: parser-error-reporting-diagnostics
description: Use when when implementing or extending a DSL parser (lexer + recursive descent or LALR parser) that accepts user-authored query strings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
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

# Parser Error Reporting and Diagnostics

## Summary

Generate human-readable diagnostic error messages when a domain-specific language (DSL) parser fails to tokenize or parse input, pinpointing syntactic and semantic violations. This skill ensures that users receive actionable feedback rather than opaque parse failures, enabling rapid query iteration and debugging.

## When to use

When implementing or extending a DSL parser (lexer + recursive descent or LALR parser) that accepts user-authored query strings. Apply this skill whenever a query fails to tokenize (lexical error) or construct an Abstract Syntax Tree (semantic/syntactic error), to communicate exactly which token, line, column, or grammar rule caused the failure.

## When NOT to use

- Input is already a validated, serialized Abstract Syntax Tree (AST) or canonical JSON representation — errors should have been caught upstream.
- The goal is to silently recover from parse errors without user notification; diagnostics are meant to inform, not replace error handling.
- The parser is used only internally and never exposed to end users; minimal diagnostic detail may suffice.

## Inputs

- MassQL query string (or other DSL query text)
- Context from query parsing attempt (token stream, partial AST, rule being evaluated)

## Outputs

- Diagnostic error report (human-readable message with line, column, token, expected vs. actual, and suggestion)
- Parse result status (success/failure flag with associated error collection)

## How to apply

Instrument the lexer to report unrecognized tokens with their position (line, column) and context. In the parser, catch syntax errors at each grammar rule boundary and report the expected token(s), actual token received, and the rule being parsed. For semantic violations (e.g., invalid m/z range or unsupported filter construct in MassQL), validate the Abstract Syntax Tree post-parse and attach error messages to the offending node. Format all errors with the original query snippet, position indicator, and a suggestion for correction. Return errors alongside the parse result (success/failure flag) to enable graceful degradation.

## Related tools

- **MassQL** (Domain-specific language parser that uses lexer and recursive descent/LALR parsing; diagnostic error reporting is applied to lexical, syntactic, and semantic failures during query parsing) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine
results_df = msql_engine.process_query(input_query, input_filename)
# On parse failure, diagnostic errors are returned in results_df or raised with line/column/suggestion info
```

## Evaluation signals

- Parser correctly identifies and reports the character position (line, column) of a malformed token or syntax error in the input query string.
- Diagnostic message clearly states the expected grammar rule(s) or token type(s) and what was actually received.
- Error message is human-readable and actionable for a mass spectrometry domain user (e.g., 'Expected tolerance value (numeric) after TOLERANCEMZ, got KEYWORD "WHERE"').
- Validation of AST against design constraints (expressiveness, precision, scalability) detects and reports semantic violations (e.g., unsupported m/z range or ambiguous intensity match specification).
- All parse failures are tagged with success/failure status and include collected error messages; no exceptions are silently swallowed.

## Limitations

- Lexer-level diagnostics depend on the granularity of tokenization; very long or nested query structures may produce confusing error positions if the grammar is ambiguous.
- Semantic validation against MassQL design principles (expressiveness, precision, scalability) requires domain knowledge; generic parser frameworks may not catch mass-spectrometry-specific violations.
- Error recovery (attempting to continue parsing after an error) is not mentioned in the source material; diagnostics as described are failure-terminal, not fault-tolerant.
- The README does not detail error message formatting or localization; implementation may vary across Python API, CLI, and web API endpoints.

## Evidence

- [other] Implement a lexer to tokenize the input MassQL query string, identifying SQL keywords, MS-specific operators, and numeric literals.: "Implement a lexer to tokenize the input MassQL query string, identifying SQL keywords, MS-specific operators, and numeric literals."
- [other] Implement a parser using recursive descent or LALR parsing to build an Abstract Syntax Tree (AST) from the token stream, enforcing syntactic and semantic constraints.: "Implement a parser using recursive descent or LALR parsing to build an Abstract Syntax Tree (AST) from the token stream, enforcing syntactic and semantic constraints."
- [other] Serialize the AST to JSON or canonical text format and report parsing success/failure with diagnostic error messages.: "Serialize the AST to JSON or canonical text format and report parsing success/failure with diagnostic error messages."
- [readme] The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion.: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion."
- [readme] MassQL should be relatively easy to read and write and even use to communicate ideas about mass spectrometry, you know like a language.: "MassQL should be relatively easy to read and write and even use to communicate ideas about mass spectrometry, you know like a language."
