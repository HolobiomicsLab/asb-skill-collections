# Evaluation Strategy

## Direct Checks

- verify file exists in github:mwang87__DeepSAT repository containing API endpoint documentation or implementation for /api/smart3/search
- script_runs: execute a programmatic POST request to the /api/smart3/search endpoint with a valid JSON payload containing a list of dicts with '1H' and '13C' keys
- output_matches_reference: returned response is valid JSON with a structured prediction object (no canonical answer — structure depends on model version and API contract)
- verify response contains at least one field indicative of classification output (e.g. compound name, confidence score, or metadata — parameter-sensitive to API contract version)

## Expert Review

- assess whether the JSON response structure and field semantics align with the documented DeepSAT Classification API specification
- evaluate whether peak input format (1H and 13C headers as list of dicts) matches the actual API contract and produces chemically valid predictions
- review whether any validation errors or malformed responses indicate missing or incompatible model input names (per finding: 'Model input names may change and require code updates')
