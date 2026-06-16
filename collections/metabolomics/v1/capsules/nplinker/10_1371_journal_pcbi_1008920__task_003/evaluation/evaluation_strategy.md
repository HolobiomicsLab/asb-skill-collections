# Evaluation Strategy

## Direct Checks

- file_exists: S1 Data (Linked MIBiG and GNPS databases with SMILES strings and BGC-spectrum links)
- file_exists: S2 Data (High-scoring links from Crüsemann dataset)
- file_exists: S3 Data (High-scoring links from Leão dataset)
- file_exists: S4 Data (High-scoring links from Gross dataset)
- script_runs: NPLinker strain correlation scoring module on input GCF-MF pairs from three datasets, producing standardised scores
- script_runs: NPLinker IOKR scoring module on input spectra and BGC candidates, producing IOKR scores for the three datasets
- script_runs: NPLinker combined scoring function (ℓp-norm with sign adjustment) integrating both standardised scores
- output_matches_reference: ratio of validated links in top 10% by combined score vs. top 10% by strain correlation alone, across all three datasets (reference: Table 4 values)
- output_matches_reference: ratio of validated links in top 10% by combined score vs. top 10% by IOKR alone, across all three datasets (reference: Table 4 values)
- value_in_range: proportion of validated links in 90th percentile for standardised strain correlation score in Crüsemann dataset, robust to choice of percentile threshold
- value_in_range: proportion of validated links in 90th percentile for IOKR score in Crüsemann dataset, robust to choice of percentile threshold
- value_in_range: proportion of validated links in 90th percentile for combined score in Crüsemann dataset, robust to choice of percentile threshold
- row_count_equals: number of GCF-MF pairs evaluated in each of Crüsemann, Gross, and Leão datasets matches supplementary data counts
- contains_substring: Table 4 in published article reports enrichment ratios and p-values for joint top-percentile performance across three datasets

## Expert Review

- Verify that the reported improvement in validated link ratio (Table 4) represents a meaningful biological or chemical validation criterion (e.g., spectral matching, known biosynthetic relationship)
- Assess whether the choice of ℓp-norm exponent (p=0.5 in combined function) is justified and whether alternative exponents were tested and reported
- Evaluate whether the three datasets (Crüsemann, Gross, Leão) represent adequate diversity in microbial ecology, strain characteristics, and compound classes to support generalisability claims
- Review the statistical significance and effect sizes reported in Table 4 to determine whether improvements are both statistically and practically significant
