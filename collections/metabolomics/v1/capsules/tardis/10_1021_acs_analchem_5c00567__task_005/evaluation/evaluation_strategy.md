# Evaluation Strategy

## Direct Checks

- verify that vignette mzML files exist in the package distribution
- verify that tardisPeaks() function accepts both MsExperiment object and file-path inputs
- verify that screening_mode parameter is accepted by tardisPeaks() function
- verify that output directory contains Diagnostic EIC PNG files after execution
- file_format_is: output files are PNG format
- verify that PNG files generated from MsExperiment object invocation exist in expected output directory
- verify that PNG files generated from file-path-based invocation exist in expected output directory
- robust comparison of PNG file dimensions, byte-for-byte matching not required due to potential compression variations

## Expert Review

- visual inspection and quantitative comparison of EIC chromatograms from MsExperiment-based vs. file-path-based invocations for equivalence in peak detection patterns, retention time accuracy, and ion intensity representation
- assessment of whether minor rendering differences (e.g., color profiles, font rendering, metadata) constitute meaningful divergence from expected reproducibility
