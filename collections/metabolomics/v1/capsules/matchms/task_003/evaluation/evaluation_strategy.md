# Evaluation Strategy

## Direct Checks

- verify that a Python script using matchms.similarity.cosine can be executed on the input spectra file without errors
- verify that the output scores matrix file exists and has .npy, .csv, or .pkl format
- verify that the scores matrix has shape (N, N) where N equals the number of spectra in the input file
- verify that all values in the scores matrix are in the range [0.0, 1.0] (cosine similarity bounds)
- verify that the scores matrix is symmetric (i.e., scores[i,j] == scores[j,i] for all i,j)
- verify that the diagonal of the scores matrix equals 1.0 (self-similarity), byte-for-byte or within numerical precision (±1e-6)
- script_runs: execute a minimal matchms cosine similarity workflow (import Spectrum, CosineGreedy/CosineHungarian, compute pairwise similarities) on reference spectra from matchms repository without runtime errors

## Expert Review

- assess whether the cosine similarity implementation correctly weights peak intensities and mass-to-charge ratios according to the Cosine/CosineGreedy algorithm specification
- assess whether the choice of cosine variant (CosineGreedy, CosineHungarian, or ModifiedCosine) is justified and documented for the use case
- assess whether preprocessing/normalization of input spectra (if applied before cosine scoring) is appropriate and does not artificially inflate or suppress similarity values
