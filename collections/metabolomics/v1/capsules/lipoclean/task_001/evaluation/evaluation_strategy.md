# Evaluation Strategy

## Direct Checks

- verify file exists: the TOML-formatted options file passed as input to the CLI
- verify file exists: the MS-DIAL export artifact (input dataset or reference file) referenced in the TOML config
- script_runs: LipoCLEAN CLI invocation with TOML config file completes without non-zero exit code
- file_exists: at least one output artifact is produced by the tool (file, report, or structured record); exact output format and naming convention should be confirmed from tool documentation or repository README
- robust to parameter choices: the TOML config can specify different MS-DIAL versions (4 or 5 per EnrichedIndex) and tool should handle version-specific defaults

## Expert Review

- Verify that the output artifact(s) produced by LipoCLEAN are scientifically plausible quality-filtered lipid identifications (e.g., records retain expected fields, filtering logic is applied, no data corruption)
- Confirm that the TOML configuration was correctly parsed and applied by inspecting output metadata or logs for parameter echo
