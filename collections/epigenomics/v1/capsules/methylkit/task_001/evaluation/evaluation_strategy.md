# Evaluation Strategy

## Direct Checks

- verify file_exists: input CpG text files in package example data directory
- verify script_runs: R code executing unite() on methylRawList object without errors
- verify script_runs: R code executing calculateDiffMeth() on united methylBase object without errors
- verify script_runs: R code executing getMethylDiff() with q-value < 0.01 and 25% difference threshold parameters without errors
- verify output_matches_reference: methylDiff object row count for hyper-methylated bases matches vignette reported value (byte-for-byte exact match required)
- verify output_matches_reference: methylDiff object row count for hypo-methylated bases matches vignette reported value (byte-for-byte exact match required)
- verify field_present: methylDiff output object contains 'hyper' and 'hypo' annotation columns or equivalent slot structure

## Expert Review

- Confirm that the methylDiff object structure and content are consistent with methylKit's documented data model for differential methylation results
- Verify that q-value filtering at threshold 0.01 and 25% methylation difference threshold are correctly applied and produce biologically plausible hyper- vs. hypo-methylated base distributions
