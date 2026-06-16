# Evaluation Strategy

## Direct Checks

- verify file '.github/workflows/main.yml' exists in cloned repository pbjarterot/Met-ID
- script_runs: execute the GitHub Actions workflow main.yml locally (using act, tox, or equivalent CI simulator) and capture exit code
- output_matches_reference: CI workflow exit code equals 0 (success), or document the specific failure stage and error message if non-zero
- verify file_exists for any badge/status artifact (e.g., README.md badge markdown) that claims passing CI status

## Expert Review

- assess whether the locally-simulated CI environment and dependencies sufficiently mirror the GitHub Actions runner specification (OS, Python version, RDKit version) to confirm reproducibility
- evaluate whether any environment-specific or credential-dependent steps (e.g., API keys, private data) prevent genuine local reproduction and determine if the workflow is truly reproducible without external services
