# Workflow Challenge: `coll_mamsi_workflow`


> MAMSI is a Python framework for integrating multi-assay LC-MS metabolomics datasets and identifying statistically significant features through multi-block partial least squares (MB-PLS) analysis coupled with structural clustering based on mass-to-charge ratio and retention time.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MAMSI provides tools for analyzing untargeted multi-assay LC-MS metabolomics datasets through multi-block PLS discriminant analysis to identify statistically significant predictive features. The framework implements multi-block variable importance in projection (MB-VIP) with permutation testing to derive empirical p-values for feature ranking. Significant features are then organized into structural clusters using retention time windows and mass-to-charge ratio tolerances; the clustering mechanism searches for isotopologue signatures (mass differences of 1.00335 Da), common adduct signatures via hypothetical neutral mass matching, and cross-assay links. The structural relationships between features can be visualized as a network graph and exported as a NetworkX object for interactive analysis in Cytoscape. The framework was tested and demonstrated on metabolomics phenotyping data from the AddNeuroMed cohort but is designed for general applicability to LC-MS datasets.

## Research questions

- What are the model performance metrics and statistically significant metabolomic features identified when applying the full MAMSI pipeline (MB-PLS model fitting, MB-VIP feature selection, and cross-validation) to multi-assay LC-MS metabolomics datasets?
- How does the MamsiStructSearch module group statistically significant LC-MS features into structural clusters using mass-to-charge ratio and retention time information?
- How does MAMSI convert structural cluster assignments into an interactive network graph representation suitable for visualization and analysis?
- How do structural cluster outputs (cluster count and size distribution) differ between using all adducts versus only the most-common adducts in the MAMSI framework's adduct signature search?
- Does the silhouette flattening method produce different structural cluster assignments compared to the default constant-threshold method in the MAMSI structural clustering pipeline?

## Methods overview

