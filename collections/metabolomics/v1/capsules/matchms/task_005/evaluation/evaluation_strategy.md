# Evaluation Strategy

## Direct Checks

- verify file_exists: Python environment with pip and/or conda available
- script_runs: `pip install matchms` completes without error exit code
- script_runs: `python -c 'import matchms'` executes without ImportError or exception
- script_runs: `conda install -c bioconda matchms` completes without error exit code (if conda/bioconda accessible)
- script_runs: `python -c 'import matchms; print(matchms.__version__)'` returns a non-empty version string
- value_in_range: installed matchms version matches or is compatible with current release tag from github.com/matchms/matchms/releases
- contains_substring: matchms module namespace contains expected submodules (e.g., 'matchms.importing', 'matchms.filtering', 'matchms.similarity')

## Expert Review

- Confirm that PyPI package metadata and Bioconda recipe are correctly synchronized and point to the same upstream source
- Assess whether any warnings or deprecation notices emitted during import are acceptable for the current release cycle
