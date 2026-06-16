# Evaluation Strategy

## Direct Checks

- verify that the GitHub repository samgoldman97/mist-cf contains a MULTI_ADDUCT_SUPPORT module or component with code comments or documentation explicitly listing supported adduct types
- verify file_exists: a trained or fine-tuned model checkpoint in the repository targeting negative-mode MS/MS spectra
- verify that the repository contains a script or notebook that can load a public negative-mode MS/MS dataset (e.g. from MassIVE, MetaboLights, or PRIDE with explicit accession or URL)
- verify that evaluation results (top-k formula ranking accuracy metrics) are reported in a table, CSV, or JSON file within the repository with numeric accuracy values and corresponding k values
- verify format_is: the accuracy results are in a structured format (table, JSON, or CSV) with at least columns/fields for 'k', 'accuracy', and 'dataset_name' or 'mode'
- verify contains_substring: any model card, README, or results document references 'negative' mode or '[M-H]-' adduct support
- verify output_matches_reference: if a reference negative-mode benchmark is cited, the reported top-k accuracies fall within the expected range stated in that benchmark (requires expert review of literature values)

## Expert Review

- chemical plausibility of the negative-mode adduct list: confirm that selected adducts ([M-H]-, [M+Cl]-, [M+HCOO]-, etc.) represent the most common species observed in negative-mode ESI-MS/MS for organic small molecules
- appropriateness of fine-tuning strategy: assess whether the retraining approach (learning rates, batch sizes, data split, validation protocol) is sound for transfer learning from positive to negative mode
- statistical significance of top-k accuracy: confirm that reported accuracies are computed on a held-out test set with sufficient sample size and that confidence intervals or standard errors are provided
- completeness of negative-mode MS/MS dataset: verify that the public dataset used contains sufficient structural diversity and spectral quality to support robust model training and generalization
- comparison fairness: if baseline or ablation comparisons are made, confirm that all models are trained and evaluated on identical data splits and with equivalent hyperparameter tuning effort
