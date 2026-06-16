# Workflow Challenge: `coll_mimenet_workflow`


> MiMeNet is a multi-layer perceptron neural network framework that predicts metabolite abundances from microbiome features and identifies biologically meaningful microbe-metabolite interaction modules through feature attribution scoring and biclustering.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This paper presents MiMeNet, a neural network approach for modeling microbiome-metabolome relationships on three paired datasets (IBD, cystic fibrosis, and soil). Using 10 iterations of 10-fold cross-validation, MiMeNet achieves mean Spearman correlation coefficients of 0.309 for IBD (PRISM), 0.457 for cystic fibrosis, and 0.264 for soil datasets, and identifies 366, 143, and 29 well-predicted metabolites respectively, compared to 198, 104, and 4 for the linear regression model MelonnPan. On external validation using the entire IBD (PRISM) dataset to predict the IBD (External) test set, MiMeNet identifies 308 well-predicted metabolites with mean correlation of 0.275 for annotated metabolites, compared to 186 metabolites and correlation of 0.168 for MelonnPan. The paper demonstrates that training on all metabolites simultaneously improves prediction of annotated metabolites (mean Spearman correlation from 0.259 to 0.309, P < 10−47, with well-predicted metabolites increasing from 333 to 366 out of 466). Additionally, MiMeNet computes microbe-metabolite feature attribution scores from network weights and applies biclustering to organize microbes and metabolites into modules with shared interaction patterns, identifying eight microbial and eight metabolic modules in the IBD dataset where positive and negative attribution scores indicate the direction of microbe contributions to metabolite abundance prediction.

## Research questions

- Does MiMeNet achieve higher mean Spearman correlation coefficients and identify more well-predicted metabolites compared to MelonnPan, Random Forest, and CCA baselines across IBD (PRISM), Cystic Fibrosis, and Soil datasets using ten iterations of 10-fold cross-validation?
- What are the prediction correlation metrics achieved by a MiMeNet model trained on the full IBD (PRISM) dataset when evaluated on the held-out IBD (External) dataset?
- How does Olden's method derive microbe-metabolite feature attribution scores from MLPNN network weights, and how are these scores subsequently used to construct functional modules via biclustering?
- Does training MiMeNet on all metabolites (annotated + unannotated) improve prediction accuracy for annotated metabolites compared to training only on annotated metabolites?
- Does per-partition hyperparameter tuning improve MiMeNet's metabolite prediction performance compared to tuning hyperparameters once on the first partition?

## Methods overview

