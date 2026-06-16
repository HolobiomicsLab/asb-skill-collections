# Evaluation Strategy

## Direct Checks

- file_exists: verify that salmon 2.0 source code repository (github:COMBINE-lab/salmon) contains a writeMappings function or equivalent SAM output handler
- script_runs: execute salmon 2.0 quant on a test dataset (human GEUVADIS ERR188044 or yeast ERR458493) with SAM output enabled (if available via --writeMappings or similar flag) and confirm the command completes without error
- output_matches_reference: retrieve the reported mapping count (total mapped reads) from salmon quant's standard output or log file on the test dataset
- row_count_equals: verify that the SAM output file record count (excluding header lines, byte-for-byte) matches the mapping count reported by salmon quant on the same test run
- file_format_is: verify that the SAM output file conforms to SAM format specification (header lines starting with @, data lines with tab-delimited fields)
- value_in_range: confirm that per-transcript selective-alignment quantification Pearson correlation vs. C++ salmon 1.12.0 remains at or above 0.999 on byte-identical index (robust to parameter choices)

## Expert Review

- Review salmon 2.0 source code (cpp branch and Rust rewrite) to identify and document the exact nature of the writeMappings flush bug: confirm whether an ostream buffer was indeed not flushed before close, and verify that the fix (if applied) correctly calls flush() or uses a non-buffered stream
- Verify that the fix does not introduce off-by-one errors, duplicate records, or corrupted SAM records in the output
- Assess whether the fix is consistent with SAM specification and whether downstream tools (e.g., samtools, alignment viewers) successfully parse the corrected SAM file without warnings or errors
