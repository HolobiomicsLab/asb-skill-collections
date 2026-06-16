# Evaluation Strategy

## Direct Checks

- verify that matchms package is importable and contains a fingerprint-based similarity module
- verify that preprocessed spectra are available in the matchms repository (check for example datasets or test data files in common formats: .msp, .mgf, .json)
- verify that the fingerprint similarity function executes without runtime errors on a set of ≥2 preprocessed spectra
- verify that the output is a named matrix file (csv, tsv, or numpy format) with row and column count equal to number of input spectra
- verify that all pairwise similarity scores in the output matrix are numeric values in a valid range (typically [0, 1] for similarity measures)
- verify that the matrix is symmetric (or as expected for the specific fingerprint method used) by checking that score[i,j] matches score[j,i] where applicable
- verify that the output file exists and is readable in the declared format

## Expert Review

- confirm that the fingerprint similarity measure applied is chemically and computationally appropriate for mass spectrometry spectral comparison
- assess whether the pairwise similarity scores align with known fingerprint-based similarity properties (e.g., identical spectra should yield maximum similarity)
- review that the preprocessing applied to input spectra is consistent with matchms best practices for fingerprint-based workflows
