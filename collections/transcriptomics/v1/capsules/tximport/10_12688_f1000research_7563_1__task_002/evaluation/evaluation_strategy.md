# Evaluation Strategy

## Direct Checks

- verify file exists: tximportData salmon quantification files (input directory from github:thelovelab__tximport)
- verify file exists: tx2gene mapping object (tx2gene data.frame from tximportData or article SI)
- script_runs: execute tximport() with txOut=TRUE on salmon files and store result
- script_runs: execute summarizeToGene() on txOut=TRUE result using tx2gene mapping
- script_runs: execute tximport() with txOut=FALSE (default) on same salmon files
- output_matches_reference: verify count matrix from (txOut=TRUE + summarizeToGene) is byte-for-byte identical to count matrix from txOut=FALSE, robust to floating-point representation choices in matrix serialization
- file_format_is: both resulting count matrices are in standard R matrix or SummarizedExperiment format

## Expert Review

- verify that the tximport parameters (type, countsFromAbundance, etc.) match those used in the article's reported equivalence test
- assess whether numerical precision and rounding in the two pipelines are sufficiently aligned to justify claimed equivalence
