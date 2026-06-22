---
name: rest-api-contract-documentation
description: Use when a webservice component (like MAGMa's joblauncher) lacks formal API documentation but the source code is accessible, and downstream consumers (web applications, external services) need to understand available HTTP endpoints, parameter schemas, and response formats without manual.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3489
  - http://edamontology.org/topic_0091
  tools:
  - MAGMa
  - MAGMa joblauncher
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5702/massspectrometry.S0033
  all_source_dois:
  - 10.5702/massspectrometry.S0033
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# REST API Contract Documentation

## Summary

Generate machine-readable API specifications (OpenAPI 3.0) by systematically analyzing webservice source code to extract endpoints, HTTP methods, request/response schemas, and authentication mechanisms. This skill ensures API consumers have a complete, validated contract of available operations and data structures.

## When to use

Apply this skill when a webservice component (like MAGMa's joblauncher) lacks formal API documentation but the source code is accessible, and downstream consumers (web applications, external services) need to understand available HTTP endpoints, parameter schemas, and response formats without manual reverse-engineering.

## When NOT to use

- Webservice source code is not available or access is restricted — use client-side introspection tools instead.
- API already has an existing, maintained OpenAPI/Swagger specification — validate and update that rather than regenerating.
- Endpoints are dynamically generated at runtime with no static route definitions — static source analysis will be incomplete.

## Inputs

- Webservice source repository (Git clone or codebase snapshot)
- Route definition files (Flask blueprints, FastAPI app files, etc.)
- Handler function implementations with type hints and decorators
- Request validation and serialization code

## Outputs

- OpenAPI 3.0 specification document (YAML or JSON)
- Validated endpoint inventory (paths, methods, parameters)
- Request/response schema definitions
- Authentication mechanism documentation

## How to apply

Clone the target repository and locate webservice source files (route definitions, handler functions, serialization logic). Examine function signatures, type hints, decorators (e.g., Flask/FastAPI route annotations), and parameter validation to identify all HTTP endpoints and methods. Extract request payload structures by analyzing function parameters, request body parsing, and validation rules; extract response schemas by tracing return statements and serialization code. Map all discovered paths, HTTP methods, query/path/body parameters, and response schemas into OpenAPI 3.0 format using a structured generator or manual transcription. Validate the resulting specification for structural correctness (valid YAML/JSON, required fields present) and completeness (all routes from source code are represented) by cross-referencing against the original source.

## Related tools

- **MAGMa joblauncher** (Webservice component whose HTTP endpoints, request schemas, and response formats are extracted and documented as an OpenAPI specification) — https://github.com/NLeSC/MAGMa

## Evaluation signals

- Generated OpenAPI specification is valid YAML/JSON with no syntax errors
- All HTTP endpoints discovered in source code route definitions are represented in the specification with correct methods (GET, POST, etc.)
- Request parameter names, types (string, integer, etc.), and required/optional status match the source code function signatures and validation logic
- Response schema structures match the data returned by handler functions as evidenced by serialization and return statements
- Authentication mechanisms (if present) are correctly documented in the OpenAPI securitySchemes section and applied to appropriate endpoints

## Limitations

- Source code analysis captures only statically-defined routes; dynamically-generated endpoints or plugin-based extensions may be missed.
- Type hints and documentation must be present or complete in source code; weakly-typed or undocumented handlers may produce incomplete schemas.
- Complex request payloads with nested objects or conditional fields may require manual refinement after initial extraction.

## Evidence

- [readme] joblauncher - Webservice to execute jobs: "joblauncher - Webservice to execute jobs"
- [other] The MAGMa project includes a joblauncher subproject that functions as a webservice to execute jobs, serving as the interface for triggering MAGMa calculations.: "The MAGMa project includes a joblauncher subproject that functions as a webservice to execute jobs, serving as the interface for triggering MAGMa calculations."
- [other] Locate and examine joblauncher source files (Python, configuration, and route definitions) to identify all HTTP endpoints, HTTP methods, URL patterns, and parameter names.: "Locate and examine joblauncher source files (Python, configuration, and route definitions) to identify all HTTP endpoints, HTTP methods, URL patterns, and parameter names."
- [other] Map endpoint paths, methods, parameters (query, path, body), and response schemas into OpenAPI 3.0 format.: "Map endpoint paths, methods, parameters (query, path, body), and response schemas into OpenAPI 3.0 format."
- [other] Validate the generated OpenAPI specification for structural correctness and completeness against the observed source code.: "Validate the generated OpenAPI specification for structural correctness and completeness against the observed source code."