Preprocess three paired microbiome-metabolomic datasets by filtering features present in <10% of samples and applying centered log-ratio transformation with pseudocount addition. Optimize MiMeNet neural network architecture via nested 5-fold cross-validation, tuning layer size (32, 128, 512), number of layers (1–3), L2 penalty (0.0001–0.1), and dropout (0.1–0.5). Train MiMeNet and three linear baselines (Elastic Net, CCA, Random Forest) using ten iterations of 10-fold cross-validation with ADAM optimization, ReLU activation, and early stopping. Calculate mean Spearman correlation coefficient and identify well-predicted metabolites (SCC > 95th percentile of background distribution from 100 shuffled models) for each model and dataset. Validation: Reported mean SCC and well-predicted metabolite counts must match published abstract values (IBD PRISM: 0.108→0.309 SCC, 198→366 metabolites; Cystic Fibrosis: 0.276→0.457, 104→143; Soil: -0.272→0.264, 4→29) within statistical noise (±SD reported in supplementary tables). References: source article (DOI: 10.1371/journal.pcbi.1009021) Preprocess IBD (PRISM) and IBD (External) microbiome and metabolome data using centered log-ratio transformation, removing features in <10% of samples. Train a single MiMeNet MLPNN on the full IBD (PRISM) dataset (layer size 512, 1 hidden layer, L2 penalty 0.001, dropout 0.5) using ADAM optimizer with early stopping. Apply the trained model to IBD (External) test data to generate predicted metabolite abundances. Compute Spearman correlation coefficients between predicted and observed metabolite abundances for external validation. Identify well-predicted metabolites as those with SCC above the 95th percentile threshold derived from shuffled background distribution. Compare prediction performance to benchmark models (MelonnPan, Random Forest, Elastic Net, WGCNA) using identical evaluation metrics. Validation: External validation is successful if the mean SCC and count of well-predicted metabolites on IBD (External) are comparable to or exceed reported baseline methods and cross-validation results on held-out internal folds. References: source article (DOI: 10.1371/journal.pcbi.1009021) Extract trained MLPNN weight matrices across all hidden layers from 100 cross-validated models. Compute microbe-metabolite feature attribution scores via Olden's method (multiply weight matrices layer-by-layer) for each model. Average attribution matrices across all 100 models and apply 97.5 percentile threshold to identify significant microbe-metabolite associations. Normalize significant attribution scores to [-1, 1] range by dividing by the 97.5 percentile value. Apply hierarchical clustering with consensus resampling (k = 2–20) to microbes and metabolites independently, selecting optimal cluster numbers (k*, k**) where proportional change in consensus matrix area exceeds 0.025 threshold. Bicluster normalized attribution matrix using selected k* and k** to produce final microbe and metabolite functional modules. Compute inter-module interaction scores as average normalized attribution between all microbe-metabolite pairs in each module pair, filter edges to |score| ≥ 0.25 for network visualization. Validation: Confirm module membership is stable across cross-validated models, verify clustering dendrogram height consistency, and check that filtered interaction network contains ≥1 edges per non-singleton module pair. References: source article (DOI: 10.1371/journal.pcbi.1009021) Load and preprocess IBD (PRISM) microbiome and metabolomic data: apply centered log-ratio transformation (pseudocount=1), filter features <10% prevalence, segregate annotated from unannotated metabolites. Partition data into 10 iterations of 10-fold cross-validation; for each fold, reserve 10% for testing, allocate 80% to training and 20% to validation. Train two parallel MiMeNet MLPNN models per fold using identical architecture (1 hidden layer, 512 nodes, ReLU, L2 λ=0.001, dropout=0.5, ADAM optimizer, MSE loss): one predicting all metabolites, one predicting annotated metabolites only. Apply early stopping on validation loss (patience=40 epochs) to select final model weights for each fold; evaluate on held-out test set. Calculate Spearman correlation coefficient (SCC) between predicted and observed abundance for each annotated metabolite; aggregate across 100 runs (10 iterations × 10 folds) to obtain mean SCC per metabolite for each training regime. Generate scatterplot comparing mean SCCs and compute per-metabolite delta; calculate overall mean SCC, delta, and 95% confidence intervals. Validation: mean SCC on annotated metabolites when training on all metabolites must be ≥ mean SCC when training on annotated-only, confirming that unannotated metabolites provide shared signal; per-metabolite deltas are visualized to identify metabolites with largest performance gains from multi-task learning. References: source article (DOI: 10.1371/journal.pcbi.1009021) Load and preprocess paired microbiome-metabolome data: filter features present in <10% of samples and apply CLR transformation (with pseudocount 1) to metabolomic and applicable microbiome data. Tune hyperparameters once on first CV partition (Condition A): use nested 5-fold CV over grid {layer size: 32/128/512, hidden layers: 1–3, λ: log-uniform 0.0001–0.1, dropout: 0.1/0.3/0.5}; record optimal settings. Execute 10-fold CV twice in parallel: (A) reuse first-partition hyperparameters across all 10 folds; (B) retune hyperparameters independently for each fold. Train MLPNN models for each fold: use ReLU activation, ADAM optimizer, MSE loss, L2 regularization, dropout; apply early stopping when validation loss plateaus (no improvement ≥40 iterations). Calculate per-metabolite mean SCC and aggregate across all 10 folds for both conditions; count metabolites with SCC exceeding 95th percentile of background distribution (100 shuffled CV runs). Validation: compare mean SCC and well-predicted metabolite counts between Tune Once and Tune Every Partition; statistical significance and relative improvement in metabolite prediction sensitivity quantify the ablation effect. References: source article (DOI: 10.1371/journal.pcbi.1009021)

