# Evaluation Strategy

## Direct Checks

- file_exists: verify that joblauncher source files are present in github:NLeSC/MAGMa repository under a joblauncher/ or equivalent subdirectory
- file_format_is: verify that produced artifact is valid JSON or YAML (OpenAPI 3.0 or 3.1 specification)
- contains_substring: verify that output schema contains at least one 'paths' or 'endpoints' key documenting HTTP routes
- contains_substring: verify that output schema declares HTTP methods (GET, POST, PUT, DELETE, PATCH) for joblauncher endpoints
- contains_substring: verify that output schema includes 'components' or 'definitions' section with request/response model schemas
- script_runs: verify that produced OpenAPI artifact passes validation against openapi-generator or swagger-cli validate command without fatal errors

## Expert Review

- Verify that extracted endpoint signatures (paths, parameters, request bodies, response codes) accurately reflect joblauncher source code; require spot-check of 3+ endpoints against raw implementation
- Assess completeness of parameter documentation (required vs optional, data types, constraints) relative to actual function signatures in joblauncher source
- Evaluate semantic accuracy of request and response schema definitions against actual data structures used in joblauncher handlers
