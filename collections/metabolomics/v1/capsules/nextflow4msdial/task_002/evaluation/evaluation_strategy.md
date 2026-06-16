# Evaluation Strategy

## Direct Checks

- Verify file github:Nextflow4Metabolomics__nextflow4ms-dial exists and is accessible
- Verify Nextflow version ≥22.10.0 is installed and executable
- Verify Docker is installed and daemon is running
- Script runs: execute nextflow run on the repository with Docker profile and a public .mzML dataset (e.g., from MetaboLights or MassIVE); workflow must complete without fatal errors
- File exists: verify that MS-DIAL output directory contains expected metabolomics feature table or annotation files (robust to naming convention variations)
- File exists: verify that MSFLO output files are present in designated output directory
- Verify workflow execution log contains no ERROR or FAILED status messages

## Expert Review

- Evaluate whether output feature table structure and column headers match expected MS-DIAL output schema for LC-HRMS metabolomics data
- Evaluate whether detected metabolite annotations and mass accuracy are chemically plausible for the input dataset
- Assess whether output files are suitable for downstream metabolomics statistical analysis