**Domain:** multi-omics

**Techniques:** deep-learning, machine-learning, random-forest, correlation-analysis, clustering

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MiMeNet more accurately predicts metabolite abundances than MelonnPan, with mean Spearman correlation coefficients increasing from 0.108 to 0.309 in the IBD (PRISM) dataset. _[grounded: MiMeNet]_
- **(finding)** In the cystic fibrosis dataset, MiMeNet achieves a mean correlation of 0.457 compared to MelonnPan's 0.410. _[grounded: MiMeNet]_
- **(finding)** MiMeNet identified 351 well-predicted metabolites in the IBD (PRISM) dataset compared to MelonnPan's 198. _[grounded: MiMeNet]_
- **(finding)** MiMeNet identified 143 well-predicted metabolites in the cystic fibrosis dataset while MelonnPan identified 104. _[grounded: MiMeNet]_
- **(finding)** MiMeNet identified 29 well-predicted metabolites in the soil dataset while MelonnPan identified 4. _[grounded: MiMeNet]_
- **(finding)** Multivariate learning increased well-predicted annotated metabolites from 333 to 366 in the IBD (PRISM) dataset. _[grounded: IBD_PRISM_dataset]_
- **(finding)** The Spearman correlation coefficients of annotated metabolites increased from 0.259 to 0.309 when using all metabolites to train MiMeNet, with significance p < 10^-47. _[grounded: MiMeNet]_
- **(finding)** 77.50% of metabolites (6857 of 8848) were well-predicted in the IBD (PRISM) dataset. _[grounded: IBD_PRISM_dataset]_
- **(finding)** 94.08% of metabolites (143 of 152) were well-predicted in the cystic fibrosis dataset. _[grounded: cystic_fibrosis_dataset]_
- **(finding)** 34.12% of metabolites (29 of 85) were well-predicted in the soil dataset.
- **(finding)** The cutoff Spearman correlation coefficient for well-predicted metabolites was 0.136 for the IBD (PRISM) dataset. _[grounded: IBD_PRISM_dataset]_
- **(finding)** The cutoff Spearman correlation coefficient for well-predicted metabolites was 0.129 for the cystic fibrosis dataset. _[grounded: cystic_fibrosis_dataset]_
- **(finding)** The cutoff Spearman correlation coefficient for well-predicted metabolites was 0.410 for the soil dataset.
- **(finding)** The IBD (PRISM) dataset contains 121 IBD patients and 34 controls. _[grounded: IBD_PRISM_dataset]_
- **(finding)** The IBD (PRISM) dataset contains 201 microbial features and 8848 metabolites. _[grounded: IBD_PRISM_dataset]_
- **(finding)** The cystic fibrosis dataset contains 657 microbial features and 168 metabolites. _[grounded: MiMeNet]_
- **(finding)** The soil dataset contains 446 microbial features and 85 metabolites.
- **(finding)** MiMeNet uses a multi-layer perceptron neural network (MLPNN) to model the community metabolome profile based on microbiome samples. _[grounded: MiMeNet]_
- **(finding)** MiMeNet benefits from multivariate learning by predicting the abundance of all metabolites at once, which facilitates prediction through shared information across different metabolites. _[grounded: MiMeNet]_
- **(finding)** MiMeNet uses biclustering to organize microbes and metabolites into modules based on their feature attribution patterns. _[grounded: MiMeNet]_
- **(finding)** The IBD (External) dataset includes 43 IBD patients and 20 control subjects. _[grounded: IBD_external_dataset]_
- **(finding)** The cystic fibrosis dataset contains 172 patients with cystic fibrosis. _[grounded: cystic_fibrosis_dataset]_
- **(finding)** MiMeNet identified 8 modules of microbes and 8 modules of metabolites in the IBD (PRISM) dataset. _[grounded: MiMeNet]_
- **(finding)** Four metabolite modules were enriched in healthy subjects in the IBD study.
- **(finding)** Three metabolite modules were enriched in IBD patients.
- **(finding)** Module 2 (healthy-enriched) contained medium-chain fatty acids, triterpenoids, and cholesterols.
- **(finding)** Module 7 (healthy-enriched) was mainly composed of short-chain fatty acids such as propionate, butyrate, and valeric acid.
- **(finding)** MiMeNet uses ReLU (rectified linear unit) as the activation function in the neural network. _[grounded: MiMeNet]_
- **(finding)** MiMeNet uses L2 regularization and dropout for regularization to prevent overfitting. _[grounded: MiMeNet]_
- **(finding)** MiMeNet training uses the ADAM optimizer and mean squared error (MSE) loss function. _[grounded: MiMeNet]_
- **(finding)** MiMeNet evaluation was conducted using 10 iterations of 10-fold cross-validation. _[grounded: MiMeNet]_
- **(finding)** MiMeNet uses early stopping to prevent overfitting during neural network training. _[grounded: MiMeNet]_
- **(finding)** The microbiome impacts host development, normal metabolic processes, and pathogenesis of various diseases.
- **(finding)** The gut microbiome has been linked to inflammatory bowel disease (IBD), obesity, and diabetes mellitus. _[grounded: IBD_component]_
- **(finding)** Bacterial metabolites play a central role in microbiome-host health interactions at a metabolic level.
- **(finding)** Strong associations between microbes and metabolites were found in gut and blood metabolomic profiles, and in the gut of patients with IBD.
- **(finding)** Identification of microbiome-metabolome interaction mechanisms through modeling is essential for understanding how the microbiome affects host health and for development of precise therapies.
- **(finding)** Early constraint-based stoichiometric modeling methods for microbiome-metabolome mapping have limitations due to reliance on annotated references.
- **(finding)** Several machine learning models have been developed to map metagenomic features to metabolites as both data types have become increasingly available.
- **(finding)** MelonnPan models each metabolite individually, missing shared information across metabolomic features that could boost prediction performance. _[grounded: MelonnPan_tool]_
- **(finding)** MiMeNet performs better than models trained on only the annotated metabolite set when noise is added to the training data. _[grounded: MiMeNet]_
- **(finding)** MiMeNet shows robust performance across different fold cross-validation settings (k=10, 5, 3, 2) in the IBD (PRISM) dataset. _[grounded: MiMeNet]_
- **(finding)** Triterpenoids such as oleanolic acid and maslinic acid have been shown to have anti-inflammatory effects and enhance intestinal tight junction integrity.
- **(finding)** Both cholesterols and medium-chain fatty acids have been noted to be depleted in subjects with IBD.
- **(finding)** Secondary bile acids (deoxycholic acid and lithocholic acid) have been found to be reduced in IBD patients.
- **(finding)** Short-chain fatty acids (propionate, butyrate, and valeric acid) have been shown to be protective against IBD.
- **(finding)** Primary bile acids bind to the farnesoid X receptor, which is linked to elevated immune response in IBD.
- **(finding)** N-acylethanolamines have been shown to alter the gut microbiome and potentially increase levels of lipopolysaccharides, causing inflammation.
- **(finding)** Sphingosine-1-phosphate is a signaling sphingolipid that has been implicated in increased inflammation of the gut.
- **(finding)** Long-chain fatty acids (eicosapentaenoic acid, arachidonic acid, and docosapentaenoic acid) have been implicated with IBD.
- **(finding)** Bacterial-derived sphingolipids have been shown to play a crucial role in the development of IBD through multiple signaling pathways.
- **(finding)** Bacteria such as Bacteroides, Clostridium, Eubacterium, and Ruminococcus produce enzymes responsible for conversion of conjugated bile acids to secondary bile acids.
- **(finding)** Triterpenoids have been explored as therapeutic options for IBD.
- **(finding)** The accuracy of metabolite prediction decreases as training dataset size is reduced in both IBD (PRISM) and cystic fibrosis datasets. _[grounded: IBD_PRISM_dataset]_
- **(finding)** Short-chain fatty acids, particularly butyrate, have been shown to be protective against inflammation in the gut and important for gut homeostasis.
- **(finding)** Five butyrate-producing microbes (Eubacterium biforme, Eubacterium hallii, Eubacterium rectale, Roseburia intestinalis, and Roseburia inulinivorans) were found in microbial module 6.
- **(finding)** Pairwise univariate correlation analysis identified only 12 significant correlations with butyrate, indicating that module-based analysis captures more biologically relevant interactions than pairwise methods.
- **(finding)** MiMeNet's modules capture biologically meaningful microbe-metabolite interactions by grouping microbes with similar functional effects on metabolites. _[grounded: MiMeNet]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- State-of-the-art linear models for individual metabolite predictions
- Predictive Reactive Metabolic Turnover (PRMT) as alternative to machine learning for mapping metagenomic features
- Constraint-based stoichiometric modeling using flux balance analysis as alternative to PRMT
- Neural network encoder-decoder (NED) as alternative machine learning approach
- Multivariate Elastic Net could be used instead of MLPNN
- Random Forest, Canonical Correlation Analysis, or Multivariate Elastic Net as alternative regression models
- Random forest as alternative to neural networks, though cannot provide feature attribution scores from network weights
- NED (Neural Encoder Decoder) as alternative predictive model for microbiome-metabolome relationships
- Regularized linear regression as used in MelonnPan for metabolite modeling
- Multivariate correlation analysis approaches for integrative omics analysis
- WGCNA for identifying clusters of metabolites
- MelonnPan for microbiome and metabolome integrative analysis
- mmvec for microbiome and metabolome relationships

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Non-negative weight constraints in NED diminish capability to capture interactions where some microbes negatively affect metabolites

