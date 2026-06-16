# Evaluation Strategy

## Direct Checks

- file_exists: Verify S1 Compressed File Archive (cell-relative metabolic models in SBML format) is accessible in Zenodo deposit 10.5281/zenodo.5824504
- file_exists: Verify S1 File containing experimental growth yield data, extracellular flux measurements, and protein content for all five cell lines is available
- file_format_is: Verify FFD datasets (Feasible Flux Distributions) from ENGRO2 models are in format specified in Materials and Methods (sampled steady-state solutions)
- value_in_range: Spearman correlation coefficient reported in Fig 3E for constraint scenario C (transcriptomics-derived constraints alone, Type 3) is positive and exceeds correlation from Type 1+2 constraints alone
- value_in_range: Spearman correlation coefficient for all three constraints combined (Type 1+2+3, Fig 3D) shows improvement over Type 3 alone, but Fig 3 caption states Type 3 constraints alone 'result in a good separation of the feasible regions'
- script_runs: Code workflow from https://github.com/qLSLab/integrate executes without error when applied to deposited cell-relative models and experimental inputs
- output_matches_reference: Reconstructed growth yield predictions (median protein synthesis flux over glucose uptake) match values reported in S1 File for all five cell lines under Type 3 constraints, robust to parameter choices in FVA and sampling (thinning=10)

## Expert Review

- Assess whether the selection of 20% fold-change threshold for registering variation sign (Materials and Methods, Concordance analysis section) is justified and consistent with prior metabolic pathway sensitivity literature cited
- Evaluate whether constraint-based modeling assumptions (steady-state, pseudo-stoichiometric mass action kinetics without enzyme kinetic parameters) adequately justify the causal interpretation that Type 3 constraints capture transcriptional regulation independent of metabolic regulation
- Examine whether the reported improvement in growth yield correlation under Type 3 constraints versus Type 1 or Type 1+2 (Fig 3E) reflects genuine superior predictive power or confounding from degrees-of-freedom in flux sampling and constraint relaxation
- Review whether the experimental growth yield computation (protein synthesis flux / glucose uptake flux, based on Bradford assay and YSI analysis) adequately controls for non-protein biomass components and whether this affects the correlation baseline