Load multi-assay LC-MS intensity data (HPOS, LPOS, LNEG) and clinical outcome variable; apply assay-specific column name prefixes for downstream traceability. Partition data into training (90%) and test (10%) sets using stratified random split, maintaining block alignment. Fit multiblock PLS discriminant model on training data using NIPALS algorithm with unit-variance standardization; compute super-scores, block loadings, and regression coefficients. Estimate optimal latent variable count via k-fold cross-validation (k=5) using AUC metric; identify plateau at lowest LV count with stable validation performance. Evaluate final model on held-out test set; record classification metrics (accuracy, recall, specificity, F1-score, AUC) and confusion matrix. Calculate Multi-Block Variable Importance in Projection (MB-VIP) scores summarizing feature importance across all latent variables weighted by variance explained. Perform empirical permutation testing (n≥10,000 permutations) by repeated Y-shuffling and model refitting; compute empirical p-values as proportion of null VIP scores exceeding observed. Filter features at p<0.01 significance threshold and export ranked feature importance table with MB-VIP scores and empirical p-values. Validation: confirmed output table row count, column names, and p-value range [0, 1]. References: source article (DOI: 10.1371/journal.pcbi.1011814) Extract m/z, RT, and assay identity from LC-MS feature column names. Partition features into retention-time windows and search each window for isotopologue mass differences (1.00335 Da). Calculate hypothetical neutral masses for each feature under common ESI adducts and group features with matching neutral masses within ppm tolerance. Merge overlapping isotopologue and adduct clusters into unified structural clusters. Perform hierarchical correlation clustering using Pearson/Spearman correlation and flatten via constant threshold or silhouette-score optimization. Assign each feature a structural cluster ID, adduct group, isotopologue pattern label, and correlation cluster ID; optionally annotate with compound name. Validation: structural clusters must contain ≥2 co-eluting features per isotopologue or adduct group; silhouette score ≥0.20 indicates acceptable cluster separation; cross-assay links validated by neutral-mass match within ppm tolerance. References: source article (DOI: 10.1371/journal.pcbi.1011814) Extract structural and correlation cluster assignments from upstream MamsiStructSearch outputs (isotopologue groups, adduct groups, cross-assay links, correlation cluster labels). Instantiate NetworkX graph and populate nodes with feature identifiers and node attributes (assay, m/z, RT, cluster memberships, optional compound annotations). Encode structural relationships as weighted edges: isotopologue links (weight=1), adduct links (weight=5), cross-assay links (weight=10), correlation co-membership (weight=15). Optionally filter to linked features only or include all features based on include_all parameter. Render interactive pyvis.network visualization with spring layout, node coloring by correlation cluster, and edge thickness scaled by link weight; save to HTML file. Validation: verify NetworkX object contains correct node count, edge count, and edge weight distribution matching structural cluster topology; confirm HTML renders without JavaScript errors and interactive features (pan, zoom, node drag) are functional. References: source article (DOI: 10.1371/journal.pcbi.1011814) Load LC-MS feature intensity data with retention time and m/z metadata into MamsiStructSearch. Execute structural clustering with 'all adducts' mode: identify isotopologues (1.00335 Da threshold), detect adduct patterns (15 ppm tolerance), merge overlapping clusters. Compute cluster statistics for 'all adducts': total count, size distribution (mean, median, max), feature coverage percentage. Repeat clustering and statistics with 'most-common adducts' mode. Compare outputs: tabulate cluster counts, sizes, and coverage; compute absolute and percentage differences between modes. Validation: verify that both modes produce cluster assignments for ≥80% of input features; confirm cluster count and size statistics are computed correctly by manual spot-check on a subset of clusters. References: source article (DOI: 10.1371/journal.pcbi.1011814) Load the correlation matrix and hierarchical linkage tree from a prior constant-threshold clustering run (cut_threshold=0.7, linkage_method='complete', metric='euclidean'). Re-flatten the dendrogram using silhouette-score optimization (flat_method='silhouette', max_clusters=11) to identify the cluster count that maximizes mean silhouette coefficient. Extract cluster labels for all features under both flattening strategies and align them in a comparison table. Compute inter-solution agreement metrics (adjusted Rand index, normalized mutual information) to quantify the degree of concordance between constant-threshold and silhouette-based cluster assignments. Validation: silhouette plot exhibits a clear maximum silhouette coefficient at an intermediate cluster count (reported as 8 in the reference materials); cluster comparison table shows ≥70% of features reassigned to different clusters when switching methods, confirming substantive methodological impact. References: source article (DOI: 10.1371/journal.pcbi.1011814)

**Domain:** multi-omics