## Steps

### Step `task_001`
- Title: Reproduce MiMeNet vs. linear-model prediction performance across three datasets
- Task kind: `reproduction`
- Task: Reproduce the mean Spearman correlation coefficients and well-predicted metabolite counts for MiMeNet and three baseline models (Elastic Net via MelonnPan, Canonical Correlation Analysis, Random Forest) on IBD (PRISM), Cystic Fibrosis, and Soil datasets using ten iterations of 10-fold cross-validation, matching reported abstract values.
- Inputs:
  - IBD (PRISM) microbiome and metabolomic data (121 IBD patients + 34 controls; 201 microbial species, 8848 metabolites)
  - Cystic Fibrosis lung sputum microbiome and metabolomic data (172 samples; 657 microbial genera, 168 metabolites)
  - Soil biocrust microbiome and metabolomic data (five time points, four successional stages; 466 microbes, 85 metabolites)
- Expected outputs:
  - Mean Spearman correlation coefficients (±SD) for MiMeNet and baseline models (Elastic Net, CCA, Random Forest) across ten iterations of 10-fold cross-validation on each dataset
  - Count of well-predicted metabolites (SCC > 95th percentile of background) for MiMeNet and baseline models on each dataset
  - Tabular summary of performance metrics (SCC, PCC, MAE) for all models and datasets with mean and standard deviation
