---
name: http-endpoint-identification
description: Use when when you have source code access to a webservice component (such as the MAGMa joblauncher) and need to enumerate all exposed HTTP endpoints, their methods (GET, POST, etc.), URL patterns, parameter names, request/response payload structures, and authentication requirements in order to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3071
  tools:
  - MAGMa
  - MAGMa joblauncher
  - OpenAPI 3.0
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# http-endpoint-identification

## Summary

Systematic extraction of HTTP endpoints, request/response schemas, and authentication mechanisms from a webservice codebase by analyzing source files, route definitions, and function signatures. This skill produces a machine-readable API specification (e.g., OpenAPI 3.0) suitable for client integration and documentation.

## When to use

When you have source code access to a webservice component (such as the MAGMa joblauncher) and need to enumerate all exposed HTTP endpoints, their methods (GET, POST, etc.), URL patterns, parameter names, request/response payload structures, and authentication requirements in order to build API documentation or client libraries.

## When NOT to use

- When the webservice is a closed-source binary or compiled component with no accessible source code—reverse-engineering HTTP traffic is required instead.
- When only runtime HTTP traffic traces (network logs, HAR files) are available and source code is unavailable—use packet analysis and behavior-driven endpoint discovery instead.
- When the webservice uses highly dynamic, reflection-based routing that cannot be statically determined from source inspection—runtime introspection or OpenAPI schema served by the application itself is more reliable.

## Inputs

- webservice source code (Python files, route definitions)
- configuration files (e.g., Flask/FastAPI app.py, route blueprints)
- function signatures with type hints and docstrings

## Outputs

- OpenAPI 3.0 specification (JSON or YAML)
- HTTP endpoint inventory (paths, methods, parameters)
- request/response payload schemas
- authentication mechanism documentation

## How to apply

Clone or access the webservice repository and locate all Python route definitions, configuration files, and function signatures. Extract HTTP methods, URL patterns, and parameter names (query, path, body) by parsing route decorators and function signatures. Analyze type hints, docstrings, and serialization logic to infer request and response payload structures. Map the extracted endpoints, methods, parameters, and schemas into a formal API specification format (e.g., OpenAPI 3.0 with components, paths, and operation objects). Validate the generated specification for structural correctness by checking that all endpoint paths are unique, all referenced request/response schemas are defined, and all parameter types are valid. Cross-check the specification against the observed source code to ensure completeness—e.g., verify that every route in the codebase is represented and that no parameter is missing.

## Related tools

- **MAGMa joblauncher** (target webservice component whose HTTP endpoints are to be identified and documented) — https://github.com/NLeSC/MAGMa
- **OpenAPI 3.0** (formal specification format for documenting extracted endpoints, methods, parameters, request/response schemas, and authentication)

## Evaluation signals

- The generated OpenAPI specification parses successfully as valid OpenAPI 3.0 JSON/YAML (no schema validation errors).
- Every HTTP route definition in the source code (e.g., @app.route, @bp.post) is represented as exactly one path and operation in the specification.
- All request and response payload schemas referenced in operations are defined in the components section; no undefined $ref entries remain.
- Parameter counts (query, path, body) match between the source code function signatures and the OpenAPI specification.
- Manual spot-checks on a sample of endpoints (e.g., request a job submission endpoint with correct parameters to the running service) produce responses consistent with the schema.

## Limitations

- Dynamic routing or reflection-based route generation that cannot be statically analyzed from source code may be missed.
- Implicit request/response payload structures (e.g., those inferred only at runtime from serialization libraries) may be incompletely captured without runtime type inspection.
- Custom authentication or middleware logic embedded in decorators or middleware stacks may require additional manual documentation beyond source parsing.
- Changelog documentation for API version history and breaking changes is typically not present in source code and must be sourced separately.

## Evidence

- [other] Locate and examine joblauncher source files (Python, configuration, and route definitions) to identify all HTTP endpoints, HTTP methods, URL patterns, and parameter names.: "Locate and examine joblauncher source files (Python, configuration, and route definitions) to identify all HTTP endpoints, HTTP methods, URL patterns, and parameter names."
- [other] Extract request and response payload structures by analyzing function signatures, type hints, and serialization logic in the joblauncher codebase.: "Extract request and response payload structures by analyzing function signatures, type hints, and serialization logic in the joblauncher codebase."
- [other] Map endpoint paths, methods, parameters (query, path, body), and response schemas into OpenAPI 3.0 format.: "Map endpoint paths, methods, parameters (query, path, body), and response schemas into OpenAPI 3.0 format."
- [readme] The joblauncher subproject that functions as a webservice to execute jobs, serving as the interface for triggering MAGMa calculations.: "joblauncher - Webservice to execute jobs"
- [readme] The web application starts job calculations via the joblauncher webservice.: "The `web` application starts `job` calculations via the `joblauncher` webservice."
