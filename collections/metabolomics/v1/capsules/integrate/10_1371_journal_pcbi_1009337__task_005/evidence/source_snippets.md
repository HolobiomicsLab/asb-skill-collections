# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How can RAS, RPS, and FFD datasets be intersected to classify each metabolic reaction into regulatory categories (transcriptional, metabolic, combined, or unclassified)?: 'INTEGRATE then assigns two scores to metabolic reactions. The first score quantifies the concordance level between the variation signs obtained for the RAS dataset and those obtained for the RPS'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Reactions are classified by measuring Cohen's kappa concordance between RAS-vs-FFD and RPS-vs-FFD variation signs: positive concordance for both indicates combined regulation, positive RPSvsFFD with negative RASvsFFD indicates metabolic control only, and positive values for both RASvsFFD and RASvsRPS indicates transcriptional and metabolic regulation.: 'Reactions displaying positive values for both RPSvsFFD and RPSvsRAS scores (first quadrant). Variations in these reactions must be imputed to transcriptional and metabolic regulation. Reactions'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] RAS (Reaction Activity Score) dataset for all reactions and cell lines from ENGRO2 model (Zenodo 10.5281/zenodo.5824504 or qLSLab/integrate repository): 'Scripts to reproduce the integrate, and are also available at https://github.com/qLSLab/integrate'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] RPS (Reaction Propensity Score) dataset computed from intracellular metabolomics concentrations: 'INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] FFD (Feasible Flux Distributions) sampled from constrained ENGRO2 metabolic models for each cell line (10 batches of 100,000 steady-state solutions each): 'we sampled a million steady state solutions of the ENGRO2 model in all the tested conditions. To get a large number of samples, we used the batch generator option of the algorithm, creating ten'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Intracellular metabolomics data (LC-MS metabolite abundance measurements from MTBLS3597): 'raw data are deposited at www.ebi.ac.uk/metabolights/MTBLS3597'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Transcriptomics data (RNA-seq read counts in FPKM, deposited as PRJNA767228): 'Raw reads are available in NCBI Short Reads Archive (SRA) under Accession Number PRJNA767228'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Reaction classification table (XLSX or CSV) with columns: reaction identifier, Cohen's kappa RPSvsFFD score, Cohen's kappa RPSvsRAS score, empirical p-value, FDR-adjusted p-value, regulatory class label (transcriptional/metabolic/combined/other), and confidence intervals: 'Table of RPSvsRAS and RPSvsFFD Cohen's kappa coefficients, empirical and adjusted p-values and confidence intervals for all model reactions'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Q–Q plot comparing empirical probability distribution of Cohen's kappa agreement between independent datasets versus INTEGRATE RPS-vs-FFD concordance results: 'Q − Q plot between the empirical probability of agreement between two independent datasets and INTEGRATE Cohen's kappa distribution'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Heatmap visualization of RPSvsRAS and RPSvsFFD concordance scores for reactions with fair concordance (score >0.2), annotated with reaction names and regulatory class assignments: 'Heatmap showing the RPSvsRAS and the RPSvsFFD concordance scores, for reactions having a level of concordance between RPS and FFD greater than 0.2'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] constraint-based stoichiometric metabolic models: 'using constraint-based stoichiometric metabolic models as a scaffold'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] COBRApy (for optGpSampler uniform sampling): 'optGpSampler algorithm [71] available in COBRApy [72]'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The exact number of metabolic reactions in ENGRO2 model that have complete substrate abundance data available in the metabolomics dataset: 'we computed for each reaction r and for each cell line c (assumed at steady state) a Reaction Propensity Score (RPS)'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The computational method used to determine whether a fold-change or concordance variation is statistically significant when comparing a given cell-line pair across RAS, RPS, and FFD datasets: 'We consider a variation as statistically significant if both test is rejected according to any suited statistical test and if the variation exceeds a threshold value'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The precise definition and cutoff thresholds used to classify reactions into the 'other' category (those with negative RPSvsFFD but positive RPSvsRAS that are not purely transcriptional): 'we simply labeled this category as 'other''

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Whether the 10 pairwise cell-line comparisons include all possible pairs (5 choose 2 = 10) or a subset, and the specific identity of cell lines being compared: 'for all eligible reactions, i.e. reactions for which quantification of all substrate abundances was available. We focused on the qualitative concordance'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The number of reactions discarded or marked as 'missing data' due to absence of GPR associations or incomplete substrate abundance coverage: 'For reactions not associated with a GPR the RAS was set to 1'
