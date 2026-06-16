# Evaluation Strategy

## Direct Checks

- verify file exists in glasgowcompbio/PALS repository containing PLAGE implementation
- verify input metabolite intensity matrix file format is compatible (CSV, TSV, or matrix-like structure)
- verify pathway database input file format is compatible (JSON, CSV, or standard pathway annotation format)
- verify output pathway activity scores table contains at least one column for pathway identifiers and one column for activity scores
- verify output table has row_count_equals number of rows matching number of pathways in input database
- script_runs: execute PLAGE decomposition step on sample metabolite matrix and pathway database without errors
- output_matches_reference: verify output pathway activity scores are mathematically consistent with singular value decomposition applied to pathway-specific metabolite submatrices (requires expert verification of calculation logic)
- verify output table contains field for pathway ranking or sorting by activity score magnitude

## Expert Review

- assess whether PLAGE decomposition step correctly implements singular value decomposition on pathway-stratified metabolite intensity submatrices
- evaluate whether pathway activity level scores are appropriately normalized and scaled for downstream comparison
- verify that the ranked pathway results table is interpretable and that ranking order reflects biological relevance of pathway activity differences
- confirm that output scores handle edge cases appropriately (pathways with single metabolite, pathways with all zero intensities, missing data in matrix)
