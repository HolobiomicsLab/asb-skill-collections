# Evaluation Strategy

## Direct Checks

- verify file exists: airway dataset accessible via R library('airway'); data('airway')
- verify script_runs: R script executing DESeq() on airway dds object completes without error
- verify script_runs: lfcShrink(dds, coef='condition_trt_vs_untrt', type='apeglm') executes and returns results object
- verify script_runs: lfcShrink(dds, coef='condition_trt_vs_untrt', type='normal') executes and returns results object
- verify script_runs: lfcShrink(dds, coef='condition_trt_vs_untrt', type='ashr') executes and returns results object
- verify field_present: each output results object contains columns 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'
- verify value_in_range: log2FoldChange values are numeric and finite (no NaN/Inf) for all three shrinkage estimators
- verify output_matches_reference: shrunken LFC tables for treated-vs-untreated contrast match reported summaries in article text or supplementary materials (multiple defensible approaches to exact match tolerance)
- verify robust to parameter choices: shrinkage results are reproducible across DESeq2 version compatibility within same major release

## Expert Review

- Assess whether shrinkage magnitude (reduction in log2FoldChange from unshrunk to shrunken estimates) is biologically plausible and consistent with expected behavior of each estimator (apeglm, normal, ashr)
- Evaluate whether the three shrinkage estimators produce qualitatively similar ranking of genes by effect size, or whether differences reflect expected estimator properties
- Confirm that reported p-values and adjusted p-values after shrinkage are appropriate (should remain unchanged or reflect only reordering, not recomputation)
- Verify that the treated-vs-untreated contrast is correctly specified (reference level 'untreated', compared against 'treated')
