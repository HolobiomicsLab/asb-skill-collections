# Evaluation Strategy

## Direct Checks

- verify that github:GreenleafLab__ArchR repository is accessible and contains ArchR package source code
- verify that ArchR package documentation or vignettes include functions importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, and addCombinedDims
- script_runs: execute a minimal R script that loads ArchR, calls importFeatureMatrix on a test scRNA-seq matrix, calls addGeneExpressionMatrix on a test ArchRProject with paired scATAC-seq data, calls addIterativeLSI, and calls addCombinedDims without errors
- verify that the R script output includes a ArchRProject object or SummarizedExperiment with dimensionality-reduction slots populated (e.g., containing LSI or combined embedding matrices)
- verify that the combined embedding produced has multiple dimensions (parameter-sensitive: exact dimensionality may vary by LSI iteration count, but must be ≥ 2)

## Expert Review

- assess whether the joint reduced-dimension embedding produced by addCombinedDims meaningfully integrates information from both scATAC-seq and scRNA-seq modalities (e.g., by examining correlation structure, variance explained, or cross-modality clustering concordance)
- evaluate whether the paired multiome workflow as implemented follows best practices for joint dimensionality reduction in the scATAC-seq and scRNA-seq literature
