# Evaluation Strategy

## Direct Checks

- verify file exists at github:FredHutch__SEACR
- verify repository can be cloned without errors
- file_exists: shell script files (*.sh) in cloned repository root or standard subdirectories (bin/, scripts/)
- file_exists: R script files (*.R) in cloned repository root or standard subdirectories (bin/, scripts/, R/)
- verify shell scripts have executable permissions (mode includes +x)
- verify R scripts are readable and syntactically valid R (script_runs on R parser without fatal errors)
- script_runs: end-to-end SEACR execution with minimal valid CUT&RUN bedGraph input file
- file_exists: peaked-regions output file produced after end-to-end run
- file_format_is: output file has expected format (BED or similar tabular peak region format), robust to naming conventions
- output_matches_reference: output structure contains expected columns for peak regions (chromosome, start, end, score or similar), no canonical answer for exact column names or order across SEACR versions

## Expert Review

- confirm that the cloned SEACR repository is the correct and current version intended for CUT&RUN analysis
- assess whether the minimal test bedGraph input is representative of real CUT&RUN data and appropriate for validating end-to-end functionality
- evaluate whether the peaked-regions output file content is biologically sensible (e.g., peak coordinates fall within expected genomic ranges, score values are in expected ranges)
