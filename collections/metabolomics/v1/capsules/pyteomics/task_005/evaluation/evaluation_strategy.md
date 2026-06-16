# Evaluation Strategy

## Direct Checks

- verify conda is available and executable in the agent's environment
- verify Bioconda channel is accessible and queryable
- script_runs: conda install -c bioconda pyteomics completes without error
- file_exists: verify Python site-packages contains pyteomics directory after installation
- script_runs: Python script imports pyteomics.mass, pyteomics.pepxml, pyteomics.mzid without ImportError
- output_matches_reference: verify each module import returns a module object with __name__ attribute matching the expected module path

## Expert Review

- Assess whether the installed version and dependency resolution from Bioconda matches upstream source (github:levitsky/pyteomics) in functionality for the three tested modules
- Confirm that no runtime errors or missing optional dependencies prevent the three core module imports from succeeding in a clean conda environment
