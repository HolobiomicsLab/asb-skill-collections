# Evaluation Strategy

## Direct Checks

- verify that a README or documentation file exists in the repository adelabriere/SLAW or zamboni-lab/SLAW that describes the MS2 spectra and isotopic data extraction step
- verify that the repository contains executable code (Python, R, or other language) implementing the extraction module that consolidates MS2 spectra per feature group
- verify that example output files or schema documentation exist that define the structure of the consolidated MS2 spectra output (format specification: CSV, TSV, HDF5, or other structured format)
- file_exists: a named output artifact from the extraction step (e.g., 'consolidated_ms2_spectra.csv', 'feature_ms2_data.tsv', or equivalent) in test data or example outputs
- script_runs: the extraction module executes without error on provided example LC-MS input files (format: mzML, mzXML, or raw vendor formats supported by the workflow)

## Expert Review

- evaluate whether the consolidation logic correctly groups MS2 spectra across all replicates for the same feature group (isotopologue + adduct identity)
- evaluate whether the isotopic data extraction accurately captures natural abundance isotope ratios and their variance across samples
- assess whether the output format and data organization align with standard metabolomics feature table conventions and downstream analysis requirements
- review the handling of missing MS2 data (e.g., when MS2 is absent for a feature in some samples) and whether consolidation strategy is statistically sound
