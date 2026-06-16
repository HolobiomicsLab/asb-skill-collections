# SciTask Card: Reproduce growth yield correlation improvement attributable to Type 3 (transcriptomics-derived) constraints

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:26:15.469347+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_integrate`
- Domain: `bioinformatics`
- Subtask categories: `data-analysis`, `statistical-analysis`, `simulation`
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
Does integration of transcriptomics-derived constraints alone improve the correlation between predicted and experimental growth yield compared to constraints on nutrient availability alone, and how does adding metabolomics-derived extracellular flux constraints further affect this correlation?

## Connected Finding
Transcriptomics-derived constraints alone (Type 3) result in good separation of feasible flux distributions and better discrimination of growth rates across five cell lines, with further improvement when extracellular flux constraints (Type 1+2) are simultaneously applied.

## Task Description
Compute Spearman correlation coefficients between experimental and in silico growth yield on glucose for the five breast cell lines under four constraint scenarios (Type 1 alone, Type 1+2, Type 1+2+3, and Type 3 alone), reproducing the reported finding that transcriptomics-derived constraints (Type 3) alone yield the best discrimination while Type 1+2+3 combined provides the highest correlation.

## Inputs
- Five cell-relative metabolic models in SBML format (ENGRO2) with Type 1, Type 2, and Type 3 constraints defined separately
- Experimental growth yield measurements (protein produced over 48h / glucose consumed over 48h) for five cell lines from Bradford assay and YSI bioanalyzer
- ENGRO2 metabolic network model with 494 reactions, 410 metabolites, and gene-protein-reaction associations

## Expected Outputs
- Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1 constraints alone
- Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1+2 constraints
- Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1+2+3 constraints
- Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 3 constraints alone
- Correlation plot with four scatter subplots (one per constraint scenario) showing experimental vs. in silico growth yield with ρ and p-value annotations

## Expected Output File

- `growth_yield_correlation_analysis.pdf`

## Landmark Outputs

- `type1_ffd_samples.csv`
- `type12_ffd_samples.csv`
- `type3_ffd_samples.csv`
- `type123_ffd_samples.csv`
- `experimental_growth_yields.csv`
- `predicted_growth_yields_all_scenarios.csv`

## Tools
- COBRApy (optGpSampler algorithm)
- Flux Variability Analysis (FVA)
- constraint-based stoichiometric metabolic models

## Skills
- growth-yield-computation-from-omics
- constraint-based-model-sampling-and-flux-prediction
- correlation-analysis-between-experimental-computational-data
- metabolic-model-constraint-integration-and-comparison
- spearman-rank-correlation-statistical-testing

## Workflow Description
1. Load the five cell-relative constraint-based metabolic models (ENGRO2 with Type 1, Type 2, and Type 3 constraints applied separately and in combination) from the Zenodo deposit (10.5281/zenodo.5824504). 2. For each of the four constraint scenarios, uniformly sample the feasible flux region of each model using optGpSampler with 10 batches of 100,000 samples each (1 million total steady-state solutions per model per scenario), retaining the growth yield constraint (Eq. 6: 0.001 · 0.131972 · v_Biomass ≤ max · v_ExGlc · mw_Glc ≤ 0.001). 3. Compute the median protein synthesis flux divided by median glucose uptake flux (in silico growth yield) for each cell line under each scenario, converting flux ratio to grams/hour using the biomass protein fraction (0.131972). 4. Load experimental growth yield data (protein produced over 48h / glucose consumed over 48h, in grams/hour from Bradford assay and YSI analysis in S1 File). 5. Calculate Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico growth yield for each constraint scenario. 6. Generate a correlation plot (matching Fig 3E) with Spearman ρ and p-value annotations for all four scenarios, highlighting that Type 3 constraints alone best separate the five cell lines while Type 1+2+3 yields the highest overall correlation.

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
- Number of sampled Feasible Flux Distribution (FFD) solutions per cell line and constraint scenario used to compute correlation with experimental growth yield in Fig 3
- Exact statistical test employed to determine whether correlation differences between constraint scenarios (Fig 3E, comparing Type 1, Type 1+2, Type 3, Type 1+2+3) are statistically significant
- Whether experimental growth yield values (S1 File) represent mean and standard deviation across biological and technical replicates, or individual replicate measurements

## Domain Knowledge
- Growth yield is computed as the ratio of total biomass (protein) synthesized over the time period to total substrate (glucose) consumed, normalized by the molecular weight of glucose and the protein fraction of biomass (0.131972 in ENGRO2).
- Type 1 constraints define nutrient availability based on medium composition; Type 2 constraints enforce metabolic flux ratios (lactate/glucose, glutamate/glutamine) from extracellular measurements; Type 3 constraints bound internal fluxes proportionally to Reaction Activity Scores derived from transcriptomics via gene-protein-reaction rules.
- Uniform flux sampling via optGpSampler with thinning=10 explores the null space of the stoichiometric matrix under steady-state mass balance; the median of sampled fluxes represents a robust central estimate less sensitive to outliers than mean.
- Spearman rank correlation is robust to non-linear monotonic relationships and is appropriate when sample size is small (n=5 cell lines) and normality cannot be assumed.
- The reported growth yield constraint (Eq. 6) enforces that predicted growth yield lies within the minimum (3.90762 × 10⁻⁵) and maximum (1.67998 × 10⁻⁴) observed experimentally, preventing unrealistic flux distributions.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Does integration of transcriptomics-derived constraints alone improve the correlation between predicted and experimental growth yield compared to constraints on nutrient availability alone, and how does adding metabolomics-derived extracellular flux constraints further affect this correlation?: 'However, predictions of growth rates improve when constraints on extracellular fluxes are also added.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] Transcriptomics-derived constraints alone (Type 3) result in good separation of feasible flux distributions and better discrimination of growth rates across five cell lines, with further improvement when extracellular flux constraints (Type 1+2) are simultaneously applied.: 'transcriptomics-derived constraints alone (Fig 3C) result in a good separation of the feasible flux regions of the five models. The combination of both kinds of constraints (Fig 3D) decreases the'
- `ev_003` from `agent2_synthesis` (agent2_traced): [results] Five cell-relative metabolic models in SBML format (ENGRO2) with Type 1, Type 2, and Type 3 constraints defined separately: 'The final five cell-relative metabolic models (SBML format) are included in S1 Compressed File Archive'
- `ev_004` from `agent2_synthesis` (agent2_traced): [results] Experimental growth yield measurements (protein produced over 48h / glucose consumed over 48h) for five cell lines from Bradford assay and YSI bioanalyzer: 'Experimental data (reported in S1 File) was computed for each of the two collected biological replicates as the ratio of the total proteins produced over 48 hours (grams/hour, determined by Bradford'
- `ev_005` from `agent2_synthesis` (agent2_traced): [results] ENGRO2 metabolic network model with 494 reactions, 410 metabolites, and gene-protein-reaction associations: 'The ENGRO2 core model consists of 494 reactions, 410 metabolites and 494 genes'
- `ev_006` from `agent2_synthesis` (agent2_traced): [results] Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1 constraints alone: 'The Spearman correlation coefficient and p-value are reported on top of each plot'
- `ev_007` from `agent2_synthesis` (agent2_traced): [results] Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1+2 constraints: 'The Spearman correlation coefficient and p-value are reported on top of each plot'
- `ev_008` from `agent2_synthesis` (agent2_traced): [results] Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1+2+3 constraints: 'The Spearman correlation coefficient and p-value are reported on top of each plot'
- `ev_009` from `agent2_synthesis` (agent2_traced): [results] Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 3 constraints alone: 'The Spearman correlation coefficient and p-value are reported on top of each plot'
- `ev_010` from `agent2_synthesis` (agent2_traced): [results] Correlation plot with four scatter subplots (one per constraint scenario) showing experimental vs. in silico growth yield with ρ and p-value annotations: 'Correlation between the experimental and in silico growth yield on glucose is reported for each of the four settings in panels A, B, C and D'
- `ev_011` from `agent2_synthesis` (agent2_traced): [results] COBRApy (optGpSampler algorithm): 'we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions of the ENGRO2 model'
- `ev_012` from `agent2_synthesis` (agent2_traced): [results] Flux Variability Analysis (FVA): 'We performed a Flux Variability Analysis (FVA). FVA [67, 68] is a constraint-based modelling technique aimed at determining the maximal (and minimal) possible flux through any reaction'
- `ev_013` from `agent2_synthesis` (agent2_traced): [abstract] constraint-based stoichiometric metabolic models: 'using constraint-based stoichiometric metabolic models as a scaffold'
- `ev_014` from `agent2_synthesis` (agent2_traced): [other] Number of sampled Feasible Flux Distribution (FFD) solutions per cell line and constraint scenario used to compute correlation with experimental growth yield in Fig 3: 'we sampled a million steady-state solutions of the ENGRO2 model in all the tested conditions. To get a large number of samples, we used the batch generator option of the algorithm, creating ten'
- `ev_015` from `agent2_synthesis` (agent2_traced): [other] Exact statistical test employed to determine whether correlation differences between constraint scenarios (Fig 3E, comparing Type 1, Type 1+2, Type 3, Type 1+2+3) are statistically significant: 'The Spearman correlation coefficient and p-value are reported on top of each plot.'
- `ev_016` from `agent2_synthesis` (agent2_traced): [other] Whether experimental growth yield values (S1 File) represent mean and standard deviation across biological and technical replicates, or individual replicate measurements: 'The experimental growth yield (reported in S1 File) was computed for each of the two collected biological replicates as the ratio of the total proteins produced over 48 hours'

## Evaluation Strategy
### Direct Checks
- file_exists: Verify S1 Compressed File Archive (cell-relative metabolic models in SBML format) is accessible in Zenodo deposit 10.5281/zenodo.5824504
- file_exists: Verify S1 File containing experimental growth yield data, extracellular flux measurements, and protein content for all five cell lines is available
- file_format_is: Verify FFD datasets (Feasible Flux Distributions) from ENGRO2 models are in format specified in Materials and Methods (sampled steady-state solutions)
- value_in_range: Spearman correlation coefficient reported in Fig 3E for constraint scenario C (transcriptomics-derived constraints alone, Type 3) is positive and exceeds correlation from Type 1+2 constraints alone
- value_in_range: Spearman correlation coefficient for all three constraints combined (Type 1+2+3, Fig 3D) shows improvement over Type 3 alone, but Fig 3 caption states Type 3 constraints alone 'result in a good separation of the feasible regions'
- script_runs: Code workflow from https://github.com/qLSLab/integrate executes without error when applied to deposited cell-relative models and experimental inputs
- output_matches_reference: Reconstructed growth yield predictions (median protein synthesis flux over glucose uptake) match values reported in S1 File for all five cell lines under Type 3 constraints, robust to parameter choices in FVA and sampling (thinning=10)

### Expert Review
- Assess whether the selection of 20% fold-change threshold for registering variation sign (Materials and Methods, Concordance analysis section) is justified and consistent with prior metabolic pathway sensitivity literature cited
- Evaluate whether constraint-based modeling assumptions (steady-state, pseudo-stoichiometric mass action kinetics without enzyme kinetic parameters) adequately justify the causal interpretation that Type 3 constraints capture transcriptional regulation independent of metabolic regulation
- Examine whether the reported improvement in growth yield correlation under Type 3 constraints versus Type 1 or Type 1+2 (Fig 3E) reflects genuine superior predictive power or confounding from degrees-of-freedom in flux sampling and constraint relaxation
- Review whether the experimental growth yield computation (protein synthesis flux / glucose uptake flux, based on Bradford assay and YSI analysis) adequately controls for non-protein biomass components and whether this affects the correlation baseline

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Load ENGRO2 models with Type 1, Type 2, and Type 3 constraints specified separately and in combination.
2. Sample 1 million steady-state flux distributions per cell line per constraint scenario using optGpSampler with thinning=10, enforcing growth yield bounds (Eq. 6: 0.001 · 0.131972 · v_Biomass ≤ max · v_ExGlc · mw_Glc ≤ 0.001).
3. Compute in silico growth yield as median(v_Biomass) / median(v_ExGlc) × 0.131972 for each scenario.
4. Extract experimental growth yield (total protein over 48h / total glucose over 48h) from Bradford and YSI measurements.
5. Calculate Spearman ρ and two-tailed p-value for experimental vs. in silico growth yield under each constraint scenario.
6. Validation: Confirm that Type 3 constraints alone achieve the highest separation of the five cell lines in t-SNE space (Fig 3C vs 3D) while Type 1+2+3 combined yields the highest Spearman correlation with experimental data.
7. References: source article (DOI: 10.1371/journal.pcbi.1009337); MTBLS3597 (https://www.ebi.ac.uk/metabolights/MTBLS3597); PRJNA767228 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228)

## Workflow Ports

**Inputs:**

- `cell_relative_models` — Five cell-relative ENGRO2 models with Type 1, 2, 3 constraints (SBML) ← `task_001/tsne_plot`
- `experimental_growth_yield` — Experimental growth yield (protein/glucose) for five cell lines
- `engro2_network` — ENGRO2 metabolic network (494 reactions, 410 metabolites, GPRs)

**Outputs:**

- `type1_correlation` — Spearman ρ and p-value for Type 1 constraints
- `type12_correlation` — Spearman ρ and p-value for Type 1+2 constraints
- `type123_correlation` — Spearman ρ and p-value for Type 1+2+3 constraints
- `type3_correlation` — Spearman ρ and p-value for Type 3 constraints alone
- `correlation_plot` — Four-panel correlation plot (experimental vs. in silico growth yield)

**Used:** `urn:asb:port:task_001/tsne_plot`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
