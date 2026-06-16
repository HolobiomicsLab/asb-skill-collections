# Evaluation Strategy

## Direct Checks

- verify that github:mwang87__MassQueryLanguage repository is publicly accessible and contains test-package.yml in .github/workflows/ directory
- verify file_exists: test-package.yml at path .github/workflows/test-package.yml in the repository
- verify script_runs: execute test-package.yml workflow using GitHub Actions CLI or local CI runner against the published MassQL package without errors
- verify output_matches_reference: the workflow execution produces a structured pass/fail report (JSON, YAML, or plain text) with at least one test result field indicating overall pass or fail status
- verify file_format_is: the generated report is in a machine-readable format (JSON, YAML, CSV, or plaintext with parseable structure)
- verify contains_substring: the final report output contains explicit pass/fail indicators (e.g. 'PASSED', 'FAILED', 'success: true', or equivalent status token) — multiple defensible output formats acceptable

## Expert Review

- confirm that all integration tests in test-package.yml are semantically appropriate for validating core MassQL package functionality (query parsing, execution, result serialization) and not redundant with unit tests
- assess whether the reported passing badge state (if claimed in repository README or CI status page) aligns with the observed workflow execution result
