# Evaluation Strategy

## Direct Checks

- verify file output exists and has extension .bed or .bed.gz
- verify file_format_is gzip-compressed or plain text BED format
- verify row_count_equals greater than 0 (non-empty file)
- verify field_present: file contains at least 3 tab-separated columns (chrom, chromStart, chromEnd per BED standard)
- verify field_present: file contains additional fragment-specific fields (e.g., name/barcode, count, strand information); multiple valid column schemas exist for fragment files
- script_runs: pp.make_fragment_file executes without error on input BAM with coordinate-sorted property verified
- verify output_matches_reference: fragment file structure aligns with SnapATAC2 fragment file specification (exact schema may vary; no canonical reference deposit provided)

## Expert Review

- inspect fragment file for biological plausibility: barcode distribution, fragment length statistics, and per-barcode read counts are reasonable for input BAM
- assess whether fragment file is suitable for downstream SnapATAC2 operations (pp.import_fragments, matrix generation)
- confirm coordinate sorting and overlapping fragment handling are correct relative to BAM input
