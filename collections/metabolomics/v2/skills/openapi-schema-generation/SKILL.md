---
name: openapi-schema-generation
description: Use when when you have a webservice codebase (Python, Java, etc.) with HTTP route definitions, parameter handling, and serialization logic, and you need to generate an OpenAPI 3.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3361
  tools:
  - MAGMa
  - MAGMa joblauncher
  - OpenAPI 3.0 specification standard
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

# openapi-schema-generation

## Summary

Extract HTTP endpoint definitions, request/response schemas, and authentication mechanisms from a webservice codebase and map them into a machine-readable OpenAPI 3.0 specification. This skill is essential for documenting REST API contracts and enabling automated client generation or API validation.

## When to use

When you have a webservice codebase (Python, Java, etc.) with HTTP route definitions, parameter handling, and serialization logic, and you need to generate an OpenAPI 3.0 specification that documents all endpoints, HTTP methods, URL patterns, query/path/body parameters, response payloads, and authentication requirements for client integration or API documentation.

## When NOT to use

- The webservice is not REST-based or uses a different API paradigm (e.g., gRPC, GraphQL, message queues).
- Source code is unavailable or heavily obfuscated, making route definitions and parameter extraction impossible.
- The primary goal is runtime API discovery rather than static documentation; consider dynamic introspection or API proxy tools instead.

## Inputs

- Webservice source code repository (e.g., cloned Git repository with Python Flask/FastAPI/Django routes or similar framework)
- Route definition files (decorators, configuration, URL patterns)
- Function signatures and type hints for endpoint handlers
- Serialization and validation logic (e.g., Pydantic models, JSON schema definitions)
- Authentication and middleware configuration

## Outputs

- OpenAPI 3.0 specification file (JSON or YAML format)
- Documented HTTP endpoints with paths, methods, parameters, and response schemas
- Authentication mechanism definitions (API keys, OAuth, bearer tokens, etc.)
- Request and response payload schema definitions

## How to apply

Clone or obtain the webservice source repository and locate all route/endpoint definitions (e.g., Python decorators, configuration files). Extract endpoint paths, HTTP methods (GET, POST, PUT, DELETE, etc.), parameter names and types from function signatures and type hints, and request/response payload structures from serialization logic or data classes. Map each endpoint's metadata—URL pattern, method, parameters (query, path, body), response schemas, and any authentication headers or mechanisms—into OpenAPI 3.0 format, grouping related endpoints by tags. Validate the generated specification for structural correctness (e.g., required fields, type consistency) and completeness by comparing it against the observed source code to ensure no endpoints or parameters are missing.

## Related tools

- **MAGMa joblauncher** (Webservice component whose HTTP endpoints, request/response schemas, and authentication mechanisms are extracted and mapped to OpenAPI 3.0) — https://github.com/NLeSC/MAGMa
- **OpenAPI 3.0 specification standard** (Target schema format for documenting extracted endpoint definitions, parameters, and response payloads)

## Evaluation signals

- All HTTP endpoints present in the source code are represented in the generated OpenAPI specification (no missing routes).
- Each endpoint's HTTP method, URL path, and parameter names match exactly with the source code definitions.
- Request and response payload schemas are structurally valid and type-consistent with the serialization logic in the codebase.
- Authentication mechanisms (headers, API keys, tokens) specified in the source are correctly documented in the OpenAPI securitySchemes section.
- The generated OpenAPI specification passes structural validation against the OpenAPI 3.0 JSON schema.

## Limitations

- Extraction accuracy depends on code structure clarity; complex or poorly documented parameter handling may require manual refinement.
- Dynamic or runtime-generated routes may not be captured by static source code analysis alone.
- README or repository documentation may be missing or outdated, requiring independent verification of endpoint behavior against the observed codebase.

## Evidence

- [other] Extract HTTP endpoints, request/response schemas, and authentication mechanisms: "What are the HTTP endpoints, request/response schemas, and authentication mechanisms exposed by the joblauncher webservice component in the MAGMa project?"
- [other] Locate and examine joblauncher source files to identify endpoints and parameters: "Locate and examine joblauncher source files (Python, configuration, and route definitions) to identify all HTTP endpoints, HTTP methods, URL patterns, and parameter names."
- [other] Extract payloads from function signatures and type hints: "Extract request and response payload structures by analyzing function signatures, type hints, and serialization logic in the joblauncher codebase."
- [other] Map metadata into OpenAPI 3.0 format: "Map endpoint paths, methods, parameters (query, path, body), and response schemas into OpenAPI 3.0 format."
- [other] Validate the generated specification against source code: "Validate the generated OpenAPI specification for structural correctness and completeness against the observed source code."
- [readme] joblauncher functions as webservice for job submission: "joblauncher - Webservice to execute jobs"
