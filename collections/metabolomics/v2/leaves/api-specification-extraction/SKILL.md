---
name: api-specification-extraction
description: Use when you have access to the source code of a webservice component
  (Python, configuration files, route definitions) and need to produce machine-readable
  API documentation (OpenAPI 3.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3361
  - http://edamontology.org/topic_0769
  tools:
  - MAGMa
  - joblauncher
  license_tier: open
  provenance_tier: literature
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

# api-specification-extraction

## Summary

Extract HTTP endpoint definitions, request/response schemas, and authentication mechanisms from webservice source code and map them into a formal API specification (OpenAPI 3.0). This skill is essential when integrating or documenting webservice components whose interfaces are defined in code rather than published specifications.

## When to use

You have access to the source code of a webservice component (Python, configuration files, route definitions) and need to produce machine-readable API documentation (OpenAPI 3.0 format) that captures all HTTP endpoints, methods, URL patterns, parameter names, payload schemas, and authentication details. This is triggered when the webservice lacks published API documentation but serves as a dependency for other components (e.g., joblauncher webservice in MAGMa is called by the web application to trigger job calculations).

## When NOT to use

- API specification is already published or available in OpenAPI/Swagger format — use direct specification import instead
- Webservice source code is unavailable or obfuscated — extraction requires readable source
- Endpoint behavior is dynamically generated or non-deterministic at runtime — static extraction will be incomplete or inaccurate

## Inputs

- webservice source code repository (Python, configuration files, route definitions)
- function signatures and type hints from endpoint handlers
- serialization logic and data model definitions

## Outputs

- OpenAPI 3.0 specification document (JSON or YAML)
- mapped HTTP endpoints with methods, URL patterns, and parameters
- request and response schemas with type definitions
- authentication mechanism documentation

## How to apply

Clone the webservice repository and locate source files defining HTTP routes, endpoints, and request/response handlers (e.g., Python route definitions and function signatures). Systematically examine each endpoint to extract: (1) HTTP method and URL pattern, (2) query, path, and body parameters with their names and types from function signatures and type hints, (3) request and response payload structures by analyzing serialization logic and type annotations, (4) authentication and authorization mechanisms (e.g., API keys, headers). Map these extracted elements into an OpenAPI 3.0 document structure with proper schemas, parameter definitions, and response models. Validate the generated specification against the source code for structural correctness, parameter completeness, and schema accuracy by cross-referencing endpoint implementations.

## Related tools

- **MAGMa** (source webservice project from which joblauncher component endpoints are extracted) — https://github.com/NLeSC/MAGMa
- **joblauncher** (webservice subcomponent of MAGMa whose HTTP endpoints and schemas are extracted into OpenAPI specification) — https://github.com/NLeSC/MAGMa

## Evaluation signals

- Generated OpenAPI specification validates against OpenAPI 3.0 JSON schema without structural errors
- All HTTP endpoints present in source code are represented in the specification with correct methods and URL patterns
- Request and response payload schemas match the serialization logic and type annotations observed in source code
- Parameter names, types, and locations (query/path/body) extracted from function signatures correspond exactly to actual endpoint implementations
- Authentication mechanisms (if present) are documented with correct header names and validation logic from source code

## Limitations

- Extraction accuracy depends on code readability and consistent use of type hints; untyped or poorly structured code may yield incomplete specifications
- Dynamic endpoints generated at runtime or conditional route definitions may not be fully captured by static source analysis
- Implicit API contracts (e.g., undocumented headers, version-specific behavior) present in code comments but not type annotations may be missed
- The README does not provide detailed endpoint examples or authentication specification details, requiring deep source code inspection for completeness

## Evidence

- [other] what are the HTTP endpoints, request/response schemas, and authentication mechanisms exposed by the joblauncher webservice component in the MAGMa project?: "What are the HTTP endpoints, request/response schemas, and authentication mechanisms exposed by the joblauncher webservice component in the MAGMa project?"
- [other] The MAGMa project includes a joblauncher subproject that functions as a webservice to execute jobs, serving as the interface for triggering MAGMa calculations.: "The MAGMa project includes a joblauncher subproject that functions as a webservice to execute jobs, serving as the interface for triggering MAGMa calculations."
- [other] Locate and examine joblauncher source files (Python, configuration, and route definitions) to identify all HTTP endpoints, HTTP methods, URL patterns, and parameter names.: "Locate and examine joblauncher source files (Python, configuration, and route definitions) to identify all HTTP endpoints, HTTP methods, URL patterns, and parameter names."
- [other] Map endpoint paths, methods, parameters (query, path, body), and response schemas into OpenAPI 3.0 format.: "Map endpoint paths, methods, parameters (query, path, body), and response schemas into OpenAPI 3.0 format."
- [readme] The `web` application starts `job` calculations via the `joblauncher` webservice.: "The `web` application starts `job` calculations via the `joblauncher` webservice."
