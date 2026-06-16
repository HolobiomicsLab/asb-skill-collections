# Evaluation Strategy

## Direct Checks

- verify that github:sirius-ms__sirius repository contains CANOPUS web service client code or endpoint documentation
- file_exists: locate a concrete example or integration test file in the repository that demonstrates submitting a fingerprint/spectrum query to CANOPUS and parsing the response
- script_runs: execute a minimal reproducible example (if present in repo) that submits a query to the CANOPUS endpoint and confirm it returns a structured compound-class annotation without error
- verify output_matches_reference: confirm that the returned annotation structure contains expected fields (e.g., compound class labels, confidence scores, or similar structured metadata) consistent with CANOPUS documentation or published examples

## Expert Review

- assess whether the CANOPUS endpoint query implementation correctly encodes fingerprints or spectra in the format required by the service
- evaluate whether the returned compound-class annotations are chemically and methodologically valid for a representative test case
- verify that error handling and response parsing are robust to edge cases (e.g., ambiguous matches, no-hit scenarios, malformed input)
