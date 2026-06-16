# Evaluation Strategy

## Direct Checks

- verify that S1 Data, S2 Data, S3 Data, and S4 Data files (containing high-scoring links from Crüsemann, Leão, and Gross datasets) are present in the supplementary materials
- verify that the reported combined score formula s'₁/p = sgn(s'_corr)|s'_corr|^(1/p) + sgn(s'_IOKR)|s'_IOKR|^(1/p) is correctly implemented in NPLinker source code (zenodo.org/record/4680579) or referenced supplementary code
- value_in_range: confirm that p values tested in sensitivity analysis span at least the range [0.5, 1.0, 2.0, 4.0] or comparable exponents, with documentation of which values were evaluated
- value_in_range: confirm that validated-link ratio (proportion of validated links among top-scoring links at 90th percentile or equivalent threshold) is reported for each combination function variant, with ratios between 0 and 1
- output_matches_reference: for any combination function form reported, verify that the enrichment p-value and validated-link count matches the corresponding entry in Table 2 or supplementary tables for the baseline case (p=0.5 or equivalent baseline exponent)
- file_exists: verify presence of a supplementary table, figure, or dataset file reporting systematic variation of p and alternative combination functions with corresponding enrichment metrics
- script_runs: verify that a reproducible script or Jupyter notebook exists (in the NPLinker repository or supplementary materials) that accepts the precomputed IOKR and standardised strain correlation score outputs and produces the sensitivity analysis outputs without requiring re-computation of IOKR or strain correlation scores

## Expert Review

- Assess whether the choice of alternative combination function forms (beyond ℓp-norm) is mathematically sound and biologically justified—e.g., weighted linear combinations, geometric means, other norms
- Evaluate whether the reported sensitivity trend (validated-link ratio as a function of p) is consistent across the three datasets (Crüsemann, Leão, Gross) and whether any deviation is explained or flagged
- Judge whether the span of p values and combination functions tested is sufficiently comprehensive to characterize the sensitivity landscape, or whether critical parameter regimes may have been missed
- Review whether the authors discuss or acknowledge limitations in extrapolating sensitivity findings to untested product classes or datasets beyond the three reported microbial strains
