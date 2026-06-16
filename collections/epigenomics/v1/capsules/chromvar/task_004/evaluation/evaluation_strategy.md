# Evaluation Strategy

## Direct Checks

- verify that input is a chromVARDeviations object (or SummarizedExperiment with deviation assays) loadable from the chromVAR package
- verify that getAnnotationCorrelation function executes without error on the input object
- verify that getAnnotationSynergy function executes without error on the input object
- file_format_is: correlation matrix output file (CSV, TSV, or RDS format)
- file_format_is: synergy score table output file (CSV, TSV, or RDS format)
- field_present: correlation matrix contains row and column labels corresponding to annotation sets
- field_present: synergy score table contains columns for annotation pair identifiers and numeric synergy scores
- value_in_range: correlation coefficients in output matrix are between −1.0 and +1.0
- value_in_range: synergy scores are numeric (verify absence of NA/NaN where data should be present), robust to parameter choices in function calls

## Expert Review

- evaluate whether correlation matrix and synergy scores are biologically plausible given the annotation sets used (e.g., JASPAR motifs vs. kmers)
- assess whether high correlation or synergy values correspond to expected redundancy or complementarity between the two annotation modalities
- verify that the choice of correlation metric and synergy computation method are appropriate for the sparse accessibility data context
