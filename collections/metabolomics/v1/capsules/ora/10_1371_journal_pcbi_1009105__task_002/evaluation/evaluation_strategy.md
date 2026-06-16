# Evaluation Strategy

## Direct Checks

- verify file exists: github:cwieder__metabolomics-ORA repository is accessible and contains Jupyter notebook(s)
- file_format_is: notebook file(s) in repository use .ipynb extension
- script_runs: execute the simulation notebook(s) without errors on Python environment with dependencies installed
- field_present: output table or figure contains columns/axes representing metabolite coverage fraction, ORA p-values, and false-positive rates
- output_matches_reference: summary statistics table rows correspond to distinct coverage levels tested in simulation (robust to row ordering)
- contains_substring: notebook code cells contain logic that varies metabolite detection fraction as a parameter

## Expert Review

- evaluate whether the simulation framework appropriately models the relationship between metabolite coverage and ORA statistical performance
- assess whether the summary statistics table or figure meaningfully communicates how coverage affects false-positive rates and p-value distributions
- judge whether the experimental design (choice of coverage fractions, number of simulations, statistical metrics reported) follows best practices for pathway analysis validation
