# Evaluation Strategy

## Direct Checks

- file_exists: verify that cooltools/lib module directory exists in the open2c/cooltools repository at the documented location
- script_runs: execute Python import statement `from cooltools.lib import adaptive_coarsegrain` and verify script completes without ImportError
- field_present: verify that adaptive_coarsegrain is listed in the __all__ export list or module __init__.py of cooltools.lib
- contains_substring: verify that the function signature and docstring are present in the source file containing adaptive_coarsegrain definition

## Expert Review

- confirm that adaptive_coarsegrain is semantically consistent with described functionality as a library utility for coarse-graining operations
- verify that the function's implementation and documentation align with standard Hi-C analysis practices for adaptive resolution adjustment
