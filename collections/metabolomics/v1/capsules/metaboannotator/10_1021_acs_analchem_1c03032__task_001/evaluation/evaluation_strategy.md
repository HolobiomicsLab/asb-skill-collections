# Evaluation Strategy

## Direct Checks

- verify file targetTable.csv exists in the repository
- verify file_format_is targetTable.csv a valid CSV with at least 6 rows (features)
- verify that xcmsSet (xset) object file exists in the repository or is loadable from the package
- verify that RAMClustR (RC) object file exists in the repository or is loadable from the package
- verify that LipidPos library files are present or accessible within the MetaboAnnotatoR package
- script_runs: annotateRC function executes without error when called on targetTable.csv, xset, RC, and LipidPos libraries
- output_matches_reference: annotateRC produces exactly 3 annotated features (no more, no fewer)
- output_matches_reference: feature 3 is assigned LPC(14:0) as the rank-1 (top-ranked) annotation
- value_in_range: annotation confidence/score for the three features meets expected thresholds (requires parameter-sensitive specification of score cutoff)

## Expert Review

- Assess whether the three annotated features and their ranked assignments are chemically and metabolomically plausible given the input xcms peak-picking and RAMClustR pseudo-MS/MS spectra
- Verify that LPC(14:0) assignment to feature 3 is consistent with expected fragment ion patterns and mass accuracy for a lipid of that composition
- Confirm that the four unannotated features represent genuine metabolites or artifacts that appropriately fall below the annotation threshold
