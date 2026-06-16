# Evaluation Strategy

## Direct Checks

- file_exists: verify that AllPositive dataset is accessible at https://doi.org/10.5281/zenodo.3978118 or https://zenodo.org/record/4173596
- file_exists: verify that UniqueInchiKeys dataset is accessible at https://doi.org/10.5281/zenodo.3978118
- file_exists: verify that pre-trained Word2Vec models are accessible at https://doi.org/10.5281/zenodo.3978054 (UniqueInchikey) and https://zenodo.org/record/4173596 (AllPositive)
- file_exists: verify that matchms package implementation is accessible at https://github.com/matchms/matchms
- file_exists: verify that spec2vec package is accessible at https://github.com/iomega/spec2vec
- script_runs: verify that cosine, modified cosine, and Spec2Vec similarity score calculations execute without error on both AllPositive and UniqueInchiKeys datasets
- value_in_range: verify that computed similarity scores fall within [0.0, 1.0] for all three methods
- row_count_equals: verify that the number of spectral pairs evaluated matches the expected pairwise combinations for each dataset (robust to parameter choices in preprocessing)
- output_matches_reference: verify that average Tanimoto similarity at top 0.1% of scores for cosine, modified cosine, and Spec2Vec methods matches the values reported in Figure 3B of the published article (exact byte-for-byte match for reported numerical values)
- field_present: verify that output similarity matrices or score rankings contain at least three columns corresponding to cosine score, modified cosine score, and Spec2Vec score

## Expert Review

- Confirm that the filtering strategy applied to both datasets (removal of spectra with <10 fragments, filtering by m/z range [0, 1000], relative intensity threshold <0.01, and parent mass scaling for peak retention) matches the methods described in the paper
- Confirm that the top 0.1% percentile threshold is correctly computed and applied identically across all three similarity scoring methods
- Confirm that Tanimoto similarity values computed from structural fingerprints (InChIKey-based or RDKit-derived) represent the ground-truth structural similarity metric and are correctly paired with spectra
- Assess whether observed Tanimoto similarity distributions at top 0.1% of scores demonstrate the expected pattern: Spec2Vec scores should show higher average Tanimoto than cosine and modified cosine, consistent with the paper's reported advantage in capturing structural relationships
- Confirm that neutral losses are correctly calculated as precursor m/z minus peak m/z and are properly encoded as 'loss@xxx.xx' features in the Word2Vec training corpus
