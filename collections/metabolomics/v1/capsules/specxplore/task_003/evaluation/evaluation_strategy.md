# Evaluation Strategy

## Direct Checks

- Verify that kevinmildau/specXplore repository is accessible on GitHub and contains source code for t-SNE embedding pipeline
- Verify that ms2deepscore package is importable and callable from the specXplore codebase
- Verify that output file exists and is in a standard 2-D coordinate format (CSV, TSV, NPY, or similar)
- Verify output file contains exactly two numeric columns (or equivalent structured representation of 2-D coordinates)
- Verify that coordinate values are within plausible t-SNE range (typically [-100, 100] or similar bounded space), robust to different random seeds
- Verify that the number of rows in output coordinates matches the number of input spectra

## Expert Review

- Expert judgment on whether t-SNE hyperparameters (perplexity, learning rate, n_iter) are documented and appropriate for mass spectral dataset size
- Expert judgment on whether the embedding quality is sufficient to visually separate spectrally distinct compounds and cluster similar spectra
- Expert judgment on whether ms2deepscore distance metric is correctly applied as input to t-SNE (e.g., whether it is used as a precomputed distance matrix or similarity is converted to distance)
- Expert judgment on reproducibility: whether random seed is fixed or documented such that embeddings can be regenerated with equivalent structure
