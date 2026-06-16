# Evaluation Strategy

## Direct Checks

- verify file exists: descriptor CSV input file referenced in task inputs
- verify file_format_is: output ablation results table is CSV or TSTable with named columns for descriptor_group, molecules_affected, prediction_change_rate
- verify field_present: each row in output table contains descriptor_group identifier, count of molecules with changed predictions, and rate (numeric, 0.0–1.0 range)
- verify row_count_equals: output table has one row per descriptor subgroup ablated (exact count depends on descriptor grouping scheme — no canonical answer)
- verify script_runs: ablation script executes without error on the descriptor CSV input, producing complete output for all subgroups
- verify output_matches_reference: if reference ablation results are deposited in the repository, output table row counts and prediction_change_rate values match reference (byte-for-byte for numeric precision requires careful parameter specification)

## Expert Review

- verify descriptor subgroups are partitioned logically (e.g., by chemical property domain, fingerprint family, or physicochemical class) and defensible given the BitterPredict model architecture
- verify ablation procedure (zero-out or removal strategy) is chemically and computationally sound: does zeroing a descriptor subgroup preserve valid input format and avoid model crashes?
- verify prediction_change_rate interpretation: confirm that reported changes reflect true label flips (bitter→not-bitter or vice versa) vs. confidence score shifts, and that rate calculation (numerator/denominator) is correctly specified
- verify reproducibility: confirm that ablation order, random seeds (if stochastic), and tie-breaking rules are documented sufficiently to allow a second computational agent to reproduce identical rates
