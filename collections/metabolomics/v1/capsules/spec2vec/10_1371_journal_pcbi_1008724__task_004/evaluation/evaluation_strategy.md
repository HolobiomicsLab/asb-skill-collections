# Evaluation Strategy

## Direct Checks

- file_exists: verify AllPositive dataset is accessible at https://doi.org/10.5281/zenodo.3978118
- file_exists: verify trained Word2Vec model (AllPositive, 15-epoch) is accessible at https://zenodo.org/record/4173596
- script_runs: verify spec2vec package (https://github.com/iomeva/spec2vec) can be installed and imported successfully
- file_format_is: verify AllPositive dataset contains mass spectra in a loadable format (e.g., JSON, MGF, or compatible pickle)
- row_count_equals: verify AllPositive dataset contains exactly 95,320 spectra as reported in methods section
- value_in_range: verify computed peak coverage statistic (missing-fraction = 1 − Σ√w_i / Σ√w_i) outputs a value between 0.0 and 1.0 for each corpus size
- output_matches_reference: verify final missing-fraction value for full 95,320-spectrum corpus matches the reported 97% peak coverage (or equivalently, 0.03 missing fraction) from discussion text, within ±1 percentage point
- script_runs: verify analysis script (from https://github.com/iomega/spec2vec_gnps_data_analysis or equivalent) can compute coverage curve without errors
- contains_substring: verify output plot or table contains coverage measurements at multiple corpus sizes showing progression toward 97% coverage, parameter-sensitive to corpus size intervals chosen

## Expert Review

- Verify that the missing-fraction calculation (1 − Σ√w_i / Σ√w_i) correctly implements the intended peak coverage metric described in methods; confirm interpretation of w_i as peak weights and that square root weighting is appropriate for this analysis
- Assess whether the reported 97% peak coverage for the 15-epoch model is consistent with the claim that 'a model pre-trained on a large spectra dataset will cover a large enough fraction of the features' from the discussion section
- Evaluate whether coverage curve shape and saturation behavior are reasonable given typical Word2Vec learning dynamics on ~95k spectra