**Techniques:** multivariate-statistics, partial-least-squares, pathway-analysis, dimensionality-reduction, normalization, statistical-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets. _[grounded: MAMSI_system]_
- **(finding)** MAMSI provides a platform for linking statistically significant features of untargeted multi-assay LC-MS metabolomics datasets into clusters defined by their structural properties based on mass-to-charge ratio and retention time. _[grounded: MAMSI_system]_
- **(finding)** The MAMSI framework was tested on metabolomics phenotyping data but should be usable with other types of LC-MS data. _[grounded: MAMSI_system]_
- **(finding)** MamsiPls is a class that extends the MB_PLS class by extra methods convenient in Chemometrics and Metabolomics research. _[grounded: MamsiPls_component]_
- **(finding)** MamsiPls is based on the MB-PLS package by Baum et al., 2019. _[grounded: MamsiPls_component]_
- **(finding)** The default number of latent variables (LV) for MamsiPls is 2. _[grounded: MamsiPls_component]_
- **(finding)** The default method used to derive model attributes in MamsiPls is NIPALS. _[grounded: MamsiPls_component]_
- **(finding)** The default maximum tolerance for the iterative NIPALS algorithm in MamsiPls is 1e-14. _[grounded: MamsiPls_component]_
- **(finding)** The default nipals_convergence_norm for MamsiPls is 2. _[grounded: MamsiPls_component]_
- **(finding)** MamsiPls defaults to standardizing the data using unit-variance scaling. _[grounded: MamsiPls_component]_
- **(finding)** The estimate_lv method in MamsiPls estimates the number of latent variables using cross-validation combined with an outer loop with increasing number of LVs. _[grounded: MamsiPls_component]_
- **(finding)** The default maximum number of components for LV estimation in MamsiPls is 10. _[grounded: MamsiPls_component]_
- **(finding)** The default metric for LV estimation in MamsiPls for classification is AUC. _[grounded: MamsiPls_component]_
- **(finding)** The default cross-validation method for LV estimation in MamsiPls is k-fold. _[grounded: MamsiPls_component]_
- **(finding)** The default number of splits for k-fold cross-validation in MamsiPls is 5. _[grounded: MamsiPls_component]_
- **(finding)** Available metrics for LV estimation in MamsiPls for categorical outcome variables are AUC, precision, recall, and f1. _[grounded: MamsiPls_component]_
- **(finding)** The available metric for LV estimation in MamsiPls for continuous outcome variables is q2. _[grounded: MamsiPls_component]_
- **(finding)** Available cross-validation methods for LV estimation in MamsiPls are k-fold and Monte Carlo. _[grounded: MamsiPls_component]_
- **(finding)** The default plateau threshold for LV estimation in MamsiPls is 0.01. _[grounded: MamsiPls_component]_
- **(finding)** The default increase threshold for LV estimation in MamsiPls is 0.05. _[grounded: MamsiPls_component]_
- **(finding)** The evaluate_class_model method evaluates a classification MB-PLS model using a testing dataset. _[grounded: MBPLS_arch]_
- **(finding)** The evaluate_regression_model method evaluates a regression MB-PLS model using a testing dataset. _[grounded: MBPLS_arch]_
- **(finding)** The kfold_cv method performs k-fold cross-validation for the MB-PLS model. _[grounded: MBPLS_arch]_
- **(finding)** The default number of splits for k-fold cross-validation in the kfold_cv method is 5. _[grounded: method_kfold_cv]_
- **(finding)** The montecarlo_cv method evaluates the MB-PLS model using Monte Carlo Cross-Validation. _[grounded: MBPLS_arch]_
- **(finding)** The default test size for Monte Carlo cross-validation in the montecarlo_cv method is 0.2. _[grounded: method_mccv]_
- **(finding)** The default number of repeats for Monte Carlo cross-validation in the montecarlo_cv method is 10. _[grounded: method_mccv]_
- **(finding)** The mb_vip method calculates Multi-block Variable Importance in Projection scores for the multiblock PLS model. _[grounded: MBVIP_method]_
- **(finding)** The mb_vip method is based on an adaptation of C. Wieder et al., 2024, PathIntegrate.
- **(finding)** The block_importance method calculates the block importance for each block in the multiblock PLS model.
- **(finding)** The mb_vip_permtest method calculates empirical p-values for each feature by permuting the Y outcome variable and refitting the model.
- **(finding)** The default number of permutations for the mb_vip_permtest method is 1000.
- **(finding)** The calculate_ci static method calculates mean, margin of error, and confidence interval for each column.
- **(finding)** The default confidence level for the calculate_ci method is 0.90.
- **(finding)** The group_train_test_split static method splits data into train and test sets based on groups.
- **(finding)** MamsiStructSearch is a class for performing structural search on multi-modal MS data. _[grounded: MamsiStructSearch_component]_
- **(finding)** MamsiStructSearch allows searching for structural signatures in LC-MS data based on m/z and RT, including isotopologues and adduct patterns. _[grounded: MamsiStructSearch_component]_
- **(finding)** The default retention time tolerance window for MamsiStructSearch is 5. _[grounded: MamsiStructSearch_component]_
- **(finding)** The default mass-to-charge ratio tolerance for MamsiStructSearch is 15 ppm. _[grounded: MamsiStructSearch_component]_
- **(finding)** The load_msi method of MamsiStructSearch imports MSI intensity data and extracts feature metadata from column names. _[grounded: MamsiStructSearch_component]_
- **(finding)** The load_lcms method of MamsiStructSearch imports LC-MS intensity data and extracts feature metadata from column names. _[grounded: MamsiStructSearch_component]_
- **(finding)** The get_structural_clusters method searches structural signatures in LC-MS data including isotopologues, adduct patterns, and cross-assay links.
- **(finding)** The default adduct option for the get_structural_clusters method is 'all'.
- **(finding)** The default annotate option for the get_structural_clusters method is True.
- **(finding)** The get_correlation_clusters method clusters features based on their correlations using hierarchical clustering.
- **(finding)** The default flat_method for the get_correlation_clusters method is 'constant'.
- **(finding)** The default cut_threshold for the get_correlation_clusters method is 0.7.
- **(finding)** The default max_clusters for the get_correlation_clusters method is 5.
- **(finding)** The get_structural_network method generates a structural network graph based on structural links data or a provided master file. _[grounded: structural_network_artifact]_
- **(finding)** MAMSI was developed as part of Lukas Kopecky's PhD project at Imperial College London. _[grounded: MAMSI_system]_
- **(finding)** MAMSI is published under BSD 3-Clause licence. _[grounded: MAMSI_system]_
- **(finding)** MAMSI can be installed from PyPI using pip. _[grounded: MAMSI_system]_
- **(finding)** MAMSI requires Python version 3.9 or higher. _[grounded: MAMSI_system]_
- **(finding)** The AddNeuroMed dataset comprises 283 male and 294 female samples. _[grounded: dataset_addneuromed]_
- **(finding)** The HPOS assay has 681 features.
- **(finding)** The LPOS assay has 4,886 features.
- **(finding)** The LNEG assay has 2,091 features.
- **(finding)** MB-PLS algorithm is based on the mbpls package version 1.0.4. _[grounded: MBPLS_arch]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- UNIPALS, SIMPLS, KERNEL methods as alternatives to NIPALS
- k-fold cross-validation or Monte Carlo cross-validation for LV estimation
- constant threshold or silhouette score for flattening correlation clusters
- different linkage methods for hierarchical clustering
- different norm orders for NIPALS convergence calculation

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- sparse_data parameter must be True to accept sparse data with NIPALS algorithm
- full_svd should be set to False when using very large quadratic matrices
- annotate parameter only works for data analyzed by National Phenome Centre
- fname parameter required when savefig=True for saving plots
- linkage_method weighted and centroid only available for constant flattening method

