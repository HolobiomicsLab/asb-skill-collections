# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How does the mass action law formulation translate intracellular metabolomics data into Reaction Propensity Scores (RPS) that quantify the expected relative metabolic flux changes across cell lines based purely on substrate availability differences?: 'INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes (metabolic'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] For each reaction r and cell line c, the Reaction Propensity Score (RPS) is computed as the product of substrate concentrations each raised to their stoichiometric coefficients: RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q), where [X_q] is substrate concentration and s_r,q is the stoichiometric coefficient. If any substrate is unmeasured, the reaction is omitted from the RPS dataset.: 'the RPS score is computed as the product of the concentrations of the reacting substances, with each concentration raised to a power equal to its stoichiometric coefficient. According to the mass'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Intracellular metabolomics abundance data (metabolite concentrations in molar or relative units) for five breast cell lines (MCF102A, MCF7, MDAMB231, MDAMB361, SKBR3), including at least 2 biological replicates per cell line: 'We quantified the abundance of intracellular metabolites and prepared libraries for RNA-sequencing at 48h'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] ENGRO2 constraint-based stoichiometric metabolic network model with Gene-Protein-Reaction (GPR) associations and complete reaction-metabolite stoichiometry: 'The ENGRO2 core model consists of 494 reactions, 410 metabolites and 494 genes'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Reaction Propensity Scores (RPS) dataset: a matrix (or table) with metabolic reactions as rows, cell lines as columns, and normalized RPS values (0–1 range) as entries, computed from mass action law applied to substrate concentrations: 'This dataset includes an RPS score, based on the availability of reaction substrates, for (ideally) each input model reaction and for each sample'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] constraint-based stoichiometric metabolic models: 'using constraint-based stoichiometric metabolic models as a scaffold'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No explicit specification of whether metabolite abundance values are normalized, log-transformed, or left in raw concentration units before RPS computation; unclear if concentrations are treated as absolute (mM) or relative: 'RPS_r^c = ∏([X_q])^s_r,q does not specify the units or normalization of [X_q] metabolite concentration values or whether they are absolute or relative abundances'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] No explicit listing of how many reactions in ENGRO2 (out of 494 total) are expected to retain RPS values after applying the missing-substrate-omission rule; no count of excluded reactions provided: 'If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset; 81 reactions analyzed for concordance but unclear if 81 is the post-omission'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No explicit detail on whether stoichiometric coefficients (s_r,q) are sourced from the ENGRO2 stoichiometric matrix directly or computed from GPR rule parsing; unclear if the formula applies stoichiometric integer coefficients or fractional ATP/cofactor stoichiometries: 'the mass action law is assumed: v_r = k_r ∏[X_q]^s_r,q; s_r is the stoichiometric coefficient of substrate X_q in reaction r i.e., how many molecules of the substrate partake to the reaction; no'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No explicit documentation of how the stage handles metabolites with below-detection-limit (BDL) or missing values in the LC-MS dataset; unclear whether BDL values are set to zero, a floor, or excluded entirely: 'Metabolite extraction and LC-MS profiling method describes instrument parameters and data processing with MassHunter ProFinder but does not address missing or below-detection-limit metabolite'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No explicit statement on whether the RPS stage applies the same cell-relative model constraints (Type 1, Type 2, Type 3 nutrient/extracellular/transcriptomics constraints) as described for FFD generation, or operates independently on raw metabolomics data: 'INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict differences in metabolic fluxes (metabolic regulation only), neglecting enzymatic activity;'
