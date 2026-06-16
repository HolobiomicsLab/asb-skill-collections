# Evaluation Strategy

## Direct Checks

- verify that SUPPA2 PSI subcommand accepts transcript-level quantification file (Salmon or kallisto format) as input
- verify that SUPPA2 PSI subcommand accepts ioe or ioi event definition file as input
- verify that SUPPA2 PSI subcommand produces a PSI matrix file as output
- verify output file exists and is in a structured tabular format (TSV, CSV, or similar)
- script_runs: execute SUPPA2 PSI calculation on example transcript quantification and event files from github:comprna__SUPPA repository, solution_space: multiple valid test datasets may exist
- verify PSI values in output matrix are numeric and fall within valid range [0, 1]
- verify output matrix row count equals number of events in input ioe/ioi file
- verify output matrix column count equals number of samples in input quantification file

## Expert Review

- assess whether PSI calculation correctly aggregates transcript-level abundances to event-level splicing ratios according to the SUPPA2 methodological definition
- evaluate numerical accuracy of PSI values against reference calculations or published benchmark results
- review whether output matrix structure and annotation fields (event identifiers, sample identifiers) are correctly labeled and match input metadata
