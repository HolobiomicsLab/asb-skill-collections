# SciTask Card: Extend MiMeNet evaluation to a shared vs. per-partition hyper-parameter tuning ablation

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T07:36:08.260853+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_mimenet`
- Domain: `bioinformatics`
- Subtask categories: `model-training`, `benchmark-evaluation`, `statistical-analysis`
- DOI: `10.1371/journal.pcbi.1009021`
- GitHub: `biobakery/melonnpan`
- Input from: `task_001`

## Classification

- Task kind: `extension`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `microbiome-metabolomics`, `artificial-intelligence`, `multi-omics-integration`
- Techniques: `deep-learning`, `machine-learning`, `random-forest`, `correlation-analysis`, `clustering`

## Research Question
Does per-partition hyperparameter tuning improve MiMeNet's metabolite prediction performance compared to tuning hyperparameters once on the first partition?

## Connected Finding
Using the IBD (PRISM) dataset, per-partition tuning increased mean SCC while cystic fibrosis showed a slight decrease, yet 141 of 143 significantly correlated metabolites were still identified with shared hyperparameters.

## Task Description
Conduct a controlled ablation study comparing MiMeNet's 10-fold cross-validation performance under two hyperparameter tuning strategies—tuning once from the first partition versus per-partition tuning—on at least one microbiome-metabolome dataset. Report mean Spearman correlation coefficients (SCC) and counts of well-predicted metabolites for each condition to quantify sensitivity to tuning strategy.

## Inputs
- IBD (PRISM) microbiome (16S rRNA OTU abundance in relative abundance format) and paired metabolomic data (LC-MS/MS, 121 IBD patients + 34 controls, 201 microbial species, 8848 metabolites)
- Cystic fibrosis lung sputum microbiome (16S rRNA, genus-level, 657 unique features from 172 samples) and paired metabolomic data (LC-MS/MS, 168 unique metabolites)

## Expected Outputs
- Comparison table with mean SCC and standard deviation, and count of well-predicted metabolites (SCC >95th percentile background threshold) for Tune Once and Tune Every Partition conditions across 10-fold CV iterations
- Scatterplot or line plot showing per-metabolite mean SCC correlation comparison between Tune Once and Tune Every Partition conditions, with well-predicted metabolite threshold indicated

## Expected Output File

- `ablation_study_results.csv`

## Landmark Outputs

- `filtered_microbiome_abundance.csv`
- `filtered_metabolome_abundance.csv`
- `tune_once_scc_by_metabolite.csv`
- `tune_every_partition_scc_by_metabolite.csv`
- `background_scc_distribution.csv`

## Tools
- neural networks
- MiMeNet

## Skills
- microbiome-metabolome-data-preprocessing-clr-transformation
- neural-network-hyperparameter-tuning-cross-validation
- metabolite-prediction-correlation-analysis
- background-distribution-null-hypothesis-testing
- ablation-study-design-and-interpretation

## Workflow Description
1. Load raw microbiome (relative or CLR-transformed abundance) and metabolomic data (LC-MS/MS or 16S rRNA-derived, CLR-transformed) from the IBD (PRISM) or cystic fibrosis dataset, filtering out features present in <10% of samples. 2. Execute 10-fold cross-validation in which (Condition A) hyperparameters (layer size, number of layers, L2 penalty λ, dropout rate) are tuned once on the first training partition using nested 5-fold cross-validation over a grid (layer size ∈ {32, 128, 512}, λ evenly spaced on log scale 0.0001–0.1, dropout ∈ {0.1, 0.3, 0.5}) and reused for all remaining 9 folds. 3. In parallel, execute 10-fold cross-validation in which (Condition B) hyperparameters are re-tuned on each of the 10 training partitions using the same nested grid search. 4. For both conditions, train MLPNN models with ReLU activation, L2 regularization, dropout, ADAM optimizer, and MSE loss; apply early stopping when validation loss does not improve within 40 iterations. 5. Calculate SCC between predicted and observed metabolite abundances for each fold and both conditions; compute mean SCC across all folds. 6. Generate a background SCC distribution by shuffling microbiome and metabolome data independently, re-running 10-fold cross-validation 100 times, and identifying metabolites with SCC >95th percentile as well-predicted. 7. Count well-predicted metabolites under each condition and compare mean SCC and metabolite counts to quantify sensitivity to tuning strategy.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `mimenet.pdf` | main_article | True |

## Missing Information
- No specification of which hyperparameters are tuned 'once' in the Tune Once condition versus tuned 'every partition' in the Tune Every Partition condition; number of hidden layers, hidden layer sizes, L2 regularization penalty, and learning rate tuning strategy across folds not detailed
- No explicit reporting of mean SCC and well-predicted metabolite counts separately stratified by ablation condition (Tune Once vs. Tune Every Partition); only aggregate cross-dataset results provided in abstract
- No documentation of the number of iterations of 10-fold CV performed under each ablation condition or whether the same data splits are reused across conditions for fair comparison
- Computational cost, runtime, and convergence properties of Tune Once versus Tune Every Partition not reported; no analysis of whether tuning every partition provides improvement commensurate with increased training time
- No specification of whether ablation study is restricted to one dataset (IBD PRISM) or applied across all three datasets (IBD PRISM, Cystic Fibrosis, Soil); unclear if sensitivity to tuning strategy is dataset-dependent

## Domain Knowledge
- CLR (centered log-ratio) transformation is standard for compositional microbiome-metabolome data to address zero-inflation and compositional constraints; a pseudocount of 1 must be added before log transformation to avoid log(0).
- Well-predicted metabolites are identified using the 95th percentile of a background SCC distribution generated by shuffling microbiome and metabolome data independently; this threshold is empirically determined and controls false-discovery.
- Hyperparameter tuning sensitivity is assessed by comparing results from tuning once (on first partition only, reused across all folds) versus per-partition tuning; per-partition tuning risks overfitting to individual folds while tuning once risks suboptimal parameters for subsequent folds.
- Early stopping should be triggered when validation loss fails to improve within 40 iterations to prevent overfitting during neural network training; the model weights are reverted to the best validation epoch.
- ADAM optimizer with MSE loss, ReLU activation, L2 regularization (λ), and dropout are standard regularization strategies for MLPNN; the grid search ranges λ from 0.0001 to 0.1 on log scale and dropout from 0.1 to 0.5.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Comparison table with mean SCC and standard deviation, and count of well-predicted metabolites (SCC >95th percentile background threshold) for Tune Once and Tune Every Partition conditions across 10-fold CV iterations.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Does per-partition hyperparameter tuning improve MiMeNet's metabolite prediction performance compared to tuning hyperparameters once on the first partition?: 'we evaluated the IBD (PRISM) and cystic fibrosis datasets using a single shared hyper-parameter set learned on the first partition against cross-validation where hyper-parameters are tuned every'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] Using the IBD (PRISM) dataset, per-partition tuning increased mean SCC while cystic fibrosis showed a slight decrease, yet 141 of 143 significantly correlated metabolites were still identified with shared hyperparameters.: 'Using the IBD (PRISM) dataset, we observed an increase in mean SCC when tuning every iteration, while in the cystic fibrosis dataset, we observed a decrease in mean SCC. Despite the decrease of'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] IBD (PRISM) microbiome (16S rRNA OTU abundance in relative abundance format) and paired metabolomic data (LC-MS/MS, 121 IBD patients + 34 controls, 201 microbial species, 8848 metabolites): 'The first dataset was taken from a published study of patients with inflammatory bowel disease (IBD) [15]. It includes one cohort from the Prospective Registry (PRISM), which enrolled patients with a'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Cystic fibrosis lung sputum microbiome (16S rRNA, genus-level, 657 unique features from 172 samples) and paired metabolomic data (LC-MS/MS, 168 unique metabolites): 'The second dataset was taken from a study that collected 172 lung sputum samples from patients with cystic fibrosis. Microbial features were generated using 16S rRNA gene sequencing and abundance was'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Comparison table with mean SCC and standard deviation, and count of well-predicted metabolites (SCC >95th percentile background threshold) for Tune Once and Tune Every Partition conditions across 10-fold CV iterations: 'Using 10 iterations of 10-fold cross-validation, evaluations using shared hyper-parameters tuned from the first partition (Tune Once) were compared against evaluations with tuning for each partition'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Scatterplot or line plot showing per-metabolite mean SCC correlation comparison between Tune Once and Tune Every Partition conditions, with well-predicted metabolite threshold indicated: 'evaluations using shared hyper-parameters tuned from the first partition (Tune Once) were compared against evaluations with tuning for each partition (Tune Every Partition)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [abstract] neural networks: 'we present MiMeNet, a neural network framework for modeling microbe-metabolite relationships'
- `ev_008` from `agent2_synthesis` (agent2_traced): [results] MiMeNet: 'MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome based on a microbiome'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] No specification of which hyperparameters are tuned 'once' in the Tune Once condition versus tuned 'every partition' in the Tune Every Partition condition; number of hidden layers, hidden layer sizes, L2 regularization penalty, and learning rate tuning strategy across folds not detailed: 'The network architecture in MiMeNet is first determined for each paired dataset by tuning the hyperparameters for the number and size of the hidden layers, the L2 regularization penalty parameter,'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] No explicit reporting of mean SCC and well-predicted metabolite counts separately stratified by ablation condition (Tune Once vs. Tune Every Partition); only aggregate cross-dataset results provided in abstract: 'MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264)'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] No documentation of the number of iterations of 10-fold CV performed under each ablation condition or whether the same data splits are reused across conditions for fair comparison: 'Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets'
- `ev_012` from `agent2_synthesis` (agent2_traced): [other] Computational cost, runtime, and convergence properties of Tune Once versus Tune Every Partition not reported; no analysis of whether tuning every partition provides improvement commensurate with increased training time: 'MiMeNet then trains multiple network models using 10-fold cross-validation'
- `ev_013` from `agent2_synthesis` (agent2_traced): [results] No specification of whether ablation study is restricted to one dataset (IBD PRISM) or applied across all three datasets (IBD PRISM, Cystic Fibrosis, Soil); unclear if sensitivity to tuning strategy is dataset-dependent: 'The first dataset was taken from a published study of patients enrolled in PRISM (the Prospective Registry in Inflammatory Bowel Disease Study at Massachusetts General Hospital) containing 121 IBD'

## Evaluation Strategy
### Direct Checks
- file_exists: MiMeNet package or evaluation code at https://github.com/YDaiLab/MiMeNet
- script_runs: MiMeNet 10-fold CV pipeline executable on IBD (PRISM) dataset with hyperparameter configuration input
- output_matches_reference: mean SCC values for IBD (PRISM) dataset reported in article abstract (increase from 0.108 to 0.309), robust to random seed variation within ±0.01
- row_count_equals: well-predicted metabolite count for IBD (PRISM) dataset matches article abstract (increase from 198 to 366), allowing ±5 metabolites due to threshold sensitivity
- value_in_range: SCC values for both Tune Once and Tune Every Partition conditions fall between -1.0 and 1.0
- contains_substring: output report includes labeled fields for 'mean_scc_tune_once', 'mean_scc_tune_every_partition', 'well_predicted_count_tune_once', 'well_predicted_count_tune_every_partition'
- format_is: ablation output structured as table or CSV with columns: condition_name, mean_scc, std_scc, well_predicted_metabolite_count, fold_identifiers

### Expert Review
- Verify that hyperparameter tuning strategy ('Tune Once' vs. 'Tune Every Partition') is implemented as described in methods section and produces materially different network configurations across folds
- Assess whether reported SCC improvements and well-predicted metabolite counts are biologically plausible given dataset size (121 IBD PRISM samples) and feature dimensionality
- Evaluate whether ablation design isolates the effect of tuning strategy alone without confounding from random initialization, cross-validation splitting strategy, or other hyperparameter changes
- Confirm that well-predicted metabolite threshold (95th percentile of background distribution) is applied consistently across both ablation conditions and computed from shuffled dataset
- Judge whether performance difference between Tune Once and Tune Every Partition is substantial enough to warrant the computational cost difference and support the article's claims about hyperparameter sensitivity

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load and preprocess paired microbiome-metabolome data: filter features present in <10% of samples and apply CLR transformation (with pseudocount 1) to metabolomic and applicable microbiome data.
2. Tune hyperparameters once on first CV partition (Condition A): use nested 5-fold CV over grid {layer size: 32/128/512, hidden layers: 1–3, λ: log-uniform 0.0001–0.1, dropout: 0.1/0.3/0.5}; record optimal settings.
3. Execute 10-fold CV twice in parallel: (A) reuse first-partition hyperparameters across all 10 folds; (B) retune hyperparameters independently for each fold.
4. Train MLPNN models for each fold: use ReLU activation, ADAM optimizer, MSE loss, L2 regularization, dropout; apply early stopping when validation loss plateaus (no improvement ≥40 iterations).
5. Calculate per-metabolite mean SCC and aggregate across all 10 folds for both conditions; count metabolites with SCC exceeding 95th percentile of background distribution (100 shuffled CV runs).
6. Validation: compare mean SCC and well-predicted metabolite counts between Tune Once and Tune Every Partition; statistical significance and relative improvement in metabolite prediction sensitivity quantify the ablation effect.
7. References: source article (DOI: 10.1371/journal.pcbi.1009021)

## Workflow Ports

**Inputs:**

- `microbiome_abundance` — Microbiome abundance matrix (OTU/genus-level, samples × features) ← `task_001/benchmark_results`
- `metabolome_abundance` — Metabolome abundance matrix (samples × metabolites, LC-MS/MS-derived)

**Outputs:**

- `ablation_results_table` — Ablation study results: mean SCC, SD, well-predicted metabolite counts per condition
- `metabolite_scc_comparison_plot` — Scatterplot: per-metabolite SCC comparison Tune Once vs Tune Every Partition

**Used:** `urn:asb:port:task_001/benchmark_results`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
