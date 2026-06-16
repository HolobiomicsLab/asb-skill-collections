# Evaluation Strategy

## Direct Checks

- verify file exists: GSE116240 dataset accessible via GEOquery at https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE116240
- verify script_runs: R script loads GSE116240 data using GEOquery::getGEO() without errors
- verify script_runs: Seurat SCTransform normalization completes on GSE116240 expression matrix
- verify script_runs: fgsea::geseca() executes with KEGG_LEGACY pathway collection and GSE116240 SCTransform-normalized data without errors
- verify output_matches_reference: KEGG_LEISHMANIA_INFECTION pathway appears in geseca results table with non-foamy intimal macrophage cell type assignment
- verify output_matches_reference: KEGG_LYSOSOME pathway appears in geseca results table with foamy macrophage cell type assignment
- verify field_present: geseca output table contains columns for pathway name, cell type annotation, and enrichment statistic

## Expert Review

- confirm that KEGG_LEISHMANIA_INFECTION association with non-foamy intimal macrophages is biologically plausible given known pathogen-response gene signatures
- confirm that KEGG_LYSOSOME specificity to intimal foamy macrophages is consistent with lipid catabolism and foam cell biology
- assess whether SCTransform normalization parameters and geseca settings (minSize, maxSize, other hyperparameters) are appropriate for single-cell RNA-seq data and KEGG_LEGACY pathway collection
- evaluate whether cell type annotations in GSE116240 are sufficiently granular and accurate to support macrophage subtype-specific enrichment claims
