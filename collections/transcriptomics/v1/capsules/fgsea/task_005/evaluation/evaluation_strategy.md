# Evaluation Strategy

## Direct Checks

- verify file exists in fgsea package: examplePathways (R data object)
- verify file exists in fgsea package: exampleRanks (R data object)
- script_runs: load examplePathways and exampleRanks in R and execute fgsea(examplePathways, exampleRanks, eps=0) without errors
- script_runs: load examplePathways and exampleRanks in R and execute fgsea(examplePathways, exampleRanks, eps=1e-10) without errors
- output_matches_reference: fgsea with eps=0 returns data.frame or list with named column 'pval' (or 'padj') for each pathway
- output_matches_reference: fgsea with eps=1e-10 returns data.frame or list with named column 'pval' (or 'padj') for each pathway
- value_in_range: median or mean P-value from eps=0 run is strictly less than median or mean P-value from eps=1e-10 run across same pathways (robust to ordering; parameter-sensitive to choice of aggregation statistic)
- row_count_equals: both fgsea runs return results for identical set of pathways (same number of rows, same pathway names)

## Expert Review

- Assess whether reported P-values from eps=0 run are substantively more precise (lower variance, finer granularity) than eps=1e-10 lower-bound estimates, as claimed for adaptive multi-level split scheme
- Evaluate whether precision improvement is consistent across pathways of different sizes and effect magnitudes, or only in specific subsets
- Judge whether the comparison demonstrates the correctness and practical benefit of the adaptive multi-level split Monte Carlo implementation versus the fixed eps truncation
