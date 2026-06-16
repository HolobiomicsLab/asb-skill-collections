# Evaluation Strategy

## Direct Checks

- verify file exists: trained model weights from zenodo.org/record/4699356
- verify file exists: test-set spectra data (3601 spectra) in deposited dataset or GitHub repository
- script_runs: Python script that loads MS2DeepScore model, extracts 200-dimensional embeddings for test-set spectra, runs t-SNE dimensionality reduction using scikit-learn t-SNE implementation with default or reported parameters
- file_format_is: output t-SNE coordinates file contains exactly 3601 rows (one per test spectrum) and 2 columns (x, y coordinates)
- file_exists: ClassyFire chemical superclass labels for 3601 test-set spectra (must be retrievable or pre-computed from InChIKey annotations)
- output_matches_reference: generated t-SNE visualization (colored by ClassyFire superclass) matches or closely reproduces Fig. 2, 4, 5, 7, or 8 as reported in article or supplementary materials (robust to visualization library differences, parameter-sensitive to t-SNE random seed and perplexity)
- value_in_range: silhouette coefficient or Davies-Bouldin index computed on t-SNE clusters grouped by chemical superclass is consistent with visual clustering quality shown in reference figure

## Expert Review

- assess whether observed chemical class clustering in t-SNE plot is chemically meaningful and consistent with structural similarity expectations (requires domain chemistry knowledge to interpret superclass assignments and their expected co-localization)
- evaluate whether any chemical superclasses fail to cluster coherently and whether such failures are explainable by inter-class structural similarity or data imbalance (expert judgment on expected chemical class relationships)
- verify that embedding extraction pipeline correctly preserves spectrum identity and that ClassyFire labels are accurately matched to spectra (requires inspection of intermediate data integrity)
