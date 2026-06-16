# Evaluation Strategy

## Direct Checks

- verify that the bittremieux/GNPS_GC repository is accessible at github.com/bittremieux/GNPS_GC
- verify file_exists: deconvolved output file (MGF or mzML format) produced by MSHub deconvolution step
- verify file_format_is: output file matches declared format (MGF or mzML), byte-for-byte structural validation
- verify that raw GC-MS input files are present and loadable in the companion repository or deposited dataset
- verify script_runs: MSHub deconvolution module executes without fatal errors on supplied raw GC-MS files
- verify output_matches_reference: deconvolved spectra file contains expected spectrum records (no canonical answer — multiple valid deconvolution outcomes defensible depending on algorithm parameters), robust to parameter choices

## Expert Review

- assess whether deconvolved spectra are chemically and spectroscopically valid (mass-to-charge assignments, peak intensities, baseline correction quality)
- evaluate whether MSHub deconvolution settings and parameters are appropriate for the GC-MS data type and chemical analytes
- confirm that deconvolution removes or separates co-eluting compounds and resolves overlapping peaks as intended
