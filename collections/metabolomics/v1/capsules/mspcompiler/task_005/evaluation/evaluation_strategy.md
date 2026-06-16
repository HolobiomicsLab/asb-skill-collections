# Evaluation Strategy

## Direct Checks

- verify that a test directory containing multiple MSP files exists and is accessible
- verify file_exists: output object from read_multilibs is a valid R object with class attribute
- verify that future::plan(multisession) can be called without error before read_multilibs execution
- verify script_runs: parallel execution with multisession backend completes without error
- verify that the merged library object produced by multisession execution has identical structure (field names, row counts) to the serial baseline result, robust to library content variations
- verify that the multisession merged result contains_substring matching all expected spectral records from input MSP files

## Expert Review

- Assess whether worker session spawning can be confirmed (e.g., via system monitoring, process logging, or future internals inspection) — multiple defensible approaches exist for verification
- Assess whether the merged library object values (compound names, m/z ratios, retention indices) are identical between serial and parallel execution paths, accounting for floating-point tolerance if applicable
- Assess whether performance metrics (execution time, CPU utilization) demonstrate genuine parallelism or merely concurrent scheduling without speedup