## Steps

### Step `task_001`
- Title: Reproduce the MAMSI multi-assay MS integration workflow on metabolomics phenotyping data
- Task kind: `reproduction`
- Task: Execute the complete MAMSI pipeline on multi-assay LC-MS metabolomics data (AddNeuroMed or MY Diabetes) to train a multiblock PLS discriminant model, identify statistically significant features via MB-VIP with permutation testing, and deliver model performance metrics and significant feature rankings.
- Inputs:
  - AddNeuroMed or MY Diabetes multi-assay LC-MS metabolomics data: HPOS (HILIC positive), LPOS (lipidomic reversed-phase positive), LNEG (lipidomic reversed-phase negative) intensity matrices (n_samples × n_features) and clinical metadata with outcome variable (e.g., biological sex or disease status)
- Expected outputs:
  - Model performance metrics table: accuracy, recall, specificity, F1-score, AUC, confusion matrix for test set predictions
  - Feature importance table with MB-VIP scores and empirical p-values for all features, sorted by statistical significance (p<0.01 threshold)
  - Latent variable estimation plot showing model performance (AUC) versus number of components, identifying optimal LV count at plateau
  - MB-VIP score visualization showing feature importance across all blocks
- Tools: Python, mbpls, pandas, numpy, scikit-learn, matplotlib
- Landmark output files: train_test_split_indices.pkl, mbpls_model_fitted.pkl, lv_estimation_results.csv, test_predictions.csv, mb_vip_scores.csv, null_model_vip_permutations.npy
- Primary expected artifact: `feature_significance_table.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the structural cluster generation step using MamsiStructSearch
- Task kind: `component_reconstruction`
- Task: Implement the MamsiStructSearch module to identify and cluster statistically significant LC-MS features based on structural signatures (isotopologues, adducts, cross-assay links) and correlation patterns. Produce a structured DataFrame of features grouped into coherent structural clusters.
- Inputs:
  - LC-MS intensity data (DataFrame) with rows=samples, columns=features in format (AssayName)_(RTsec)_(m/z)m/z; e.g., HPOS_233.25_149.111m/z
  - List or array of statistically significant feature indices or binary mask selecting features from the full LC-MS matrix
- Expected outputs:
  - DataFrame of statistically significant features annotated with structural cluster IDs, adduct group assignments, isotopologue group assignments, adduct labels, cross-assay link IDs, correlation cluster assignments, and (if applicable) compound names from annotation
  - Visualizations including isotopologue pattern dendrogram, adduct cluster heatmap, silhouette plot (if silhouette flattening used), and correlation-structure heatmap
- Tools: Python, pandas, numpy, scipy, scikit-learn, matplotlib, networkx, MamsiStructSearch
- Landmark output files: isotopologue_clusters.csv, adduct_groups.csv, correlation_dendrogram.png, structural_heatmap.png
- Primary expected artifact: `structural_clusters.csv`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the structural network graph generation from significant features
- Task kind: `component_reconstruction`
- Task: Build an interactive structural network graph from MAMSI structural cluster assignments and correlation clusters, outputting both a NetworkX object and an interactive pyvis HTML visualization with nodes representing features and edges encoding isotopologue, adduct, cross-assay, and correlation links.
- Inputs:
  - Structural cluster DataFrame with columns: Feature, Assay, Isotopologue group, Isotopologue pattern, Adduct group, Adduct, Structural cluster, Correlation cluster, Cross-assay link, and optionally cpdName
  - Feature metadata table with m/z and retention time values indexed by feature identifier
- Expected outputs:
  - Interactive HTML network visualization file generated by pyvis.network with nodes colored by correlation cluster, edges weighted by link type, and optional labels
  - NetworkX graph object with nodes (features) and weighted edges (structural and correlation links) that can be saved, exported, or imported into Cytoscape for manual curation
- Tools: Python, networkx, pyvis, pandas, Cytoscape
- Landmark output files: networkx_graph.gml, feature_nodes_metadata.csv, structural_edges.csv
- Primary expected artifact: `interactive.html`

### Step `task_004`
- Depends on: `task_001`
- Title: Analyze the effect of adduct mode selection on structural cluster outputs
- Task kind: `analysis`
- Task: Run the MAMSI structural search pipeline on a selected LC-MS feature list under two adduct-selection modes ('all' vs. 'most-common'), compare the resulting structural cluster counts and size distributions, and produce a summary results table quantifying differences.
- Inputs:
  - Selected LC-MS feature intensity table (rows: samples, columns: features with naming convention (AssayName)_(RTsec)_(m/z)m/z, e.g. HPOS_233.25_149.111m/z)
- Expected outputs:
  - Structural cluster results table containing cluster ID, cluster size, member features, isotopologue group, adduct group, and cross-assay link status for 'all adducts' mode
  - Structural cluster results table for 'most-common adducts' mode with identical columns as 'all adducts' mode output
  - Comparative summary table with rows for each adduct mode, columns: Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage (%)
- Tools: Python, pandas, numpy, matplotlib, MAMSI (MamsiStructSearch)
- Landmark output files: structural_clusters_all_adducts.csv, structural_clusters_most_common_adducts.csv, cluster_size_distribution_comparison.png
- Primary expected artifact: `cluster_comparison_summary.csv`

### Step `task_005`
- Depends on: `task_002`
- Title: Extend MAMSI by substituting silhouette-based cluster flattening for constant-threshold flattening
- Task kind: `extension`
- Task: Re-run the MamsiStructSearch hierarchical clustering pipeline substituting the 'silhouette' flattening method for the default constant-threshold approach, and produce a comparative table of cluster assignments before and after the method substitution.
- Inputs:
  - Correlation matrix (Pearson) and hierarchical linkage tree from prior structural clustering run, stored as Python objects or saved as .npy/.pkl files
  - Selected LC-MS feature intensity table (CSV or pandas DataFrame) with features as columns and samples as rows
  - Cluster assignments from prior constant-threshold flattening (flat_method='constant', cut_threshold=0.7)
- Expected outputs:
  - Cluster assignment table (CSV) with columns: feature_id, constant_threshold_cluster, silhouette_cluster, assignment_change (boolean)
  - Silhouette score plot (PNG) showing silhouette coefficient as a function of cluster count, with optimal k marked
  - Cluster cardinality comparison table (CSV) with columns: method, num_clusters, cluster_id, num_features, mean_silhouette_coeff
  - Agreement metrics summary (TXT or JSON) reporting adjusted Rand index and normalized mutual information between constant-threshold and silhouette solutions
- Tools: Python, pandas, numpy, scipy, scikit-learn, matplotlib
- Landmark output files: constant_threshold_clusters.pkl, silhouette_optimized_clusters.pkl, silhouette_score_curve.png, cluster_cardinality_summary.csv
- Primary expected artifact: `cluster_comparison_table.csv`

## Final expected outputs

- `Interactive HTML network visualization file generated by pyvis.network with nodes colored by correlation cluster, edges weighted by link type, and optional labels` (type: file, tolerance: hash)
- `NetworkX graph object with nodes (features) and weighted edges (structural and correlation links) that can be saved, exported, or imported into Cytoscape for manual curation` (type: file, tolerance: hash)
- `Structural cluster results table containing cluster ID, cluster size, member features, isotopologue group, adduct group, and cross-assay link status for 'all adducts' mode` (type: file, tolerance: hash)
- `Structural cluster results table for 'most-common adducts' mode with identical columns as 'all adducts' mode output` (type: file, tolerance: hash)
- `Comparative summary table with rows for each adduct mode, columns: Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage (%)` (type: file, tolerance: hash)
- `Cluster assignment table (CSV) with columns: feature_id, constant_threshold_cluster, silhouette_cluster, assignment_change (boolean)` (type: file, tolerance: hash)
- `Silhouette score plot (PNG) showing silhouette coefficient as a function of cluster count, with optimal k marked` (type: file, tolerance: hash)
- `Cluster cardinality comparison table (CSV) with columns: method, num_clusters, cluster_id, num_features, mean_silhouette_coeff` (type: file, tolerance: hash)
- `Agreement metrics summary (TXT or JSON) reporting adjusted Rand index and normalized mutual information between constant-threshold and silhouette solutions` (type: file, tolerance: hash)

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

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_mamsi_workflow",
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
    "Interactive HTML network visualization file generated by pyvis.network with nodes colored by correlation cluster, edges weighted by link type, and optional labels": "<locator>",
    "NetworkX graph object with nodes (features) and weighted edges (structural and correlation links) that can be saved, exported, or imported into Cytoscape for manual curation": "<locator>",
    "Structural cluster results table containing cluster ID, cluster size, member features, isotopologue group, adduct group, and cross-assay link status for 'all adducts' mode": "<locator>",
    "Structural cluster results table for 'most-common adducts' mode with identical columns as 'all adducts' mode output": "<locator>",
    "Comparative summary table with rows for each adduct mode, columns: Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage (%)": "<locator>",
    "Cluster assignment table (CSV) with columns: feature_id, constant_threshold_cluster, silhouette_cluster, assignment_change (boolean)": "<locator>",
    "Silhouette score plot (PNG) showing silhouette coefficient as a function of cluster count, with optimal k marked": "<locator>",
    "Cluster cardinality comparison table (CSV) with columns: method, num_clusters, cluster_id, num_features, mean_silhouette_coeff": "<locator>",
    "Agreement metrics summary (TXT or JSON) reporting adjusted Rand index and normalized mutual information between constant-threshold and silhouette solutions": "<locator>"
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
