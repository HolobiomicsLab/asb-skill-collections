# Evaluation Strategy

## Direct Checks

- verify file exists: check that falcon-ms and spectrum-utils==0.3.5 can be installed via pip without errors
- script_runs: execute falcon command-line tool on the Bittremieux et al. 2021 dataset (doi:10.1002/rcm.9153) and confirm exit code is 0
- file_exists: verify that cluster assignment output file is produced by the falcon run
- file_format_is: confirm output file is a valid structured format (CSV, TSV, or JSON) that can be parsed
- row_count_equals: verify output file contains at least 1 row of cluster assignments (non-empty result)

## Expert Review

- Inspect cluster assignment output for semantic correctness: verify that spectrum identifiers are present and cluster IDs are assigned as expected for MS/MS data
- Confirm that the number of clusters and cluster size distribution are reasonable given the dataset size and falcon algorithm parameters