- Tools: neural networks, neural networks (MLPNN with ReLU activation), MelonnPan (Elastic Net linear regression), Elastic Net regression, Random Forest regression, Canonical Correlation Analysis (CCA), ADAM optimizer, scikit-learn (Python)
- Landmark output files: preprocessed_ibd_prism_microbiome.csv, preprocessed_ibd_prism_metabolome.csv, hyperparameters_optimized.json, background_distribution_sccs.csv, well_predicted_metabolites_per_dataset.csv, mimenet_predictions_ibd_prism.csv
- Primary expected artifact: `benchmark_results_mimenet_baselines.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce MiMeNet external validation on the IBD (External) dataset
- Task kind: `reproduction`
- Task: Train a MiMeNet neural network model on the full IBD (PRISM) dataset and evaluate its metabolite abundance prediction performance on the held-out IBD (External) dataset, reporting Spearman correlation coefficient (SCC) and prediction accuracy metrics.
- Inputs:
  - IBD (PRISM) microbiome abundance data (201 microbial species, 121 IBD patients + 34 controls)
  - IBD (PRISM) metabolome abundance data (8848 metabolites, 121 IBD patients + 34 controls)
  - IBD (External) microbiome abundance data (two cohorts: 20 healthy subjects from LifeLines-DEEP + 43 subjects from Groningen)
  - IBD (External) metabolome abundance data (paired with external microbiome cohorts)
- Expected outputs:
  - Mean Spearman correlation coefficients (SCC) for metabolite prediction on IBD (External) dataset
  - Count of well-predicted metabolites on IBD (External) dataset (those with SCC above 95th percentile threshold)
  - Per-metabolite prediction correlations table for IBD (External) evaluation
  - Comparison metrics (SCC, prediction accuracy) versus benchmark models (MelonnPan, Random Forest, Elastic Net, WGCNA) on IBD (External) data
- Tools: MiMeNet, neural networks, ADAM optimizer, MelonnPan, Random Forest, Elastic Net, WGCNA, CCA (Canonical Correlation Analysis)
- Landmark output files: ibd_prism_preprocessed.csv, trained_mimenet_model.pkl, ibd_external_preprocessed.csv, predicted_metabolite_abundances_external.csv, per_metabolite_scc_external.csv, well_predicted_metabolites_external.txt
- Primary expected artifact: `ibd_external_validation_metrics.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct the Microbe-Metabolite Feature Attribution and Consensus-Clustering Module Construction pipeline
- Task kind: `component_reconstruction`
- Task: Implement the MiMeNet feature attribution and consensus clustering pipeline to derive microbe-metabolite interaction modules from trained MLPNN weights on the IBD (PRISM) dataset. Produce normalized feature attribution scores, identify significant microbe-metabolite pairs, and construct functional modules via biclustering.
- Inputs:
  - Trained MLPNN models (100 models from 10 iterations of 10-fold cross-validation with saved weight tensors)
  - Well-predicted metabolites list (metabolites with Spearman correlation coefficient above 95th percentile of background distribution)
  - IBD (PRISM) microbiome and metabolome data (centered log-ratio transformed, 201 microbes × 8848 metabolites)
  - Background feature attribution score distribution (from 100 models with randomly shuffled microbiome-metabolome samples)
