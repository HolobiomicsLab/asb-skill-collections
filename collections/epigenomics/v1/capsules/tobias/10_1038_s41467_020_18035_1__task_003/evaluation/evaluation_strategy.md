# Evaluation Strategy

## Direct Checks

- verify that TOBIAS BINDetect executable is available in the loosolab/TOBIAS repository at the commit or release specified in inputs
- verify input file exists: ATAC-seq BAM or bed file (or task output containing aligned reads/peaks)
- verify input file exists: motif Position Weight Matrix (PWM) file in standard format (JASPAR, MEME, or similar)
- verify input file exists: file specifying two or more conditions/samples to compare for differential footprint analysis
- script_runs: BINDetect command executes without fatal errors on provided inputs
- output file exists: structured table (TSV, CSV, or similar tabular format) with one row per TF motif
- field_present: output table contains columns for TF identifier, motif name, and per-condition footprint scores or statistics
- field_present: output table contains a bound/unbound classification or differential occupancy score per TF motif
- value_in_range: occupancy predictions or scores are numeric and fall within expected statistical range (robust to parameter choices)

## Expert Review

- evaluate whether the bound/unbound predictions are biologically plausible given the footprint depletion patterns at motif sites
- assess whether differential occupancy rankings align with known or expected TF activity changes across conditions
- review parameter choices (window size, threshold, normalization) for appropriateness given ATAC-seq data characteristics
