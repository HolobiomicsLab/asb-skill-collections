# Evaluation Strategy

## Direct Checks

- file_exists: verify S1 Fig exists in supplementary materials or deposited package
- file_format_is: S1 Fig output format is PDF or PNG
- script_runs: NPLinker implementation of standardised strain correlation score (σ*_corr) executes without errors on Crüsemann, Gross, and Leão datasets from Paired Omics Data Platform
- output_matches_reference: histogram distributions for raw and standardised strain correlation scores in reproduced S1 Fig match published S1 Fig (visually robust to minor plotting parameter choices)
- value_in_range: computed standardised strain correlation score for all links in Crüsemann dataset is approximately −0.0060 (parameter-sensitive; exact match not required, allow ±5% tolerance)
- value_in_range: computed standardised strain correlation score for validated links in Crüsemann dataset is approximately 3.6717 (parameter-sensitive; exact match not required, allow ±5% tolerance)
- contains_substring: reproduced figure caption or metadata explicitly identifies validated link positions marked within score distribution histogram
- format_is: computed σ*_corr scores are numeric, real-valued, with no missing values across all three datasets

## Expert Review

- Verify that hypergeometric expectation and variance calculations used to standardise raw strain correlation score are statistically sound and correctly map the raw score distribution to zero-mean standardised form
- Confirm that the standardised score formula correctly implements the reported mathematical definition of σ*_corr (trace back to Methods section for exact formula; not present in discussion excerpt)
- Validate that validated link positions in reproduced histograms align with expected enrichment signal reported in text (e.g., p-value of 2.483 × 10−11 at 90th percentile)
- Review whether handling of ties, missing data, or edge cases in strain correlation (e.g., links with single shared strain) is consistent with article description
