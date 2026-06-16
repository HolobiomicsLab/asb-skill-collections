# Evaluation Strategy

## Direct Checks

- verify that a TSV table file exists in bioRxiv preprint 739011 (Chen et al.) or its supplementary materials containing clustering accuracy metrics
- file_format_is TSV with columns for method name, dataset identifier, and clustering accuracy metric (e.g., ARI, NMI, or purity score)
- verify that the table row_count_equals at least 3 for chromVAR variants (including kmers+PCA variant) and at least 1 row for SnapATAC, across at least 2 datasets
- value_in_range: clustering accuracy scores are between 0 and 1 (or 0–100 if percentage-scaled); no canonical answer for absolute thresholds since multiple accuracy metrics exist
- verify that SnapATAC row values are numerically greater than or equal to baseline chromVAR rows for the same dataset (robust to metric choice if direction is consistent)
- verify that chromVAR kmers+PCA variant row has the highest or tied-highest accuracy among all chromVAR variants for each dataset, parameter-sensitive to which datasets are included

## Expert Review

- confirm that the retrieved table matches the summary statement 'SnapATAC outperforms chromVAR for clustering' by inspecting whether SnapATAC values exceed chromVAR baseline across all reported datasets
- confirm that the retrieved table supports 'kmers+PCA is the best chromVAR variant' by verifying that kmers+PCA consistently achieves equal or superior clustering accuracy versus other chromVAR approaches (e.g., plain chromVAR, chromVAR+other feature engineering)
- assess whether the table structure and metric definitions are consistent with standard clustering evaluation practice (e.g., higher values indicate better clustering, metric is invariant to label permutation)
