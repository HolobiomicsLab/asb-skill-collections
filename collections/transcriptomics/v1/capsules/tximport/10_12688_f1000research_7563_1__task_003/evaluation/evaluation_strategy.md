# Evaluation Strategy

## Direct Checks

- verify file tximportData salmon files exist in the package or referenced deposit
- script_runs: execute R code calling tximport() on salmon files to produce txi list object
- script_runs: execute R code calling DESeq2::DESeqDataSetFromTximport() with txi list and two-condition sample table
- verify DESeqDataSet object contains 'offset' matrix (field_present: object@assays[['offset']] or equivalent accessor)
- verify offset matrix dimensions match gene count matrix (row and column counts equal between counts and offset)
- verify offset matrix is numeric and finite (no NaN or Inf values), robust to numerical precision
- verify offset matrix derives from tximport length matrix (output_matches_reference: offset approximately equals log(length matrix) with standard DESeq2 transformation)

## Expert Review

- confirm offset matrix embedding method matches 'original counts and offset' approach described in Soneson et al. article
- confirm two-condition sample table specification is valid (correct column names, factor levels, sample counts)
- confirm DESeqDataSet construction did not discard or alter the offset information from tximport
- assess whether downstream DESeq analysis using this offset object produces sensible results (e.g., length bias correction is applied)
