# Evaluation Strategy

## Direct Checks

- verify file airdpro:cli Docker image exists in build artifact repository
- verify file run-cli.sh exists in package inputs or repository root
- verify file sample vendor mass spectrometry raw file (e.g., .raw, .d, .wiff format) is accessible as input
- script_runs: execute run-cli.sh with sample MS raw file in airdpro:cli container and capture stdout/stderr logs
- contains_substring: Wine initialization logs contain evidence of .NET Framework download/setup activity
- file_exists: verify converted Aird output file (.aird or .aird.gz) is created in expected output directory
- value_in_range: if result_wine_startup_time is logged, verify value is >30 min (parameter-sensitive to container overhead and network conditions)
- file_format_is: verify output file format matches Aird specification (robust to compression variant)

## Expert Review

- Examine Wine initialization logs to confirm .NET Framework 4.8 components were downloaded and installed
- Inspect converted Aird output file for structural integrity and compliance with Aird format specification
- Assess whether first-run initialization time documentation aligns with observed >30 min threshold and is reproducible across runs
