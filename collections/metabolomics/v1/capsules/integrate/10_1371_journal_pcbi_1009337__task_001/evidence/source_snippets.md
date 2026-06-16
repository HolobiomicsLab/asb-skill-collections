# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Can the INTEGRATE pipeline with all three constraint types (nutrient availability, extracellular fluxes, and transcriptomics-derived constraints) successfully segregate the feasible flux distributions of five breast cancer cell lines with distinct metabolic profiles?: 'the simultaneous application of the three constraints help the flux distributions sampled from each model (corresponding to the specific colour in the plot) from one another'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The combination of all three constraint types (type 1+2+3) applied to ENGRO2 achieves clear separation of the five cell-line FFD clusters in t-SNE space, with transcriptomics-derived constraints alone providing good segregation but extracellular flux constraints improving inter-model separation.: 'Notably, constraints on extracellular fluxes alone (Fig 3B) do not allow the feasible flux distributions of the five models to be discriminated. On the contrary, transcriptomics-derived constraints'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] ENGRO2 metabolic network model (SBML format, 494 reactions, 410 metabolites, 494 genes): 'The final version of the ENGRO2 core model consists of 494 reactions, 410 metabolites and 494 genes.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] RNA-seq transcriptomics data from five breast cell lines (PRJNA767228, FPKM format, 3 biological replicates each): 'Raw reads are available in NCBI Short Reads Archive (SRA) under Accession Number PRJNA767228.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Intracellular metabolomics quantification from LC-MS analysis (MTBLS3597, 0–48 hour time window): 'raw data are deposited at www.ebi.ac.uk/metabolights/MTBLS3597. Normalized data (on protein μg) used for computational analyses are reported in S1 File.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Extracellular flux measurements: glucose, lactate, glutamine, glutamate concentrations (YSI2950 bioanalyzer, fresh medium t=0 and spent medium after 48 hours): 'Absolute quantification of glucose, lactate, glutamine, and glutamate in fresh medium at t = 0 and in spent media after 48 hours of growth was determined enzymatically using YSI2950 bioanalyzer'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Gene-Protein-Reaction (GPR) associations embedded in ENGRO2 model and Growth medium composition specifications for five cell lines: 'we set flux boundaries to the generic reconstruction of human metabolism ENGRO2, according to the differences observed in the experimental input data relative to the five investigated cell lines'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] t-SNE 2D projection plot showing clear separation of five cell-line Feasible Flux Distribution (FFD) clusters with all three constraint types applied (Fig 3D): 'we represented the high-dimensional sampled flux distributions in a two-dimensional space [50]. It is possible to appreciate how the simultaneous application of the three constraints better separates'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Five cell-relative metabolic models (SBML format) with Type 1, Type 2, and Type 3 constraints applied: 'The final five cell-relative metabolic models (SBML format) are included in S1 Compressed File Archive.'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Quantitative evaluation: Spearman correlation coefficient between experimental and in silico growth yield on glucose for all four constraint scenarios (Type 1; Type 1+2; Type 3; Type 1+2+3): 'E) Correlation between the experimental and in silico growth yield on glucose is reported for each of the four settings in panels A, B, C and D. The Spearman correlation coefficient and p-value are'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] constraint-based stoichiometric metabolic models: 'using constraint-based stoichiometric metabolic models as a scaffold'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] eFlux: 'we set flux boundaries as a function of gene expression as done, among others, by eFlux [36]'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] TRFBA: 'we set flux boundaries as a function of gene expression as done, among others, by eFlux [36] and TRFBA'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] GX-FBA: 'We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in GX-FBA [26]'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] scFBA: 'We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA [38]'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] STAR aligner (v.2.6.1d): 'raw reads were mapped with STAR aligner (v.2.6.1d) to human reference genome (hg38)'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] HTSeq (v.0.6.1): 'gene counts were calculated by HTSeq (v.0.6.1), using the hg38 Encode-Gencode GTF file (v28)'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] YSI2950 bioanalyzer: 'Absolute quantification of glucose, lactate, glutamine, and glutamate in fresh medium at t = 0 and in spent media after 48 hours of growth was determined enzymatically using YSI2950 bioanalyzer'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Agilent 1290 Infinity UHPLC system: 'LC separation was performed using an Agilent 1290 Infinity UHPLC system and an InfintyLab Poroshell 120 PFP column'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Agilent 6550 iFunnel Q-TOF mass spectrometer: 'MS detection was performed using an Agilent 6550 iFunnel Q-TOF mass spectrometer with Dual JetStream source operating in negative ionization mode'

## ev_021

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] optGpSampler algorithm: 'we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions of the ENGRO2 model in all the tested conditions'

## ev_022

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] t-SNE (t-distributed Stochastic Neighbor Embedding): 'We then applied a t-distributed stochastic neighbor embedding (t-SNE) algorithm and represented the high-dimensional sampled flux distributions in a two-dimensional space'

## ev_023

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] COBRApy: 'we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72]'

## ev_024

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Specific t-SNE algorithm hyperparameters (perplexity, learning rate, number of iterations, random seed) used to generate the t-SNE plot shown in Fig 3D are not stated in the text; only that 10,000 steady-state solutions per model were plotted: 'For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted.'

## ev_025

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The paper does not explicitly state whether the published t-SNE plot in Fig 3D was generated from a single run or averaged/consensus visualization across multiple runs with different random seeds: 'A two-dimensional map of the FFDs of the five cell lines in each setting is shown.'

## ev_026

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] No explicit statement of how the qualitative concordance threshold (Cohen's kappa > 0.2) used for concordance analysis relates to the FFD cluster separation quality or whether cluster separation metrics (silhouette score, Davies-Bouldin index) are reported: 'We reported the names of the reactions having at least one of the scores greater than 0.2 (i.e. fair concordance).'

## ev_027

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The exact computational cost (CPU time, memory requirements) for uniform sampling one million solutions per cell-line model with three constraint types is not reported, making reproducibility timing difficult to predict: 'we sampled a million steady state solutions of the ENGRO2 model in all the tested conditions.'

## ev_028

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Whether the cell-relative models' performance on growth yield prediction (Fig 3E) shows comparable accuracy across all five cell lines or if certain cell lines have systematically higher/lower prediction error is not discussed: 'The condition where transcriptomics-derived constraints alone are integrated well discriminates the five cell lines in terms of their growth rate, as shown in the relative correlation plot in Fig 3.'
