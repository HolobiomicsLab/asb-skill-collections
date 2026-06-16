# Evaluation Strategy

## Direct Checks

- verify that inputs include a united methylBase object (output of unite() on example CpG files) or a concrete file path to such an object in the methylKit package repository
- verify that clusterSamples() function is callable on the methylBase object and produces a dendrogram object (class 'dendrogram' or equivalent hierarchical clustering structure)
- verify that PCASamples() function is callable on the methylBase object and produces at least two plot files in PNG or PDF format
- verify that the dendrogram object can be serialized and matches the visual structure described in the methylKit vignette (no canonical answer for exact tree topology, but structure must be reproducible from the same input)
- verify that the PCA scree plot file exists and contains variance explained per principal component
- verify that the PC1/PC2 scatter plot file exists and displays sample clustering in 2D space
- script_runs: both clusterSamples() and PCASamples() execute without error on the provided methylBase input
- file_format_is: output plot files are valid PNG or PDF (robust to file format choice)

## Expert Review

- visual inspection of dendrogram: confirm that hierarchical clustering structure is biologically plausible given the input methylation data (e.g., expected samples cluster together, no inverted relationships)
- visual inspection of PCA plots: confirm that the scree plot shows expected variance decay and that PC1/PC2 scatter reflects meaningful sample separation (no canonical answer; requires domain judgment of methylation patterns)
- confirm that clusterSamples() and PCASamples() implementations in the methylKit package match the documented behavior in the vignette
