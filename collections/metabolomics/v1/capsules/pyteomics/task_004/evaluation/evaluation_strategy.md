# Evaluation Strategy

## Direct Checks

- verify file exists: psims package installed and importable in Python environment
- script_runs: execute `python -c 'import pyteomics.proforma'` without error
- script_runs: execute `python -c 'from pyteomics.proforma import ProForma'` without error
- output_matches_reference: confirm ProForma class or parsing function is accessible in pyteomics.proforma namespace

## Expert Review

- Review whether ProForma notation parsing functionality is fully operational and not degraded by optional dependency wiring
- Assess whether psims installation correctly resolves conditional dependency chain for proforma component
