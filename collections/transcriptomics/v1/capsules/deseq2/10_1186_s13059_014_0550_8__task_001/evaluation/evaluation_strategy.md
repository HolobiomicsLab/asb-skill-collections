# Evaluation Strategy

## Direct Checks

- verify file exists: airway dataset loaded from airway R package via library('airway'); data('airway')
- script_runs: DESeq2 pipeline executes without error on airway dataset with commands: dds <- DESeqDataSet(airway); dds <- DESeq(dds); res <- results(dds, contrast=c('condition','treated','untreated'), alpha=0.1)
- value_in_range: number of genes with padj < 0.1 is a non-negative integer
- output_matches_reference: count of significant genes (padj < 0.1) from treated-vs-untreated contrast reproducible across independent runs with identical parameter settings (robust to random seed where applicable)

## Expert Review

- statistical validity: verify that DESeq2 was called with correct default parameters (negative binomial GLM, standard dispersion estimation, independent filtering enabled by default in results() function)
- contrast specification: confirm treated-vs-untreated contrast is correctly specified and that reference level ordering matches reported analysis
- FDR control: verify that alpha=0.1 threshold is applied to adjusted p-values (padj) rather than raw p-values, and that independent filtering does not artificially inflate or suppress significant gene count
