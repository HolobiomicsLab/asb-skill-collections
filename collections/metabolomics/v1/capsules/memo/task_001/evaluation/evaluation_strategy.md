# Evaluation Strategy

## Direct Checks

- verify that the implementation accepts MS2 spectra files as input (file_format_is: common MS formats such as .mgf, .msp, or .mzML)
- verify that the implementation produces a numeric fingerprint vector output for each sample (format_is: numeric array or matrix, e.g., numpy array, CSV, or HDF5)
- verify that the fingerprint vector contains counts of MS2 peaks and neutral losses (field_present: vector entries represent peak/loss counts; robust to parameter choices for binning or filtering thresholds)
- verify that output fingerprint dimensions match the number of input samples (row_count_equals: one fingerprint per sample)
- script_runs: execute the MS2_FINGERPRINT_COMPONENT on a reference MS2 spectra dataset (e.g., from mandelbrot-project/memo_publication_examples) without errors
- output_matches_reference: compare generated fingerprints against documented reference fingerprints (if available in the publication examples repository) byte-for-byte or within documented numerical tolerance

## Expert Review

- assess whether peak and neutral loss counting methodology aligns with MS2 fragmentation mass spectrometry best practices and the MEMO publication intent
- evaluate whether the fingerprint vector dimensionality and binning strategy are appropriate for downstream alignment and sample comparison tasks
- review whether handling of precursor ions and neutral loss calculations is biochemically sound
