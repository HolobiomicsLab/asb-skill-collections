# SciTask Card: Reproduce the MAMSI multi-assay MS integration workflow on metabolomics phenotyping data

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T13:26:03.540713+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_mamsi/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `model-training`, `statistical-analysis`
- DOI: `10.1371/journal.pcbi.1011814`
- GitHub: `kopeckylukas/py-mamsi`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `multi-omics`
- Subdomains: `multi-omics-integration`, `computational-metabolomics`, `biomarker-discovery`
- Techniques: `multivariate-statistics`, `partial-least-squares`, `pathway-analysis`, `dimensionality-reduction`, `normalization`, `statistical-analysis`

## Research Question
What are the model performance metrics and statistically significant metabolomic features identified when applying the full MAMSI pipeline (MB-PLS model fitting, MB-VIP feature selection, and cross-validation) to multi-assay LC-MS metabolomics datasets?

## Connected Finding
MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets and enables statistical feature selection from LC-MS metabolomics data.

## Task Description
Execute the complete MAMSI pipeline on multi-assay LC-MS metabolomics data (AddNeuroMed or MY Diabetes) to train a multiblock PLS discriminant model, identify statistically significant features via MB-VIP with permutation testing, and deliver model performance metrics and significant feature rankings.

## Inputs
- AddNeuroMed or MY Diabetes multi-assay LC-MS metabolomics data: HPOS (HILIC positive), LPOS (lipidomic reversed-phase positive), LNEG (lipidomic reversed-phase negative) intensity matrices (n_samples × n_features) and clinical metadata with outcome variable (e.g., biological sex or disease status)

## Expected Outputs
- Model performance metrics table: accuracy, recall, specificity, F1-score, AUC, confusion matrix for test set predictions
- Feature importance table with MB-VIP scores and empirical p-values for all features, sorted by statistical significance (p<0.01 threshold)
- Latent variable estimation plot showing model performance (AUC) versus number of components, identifying optimal LV count at plateau
- MB-VIP score visualization showing feature importance across all blocks

## Expected Output File

- `feature_significance_table.csv`

## Landmark Outputs

- `train_test_split_indices.pkl`
- `mbpls_model_fitted.pkl`
- `lv_estimation_results.csv`
- `test_predictions.csv`
- `mb_vip_scores.csv`
- `null_model_vip_permutations.npy`

## Tools
- Python
- mbpls
- pandas
- numpy
- scikit-learn
- matplotlib

## Skills
- multiblock-pls-model-fitting
- mb-vip-feature-importance-ranking
- permutation-test-p-value-estimation
- k-fold-cross-validation-model-selection
- metabolomics-feature-selection-significance-filtering
- multi-assay-data-integration-and-harmonization
- classification-model-performance-evaluation

