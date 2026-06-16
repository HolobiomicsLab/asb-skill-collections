# Evaluation Strategy

## Direct Checks

- verify that repository constantino-garcia/cmmrt contains implementation of Bayesian meta-learning projection mechanism
- verify that implementation accepts as input: (i) a pre-trained DNN model trained on METLIN SMRT dataset, (ii) calibration molecules (≥10), and (iii) a held-out test set with known retention times
- verify that code produces projected RT predictions (numeric values in seconds) for the held-out test set as named output artifact
- verify that projection mechanism maps retention times from external chromatographic method onto METLIN-trained DNN's feature space
- script_runs: execute meta-learning projection pipeline with minimum 10 calibration molecules and report absence of runtime errors
- value_in_range: reported mean absolute error on held-out test set is within the range cited in article (39.2±1.2 s or better), or expert review explains variance
- file_exists: verify presence of trained model weights or checkpoint file for METLIN-trained DNN in repository

## Expert Review

- assess whether Bayesian formulation of meta-learning projection is mathematically sound and implements posterior inference over projection parameters
- evaluate whether projected RT predictions on held-out test set are competitive with baseline methods (as claimed in article abstract)
- review whether the implementation correctly handles the low-data regime (10 calibration molecules) and produces credible uncertainty estimates
- assess reproducibility: compare projected RT predictions against reference results reported in article or supplementary material if available