- Expected outputs:
  - Normalized microbe-metabolite feature attribution score matrix (microbes × metabolites, values clipped to [-1, 1])
  - Microbial module assignments (list of microbe IDs grouped by cluster number k*)
  - Metabolite module assignments (list of metabolite IDs grouped by cluster number k**)
  - Module-based interaction network edge list (microbe module–metabolite module pairs with average normalized attribution scores, filtered to |score| ≥ 0.25)
- Tools: neural networks, WGCNA, Seaborn clustermap, Cytoscape, Python scikit-learn
- Landmark output files: attribution_scores_raw.npy, attribution_scores_normalized.csv, significant_microbes.txt, consensus_clustering_k_selection.png, microbe_clusters.csv, metabolite_clusters.csv
- Primary expected artifact: `microbe_metabolite_modules.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Analyze the benefit of multivariate (annotated + unannotated) training versus annotated-only training for metabolite prediction
- Task kind: `analysis`
- Task: Train MiMeNet neural network models on the IBD (PRISM) dataset using two distinct metabolite feature sets — all metabolites (annotated + unannotated) versus annotated metabolites only — and compare mean Spearman correlation coefficients on annotated metabolites to quantify the performance differential.
- Inputs:
  - IBD (PRISM) microbiome abundance data (OTU/ASV table, relative abundance format)
  - IBD (PRISM) metabolomic abundance data (LC-MS/MS, both annotated and unannotated metabolites)
  - Metabolite annotation status (binary flag indicating annotated versus unannotated metabolites)
- Expected outputs:
  - Scatterplot (PNG/PDF) comparing mean Spearman correlation coefficients for annotated metabolites: x-axis = SCC (MiMeNet trained on all metabolites), y-axis = SCC (MiMeNet trained on annotated metabolites only)
  - Numeric table (CSV) containing per-metabolite mean SCC values for both training regimes (all metabolites vs. annotated-only) and computed delta
  - Summary statistics: overall mean SCC (all metabolites regime), overall mean SCC (annotated-only regime), mean delta, and 95% CI or standard deviation
- Tools: MiMeNet, neural networks, ADAM optimizer, Python (scikit-learn, seaborn, or matplotlib for visualization)
- Landmark output files: clr_transformed_ibd_features.csv, model_fold_predictions_all_metabolites.csv, model_fold_predictions_annotated_only.csv, per_metabolite_scc_all.csv, per_metabolite_scc_annotated.csv
- Primary expected artifact: `scc_comparison_all_vs_annotated.csv`

### Step `task_005`
- Depends on: `task_001`
- Title: Extend MiMeNet evaluation to a shared vs. per-partition hyper-parameter tuning ablation
- Task kind: `extension`
- Task: Conduct a controlled ablation study comparing MiMeNet's 10-fold cross-validation performance under two hyperparameter tuning strategies—tuning once from the first partition versus per-partition tuning—on at least one microbiome-metabolome dataset. Report mean Spearman correlation coefficients (SCC) and counts of well-predicted metabolites for each condition to quantify sensitivity to tuning strategy.
- Inputs:
  - IBD (PRISM) microbiome (16S rRNA OTU abundance in relative abundance format) and paired metabolomic data (LC-MS/MS, 121 IBD patients + 34 controls, 201 microbial species, 8848 metabolites)
  - Cystic fibrosis lung sputum microbiome (16S rRNA, genus-level, 657 unique features from 172 samples) and paired metabolomic data (LC-MS/MS, 168 unique metabolites)
- Expected outputs:
  - Comparison table with mean SCC and standard deviation, and count of well-predicted metabolites (SCC >95th percentile background threshold) for Tune Once and Tune Every Partition conditions across 10-fold CV iterations
  - Scatterplot or line plot showing per-metabolite mean SCC correlation comparison between Tune Once and Tune Every Partition conditions, with well-predicted metabolite threshold indicated
- Tools: neural networks, MiMeNet
- Landmark output files: filtered_microbiome_abundance.csv, filtered_metabolome_abundance.csv, tune_once_scc_by_metabolite.csv, tune_every_partition_scc_by_metabolite.csv, background_scc_distribution.csv
- Primary expected artifact: `ablation_study_results.csv`

## Final expected outputs

- `Mean Spearman correlation coefficients (SCC) for metabolite prediction on IBD (External) dataset` (type: file, tolerance: hash)
- `Count of well-predicted metabolites on IBD (External) dataset (those with SCC above 95th percentile threshold)` (type: file, tolerance: hash)
- `Per-metabolite prediction correlations table for IBD (External) evaluation` (type: file, tolerance: hash)
- `Comparison metrics (SCC, prediction accuracy) versus benchmark models (MelonnPan, Random Forest, Elastic Net, WGCNA) on IBD (External) data` (type: file, tolerance: hash)
- `Normalized microbe-metabolite feature attribution score matrix (microbes × metabolites, values clipped to [-1, 1])` (type: file, tolerance: hash)
- `Microbial module assignments (list of microbe IDs grouped by cluster number k*)` (type: file, tolerance: hash)
- `Metabolite module assignments (list of metabolite IDs grouped by cluster number k**)` (type: file, tolerance: hash)
- `Module-based interaction network edge list (microbe module–metabolite module pairs with average normalized attribution scores, filtered to |score| ≥ 0.25)` (type: file, tolerance: hash)
- `Scatterplot (PNG/PDF) comparing mean Spearman correlation coefficients for annotated metabolites: x-axis = SCC (MiMeNet trained on all metabolites), y-axis = SCC (MiMeNet trained on annotated metabolites only)` (type: file, tolerance: hash)
- `Numeric table (CSV) containing per-metabolite mean SCC values for both training regimes (all metabolites vs. annotated-only) and computed delta` (type: file, tolerance: hash)
- `Summary statistics: overall mean SCC (all metabolites regime), overall mean SCC (annotated-only regime), mean delta, and 95% CI or standard deviation` (type: file, tolerance: hash)
- `Comparison table with mean SCC and standard deviation, and count of well-predicted metabolites (SCC >95th percentile background threshold) for Tune Once and Tune Every Partition conditions across 10-fold CV iterations` (type: file, tolerance: hash)
- `Scatterplot or line plot showing per-metabolite mean SCC correlation comparison between Tune Once and Tune Every Partition conditions, with well-predicted metabolite threshold indicated` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: mixed — per-step.** Closed steps must reproduce (rubrics above bind on them); open steps are judged by **SCIENTIFIC_VALIDITY** (below). Invariants bind everywhere; different is not wrong on the open steps.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** intermediate

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_mimenet_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Mean Spearman correlation coefficients (SCC) for metabolite prediction on IBD (External) dataset": "<locator>",
    "Count of well-predicted metabolites on IBD (External) dataset (those with SCC above 95th percentile threshold)": "<locator>",
    "Per-metabolite prediction correlations table for IBD (External) evaluation": "<locator>",
    "Comparison metrics (SCC, prediction accuracy) versus benchmark models (MelonnPan, Random Forest, Elastic Net, WGCNA) on IBD (External) data": "<locator>",
    "Normalized microbe-metabolite feature attribution score matrix (microbes \u00d7 metabolites, values clipped to [-1, 1])": "<locator>",
    "Microbial module assignments (list of microbe IDs grouped by cluster number k*)": "<locator>",
    "Metabolite module assignments (list of metabolite IDs grouped by cluster number k**)": "<locator>",
    "Module-based interaction network edge list (microbe module\u2013metabolite module pairs with average normalized attribution scores, filtered to |score| \u2265 0.25)": "<locator>",
    "Scatterplot (PNG/PDF) comparing mean Spearman correlation coefficients for annotated metabolites: x-axis = SCC (MiMeNet trained on all metabolites), y-axis = SCC (MiMeNet trained on annotated metabolites only)": "<locator>",
    "Numeric table (CSV) containing per-metabolite mean SCC values for both training regimes (all metabolites vs. annotated-only) and computed delta": "<locator>",
    "Summary statistics: overall mean SCC (all metabolites regime), overall mean SCC (annotated-only regime), mean delta, and 95% CI or standard deviation": "<locator>",
    "Comparison table with mean SCC and standard deviation, and count of well-predicted metabolites (SCC >95th percentile background threshold) for Tune Once and Tune Every Partition conditions across 10-fold CV iterations": "<locator>",
    "Scatterplot or line plot showing per-metabolite mean SCC correlation comparison between Tune Once and Tune Every Partition conditions, with well-predicted metabolite threshold indicated": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
