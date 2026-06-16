# Evaluation Strategy

## Direct Checks

- verify file exists in tximportData package: tximportData/extdata/ directory contains transcript quantification files (Salmon, kallisto, or RSEM format)
- verify script_runs: R script loading tximportData, calling tximport() with type parameter matching quantification tool, and tx2gene mapping produces executable code without errors
- verify output_matches_reference: tximport() output is a list with named element 'counts' (gene-level matrix)
- verify file_format_is: resulting counts matrix is numeric (non-negative integers), rows labeled by gene identifiers, columns labeled by sample identifiers
- verify value_in_range: all values in counts matrix are non-negative integers (un-normalized raw counts, no fractional or negative values)
- verify row_count_equals: gene-level count matrix row count matches expected number of unique genes in tx2gene mapping (no duplicates or missing genes)
- verify field_present: output matrix has row names (gene IDs) and column names (sample IDs) as character vectors

## Expert Review

- Confirm that tximport aggregation from transcript to gene level preserves count semantics: summed transcript counts per gene are appropriate for DESeq2 input (not scaled, not normalized by library size, not length-adjusted)
- Verify that un-normalized counts are suitable as input to DESeqDataSetFromTximport() (i.e., counts have not been TPM/FPKM/CPM transformed or offset)
- Confirm tx2gene mapping is correctly constructed and matches the transcript identifiers in the quantification files
