# Evaluation Strategy

## Direct Checks

- verify file exists in tximportData package: path matching '*SG-Nex*oarfish*.quant.gz' for three replicates
- script_runs: tximport() call with type='oarfish' and txOut=TRUE completes without error
- output_matches_reference: returned object is a list containing exactly three named elements: 'abundance', 'counts', 'length'
- file_format_is: each matrix in output (abundance, counts, length) is numeric matrix or data.frame with rows=transcripts, columns=samples
- row_count_equals: transcript-level matrix row count matches number of unique transcript IDs in input oarfish quant.gz files
- value_in_range: all abundance values are non-negative; all count values are non-negative integers; all length values are positive
- field_present: output object contains no gene-level aggregation (txOut=TRUE was honored, not summarized to genes)

## Expert Review

- oarfish quantification format (quant.gz structure and field semantics) is correctly parsed by tximport type='oarfish' handler
- transcript-level abundance, count, and length estimates from oarfish are biologically reasonable for SG-Nex RNA-seq data
- matrix dimensions and values are consistent with typical transcript-level quantification from short-read RNA-seq
