# Evaluation Strategy

## Direct Checks

- file_exists: MiMeNet package or evaluation code at https://github.com/YDaiLab/MiMeNet
- script_runs: MiMeNet 10-fold CV pipeline executable on IBD (PRISM) dataset with hyperparameter configuration input
- output_matches_reference: mean SCC values for IBD (PRISM) dataset reported in article abstract (increase from 0.108 to 0.309), robust to random seed variation within ±0.01
- row_count_equals: well-predicted metabolite count for IBD (PRISM) dataset matches article abstract (increase from 198 to 366), allowing ±5 metabolites due to threshold sensitivity
- value_in_range: SCC values for both Tune Once and Tune Every Partition conditions fall between -1.0 and 1.0
- contains_substring: output report includes labeled fields for 'mean_scc_tune_once', 'mean_scc_tune_every_partition', 'well_predicted_count_tune_once', 'well_predicted_count_tune_every_partition'
- format_is: ablation output structured as table or CSV with columns: condition_name, mean_scc, std_scc, well_predicted_metabolite_count, fold_identifiers

## Expert Review

- Verify that hyperparameter tuning strategy ('Tune Once' vs. 'Tune Every Partition') is implemented as described in methods section and produces materially different network configurations across folds
- Assess whether reported SCC improvements and well-predicted metabolite counts are biologically plausible given dataset size (121 IBD PRISM samples) and feature dimensionality
- Evaluate whether ablation design isolates the effect of tuning strategy alone without confounding from random initialization, cross-validation splitting strategy, or other hyperparameter changes
- Confirm that well-predicted metabolite threshold (95th percentile of background distribution) is applied consistently across both ablation conditions and computed from shuffled dataset
- Judge whether performance difference between Tune Once and Tune Every Partition is substantial enough to warrant the computational cost difference and support the article's claims about hyperparameter sensitivity
