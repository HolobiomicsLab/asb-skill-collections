# SciTask Card: Extend MAMSI by substituting silhouette-based cluster flattening for constant-threshold flattening

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T13:26:03.540713+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_mamsi/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `statistical-analysis`, `visualization`
- DOI: `10.1371/journal.pcbi.1011814`
- GitHub: `kopeckylukas/py-mamsi`
- Input from: `task_002`

## Classification

- Task kind: `extension`
- Article type: `research-article`
- Primary domain: `multi-omics`
- Subdomains: `multi-omics-integration`, `computational-metabolomics`, `biomarker-discovery`
- Techniques: `multivariate-statistics`, `partial-least-squares`, `pathway-analysis`, `dimensionality-reduction`, `normalization`, `statistical-analysis`

## Research Question
Does the silhouette flattening method produce different structural cluster assignments compared to the default constant-threshold method in the MAMSI structural clustering pipeline?

## Connected Finding
MAMSI integrates multi-assay mass spectrometry datasets and clusters statistically significant LC-MS features based on structural properties defined by m/z and retention time.

## Task Description
Re-run the MamsiStructSearch hierarchical clustering pipeline substituting the 'silhouette' flattening method for the default constant-threshold approach, and produce a comparative table of cluster assignments before and after the method substitution.

## Inputs
- Correlation matrix (Pearson) and hierarchical linkage tree from prior structural clustering run, stored as Python objects or saved as .npy/.pkl files
- Selected LC-MS feature intensity table (CSV or pandas DataFrame) with features as columns and samples as rows
- Cluster assignments from prior constant-threshold flattening (flat_method='constant', cut_threshold=0.7)

## Expected Outputs
- Cluster assignment table (CSV) with columns: feature_id, constant_threshold_cluster, silhouette_cluster, assignment_change (boolean)
- Silhouette score plot (PNG) showing silhouette coefficient as a function of cluster count, with optimal k marked
- Cluster cardinality comparison table (CSV) with columns: method, num_clusters, cluster_id, num_features, mean_silhouette_coeff
- Agreement metrics summary (TXT or JSON) reporting adjusted Rand index and normalized mutual information between constant-threshold and silhouette solutions

## Expected Output File

- `cluster_comparison_table.csv`

## Landmark Outputs

- `constant_threshold_clusters.pkl`
- `silhouette_optimized_clusters.pkl`
- `silhouette_score_curve.png`
- `cluster_cardinality_summary.csv`

## Tools
- Python
- pandas
- numpy
- scipy
- scikit-learn
- matplotlib

## Skills
- hierarchical-clustering-dendrogram-interpretation
- silhouette-analysis-threshold-optimization
- clustering-solution-comparison-metrics
- correlation-matrix-heatmap-visualization
- metabolite-feature-annotation-aggregation

## Workflow Description
1. Load pre-computed correlation matrix and hierarchical dendrogram from a prior MamsiStructSearch run using constant threshold (cut_threshold=0.7, linkage_method='complete'). 2. Re-flatten the same dendrogram using silhouette-score optimization with max_clusters=11 via the get_correlation_clusters() method with flat_method='silhouette'. 3. Extract and tabulate cluster assignment labels for all features from both flattening methods. 4. Compute agreement metrics (adjusted Rand index, normalized mutual information) between the two clustering solutions. 5. Generate a side-by-side comparison table showing feature IDs, constant-threshold cluster ID, silhouette-optimized cluster ID, and agreement status.

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
- No changelog documenting available flattening methods, parameter names, or API signatures for MamsiStructSearch

