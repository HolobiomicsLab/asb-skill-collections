# Evaluation Strategy

## Direct Checks

- verify that input MemoMatrix file exists and is loadable by memo-ms package
- verify that output coordinate table contains at least 2 columns (for 2D embedding) and one row per input sample
- verify that output scatter plot file exists in a standard image format (PNG, PDF, or SVG)
- verify that scatter plot contains plotted points corresponding to each sample in the coordinate table
- verify that the embedding method used (MDS or PCoA) is correctly identified in output metadata or plot labels
- verify output matches reference implementation by comparing embedding coordinates to a reference deposit (if available) with robust tolerance for numerical precision (e.g., within 1% variance explained)

## Expert Review

- expert judgment on whether the 2D embedding preserves meaningful sample relationships and separations evident in the original high-dimensional MemoMatrix
- expert judgment on whether the choice between MDS and PCoA is appropriate for the sample collection and biological question being addressed
