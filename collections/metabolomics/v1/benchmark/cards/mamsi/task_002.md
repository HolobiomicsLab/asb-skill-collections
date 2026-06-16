# SciTask Card: Reconstruct the structural cluster generation step using MamsiStructSearch

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T13:26:03.540713+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_mamsi/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `data-analysis`, `information-extraction`
- DOI: `10.1371/journal.pcbi.1011814`
- GitHub: `kopeckylukas/py-mamsi`
- Input from: `task_001`

## Classification

- Task kind: `component_reconstruction`
- Article type: `research-article`
- Primary domain: `multi-omics`
- Subdomains: `multi-omics-integration`, `computational-metabolomics`, `biomarker-discovery`
- Techniques: `multivariate-statistics`, `partial-least-squares`, `pathway-analysis`, `dimensionality-reduction`, `normalization`, `statistical-analysis`

## Research Question
How does the MamsiStructSearch module group statistically significant LC-MS features into structural clusters using mass-to-charge ratio and retention time information?

## Connected Finding
MamsiStructSearch operates by searching retention time windows for isotopologue signatures (mass differences of 1.00335 Da), then searching for common adduct signatures by calculating hypothetical neutral masses from common electrospray ionisation adducts, and finally merging overlapping adduct and isotopologue clusters to form structural clusters.

## Task Description
Implement the MamsiStructSearch module to identify and cluster statistically significant LC-MS features based on structural signatures (isotopologues, adducts, cross-assay links) and correlation patterns. Produce a structured DataFrame of features grouped into coherent structural clusters.

## Inputs
- LC-MS intensity data (DataFrame) with rows=samples, columns=features in format (AssayName)_(RTsec)_(m/z)m/z; e.g., HPOS_233.25_149.111m/z
- List or array of statistically significant feature indices or binary mask selecting features from the full LC-MS matrix

## Expected Outputs
- DataFrame of statistically significant features annotated with structural cluster IDs, adduct group assignments, isotopologue group assignments, adduct labels, cross-assay link IDs, correlation cluster assignments, and (if applicable) compound names from annotation
- Visualizations including isotopologue pattern dendrogram, adduct cluster heatmap, silhouette plot (if silhouette flattening used), and correlation-structure heatmap

## Expected Output File

- `structural_clusters.csv`

## Landmark Outputs

- `isotopologue_clusters.csv`
- `adduct_groups.csv`
- `correlation_dendrogram.png`
- `structural_heatmap.png`

## Tools
- Python
- pandas
- numpy
- scipy
- scikit-learn
- matplotlib
- networkx
- MamsiStructSearch

## Skills
- lc-ms-feature-m/z-rt-extraction
- isotopologue-signature-detection
- adduct-mass-matching-and-clustering
- hierarchical-correlation-clustering-interpretation
- multi-assay-cross-linking-validation
- metabolite-structural-annotation-integration
- mass-tolerance-calibration-ppm-units

## Workflow Description
1. Load preprocessed LC-MS intensity data with column names in format (AssayName)_(RTsec)_(m/z)m/z into MamsiStructSearch using .load_lcms() to extract feature metadata (m/z, RT, assay). 2. Define retention time tolerance window (rt_win, default 5 seconds) and mass tolerance (ppm, default 15 ppm) for structural matching. 3. Search for isotopologue signatures within each RT window by identifying mass differences of 1.00335 Da between feature m/z values. 4. Search for adduct signatures by calculating hypothetical neutral masses from common ESI adducts and matching within ppm tolerance; group features with matching neutral masses. 5. Merge overlapping isotopologue and adduct clusters into structural clusters via .get_structural_clusters(). 6. Perform hierarchical correlation clustering on features using .get_correlation_clusters() with choice of flattening method (constant threshold or silhouette score) and linkage criterion (complete, average, ward, etc.). 7. Combine structural and correlation cluster assignments and return annotated feature table with cluster membership.

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
- No changelog found.
- No specification of exact mass tolerance windows or RT tolerance thresholds for adduct and isotopologue clustering
- No detailed specification of the data structure or file format of the structural cluster output artifact

