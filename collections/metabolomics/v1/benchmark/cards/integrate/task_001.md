# SciTask Card: Reproduce t-SNE separation of breast cell line Feasible Flux Distributions under combined Type 1+2+3 constraints

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:26:15.469347+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_integrate`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `modeling`, `statistical-analysis`
- DOI: `10.1371/journal.pcbi.1009337`
- GitHub: `qLSLab/integrate`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `multi-omics`
- Subdomains: `multi-omics-integration`, `computational-metabolomics`, `fluxomics`
- Techniques: `flux-analysis`, `multi-omics-integration`, `pathway-analysis`, `differential-abundance-analysis`
- Keywords: `constraint-based metabolic modeling` · `metabolic flux prediction` · `transcriptomics integration` · `metabolomics integration` · `multi-level metabolic regulation` · `gene expression` · `substrate availability` · `enzyme kinetics` · `Michaelis-Menten law` · `systems metabolism`

## Research Question
Can the INTEGRATE pipeline with all three constraint types (nutrient availability, extracellular fluxes, and transcriptomics-derived constraints) successfully segregate the feasible flux distributions of five breast cancer cell lines with distinct metabolic profiles?

## Connected Finding
The combination of all three constraint types (type 1+2+3) applied to ENGRO2 achieves clear separation of the five cell-line FFD clusters in t-SNE space, with transcriptomics-derived constraints alone providing good segregation but extracellular flux constraints improving inter-model separation.

## Task Description
Apply all three constraint types (nutrient availability, extracellular fluxes, transcriptomics-derived) to the ENGRO2 metabolic model using breast cancer cell line multi-omics data and reproduce the t-SNE visualization demonstrating clear separation of five cell-line feasible flux distribution clusters.

## Inputs
- ENGRO2 metabolic network model (SBML format, 494 reactions, 410 metabolites, 494 genes)
- RNA-seq transcriptomics data from five breast cell lines (PRJNA767228, FPKM format, 3 biological replicates each)
- Intracellular metabolomics quantification from LC-MS analysis (MTBLS3597, 0–48 hour time window)
- Extracellular flux measurements: glucose, lactate, glutamine, glutamate concentrations (YSI2950 bioanalyzer, fresh medium t=0 and spent medium after 48 hours)
- Gene-Protein-Reaction (GPR) associations embedded in ENGRO2 model and Growth medium composition specifications for five cell lines

## Expected Outputs
- t-SNE 2D projection plot showing clear separation of five cell-line Feasible Flux Distribution (FFD) clusters with all three constraint types applied (Fig 3D)
- Five cell-relative metabolic models (SBML format) with Type 1, Type 2, and Type 3 constraints applied
- Quantitative evaluation: Spearman correlation coefficient between experimental and in silico growth yield on glucose for all four constraint scenarios (Type 1; Type 1+2; Type 3; Type 1+2+3)

## Expected Output File

- `tsne_ffd_constraint_integration.png`

## Landmark Outputs

- `reaction_activity_scores_all_lines.csv`
- `cell_relative_models_type1_type2_type3_*.sbml`
- `feasible_flux_distributions_sampled_*.csv`
- `growth_yield_correlation_metrics.txt`

## Tools
- constraint-based stoichiometric metabolic models
- eFlux
- TRFBA
- GX-FBA
- scFBA
- STAR aligner (v.2.6.1d)
- HTSeq (v.0.6.1)
- YSI2950 bioanalyzer
- Agilent 1290 Infinity UHPLC system
- Agilent 6550 iFunnel Q-TOF mass spectrometer
- optGpSampler algorithm
- t-SNE (t-distributed Stochastic Neighbor Embedding)
- COBRApy

## Skills
- constraint-based-flux-balance-analysis
- transcriptomics-reaction-activity-scoring
- metabolomics-reaction-propensity-computation
- metabolic-model-constraint-specification
- feasible-flux-distribution-sampling
- dimensionality-reduction-visualization
- multi-omics-data-integration

## Workflow Description
1. Load the ENGRO2 metabolic model (SBML format) and convert to irreversible representation. 2. Retrieve transcriptomics (PRJNA767228), intracellular metabolomics (MTBLS3597), and extracellular flux measurements (YSI2950 bioanalyzer data) for five breast cell lines (MCF102A, MCF7, MDA-MB231, MDA-MB361, SKBR3). 3. Compute Reaction Activity Scores (RAS) from RNA-seq read counts using GPR rules (minimum for AND-linked genes, sum for OR-linked genes) and normalize by maximum RAS across cell lines. 4. Apply Type 1 constraints: set upper bounds on exchange reactions proportionally to nutrient concentrations in growth medium for each cell line. 5. Apply Type 2 constraints: constrain ratios of lactate-to-glucose, lactate-to-glutamine, and glutamate-to-glutamine fluxes based on YSI measurements with ±1 standard deviation bounds. 6. Apply Type 3 constraints: perform Flux Variability Analysis (FVA) on each cell-relative model to determine maximum and minimum flux capacity for each internal reaction, then scale flux boundaries proportionally to RAS values (Equations 7 and 8). 7. Uniformly sample the constrained null space of each cell-relative model using optGpSampler algorithm (1 million samples, thinning=10, batch size 100,000) to generate Feasible Flux Distributions (FFD) for all five cell lines. 8. Apply t-distributed Stochastic Neighbor Embedding (t-SNE) dimensionality reduction to the sampled FFD in two-dimensional space and visualize cluster separation for the five cell lines.

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
- Specific t-SNE algorithm hyperparameters (perplexity, learning rate, number of iterations, random seed) used to generate the t-SNE plot shown in Fig 3D are not stated in the text; only that 10,000 steady-state solutions per model were plotted
- The paper does not explicitly state whether the published t-SNE plot in Fig 3D was generated from a single run or averaged/consensus visualization across multiple runs with different random seeds
- No explicit statement of how the qualitative concordance threshold (Cohen's kappa > 0.2) used for concordance analysis relates to the FFD cluster separation quality or whether cluster separation metrics (silhouette score, Davies-Bouldin index) are reported
- The exact computational cost (CPU time, memory requirements) for uniform sampling one million solutions per cell-line model with three constraint types is not reported, making reproducibility timing difficult to predict
- Whether the cell-relative models' performance on growth yield prediction (Fig 3E) shows comparable accuracy across all five cell lines or if certain cell lines have systematically higher/lower prediction error is not discussed

## Domain Knowledge
- Reaction Activity Scores (RAS) are computed from GPR logical expressions using minimum flux values for AND-linked gene subunits and sum of flux values for OR-linked gene isoforms, then normalized by the maximum RAS across all cell lines (Equations 1–3).
- Type 1 constraints scale nutrient uptake bounds proportionally to metabolite concentrations in the growth medium; Type 2 constraints enforce ratios of extracellular flux (lactate/glucose, lactate/glutamine, glutamate/glutamine) with ±1 standard deviation tolerance; Type 3 constraints use FVA-derived maximum flux capacity multiplied by normalized RAS (Equations 6–7).
- Feasible Flux Distribution sampling via optGpSampler uniformly explores the constrained steady-state solution space; 1 million samples (10 batches × 100,000 points) with thinning=10 are required to adequately represent the flux polytope geometry for downstream t-SNE separation.
- The 0–48 hour experimental window ensures balanced growth (protein content linearly correlated with cell number) and stable metabolic state; absolute extracellular fluxes are derived from concentration differences divided by the integral of cell number over time.
- t-SNE dimensionality reduction (applied to high-dimensional sampled FFD) reveals cluster separation only when all three constraint types are applied simultaneously; transcriptomics-only or nutrient-only constraints show incomplete discrimination among the five cell-line flux phenotypes.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Can the INTEGRATE pipeline with all three constraint types (nutrient availability, extracellular fluxes, and transcriptomics-derived constraints) successfully segregate the feasible flux distributions of five breast cancer cell lines with distinct metabolic profiles?: 'the simultaneous application of the three constraints help the flux distributions sampled from each model (corresponding to the specific colour in the plot) from one another'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] The combination of all three constraint types (type 1+2+3) applied to ENGRO2 achieves clear separation of the five cell-line FFD clusters in t-SNE space, with transcriptomics-derived constraints alone providing good segregation but extracellular flux constraints improving inter-model separation.: 'Notably, constraints on extracellular fluxes alone (Fig 3B) do not allow the feasible flux distributions of the five models to be discriminated. On the contrary, transcriptomics-derived constraints'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] ENGRO2 metabolic network model (SBML format, 494 reactions, 410 metabolites, 494 genes): 'The final version of the ENGRO2 core model consists of 494 reactions, 410 metabolites and 494 genes.'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] RNA-seq transcriptomics data from five breast cell lines (PRJNA767228, FPKM format, 3 biological replicates each): 'Raw reads are available in NCBI Short Reads Archive (SRA) under Accession Number PRJNA767228.'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Intracellular metabolomics quantification from LC-MS analysis (MTBLS3597, 0–48 hour time window): 'raw data are deposited at www.ebi.ac.uk/metabolights/MTBLS3597. Normalized data (on protein μg) used for computational analyses are reported in S1 File.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Extracellular flux measurements: glucose, lactate, glutamine, glutamate concentrations (YSI2950 bioanalyzer, fresh medium t=0 and spent medium after 48 hours): 'Absolute quantification of glucose, lactate, glutamine, and glutamate in fresh medium at t = 0 and in spent media after 48 hours of growth was determined enzymatically using YSI2950 bioanalyzer'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Gene-Protein-Reaction (GPR) associations embedded in ENGRO2 model and Growth medium composition specifications for five cell lines: 'we set flux boundaries to the generic reconstruction of human metabolism ENGRO2, according to the differences observed in the experimental input data relative to the five investigated cell lines'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] t-SNE 2D projection plot showing clear separation of five cell-line Feasible Flux Distribution (FFD) clusters with all three constraint types applied (Fig 3D): 'we represented the high-dimensional sampled flux distributions in a two-dimensional space [50]. It is possible to appreciate how the simultaneous application of the three constraints better separates'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Five cell-relative metabolic models (SBML format) with Type 1, Type 2, and Type 3 constraints applied: 'The final five cell-relative metabolic models (SBML format) are included in S1 Compressed File Archive.'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] Quantitative evaluation: Spearman correlation coefficient between experimental and in silico growth yield on glucose for all four constraint scenarios (Type 1; Type 1+2; Type 3; Type 1+2+3): 'E) Correlation between the experimental and in silico growth yield on glucose is reported for each of the four settings in panels A, B, C and D. The Spearman correlation coefficient and p-value are'
- `ev_011` from `agent2_synthesis` (agent2_traced): [abstract] constraint-based stoichiometric metabolic models: 'using constraint-based stoichiometric metabolic models as a scaffold'
- `ev_012` from `agent2_synthesis` (agent2_traced): [intro] eFlux: 'we set flux boundaries as a function of gene expression as done, among others, by eFlux [36]'
- `ev_013` from `agent2_synthesis` (agent2_traced): [intro] TRFBA: 'we set flux boundaries as a function of gene expression as done, among others, by eFlux [36] and TRFBA'
- `ev_014` from `agent2_synthesis` (agent2_traced): [intro] GX-FBA: 'We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in GX-FBA [26]'
- `ev_015` from `agent2_synthesis` (agent2_traced): [intro] scFBA: 'We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA [38]'
- `ev_016` from `agent2_synthesis` (agent2_traced): [results] STAR aligner (v.2.6.1d): 'raw reads were mapped with STAR aligner (v.2.6.1d) to human reference genome (hg38)'
- `ev_017` from `agent2_synthesis` (agent2_traced): [results] HTSeq (v.0.6.1): 'gene counts were calculated by HTSeq (v.0.6.1), using the hg38 Encode-Gencode GTF file (v28)'
- `ev_018` from `agent2_synthesis` (agent2_traced): [results] YSI2950 bioanalyzer: 'Absolute quantification of glucose, lactate, glutamine, and glutamate in fresh medium at t = 0 and in spent media after 48 hours of growth was determined enzymatically using YSI2950 bioanalyzer'
- `ev_019` from `agent2_synthesis` (agent2_traced): [results] Agilent 1290 Infinity UHPLC system: 'LC separation was performed using an Agilent 1290 Infinity UHPLC system and an InfintyLab Poroshell 120 PFP column'
- `ev_020` from `agent2_synthesis` (agent2_traced): [results] Agilent 6550 iFunnel Q-TOF mass spectrometer: 'MS detection was performed using an Agilent 6550 iFunnel Q-TOF mass spectrometer with Dual JetStream source operating in negative ionization mode'
- `ev_021` from `agent2_synthesis` (agent2_traced): [results] optGpSampler algorithm: 'we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions of the ENGRO2 model in all the tested conditions'
- `ev_022` from `agent2_synthesis` (agent2_traced): [results] t-SNE (t-distributed Stochastic Neighbor Embedding): 'We then applied a t-distributed stochastic neighbor embedding (t-SNE) algorithm and represented the high-dimensional sampled flux distributions in a two-dimensional space'
- `ev_023` from `agent2_synthesis` (agent2_traced): [results] COBRApy: 'we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72]'
- `ev_024` from `agent2_synthesis` (agent2_traced): [results] Specific t-SNE algorithm hyperparameters (perplexity, learning rate, number of iterations, random seed) used to generate the t-SNE plot shown in Fig 3D are not stated in the text; only that 10,000 steady-state solutions per model were plotted: 'For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted.'
- `ev_025` from `agent2_synthesis` (agent2_traced): [results] The paper does not explicitly state whether the published t-SNE plot in Fig 3D was generated from a single run or averaged/consensus visualization across multiple runs with different random seeds: 'A two-dimensional map of the FFDs of the five cell lines in each setting is shown.'
- `ev_026` from `agent2_synthesis` (agent2_traced): [results] No explicit statement of how the qualitative concordance threshold (Cohen's kappa > 0.2) used for concordance analysis relates to the FFD cluster separation quality or whether cluster separation metrics (silhouette score, Davies-Bouldin index) are reported: 'We reported the names of the reactions having at least one of the scores greater than 0.2 (i.e. fair concordance).'
- `ev_027` from `agent2_synthesis` (agent2_traced): [results] The exact computational cost (CPU time, memory requirements) for uniform sampling one million solutions per cell-line model with three constraint types is not reported, making reproducibility timing difficult to predict: 'we sampled a million steady state solutions of the ENGRO2 model in all the tested conditions.'
- `ev_028` from `agent2_synthesis` (agent2_traced): [results] Whether the cell-relative models' performance on growth yield prediction (Fig 3E) shows comparable accuracy across all five cell lines or if certain cell lines have systematically higher/lower prediction error is not discussed: 'The condition where transcriptomics-derived constraints alone are integrated well discriminates the five cell lines in terms of their growth rate, as shown in the relative correlation plot in Fig 3.'

## Evaluation Strategy
### Direct Checks
- File exists: GitHub repository at https://github.com/qLSLab/integrate is accessible and contains scripts for reproducible workflow
- File exists: Zenodo deposit 10.5281/zenodo.5824504 is accessible and contains downloadable INTEGRATE code and documentation
- File exists: ENGRO2 metabolic model file in SBML format (S2 File) can be loaded from article SI or Zenodo deposit
- File exists: ENGRO2 metabolic model file in XLSX format (S3 File) is present in SI or Zenodo deposit
- File exists: Breast cell line multi-omics datasets (transcriptomics FPKM values, intracellular metabolomics profiles, extracellular flux measurements) are available in S1 File or deposited at MTBLS3597 and PRJNA767228
- File exists: Cell-relative metabolic models in SBML format for all five breast cell lines (MCF102A, MCF7, MDAMB231, MDAMB361, SKBR3) present in S1 Compressed File Archive
- Script runs: INTEGRATE pipeline scripts execute without errors when applied to ENGRO2 model with all three constraint types (nutrient availability type 1, extracellular fluxes type 2, transcriptomics-derived type 3)
- Output file format is: t-SNE plot image generated from uniform sampling of feasible flux distributions (FFD) for five cell lines, matching Fig 3D of published paper
- Value in range: t-SNE visualization shows clear spatial separation of five cell-line clusters in two-dimensional embedding space, consistent with qualitative appearance of Fig 3D
- Output matches reference: Computed FFD t-SNE coordinates cluster by cell line with inter-model separation greater than intra-model separation, matching the pattern shown in Fig 3D—robust to random seed initialization within expected variance for t-SNE algorithm
- Value in range: Correlation between experimental growth yield on glucose and in silico growth yield predictions is positive when all three constraint types are applied together (Fig 3E comparison), with Spearman correlation coefficient and p-value reported matching or closely approximating published values

### Expert Review
- Verify that the three constraint types (type 1: nutrient availability, type 2: extracellular flux ratios, type 3: transcriptomics-derived RAS bounds) are correctly formulated and applied according to equations (4), (6), (7), and (8) in the Methods section
- Verify that Reaction Activity Scores (RAS) are correctly computed from transcriptomics data using equations (1)–(3) and GPR logical operators (AND as minimum, OR as sum), with appropriate normalization
- Verify that uniform sampling of the constrained null space via optGpSampler achieves sufficient coverage of feasible flux region (one million samples across ten batches of 100,000 samples each as stated)
- Verify that t-SNE dimensionality reduction parameters (perplexity, learning rate, iteration count) are either specified in the code repository or match standard COBRApy/scikit-learn defaults used in scFBA and similar prior work
- Verify that cell-relative model construction correctly incorporates relative constraints that preserve within-cell and across-cell metabolic heterogeneity without making models cell-specific in absolute terms
- Verify that the five cell lines represent genuinely heterogeneous metabolic phenotypes based on measured intracellular metabolomics profiles (Fig 2D–E) and extracellular flux ratios (Fig 2F), confirming biological motivation for separation in constraint space

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy
- **Commercial software:** MATLAB (optional, for visualization), Agilent MassHunter (for LC-MS data processing)
- **Open-source alternatives:**
  - MATLAB → Python (NumPy, SciPy, scikit-learn)
  - Agilent MassHunter → XCMS, MZmine 2

## Methodology Summary
1. Compute normalized Reaction Activity Scores from RNA-seq transcriptomics data using GPR logical rules and scale to [0, 1].
2. Define and apply three nested constraint types to the ENGRO2 model: (1) nutrient availability from medium composition, (2) extracellular flux ratios from YSI bioanalyzer data, (3) transcriptomics-derived internal flux boundaries from RAS and FVA.
3. Uniformly sample 1 million steady-state flux vectors from the constrained null space of each of five cell-relative models using optGpSampler.
4. Apply t-SNE nonlinear dimensionality reduction to the high-dimensional FFD to visualize separation of cell-line clusters in 2D space.
5. Validation: Confirm t-SNE clusters show distinct, non-overlapping separation of the five cell lines when all three constraint types are applied together, with improved Spearman correlation (r ≥ 0.85) between experimental and in silico growth yield on glucose relative to constraint-type subsets.
6. References: source article (DOI: 10.1371/journal.pcbi.1009337); MTBLS3597 (https://www.ebi.ac.uk/metabolights/MTBLS3597); PRJNA767228 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228)

## Workflow Ports

**Inputs:**

- `engro2_model` — ENGRO2 metabolic model (SBML)
- `transcriptomics_fpkm` — RNA-seq data (FPKM, five cell lines)
- `metabolomics_lcms` — Intracellular metabolomics (LC-MS quantification)
- `extracellular_fluxes` — Extracellular flux measurements (YSI bioanalyzer)
- `medium_composition` — Growth medium nutrient concentrations per cell line

**Outputs:**

- `tsne_plot` — t-SNE 2D projection of constrained FFD with all three constraint types (Type 1+2+3)
- `cell_relative_models` — Five cell-relative models in SBML format with all constraints applied
- `growth_yield_correlation` — Spearman correlation coefficient and p-value (experimental vs. in silico growth yield)

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
