# SciTask Card: Analyze reaction-level regulatory classification using the intersection of RPS-vs-FFD and RAS-vs-FFD fold-changes

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:26:15.469347+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_integrate`
- Domain: `bioinformatics`
- Subtask categories: `data-analysis`, `statistical-analysis`, `information-extraction`
- DOI: `10.1371/journal.pcbi.1009337`
- GitHub: `qLSLab/integrate`
- Input from: `task_001`

## Classification

- Task kind: `analysis`
- Article type: `research-article`
- Primary domain: `multi-omics`
- Subdomains: `multi-omics-integration`, `computational-metabolomics`, `fluxomics`
- Techniques: `flux-analysis`, `multi-omics-integration`, `pathway-analysis`, `differential-abundance-analysis`
- Keywords: `constraint-based metabolic modeling` · `metabolic flux prediction` · `transcriptomics integration` · `metabolomics integration` · `multi-level metabolic regulation` · `gene expression` · `substrate availability` · `enzyme kinetics` · `Michaelis-Menten law` · `systems metabolism`

## Research Question
How can RAS, RPS, and FFD datasets be intersected to classify each metabolic reaction into regulatory categories (transcriptional, metabolic, combined, or unclassified)?

## Connected Finding
Reactions are classified by measuring Cohen's kappa concordance between RAS-vs-FFD and RPS-vs-FFD variation signs: positive concordance for both indicates combined regulation, positive RPSvsFFD with negative RASvsFFD indicates metabolic control only, and positive values for both RASvsFFD and RASvsRPS indicates transcriptional and metabolic regulation.

## Task Description
Classify metabolic reactions into regulatory categories (transcriptional, metabolic, combined, or unclassified) by computing Cohen's kappa concordance scores between RAS-vs-FFD and RPS-vs-FFD fold-change directions across all pairwise cell-line comparisons, and produce a labelled reaction classification table.

## Inputs
- RAS (Reaction Activity Score) dataset for all reactions and cell lines from ENGRO2 model (Zenodo 10.5281/zenodo.5824504 or qLSLab/integrate repository)
- RPS (Reaction Propensity Score) dataset computed from intracellular metabolomics concentrations
- FFD (Feasible Flux Distributions) sampled from constrained ENGRO2 metabolic models for each cell line (10 batches of 100,000 steady-state solutions each)
- Intracellular metabolomics data (LC-MS metabolite abundance measurements from MTBLS3597)
- Transcriptomics data (RNA-seq read counts in FPKM, deposited as PRJNA767228)

## Expected Outputs
- Reaction classification table (XLSX or CSV) with columns: reaction identifier, Cohen's kappa RPSvsFFD score, Cohen's kappa RPSvsRAS score, empirical p-value, FDR-adjusted p-value, regulatory class label (transcriptional/metabolic/combined/other), and confidence intervals
- Q–Q plot comparing empirical probability distribution of Cohen's kappa agreement between independent datasets versus INTEGRATE RPS-vs-FFD concordance results
- Heatmap visualization of RPSvsRAS and RPSvsFFD concordance scores for reactions with fair concordance (score >0.2), annotated with reaction names and regulatory class assignments

## Expected Output File

- `reaction_classification_table.xlsx`

## Landmark Outputs

- `concordance_scores_raw.csv`
- `variation_signs_by_pair.csv`
- `empirical_pvalue_distribution.csv`
- `fdr_corrected_classifications.csv`

## Tools
- constraint-based stoichiometric metabolic models
- COBRApy (for optGpSampler uniform sampling)

## Skills
- reaction-flux-concordance-analysis
- cohen-kappa-interrater-reliability-scoring
- metabolic-regulation-classification-scheme
- fold-change-sign-determination-statistics
- fdr-correction-multiple-testing
- flux-variability-analysis-interpretation
- constraint-based-model-output-integration

## Workflow Description
1. Load pre-computed RAS, RPS, and FFD datasets from deposited sources (Zenodo 10.5281/zenodo.5824504 or GitHub qLSLab/integrate) for all reactions and cell-line pairs. 2. For each of the 10 pairwise cell-line comparisons, compute the sign of variation (up +1, down −1, no-change 0) for RAS and RPS using t-test and Mann–Whitney U test (p<0.05) with fold-change threshold ≥20%. 3. Compute the sign of FFD variation for each pair using Mann–Whitney U test on sampled flux distributions with log₂ fold-change ratio. 4. For each reaction, calculate two Cohen's kappa coefficients: RASvsFFD and RPSvsRAS, quantifying concordance of variation signs across the 10 pairwise comparisons. 5. Classify reactions into four categories: positive RASvsFFD and RPSvsRAS (combined transcriptional and metabolic), positive RPSvsFFD and negative RPSvsRAS (metabolic only), negative both scores with high RASvsFFD (transcriptional only), or positive RPSvsRAS but negative RPSvsFFD (unclassified/other). 6. Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR<5%. 7. Compile final classification table with reaction identifiers, Cohen's kappa scores, adjusted p-values, and assigned regulatory class.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `integrate.pdf` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| metabolights | `MTBLS3597` | https://www.ebi.ac.uk/metabolights/MTBLS3597 | etails on data processing the at www.ebi.ac.uk/metabolights/MTBLS3597. Normalized data (on utational analyses are reported in S1 |
| bioproject | `PRJNA767228` | https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228 | sing the h abundance was measured i Raw reads are available PRJNA767228. ENGRO2 model recon Starting from ENGRO1 [44 core model of |

## Missing Information
- The exact number of metabolic reactions in ENGRO2 model that have complete substrate abundance data available in the metabolomics dataset
- The computational method used to determine whether a fold-change or concordance variation is statistically significant when comparing a given cell-line pair across RAS, RPS, and FFD datasets
- The precise definition and cutoff thresholds used to classify reactions into the 'other' category (those with negative RPSvsFFD but positive RPSvsRAS that are not purely transcriptional)
- Whether the 10 pairwise cell-line comparisons include all possible pairs (5 choose 2 = 10) or a subset, and the specific identity of cell lines being compared
- The number of reactions discarded or marked as 'missing data' due to absence of GPR associations or incomplete substrate abundance coverage

## Domain Knowledge
- Cohen's kappa coefficient quantifies inter-rater agreement accounting for chance; values <0.2 indicate poor concordance, 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 good, and 0.81–1.0 very good agreement.
- Reaction classification assumes a monotonic relationship between RAS/RPS and FFD fold-changes; reactions lacking all substrate measurements are omitted from concordance analysis.
- Metabolic regulation occurs when substrate availability (RPS) concordantly drives flux variation (FFD) but gene expression (RAS) does not; transcriptional regulation is the inverse.
- Benjamini–Hochberg FDR correction maintains false discovery rate <5% when testing Cohen's kappa values across multiple reactions, accounting for multiple-comparisons bias.
- The fold-change threshold of ≥20% is relaxed relative to stricter single-gene thresholds because even modest differences in pathway enzyme abundance can dramatically alter flux through that pathway.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] How can RAS, RPS, and FFD datasets be intersected to classify each metabolic reaction into regulatory categories (transcriptional, metabolic, combined, or unclassified)?: 'INTEGRATE then assigns two scores to metabolic reactions. The first score quantifies the concordance level between the variation signs obtained for the RAS dataset and those obtained for the RPS'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] Reactions are classified by measuring Cohen's kappa concordance between RAS-vs-FFD and RPS-vs-FFD variation signs: positive concordance for both indicates combined regulation, positive RPSvsFFD with negative RASvsFFD indicates metabolic control only, and positive values for both RASvsFFD and RASvsRPS indicates transcriptional and metabolic regulation.: 'Reactions displaying positive values for both RPSvsFFD and RPSvsRAS scores (first quadrant). Variations in these reactions must be imputed to transcriptional and metabolic regulation. Reactions'
- `ev_003` from `agent2_synthesis` (agent2_traced): [results] RAS (Reaction Activity Score) dataset for all reactions and cell lines from ENGRO2 model (Zenodo 10.5281/zenodo.5824504 or qLSLab/integrate repository): 'Scripts to reproduce the integrate, and are also available at https://github.com/qLSLab/integrate'
- `ev_004` from `agent2_synthesis` (agent2_traced): [results] RPS (Reaction Propensity Score) dataset computed from intracellular metabolomics concentrations: 'INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes'
- `ev_005` from `agent2_synthesis` (agent2_traced): [results] FFD (Feasible Flux Distributions) sampled from constrained ENGRO2 metabolic models for each cell line (10 batches of 100,000 steady-state solutions each): 'we sampled a million steady state solutions of the ENGRO2 model in all the tested conditions. To get a large number of samples, we used the batch generator option of the algorithm, creating ten'
- `ev_006` from `agent2_synthesis` (agent2_traced): [results] Intracellular metabolomics data (LC-MS metabolite abundance measurements from MTBLS3597): 'raw data are deposited at www.ebi.ac.uk/metabolights/MTBLS3597'
- `ev_007` from `agent2_synthesis` (agent2_traced): [results] Transcriptomics data (RNA-seq read counts in FPKM, deposited as PRJNA767228): 'Raw reads are available in NCBI Short Reads Archive (SRA) under Accession Number PRJNA767228'
- `ev_008` from `agent2_synthesis` (agent2_traced): [results] Reaction classification table (XLSX or CSV) with columns: reaction identifier, Cohen's kappa RPSvsFFD score, Cohen's kappa RPSvsRAS score, empirical p-value, FDR-adjusted p-value, regulatory class label (transcriptional/metabolic/combined/other), and confidence intervals: 'Table of RPSvsRAS and RPSvsFFD Cohen's kappa coefficients, empirical and adjusted p-values and confidence intervals for all model reactions'
- `ev_009` from `agent2_synthesis` (agent2_traced): [results] Q–Q plot comparing empirical probability distribution of Cohen's kappa agreement between independent datasets versus INTEGRATE RPS-vs-FFD concordance results: 'Q − Q plot between the empirical probability of agreement between two independent datasets and INTEGRATE Cohen's kappa distribution'
- `ev_010` from `agent2_synthesis` (agent2_traced): [results] Heatmap visualization of RPSvsRAS and RPSvsFFD concordance scores for reactions with fair concordance (score >0.2), annotated with reaction names and regulatory class assignments: 'Heatmap showing the RPSvsRAS and the RPSvsFFD concordance scores, for reactions having a level of concordance between RPS and FFD greater than 0.2'
- `ev_011` from `agent2_synthesis` (agent2_traced): [abstract] constraint-based stoichiometric metabolic models: 'using constraint-based stoichiometric metabolic models as a scaffold'
- `ev_012` from `agent2_synthesis` (agent2_traced): [results] COBRApy (for optGpSampler uniform sampling): 'optGpSampler algorithm [71] available in COBRApy [72]'
- `ev_013` from `agent2_synthesis` (agent2_traced): [results] The exact number of metabolic reactions in ENGRO2 model that have complete substrate abundance data available in the metabolomics dataset: 'we computed for each reaction r and for each cell line c (assumed at steady state) a Reaction Propensity Score (RPS)'
- `ev_014` from `agent2_synthesis` (agent2_traced): [results] The computational method used to determine whether a fold-change or concordance variation is statistically significant when comparing a given cell-line pair across RAS, RPS, and FFD datasets: 'We consider a variation as statistically significant if both test is rejected according to any suited statistical test and if the variation exceeds a threshold value'
- `ev_015` from `agent2_synthesis` (agent2_traced): [results] The precise definition and cutoff thresholds used to classify reactions into the 'other' category (those with negative RPSvsFFD but positive RPSvsRAS that are not purely transcriptional): 'we simply labeled this category as 'other''
- `ev_016` from `agent2_synthesis` (agent2_traced): [results] Whether the 10 pairwise cell-line comparisons include all possible pairs (5 choose 2 = 10) or a subset, and the specific identity of cell lines being compared: 'for all eligible reactions, i.e. reactions for which quantification of all substrate abundances was available. We focused on the qualitative concordance'
- `ev_017` from `agent2_synthesis` (agent2_traced): [results] The number of reactions discarded or marked as 'missing data' due to absence of GPR associations or incomplete substrate abundance coverage: 'For reactions not associated with a GPR the RAS was set to 1'

## Evaluation Strategy
### Direct Checks
- file_exists: verify that RAS, RPS, and FFD datasets are deposited in Zenodo (10.5281/zenodo.5824504) or S1 Compressed File Archive and contain reaction-by-sample-by-cellline matrices
- file_format_is: RAS dataset contains normalized Reaction Activity Scores (0–1 range) for each reaction and cell line, derived from transcriptomics via GPR rules
- file_format_is: RPS dataset contains Reaction Propensity Scores computed as product of substrate concentrations raised to stoichiometric coefficients for each reaction and cell line
- file_format_is: FFD dataset contains flux distributions sampled from feasible solution space; verify at least 100,000 steady-state solutions per cell line are present
- row_count_equals: verify classification table has one row per unique (reaction, cell-line-pair) combination; total rows should equal (number of eligible reactions) × 10 pairwise comparisons
- field_present: classification table contains columns: reaction_id, cell_line_pair, RPSvsFFD_concordance_score, RPSvsRAS_concordance_score, regulatory_class, cohen_kappa_value
- value_in_range: Cohen's kappa values in classification table range from -1.0 to +1.0 (robust to parameter choices in concordance computation)
- contains_substring: classification table regulatory_class column contains only values from {transcriptional, metabolic, combined, unclassified, other} matching paper's four-category scheme
- output_matches_reference: classification results for ENGRO2 match or closely align with Fig 4B heatmap (RPSvsRAS and RPSvsFFD scores) and the stated outcomes (44 transcriptional+metabolic, 13 metabolic only) — multiple defensible approaches to exact matching acceptable due to stochasticity in sampling
- script_runs: verify that Cohen's kappa calculation script (from qLSLab/integrate GitHub or Zenodo) executes without error on input RAS, RPS, FFD matrices and produces a kappa coefficient matrix

### Expert Review
- Verify that the concordance classification logic correctly implements the decision rules stated in the paper: positive RPSvsFFD + positive RPSvsRAS → transcriptional+metabolic; positive RPSvsFFD + negative RPSvsRAS → metabolic only; negative RPSvsFFD + positive RPSvsRAS → transcriptional only; negative RPSvsFFD + negative RPSvsRAS → unclassified/other
- Assess whether the threshold of Cohen's kappa > 0.2 for 'fair concordance' is applied consistently across all reactions and whether the FDR-adjusted p-value cutoff (5%) appropriately filters spurious concordance assignments
- Evaluate whether reactions with missing substrate abundance data (omitted from RPS calculation) are correctly marked as ineligible for RPS-based classification and handled transparently in the final table
- Judge whether the handling of reactions lacking GPR associations (RAS = 1.0 by default) in the RPSvsRAS concordance calculation is scientifically justified and clearly documented in the classification table
- Review whether the classification assignments are biologically plausible by spot-checking 5–10 reactions with well-characterized metabolic regulation (e.g., ACONT, RPI, RPE) against literature and the paper's mechanistic descriptions

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load pre-computed RAS, RPS, and FFD datasets from deposited repositories for all reactions and pairwise cell-line comparisons.
2. Compute signed fold-change directions (up/down/no-change) for each reaction across 10 pairwise cell-line comparisons using statistical tests (Mann–Whitney U for FFD, t-test for RAS/RPS) with p<0.05 and ≥20% fold-change threshold.
3. Calculate two Cohen's kappa coefficients per reaction quantifying concordance between RAS-vs-FFD and RPS-vs-RAS fold-change sign patterns.
4. Classify reactions into regulatory categories based on quadrant assignment: positive RASvsFFD + positive RPSvsRAS = combined; positive RPSvsFFD + negative RPSvsRAS = metabolic-only; negative both + high RASvsFFD = transcriptional-only; other = unclassified.
5. Compute empirical p-values by repeated random sampling (1000 iterations) of RPS variation distributions and derive FDR-adjusted p-values using Benjamini–Hochberg procedure with target FDR <5%.
6. Validation: reactions ACONT, ASPTA, RPI, and RPE show statistically significant concordance (FDR<5%) in both core and genome-wide models, confirming robustness of classification scheme.
7. References: source article (DOI: 10.1371/journal.pcbi.1009337); MTBLS3597 (https://www.ebi.ac.uk/metabolights/MTBLS3597); PRJNA767228 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228)

## Workflow Ports

**Inputs:**

- `ras_scores` — RAS (Reaction Activity Score) dataset ← `task_001/tsne_plot`
- `rps_scores` — RPS (Reaction Propensity Score) dataset
- `ffd_distributions` — FFD (Feasible Flux Distributions) sampled data
- `metabolomics_data` — Intracellular metabolomics measurements (LC-MS)
- `transcriptomics_data` — RNA-seq read counts (FPKM)

**Outputs:**

- `reaction_classification_table` — Reaction classification table with regulatory class labels and concordance scores
- `qq_plot` — Q–Q plot of empirical concordance distribution
- `concordance_heatmap` — Heatmap of RPSvsRAS and RPSvsFFD concordance scores

**Used:** `urn:asb:port:task_001/tsne_plot`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
