# Evaluation Strategy

## Direct Checks

- verify file 'example_counts' can be loaded from chromVAR package using data(example_counts, package = "chromVAR")
- verify assembleKmers function exists and is callable in chromVAR package
- verify computeDeviations function exists and is callable in chromVAR package
- verify 6-mer annotation matrix output file_format_is matrix or SummarizedExperiment
- verify 7-mer annotation matrix output file_format_is matrix or SummarizedExperiment
- verify numeric summary table contains fields for mean and median variability scores
- verify numeric summary table row_count_equals 2 (one row per kmer size: 6-mer and 7-mer)
- verify summary table field_present 'kmer_size' with values 6 and 7
- verify summary table field_present 'mean_variability' and 'median_variability' with numeric values
- verify output script_runs without errors in R environment with chromVAR, Matrix, SummarizedExperiment libraries loaded

## Expert Review

- confirm that reported direction of variability difference between 6-mers and 7-mers matches expected biological or statistical pattern documented in chromVAR literature or package vignette
- assess whether the magnitude of difference in variability scores between 6-mer and 7-mer distributions is scientifically meaningful for kmer-based annotation analysis
