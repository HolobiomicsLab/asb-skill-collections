# Evaluation Strategy

## Direct Checks

- verify file tximportData (or equivalent salmon_gibbs inferential replicate output) exists and is loadable
- verify tximport function accepts txOut=TRUE parameter without error
- verify edgeR::DGEListFromTximport function accepts divide=TRUE parameter without error
- verify output object is of class 'DGEList' (format_is DGEList)
- verify DGEList contains 'counts' matrix field (field_present counts)
- verify DGEList contains 'samples' data.frame with sample metadata (field_present samples)
- verify counts matrix dimensions are consistent with input (row_count_equals and column count match transcript/sample structure)
- verify script_runs: complete R code path from tximport(txOut=TRUE) → edgeR::DGEListFromTximport(divide=TRUE) without error
- verify output_matches_reference: DGEList structure mirrors edgeR documentation for transcript-level DGEList objects created from tximport with divide=TRUE

## Expert Review

- confirm that count overdispersion estimates (tagwise.dispersion or common.dispersion fields if present post-estimation) are numerically reasonable and consistent with RNA-seq count variance expectations
- confirm that division of counts by inferential replicate uncertainty (when divide=TRUE is applied) produces a DGEList suitable for proper downstream variance modeling in transcript-level edgeR analysis
