# Evaluation Strategy

## Direct Checks

- Verify that github:MarklandGroup__NMR2Struct repository is accessible and contains the NMR2Struct pipeline code (CNN encoder + transformer assembler)
- Verify that the repository contains a test set artifact or reference to a test set of molecules with up to 19 heavy atoms
- Verify that the repository contains trained model weights or instructions to train/obtain them
- Script runs: execute the full NMR2Struct inference pipeline on the test set without errors
- Output matches reference: reproduced top-k exact structure recovery rates (any value of k reported in paper) are within ±2% of reported accuracy metrics
- Verify file_format_is: test set input (NMR spectra) is in a documented format (e.g. CSV, JSON, HDF5, or proprietary format described in README)
- Verify file_exists: model checkpoint or weights file exists in repository or is downloadable from documented source
- Verify row_count_equals or contains_substring: output metrics table contains entries for molecule size bins (e.g. heavy atom ranges) matching reported stratification

## Expert Review

- Whether the reproduced accuracy metrics are chemically and statistically consistent with the reported results, accounting for any stochasticity in model inference
- Whether the test set used for reproduction is identical to or appropriately representative of the reported test set (same molecular diversity, size distribution, spectral acquisition conditions)
- Whether differences in accuracy (if any) are attributable to documented causes (e.g. random seed, hardware differences, library version changes) or indicate pipeline failure
