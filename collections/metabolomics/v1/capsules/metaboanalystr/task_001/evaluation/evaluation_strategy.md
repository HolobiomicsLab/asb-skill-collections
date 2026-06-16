# Evaluation Strategy

## Direct Checks

- verify that xia-lab/MetaboAnalystR repository is accessible and contains R package structure (DESCRIPTION, R/, man/ directories present)
- verify file_exists: R scripts or functions implementing LC-MS peak detection module
- verify file_exists: R scripts or functions implementing peak alignment module
- verify file_exists: R scripts or functions implementing feature table generation module
- verify file_exists: example or vignette demonstrating end-to-end workflow from raw spectral data input to feature table output
- script_runs: execute a minimal end-to-end workflow using provided example data (if present in repo) and confirm feature table output is generated in expected format (CSV, data.frame, or matrix)
- verify field_present: output feature table contains expected columns (m/z, retention time, intensity/abundance) — no canonical answer for exact column names; any schema that represents features with mass and temporal dimensions is acceptable
- verify file_format_is: final feature table output in standard rectangular format (CSV, TSV, or R data object)

## Expert Review

- assess whether peak detection algorithm implementation (e.g., centWave, matched filter, or equivalent) follows standard LC-MS metabolomics practices and produces chemically interpretable results
- assess whether peak alignment algorithm correctly handles retention time drift and m/z calibration across multiple samples
- assess whether feature table generation properly handles missing values, duplicate features, and isotope/adduct relationships in a way consistent with published metabolomics best practices
- assess overall fidelity of the implemented pipeline to stated LC-MS metabolomics workflow in MetaboAnalystR 4.0 title and documentation
