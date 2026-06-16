# Evaluation Strategy

## Direct Checks

- file_exists: verify that peak-abundance list file (formatted for MetaboDirect) is retrievable from OSF deposit https://doi.org/10.17605/OSF.IO/XFHZ9
- file_exists: verify that molecular-formula-assigned file for bacterium-phage dataset is retrievable from OSF deposit https://doi.org/10.17605/OSF.IO/XFHZ9
- file_format_is: confirm peak-abundance file is in format compatible with MetaboDirect pipeline input (XML or tabular format with peak m/z, intensity, and sample identifiers)
- file_format_is: confirm molecular-formula file contains assigned elemental composition (C, H, O, N, S, P counts) and associated peak identifiers matching abundance data
- script_runs: verify MetaboDirect v0.3.4 (from GitHub https://github.com/Coayala/MetaboDirect at commit https://doi.org/10.5281/zenodo.7278253) executes Step 5 (multivariate statistical analysis) without errors on the downloaded OSF files
- value_in_range: extract PERMANOVA p-value for phage-type factor (HP1 vs. HS2 vs. control) from MetaboDirect Step 5 output; verify value is numeric, bounded [0, 1], and matches reported result in Supplementary Fig. S7C (expected: non-significant, p > 0.05)
- contains_substring: verify MetaboDirect Step 5 output log or results table contains PERMANOVA test label and phage-type factor designation
- output_matches_reference: compare computed PERMANOVA p-value against the reported p-value shown in Supplementary Fig. S7C panel (last column of PERMANOVA results); allow tolerance of ±0.01 for numerical precision across software versions, parameter-sensitive to effect-size threshold and distance metric choices in PERMANOVA function

## Expert Review

- Verify that MetaboDirect's PERMANOVA implementation (using vegan::adonis2 or equivalent) applies the correct statistical model: response = phage type, with appropriate distance metric (Euclidean or Bray-Curtis) and permutation count (typically 999)
- Confirm that the phage-type factor in the analysis correctly encodes the three levels (HP1, HS2, control) from the bacterium-phage dataset design and that sample annotations are properly read from the input files
- Assess whether the reported non-significant result (p > 0.05 for phage-type in Fig. S7C) is consistent with the biological context: evaluate whether the data structure (36 samples, ~495 molecular formulas per sample on average) would support detection of a true phage effect if present, given the observed variance in DOM composition
- Evaluate methodological transparency: confirm that MetaboDirect's Step 5 documentation (GitHub README, User's Guide at https://metabodirect.readthedocs.io, or Supplementary Information Table S3) explicitly specifies the PERMANOVA distance metric, permutation scheme, and statistical assumptions used
