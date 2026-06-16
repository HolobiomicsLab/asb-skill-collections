# Evaluation Strategy

## Direct Checks

- Verify file ESI_NEG_SRFA.d exists in tests/tests_data/ftms/ or is accessible via github:EMSL-Computing/CoreMS
- Verify output is a structured record (JSON or CSV row) with at least three fields: condition_id, method_name, peaks_retained
- Verify peaks_retained is a non-negative integer for each of the three mutually exclusive conditions
- Verify script_runs: the dispatch implementation executes without error on both DS-001 (ESI_NEG_SRFA.d) and DS-003 if available
- Verify output_matches_reference: compare peak counts against SRFA.ref if reference annotations are present
- Verify exactly one of {COND-001, COND-002, COND-003} is selected per spectrum mode (no overlap, no gaps)

## Expert Review

- Chemical validity: confirm that the three noise-threshold conditions produce materially different peak-retention behavior (not spurious or identical results)
- Method selection logic: verify the dispatch criterion (which condition is chosen for each mode) aligns with documented CoreMS parameter selection strategy
- Peak annotation correctness: expert review that peaks retained under each condition are genuine peaks, not noise artifacts or missed signals, by spot-checking against MS domain knowledge
