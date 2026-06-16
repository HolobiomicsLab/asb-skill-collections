# SciTask Card: Analyze the benefit of multivariate (annotated + unannotated) training versus annotated-only training for metabolite prediction

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T07:36:08.260853+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_mimenet`
- Domain: `bioinformatics`
- Subtask categories: `model-training`, `data-analysis`, `benchmark-evaluation`
- DOI: `10.1371/journal.pcbi.1009021`
- GitHub: `biobakery/melonnpan`
- Input from: `task_001`

## Classification

- Task kind: `analysis`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `microbiome-metabolomics`, `artificial-intelligence`, `multi-omics-integration`
- Techniques: `deep-learning`, `machine-learning`, `random-forest`, `correlation-analysis`, `clustering`

## Research Question
Does training MiMeNet on all metabolites (annotated + unannotated) improve prediction accuracy for annotated metabolites compared to training only on annotated metabolites?

## Connected Finding
Training MiMeNet on all metabolites improved mean Spearman correlation coefficients for annotated metabolites from 0.259 to 0.309 (P < 10−47), with well-predicted metabolites increasing from 333 to 366 out of 466 annotated metabolites in the IBD (PRISM) dataset.

## Task Description
Train MiMeNet neural network models on the IBD (PRISM) dataset using two distinct metabolite feature sets — all metabolites (annotated + unannotated) versus annotated metabolites only — and compare mean Spearman correlation coefficients on annotated metabolites to quantify the performance differential.

## Inputs
- IBD (PRISM) microbiome abundance data (OTU/ASV table, relative abundance format)
- IBD (PRISM) metabolomic abundance data (LC-MS/MS, both annotated and unannotated metabolites)
- Metabolite annotation status (binary flag indicating annotated versus unannotated metabolites)

## Expected Outputs
- Scatterplot (PNG/PDF) comparing mean Spearman correlation coefficients for annotated metabolites: x-axis = SCC (MiMeNet trained on all metabolites), y-axis = SCC (MiMeNet trained on annotated metabolites only)
- Numeric table (CSV) containing per-metabolite mean SCC values for both training regimes (all metabolites vs. annotated-only) and computed delta
- Summary statistics: overall mean SCC (all metabolites regime), overall mean SCC (annotated-only regime), mean delta, and 95% CI or standard deviation

## Expected Output File

- `scc_comparison_all_vs_annotated.csv`

## Landmark Outputs

- `clr_transformed_ibd_features.csv`
- `model_fold_predictions_all_metabolites.csv`
- `model_fold_predictions_annotated_only.csv`
- `per_metabolite_scc_all.csv`
- `per_metabolite_scc_annotated.csv`

## Tools
- MiMeNet
- neural networks
- ADAM optimizer
- Python (scikit-learn, seaborn, or matplotlib for visualization)

## Skills
- microbe-metabolite-feature-selection-by-annotation-status
- neural-network-hyperparameter-tuning-for-regression
- spearman-correlation-coefficient-calculation-cross-validation
- feature-attribution-score-interpretation-neural-networks
- multi-regime-model-performance-comparison-visualization
- data-transformation-centered-log-ratio-with-pseudocounts

## Workflow Description
1. Load IBD (PRISM) microbiome and metabolomic data, apply centered log-ratio transformation with pseudocount of 1, and filter features present in <10% of samples. 2. Split data into training (80%) and validation (20%) sets, then perform 10 iterations of 10-fold cross-validation. 3. For each iteration-fold, train a separate MiMeNet MLPNN model (using optimal hyperparameters: 512-node single hidden layer, L2 penalty λ=0.001, dropout=0.5, ReLU activation) on the complete feature set (all metabolites), using ADAM optimizer and mean squared error loss with early stopping (patience=40 epochs). 4. In parallel, train an identically configured MiMeNet model using only annotated metabolites as outputs. 5. Evaluate both models on the held-out test fold; calculate Spearman correlation coefficient (SCC) between predicted and observed abundance for each annotated metabolite across all 100 model runs (10 iterations × 10 folds). 6. Compute mean SCC per annotated metabolite for each training regime and generate scatterplot comparing the two conditions; calculate per-metabolite delta (SCC_all − SCC_annotated_only) and overall mean delta.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `mimenet.pdf` | main_article | True |

## Missing Information
- The discussion states that MiMeNet prediction on annotated metabolites 'benefited from including tasks of predicting the rest of the unannotated metabolites' but does not provide the exact numeric correlation values or deltas for annotated metabolites in the two training scenarios.
- The discussion acknowledges that 'not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation' but does not specify what fraction of the annotated metabolite set falls into this category or how this affects the comparison.
- The section references Fig 2D–2F to support the claim about improved prediction of annotated metabolites when training on all metabolites, but the referenced figure images and their numeric legends are not included in the provided discussion text.

## Domain Knowledge
- Centered log-ratio (CLR) transformation with pseudocount=1 prevents log(0) errors in compositional microbiome-metabolome abundance data; relative abundance inputs (IBD microbes) bypass CLR conversion per protocol.
- Early stopping with patience=40 epochs on validation loss prevents overfitting during MLPNN training when dropout and L2 regularization are applied; optimal architecture for IBD (PRISM) is a single 512-node hidden layer with ReLU activation.
- Spearman correlation coefficient (SCC) is robust to non-linear monotonic relationships and suitable for abundance predictions; mean SCC across test folds serves as the primary performance metric with 95th percentile background threshold to define well-predicted metabolites.
- Annotated metabolites have chemical structure and functional assignment; unannotated metabolites are mass-to-charge-ratio features without confirmed identity. Training on all metabolites may capture co-abundance patterns that improve prediction of annotated metabolites; training on annotated-only baseline isolates signal from known compounds.
- 10 iterations of 10-fold cross-validation (100 total model fits) provide robust averaging of SCC values; per-fold hold-out test sets ensure unbiased correlation estimates independent of hyperparameter tuning partition.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Numeric table (CSV) containing per-metabolite mean SCC values for both training regimes (all metabolites vs. annotated-only) and computed delta.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Does training MiMeNet on all metabolites (annotated + unannotated) improve prediction accuracy for annotated metabolites compared to training only on annotated metabolites?: 'by training on the entire set of metabolites, the number of well-predicted metabolites for the annotated set increased from 333 to 366. Additionally, the SCCs of the annotated metabolites'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] Training MiMeNet on all metabolites improved mean Spearman correlation coefficients for annotated metabolites from 0.259 to 0.309 (P < 10−47), with well-predicted metabolites increasing from 333 to 366 out of 466 annotated metabolites in the IBD (PRISM) dataset.: 'by training on the entire set of metabolites, the number of well-predicted metabolites for the annotated set increased from 333 to 366. Additionally, the SCCs of the annotated metabolites'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] IBD (PRISM) microbiome abundance data (OTU/ASV table, relative abundance format): 'The first dataset was taken from a published study of patients with inflammatory bowel disease (IBD). It includes one cohort from the Prospective Registry (PRISM), which enrolled patients with a'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] IBD (PRISM) metabolomic abundance data (LC-MS/MS, both annotated and unannotated metabolites): 'A total of 201 microbial species and 8848 metabolites were identified for the IBD (PRISM) and IBD (External) datasets'
- `ev_005` from `agent2_synthesis` (agent2_traced): [results] Metabolite annotation status (binary flag indicating annotated versus unannotated metabolites): 'trained only on the annotated metabolites'
- `ev_006` from `agent2_synthesis` (agent2_traced): [results] Scatterplot (PNG/PDF) comparing mean Spearman correlation coefficients for annotated metabolites: x-axis = SCC (MiMeNet trained on all metabolites), y-axis = SCC (MiMeNet trained on annotated metabolites only): 'Scatterplot of mean predicted Spearman's correlation over 10 iterations of 10-fold cross-validation for each metabolite between MiMeNet'
- `ev_007` from `agent2_synthesis` (agent2_traced): [results] Numeric table (CSV) containing per-metabolite mean SCC values for both training regimes (all metabolites vs. annotated-only) and computed delta: 'mean SCC and (B) mean PCC values of the members within the module'
- `ev_008` from `agent2_synthesis` (agent2_traced): [results] Summary statistics: overall mean SCC (all metabolites regime), overall mean SCC (annotated-only regime), mean delta, and 95% CI or standard deviation: 'the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundances'
- `ev_009` from `agent2_synthesis` (agent2_traced): [results] MiMeNet: 'MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome based on a microbiome'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] neural networks: 'An MLPNN model is composed of multiple fully connected hidden layers composed of perceptrons'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] ADAM optimizer: 'MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] Python (scikit-learn, seaborn, or matplotlib for visualization): 'using Seaborn's clustermap function in Python'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] The discussion states that MiMeNet prediction on annotated metabolites 'benefited from including tasks of predicting the rest of the unannotated metabolites' but does not provide the exact numeric correlation values or deltas for annotated metabolites in the two training scenarios.: 'Indeed, our results of the IBD data demonstrated that the MiMeNet prediction on the set of the annotated metabolites benefited from including tasks of predicting the rest of the unannotated'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] The discussion acknowledges that 'not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation' but does not specify what fraction of the annotated metabolite set falls into this category or how this affects the comparison.: 'We note that since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] The section references Fig 2D–2F to support the claim about improved prediction of annotated metabolites when training on all metabolites, but the referenced figure images and their numeric legends are not included in the provided discussion text.: 'Indeed, our results of the IBD data demonstrated that the MiMeNet prediction on the set of the annotated metabolites benefited from including tasks of predicting the rest of the unannotated'

## Evaluation Strategy
### Direct Checks
- file_exists: verify that IBD (PRISM) dataset microbiome and metabolome input files are accessible in the MiMeNet repository or cited deposit (Zenodo/GEO/MetaboLights)
- script_runs: execute MiMeNet training pipeline with configuration parameter 'train_on_all_metabolites=True' on IBD (PRISM) dataset and verify no runtime errors
- script_runs: execute MiMeNet training pipeline with configuration parameter 'train_on_all_metabolites=False' (annotated only) on IBD (PRISM) dataset and verify no runtime errors
- output_matches_reference: mean Spearman correlation on annotated metabolites for all-metabolites model is between 0.45 and 0.50 (robust to minor numerical precision differences), matching Fig 2D–2F context or SI Table
- output_matches_reference: mean Spearman correlation on annotated metabolites for annotated-only model is lower than all-metabolites model, with delta (improvement) reported in Fig 2D–2F or supplementary materials
- file_format_is: scatterplot output file (PNG/PDF/SVG) exists and contains two-dimensional visualization of prediction correlations across annotated metabolites for both training conditions
- contains_substring: Fig 2D–2F caption or associated text explicitly states numeric mean correlation values and/or delta improvements for annotated metabolites across the two training regimes

### Expert Review
- assess whether the reported improvement in mean Spearman correlation when including unannotated metabolites during training is biologically plausible and consistent with the stated hypothesis that shared information across metabolites improves prediction
- evaluate whether the comparison controls for confounding factors (network architecture, hyperparameters, cross-validation scheme, random seed) between the two training conditions to isolate the effect of metabolite set composition
- determine whether the annotated metabolite set is clearly defined and reproducibly extracted from the input metabolomic data, and verify no data leakage or label contamination between conditions

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Load and preprocess IBD (PRISM) microbiome and metabolomic data: apply centered log-ratio transformation (pseudocount=1), filter features <10% prevalence, segregate annotated from unannotated metabolites.
2. Partition data into 10 iterations of 10-fold cross-validation; for each fold, reserve 10% for testing, allocate 80% to training and 20% to validation.
3. Train two parallel MiMeNet MLPNN models per fold using identical architecture (1 hidden layer, 512 nodes, ReLU, L2 λ=0.001, dropout=0.5, ADAM optimizer, MSE loss): one predicting all metabolites, one predicting annotated metabolites only.
4. Apply early stopping on validation loss (patience=40 epochs) to select final model weights for each fold; evaluate on held-out test set.
5. Calculate Spearman correlation coefficient (SCC) between predicted and observed abundance for each annotated metabolite; aggregate across 100 runs (10 iterations × 10 folds) to obtain mean SCC per metabolite for each training regime.
6. Generate scatterplot comparing mean SCCs and compute per-metabolite delta; calculate overall mean SCC, delta, and 95% confidence intervals.
7. Validation: mean SCC on annotated metabolites when training on all metabolites must be ≥ mean SCC when training on annotated-only, confirming that unannotated metabolites provide shared signal; per-metabolite deltas are visualized to identify metabolites with largest performance gains from multi-task learning.
8. References: source article (DOI: 10.1371/journal.pcbi.1009021)

## Workflow Ports

**Inputs:**

- `ibd_microbiome_ra` — IBD (PRISM) microbiome relative abundance table ← `task_001/benchmark_results`
- `ibd_metabolome_all` — IBD (PRISM) metabolomic data (all metabolites, annotated + unannotated)
- `metabolite_annotation_flags` — Binary vector indicating annotated metabolites in IBD (PRISM) dataset

**Outputs:**

- `scc_comparison_plot` — Scatterplot comparing mean SCC by training regime
- `per_metabolite_scc_table` — Per-metabolite SCC and delta values (CSV)
- `summary_statistics` — Overall mean SCC, delta, and confidence intervals

**Used:** `urn:asb:port:task_001/benchmark_results`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
