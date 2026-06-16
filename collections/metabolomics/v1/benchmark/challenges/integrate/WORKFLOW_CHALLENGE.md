# Workflow Challenge: `coll_integrate_workflow`


> INTEGRATE is a computational pipeline that integrates transcriptomics and intracellular metabolomics data with constraint-based metabolic modeling to uncover whether metabolic flux variations across cell lines are governed by transcriptional regulation, substrate availability, or both.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Metabolism is regulated through multiple hierarchical layers: gene expression controls enzyme abundance, while metabolite concentrations modulate enzymatic activity through substrate availability and allosteric effects. The paper presents INTEGRATE, a model-based framework that combines transcriptomics-derived Reaction Activity Scores (RAS), intracellular metabolomics-derived Reaction Propensity Scores (RPS) computed via mass action kinetics, and constraint-based steady-state metabolic modeling to characterize which regulatory layer controls each metabolic reaction. Applied to five breast cell lines (one non-tumorigenic and four cancer-derived), the authors generated transcriptomics and metabolomics datasets and integrated them into a manually curated constraint-based model of human central carbon metabolism (ENGRO2). By assessing concordance between RAS and flux variations, and between RPS and flux variations using Cohen's kappa, INTEGRATE classified reactions as controlled by transcriptional regulation, metabolic regulation only, or combined control. Constraint integration on nutrient availability (Type 1), extracellular flux ratios (Type 2), and transcriptomics-derived flux bounds (Type 3) progressively improved segregation of cell-line-specific feasible flux distributions and growth yield predictions, with Type 3 constraints alone achieving good cell-line discrimination. Among 81 reactions with complete substrate abundance data, concordance analysis identified distinct regulatory signatures across the five cell lines, providing a framework for identifying metabolic intervention points in personalized therapeutic strategies for multifactorial diseases.

## Research questions

- Can the INTEGRATE pipeline with all three constraint types (nutrient availability, extracellular fluxes, and transcriptomics-derived constraints) successfully segregate the feasible flux distributions of five breast cancer cell lines with distinct metabolic profiles?
- What are the Cohen's kappa concordance values between RAS and RPS directional changes for metabolic reactions with complete substrate metabolomics coverage across the five breast cell lines?
- Does integration of transcriptomics-derived constraints alone improve the correlation between predicted and experimental growth yield compared to constraints on nutrient availability alone, and how does adding metabolomics-derived extracellular flux constraints further affect this correlation?
- How does the mass action law formulation translate intracellular metabolomics data into Reaction Propensity Scores (RPS) that quantify the expected relative metabolic flux changes across cell lines based purely on substrate availability differences?
- How can RAS, RPS, and FFD datasets be intersected to classify each metabolic reaction into regulatory categories (transcriptional, metabolic, combined, or unclassified)?

## Methods overview