## Workflow Description
1. Load and prepare multi-assay LC-MS intensity data (HPOS, LPOS, LNEG) and metadata using pandas, adding assay-specific prefixes to column names. 2. Split data into training (90%) and testing (10%) subsets using scikit-learn's train_test_split with random_state=42, maintaining sample correspondence across blocks. 3. Fit MB-PLS discriminant model on training data using MamsiPls with NIPALS algorithm and unit-variance standardization (standardize=True). 4. Estimate optimal number of latent variables using k-fold cross-validation (n_splits=5) with AUC metric via MamsiPls.estimate_lv(), identifying the model plateau threshold (plateau_threshold=0.01). 5. Refit MB-PLS with optimal latent variable count and evaluate on independent test set using MamsiPls.evaluate_class_model(), recording accuracy, recall, specificity, F1-score, and AUC. 6. Calculate Multi-Block Variable Importance in Projection (MB-VIP) scores for all features via MamsiPls.mb_vip(). 7. Perform empirical permutation testing (n_permutations≥10,000) using MamsiPls.mb_vip_permtest() with Y shuffling to generate empirical p-values for each feature. 8. Select statistically significant features at p<0.01 threshold and export feature importance table with p-values and VIP scores.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/MAMSI_logo.png` | figure | False |
| `figures/MAMSI_logo.svg` | figure | False |
| `figures/confusion_matrix.png` | figure | False |
| `figures/correlation_heatmap.png` | figure | False |
| `figures/lv_estimation.png` | figure | False |
| `figures/mb-vip.png` | figure | False |
| `figures/network.png` | figure | False |
| `figures/null_models_distribution.png` | figure | False |
| `figures/silhouette_plot.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found

## Domain Knowledge
- Multiblock PLS (MB-PLS) extends standard PLS to integrate multiple data blocks simultaneously, weighting each block's contribution through super-weights (A_) and block importances that reflect cross-block correlations with the outcome.
- MB-VIP scores aggregate weighted variance explained across all latent variables; features with VIP > 1 are generally considered important, but empirical p-values from permutation testing are required to establish statistical significance because VIP pooling can obscure small-effect components.
- Permutation testing in MB-VIP involves shuffling the outcome variable Y repeatedly (≥10,000 permutations recommended) and recalculating MB-VIP for each null model; empirical p-values are the proportion of null MB-VIP scores exceeding the observed test statistic.
- Cross-validation with k-fold (typically k=5) identifies the optimal number of latent variables by finding the plateau point where adding more components does not substantially improve validation performance; this prevents overfitting to training data noise.
- In metabolomics LC-MS, features are denoted as peak identifiers combining assay name, retention time (seconds), and m/z value (e.g., HPOS_233.25_149.111m/z); standardization of feature naming conventions across assays is essential for downstream structural linking and cross-assay validation.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: pandas, numpy, scikit-learn, matplotlib.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What are the model performance metrics and statistically significant metabolomic features identified when applying the full MAMSI pipeline (MB-PLS model fitting, MB-VIP feature selection, and cross-validation) to multi-assay LC-MS metabolomics datasets?: 'the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets and enables statistical feature selection from LC-MS metabolomics data.: 'MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] AddNeuroMed or MY Diabetes multi-assay LC-MS metabolomics data: HPOS (HILIC positive), LPOS (lipidomic reversed-phase positive), LNEG (lipidomic reversed-phase negative) intensity matrices (n_samples × n_features) and clinical metadata with outcome variable (e.g., biological sex or disease status): 'Data used within this quickstart guide originate from the the AddNeuroMed [[1](./index.md/#references)] cohort - dataset of Alzheimer's disease patients. You can download the sample data from this'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Model performance metrics table: accuracy, recall, specificity, F1-score, AUC, confusion matrix for test set predictions: '| Metric              | Score |
| ------------        | ----- |
| Accuracy            | 0.966 |
| Recall              | 1.0   |
| Specificity         | 0.943 |
| F<sub>1</sub> Score | 0.971 |
| AUC'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Feature importance table with MB-VIP scores and empirical p-values for all features, sorted by statistical significance (p<0.01 threshold): 'Select features with p-value < 0.01. You can also apply multiple testing correction methods to adjust the p-value threshold.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Latent variable estimation plot showing model performance (AUC) versus number of components, identifying optimal LV count at plateau: 'The LV estimation result shows that the model has 6 latent variables/components. Adding more LVs to the model could lead to overfitting.'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] MB-VIP score visualization showing feature importance across all blocks: '#### Multiblock Variable Importance in Projection'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Python: 'MAMSI is a Python framework'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] mbpls: 'It is based on MB_PLS package: Baum et al., (2019). Multiblock PLS: Block dependent prediction modeling for Python.'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] pandas: 'import pandas as pd'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] numpy: 'import numpy as np'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] scikit-learn: 'from sklearn.model_selection import train_test_split'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] matplotlib: 'from matplotlib import pyplot as plt'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify that kopeckylukas/py-mamsi repository is accessible and contains MB-PLS pipeline implementation
- verify that kopeckylukas/py-mamsi-tutorials repository contains AddNeuroMed or MY Diabetes sample dataset files
- script_runs: execute full MAMSI pipeline (MB-PLS model fitting, MB-VIP feature selection, cross-validation) on sample dataset without errors
- output_matches_reference: model performance metrics (AUC, accuracy, sensitivity, specificity) are numeric values in valid range [0.0, 1.0]
- output_matches_reference: cross-validation fold count and latent variable estimates are positive integers
- file_exists: pipeline produces a significant features list file (CSV or table format)
- file_format_is: significant features output contains at least columns for feature identifier, VIP score, and p-value
- value_in_range: MB-VIP scores are numeric and non-negative, robust to dataset-specific scaling

### Expert Review
- assess whether reported model performance metrics (AUC, accuracy) are scientifically reasonable for metabolomics classification on the specific dataset
- assess whether selected statistically significant features (after MB-VIP and permutation testing) align with known metabolic biomarkers or plausible biological signals for the phenotype
- assess whether cross-validation strategy (k-fold count, metric choice) is appropriate for the sample size and data characteristics of AddNeuroMed or MY Diabetes dataset

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load multi-assay LC-MS intensity data (HPOS, LPOS, LNEG) and clinical outcome variable; apply assay-specific column name prefixes for downstream traceability.
2. Partition data into training (90%) and test (10%) sets using stratified random split, maintaining block alignment.
3. Fit multiblock PLS discriminant model on training data using NIPALS algorithm with unit-variance standardization; compute super-scores, block loadings, and regression coefficients.
4. Estimate optimal latent variable count via k-fold cross-validation (k=5) using AUC metric; identify plateau at lowest LV count with stable validation performance.
5. Evaluate final model on held-out test set; record classification metrics (accuracy, recall, specificity, F1-score, AUC) and confusion matrix.
6. Calculate Multi-Block Variable Importance in Projection (MB-VIP) scores summarizing feature importance across all latent variables weighted by variance explained.
7. Perform empirical permutation testing (n≥10,000 permutations) by repeated Y-shuffling and model refitting; compute empirical p-values as proportion of null VIP scores exceeding observed.
8. Filter features at p<0.01 significance threshold and export ranked feature importance table with MB-VIP scores and empirical p-values. Validation: confirmed output table row count, column names, and p-value range [0, 1].
9. References: source article (DOI: 10.1371/journal.pcbi.1011814)

## Workflow Ports

**Inputs:**

- `lcms_data` — Multi-assay LC-MS intensity matrices with assay prefixes
- `metadata` — Clinical metadata with outcome variable

**Outputs:**

- `model_metrics` — Test set performance metrics and confusion matrix
- `feature_significance` — Feature importance table with MB-VIP scores and p-values
- `lv_estimate_plot` — Latent variable estimation curve
- `vip_plot` — MB-VIP score visualization

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:kopeckylukas__py-mamsi`
- **Synthesized at:** 2026-06-15T13:34:24+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
