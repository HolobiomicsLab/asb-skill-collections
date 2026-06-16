# Evaluation Strategy

## Direct Checks

- verify file exists: pbmc3k_processed dataset accessible from Scanpy data module or deposited repository
- script_runs: Python script loading pbmc3k_processed dataset via scanpy.datasets or equivalent and executing tl.rank_genes_groups with Wilcoxon test on leiden cluster labels
- output_matches_reference: returned DataFrame column names include 'names', 'scores', or equivalent ranked gene identifiers and statistical values
- file_format_is: output is a pandas DataFrame or AnnData object with ranked genes structure
- value_in_range: top gene scores (p-values, log fold changes, or test statistics) fall within documented ranges for Wilcoxon test output, robust to minor numerical precision differences
- contains_substring: output DataFrame or figure legend contains at least 3 of the top marker gene names documented in Scanpy examples for pbmc3k leiden clusters

## Expert Review

- verify that top-ranked genes identified are biologically plausible marker genes for the reported leiden clusters (e.g., known markers for immune cell types in PBMC data)
- confirm that Wilcoxon test ranks and effect sizes align with expected differential expression patterns between clusters as reported in Scanpy documentation examples
