# Evaluation Strategy

## Direct Checks

- verify that edgeR package is available in the computational environment (script_runs check: attempt to load edgeR library)
- verify that limma package is available and loadable from github:bioc__limma (script_runs check: load limma library)
- verify that a public RNA-seq dataset can be retrieved and loaded (file_exists check for dataset artifact or accession identifier)
- verify that calcNormFactors function from edgeR executes without error on the input dataset (script_runs check)
- verify that voom function accepts TMM-normalized library sizes as input and produces a voom object (script_runs check: output_matches_reference structure)
- verify that the extended pipeline (edgeR calcNormFactors → voom → limma workflow) completes and produces a top-table output file (file_exists and format_is checks)
- verify that the baseline limma-only pipeline (without edgeR prepend) also completes on the same dataset and produces a comparable top-table (file_exists and format_is checks)
- verify that both top-tables have identical or near-identical structure (row_count_equals and field_present checks for gene identifiers, log-fold-change, adjusted p-values)
- robust comparison: calculate rank correlation (Spearman or similar) between log-fold-change columns of extended vs. baseline pipelines, value in range [−1, 1]

## Expert Review

- Assess whether observed differences in top-table rankings (gene order, adjusted p-value thresholds) are biologically meaningful or expected given TMM normalization theory
- Evaluate whether the choice of public RNA-seq dataset is representative (e.g., sample size, sequencing depth, biological context) for a fair comparison
- Judge whether the comparison accounts for known behavior of TMM normalization vs. other limma defaults in this context
- Review whether the prepended edgeR step introduces any violations of limma's statistical assumptions or downstream function requirements
