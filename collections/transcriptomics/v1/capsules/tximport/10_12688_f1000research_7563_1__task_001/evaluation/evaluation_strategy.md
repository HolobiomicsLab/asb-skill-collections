# Evaluation Strategy

## Direct Checks

- verify file 'tx2gene.gencode.v27.csv' exists in tximportData package
- verify six salmon quant.sf.gz sample files exist in tximportData package
- script_runs: tximport function executes without error on the six salmon samples with tx2gene mapping
- output_matches_reference: counts matrix dimensions are consistent with gene count (rows) × sample count (columns)
- output_matches_reference: abundance matrix dimensions are consistent with gene count (rows) × sample count (columns)
- output_matches_reference: length matrix dimensions are consistent with gene count (rows) × sample count (columns)
- verify counts matrix contains non-negative numeric values
- verify abundance matrix contains non-negative numeric values
- verify length matrix contains positive numeric values

## Expert Review

- verify that the three returned matrices (counts, abundance, length) are biologically plausible for RNA-seq transcript aggregation, robust to parameter choices
- verify that length-corrected counts appropriately account for differential isoform usage across samples
