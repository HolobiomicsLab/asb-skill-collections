# Evaluation Strategy

## Direct Checks

- verify file inst/extdata/msi.csv exists in github:kbseah__mass2adduct repository
- file_format_is: msi.csv is plain-text CSV with semicolon delimiter
- script_runs: R code `library(mass2adduct); d <- msimat(system.file('extdata','msi.csv',package='mass2adduct'),sep=';'); d.diff <- massdiff(d); d.diff.annot.cor <- corrPairsMSI(d.diff)` executes without error
- field_present: output data frame contains columns 'Estimate', 'P-value', and corrected significance field (e.g., 'adj.p' or similar)
- value_in_range: Estimate values are numeric correlations between -1 and 1
- value_in_range: P-value and corrected significance fields contain numeric values between 0 and 1
- output_matches_reference: corrected P-values are not smaller than uncorrected P-values (Bonferroni correction monotonicity check)

## Expert Review

- verify that Bonferroni correction was applied correctly: number of comparisons equals number of pairwise mass differences, and adjustment factor is appropriate
- assess whether Pearson correlation coefficients and their significance are biologically sensible given the MSI imaging context and expected spatial colocalization patterns
