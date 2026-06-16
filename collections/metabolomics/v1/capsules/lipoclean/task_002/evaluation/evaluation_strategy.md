# Evaluation Strategy

## Direct Checks

- verify file 'options.txt' exists in the working directory after CLI execution
- verify file 'options.txt' has format TOML (text file parseable as TOML key-value pairs)
- verify options.txt contains field 'msdial_version' with value '4' or '5' matching the --print argument
- verify options.txt contains at least one configuration key expected for MS-DIAL lipid filtering (e.g., thresholds, model paths, or feature columns); no canonical answer for exact key set without seeing reference file
- script_runs: LipoCLEAN CLI invocation with '--print MSD4' argument completes without error
- script_runs: LipoCLEAN CLI invocation with '--print MSD5' argument completes without error

## Expert Review

- Confirm that the keys and structure present in options.txt are appropriate for configuring MS-DIAL version 4 or 5 lipid filtering (requires domain knowledge of MS-DIAL configuration format and LipoCLEAN expected parameters)
