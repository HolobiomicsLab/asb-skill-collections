# Evaluation Strategy

## Direct Checks

- file_exists: verify that a public .msp test file is accessible in the github.com/RECETOX/MSMetaEnhancer repository (check repository structure or documentation for file location)
- script_runs: execute MSMetaEnhancer annotation pipeline on the .msp file with logging enabled and verify that the process completes without fatal errors
- file_format_is: verify that the Logger component output file exists and is valid JSON or structured text format
- contains_substring: verify that the Logger output contains per-attribute fill-rate statistics (quantitative progress metrics)
- output_matches_reference: verify that the summary table structure includes named metadata field columns and numeric coverage/fill-rate values, robust to ordering and whitespace
- value_in_range: verify that all fill-rate values in the summary table are between 0 and 100 (or 0 and 1 if normalized), parameter-sensitive to normalization convention

## Expert Review

- assess whether the per-attribute fill-rate statistics reported in the Logger output are consistent with expected behavior for the annotation services queried (CIR, CTS, PubChem, IDSM, BridgeDb)
- evaluate whether the summary table's coverage metrics reflect realistic annotation success rates given potential service downtime, rate limiting, or malformed input compounds
- assess whether the choice and labeling of metadata fields in the summary table align with the package's stated design (SMILES, InChI, CAS number, and related attributes)
