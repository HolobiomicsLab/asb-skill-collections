# SciTask Card: Reproduce PALS robustness comparison against ORA and GSEA baselines

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T21:26:46.708623+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_pals/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `benchmark-evaluation`, `statistical-analysis`
- DOI: `10.1186/1471-2105-6-225`
- GitHub: `glasgowcompbio/PALS`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `transcriptomics`
- Subdomains: `differential-expression`, `gene-regulation`
- Techniques: `dimensionality-reduction`, `pathway-analysis`, `enrichment-analysis`
- Keywords: `pathway activity scoring` · `plage method` · `metabolomics peak detection` · `untargeted metabolomics` · `molecular families` · `mass2motifs` · `fragmentation spectra analysis`

## Research Question
Does PALS demonstrate greater robustness to noise and missing peaks in metabolomics peak data compared to ORA and GSEA methods?

## Connected Finding
PALS exhibits greater robustness to noise and missing peaks compared to ORA and GSEA alternatives, with particular importance for metabolomics peak data where such artifacts are prevalent.

## Task Description
Re-run PALS (PLAGE-based pathway activity scoring) alongside ORA and GSEA on the same metabolomics peak dataset and reproduce the reported finding that PALS is more robust to noise and missing peaks than either baseline method. Output a comparison report with robustness metrics.

## Inputs
- Metabolomics peak dataset (intensity matrix: peaks × samples)
- Pathway or metabolite set database (e.g., KEGG, HMDB, or custom collection)

## Expected Outputs
- Robustness comparison table (methods × noise-level × robustness-metric)
- Robustness metric visualization (e.g., line plot or heatmap showing PALS vs. ORA vs. GSEA performance under noise)

## Expected Output File

- `robustness_comparison.csv`

## Landmark Outputs

- `pals_original_scores.csv`
- `ora_original_scores.csv`
- `gsea_original_scores.csv`
- `pals_noise_perturbed_scores.csv`
- `ora_noise_perturbed_scores.csv`
- `gsea_noise_perturbed_scores.csv`

## Tools
- PALS (Pathway Activity Level Scoring)

## Skills
- metabolite-set-activity-scoring
- pathway-database-integration
- robustness-analysis-under-perturbation
- missing-data-simulation-in-omics
- comparative-enrichment-method-evaluation

## Workflow Description
1. Load metabolomics peak dataset and pathway/metabolite set database. 2. Apply PALS decomposition using the PLAGE method to compute pathway activity scores. 3. Apply ORA (Over-Representation Analysis) on the same dataset using standard hypergeometric test. 4. Apply GSEA (Gene Set Enrichment Analysis) on the same dataset using ranked scoring approach. 5. Systematically introduce noise and missing peaks at controlled levels (e.g., 10%, 25%, 50% dropout) to the original peak data. 6. Re-run all three methods (PALS, ORA, GSEA) on each noise-perturbed dataset variant. 7. Compute robustness metrics (e.g., rank correlation, result stability, or effect size preservation) between original and perturbed results for each method. 8. Generate comparison table and visualization showing PALS robustness advantage over ORA and GSEA across noise levels.

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
- No changelog documenting software versions, dependencies, or reproducibility instructions is present
- Location and format of the metabolomics peak dataset used in the robustness comparison are not specified in the discussion
- Specific versions or parameterizations of ORA and GSEA baseline implementations are not documented
- Quantitative definitions of 'robustness' (e.g., metric type, threshold, statistical test) are not stated in the discussion section

