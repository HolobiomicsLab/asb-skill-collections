# Evaluation Strategy

## Direct Checks

- verify file exists: chromVAR package installed and loadable via library(chromVAR)
- verify script_runs: R script calling computeVariability on chromVARDeviations object from 10-GM / 10-H1 example dataset completes without error
- verify script_runs: R script calling differentialDeviations to test GM vs H1 group differences completes without error
- verify output_matches_reference: ranked variability table contains per-motif variability scores; row_count_equals at least one row per tested motif
- verify output_matches_reference: differential-deviation results table contains per-motif test statistics (p-values, effect sizes, or equivalent); structure matches reported statistics in article or supplementary material
- verify field_present: both output tables include motif identifiers (name or ID column)
- verify field_present: variability table includes numeric rank or score column; differential results table includes numeric test statistic column

## Expert Review

- Verify that motif ranking by variability score is biologically plausible given the 10-GM / 10-H1 cell populations (genomics domain expertise required)
- Verify that GM vs H1 differential-deviation test results are consistent with expected cell-type-specific transcription factor usage patterns (domain expertise required)
- Assess whether reported per-motif statistics in article or SI match the computational outputs in magnitude and direction (statistical and biological interpretation)
