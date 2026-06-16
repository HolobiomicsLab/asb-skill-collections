# Evaluation Strategy

## Direct Checks

- verify file exists: input differential peaks table (from task_NNN.expected_outputs or public deposit)
- verify file exists: CIS-BP motif database (public accession or downloaded artifact)
- script_runs: SnapATAC2 tl.motif_enrichment invocation on input peaks and motif database completes without error
- file_format_is: output table is CSV, TSV, or structured record (Parquet/HDF5)
- field_present: output table contains column for motif IDs
- field_present: output table contains column for enrichment scores
- field_present: output table contains column for p-values
- row_count_equals: output table has at least one row (robust to dataset size, parameter-sensitive to motif database version and filtering thresholds)
- value_in_range: enrichment score values are numeric and finite
- value_in_range: p-values are numeric, in range [0, 1]

## Expert Review

- Enrichment scores and p-values are statistically reasonable given the input peak set and motif database (no implausibly extreme values or systematic biases)
- Motif IDs match expected CIS-BP identifier format and are present in the version of the database used
