# SciTask Card: Reproduce concordance analysis between RAS and RPS variants for 81 fully covered reactions

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:26:15.469347+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_integrate`
- Domain: `bioinformatics`
- Subtask categories: `data-analysis`, `statistical-analysis`
- DOI: `10.1371/journal.pcbi.1009337`
- GitHub: `qLSLab/integrate`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `multi-omics`
- Subdomains: `multi-omics-integration`, `computational-metabolomics`, `fluxomics`
- Techniques: `flux-analysis`, `multi-omics-integration`, `pathway-analysis`, `differential-abundance-analysis`
- Keywords: `constraint-based metabolic modeling` · `metabolic flux prediction` · `transcriptomics integration` · `metabolomics integration` · `multi-level metabolic regulation` · `gene expression` · `substrate availability` · `enzyme kinetics` · `Michaelis-Menten law` · `systems metabolism`

## Research Question
What are the Cohen's kappa concordance values between RAS and RPS directional changes for metabolic reactions with complete substrate metabolomics coverage across the five breast cell lines?

## Connected Finding
Concordance analysis of RAS and RPS directional variations across the 81 metabolic reactions with full substrate abundances yields Cohen's kappa values reported in a heatmap, with reactions ranked according to RPSvsFFD concordance scores and only those with scores greater than 0.2 displayed.

## Task Description
Using deposited RAS and RPS datasets from the INTEGRATE Zenodo archive (10.5281/zenodo.5824504), compute Cohen's kappa concordance scores between RAS and RPS directional changes across all pairwise comparisons of the five breast cell lines for the 81 reactions with complete substrate metabolomics coverage, and reproduce the concordance heatmap and scatter plot reported in Fig 4A–B.

## Inputs
- RAS (Reaction Activity Score) matrix for five breast cell lines (MCF102A, SKBR3, MCF7, MDAMB231, MDAMB361) from Zenodo deposit 10.5281/zenodo.5824504
- RPS (Reaction Propensity Score) matrix for five breast cell lines computed from intracellular metabolomics data (LC-MS, deposited at MTBLS3597) and reaction stoichiometry
- FFD (Feasible Flux Distribution) samples for five cell lines uniformly sampled from constrained metabolic models using optGpSampler
- Metadata table identifying the 81 reactions with complete substrate metabolomics coverage and their Gene-Protein-Reaction associations

## Expected Outputs
- Cohen's kappa concordance scores (RPSvsRAS and RPSvsFFD) for all 81 reactions with complete substrate coverage, formatted as a two-column numeric table with reaction names and kappa values
- Scatter plot (RPSvsFFD kappa vs. RPSvsRAS kappa) with reactions colored by RASvsFFD concordance score and labeled for kappa ≥ 0.2
- Heatmap of RPSvsRAS and RPSvsFFD Cohen's kappa values for reactions with RPSvsFFD concordance > 0.2, ordered by RPSvsFFD score
- Empirical p-values and Benjamini-Hochberg adjusted p-values (FDR < 5%) for each reaction's kappa concordance, assessed against the null distribution from random permutation of RPS variations

## Expected Output File

- `concordance_kappa_table.csv`

## Landmark Outputs

- `ras_variation_signs.csv`
- `rps_variation_signs.csv`
- `ffd_variation_signs.csv`
- `pairwise_kappa_matrix.csv`
- `scatter_concordance_plot.png`
- `heatmap_kappa_reactions.png`

## Tools
- constraint-based stoichiometric metabolic models
- COBRApy
- optGpSampler
- Mann-Whitney U test
- Cohen's kappa metric
- Benjamini-Hochberg FDR correction

## Skills
- metabolic-flux-concordance-analysis
- cohen-kappa-inter-rater-reliability
- reaction-activity-score-computation
- reaction-propensity-score-mass-action-law
- feasible-flux-distribution-sampling
- multi-omics-dataset-integration
- statistical-significance-testing-metabolic-networks

## Workflow Description
1. Load RAS (Reaction Activity Score) vectors for all five cell lines from the deposited Zenodo dataset, derived from RNA-seq read counts and Gene-Protein-Reaction associations. 2. Load RPS (Reaction Propensity Score) vectors for all five cell lines from the deposited dataset, computed as the product of substrate concentrations raised to stoichiometric coefficients per the mass action law. 3. For each of the 10 pairwise cell-line comparisons, perform Mann-Whitney U testing (p < 0.05) on RAS and RPS distributions to determine the sign of directional change (up, down, or no-change) for each reaction. 4. Filter to retain only the 81 reactions for which all substrate abundances were quantified in the LC-MS metabolomics dataset. 5. For each reaction and each pairwise comparison, compute the Cohen's kappa coefficient quantifying agreement between RAS variation sign and RPS variation sign, accounting for chance agreement. 6. Generate a scatter plot with RPSvsRAS kappa on the y-axis and RPSvsFFD kappa on the x-axis, coloring points by RASvsFFD concordance score and labeling reactions with fair or better concordance (kappa ≥ 0.2). 7. Generate a heatmap displaying RPSvsRAS and RPSvsFFD kappa values for all 81 reactions, ordered by RPSvsFFD score. 8. Validation: verify that the produced kappa values and agreement distributions match those displayed in the published Fig 4A–B and that the empirical probability of agreement between RAS and RPS variations exceeds that expected from two independent random datasets.

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
- Exact formula and implementation details for Mann-Whitney U test p-value threshold and log₂ fold-change threshold (20%) application to determine directional signs for FFD variations across pairwise cell-line comparisons
- Specific file names and internal structure of the Zenodo 10.5281/zenodo.5824504 deposit containing RAS and RPS datasets, and whether they are pre-computed or require derivation from raw RNA-seq and metabolomics files
- Detailed filtering and data preprocessing steps applied to raw metabolomics data (from MetaboLights MTBLS3597) prior to RPS computation, including normalization, missing value handling, and quality control thresholds
- Rationale and justification for using Cohen's kappa (a discrete/categorical agreement metric) rather than a continuous concordance measure (e.g., Spearman or Pearson correlation) given that RAS and RPS are continuous-valued scores before sign discretization
- Explicit documentation of how the 81-reaction subset with 'full substrate abundances available' was determined, including what constitutes 'full coverage' and how reactions with missing or below-detection-limit metabolites are handled

## Domain Knowledge
- Cohen's kappa quantifies agreement between two raters beyond chance; values 0.21–0.40 indicate fair agreement, 0.41–0.60 moderate, 0.61–0.80 good, and 0.81–1.0 very good agreement.
- Reaction Activity Score (RAS) aggregates transcript abundance for enzyme subunits (AND logic) and isoforms (OR logic) to predict the maximal theoretical flux capacity of an enzyme-catalyzed reaction.
- Reaction Propensity Score (RPS) is computed from metabolomics data using the mass action law: the product of substrate concentrations each raised to their stoichiometric coefficient, predicting flux capacity constrained by substrate availability.
- A reaction is considered metabolically regulated if RPS and FFD (flux) directional changes agree (high RPSvsFFD kappa) but RAS and FFD changes disagree, indicating substrate availability, not enzyme abundance, determines flux variation.
- Reactions lacking complete quantification of all substrates in the metabolomics dataset are excluded from concordance analysis to ensure valid RPS computation.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] What are the Cohen's kappa concordance values between RAS and RPS directional changes for metabolic reactions with complete substrate metabolomics coverage across the five breast cell lines?: 'We quantified the level of concordance of the 10 variation signs (1 for each pair of cell lines) for a given pair of datasets by means of the Cohen's kappa metric'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] Concordance analysis of RAS and RPS directional variations across the 81 metabolic reactions with full substrate abundances yields Cohen's kappa values reported in a heatmap, with reactions ranked according to RPSvsFFD concordance scores and only those with scores greater than 0.2 displayed.: 'The heatmap in Fig 4B reports the RPSvsRAS and the RPSvsFFD concordance scores (Cohen's kappa) of ENGRO2 metabolic reactions, limited to the subset (of cardinality 81) of reactions for which'
- `ev_003` from `agent2_synthesis` (agent2_traced): [results] RAS (Reaction Activity Score) matrix for five breast cell lines (MCF102A, SKBR3, MCF7, MDAMB231, MDAMB361) from Zenodo deposit 10.5281/zenodo.5824504: 'available in Zenodo under permanent identifier 10.5281/zenodo.5824504'
- `ev_004` from `agent2_synthesis` (agent2_traced): [results] RPS (Reaction Propensity Score) matrix for five breast cell lines computed from intracellular metabolomics data (LC-MS, deposited at MTBLS3597) and reaction stoichiometry: 'raw data are deposited at www.ebi.ac.uk/metabolights/MTBLS3597'
- `ev_005` from `agent2_synthesis` (agent2_traced): [results] FFD (Feasible Flux Distribution) samples for five cell lines uniformly sampled from constrained metabolic models using optGpSampler: 'we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions'
- `ev_006` from `agent2_synthesis` (agent2_traced): [results] Metadata table identifying the 81 reactions with complete substrate metabolomics coverage and their Gene-Protein-Reaction associations: 'limited to the subset (of cardinality 81) of reactions for which quantification of all substrate abundances was available'
- `ev_007` from `agent2_synthesis` (agent2_traced): [results] Cohen's kappa concordance scores (RPSvsRAS and RPSvsFFD) for all 81 reactions with complete substrate coverage, formatted as a two-column numeric table with reaction names and kappa values: 'We quantified the level of concordance of the 10 variation signs (1 for each pair of cell lines) for a given pair of datasets by means of the Cohen's kappa metric'
- `ev_008` from `agent2_synthesis` (agent2_traced): [results] Scatter plot (RPSvsFFD kappa vs. RPSvsRAS kappa) with reactions colored by RASvsFFD concordance score and labeled for kappa ≥ 0.2: 'Fig 4A reports the concordance level between RAS and RPS variations (briefly RPSvsRAS) versus the concordance level between RPS and FFD variation (briefly RPSvsFFD), for the 81 metabolic reactions'
- `ev_009` from `agent2_synthesis` (agent2_traced): [results] Heatmap of RPSvsRAS and RPSvsFFD Cohen's kappa values for reactions with RPSvsFFD concordance > 0.2, ordered by RPSvsFFD score: 'The heatmap in Fig 4B reports the RPSvsRAS and the RPSvsFFD concordance scores (Cohen's kappa) of ENGRO2 metabolic reactions, limited to the subset (of cardinality 81)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [results] Empirical p-values and Benjamini-Hochberg adjusted p-values (FDR < 5%) for each reaction's kappa concordance, assessed against the null distribution from random permutation of RPS variations: 'we adjusted it with the Benjamini and Hochberg procedure to keep the False Discovery Rate (FDR) below 5%. After FDR correction of the p-values, the concordance between RPSs and FFDs resulted'
- `ev_011` from `agent2_synthesis` (agent2_traced): [results] COBRApy: 'we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72]'
- `ev_012` from `agent2_synthesis` (agent2_traced): [results] optGpSampler: 'we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions'
- `ev_013` from `agent2_synthesis` (agent2_traced): [results] Mann-Whitney U test: 'we first performed the Mann-Whitney U test [73] (p-value < 0.05) between the FFD distributions of each pair of the five cell lines'
- `ev_014` from `agent2_synthesis` (agent2_traced): [results] Cohen's kappa metric: 'We quantified the level of concordance of the 10 variation signs (1 for each pair of cell lines) for a given pair of datasets by means of the Cohen's kappa metric, which has been commonly used to'
- `ev_015` from `agent2_synthesis` (agent2_traced): [results] Benjamini-Hochberg FDR correction: 'we adjusted it with the Benjamini and Hochberg procedure to keep the False Discovery Rate (FDR) below 5%'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] Exact formula and implementation details for Mann-Whitney U test p-value threshold and log₂ fold-change threshold (20%) application to determine directional signs for FFD variations across pairwise cell-line comparisons: 'At first instance, a positive sign was registered if the distribution of samples values of the first member of the comparison was statistically higher (according to the statistical tests described'
- `ev_017` from `agent2_synthesis` (agent2_traced): [other] Specific file names and internal structure of the Zenodo 10.5281/zenodo.5824504 deposit containing RAS and RPS datasets, and whether they are pre-computed or require derivation from raw RNA-seq and metabolomics files: 'available in Zenodo under permanent identifier 10.5281/zenodo.5824504'
- `ev_018` from `agent2_synthesis` (agent2_traced): [other] Detailed filtering and data preprocessing steps applied to raw metabolomics data (from MetaboLights MTBLS3597) prior to RPS computation, including normalization, missing value handling, and quality control thresholds: 'raw data are deposited at www.ebi.ac.uk/metabolights/MTBLS3597. Normalized data (on protein μg) used for computational analyses are reported in S1 File.'
- `ev_019` from `agent2_synthesis` (agent2_traced): [other] Rationale and justification for using Cohen's kappa (a discrete/categorical agreement metric) rather than a continuous concordance measure (e.g., Spearman or Pearson correlation) given that RAS and RPS are continuous-valued scores before sign discretization: 'We quantified the level of concordance of the 10 variation signs (1 for each pair of cell lines) for a given pair of datasets by means of the Cohen's kappa metric, which has been commonly used to'
- `ev_020` from `agent2_synthesis` (agent2_traced): [other] Explicit documentation of how the 81-reaction subset with 'full substrate abundances available' was determined, including what constitutes 'full coverage' and how reactions with missing or below-detection-limit metabolites are handled: 'If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset.'

## Evaluation Strategy
### Direct Checks
- verify file 10.5281/zenodo.5824504 is accessible and contains RAS and RPS datasets
- verify RAS dataset file exists and contains reaction scores for all five cell lines (MCF102A, SKBR3, MCF7, MDAMB231, MDAMB361)
- verify RPS dataset file exists and contains reaction propensity scores for all five cell lines
- verify metabolomics coverage metadata file identifies exactly 81 reactions with full substrate abundance quantification
- verify that input datasets contain directional change annotations (up/down/no-change) for pairwise comparisons across five cell lines
- script_runs: Cohen's kappa computation script completes without error on RAS and RPS input matrices
- output_matches_reference: Cohen's kappa concordance values for RASvsRPS comparisons match reported values in Fig 4A (robust to rounding to 2 decimal places)
- output_matches_reference: number of reactions with RPSvsRAS concordance score ≥0.2 equals 44 as reported in text
- output_matches_reference: number of reactions with RPSvsFFD concordance score ≥0.2 equals 13 as reported in text
- verify that reactions without GPR associations are correctly excluded from RASvsRPS concordance analysis
- verify that reactions missing any substrate metabolomics measurement are excluded from the 81-reaction subset

### Expert Review
- Cohen's kappa concordance calculation follows standard definition: (observed agreement − expected agreement by chance) / (1 − expected agreement by chance)
- interpretation of Cohen's kappa thresholds (poor <0.2, fair 0.21–0.40, moderate 0.41–0.60, good 0.61–0.80, very good 0.81–1.0) aligns with cited references [51]
- directionality of sign changes (up=+1, down=−1, no-change=0) is correctly determined from Mann-Whitney U test (p<0.05) and log₂ fold-change threshold (≥20% or ≤−20%) as specified in Material and methods
- statistical tests (Mann-Whitney U for FFD, t-test for RPS) are applied correctly to compare distributions across pairwise cell-line comparisons
- any discrepancies between reproduced and reported kappa values are investigated for potential causes: sampling variability in FFD (10 batches of 100k solutions), RPS sensitivity to kinetic assumptions, or threshold parameter choices

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load RAS vectors (derived from RNA-seq and GPR rules) and RPS vectors (derived from LC-MS metabolomics and stoichiometry) for five cell lines from the Zenodo deposit.
2. For each of 10 pairwise cell-line comparisons and each reaction, perform Mann-Whitney U test to assign directional change sign (+1 up, −1 down, 0 no-change) to RAS, RPS, and FFD distributions.
3. Filter to 81 reactions with complete substrate metabolomics coverage, excluding reactions missing any substrate quantification.
4. Compute Cohen's kappa agreement between RAS and RPS directional signs for each reaction, accounting for chance agreement.
5. Compute Cohen's kappa agreement between RPS and FFD directional signs (RPSvsFFD) and between RAS and FFD signs (RASvsFFD) for each reaction.
6. Assign empirical p-values by permuting RPS variation signs 1000 times and comparing the distribution of kappa values to the original; apply Benjamini-Hochberg FDR correction (threshold α = 0.05).
7. Validation: verify that reactions flagged as statistically significant (post-FDR) match the subset identified in the published paper (ACONT, ASPTA, RPI, RPE) and that the empirical agreement distribution significantly exceeds the Q–Q quantile distribution of two independent random datasets.
8. References: source article (DOI: 10.1371/journal.pcbi.1009337); MTBLS3597 (https://www.ebi.ac.uk/metabolights/MTBLS3597); PRJNA767228 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228)

## Workflow Ports

**Inputs:**

- `ras_matrix` — RAS (Reaction Activity Score) matrix for five cell lines ← `task_001/tsne_plot`
- `rps_matrix` — RPS (Reaction Propensity Score) matrix for five cell lines
- `ffd_samples` — FFD (Feasible Flux Distribution) sample collections for five cell lines
- `reaction_metadata` — Reaction metadata with GPR associations and substrate coverage flags

**Outputs:**

- `kappa_table` — Cohen's kappa concordance scores for all 81 reactions
- `scatter_plot` — Scatter plot of RPSvsFFD vs. RPSvsRAS kappa concordance
- `heatmap` — Heatmap of kappa values for reactions with concordance > 0.2
- `pvalue_table` — Empirical and adjusted p-values for kappa concordance

**Used:** `urn:asb:port:task_001/tsne_plot`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
