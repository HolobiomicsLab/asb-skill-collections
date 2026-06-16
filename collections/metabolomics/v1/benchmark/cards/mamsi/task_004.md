# SciTask Card: Analyze the effect of adduct mode selection on structural cluster outputs

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T13:26:03.540713+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_mamsi/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `statistical-analysis`, `visualization`
- DOI: `10.1371/journal.pcbi.1011814`
- GitHub: `kopeckylukas/py-mamsi`
- Input from: `task_001`

## Classification

- Task kind: `analysis`
- Article type: `research-article`
- Primary domain: `multi-omics`
- Subdomains: `multi-omics-integration`, `computational-metabolomics`, `biomarker-discovery`
- Techniques: `multivariate-statistics`, `partial-least-squares`, `pathway-analysis`, `dimensionality-reduction`, `normalization`, `statistical-analysis`

## Research Question
How do structural cluster outputs (cluster count and size distribution) differ between using all adducts versus only the most-common adducts in the MAMSI framework's adduct signature search?

## Connected Finding
MAMSI enables clustering of LC-MS features by structural properties through adduct signature detection, which can be parameterized to search either all common adducts or a restricted set of most-common adducts.

## Task Description
Run the MAMSI structural search pipeline on a selected LC-MS feature list under two adduct-selection modes ('all' vs. 'most-common'), compare the resulting structural cluster counts and size distributions, and produce a summary results table quantifying differences.

## Inputs
- Selected LC-MS feature intensity table (rows: samples, columns: features with naming convention (AssayName)_(RTsec)_(m/z)m/z, e.g. HPOS_233.25_149.111m/z)

## Expected Outputs
- Structural cluster results table containing cluster ID, cluster size, member features, isotopologue group, adduct group, and cross-assay link status for 'all adducts' mode
- Structural cluster results table for 'most-common adducts' mode with identical columns as 'all adducts' mode output
- Comparative summary table with rows for each adduct mode, columns: Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage (%)

## Expected Output File

- `cluster_comparison_summary.csv`

## Landmark Outputs

- `structural_clusters_all_adducts.csv`
- `structural_clusters_most_common_adducts.csv`
- `cluster_size_distribution_comparison.png`

## Tools
- Python
- pandas
- numpy
- matplotlib
- MAMSI (MamsiStructSearch)

## Skills
- lc-ms-adduct-pattern-detection
- isotopologue-signature-identification
- spectral-feature-clustering-and-comparison
- mass-spectrometry-structural-annotation
- cross-assay-feature-linkage-analysis
- data-summarization-and-tabulation

## Workflow Description
1. Load the selected LC-MS feature intensity data into MamsiStructSearch using load_lcms() with column naming convention (AssayName)_(RTsec)_(m/z)m/z. 2. Call get_structural_clusters() with adducts='all' parameter to identify isotopologue signatures (mass difference 1.00335 Da), adduct patterns (ESI-based neutral mass matching at 15 ppm tolerance), and cross-assay links ([M+H]+/[M-H]- references); merge overlapping clusters into structural clusters. 3. Extract cluster metadata (cluster ID, size, member count, feature composition) and compute summary statistics (total cluster count, mean/median/max cluster sizes, size distribution histogram). 4. Repeat steps 2–3 using adducts='most-common' parameter. 5. Compare outputs side-by-side: tabulate cluster counts, generate size-distribution plots for both modes, and compute effect-size differences (absolute and percentage change in cluster count and mean cluster size). 6. Produce a consolidated results table with columns: Adduct Mode, Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage (% features in ≥1 cluster).

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
- No changelog documenting version history, bug fixes, or feature changes for the py-mamsi package.

