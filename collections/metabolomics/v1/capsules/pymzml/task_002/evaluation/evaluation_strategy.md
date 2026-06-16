# Evaluation Strategy

## Direct Checks

- verify file exists: github:pymzML__pymzML repository is accessible and contains GSGW class implementation
- verify file_format_is: output file has .gz extension and is a valid gzip archive
- verify format_is: gzip header matches igzip specification (magic bytes 1f 8b and compression method byte)
- verify script_runs: GSGW class can be instantiated and accepts Moby Dick text file as input without runtime errors
- verify output_matches_reference: each chapter is stored as independently seekable compressed block (robust to block boundary alignment)
- verify file_exists: indexed .gz file contains valid index structure allowing random access to chapter boundaries
- verify contains_substring: .gz file header contains igzip-compliant index metadata (no canonical answer — multiple index formats valid if igzip-compliant)

## Expert Review

- confirm GSGW class implementation correctly partitions Moby Dick into chapter boundaries (requires manual verification of chapter detection logic)
- assess whether compression efficiency and seek performance meet practical standards for chapter-by-chapter access
- validate igzip specification compliance against RFC 1952 and igzip documentation standards
