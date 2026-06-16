# SciTask Card: Reproduce MiMeNet vs. linear-model prediction performance across three datasets

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T07:36:08.260853+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_mimenet`
- Domain: `bioinformatics`
- Subtask categories: `model-training`, `benchmark-evaluation`, `statistical-analysis`
- DOI: `10.1371/journal.pcbi.1009021`
- GitHub: `biobakery/melonnpan`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `microbiome-metabolomics`, `artificial-intelligence`, `multi-omics-integration`
- Techniques: `deep-learning`, `machine-learning`, `random-forest`, `correlation-analysis`, `clustering`

## Research Question
Does MiMeNet achieve higher mean Spearman correlation coefficients and identify more well-predicted metabolites compared to MelonnPan, Random Forest, and CCA baselines across IBD (PRISM), Cystic Fibrosis, and Soil datasets using ten iterations of 10-fold cross-validation?

## Connected Finding
MiMeNet achieves mean Spearman correlation coefficients that increase from 0.108 to 0.309 (IBD PRISM), 0.276 to 0.457 (Cystic Fibrosis), and -0.272 to 0.264 (Soil) compared to MelonnPan, and identifies more well-predicted metabolites: 366 vs 198 (IBD), 143 vs 104 (CF), and 29 vs 4 (Soil).

## Task Description
Reproduce the mean Spearman correlation coefficients and well-predicted metabolite counts for MiMeNet and three baseline models (Elastic Net via MelonnPan, Canonical Correlation Analysis, Random Forest) on IBD (PRISM), Cystic Fibrosis, and Soil datasets using ten iterations of 10-fold cross-validation, matching reported abstract values.

## Inputs
- IBD (PRISM) microbiome and metabolomic data (121 IBD patients + 34 controls; 201 microbial species, 8848 metabolites)
- Cystic Fibrosis lung sputum microbiome and metabolomic data (172 samples; 657 microbial genera, 168 metabolites)
- Soil biocrust microbiome and metabolomic data (five time points, four successional stages; 466 microbes, 85 metabolites)

## Expected Outputs
- Mean Spearman correlation coefficients (±SD) for MiMeNet and baseline models (Elastic Net, CCA, Random Forest) across ten iterations of 10-fold cross-validation on each dataset
- Count of well-predicted metabolites (SCC > 95th percentile of background) for MiMeNet and baseline models on each dataset
- Tabular summary of performance metrics (SCC, PCC, MAE) for all models and datasets with mean and standard deviation

## Expected Output File

- `benchmark_results_mimenet_baselines.csv`

## Landmark Outputs

- `preprocessed_ibd_prism_microbiome.csv`
- `preprocessed_ibd_prism_metabolome.csv`
- `hyperparameters_optimized.json`
- `background_distribution_sccs.csv`
- `well_predicted_metabolites_per_dataset.csv`
- `mimenet_predictions_ibd_prism.csv`

## Tools
- neural networks
- neural networks (MLPNN with ReLU activation)
- MelonnPan (Elastic Net linear regression)
- Elastic Net regression
- Random Forest regression
- Canonical Correlation Analysis (CCA)
- ADAM optimizer
- scikit-learn (Python)

## Skills
- microbiome-metabolome-prediction-modeling
- neural-network-hyperparameter-tuning
- cross-validation-benchmark-evaluation
- spearman-correlation-statistical-analysis
- multivariate-regression-comparison
- compositional-data-transformation-clr
- background-distribution-threshold-calibration

## Workflow Description
1. Load and preprocess microbiome and metabolomic data from IBD (PRISM), Cystic Fibrosis, and Soil datasets, removing features present in <10% of samples and applying centered log-ratio (CLR) transformation with pseudocount of 1 (except IBD microbes in relative abundance). 2. Perform hyperparameter tuning using nested 5-fold cross-validation to select optimal layer size, number of layers, L2 regularization (λ), and dropout rates for MiMeNet MLPNN architecture on each dataset. 3. Train MiMeNet using ADAM optimizer with mean squared error loss function and L2 regularization, applying ReLU activation and dropout at each hidden layer, with early stopping when validation loss does not improve within 40 iterations. 4. Evaluate MiMeNet over 10 iterations of 10-fold cross-validation (90% training, 10% test; 80/20 train-validation split) and calculate mean Spearman correlation coefficient (SCC) between predicted and observed metabolite abundances. 5. Generate background SCC distribution by training 100 shuffled models with random sample reordering and define well-predicted metabolites as those with SCC above the 95th percentile of background correlations. 6. Train Elastic Net (via MelonnPan with α and l1_ratio grid search), Canonical Correlation Analysis (with 10, 20, 40 components), and Random Forest (100 tree estimators) baseline models using identical cross-validation protocol and calculate mean SCC and well-predicted metabolite counts. 7. Aggregate results across all three datasets and ten iterations, reporting mean ± standard deviation of SCC and total well-predicted metabolite counts for each model.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `mimenet.pdf` | main_article | True |

## Missing Information
- No specification of the exact random seed(s) used for the ten iterations of 10-fold cross-validation, making exact reproduction difficult
- No explicit reporting of mean and standard deviation of correlation coefficients across the ten iterations, only single reported values
- Hyperparameter values used for each dataset's neural network architecture not reported in main text or accessible supplementary section
- No specification of which baseline model (Elastic Net, CCA, or Random Forest) produces which reported correlation coefficients in the abstract
- Threshold value for soil data described as 'higher' than other datasets but exact numerical value not provided in discussion
- No information on computational requirements, training time, or convergence criteria for the neural network models across datasets

## Domain Knowledge
- Centered log-ratio (CLR) transformation is required for compositional microbiome data to avoid spurious correlations; pseudocount of 1 is added before log transformation to prevent log(0).
- Well-predicted metabolites are defined as those with Spearman correlation coefficient above the 95th percentile of a background distribution generated by training 100 models on randomly shuffled (unlabeled) sample data to control for false discovery.
- L2 regularization penalty (λ) and dropout rate are critical hyperparameters for preventing neural network overfitting in microbiome-metabolome prediction; optimal values typically range from 0.0001 to 0.1 for λ and 0.1 to 0.5 for dropout.
- Early stopping during neural network training is triggered when validation loss does not improve within 40 iterations, using the 20% validation partition from the 90% training set in each cross-validation fold.
- Mean Spearman correlation coefficient (SCC) is the primary metric for comparing predictive accuracy across models; values range from -1 to +1, with higher values indicating better metabolite abundance prediction from microbiome input.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Does MiMeNet achieve higher mean Spearman correlation coefficients and identify more well-predicted metabolites compared to MelonnPan, Random Forest, and CCA baselines across IBD (PRISM), Cystic Fibrosis, and Soil datasets using ten iterations of 10-fold cross-validation?: 'we compared the k-fold cross-validated prediction correlations (k = 10, 5, 3, and 2) using the IBD (PRISM) and cystic fibrosis datasets'
- `ev_002` from `agent2_synthesis` (agent2_traced): [abstract] MiMeNet achieves mean Spearman correlation coefficients that increase from 0.108 to 0.309 (IBD PRISM), 0.276 to 0.457 (Cystic Fibrosis), and -0.272 to 0.264 (Soil) compared to MelonnPan, and identifies more well-predicted metabolites: 366 vs 198 (IBD), 143 vs 104 (CF), and 29 vs 4 (Soil).: 'MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264) and identifies more well-predicted'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] IBD (PRISM) microbiome and metabolomic data (121 IBD patients + 34 controls; 201 microbial species, 8848 metabolites): 'This dataset is named as IBD (PRISM). Additionally, it includes an external validation dataset using two other cohorts... A total of 201 microbial species and 8848 metabolites were identified for the'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Cystic Fibrosis lung sputum microbiome and metabolomic data (172 samples; 657 microbial genera, 168 metabolites): 'The second dataset was taken from a study that collected 172 lung sputum samples from patients with cystic fibrosis [31]. Microbial features were generated using 16S rRNA gene sequencing and'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Soil biocrust microbiome and metabolomic data (five time points, four successional stages; 466 microbes, 85 metabolites): 'The third dataset represents microbial and metabolic activity caused by soil wetting at five-time points across four biocrust successional stages [32]. A total of 466 microbes and 85 metabolites were'
- `ev_006` from `agent2_synthesis` (agent2_traced): [abstract] Mean Spearman correlation coefficients (±SD) for MiMeNet and baseline models (Elastic Net, CCA, Random Forest) across ten iterations of 10-fold cross-validation on each dataset: 'MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [abstract] Count of well-predicted metabolites (SCC > 95th percentile of background) for MiMeNet and baseline models on each dataset: 'identifies more well-predicted metabolites (increase in the number of well-predicted metabolites from 198 to 366, 104 to 143, and 4 to 29) compared to state-of-art linear models'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Tabular summary of performance metrics (SCC, PCC, MAE) for all models and datasets with mean and standard deviation: 'Mean and standard deviation values for SCC, PCC, and MAE are shown. All data were transformed using centered log-ratio except for IBD microbial input, which was obtained in relative abundance.'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] neural networks (MLPNN with ReLU activation): 'In MiMeNet, φ is set as the rectified linear unit (ReLU).'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] MelonnPan (Elastic Net linear regression): 'MelonnPan was downloaded from https://github.com/biobakery/melonnpan and executed using the given instructions.'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] Elastic Net regression: 'Multivariate Elastic Net models were implemented using ElasticNet and GridSearchCV using 5-fold internal cross-validation for hyper-parameter tuning where the hyper-parameter grid contained'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] Random Forest regression: 'Random Forest models were implemented using RandomForestRegressor with the default parameter set-tings of 100 tree estimators.'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] Canonical Correlation Analysis (CCA): 'Canonical correlation analyses were implemented using CCA with 10, 20, and 40 components.'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] ADAM optimizer: 'MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] scikit-learn (Python): 'these models can predict the entire set of metabolites at once, and all models were evaluated using 10 iterations of 10-fold cross-validation. Random Forest, multivariate Elastic Net, and Canonical'
- `ev_016` from `agent2_synthesis` (agent2_traced): [results] No specification of the exact random seed(s) used for the ten iterations of 10-fold cross-validation, making exact reproduction difficult: 'MiMeNet then trains multiple network models using 10-fold cross-validation'
- `ev_017` from `agent2_synthesis` (agent2_traced): [abstract] No explicit reporting of mean and standard deviation of correlation coefficients across the ten iterations, only single reported values: 'mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264'
- `ev_018` from `agent2_synthesis` (agent2_traced): [results] Hyperparameter values used for each dataset's neural network architecture not reported in main text or accessible supplementary section: 'The network architecture in MiMeNet is first determined for each paired dataset by tuning the hyperparameters'
- `ev_019` from `agent2_synthesis` (agent2_traced): [abstract] No specification of which baseline model (Elastic Net, CCA, or Random Forest) produces which reported correlation coefficients in the abstract: 'mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264'
- `ev_020` from `agent2_synthesis` (agent2_traced): [discussion] Threshold value for soil data described as 'higher' than other datasets but exact numerical value not provided in discussion: 'We also observed a higher threshold value for the soil data, which may be due to the longitudinal observations.'
- `ev_021` from `agent2_synthesis` (agent2_traced): [results] No information on computational requirements, training time, or convergence criteria for the neural network models across datasets: 'MiMeNet then trains multiple network models using 10-fold cross-validation'

## Evaluation Strategy
### Direct Checks
- verify that MiMeNet GitHub repository (https://github.com/YDaiLab/MiMeNet) contains executable code for running 10-fold cross-validation experiments
- verify that MiMeNet code implements ten iterations of 10-fold cross-validation as described in methods
- verify that Spearman correlation coefficient calculation is implemented correctly in the codebase (script_runs on validation data)
- verify that well-predicted metabolite threshold is set to 95th percentile of background distribution as stated in methods
- verify that output files or logs from cross-validation contain mean Spearman correlation coefficients for each dataset and model (file_format_is CSV/TSV or JSON with named fields for correlation values)
- value of reported mean Spearman correlation for MiMeNet on IBD (PRISM) dataset is 0.309 (robust to minor numerical precision differences <0.001)
- value of reported mean Spearman correlation for MiMeNet on Cystic Fibrosis dataset is 0.457 (robust to minor numerical precision differences <0.001)
- value of reported mean Spearman correlation for MiMeNet on Soil dataset is 0.264 (robust to minor numerical precision differences <0.001)
- value of reported well-predicted metabolite count for MiMeNet on IBD (PRISM) dataset is 366 (exact match)
- value of reported well-predicted metabolite count for MiMeNet on Cystic Fibrosis dataset is 143 (exact match)
- value of reported well-predicted metabolite count for MiMeNet on Soil dataset is 29 (exact match)
- baseline model correlation and metabolite count outputs match values reported in figures (S6 Fig, S7 Fig) or supplementary tables for Elastic Net/MelonnPan, CCA, and Random Forest
- verify that all three datasets (IBD PRISM, Cystic Fibrosis, Soil) are loaded with correct sample counts and feature dimensions as reported in Methods section

### Expert Review
- assess whether hyperparameter tuning procedure (number/size of hidden layers, L2 regularization penalty) is appropriate and reproducible across the three datasets
- assess whether the choice of Spearman correlation as the performance metric is suitable for the prediction task and comparable across datasets
- assess whether the background distribution generation procedure (shuffling dataset and re-running cross-validation) is statistically sound and whether the 95th percentile threshold for well-predicted metabolites is justified
- assess whether results from ten iterations of 10-fold cross-validation are properly aggregated (mean/standard deviation reported) and whether statistical significance is tested against baselines
- assess biological plausibility: verify that reported mean correlation improvements over baselines are consistent with the nonlinear modeling advantage of neural networks claimed in the paper

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Preprocess three paired microbiome-metabolomic datasets by filtering features present in <10% of samples and applying centered log-ratio transformation with pseudocount addition.
2. Optimize MiMeNet neural network architecture via nested 5-fold cross-validation, tuning layer size (32, 128, 512), number of layers (1–3), L2 penalty (0.0001–0.1), and dropout (0.1–0.5).
3. Train MiMeNet and three linear baselines (Elastic Net, CCA, Random Forest) using ten iterations of 10-fold cross-validation with ADAM optimization, ReLU activation, and early stopping.
4. Calculate mean Spearman correlation coefficient and identify well-predicted metabolites (SCC > 95th percentile of background distribution from 100 shuffled models) for each model and dataset.
5. Validation: Reported mean SCC and well-predicted metabolite counts must match published abstract values (IBD PRISM: 0.108→0.309 SCC, 198→366 metabolites; Cystic Fibrosis: 0.276→0.457, 104→143; Soil: -0.272→0.264, 4→29) within statistical noise (±SD reported in supplementary tables).
6. References: source article (DOI: 10.1371/journal.pcbi.1009021)

## Workflow Ports

**Inputs:**

- `ibd_prism_microbiome` — IBD (PRISM) microbiome abundance table
- `ibd_prism_metabolome` — IBD (PRISM) metabolomic abundance table
- `cf_microbiome` — Cystic Fibrosis microbiome abundance table
- `cf_metabolome` — Cystic Fibrosis metabolomic abundance table
- `soil_microbiome` — Soil biocrust microbiome abundance table
- `soil_metabolome` — Soil biocrust metabolomic abundance table

**Outputs:**

- `benchmark_results` — Mean SCC and well-predicted metabolite counts for all models and datasets
- `performance_metrics_table` — Tabular performance summary (SCC, PCC, MAE with ±SD)

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
