# Evaluation Strategy

## Direct Checks

- verify that the implementation accepts a structured feature list (e.g., CSV or JSON with m/z, retention time, and elemental composition fields) as input
- verify that the implementation computes mass defect per carbon (MD/C) for each feature according to the formula: MD/C = (exact mass − nominal mass) / carbon count
- verify that the implementation returns a filtered feature list (same format as input) containing only features where MD/C and m/C criteria match thresholds described in the source article
- verify that the output file exists and is readable in the declared format (e.g., CSV, TSV, or JSON)
- verify that row_count_equals: output feature count is less than or equal to input feature count (filtering reduces or preserves set size)
- script_runs: the standalone filter executes without unhandled exceptions when provided valid inputs and valid parameter values

## Expert Review

- confirm that MD/C thresholds and m/C criteria applied match the peer-reviewed definitions and cutoff values documented in the original PFΔScreen publication (section=intro); chemical correctness of mass defect interpretation for PFAS enrichment
- assess whether the filtered subset exhibits enrichment for known PFAS structural motifs (e.g., CF₂, CF₃ groups) compared to the input set, if reference PFAS standards or literature examples are available for validation
- review the numerical precision and rounding behavior of mass defect calculations to ensure they do not introduce spurious inclusions or exclusions at boundary conditions
