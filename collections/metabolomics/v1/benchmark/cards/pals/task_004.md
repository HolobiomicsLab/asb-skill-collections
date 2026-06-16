# SciTask Card: Analyze sensitivity of PALS pathway rankings under simulated noise and peak dropout

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T21:26:46.708623+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_pals/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `benchmark-evaluation`, `statistical-analysis`
- DOI: `10.1186/1471-2105-6-225`
- GitHub: `glasgowcompbio/PALS`
- Input from: `task_002`

## Classification

- Task kind: `analysis`
- Article type: `research-article`
- Primary domain: `transcriptomics`
- Subdomains: `differential-expression`, `gene-regulation`
- Techniques: `dimensionality-reduction`, `pathway-analysis`, `enrichment-analysis`
- Keywords: `pathway activity scoring` · `plage method` · `metabolomics peak detection` · `untargeted metabolomics` · `molecular families` · `mass2motifs` · `fragmentation spectra analysis`

## Research Question
How does the rank-order stability of top-scoring pathways in PALS degrade as Gaussian noise and random peak removal increase in severity across a metabolomics dataset?

## Connected Finding
PALS demonstrates robustness to noise and missing peaks in metabolomics data, outperforming ORA and GSEA alternatives on these dimensions.

## Task Description
Inject systematically increasing levels of Gaussian noise and random peak removal into a reference metabolomics dataset, process each perturbed dataset through PALS, and quantify the rank-order stability of top-scoring pathways relative to the clean-data baseline to assess robustness.

## Inputs
- Reference metabolomics dataset: peak intensity matrix (samples × features) and associated pathway annotations (metabolite-to-pathway membership table)

## Expected Outputs
- Rank-order stability metrics: a table with noise level (% Gaussian + % peak removal) as rows and Spearman/Kendall correlation coefficient and top-K retention percentage as columns
- Stability curve plot: x-axis = noise/peak-removal level, y-axis = correlation coefficient or retention %; separate lines for noise alone, peak removal alone, and combined perturbation

## Expected Output File

- `pathway_stability_metrics.csv`

## Landmark Outputs

- `clean_baseline_pathway_scores.csv`
- `perturbed_datasets_pathways_scores_*.csv`
- `rank_correlation_matrix.csv`
- `top_k_retention_table.csv`

## Tools
- PALS (Pathway Activity Level Scoring)

## Skills
- metabolomics-noise-perturbation-simulation
- pathway-rank-stability-assessment
- peak-removal-robustness-testing
- pathway-activity-decomposition-via-plage
- rank-order-correlation-analysis

## Workflow Description
1. Load reference metabolomics dataset (peak intensity matrix and pathway annotations). 2. Establish clean baseline by running PALS on unperturbed data and record ranked pathway activity scores. 3. For each noise level (0%, 5%, 10%, 15%, 20%, 25% Gaussian noise intensity and 0%, 5%, 10%, 15%, 20% random peak removal rate), create a perturbed copy of the dataset. 4. Run PALS on each perturbed dataset using the same pathway decomposition (PLAGE method) and record ranked pathway activity scores. 5. Compute rank-order correlation (Spearman's rho or Kendall's tau) between perturbed pathway rankings and clean baseline ranking for each noise condition. 6. Compute the percentage of top-K pathways (K=5, 10, 20) that remain in the top-K set across noise conditions. 7. Generate a stability plot showing correlation or retention percentage vs. noise level and tabulate results.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/annot_df.png` | figure | False |
| `figures/int_df.png` | figure | False |
| `figures/logo.png` | figure | False |
| `figures/logo_transparent.png` | figure | False |
| `figures/output.png` | figure | False |
| `figures/overall_schematic.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history documented
- Exact synthesis/documentation date provided (2026-06-15T21:26:44+00:00) but no commit hash, branch, or software version tag specified for glasgowcompbio/PALS source

