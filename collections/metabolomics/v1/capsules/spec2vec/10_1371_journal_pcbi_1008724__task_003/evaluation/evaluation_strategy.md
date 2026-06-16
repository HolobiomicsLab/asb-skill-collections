# Evaluation Strategy

## Direct Checks

- verify file exists: spec2vec repository (https://github.com/iomega/spec2vec) contains source code for spectrum-to-vector encoding
- verify file exists: matchms repository (https://github.com/matchms/matchms) contains peak and neutral-loss word generation implementations
- script_runs: execute spectrum preprocessing and document generation on sample spectrum from AllPositive dataset (10.5281/zenodo.3978118) using spec2vec package; verify output contains peak@xxx.xx and loss@xxx.xx word tokens
- output_matches_reference: generated spectrum document tokens match expected format (peak@xxx.xx with precision and loss@xxx.xx with range 5.0–200.0 Da), multiple defensible precision choices robust to parameter choices
- file_format_is: trained Word2Vec model file downloaded from 10.5281/zenodo.3978054 or zenodo.org/record/4173596 is in standard gensim/word2vec format readable by Python Word2Vec libraries
- value_in_range: spectrum vector dimensionality matches Word2Vec embedding dimension (no canonical answer; article does not specify, requires parameter specification)
- file_exists: output spectrum vector file per input spectrum exists with consistent naming convention and format (e.g., .npy, .csv, or binary vector)

## Expert Review

- verify that weighted summation aggregation strategy (sum of word vectors weighted by peak intensity) is correctly implemented according to methods description and produces interpretable spectrum embeddings
- assess whether treatment of unknown peaks (peaks not in trained Word2Vec vocabulary) is correctly implemented via missing fraction assessment as described in methods
- evaluate whether maximum peak filtering (max(n_peaks) = 0.5 × parentmass) is correctly applied during document generation and does not remove peaks incorrectly
- assess correctness of neutral loss calculation (precursor − peak) and filtering (5.0–200.0 Da range) in document generation stage
- verify that spectrum vector aggregation preserves structural relationship information required for downstream similarity scoring, e.g., by spot-checking similarity between structurally similar pairs