## Domain Knowledge
- Isotopologue mass difference is fixed at 1.00335 Da (difference between C-13 and C-12); features within the same RT window matching this mass offset are grouped as isotopologues.
- Adduct mass differences depend on the ionization mode (ESI positive or negative) and common adducts include [M+H]+, [M+Na]+, [M-H]-, etc.; hypothetical neutral mass is calculated by subtracting the adduct mass from the observed m/z.
- Retention time tolerance (rt_win, typically 5 seconds) accounts for chromatographic peak width and co-elution; features outside this window are not considered co-eluates even if they share m/z patterns.
- Mass tolerance (ppm) is relative to m/z value: error_Da = (m/z × ppm) / 1e6; higher ppm tolerance (e.g., 15 ppm for Orbitrap-class instruments) accepts broader mass variation.
- Cross-assay links use [M+H]+/[M-H]- pairs as reference to identify the same compound measured in positive and negative ionization modes across different LC-MS assays.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: pandas, numpy, scipy, scikit-learn, matplotlib, networkx, MamsiStructSearch.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does the MamsiStructSearch module group statistically significant LC-MS features into structural clusters using mass-to-charge ratio and retention time information?: 'the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] MamsiStructSearch operates by searching retention time windows for isotopologue signatures (mass differences of 1.00335 Da), then searching for common adduct signatures by calculating hypothetical neutral masses from common electrospray ionisation adducts, and finally merging overlapping adduct and isotopologue clusters to form structural clusters.: 'each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 *Da* between mass-to-charge ratios (*m/z*) of the features. This is followed by a search for common'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] LC-MS intensity data (DataFrame) with rows=samples, columns=features in format (AssayName)_(RTsec)_(m/z)m/z; e.g., HPOS_233.25_149.111m/z: 'Data frame with LC-MS intensity data. - rows: samples - columns: features (LC-MS peaks). Column names in the format: **(AssayName)_(RTsec)_(m/z)m/z**. For example: **HPOS_233.25_149.111m/z**'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] List or array of statistically significant feature indices or binary mask selecting features from the full LC-MS matrix: 'Select features with p-value < 0.01. You can also apply multiple testing correction methods to adjust the p-value threshold.'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] DataFrame of statistically significant features annotated with structural cluster IDs, adduct group assignments, isotopologue group assignments, adduct labels, cross-assay link IDs, correlation cluster assignments, and (if applicable) compound names from annotation: 'DataFrame of significant features with structural clusters.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Visualizations including isotopologue pattern dendrogram, adduct cluster heatmap, silhouette plot (if silhouette flattening used), and correlation-structure heatmap: 'Clustering for features based on their correlations. The method uses hierarchical clustering to create clusters. To flatten clusters, the method uses either a constant threshold or silhouette score.'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Python: 'MAMSI is a Python framework'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] pandas: 'import pandas as pd'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] numpy: 'import numpy as np'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] scipy: 'scipy'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] scikit-learn: 'from sklearn.model_selection import train_test_split'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] matplotlib: 'from matplotlib import pyplot as plt'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] networkx: 'networkx'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] MamsiStructSearch: 'A class for performing structural search on multi-modal MS data using.'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found.: 'No changelog found.'
- `ev_016` from `agent2_synthesis` (agent2_traced): [other] No specification of exact mass tolerance windows or RT tolerance thresholds for adduct and isotopologue clustering: 'not present in provided discussion section'
- `ev_017` from `agent2_synthesis` (agent2_traced): [other] No detailed specification of the data structure or file format of the structural cluster output artifact: 'not present in provided discussion section'

## Evaluation Strategy
### Direct Checks
- verify that kopeckylukas/py-mamsi repository contains a MamsiStructSearch class or module
- verify that MamsiStructSearch has a load_lcms() method accepting a list or array-like input
- verify that MamsiStructSearch produces a named artifact (file, object, or data structure) representing structural clusters
- verify that the implementation searches for isotopologue signatures using mass difference of 1.00335 Da
- verify that the implementation searches for common adduct signatures via electrospray ionisation adducts
- verify that the implementation merges overlapping adduct and isotopologue clusters
- verify that the implementation supports cross-assay cluster linking using [M+H]+/[M-H]- references
- script_runs: execute a minimal MamsiStructSearch workflow on sample LC-MS features (m/z, RT columns) from kopeckylukas/py-mamsi-tutorials and confirm no runtime errors — solution_space: multiple defensible sample inputs valid
- output_matches_reference: verify that structural cluster output format is documented or demonstrated in tutorials repository

### Expert Review
- evaluate whether the adduct and correlation-clustering logic correctly implements the description in the repository README and methods section
- evaluate whether the mass tolerance thresholds and RT window parameters for isotopologue and adduct detection are biochemically appropriate
- evaluate whether the merging strategy for overlapping clusters (adduct + isotopologue) is statistically sound and avoids over-clustering

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Extract m/z, RT, and assay identity from LC-MS feature column names.
2. Partition features into retention-time windows and search each window for isotopologue mass differences (1.00335 Da).
3. Calculate hypothetical neutral masses for each feature under common ESI adducts and group features with matching neutral masses within ppm tolerance.
4. Merge overlapping isotopologue and adduct clusters into unified structural clusters.
5. Perform hierarchical correlation clustering using Pearson/Spearman correlation and flatten via constant threshold or silhouette-score optimization.
6. Assign each feature a structural cluster ID, adduct group, isotopologue pattern label, and correlation cluster ID; optionally annotate with compound name.
7. Validation: structural clusters must contain ≥2 co-eluting features per isotopologue or adduct group; silhouette score ≥0.20 indicates acceptable cluster separation; cross-assay links validated by neutral-mass match within ppm tolerance.
8. References: source article (DOI: 10.1371/journal.pcbi.1011814)

## Workflow Ports

**Inputs:**

- `lcms_intensity_data` — LC-MS intensity DataFrame with feature metadata in column names ← `task_001/model_metrics`
- `significant_feature_mask` — Binary mask or indices of statistically significant features

**Outputs:**

- `structural_clusters_table` — DataFrame with feature-to-cluster assignments and structural metadata
- `cluster_visualizations` — PNG/PDF figures of dendrogram, heatmaps, and silhouette plots

**Used:** `urn:asb:port:task_001/model_metrics`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:kopeckylukas__py-mamsi`
- **Synthesized at:** 2026-06-15T13:34:24+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
