# Evaluation Strategy

## Direct Checks

- verify file exists at github:Nextflow4Metabolomics/nextflow4ms-dial repository root
- verify nextflow executable version is ≥22.10.0 via 'nextflow -v'
- verify Singularity is installed and functional via 'singularity --version'
- file_exists: a public .mzML LC-MS dataset (input file or persistent accession/URL)
- script_runs: nextflow workflow invocation command with -profile singularity completes without fatal errors, robust to reasonable resource allocation parameter choices
- file_exists: expected output directory structure produced by MS-DIAL processing step
- file_exists: final MSFLO output artifact (format and naming convention to be confirmed against workflow definition)
- contains_substring: workflow execution log contains no 'ERROR' or 'FAILED' status indicators
- contains_substring: workflow completion message or success flag in .nextflow.log or equivalent execution report

## Expert Review

- Verify that output files (.mzML processed data, MS-DIAL feature table, MSFLO statistical results) are scientifically plausible for the input LC-HRMS dataset (e.g., reasonable peak count, mass accuracy, retention time range, feature intensity distribution)
- Assess whether workflow output schema and column names conform to MS-DIAL and MSFLO standard conventions
- Confirm that containerized MS-DIAL and MSFLO versions embedded in Singularity image are compatible with the workflow configuration and produce metabolomics results consistent with standalone tool documentation
