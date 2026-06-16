# Evaluation Strategy

## Direct Checks

- verify file exists: airway dataset accessible via library('airway'); data('airway')
- verify script runs: R code to load airway data, run DESeq(), call results() with default independent filtering enabled, and extract filtered gene count
- verify file_format_is: results object from results() is a DESeqResults class with columns: baseMean, log2FoldChange, lfcSE, stat, pvalue, padj
- value_in_range: number of genes after independent filtering is less than total genes in airway dataset (robust to parameter choices)
- verify script runs: apply IHW-based p-value adjustment using ihw() function from IHW package on results object p-values
- verify output_matches_reference: filtered gene count and adjusted p-value columns from results() match expected behavior described in DESeq2 vignette section on independent filtering (robust to parameter-sensitive threshold details)
- value_in_range: padj column contains NA values for filtered-out genes and numeric adjusted p-values in [0,1] for retained genes

## Expert Review

- verify that independent filtering threshold selection (based on mean normalized counts) aligns with the theoretical justification for filtering low-count genes in RNA-seq differential expression analysis
- verify that IHW adjustment produces p-value ordering and rejection set behavior consistent with its intended multiple-testing control under dependence on filter statistic
- verify that the intersection of genes retained by results() independent filtering and those assigned adjusted p-values via IHW represents a valid subset for downstream interpretation
