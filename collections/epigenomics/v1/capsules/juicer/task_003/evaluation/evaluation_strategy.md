# Evaluation Strategy

## Direct Checks

- verify that the input .hic file exists and is in HIC format
- verify that juicer_cli_tools command executes without fatal errors on the input .hic artifact
- verify that expected_outputs file is created with correct extension (.bedpe for loop calls, .bed or .domain for domain calls)
- verify that output file is non-empty (row_count > 0)
- verify that output file contains expected columns/fields for the annotation type (e.g., chrom1, start1, end1, chrom2, start2, end2 for loop calls)
- script_runs: juicer_cli_tools annotation command with specified input .hic and output parameters produces exit code 0

## Expert Review

- annotation output contains biologically plausible feature coordinates (no out-of-bounds or malformed genomic ranges)
- feature calls are consistent with known Hi-C contact patterns at expected resolutions and statistical thresholds
- output format and column semantics match Juicer's documented annotation specification for the chosen feature type
