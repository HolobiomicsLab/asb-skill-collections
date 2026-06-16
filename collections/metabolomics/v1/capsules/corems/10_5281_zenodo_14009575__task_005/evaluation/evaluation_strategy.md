# Evaluation Strategy

## Direct Checks

- Verify that a calibrated mass spectrum file exists in DS-001 dataset or CoreMS test data repository
- Verify that SearchMolecularFormulas function is callable from CoreMS package with parameters first_hit=True and first_hit=False
- Verify that summary table output file exists and is in tabular format (CSV or similar)
- Verify that summary table contains at least the following named columns: condition identifier, first_hit setting, assignment count, and score statistics (mean/median/std)
- Verify row_count_equals: summary table has exactly 2 data rows (one for COND-012 with first_hit=True, one for COND-013 with first_hit=False)
- Verify that score statistics values are numeric and in valid range for the algorithm's scoring scheme
- Verify script_runs: Python script executing both SearchMolecularFormulas calls completes without runtime errors

## Expert Review

- Assess whether the difference in formula assignment counts and score distributions between first_hit=True and first_hit=False modes is consistent with expected algorithmic behavior (greedy vs exhaustive search trade-offs)
- Evaluate whether score distributions (histograms or quantile summaries) reveal meaningful differences in assignment quality or confidence between the two modes
- Confirm that the same calibrated spectrum and molecular formula database were used for both COND-012 and COND-013 runs to ensure fair comparison