Compute normalized Reaction Activity Scores from RNA-seq transcriptomics data using GPR logical rules and scale to [0, 1]. Define and apply three nested constraint types to the ENGRO2 model: (1) nutrient availability from medium composition, (2) extracellular flux ratios from YSI bioanalyzer data, (3) transcriptomics-derived internal flux boundaries from RAS and FVA. Uniformly sample 1 million steady-state flux vectors from the constrained null space of each of five cell-relative models using optGpSampler. Apply t-SNE nonlinear dimensionality reduction to the high-dimensional FFD to visualize separation of cell-line clusters in 2D space. Validation: Confirm t-SNE clusters show distinct, non-overlapping separation of the five cell lines when all three constraint types are applied together, with improved Spearman correlation (r ≥ 0.85) between experimental and in silico growth yield on glucose relative to constraint-type subsets. References: source article (DOI: 10.1371/journal.pcbi.1009337); MTBLS3597 (https://www.ebi.ac.uk/metabolights/MTBLS3597); PRJNA767228 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228) Load RAS vectors (derived from RNA-seq and GPR rules) and RPS vectors (derived from LC-MS metabolomics and stoichiometry) for five cell lines from the Zenodo deposit. For each of 10 pairwise cell-line comparisons and each reaction, perform Mann-Whitney U test to assign directional change sign (+1 up, −1 down, 0 no-change) to RAS, RPS, and FFD distributions. Filter to 81 reactions with complete substrate metabolomics coverage, excluding reactions missing any substrate quantification. Compute Cohen's kappa agreement between RAS and RPS directional signs for each reaction, accounting for chance agreement. Compute Cohen's kappa agreement between RPS and FFD directional signs (RPSvsFFD) and between RAS and FFD signs (RASvsFFD) for each reaction. Assign empirical p-values by permuting RPS variation signs 1000 times and comparing the distribution of kappa values to the original; apply Benjamini-Hochberg FDR correction (threshold α = 0.05). Validation: verify that reactions flagged as statistically significant (post-FDR) match the subset identified in the published paper (ACONT, ASPTA, RPI, RPE) and that the empirical agreement distribution significantly exceeds the Q–Q quantile distribution of two independent random datasets. References: source article (DOI: 10.1371/journal.pcbi.1009337); MTBLS3597 (https://www.ebi.ac.uk/metabolights/MTBLS3597); PRJNA767228 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228) Load ENGRO2 models with Type 1, Type 2, and Type 3 constraints specified separately and in combination. Sample 1 million steady-state flux distributions per cell line per constraint scenario using optGpSampler with thinning=10, enforcing growth yield bounds (Eq. 6: 0.001 · 0.131972 · v_Biomass ≤ max · v_ExGlc · mw_Glc ≤ 0.001). Compute in silico growth yield as median(v_Biomass) / median(v_ExGlc) × 0.131972 for each scenario. Extract experimental growth yield (total protein over 48h / total glucose over 48h) from Bradford and YSI measurements. Calculate Spearman ρ and two-tailed p-value for experimental vs. in silico growth yield under each constraint scenario. Validation: Confirm that Type 3 constraints alone achieve the highest separation of the five cell lines in t-SNE space (Fig 3C vs 3D) while Type 1+2+3 combined yields the highest Spearman correlation with experimental data. References: source article (DOI: 10.1371/journal.pcbi.1009337); MTBLS3597 (https://www.ebi.ac.uk/metabolights/MTBLS3597); PRJNA767228 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228) Load intracellular metabolomics data and ENGRO2 stoichiometric model with reaction-metabolite associations. For each reaction and cell line, retrieve all substrate metabolite concentrations from the model stoichiometry. Omit reactions with any missing substrate abundance measurements from the metabolomics dataset. Compute Reaction Propensity Score for each eligible reaction in each cell line using mass action law: RPS = product of [substrate_i]^(stoichiometric_coeff_i). Aggregate RPS across biological replicates within each cell line using median or mean. Normalize RPS within each reaction across cell lines by dividing by the maximum RPS value for that reaction. Validation: verify that RPS dataset contains no reactions with missing substrate abundances, that all values are non-negative, and that normalization produces scores in the range [0, 1] for each reaction. References: source article (DOI: 10.1371/journal.pcbi.1009337); MTBLS3597 (https://www.ebi.ac.uk/metabolights/MTBLS3597); PRJNA767228 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228) Load pre-computed RAS, RPS, and FFD datasets from deposited repositories for all reactions and pairwise cell-line comparisons. Compute signed fold-change directions (up/down/no-change) for each reaction across 10 pairwise cell-line comparisons using statistical tests (Mann–Whitney U for FFD, t-test for RAS/RPS) with p<0.05 and ≥20% fold-change threshold. Calculate two Cohen's kappa coefficients per reaction quantifying concordance between RAS-vs-FFD and RPS-vs-RAS fold-change sign patterns. Classify reactions into regulatory categories based on quadrant assignment: positive RASvsFFD + positive RPSvsRAS = combined; positive RPSvsFFD + negative RPSvsRAS = metabolic-only; negative both + high RASvsFFD = transcriptional-only; other = unclassified. Compute empirical p-values by repeated random sampling (1000 iterations) of RPS variation distributions and derive FDR-adjusted p-values using Benjamini–Hochberg procedure with target FDR <5%. Validation: reactions ACONT, ASPTA, RPI, and RPE show statistically significant concordance (FDR<5%) in both core and genome-wide models, confirming robustness of classification scheme. References: source article (DOI: 10.1371/journal.pcbi.1009337); MTBLS3597 (https://www.ebi.ac.uk/metabolights/MTBLS3597); PRJNA767228 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228)

**Domain:** multi-omics

**Techniques:** flux-analysis, multi-omics-integration, pathway-analysis, differential-abundance-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Metabolism is directly and indirectly fine-tuned by a complex web of interacting regulatory mechanisms that fall into two major classes.
- **(finding)** The expression level of metabolic enzymes sets the maximal theoretical flux level for each enzyme-controlled reaction.
- **(finding)** Metabolic regulation controls the interactions of metabolites with enzymes, including substrates, cofactors, and allosteric modulators.
- **(finding)** High-throughput omics data analyzed separately do not accurately characterize the hierarchical regulation of metabolism.
- **(finding)** INTEGRATE computes differential reaction expression from transcriptomics data using constraint-based modeling to predict if differential enzyme expression originates differences in metabolic fluxes. _[grounded: INTEGRATE_system]_
- **(finding)** INTEGRATE uses metabolomics to predict how differences in substrate availability translate into differences in metabolic fluxes. _[grounded: INTEGRATE_system]_
- **(finding)** INTEGRATE discriminates fluxes regulated at the metabolic and/or gene expression level by intersecting output datasets from transcriptomics and metabolomics analysis. _[grounded: INTEGRATE_system]_
- **(finding)** The pipeline was demonstrated on a set of immortalized normal and cancer breast cell lines.
- **(finding)** Each metabolic flux depends on at least two intertwined regulatory layers: one regulating the flux of each enzyme-catalyzed metabolic reaction, and another through auto-regulation via metabolite interactions.
- **(finding)** The upper level flux for each enzyme-catalyzed metabolic reaction depends on the levels and catalytic activities of metabolic enzymes, which are set by complex mechanisms orchestrated by signal transduction pathways.
- **(finding)** Regulatory mechanisms of metabolic enzyme expression include epigenetic control of chromatin, transcription factors, transcription rate, and post-transcriptional/post-translational events.
- **(finding)** Auto-regulation of metabolism occurs through the interactions of metabolites (substrates, cofactors, allosteric modulators) with responsible enzymes.
- **(finding)** The flux of an enzyme-catalyzed reaction depends on the concentration of its substrate(s).
- **(finding)** The Michaelis-Menten law approximates the dependence of reaction rate on substrate concentration for non-allosteric enzymes.
- **(finding)** The Michaelis constant K_m describes the substrate concentration at which the reaction rate is equal to V_max/2.
- **(finding)** At substrate concentrations below K_m, there is a linear increase in reaction rate with increasing substrate concentration.
- **(finding)** Metabolites within the same pathway or belonging to related biochemical pathways can fine-tune enzyme-catalyzed reactions through allosteric effects.
- **(finding)** Differences in metabolic fluxes are only partially determined by variations in protein/gene expression.
- **(finding)** In transcriptional control scenario, variations in flux through a metabolic reaction are mainly determined by variations in enzyme abundance when substrate is in large excess.
- **(finding)** In metabolic control scenario, variations in flux are mainly determined by variations in substrate abundance when enzyme is in large excess.
- **(finding)** Combined metabolic and transcriptional control occurs when variations in fluxes are determined by concerted variations in both substrate and enzyme abundance.
- **(finding)** Direct determination of metabolic fluxes through labeled substrates lags behind other omics technologies, mainly due to technical difficulties at the sub-cellular level.
- **(finding)** Integration of transcriptomics with metabolomics datasets has been limited mainly to gene-metabolite correlation analysis or pathway enrichment analysis.
- **(finding)** Constraint-based steady-state models represent a valuable framework to predict metabolic fluxes from high-throughput omics data.
- **(finding)** Methods using cross-sectional metabolomics data to predict fluxes require a priori assumptions on the relationship between metabolites and fluxes.
- **(finding)** INTEGRATE's novel hypothesis is that evidence for a monotonic relationship between fluxes and substrate abundances, and for a concurrent non-monotonic relationship between flux variation and enzyme abundance, indicates that a reaction is controlled metabolically. _[grounded: INTEGRATE_system]_
- **(finding)** Current model-based approaches to discern transcriptionally from metabolically controlled fluxes have limitations in directly using metabolomics data.
- **(finding)** INTEGRATE takes as input a metabolic network model with Gene-Protein-Reaction associations, transcriptomics data, intracellular metabolomics data, and extracellular flux data. _[grounded: INTEGRATE_system]_
- **(finding)** INTEGRATE returns two lists of metabolic fluxes: fluxes that vary across cells consistently with both metabolic and transcriptional regulation, and fluxes that vary consistently with metabolic regulation only. _[grounded: INTEGRATE_system]_
- **(finding)** INTEGRATE generates three comparable datasets centered around the object reaction: Reaction Activity Scores, Feasible Flux Distributions, and Reaction Propensity Scores. _[grounded: INTEGRATE_system]_
- **(finding)** Reaction Activity Score (RAS) is computed for each input model reaction based on the expression value and relationship among genes encoding catalyzing enzymes. _[grounded: RAS_component]_
- **(finding)** Feasible Flux Distributions (FFD) dataset includes a large number of flux distributions obtained by uniformly sampling the feasible flux region of the metabolic model. _[grounded: FFD_component]_
- **(finding)** Reaction Propensity Score (RPS) is computed based on the availability of reaction substrates, calculated as the product of substrate concentrations with each raised to a power equal to its stoichiometric coefficient. _[grounded: RPS_component]_
- **(finding)** Five breast cell lines were selected for study: one non-tumorigenic and four breast cancer cell lines with different molecular classifications.
- **(finding)** Cell lines present significant differences in terms of metabolic profile.
- **(finding)** The ratio of lactate produced over glucose consumed is quite similar across the five cell lines.
- **(finding)** Lactate and glutamate over glutamine ratios are more heterogeneous across the five cell lines compared to lactate/glucose ratio.
- **(finding)** ENGRO2 core model consists of 494 reactions, 410 metabolites, and 494 genes. _[grounded: ENGRO2_model]_
- **(finding)** ENGRO1 model consisted of 84 reactions, 67 metabolites, and 216 genes in comparison to ENGRO2. _[grounded: ENGRO2_model]_
- **(finding)** Transcriptomics-derived constraints alone well discriminate the five cell line models.
- **(finding)** Combination of transcriptomics-derived and extracellular flux constraints improves separation of feasible solutions between cell lines.
- **(finding)** Growth rate predictions improve when transcriptomics-derived constraints are combined with extracellular flux constraints.
- **(finding)** 44 reactions resulted from consistent transcriptional and metabolic regulation.
- **(finding)** 13 reactions resulted only metabolically regulated because of positive RPSvsFFD score above 0.2 and negative RPSvsRAS score below threshold.
- **(finding)** Cohen's kappa values are considered to indicate fair concordance between 0.21 and 0.40. _[grounded: cohens_kappa_tool]_
- **(finding)** After FDR correction of p-values, concordance between RPSs and FFDs resulted statistically significant for 4 reactions.
- **(finding)** ACONT reaction catalyzes the production of cytosolic isocitrate from citrate and is metabolically controlled.
- **(finding)** RPI reaction catalyzes the conversion of ribulose 5-phosphate to ribose 5-phosphate within the non-oxidative phase of the pentose phosphate pathway.
- **(finding)** Concordance scores are robust to the choice of sample, with standard deviation of Cohen's kappa values across batches being negligible for most reactions. _[grounded: cohens_kappa_tool]_
- **(finding)** Some flux variations show concordance between independent datasets beyond reasonable doubt according to empirical probability analysis.
- **(finding)** INTEGRATE integration of transcriptomics and metabolomics data enriches their expressive power by providing complementary views of metabolic state. _[grounded: INTEGRATE_system]_
- **(finding)** Metabolic fluxes predicted by constraint-based modeling complement information on differential activity of reactions derived from gene expression data.
- **(finding)** INTEGRATE indicated that aconitase (ACONT) metabolic regulation involves the cytosolic reaction while the aconitase flux itself is not regulated at transcriptional level. _[grounded: INTEGRATE_system]_
- **(finding)** INTEGRATE does not have the ambition to predict exact flux values, but rather the sign of variation across cell lines. _[grounded: INTEGRATE_system]_
- **(finding)** The main novelty of INTEGRATE is the direct exploitation of metabolomics data to determine whether a flux is regulated at the metabolic level. _[grounded: INTEGRATE_system]_
- **(finding)** Knowing whether a flux is controlled at the metabolic or enzymatic level is mandatory in designing therapeutic strategies and identifying metabolic reactions that indirectly affect target reactions.

**Speculative claims (excluded from scoring):**
- **(finding)** Knowing the regulatory level at which a given metabolic reaction is controlled will be valuable to inform targeted, truly personalized therapies in cancer patients.
- **(finding)** INTEGRATE can be applied to different fields where metabolism plays a driving role, including cancer and neurodegeneration. _[grounded: INTEGRATE_system]_
- **(finding)** The pipeline can be extended to integrate proteomics and phosphoproteomics data alongside transcriptomics-derived RAS. _[grounded: INTEGRATE_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- iReMet, Pandey et al., Katzir et al., and Cakir et al. are alternative approaches to integrate metabolomics and transcriptomics data
- Any available method can be used in principle to set flux boundaries as a function of gene expression, with eFlux and TRFBA cited as examples
- Proteomics and phosphoproteomics data can be integrated as alternatives to transcriptomics data
- Genome-wide model Recon3D can be used as alternative to core model ENGRO2

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- INTEGRATE sets constraints on selected extracellular fluxes according to exo-metabolomics data to improve model predictions
- Transcriptomics-derived RAS must be used for reactions without proteomics coverage
- SBML format does not embed type 2 constraints on extracellular fluxes, which must be specified separately

## Steps

### Step `task_001`
- Title: Reproduce t-SNE separation of breast cell line Feasible Flux Distributions under combined Type 1+2+3 constraints
- Task kind: `reproduction`
- Task: Apply all three constraint types (nutrient availability, extracellular fluxes, transcriptomics-derived) to the ENGRO2 metabolic model using breast cancer cell line multi-omics data and reproduce the t-SNE visualization demonstrating clear separation of five cell-line feasible flux distribution clusters.
- Inputs:
  - ENGRO2 metabolic network model (SBML format, 494 reactions, 410 metabolites, 494 genes)
  - RNA-seq transcriptomics data from five breast cell lines (PRJNA767228, FPKM format, 3 biological replicates each)
  - Intracellular metabolomics quantification from LC-MS analysis (MTBLS3597, 0–48 hour time window)
  - Extracellular flux measurements: glucose, lactate, glutamine, glutamate concentrations (YSI2950 bioanalyzer, fresh medium t=0 and spent medium after 48 hours)
  - Gene-Protein-Reaction (GPR) associations embedded in ENGRO2 model and Growth medium composition specifications for five cell lines
- Expected outputs:
  - t-SNE 2D projection plot showing clear separation of five cell-line Feasible Flux Distribution (FFD) clusters with all three constraint types applied (Fig 3D)
  - Five cell-relative metabolic models (SBML format) with Type 1, Type 2, and Type 3 constraints applied
  - Quantitative evaluation: Spearman correlation coefficient between experimental and in silico growth yield on glucose for all four constraint scenarios (Type 1; Type 1+2; Type 3; Type 1+2+3)
- Tools: constraint-based stoichiometric metabolic models, eFlux, TRFBA, GX-FBA, scFBA, STAR aligner (v.2.6.1d), HTSeq (v.0.6.1), YSI2950 bioanalyzer, Agilent 1290 Infinity UHPLC system, Agilent 6550 iFunnel Q-TOF mass spectrometer, optGpSampler algorithm, t-SNE (t-distributed Stochastic Neighbor Embedding), COBRApy
- Landmark output files: reaction_activity_scores_all_lines.csv, cell_relative_models_type1_type2_type3_*.sbml, feasible_flux_distributions_sampled_*.csv, growth_yield_correlation_metrics.txt
- Primary expected artifact: `tsne_ffd_constraint_integration.png`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce concordance analysis between RAS and RPS variants for 81 fully covered reactions
- Task kind: `reproduction`
- Task: Using deposited RAS and RPS datasets from the INTEGRATE Zenodo archive (10.5281/zenodo.5824504), compute Cohen's kappa concordance scores between RAS and RPS directional changes across all pairwise comparisons of the five breast cell lines for the 81 reactions with complete substrate metabolomics coverage, and reproduce the concordance heatmap and scatter plot reported in Fig 4A–B.
- Inputs:
  - RAS (Reaction Activity Score) matrix for five breast cell lines (MCF102A, SKBR3, MCF7, MDAMB231, MDAMB361) from Zenodo deposit 10.5281/zenodo.5824504
  - RPS (Reaction Propensity Score) matrix for five breast cell lines computed from intracellular metabolomics data (LC-MS, deposited at MTBLS3597) and reaction stoichiometry
  - FFD (Feasible Flux Distribution) samples for five cell lines uniformly sampled from constrained metabolic models using optGpSampler
  - Metadata table identifying the 81 reactions with complete substrate metabolomics coverage and their Gene-Protein-Reaction associations
- Expected outputs:
  - Cohen's kappa concordance scores (RPSvsRAS and RPSvsFFD) for all 81 reactions with complete substrate coverage, formatted as a two-column numeric table with reaction names and kappa values
  - Scatter plot (RPSvsFFD kappa vs. RPSvsRAS kappa) with reactions colored by RASvsFFD concordance score and labeled for kappa ≥ 0.2
  - Heatmap of RPSvsRAS and RPSvsFFD Cohen's kappa values for reactions with RPSvsFFD concordance > 0.2, ordered by RPSvsFFD score
  - Empirical p-values and Benjamini-Hochberg adjusted p-values (FDR < 5%) for each reaction's kappa concordance, assessed against the null distribution from random permutation of RPS variations
- Tools: constraint-based stoichiometric metabolic models, COBRApy, optGpSampler, Mann-Whitney U test, Cohen's kappa metric, Benjamini-Hochberg FDR correction
- Landmark output files: ras_variation_signs.csv, rps_variation_signs.csv, ffd_variation_signs.csv, pairwise_kappa_matrix.csv, scatter_concordance_plot.png, heatmap_kappa_reactions.png
- Primary expected artifact: `concordance_kappa_table.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce growth yield correlation improvement attributable to Type 3 (transcriptomics-derived) constraints
- Task kind: `reproduction`
- Task: Compute Spearman correlation coefficients between experimental and in silico growth yield on glucose for the five breast cell lines under four constraint scenarios (Type 1 alone, Type 1+2, Type 1+2+3, and Type 3 alone), reproducing the reported finding that transcriptomics-derived constraints (Type 3) alone yield the best discrimination while Type 1+2+3 combined provides the highest correlation.
- Inputs:
  - Five cell-relative metabolic models in SBML format (ENGRO2) with Type 1, Type 2, and Type 3 constraints defined separately
  - Experimental growth yield measurements (protein produced over 48h / glucose consumed over 48h) for five cell lines from Bradford assay and YSI bioanalyzer
  - ENGRO2 metabolic network model with 494 reactions, 410 metabolites, and gene-protein-reaction associations
- Expected outputs:
  - Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1 constraints alone
  - Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1+2 constraints
  - Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1+2+3 constraints
  - Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 3 constraints alone
  - Correlation plot with four scatter subplots (one per constraint scenario) showing experimental vs. in silico growth yield with ρ and p-value annotations
- Tools: COBRApy (optGpSampler algorithm), Flux Variability Analysis (FVA), constraint-based stoichiometric metabolic models
- Landmark output files: type1_ffd_samples.csv, type12_ffd_samples.csv, type3_ffd_samples.csv, type123_ffd_samples.csv, experimental_growth_yields.csv, predicted_growth_yields_all_scenarios.csv
- Primary expected artifact: `growth_yield_correlation_analysis.pdf`

### Step `task_004`
- Title: Reconstruct the Reaction Propensity Score (RPS) computation module using mass action law formulation
- Task kind: `component_reconstruction`
- Task: Compute Reaction Propensity Scores (RPS) for all metabolic reactions in the ENGRO2 model using intracellular metabolomics data and the mass action law, producing a quantitative dataset that predicts how differences in substrate availability translate into differences in metabolic fluxes.
- Inputs:
  - Intracellular metabolomics abundance data (metabolite concentrations in molar or relative units) for five breast cell lines (MCF102A, MCF7, MDAMB231, MDAMB361, SKBR3), including at least 2 biological replicates per cell line
  - ENGRO2 constraint-based stoichiometric metabolic network model with Gene-Protein-Reaction (GPR) associations and complete reaction-metabolite stoichiometry
- Expected outputs:
  - Reaction Propensity Scores (RPS) dataset: a matrix (or table) with metabolic reactions as rows, cell lines as columns, and normalized RPS values (0–1 range) as entries, computed from mass action law applied to substrate concentrations
- Tools: constraint-based stoichiometric metabolic models
- Landmark output files: metabolite_reaction_mapping.csv, rps_raw_scores.csv, rps_normalized.csv
- Primary expected artifact: `rps_scores.csv`

### Step `task_005`
- Depends on: `task_001`
- Title: Analyze reaction-level regulatory classification using the intersection of RPS-vs-FFD and RAS-vs-FFD fold-changes
- Task kind: `analysis`
- Task: Classify metabolic reactions into regulatory categories (transcriptional, metabolic, combined, or unclassified) by computing Cohen's kappa concordance scores between RAS-vs-FFD and RPS-vs-FFD fold-change directions across all pairwise cell-line comparisons, and produce a labelled reaction classification table.
- Inputs:
  - RAS (Reaction Activity Score) dataset for all reactions and cell lines from ENGRO2 model (Zenodo 10.5281/zenodo.5824504 or qLSLab/integrate repository)
  - RPS (Reaction Propensity Score) dataset computed from intracellular metabolomics concentrations
  - FFD (Feasible Flux Distributions) sampled from constrained ENGRO2 metabolic models for each cell line (10 batches of 100,000 steady-state solutions each)
  - Intracellular metabolomics data (LC-MS metabolite abundance measurements from MTBLS3597)
  - Transcriptomics data (RNA-seq read counts in FPKM, deposited as PRJNA767228)
- Expected outputs:
  - Reaction classification table (XLSX or CSV) with columns: reaction identifier, Cohen's kappa RPSvsFFD score, Cohen's kappa RPSvsRAS score, empirical p-value, FDR-adjusted p-value, regulatory class label (transcriptional/metabolic/combined/other), and confidence intervals
  - Q–Q plot comparing empirical probability distribution of Cohen's kappa agreement between independent datasets versus INTEGRATE RPS-vs-FFD concordance results
  - Heatmap visualization of RPSvsRAS and RPSvsFFD concordance scores for reactions with fair concordance (score >0.2), annotated with reaction names and regulatory class assignments
- Tools: constraint-based stoichiometric metabolic models, COBRApy (for optGpSampler uniform sampling)
- Landmark output files: concordance_scores_raw.csv, variation_signs_by_pair.csv, empirical_pvalue_distribution.csv, fdr_corrected_classifications.csv
- Primary expected artifact: `reaction_classification_table.xlsx`

## Final expected outputs

- `Cohen's kappa concordance scores (RPSvsRAS and RPSvsFFD) for all 81 reactions with complete substrate coverage, formatted as a two-column numeric table with reaction names and kappa values` (type: file, tolerance: hash)
- `Scatter plot (RPSvsFFD kappa vs. RPSvsRAS kappa) with reactions colored by RASvsFFD concordance score and labeled for kappa ≥ 0.2` (type: file, tolerance: hash)
- `Heatmap of RPSvsRAS and RPSvsFFD Cohen's kappa values for reactions with RPSvsFFD concordance > 0.2, ordered by RPSvsFFD score` (type: file, tolerance: hash)
- `Empirical p-values and Benjamini-Hochberg adjusted p-values (FDR < 5%) for each reaction's kappa concordance, assessed against the null distribution from random permutation of RPS variations` (type: file, tolerance: hash)
- `Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1 constraints alone` (type: file, tolerance: hash)
- `Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1+2 constraints` (type: file, tolerance: hash)
- `Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1+2+3 constraints` (type: file, tolerance: hash)
- `Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 3 constraints alone` (type: file, tolerance: hash)
- `Correlation plot with four scatter subplots (one per constraint scenario) showing experimental vs. in silico growth yield with ρ and p-value annotations` (type: file, tolerance: hash)
- `Reaction Propensity Scores (RPS) dataset: a matrix (or table) with metabolic reactions as rows, cell lines as columns, and normalized RPS values (0–1 range) as entries, computed from mass action law applied to substrate concentrations` (type: file, tolerance: hash)
- `Reaction classification table (XLSX or CSV) with columns: reaction identifier, Cohen's kappa RPSvsFFD score, Cohen's kappa RPSvsRAS score, empirical p-value, FDR-adjusted p-value, regulatory class label (transcriptional/metabolic/combined/other), and confidence intervals` (type: file, tolerance: hash)
- `Q–Q plot comparing empirical probability distribution of Cohen's kappa agreement between independent datasets versus INTEGRATE RPS-vs-FFD concordance results` (type: file, tolerance: hash)
- `Heatmap visualization of RPSvsRAS and RPSvsFFD concordance scores for reactions with fair concordance (score >0.2), annotated with reaction names and regulatory class assignments` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: mixed — per-step.** Closed steps must reproduce (rubrics above bind on them); open steps are judged by **SCIENTIFIC_VALIDITY** (below). Invariants bind everywhere; different is not wrong on the open steps.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** intermediate

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_integrate_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Cohen's kappa concordance scores (RPSvsRAS and RPSvsFFD) for all 81 reactions with complete substrate coverage, formatted as a two-column numeric table with reaction names and kappa values": "<locator>",
    "Scatter plot (RPSvsFFD kappa vs. RPSvsRAS kappa) with reactions colored by RASvsFFD concordance score and labeled for kappa \u2265 0.2": "<locator>",
    "Heatmap of RPSvsRAS and RPSvsFFD Cohen's kappa values for reactions with RPSvsFFD concordance > 0.2, ordered by RPSvsFFD score": "<locator>",
    "Empirical p-values and Benjamini-Hochberg adjusted p-values (FDR < 5%) for each reaction's kappa concordance, assessed against the null distribution from random permutation of RPS variations": "<locator>",
    "Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1 constraints alone": "<locator>",
    "Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1+2 constraints": "<locator>",
    "Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 1+2+3 constraints": "<locator>",
    "Spearman correlation coefficient and p-value between experimental and in silico growth yield for Type 3 constraints alone": "<locator>",
    "Correlation plot with four scatter subplots (one per constraint scenario) showing experimental vs. in silico growth yield with \u03c1 and p-value annotations": "<locator>",
    "Reaction Propensity Scores (RPS) dataset: a matrix (or table) with metabolic reactions as rows, cell lines as columns, and normalized RPS values (0\u20131 range) as entries, computed from mass action law applied to substrate concentrations": "<locator>",
    "Reaction classification table (XLSX or CSV) with columns: reaction identifier, Cohen's kappa RPSvsFFD score, Cohen's kappa RPSvsRAS score, empirical p-value, FDR-adjusted p-value, regulatory class label (transcriptional/metabolic/combined/other), and confidence intervals": "<locator>",
    "Q\u2013Q plot comparing empirical probability distribution of Cohen's kappa agreement between independent datasets versus INTEGRATE RPS-vs-FFD concordance results": "<locator>",
    "Heatmap visualization of RPSvsRAS and RPSvsFFD concordance scores for reactions with fair concordance (score >0.2), annotated with reaction names and regulatory class assignments": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