## Domain Knowledge
- Silhouette score ranges from −1 to 1, where values >0.4 indicate moderate separation and values >0.6 indicate strong cluster definition; optimal cluster count maximizes the mean silhouette coefficient across all samples.
- Hierarchical clustering dendrogram flattening by a constant Euclidean distance threshold yields a fixed partition, whereas silhouette-based flattening optimizes cluster coherence by scanning a range of cutoff heights and selecting the one that maximizes internal cohesion and separation.
- Adjusted Rand Index (ARI) and Normalized Mutual Information (NMI) are symmetric measures of clustering agreement; ARI near 1 indicates near-identical partitions, while ARI near 0 indicates random agreement independent of method choice.
- Retention time windows of 5-second intervals separate features into independent RT bins before hierarchical clustering, ensuring that isotopologue and adduct patterns within a metabolite family are captured locally without global dendrogram distortion.
- The 'linkage_method' parameter (complete, average, ward, single) affects dendrogram topology and cluster boundaries; complete linkage tends to produce more compact, well-separated clusters and is default for constant-threshold flattening.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: pandas, numpy, scipy, scikit-learn, matplotlib, Cluster assignment table (CSV) with columns: feature_id, constant_threshold_cluster, silhouette_cluster, assignment_change (boolean), Silhouette score plot (PNG) showing silhouette coefficient as a function of cluster count, with optimal k marked, Cluster cardinality comparison table (CSV) with columns: method, num_clusters, cluster_id, num_features, mean_silhouette_coeff, Agreement metrics summary (TXT or JSON) reporting adjusted Rand index and normalized mutual information between constant-threshold and silhouette solutions.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does the silhouette flattening method produce different structural cluster assignments compared to the default constant-threshold method in the MAMSI structural clustering pipeline?: 'the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] MAMSI integrates multi-assay mass spectrometry datasets and clusters statistically significant LC-MS features based on structural properties defined by m/z and retention time.: 'MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets. In addition, the MAMSI framework provides a platform for linking statistically significant features'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Correlation matrix (Pearson) and hierarchical linkage tree from prior structural clustering run, stored as Python objects or saved as .npy/.pkl files: 'struct.get_correlation_clusters(flat_method='silhouette', max_clusters=11)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Selected LC-MS feature intensity table (CSV or pandas DataFrame) with features as columns and samples as rows: 'struct.load_lcms(selected)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Cluster assignments from prior constant-threshold flattening (flat_method='constant', cut_threshold=0.7): 'flat_method='constant', cut_threshold=0.7'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Cluster assignment table (CSV) with columns: feature_id, constant_threshold_cluster, silhouette_cluster, assignment_change (boolean): 'get_correlation_clusters(flat_method='constant', cut_threshold=0.7, linkage_method='complete') ... get_correlation_clusters(flat_method='silhouette', max_clusters=5)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Silhouette score plot (PNG) showing silhouette coefficient as a function of cluster count, with optimal k marked: 'Best number of clusters based on silhouette score: 8'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Cluster cardinality comparison table (CSV) with columns: method, num_clusters, cluster_id, num_features, mean_silhouette_coeff: 'Silhouette score for 8 clusters: 0.2436798413177305'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Agreement metrics summary (TXT or JSON) reporting adjusted Rand index and normalized mutual information between constant-threshold and silhouette solutions: 'flat_method='constant', cut_threshold=0.7 ... flat_method='silhouette', max_clusters=5'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Python: 'MAMSI is a Python framework'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] pandas: 'import pandas as pd'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] numpy: 'import numpy as np'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] scipy: 'Dependencies: scipy'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] scikit-learn: 'from sklearn.model_selection import train_test_split'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] matplotlib: 'from matplotlib import pyplot as plt'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting available flattening methods, parameter names, or API signatures for MamsiStructSearch: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists in github:kopeckylukas__py-mamsi repository containing MamsiStructSearch.flattening or equivalent parameter definition
- verify script_runs: instantiate MamsiStructSearch with flattening='silhouette' (or equivalent API) on sample LC-MS data from kopeckylukas/py-mamsi-tutorials without error
- verify script_runs: instantiate MamsiStructSearch with default flattening method (constant-threshold or equivalent) on identical sample data without error
- file_format_is: cluster assignments output from silhouette-flattened pipeline is a structured record (CSV, JSON, or Python dict-like object) with fields: feature_id, cluster_id, and confidence_score or equivalent
- file_format_is: cluster assignments output from default-flattened pipeline matches same structure
- row_count_equals or value_in_range: number of structural clusters produced by silhouette method is within ±50% of default method (or report exact counts for expert review if outside range)
- value_in_range: silhouette score(s) reported by silhouette method are in range [−1, +1], robust to parameter choices
- field_present: cluster assignment outputs include field indicating flattening method used, allowing byte-for-byte verification of method identity

### Expert Review
- Compare silhouette-method vs. default-method cluster assignments for biological/chemical plausibility: do reassignments of features to different clusters align with expected m/z and RT proximity and known metabolite structure relationships?
- Evaluate whether silhouette-based flattening produces more stable or more interpretable cluster boundaries than constant-threshold method on the same dataset
- Assess whether the silhouette method resolves ambiguous borderline features (low distance to multiple clusters) more defensibly than the default approach, multiple defensible outcomes possible

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load the correlation matrix and hierarchical linkage tree from a prior constant-threshold clustering run (cut_threshold=0.7, linkage_method='complete', metric='euclidean').
2. Re-flatten the dendrogram using silhouette-score optimization (flat_method='silhouette', max_clusters=11) to identify the cluster count that maximizes mean silhouette coefficient.
3. Extract cluster labels for all features under both flattening strategies and align them in a comparison table.
4. Compute inter-solution agreement metrics (adjusted Rand index, normalized mutual information) to quantify the degree of concordance between constant-threshold and silhouette-based cluster assignments.
5. Validation: silhouette plot exhibits a clear maximum silhouette coefficient at an intermediate cluster count (reported as 8 in the reference materials); cluster comparison table shows ≥70% of features reassigned to different clusters when switching methods, confirming substantive methodological impact.
6. References: source article (DOI: 10.1371/journal.pcbi.1011814)

## Workflow Ports

**Inputs:**

- `selected_features_lcms` — Selected LC-MS feature intensity table ← `task_002/structural_clusters_table`
- `constant_threshold_assignments` — Cluster assignments from constant-threshold flattening
- `correlation_matrix` — Pre-computed Pearson correlation matrix

**Outputs:**

- `cluster_comparison_table` — Side-by-side cluster assignment table (constant vs. silhouette)
- `silhouette_plot` — Silhouette score optimization plot
- `cardinality_summary` — Cluster cardinality and silhouette coefficient summary
- `agreement_metrics` — Clustering agreement metrics (ARI, NMI)

**Used:** `urn:asb:port:task_002/structural_clusters_table`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:kopeckylukas__py-mamsi`
- **Synthesized at:** 2026-06-15T13:34:24+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
