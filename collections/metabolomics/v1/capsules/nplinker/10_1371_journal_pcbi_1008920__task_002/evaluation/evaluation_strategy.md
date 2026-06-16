# Evaluation Strategy

## Direct Checks

- verify file exists: NPLinker repository at https://github.com/sdrogers/nplinker or Zenodo deposit http://doi.org/10.5281/zenodo.4680579
- verify input dataset exists: GNPS training set with 4138 spectra (accessible via GNPS public library or supplementary data S1 Data)
- verify input dataset exists: MIBiG-GNPS paired dataset with 2966 validated BGC-spectrum links from S1 Data
- script_runs: IOKR model training pipeline on GNPS 4138-spectrum training set with default or specified kernel parameters completes without error
- file_exists and file_format_is: IOKR model checkpoint or serialized object (e.g., pickle, joblib, HDF5) produced after training
- script_runs: IOKR scoring script applied to 2966 MIBiG-GNPS BGC-spectrum pairs produces score matrix with shape (2966,) or equivalent
- file_format_is: output score vector is numeric array or table (CSV/TSV) with one score per pair, no missing values
- row_count_equals: output score table has exactly 2966 rows (one per BGC-spectrum pair)
- field_present: score table includes spectrum identifier, BGC identifier, and IOKR score columns
- value_in_range: IOKR scores are continuous values; robust to parameter choices (no exact byte-for-byte match required, kernel and fingerprint function choices may produce slightly different score distributions)
- output_matches_reference: reproduce histogram plot from S2 Fig showing IOKR score distribution with validated-link positions marked; check that validated-link positions are visibly enriched at higher scores relative to all-link distribution (no canonical answer for exact bin edges, but visual enrichment pattern must match figure)
- output_matches_reference: reproduce summary statistics from Table 3 or results text: mean IOKR score for all links ≈ 0.0105, mean for validated links ≈ 0.0364, p-value ≈ 1.7968 × 10⁻⁹ (robust to small numerical precision differences)
- output_matches_reference: reproduce top-n accuracy metrics from Table 3 (top-1: 0.1208, top-5: 0.1708, top-10: 0.1870, top-20: 0.2121, top-200: 0.2946, AUC: 0.6534), parameter-sensitive to model hyperparameters and kernel choice

## Expert Review

- verify that IOKR kernel function (Probability Product Kernel applied to molecular fingerprints) is correctly instantiated and hyperparameters match published method description in Methods or supplementary text
- verify that molecular fingerprint representation (type and dimensionality, e.g. Morgan, MACCS, or other) matches the published protocol
- verify that training set of 4138 spectra is correctly filtered (denoising step, peak filtering to training-set peaks only) before IOKR model training
- verify that scoring procedure correctly handles the 2966 MIBiG-GNPS pairs: each spectrum is matched against candidate set of BGC structures with MIBiG homology assignment
- expert assessment: enrichment of validated links in high-scoring region is statistically significant and visually consistent with S2 Fig distribution shape and marked positions
- expert assessment: IOKR score distribution shape, spread, and skewness are reasonable and consistent with reported mean and standard deviation estimates
