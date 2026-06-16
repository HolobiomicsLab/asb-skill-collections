# Evaluation Strategy

## Direct Checks

- verify file exists at output/screening/Diagnostic_QCs_Batch_1/ directory
- file_format_is PNG for all 10 EIC plot files in output/screening/Diagnostic_QCs_Batch_1/
- row_count_equals 10 PNG files present in output/screening/Diagnostic_QCs_Batch_1/ (one per component)
- script_runs: tardisPeaks() executes without error when called with screening_mode=TRUE on vignette LC-MS dataset
- file_exists for each expected EIC plot file matching pattern corresponding to the 10 targets (5 internal standards + 5 endogenous)

## Expert Review

- visual inspection of EIC plots for correct peak identification and appropriate m/z and retention time windows for each of the 10 targets
- verification that screening mode output correctly flags target visibility within specified m/z and RT windows for all 14 runs
- assessment that EIC plot quality is sufficient for diagnostic inspection (clarity, axis labels, peak prominence relative to noise)
