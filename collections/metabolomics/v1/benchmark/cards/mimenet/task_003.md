# SciTask Card: Reconstruct the Microbe-Metabolite Feature Attribution and Consensus-Clustering Module Construction pipeline

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T07:36:08.260853+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_mimenet`
- Domain: `bioinformatics`
- Subtask categories: `data-analysis`, `modeling`, `visualization`
- DOI: `10.1371/journal.pcbi.1009021`
- GitHub: `biobakery/melonnpan`
- Input from: `task_001`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `microbiome-metabolomics`, `artificial-intelligence`, `multi-omics-integration`
- Techniques: `deep-learning`, `machine-learning`, `random-forest`, `correlation-analysis`, `clustering`

## Research Question
How does Olden's method derive microbe-metabolite feature attribution scores from MLPNN network weights, and how are these scores subsequently used to construct functional modules via biclustering?

## Connected Finding
MiMeNet computes feature attribution scores for all microbe-metabolite pairs from trained MLPNN network weights, then applies biclustering to group microbes and metabolites into modules where members share similar attribution patterns. Positive attribution scores indicate microbes that contribute positively to metabolite abundance prediction, while negative scores indicate negative contributions.

## Task Description
Implement the MiMeNet feature attribution and consensus clustering pipeline to derive microbe-metabolite interaction modules from trained MLPNN weights on the IBD (PRISM) dataset. Produce normalized feature attribution scores, identify significant microbe-metabolite pairs, and construct functional modules via biclustering.

## Inputs
- Trained MLPNN models (100 models from 10 iterations of 10-fold cross-validation with saved weight tensors)
- Well-predicted metabolites list (metabolites with Spearman correlation coefficient above 95th percentile of background distribution)
- IBD (PRISM) microbiome and metabolome data (centered log-ratio transformed, 201 microbes × 8848 metabolites)
- Background feature attribution score distribution (from 100 models with randomly shuffled microbiome-metabolome samples)

## Expected Outputs
- Normalized microbe-metabolite feature attribution score matrix (microbes × metabolites, values clipped to [-1, 1])
- Microbial module assignments (list of microbe IDs grouped by cluster number k*)
- Metabolite module assignments (list of metabolite IDs grouped by cluster number k**)
- Module-based interaction network edge list (microbe module–metabolite module pairs with average normalized attribution scores, filtered to |score| ≥ 0.25)

## Expected Output File

- `microbe_metabolite_modules.csv`

## Landmark Outputs

- `attribution_scores_raw.npy`
- `attribution_scores_normalized.csv`
- `significant_microbes.txt`
- `consensus_clustering_k_selection.png`
- `microbe_clusters.csv`
- `metabolite_clusters.csv`

## Tools
- neural networks
- WGCNA
- Seaborn clustermap
- Cytoscape
- Python scikit-learn

## Skills
- neural-network-weight-extraction
- olden-method-feature-attribution-calculation
- consensus-clustering-algorithm-selection
- microbe-metabolite-module-construction
- biclustering-for-omics-features
- network-module-interaction-scoring

## Workflow Description
1. Load trained MLPNN models (100 models from 10 iterations of 10-fold cross-validation) and extract weight matrices W_l from all hidden layers. 2. Calculate microbe-metabolite feature attribution scores S using Olden's method by multiplying weight matrices across layers (S = ∏ W_l for l ∈ L), producing one score matrix per trained model. 3. Generate mean attribution matrix S* by averaging all 100 S_i matrices, then flatten into a feature vector and apply 97.5 percentile threshold to identify significant attribution scores (absolute value above threshold). 4. Filter out non-significant microbes (those with no attribution scores above threshold with any well-predicted metabolite), and normalize all significant scores to range [-1, 1] by dividing by the 97.5 percentile threshold from background distribution. 5. Perform hierarchical clustering on normalized attribution scores using Euclidean distance and complete linkage, then apply consensus clustering with k ranging from 2 to 20; calculate cumulative distribution function area for each k and select k* as the largest k where Δk (proportional change in area) exceeds 0.025 threshold. 6. Repeat consensus clustering for metabolites to identify k** using the same Δk threshold criterion. 7. Bicluster the normalized score matrix using k* and k** to partition rows (microbes) and columns (metabolites) into final functional modules. 8. Output normalized attribution scores, module membership assignments, and module interaction network edge list.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `mimenet.pdf` | main_article | True |

## Missing Information
- Exact hyperparameter settings (soft threshold power, minimum module size, cut height threshold) for WGCNA consensus clustering applied to feature attribution score matrix for IBD (PRISM) dataset are not reported.
- Method for deriving feature attribution scores (attribution method name beyond mention of 'network weights') and mathematical formulation are not explicitly detailed in the provided discussion excerpt.
- Threshold or criteria for selecting microbes that enter the feature attribution score matrix are partially specified ('163 microbes that had at least one significant attribution score') but the initial filtering criteria (10% prevalence, abundance cutoff) and final filtering logic are not fully justified.
- Computational time, memory requirements, and scalability characteristics of the feature attribution + WGCNA pipeline are not reported.
- Sensitivity analysis of module assignments to variations in WGCNA parameters (e.g., soft threshold power, merge cut height) is not presented; robustness of biological findings to parameter choices is not assessed.

## Domain Knowledge
- Olden's method multiplies weight matrices across all hidden layers to derive input-to-output feature importance scores, with positive values indicating positive associations and negative values indicating negative associations.
- The 97.5 percentile threshold applied to background attribution scores (from shuffled microbiome-metabolome pairs) controls false discovery rate by selecting only microbe-metabolite pairs significantly more correlated than expected by chance.
- Consensus clustering with Δk = 0.025 threshold determines the optimal number of clusters by detecting the point where increasing cluster count ceases to substantially improve cohesion (measured by cumulative distribution function area), balancing module interpretability against over-segmentation.
- Biclustering simultaneously partitions rows (microbes) and columns (metabolites) such that microbes within a module share similar interaction patterns across metabolites, revealing functional co-occurrence rather than abundance co-variance alone.
- Module interaction network edge filtering (|score| ≥ 0.25) removes weak inter-module connections while preserving biologically meaningful associations, reducing visual noise in network visualization without a reported biological justification threshold.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] How does Olden's method derive microbe-metabolite feature attribution scores from MLPNN network weights, and how are these scores subsequently used to construct functional modules via biclustering?: 'using the learned network models, MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites. Then MiMeNet biclusters the score'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] MiMeNet computes feature attribution scores for all microbe-metabolite pairs from trained MLPNN network weights, then applies biclustering to group microbes and metabolites into modules where members share similar attribution patterns. Positive attribution scores indicate microbes that contribute positively to metabolite abundance prediction, while negative scores indicate negative contributions.: 'A positive score means that the microbe contributes positively to the prediction of the abundance of the metabolite. Likewise, a negative score contributes negatively to the prediction of the'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Trained MLPNN models (100 models from 10 iterations of 10-fold cross-validation with saved weight tensors): 'we calculated the mean feature attribution score matrix, which was then flattened into a feature vector and a threshold was set at the 97.5 percentile'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Well-predicted metabolites list (metabolites with Spearman correlation coefficient above 95th percentile of background distribution): 'We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] IBD (PRISM) microbiome and metabolome data (centered log-ratio transformed, 201 microbes × 8848 metabolites): 'A total of 201 microbial species and 8848 metabolites were identified for the IBD (PRISM) and IBD (External) datasets'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Background feature attribution score distribution (from 100 models with randomly shuffled microbiome-metabolome samples): 'we calculated feature attribution score matrices from the network models used to generate the background correlation distribution'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Normalized microbe-metabolite feature attribution score matrix (microbes × metabolites, values clipped to [-1, 1]): 'We normalized the values in each feature attribution score matrix S_i by dividing the significant threshold score identified from the background and clipped values to be between -1 and 1'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Microbial module assignments (list of microbe IDs grouped by cluster number k*): 'The final set of microbial and metabolite modules are then determined by biclustering S* using k* and k* to cluster the rows and columns respectively'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Metabolite module assignments (list of metabolite IDs grouped by cluster number k**): 'The final set of microbial and metabolite modules are then determined by biclustering S* using k* and k* to cluster the rows and columns respectively'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Module-based interaction network edge list (microbe module–metabolite module pairs with average normalized attribution scores, filtered to |score| ≥ 0.25): 'For visualization of the microbe-metabolite interaction network, the score between a pair of modules was calculated as the average normalized feature attribution between each microbe and metabolite'
- `ev_011` from `agent2_synthesis` (agent2_traced): [abstract] neural networks: 'we present MiMeNet, a neural network framework for modeling microbe-metabolite relationships'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] WGCNA: 'compared the microbial modules in the IBD (PRISM) dataset identified by MiMeNet to those identified by the Weighted Correlation Network Analysis (WGCNA)'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] Seaborn clustermap: 'using Seaborn's clustermap function in Python'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] Cytoscape: 'using Cytoscape'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] Python scikit-learn: 'using Python's sci-kit-learn package'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] Exact hyperparameter settings (soft threshold power, minimum module size, cut height threshold) for WGCNA consensus clustering applied to feature attribution score matrix for IBD (PRISM) dataset are not reported.: 'MiMeNet then trains multiple network models using 10-fold cross-validation'
- `ev_017` from `agent2_synthesis` (agent2_traced): [discussion] Method for deriving feature attribution scores (attribution method name beyond mention of 'network weights') and mathematical formulation are not explicitly detailed in the provided discussion excerpt.: 'the feature attribution scores derived from the network weights could be used to construct modules'
- `ev_018` from `agent2_synthesis` (agent2_traced): [discussion] Threshold or criteria for selecting microbes that enter the feature attribution score matrix are partially specified ('163 microbes that had at least one significant attribution score') but the initial filtering criteria (10% prevalence, abundance cutoff) and final filtering logic are not fully justified.: 'We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite'
- `ev_019` from `agent2_synthesis` (agent2_traced): [discussion] Computational time, memory requirements, and scalability characteristics of the feature attribution + WGCNA pipeline are not reported.: 'Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge'
- `ev_020` from `agent2_synthesis` (agent2_traced): [discussion] Sensitivity analysis of module assignments to variations in WGCNA parameters (e.g., soft threshold power, merge cut height) is not presented; robustness of biological findings to parameter choices is not assessed.: 'construct modules of microbes with similar positive or negative effects on a set of metabolites'

## Evaluation Strategy
### Direct Checks
- file_exists: verify that MiMeNet package repository (https://github.com/YDaiLab/MiMeNet) contains scripts implementing feature attribution score derivation via Olden's method
- file_exists: verify that IBD (PRISM) dataset input files (microbiome abundance matrix and metabolite abundance matrix) are accessible or documented in the repository with format specification (CSV, TSV, or HDF5)
- script_runs: execute MiMeNet feature attribution pipeline on IBD (PRISM) dataset and verify that output is a microbe-metabolite score matrix with dimensions [num_microbes × num_well_predicted_metabolites], where num_well_predicted_metabolites ≥ 163 (per stated count of microbes with significant scores)
- file_format_is: verify that feature attribution score matrix output file conforms to expected format (matrix/array with row labels matching microbe identifiers and column labels matching metabolite identifiers)
- value_in_range: verify that feature attribution scores fall within a bounded range consistent with normalized/standardized Olden's method output (typical range: [-1, 1] or [-∞, ∞] depending on implementation); no canonical answer as different software implementations may scale differently
- script_runs: execute WGCNA-based consensus clustering on feature attribution score matrix and verify that output includes: (a) dendrogram or hierarchical clustering tree, (b) microbe module assignment file (TSV/CSV with microbe ID and module ID columns), (c) metabolite module assignment file (TSV/CSV with metabolite ID and module ID columns), (d) module-level interaction network (adjacency matrix or edge list)
- row_count_equals: verify that microbe module assignment file contains exactly one row per input microbe that passed filtering thresholds; robust to order of rows
- row_count_equals: verify that metabolite module assignment file contains exactly one row per well-predicted metabolite (expected count: ≥ 198 for IBD PRISM based on abstract claim of 'increase from 198 to 366')
- contains_substring: verify that module assignment outputs contain expected column headers (e.g., 'microbe_id', 'module_id' or 'metabolite_id', 'module_id'); robust to exact header capitalization if schema is documented
- output_matches_reference: retrieve microbe-metabolite module assignments from published paper Tables or Figures (S6, S7) and verify that module memberships generated by re-implemented pipeline match reported module assignments within ≤ 10% reassignment rate; parameter-sensitive to clustering cut-height and consensus threshold choices in WGCNA

### Expert Review
- Verify that Olden's method implementation correctly computes feature attribution scores as product of normalized weights through the network layers, matching the mathematical formulation cited in methods (if provided) or standard references
- Confirm that WGCNA consensus clustering parameters (soft threshold power, minimum module size, cut height for dendrogram merging) are either explicitly reported in paper/methods or recovered from SI/code; assess whether chosen parameters are appropriate for the scale of input feature attribution matrix (163 microbes × ~200 metabolites)
- Assess whether the derived microbe and metabolite modules exhibit biological coherence: (a) verify that reported butyrate-producing bacteria (Faecalibacterium prausnitzii, Eubacterium biforme, Eubacterium hallii, Eubacterium rectale, Roseburia faecis, Roseburia inulinivorans) cluster together in module 6 as stated in discussion; (b) verify that secondary bile acid-producing genera (Bacteroides, Clostridium, Eubacterium, Ruminococcus) co-cluster in modules 2, 4, or 6
- Evaluate whether feature attribution score patterns are sufficiently informative to enable metabolite annotation via 'Guilt of Association' principle: assess whether annotated metabolites in a module show biologically plausible shared interaction patterns with the same microbial modules, and whether clustering of unannotated metabolites with annotated ones is consistent with known biochemical pathways
- Compare the MiMeNet-derived module structure to the WGCNA modules mentioned in results (paper states 'compared the microbial modules in the IBD (PRISM) dataset identified by MiMeNet to those identified by the Weighted Correlation Network Analysis (WGCNA)'); assess agreement between the two unsupervised clustering approaches and discuss potential sources of disagreement

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Extract trained MLPNN weight matrices across all hidden layers from 100 cross-validated models.
2. Compute microbe-metabolite feature attribution scores via Olden's method (multiply weight matrices layer-by-layer) for each model.
3. Average attribution matrices across all 100 models and apply 97.5 percentile threshold to identify significant microbe-metabolite associations.
4. Normalize significant attribution scores to [-1, 1] range by dividing by the 97.5 percentile value.
5. Apply hierarchical clustering with consensus resampling (k = 2–20) to microbes and metabolites independently, selecting optimal cluster numbers (k*, k**) where proportional change in consensus matrix area exceeds 0.025 threshold.
6. Bicluster normalized attribution matrix using selected k* and k** to produce final microbe and metabolite functional modules.
7. Compute inter-module interaction scores as average normalized attribution between all microbe-metabolite pairs in each module pair, filter edges to |score| ≥ 0.25 for network visualization.
8. Validation: Confirm module membership is stable across cross-validated models, verify clustering dendrogram height consistency, and check that filtered interaction network contains ≥1 edges per non-singleton module pair.
9. References: source article (DOI: 10.1371/journal.pcbi.1009021)

## Workflow Ports

**Inputs:**

- `trained_models` — Trained MLPNN models with weight tensors ← `task_001/benchmark_results`
- `well_predicted_metabolites` — Well-predicted metabolites list
- `ibd_prism_data` — IBD (PRISM) microbiome-metabolome dataset
- `background_attribution_dist` — Background feature attribution score distribution

**Outputs:**

- `normalized_attribution_scores` — Normalized microbe-metabolite feature attribution score matrix
- `microbe_modules` — Microbial module assignments
- `metabolite_modules` — Metabolite module assignments
- `module_network` — Module-based interaction network edge list

**Used:** `urn:asb:port:task_001/benchmark_results`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
