# Evaluation Strategy

## Direct Checks

- verify file pyteomics exists after pip installation (package directory or site-packages location)
- script_runs: execute 'python -c "import pyteomics.mass; import pyteomics.pepxml; import pyteomics.mzid; import pyteomics.tandem; import pyteomics.auxiliary"' and confirm exit code is 0
- verify no ImportError or ModuleNotFoundError is raised during core module imports
- verify each of the five core modules (pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, pyteomics.auxiliary) is accessible as a Python importable object after installation

## Expert Review

- confirm that installed version of Pyteomics is compatible with the versions of declared dependencies (numpy, lxml, matplotlib, pandas, sqlalchemy, pynumpress) present in the environment
