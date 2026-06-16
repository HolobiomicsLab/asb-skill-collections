# Evaluation Strategy

## Direct Checks

- verify file exists: SpectriPy package installation succeeds in R environment (script_runs: installation command from github:rformassspectrometry__SpectriPy completes without error)
- verify script_runs: R script that loads SpectriPy library, creates a Spectra object, and calls at least one wrapped Python MS function executes without error
- verify output_matches_reference: returned object from Python MS function call is an R-native object (not raw Python object or serialization artifact)
- verify field_present: R object returned from wrapped Python function call contains at least one expected attribute or field matching the documented Python function output schema

## Expert Review

- assess whether the wrapped Python MS function call produces chemically/statistically valid results consistent with the underlying Python package documentation
- evaluate whether the R-native result format correctly preserves semantic meaning and data integrity from the Python function output
