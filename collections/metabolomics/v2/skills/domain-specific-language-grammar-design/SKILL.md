---
name: domain-specific-language-grammar-design
description: Use when when you need to enable non-programmers or domain experts to formulate complex, unambiguous queries over specialized data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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

# domain-specific-language-grammar-design

## Summary

Design and implement a domain-specific language (DSL) grammar that encodes field-centric assumptions and constraints into an extended syntax, balancing expressiveness, precision, scalability, and human readability. This skill involves defining formal grammar rules, implementing a lexer and parser to convert query strings into structured representations, and validating outputs against design principles.

## When to use

When you need to enable non-programmers or domain experts to formulate complex, unambiguous queries over specialized data (e.g., mass spectrometry repositories, genomic databases) by providing a syntax that bakes in domain assumptions rather than requiring them to write generic SQL or API calls. Use this when existing query languages are too abstract or verbose for your domain's most common patterns.

## When NOT to use

- Input data is already structured as a feature matrix or parsed table — use a DSL parser only if the source is raw query strings or natural-language specifications.
- Your domain has no consensus on core operators or patterns — DSL design requires deep domain engagement; if the community's query patterns are still in flux, defer grammar design until patterns stabilize.
- You need to query only a single, small dataset with ad-hoc filters — the overhead of DSL grammar design and parser implementation is only justified by repeated, large-scale, or multi-user query needs.

## Inputs

- MassQL query string (text)
- Grammar specification (formal or semi-formal)
- Domain-specific operator definitions (list of m/z ranges, intensity thresholds, fragmentation patterns, etc.)

## Outputs

- Abstract Syntax Tree (AST) in JSON or canonical text format
- Parsing success/failure report with diagnostic error messages
- Validated query specification ready for execution

## How to apply

First, enumerate the core design principles your DSL must satisfy (e.g., Expressiveness for capturing domain patterns, Precision for unambiguous specification, Scalability from single-record to repository-scale queries, and Natural readability for domain practitioners). Define formal grammar as extended SQL syntax incorporating domain-specific operators and constructs (e.g., m/z ranges, intensity thresholds, fragmentation patterns for mass spectrometry). Implement a lexer to tokenize input strings, identifying keywords, domain operators, and numeric literals. Build a parser (recursive descent or LALR) to construct an Abstract Syntax Tree (AST) from tokens, enforcing syntactic and semantic constraints. Validate the AST against your design criteria: confirm complex patterns are expressible and unambiguous, that queries scale across your data range, and that syntax remains human-readable. Serialize the validated AST to a canonical format (JSON or text) and return parsing diagnostics with specific error messages for failure cases.

## Related tools

- **MassQL** (Reference implementation of mass-spectrometry-centric DSL; provides lexer, parser, and query execution engine for the Mass Spec Query Language) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY MS2DATA WHERE MS1MZ=100', 'input.mzML')
```

## Evaluation signals

- AST structure is valid JSON/canonical text and parses without syntax errors for well-formed queries from your design test suite.
- All four design principles are demonstrable: complex MS patterns (e.g., isotope ratios, fragmentation cascades) can be expressed in a single query; two users writing the same logical query produce identical ASTs (Precision); queries execute on both single spectra and repository-scale data without modification; domain practitioners report that query syntax is readable and matches their mental model of MS filtering (Natural).
- Error messages pinpoint the lexical or syntactic failure location and suggest correction (e.g., 'Unknown operator BADOP at position 42; did you mean INTENSITYMATCH?').
- Benchmark parsing latency on a representative query: typical queries should parse to AST in <100 ms even on large repositories.
- Roundtrip test: serialize AST back to query string; re-parse and verify AST equivalence, ensuring no semantic information is lost.

## Limitations

- DSL grammar design requires significant upfront domain expertise and community consensus on operators and semantics; changes to grammar post-launch may break existing queries.
- Parser implementation complexity (recursive descent vs. LALR) trades off development effort against error recovery quality and maintainability.
- No changelog in the MassQL repository indicates potential gaps in documenting breaking changes or deprecated operators between versions.
- Human readability is subjective and domain-specific; syntax that seems natural to expert mass spectrometrists may remain opaque to newcomers without training or extensive documentation.
- Scaling from single spectrum to repository-scale queries may require index structures or query optimization not addressed at the grammar/parser level; grammar alone does not guarantee runtime scalability.

## Evidence

- [intro] Four core design principles for DSL: Expressiveness, Precision, Scalability, Relatively Natural: "Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for; Precision - Exactly prescribe how to find data without ambiguity; Scalable - Easily facilitating"
- [other] Lexer and parser workflow for DSL implementation: "Implement a lexer to tokenize the input MassQL query string, identifying SQL keywords, MS-specific operators, and numeric literals. 3. Implement a parser using recursive descent or LALR parsing to"
- [intro] Domain-specific constructs in MassQL grammar: "it is inspired by SQL, but it attempts to bake in assumptions of mass spectrometry to make querying much more natural for mass spectrometry users"
- [other] AST validation and serialization: "Serialize the AST to JSON or canonical text format and report parsing success/failure with diagnostic error messages"
- [readme] MassQL supports spectrum-scale to repository-scale queries: "The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion"
