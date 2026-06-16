# Evaluation Strategy

## Direct Checks

- Verify file exists: github:mwang87__DeepSAT repository clone or download available
- Verify script_runs: HTTP GET request to /model/metadata endpoint completes without network/connection errors
- Verify file_format_is: returned response is valid JSON
- Verify field_present: parsed JSON response contains 'model_spec' or 'inputs' field (no canonical answer — structure depends on TensorFlow Serving version)
- Verify contains_substring: extracted model input names include at least one of '1H' or '13C' or similar spectroscopic identifiers matching EnrichedIndex evidence
- Verify output_matches_reference: response structure conforms to TensorFlow Serving /model/metadata OpenAPI schema (robust to parameter choices across compatible serving versions)

## Expert Review

- Assess whether extracted input names align with the peak JSON structure (1H, 13C headers) documented in the API specification
- Confirm that the metadata query mechanism and response parsing logic are appropriate for the specific TensorFlow Serving deployment version used by SMART 3
- Review code robustness: verify that fallback or error-handling is in place if model input names change in future deployments