## Domain Knowledge
- PALS uses the PLAGE (Pathway Level Analysis of Gene Expression) decomposition method, which is sensitive to input data integrity and mass spectrometry peak quality.
- Gaussian noise in metabolomics simulates instrument detector noise and baseline drift; peak removal simulates missed peaks due to low S/N ratio or chromatographic co-elution.
- Rank-order stability (preserved top-K pathways or Spearman ρ ≥ 0.8) is the standard robustness criterion in metabolomics pathway analysis, as absolute scores may shift but biologically relevant pathways should remain highly ranked.
- PALS robustness advantage over ORA and GSEA depends on the decomposition preserving pathway activity signal under perturbation; this property must be empirically validated across noise regimes.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Rank-order stability metrics: a table with noise level (% Gaussian + % peak removal) as rows and Spearman/Kendall correlation coefficient and top-K retention percentage as columns, Stability curve plot: x-axis = noise/peak-removal level, y-axis = correlation coefficient or retention %; separate lines for noise alone, peak removal alone, and combined perturbation.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does the rank-order stability of top-scoring pathways in PALS degrade as Gaussian noise and random peak removal increase in severity across a metabolomics dataset?: 'The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] PALS demonstrates robustness to noise and missing peaks in metabolomics data, outperforming ORA and GSEA alternatives on these dimensions.: 'The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA).'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Reference metabolomics dataset: peak intensity matrix (samples × features) and associated pathway annotations (metabolite-to-pathway membership table): 'metabolomics peak data'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Rank-order stability metrics: a table with noise level (% Gaussian + % peak removal) as rows and Spearman/Kendall correlation coefficient and top-K retention percentage as columns: 'robust to noise and missing peaks'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Stability curve plot: x-axis = noise/peak-removal level, y-axis = correlation coefficient or retention %; separate lines for noise alone, peak removal alone, and combined perturbation: 'robust to noise and missing peaks'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] PALS (Pathway Activity Level Scoring): 'we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways, decomposes activity levels in pathways'
- `ev_007` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history documented: '_No changelog found._'
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] Exact synthesis/documentation date provided (2026-06-15T21:26:44+00:00) but no commit hash, branch, or software version tag specified for glasgowcompbio/PALS source: 'Synthesized at: 2026-06-15T21:26:44+00:00'

## Evaluation Strategy
### Direct Checks
- verify that input metabolomics dataset file exists in glasgowcompbio/PALS repository or is a publicly deposited reference dataset with accession or DOI
- verify that PALS software can be installed and executed from github:glasgowcompbio/PALS source
- verify that noise injection script produces output files with Gaussian noise applied at each specified level (e.g., SNR = 10, 5, 2, 1) — file_exists and file_format_is CSV or HDF5
- verify that peak removal simulation script executes without error and produces degraded datasets with 5%, 10%, 20%, 50% random peak removal — script_runs and output_matches_reference structure
- verify that pathway rank-order stability metric (e.g., Spearman correlation or Kendall τ of top-N pathway scores) is computed for each noise/peak-removal condition relative to clean-data baseline — value_in_range [0, 1]
- verify that stability scores decrease monotonically or show expected degradation pattern as noise and peak removal increase — robust to parameter choices within reasonable noise and removal ranges
- verify that final summary table contains columns: [noise_level, peak_removal_percent, top_N_pathways_corr, rank_stability_score, pathway_count_affected] with numeric values populated — field_present and row_count_equals ≥ number of noise/removal combinations tested

### Expert Review
- validate that the choice of noise model (Gaussian with specified SNR levels) and peak-removal mechanism (random selection) are appropriate for assessing metabolomics data robustness; confirm alignment with experimental noise profiles in LC-MS/MS data
- assess whether the rank-order stability metric (e.g., Spearman ρ or Kendall τ) and the choice of top-N pathways (N=5, 10, etc.) capture clinically or biologically meaningful shifts in pathway prioritization
- review whether observed stability patterns (e.g., PALS outperforming ORA/GSEA under noise, as claimed in literature) are replicated; interpret any deviations and assess whether they support or contradict the robustness finding

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load reference metabolomics dataset and pathway annotations.
2. Run PALS on clean unperturbed data; record and rank pathway activity scores as baseline.
3. Systematically generate perturbed datasets by injecting Gaussian noise and removing random peaks across multiple intensity levels.
4. Run PALS on each perturbed dataset using identical decomposition parameters; record ranked pathway scores.
5. Compute rank-order correlations (Spearman ρ, Kendall τ) and top-K retention percentages between perturbed and baseline rankings.
6. Validation: confirm that pathway rank-order correlation remains ≥ 0.80 and top-5 pathway retention ≥ 80% under combined noise and peak-removal up to 10% intensity threshold, consistent with reported PALS robustness advantage.
7. References: source article (DOI: 10.1186/1471-2105-6-225)

## Workflow Ports

**Inputs:**

- `peak_intensity_matrix` — Reference metabolomics peak intensity matrix (samples × features) ← `task_002/pathway_scores_table`
- `pathway_annotations` — Metabolite-to-pathway membership annotations

**Outputs:**

- `stability_metrics_table` — Rank-order stability metrics table (noise level vs. correlation and retention %)
- `stability_curve_plot` — Stability curve visualization (noise level vs. pathway ranking correlation/retention)

**Used:** `urn:asb:port:task_002/pathway_scores_table`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:glasgowcompbio__PALS`
- **Synthesized at:** 2026-06-15T21:33:33+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
