# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] What are the Cohen's kappa concordance values between RAS and RPS directional changes for metabolic reactions with complete substrate metabolomics coverage across the five breast cell lines?: 'We quantified the level of concordance of the 10 variation signs (1 for each pair of cell lines) for a given pair of datasets by means of the Cohen's kappa metric'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Concordance analysis of RAS and RPS directional variations across the 81 metabolic reactions with full substrate abundances yields Cohen's kappa values reported in a heatmap, with reactions ranked according to RPSvsFFD concordance scores and only those with scores greater than 0.2 displayed.: 'The heatmap in Fig 4B reports the RPSvsRAS and the RPSvsFFD concordance scores (Cohen's kappa) of ENGRO2 metabolic reactions, limited to the subset (of cardinality 81) of reactions for which'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] RAS (Reaction Activity Score) matrix for five breast cell lines (MCF102A, SKBR3, MCF7, MDAMB231, MDAMB361) from Zenodo deposit 10.5281/zenodo.5824504: 'available in Zenodo under permanent identifier 10.5281/zenodo.5824504'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] RPS (Reaction Propensity Score) matrix for five breast cell lines computed from intracellular metabolomics data (LC-MS, deposited at MTBLS3597) and reaction stoichiometry: 'raw data are deposited at www.ebi.ac.uk/metabolights/MTBLS3597'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] FFD (Feasible Flux Distribution) samples for five cell lines uniformly sampled from constrained metabolic models using optGpSampler: 'we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Metadata table identifying the 81 reactions with complete substrate metabolomics coverage and their Gene-Protein-Reaction associations: 'limited to the subset (of cardinality 81) of reactions for which quantification of all substrate abundances was available'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Cohen's kappa concordance scores (RPSvsRAS and RPSvsFFD) for all 81 reactions with complete substrate coverage, formatted as a two-column numeric table with reaction names and kappa values: 'We quantified the level of concordance of the 10 variation signs (1 for each pair of cell lines) for a given pair of datasets by means of the Cohen's kappa metric'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Scatter plot (RPSvsFFD kappa vs. RPSvsRAS kappa) with reactions colored by RASvsFFD concordance score and labeled for kappa ≥ 0.2: 'Fig 4A reports the concordance level between RAS and RPS variations (briefly RPSvsRAS) versus the concordance level between RPS and FFD variation (briefly RPSvsFFD), for the 81 metabolic reactions'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Heatmap of RPSvsRAS and RPSvsFFD Cohen's kappa values for reactions with RPSvsFFD concordance > 0.2, ordered by RPSvsFFD score: 'The heatmap in Fig 4B reports the RPSvsRAS and the RPSvsFFD concordance scores (Cohen's kappa) of ENGRO2 metabolic reactions, limited to the subset (of cardinality 81)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Empirical p-values and Benjamini-Hochberg adjusted p-values (FDR < 5%) for each reaction's kappa concordance, assessed against the null distribution from random permutation of RPS variations: 'we adjusted it with the Benjamini and Hochberg procedure to keep the False Discovery Rate (FDR) below 5%. After FDR correction of the p-values, the concordance between RPSs and FFDs resulted'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] COBRApy: 'we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72]'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] optGpSampler: 'we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Mann-Whitney U test: 'we first performed the Mann-Whitney U test [73] (p-value < 0.05) between the FFD distributions of each pair of the five cell lines'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Cohen's kappa metric: 'We quantified the level of concordance of the 10 variation signs (1 for each pair of cell lines) for a given pair of datasets by means of the Cohen's kappa metric, which has been commonly used to'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Benjamini-Hochberg FDR correction: 'we adjusted it with the Benjamini and Hochberg procedure to keep the False Discovery Rate (FDR) below 5%'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Exact formula and implementation details for Mann-Whitney U test p-value threshold and log₂ fold-change threshold (20%) application to determine directional signs for FFD variations across pairwise cell-line comparisons: 'At first instance, a positive sign was registered if the distribution of samples values of the first member of the comparison was statistically higher (according to the statistical tests described'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Specific file names and internal structure of the Zenodo 10.5281/zenodo.5824504 deposit containing RAS and RPS datasets, and whether they are pre-computed or require derivation from raw RNA-seq and metabolomics files: 'available in Zenodo under permanent identifier 10.5281/zenodo.5824504'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Detailed filtering and data preprocessing steps applied to raw metabolomics data (from MetaboLights MTBLS3597) prior to RPS computation, including normalization, missing value handling, and quality control thresholds: 'raw data are deposited at www.ebi.ac.uk/metabolights/MTBLS3597. Normalized data (on protein μg) used for computational analyses are reported in S1 File.'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Rationale and justification for using Cohen's kappa (a discrete/categorical agreement metric) rather than a continuous concordance measure (e.g., Spearman or Pearson correlation) given that RAS and RPS are continuous-valued scores before sign discretization: 'We quantified the level of concordance of the 10 variation signs (1 for each pair of cell lines) for a given pair of datasets by means of the Cohen's kappa metric, which has been commonly used to'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Explicit documentation of how the 81-reaction subset with 'full substrate abundances available' was determined, including what constitutes 'full coverage' and how reactions with missing or below-detection-limit metabolites are handled: 'If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset.'
