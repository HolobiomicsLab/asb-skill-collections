---
name: python-source-code-analysis
description: Use when you have a Python webservice codebase (e.g., a Flask, Django,
  or FastAPI application) and need to document its HTTP API surface (endpoints, methods,
  parameters, schemas, authentication) for integration, testing, or specification
  generation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3316
  tools:
  - MAGMa
  - NLeSC/MAGMa joblauncher
  license_tier: restricted
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

# Python source code analysis

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically extract HTTP endpoints, request/response schemas, and authentication mechanisms from Python webservice source code by analyzing route definitions, function signatures, type hints, and serialization logic. This skill enables reverse-engineering of webservice interfaces from implementation source when formal API documentation is absent or incomplete.

## When to use

You have a Python webservice codebase (e.g., a Flask, Django, or FastAPI application) and need to document its HTTP API surface (endpoints, methods, parameters, schemas, authentication) for integration, testing, or specification generation. Use this when formal OpenAPI/Swagger documentation does not exist or is out of sync with the implementation.

## When NOT to use

- The webservice already has complete, up-to-date OpenAPI/Swagger documentation that matches the implementation.
- The codebase is not Python-based or does not use HTTP/REST (e.g., RPC, gRPC, or non-web protocols).
- Source code is unavailable, obfuscated, or dynamically generated at runtime without static definition points.

## Inputs

- Python webservice source code repository (git clone or directory)
- Route/endpoint definition files (Flask blueprints, Django urls.py, FastAPI routers, etc.)
- Function signatures with type hints and docstrings
- Request/response payload serialization code (e.g., Marshmallow schemas, Pydantic models, JSON handlers)

## Outputs

- HTTP endpoint inventory (path, method, parameters, request/response schemas)
- OpenAPI 3.0 specification (YAML or JSON)
- Authentication mechanism documentation
- Parameter and payload schema mapping

## How to apply

Clone or obtain the Python webservice repository and locate route/endpoint definition files (e.g., Flask blueprints, URL patterns, or decorator-based route registrations). Examine function signatures, type hints, docstrings, and parameter names to extract endpoint paths, HTTP methods (GET, POST, etc.), and query/path/body parameter structures. Analyze request and response payload handling by tracing serialization logic (JSON encoding, schema validators, ORM models). Map observed endpoint metadata into a formal specification format such as OpenAPI 3.0, ensuring all path parameters, query parameters, request bodies, and response schemas are captured. Validate the generated specification against the observed source code for structural correctness, completeness, and consistency with actual implementation.

## Related tools

- **NLeSC/MAGMa joblauncher** (Python webservice component whose HTTP endpoints, schemas, and authentication mechanisms are reverse-engineered through source code analysis to generate OpenAPI specifications) — https://github.com/NLeSC/MAGMa

## Evaluation signals

- All HTTP endpoints defined in the source code (route decorators, URL patterns, blueprint registrations) are captured in the generated specification.
- Extracted parameter names, types, and locations (path, query, body) match function signatures and type hints in the source code exactly.
- Request and response payload schemas (field names, types, required/optional status) correspond to serialization logic and model definitions in the implementation.
- Generated OpenAPI specification passes structural validation (e.g., via openapi-spec-validator or similar) and can be used to generate client code or test harnesses that interact correctly with the actual service.
- Authentication mechanisms (API keys, OAuth, token validation) referenced in source code (middleware, decorators, request handlers) are accurately documented in the specification.

## Limitations

- Dynamic route registration or endpoint generation at runtime may not be visible in static source code analysis.
- Implicit or undocumented authentication behavior (e.g., custom middleware that modifies request/response) may be missed if not explicitly coded in route handlers.
- Complex type hints, union types, or forward references may require additional interpretation beyond simple type annotation parsing.
- Version-specific API variants or deprecated endpoints embedded in the same codebase may require manual reconciliation.
- The README did not provide detailed implementation examples of the joblauncher webservice endpoints, limiting validation scope in this project.

## Evidence

- [other] The MAGMa project includes a joblauncher subproject that functions as a webservice to execute jobs, serving as the interface for triggering MAGMa calculations.: "The MAGMa project includes a joblauncher subproject that functions as a webservice to execute jobs, serving as the interface for triggering MAGMa calculations."
- [other] Locate and examine joblauncher source files (Python, configuration, and route definitions) to identify all HTTP endpoints, HTTP methods, URL patterns, and parameter names.: "Locate and examine joblauncher source files (Python, configuration, and route definitions) to identify all HTTP endpoints, HTTP methods, URL patterns, and parameter names."
- [other] Extract request and response payload structures by analyzing function signatures, type hints, and serialization logic in the joblauncher codebase.: "Extract request and response payload structures by analyzing function signatures, type hints, and serialization logic in the joblauncher codebase."
- [other] Map endpoint paths, methods, parameters (query, path, body), and response schemas into OpenAPI 3.0 format.: "Map endpoint paths, methods, parameters (query, path, body), and response schemas into OpenAPI 3.0 format."
- [readme] joblauncher - Webservice to execute jobs: "joblauncher - Webservice to execute jobs"
- [readme] The `web` application starts `job` calculations via the `joblauncher` webservice.: "The `web` application starts `job` calculations via the `joblauncher` webservice."
