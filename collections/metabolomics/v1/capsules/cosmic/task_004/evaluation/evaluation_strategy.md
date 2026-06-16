# Evaluation Strategy

## Direct Checks

- verify that github:sirius-ms__sirius repository is accessible and contains MSNovelist web service client code
- verify file_exists for MSNovelist endpoint configuration or documentation within the repository
- script_runs: execute a minimal MSNovelist query submission using the repository's API client or CLI with a test molecular mass input, and verify the script completes without runtime errors
- verify output_matches_reference: retrieved candidate structures are returned in a structured format (JSON, XML, or CSV), byte-for-byte matching the documented schema from the repository or official MSNovelist documentation

## Expert Review

- chemoinformatics expert review: assess whether the de-novo generated candidate structures are chemically plausible and consistent with the input query (molecular mass, ionization mode, adduct type)
- software architecture review: confirm that the submission and retrieval workflow follows the intended MSNovelist API contract and does not introduce undocumented side-effects or data loss