## Domain Knowledge
- Isotopologue signatures are identified by searching mass differences of 1.00335 Da between m/z values within RT windows of 5 seconds.
- Adduct patterns are detected by calculating hypothetical neutral masses from common ESI adducts and matching m/z values within 15 ppm tolerance; 'all adducts' mode uses the complete Fiehn Lab adduct calculator set, while 'most-common' uses Waters ESI documentation standards.
- Overlapping isotopologue and adduct clusters are merged into structural clusters; cross-assay links are established using [M+H]+/[M-H]- as reference ions.
- Cluster size distribution and coverage metrics (percentage of features assigned to at least one cluster) are sensitive to adduct-set selection and may reveal mode-dependent feature groupings.
- The LC-MS column naming convention (AssayName)_(RTsec)_(m/z)m/z is required for metadata extraction; deviations cause parsing failure.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: pandas, numpy, matplotlib, Structural cluster results table containing cluster ID, cluster size, member features, isotopologue group, adduct group, and cross-assay link status for 'all adducts' mode, Structural cluster results table for 'most-common adducts' mode with identical columns as 'all adducts' mode output, Comparative summary table with rows for each adduct mode, columns: Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage (%).

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How do structural cluster outputs (cluster count and size distribution) differ between using all adducts versus only the most-common adducts in the MAMSI framework's adduct signature search?: 'the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] MAMSI enables clustering of LC-MS features by structural properties through adduct signature detection, which can be parameterized to search either all common adducts or a restricted set of most-common adducts.: 'This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Selected LC-MS feature intensity table (rows: samples, columns: features with naming convention (AssayName)_(RTsec)_(m/z)m/z, e.g. HPOS_233.25_149.111m/z): 'Load Selected LC-MS Features
struct.load_lcms(selected)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Structural cluster results table containing cluster ID, cluster size, member features, isotopologue group, adduct group, and cross-assay link status for 'all adducts' mode: 'get_structural_clusters(adducts = 'all', annotate = True)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Structural cluster results table for 'most-common adducts' mode with identical columns as 'all adducts' mode output: 'get_structural_clusters(adducts = 'most-common', annotate = True)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Comparative summary table with rows for each adduct mode, columns: Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage (%): 'Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Python: 'MAMSI is a Python framework'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] pandas: 'import pandas as pd'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] numpy: 'import numpy as np'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] matplotlib: 'from matplotlib import pyplot as plt'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] MAMSI (MamsiStructSearch): 'A class for performing structural search on multi-modal MS data using'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting version history, bug fixes, or feature changes for the py-mamsi package.: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify that kopeckylukas/py-mamsi repository exists and is accessible at https://github.com/kopeckylukas/py-mamsi
- verify that kopeckylukas/py-mamsi-tutorials repository exists with sample LC-MS feature list data at https://github.com/kopeckylukas/py-mamsi-tutorials
- script_runs: execute MAMSI structural clustering workflow on provided LC-MS feature list with 'all adducts' parameter configuration without errors
- script_runs: execute MAMSI structural clustering workflow on same LC-MS feature list with 'most-common adducts' parameter configuration without errors
- file_exists: results table comparing cluster count and size distribution between 'all adducts' and 'most-common adducts' conditions
- file_format_is: results table is in a standard tabular format (CSV, TSV, or pandas DataFrame pickle)
- field_present: results table contains at least column headers for 'condition', 'total_cluster_count', and cluster size distribution metrics
- robust to parameter choices: cluster count values are numeric integers ≥ 1, cluster size distribution metrics are numeric and non-negative

### Expert Review
- Do differences in cluster counts and size distributions between 'all adducts' vs 'most-common adducts' align with expected adduct ionisation behavior in electrospray LC-MS?
- Are the structural clusters formed by the 'most-common adducts' condition chemically and biochemically meaningful given the metabolomic context?
- Do reported cluster size distributions reflect plausible m/z and retention time groupings for metabolite ion families?

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load LC-MS feature intensity data with retention time and m/z metadata into MamsiStructSearch.
2. Execute structural clustering with 'all adducts' mode: identify isotopologues (1.00335 Da threshold), detect adduct patterns (15 ppm tolerance), merge overlapping clusters.
3. Compute cluster statistics for 'all adducts': total count, size distribution (mean, median, max), feature coverage percentage.
4. Repeat clustering and statistics with 'most-common adducts' mode.
5. Compare outputs: tabulate cluster counts, sizes, and coverage; compute absolute and percentage differences between modes.
6. Validation: verify that both modes produce cluster assignments for ≥80% of input features; confirm cluster count and size statistics are computed correctly by manual spot-check on a subset of clusters.
7. References: source article (DOI: 10.1371/journal.pcbi.1011814)

## Workflow Ports

**Inputs:**

- `lcms_feature_table` — Selected LC-MS feature intensity table (rows: samples, columns: features with LC-MS naming convention) ← `task_001/model_metrics`

**Outputs:**

- `clusters_all_adducts` — Structural cluster assignments using all adducts
- `clusters_most_common_adducts` — Structural cluster assignments using most-common adducts
- `comparison_summary` — Comparative summary table of cluster statistics across adduct modes

**Used:** `urn:asb:port:task_001/model_metrics`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:kopeckylukas__py-mamsi`
- **Synthesized at:** 2026-06-15T13:34:24+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
