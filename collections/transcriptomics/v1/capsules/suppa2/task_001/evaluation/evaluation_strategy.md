# Evaluation Strategy

## Direct Checks

- verify that github:comprna__SUPPA repository is accessible and contains SUPPA2 source code
- verify file_exists: GTF input file is loadable and conforms to GTF format specification
- verify file_exists: output ioe file (isoform events) is generated with expected structure
- verify file_exists: output ioi file (isoform-isoform events) is generated with expected structure
- verify file_exists: output GTF file for local events is generated in valid GTF format
- verify row_count_equals or value_in_range: output files contain non-zero number of event records (parameter-sensitive to input annotation complexity)
- verify format_is: ioe file format matches SUPPA2 specification for isoform event output
- verify format_is: ioi file format matches SUPPA2 specification for isoform-isoform event output
- verify script_runs: SUPPA2 generateEvents subcommand executes without fatal errors on provided GTF input
- verify contains_substring: output files contain expected event type identifiers (e.g., exon skipping, alternative 5'/3' splice sites)

## Expert Review

- inspect biological plausibility of generated events: verify that isoform events correspond to known alternative splicing mechanisms and are consistent with input GTF transcript structures
- inspect consistency between three outputs: verify that events in ioe file, ioi file, and local-events GTF file are mutually coherent and do not contain logical contradictions
- inspect accuracy of event definition: verify that exon coordinates, splice sites, and event boundaries in output files correctly reflect the input GTF annotation
