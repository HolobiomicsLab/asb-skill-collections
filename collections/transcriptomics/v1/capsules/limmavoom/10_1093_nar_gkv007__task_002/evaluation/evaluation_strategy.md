# Evaluation Strategy

## Direct Checks

- verify that a GEO accession identifier or public microarray dataset URL is retrievable and contains valid expression matrix data
- verify that limma package (from github:bioc__limma or CRAN) can be loaded in R environment
- verify that lmFit function executes without error when passed (i) a valid expression matrix or ExpressionSet object as input, (ii) a design matrix of appropriate dimensions
- verify that lmFit returns an object of class MArrayLM containing at least the following fields: coefficients (matrix), stdev.unscaled (matrix), sigma (numeric vector)
- verify that coefficients matrix has dimensions matching (number of probes/genes) × (number of design matrix columns)
- verify that stdev.unscaled and sigma have lengths and dimensions consistent with the fitted model
- verify that no NA or NaN values appear in coefficients matrix where data were present in input expression matrix (robust to biological zero-inflation)

## Expert Review

- confirm that design matrix specification is appropriate for the experimental design of the chosen GEO dataset (e.g., matches sample groupings, block structure, or paired design if applicable)
- confirm that coefficient estimates and standard errors are statistically interpretable (e.g., standard errors are positive, coefficients do not show implausible magnitudes relative to the scale of expression values)
- confirm that the MArrayLM object is suitable as input for downstream empirical Bayes shrinkage functions (e.g., eBayes) without requiring additional transformation or filtering
