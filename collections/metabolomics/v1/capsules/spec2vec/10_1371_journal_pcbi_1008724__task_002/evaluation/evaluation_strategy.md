# Evaluation Strategy

## Direct Checks

- verify file exists at Zenodo deposit 10.5281/zenodo.3978118 (AllPositive dataset)
- verify AllPositive dataset contains exactly 95,320 spectra or 92,954 spectra with InChIKey as reported in methods
- verify trained Word2Vec models exist at Zenodo deposit zenodo.org/record/4173596 (AllPositive dataset models)
- verify spec2vec Python package (https://github.com/iomega/spec2vec) can be installed and imported
- verify matchms Python package (https://github.com/matchms/matchms) contains cosine and modified cosine implementations
- script_runs: library matching experiment with cosine score (tolerance=0.005, min_match=6) on AllPositive dataset subset
- script_runs: library matching experiment with modified cosine score (tolerance=0.005, min_match=10) on AllPositive dataset subset
- script_runs: library matching experiment with Spec2Vec 15-epoch model on AllPositive dataset subset
- script_runs: library matching experiment with Spec2Vec 50-epoch model on AllPositive dataset subset
- output_matches_reference: true-positive and false-positive rate values from cosine library matching match reported figure/table location in published paper (multiple defensible rounding approaches)
- output_matches_reference: true-positive and false-positive rate values from modified cosine library matching match reported figure/table location in published paper (multiple defensible rounding approaches)
- output_matches_reference: true-positive and false-positive rate values from Spec2Vec 15-epoch library matching match reported figure/table location in published paper (multiple defensible rounding approaches)
- output_matches_reference: true-positive and false-positive rate values from Spec2Vec 50-epoch library matching match reported figure/table location in published paper (multiple defensible rounding approaches)
- file_format_is: AllPositive dataset in JSON or MGF format (standard metabolomics spectrum format)
- field_present: each spectrum in dataset contains required fields for library matching (m/z, intensity, precursor_mz, InChIKey)

## Expert Review

- verify that reported library matching experimental conditions (tolerance and min_match thresholds) are appropriate for LC-MS metabolomics data
- verify that the query spectrum subset and library spectrum subset used in reported results are properly stratified (no leakage between training and test sets)
- assess whether reported true-positive and false-positive rates are consistent with expected performance differences between cosine, modified cosine, and Spec2Vec approaches
- confirm that the 15-epoch and 50-epoch training iterations for Word2Vec models are computationally justified and reasonable for the AllPositive dataset size
- assess whether precursor m/z tolerance (1ppm) used for pre-selection is appropriate for high-resolution LC-MS instruments
