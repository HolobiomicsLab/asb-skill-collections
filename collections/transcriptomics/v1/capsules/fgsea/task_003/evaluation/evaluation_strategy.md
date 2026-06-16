# Evaluation Strategy

## Direct Checks

- verify that GSE200250 expression matrix can be loaded from GEO using GEOquery
- verify that PCA reduction to 10 dimensions produces a numeric matrix with 10 columns
- verify that geseca() function runs without error on the PCA-reduced matrix with compatible pathway input
- verify that geseca() output on reduced matrix contains pathway scores (NES or similar numeric field)
- verify that geseca() output on reduced matrix contains p-values (padj or pval field)
- verify that pathway scores from reduced-matrix run are within 0.5 absolute units of full-matrix scores (parameter-sensitive; requires establishing baseline full-matrix results first)
- verify that p-values from reduced-matrix run are within 0.05 absolute difference of full-matrix p-values (parameter-sensitive; requires establishing baseline full-matrix results first)

## Expert Review

- evaluate whether score and p-value differences between full-matrix and PCA-reduced runs are biologically acceptable given the dimensionality reduction
- assess whether the choice of 10 PCA dimensions preserves sufficient variance for meaningful pathway inference
- judge whether similarity thresholds (0.5 for scores, 0.05 for p-values) are appropriate benchmarks or require adjustment based on statistical properties of the data
