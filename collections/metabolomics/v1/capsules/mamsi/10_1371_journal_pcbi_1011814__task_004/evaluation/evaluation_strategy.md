# Evaluation Strategy

## Direct Checks

- verify that kopeckylukas/py-mamsi repository exists and is accessible at https://github.com/kopeckylukas/py-mamsi
- verify that kopeckylukas/py-mamsi-tutorials repository exists with sample LC-MS feature list data at https://github.com/kopeckylukas/py-mamsi-tutorials
- script_runs: execute MAMSI structural clustering workflow on provided LC-MS feature list with 'all adducts' parameter configuration without errors
- script_runs: execute MAMSI structural clustering workflow on same LC-MS feature list with 'most-common adducts' parameter configuration without errors
- file_exists: results table comparing cluster count and size distribution between 'all adducts' and 'most-common adducts' conditions
- file_format_is: results table is in a standard tabular format (CSV, TSV, or pandas DataFrame pickle)
- field_present: results table contains at least column headers for 'condition', 'total_cluster_count', and cluster size distribution metrics
- robust to parameter choices: cluster count values are numeric integers ≥ 1, cluster size distribution metrics are numeric and non-negative

## Expert Review

- Do differences in cluster counts and size distributions between 'all adducts' vs 'most-common adducts' align with expected adduct ionisation behavior in electrospray LC-MS?
- Are the structural clusters formed by the 'most-common adducts' condition chemically and biochemically meaningful given the metabolomic context?
- Do reported cluster size distributions reflect plausible m/z and retention time groupings for metabolite ion families?
