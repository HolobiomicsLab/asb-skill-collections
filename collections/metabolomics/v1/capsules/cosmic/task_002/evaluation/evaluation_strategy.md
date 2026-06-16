# Evaluation Strategy

## Direct Checks

- verify that github:sirius-ms__sirius repository is accessible and contains CSI:FingerID implementation code
- verify that a working CSI:FingerID web service endpoint URL is documented or discoverable in the repository
- file_exists: check that example spectrum input files or test data are present in the repository (e.g., .ms, .mgf, or JSON spectrum formats)
- script_runs: verify that a parsing and submission script can be executed without runtime errors on sample spectrum data
- output_matches_reference: verify that fingerprint prediction output from the endpoint matches expected JSON schema (contains predicted fingerprint scores or feature vectors)

## Expert Review

- assess whether the fingerprint predictions returned by CSI:FingerID are chemically plausible and rank known correct structures appropriately
- evaluate whether request-response latency and service availability meet documented SLA or expected performance characteristics
- review whether authentication, rate-limiting, or access control on the endpoint is properly documented and respected
