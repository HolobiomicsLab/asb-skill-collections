# Evaluation Strategy

## Direct Checks

- verify that inputs include a concrete TXT export file from Sciex Multiquant (> v3.0.3) containing QCpool positional table data
- verify that expected_outputs artifact exists and is a named file (CSV/TSV/PDF table or PNG/PDF figure)
- verify file_exists: the output report file in the specified format
- verify that output report contains at least one column or metric labeled 'CV' or 'coefficient of variation'
- verify that output report contains at least one column or metric labeled 'signal-trend' or equivalent trend metric across QCpool injections
- script_runs: QComics package executes without error on the provided TXT input and produces the report artifact

## Expert Review

- whether CV calculations are mathematically correct (standard deviation / mean × 100 or equivalent definition)
- whether signal-trend metric appropriately captures temporal or injection-order variation in QCpool signal intensity
- whether the per-compound metrics are aggregated or presented at appropriate granularity for a 'quality overview'
- whether the report layout and visualizations align with stated goal of providing 'quick overview of quality' for metabolomics/lipidomics studies
