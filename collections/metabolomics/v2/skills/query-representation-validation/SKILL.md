---
name: query-representation-validation
description: Use when after parsing a MassQL query string into an abstract syntax
  tree or intermediate representation, before executing it against mass spectrometry
  data files (mzML, mzXML, etc.). Validation is essential when the query contains
  complex MS-specific patterns (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SQL
  - MassQL Python API
  - MassQL Command Line Utility
  - MassQL Web API (/parse endpoint)
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

# query-representation-validation

## Summary

Validate that a parsed mass spectrometry query has been correctly transformed into a structured representation (AST or canonical object) that faithfully captures the user's intent while conforming to MassQL design principles. This ensures the parse tree is both semantically sound and executable against MS data repositories.

## When to use

After parsing a MassQL query string into an abstract syntax tree or intermediate representation, before executing it against mass spectrometry data files (mzML, mzXML, etc.). Validation is essential when the query contains complex MS-specific patterns (e.g., isotope filters, intensity ratios, retention time windows, mass tolerance constraints) that must be unambiguously represented for scalable queries across single spectra or entire repositories.

## When NOT to use

- The query string has not yet been parsed into a structured representation—use parsing/tokenization first.
- The input is raw MS data (mzML, mzXML files) rather than a query object—use data loading and query execution instead.
- Validation is being applied without reference to the MassQL grammar or design principles—validation requires the formal specification.

## Inputs

- MassQL query string (text)
- Abstract syntax tree (AST) or intermediate query object representation
- MassQL grammar specification

## Outputs

- Validated query representation (JSON or Python object)
- Validation report or error log (identifying missing fields, ambiguities, or constraint violations)
- Canonical parse tree suitable for downstream execution

## How to apply

Validate the parse tree against three orthogonal MassQL design criteria: (1) Expressiveness—confirm that the parsed representation captures all specified mass spectrometry patterns (e.g., MS1MZ filters with tolerance, MS2DATA references, intensity match ratios) without loss or ambiguity; (2) Precision—verify that each constraint (mass tolerance in ppm, intensity percentages, retention time bounds) is explicitly represented with no ambiguity in how they should be applied; (3) Scalability—ensure the canonical representation (JSON or Python object) is independent of corpus size and can be applied uniformly to a single spectrum or a repository query. Return the validated parse tree in a standardized format (e.g., JSON with typed fields for mass, retention time, intensity) and confirm all user-specified clauses are present and correctly ordered in the AST.

## Related tools

- **MassQL Python API** (Reference implementation for parsing and validating MassQL queries; provides msql_engine.process_query() to execute and validate queries) — https://github.com/mwang87/MassQueryLanguage
- **MassQL Command Line Utility** (CLI interface for executing and implicitly validating MassQL queries against mzML/mzXML files) — https://github.com/mwang87/MassQueryLanguage
- **MassQL Web API (/parse endpoint)** (Parses MassQL query string into intermediate JSON representation for validation and visualization) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
from massql import msql_engine; results_df = msql_engine.process_query('QUERY MS2DATA WHERE MS1MZ=100 WITH TOLERANCEMZ=0.1', 'input.mzML')
```

## Evaluation signals

- All MS-specific clauses (MS1MZ, MS2DATA, TOLERANCEMZ, INTENSITYPERCENT, INTENSITYMATCH, INTENSITYMATCHREFERENCE, MS2PREC, etc.) present in the input query are represented in the output parse tree with no omissions.
- Numeric constraints (mass tolerance in ppm or Da, intensity thresholds as percentages, retention time windows) are parsed with correct data types and value ranges (e.g., TOLERANCEMZ ≥ 0).
- Logical operators (AND, OR) and clause ordering are preserved in the canonical representation, ensuring query semantics are not altered.
- The validated query can be successfully serialized to JSON or Python pickle format without loss of information.
- Execution of the validated query against a test mzML file produces non-empty results when the query semantically matches the data (e.g., a query for MS1MZ=100 with TOLERANCEMZ=0.1 matches peaks within [99.9, 100.1] m/z).

## Limitations

- Validation does not guarantee that the query will return results—it only ensures the representation is syntactically and semantically sound. Data matching depends on whether the specified MS patterns actually exist in the queried file.
- The README and workflow do not provide explicit error handling or recovery strategies for partially valid queries (e.g., a query with one correct clause and one malformed clause).
- No changelog or versioning information is documented, so validation rules may change across MassQL versions without explicit notification.

## Evidence

- [other] Validation against MassQL design principles: "Validate the parse tree against MassQL design principles: expressiveness (captures complex MS patterns), scalability (handles single spectrum to repository queries), and readability (natural MS"
- [other] Parse tree output format: "Return the parse tree in a canonical format (e.g., JSON or pickled Python object) for downstream query execution or analysis."
- [readme] MassQL design principles from README: "Expressiveness - Capture complex mass spectrometry patterns that the community would like to look for. Precision - Exactly prescribe how to find data without ambiguity. Scalable - Easily facilitating"
- [other] Query parsing workflow step: "Construct a parser (e.g., using recursive descent or parser generator such as ANTLR or PLY) that consumes tokens and produces a structured abstract syntax tree (AST) or query object representation."
