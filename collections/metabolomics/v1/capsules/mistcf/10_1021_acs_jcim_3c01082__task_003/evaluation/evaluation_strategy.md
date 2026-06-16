# Evaluation Strategy

## Direct Checks

- Verify that github:samgoldman97__mist-cf repository contains trained MIST-CF model checkpoint(s) and code to load them
- Verify that a published benchmark dataset is deposited and accessible (check Zenodo DOI 10.1021/acs.jcim.3c01082 supplementary materials or linked repository for dataset file or accession)
- Verify script runs: execute formula-ranking evaluation pipeline on benchmark data with MULTI_ADDUCT_SUPPORT disabled (single [M+H]+ mode only) and produces a ranked-formula output file or metrics table
- Verify script runs: execute formula-ranking evaluation pipeline on benchmark data with MULTI_ADDUCT_SUPPORT enabled (full multi-adduct mode) and produces a ranked-formula output file or metrics table
- Value in range: accuracy/recall metric for [M+H]+-only ranking must be a number between 0 and 1 (or 0–100 if percentage)
- Value in range: accuracy/recall metric for multi-adduct ranking must be a number between 0 and 1 (or 0–100 if percentage)
- Verify output matches reference: compare reported performance gap (multi-adduct vs [M+H]+-only) to any ablation or sensitivity analysis reported in article text or supplementary materials

## Expert Review

- Assess whether the experimental protocol correctly isolates MULTI_ADDUCT_SUPPORT contribution by disabling only that component and holding all other hyperparameters, training data, and model architecture constant
- Evaluate whether the benchmark dataset used is appropriate for measuring adduct-ranking contribution (sufficient diversity of compounds and adduct types, representative of real unknown samples)
- Judge whether the reported improvement in ranking accuracy from multi-adduct support is scientifically meaningful and consistent with prior literature on adduct-aware formula annotation