## Domain Knowledge
- PLAGE (Pathway Level Analysis of Gene Expression) decomposes multivariate pathway activity using singular value decomposition of gene/metabolite expression within pathway members.
- ORA (Over-Representation Analysis) tests pathway significance using hypergeometric distributions based on counts of significantly altered members, and is sensitive to missing or noisy low-abundance peaks.
- GSEA (Gene Set Enrichment Analysis) ranks all features and tests cumulative enrichment; it is less sensitive to arbitrary significance thresholds but may lose power under high missing-data rates.
- Metabolomics peak data exhibits inherent missingness (detection limits, instrument drift, ionization variability) that can degrade pathway analysis; robustness metrics should measure consistency of pathway rankings or effect sizes under systematic peak dropout.
- True robustness evaluation requires controlled in-silico perturbation (noise injection, peak removal) applied consistently across all methods to isolate method-specific resilience from data quality.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does PALS demonstrate greater robustness to noise and missing peaks in metabolomics peak data compared to ORA and GSEA methods?: 'The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] PALS exhibits greater robustness to noise and missing peaks compared to ORA and GSEA alternatives, with particular importance for metabolomics peak data where such artifacts are prevalent.: 'The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Metabolomics peak dataset (intensity matrix: peaks × samples): 'metabolomics peak dataset'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Pathway or metabolite set database (e.g., KEGG, HMDB, or custom collection): 'database queries of pathways'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Robustness comparison table (methods × noise-level × robustness-metric): 'more robust to noise and missing peaks'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Robustness metric visualization (e.g., line plot or heatmap showing PALS vs. ORA vs. GSEA performance under noise): 'more robust to noise and missing peaks compared to the alternatives'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] PALS (Pathway Activity Level Scoring): 'we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways, decomposes activity levels in pathways'
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting software versions, dependencies, or reproducibility instructions is present: 'No changelog found.'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] Location and format of the metabolomics peak dataset used in the robustness comparison are not specified in the discussion: '[UNTRUSTED_DOCUMENT] (entire section contains only metadata and reference headers; no dataset URI or format given)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] Specific versions or parameterizations of ORA and GSEA baseline implementations are not documented: '[UNTRUSTED_DOCUMENT] (section provides no methodological detail on baseline tool configuration)'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] Quantitative definitions of 'robustness' (e.g., metric type, threshold, statistical test) are not stated in the discussion section: '[UNTRUSTED_DOCUMENT] (section contains no results table, figure reference, or numerical claim)'

## Evaluation Strategy
### Direct Checks
- verify that github:glasgowcompbio__PALS repository contains executable PALS implementation with PLAGE-based scoring
- verify that a metabolomics peak dataset (with noise and missing peak variants) is available in the repository or a linked public deposit (Zenodo/GitHub/MassIVE/MetaboLights)
- verify that ORA and GSEA implementations are available as callable tools or Python/R packages with pinned versions
- verify that comparison script produces three sets of pathway/metabolite-set scores (PALS, ORA, GSEA) on identical input
- verify output files contain quantitative robustness metrics (e.g., correlation, F1-score, or error rate) across noise levels and missing-peak percentages
- robust to parameter choices: confirm that metrics show PALS with lower variance or higher accuracy than ORA and GSEA across at least two independent noise-injection or peak-removal regimes

### Expert Review
- confirm that noise injection and missing-peak simulation strategies are methodologically sound and reproducible (e.g., Gaussian noise, random peak dropout percentages)
- confirm that reported robustness advantage (PALS vs ORA/GSEA) is statistically significant and not attributable to tuning bias or parameter mismatch
- confirm that the same metabolite-set annotations and pathway database are used for all three methods to ensure fair comparison

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load metabolomics peak intensity matrix and pathway/metabolite set annotations.
2. Compute pathway activity scores using PALS (PLAGE decomposition), ORA (hypergeometric test), and GSEA (ranked enrichment).
3. Generate in-silico noise-perturbed datasets by randomly removing peaks at controlled rates (e.g., 10%, 25%, 50%).
4. Re-run all three methods on each perturbed dataset variant.
5. Calculate robustness metrics (e.g., Spearman rank correlation, or fraction of pathways with consistent effect-size direction) comparing original vs. perturbed results.
6. Validation: PALS exhibits higher rank-correlation stability and effect-size preservation across all noise levels compared to ORA and GSEA, reproducing the reported robustness advantage.
7. References: source article (DOI: 10.1186/1471-2105-6-225)

## Workflow Ports

**Inputs:**

- `peak_matrix` — Metabolomics peak intensity matrix (peaks × samples)
- `metabolite_db` — Pathway or metabolite set database

**Outputs:**

- `robustness_table` — Robustness comparison table (methods × noise-level × metric)
- `robustness_plot` — Robustness visualization across noise levels

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:glasgowcompbio__PALS`
- **Synthesized at:** 2026-06-15T21:33:33+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
