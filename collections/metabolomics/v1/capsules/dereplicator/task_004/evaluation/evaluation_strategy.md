# Evaluation Strategy

## Direct Checks

- verify file_exists: spec_nets/propagations.pdf in output directory
- verify file_exists: spec_nets output folder is created
- verify file_format_is: propagations.pdf is a valid PDF file (byte-for-byte magic number check)
- verify row_count_equals or field_present: two additional named output files are present in spec_nets folder with names matching manual documentation

## Expert Review

- inspect propagations.pdf visually to confirm spectral network visualization content is sensible and non-empty
- confirm the two additional named output files match the exact filenames and purposes documented in the NPDtools 2.5.0 manual for Spectral Networking stage
