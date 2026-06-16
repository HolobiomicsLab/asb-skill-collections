# Evaluation Strategy

## Direct Checks

- verify that exportPeakMatrixForSTREAM function exists in github:GreenleafLab__ArchR repository
- verify that the function is callable within R environment with ArchR package loaded
- verify that output file exists and has a matrix-like format (csv, tsv, or HDF5)
- verify output contains row names (peaks) and column names (cells), robust to different delimiters
- verify that peak identifiers follow standard genomic interval notation (chr:start-end), parameter-sensitive to coordinate format
- verify that cell identifiers match input ArchR project cell barcodes
- verify that matrix values are numeric and represent chromatin accessibility scores, no canonical answer on expected value ranges across datasets

## Expert Review

- confirm that exported matrix dimensions and content structure are compatible with STREAM input requirements based on STREAM documentation
- confirm that peak-by-cell matrix encoding (sparse vs. dense, normalization approach) matches STREAM specifications for trajectory inference
- confirm that cell ordering and peak filtering (if any) are appropriate for downstream STREAM analysis
