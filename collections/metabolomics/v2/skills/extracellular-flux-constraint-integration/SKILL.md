---
name: extracellular-flux-constraint-integration
description: Use when you have constraint-based metabolic models of multiple cell lines, experimental measurements of extracellular metabolite concentrations at two timepoints (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_2259
  tools:
  - Flux Variability Analysis
  - eFlux
  - TRFBA
  - scFBA
  - GX-FBA
  - constraint-based stoichiometric metabolic models
  - optGpSampler
  - COBRApy
  - YSI bioanalyzer (YSI2950)
  - Agilent 1290 Infinity UHPLC + 6550 iFunnel Q-TOF MS
  - t-SNE
  - rasIntegration.py
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA
- we set flux boundaries as a function of gene expression as done, among others, by eFlux [36] and TRFBA
- We used relative gene-expression values as in GX-FBA
- using constraint-based stoichiometric metabolic models as a scaffold
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions
- In this work, we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate_cq
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009337
  all_source_dois:
  - 10.1371/journal.pcbi.1009337
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# extracellular-flux-constraint-integration

## Summary

Integrate experimentally measured extracellular metabolite flux ratios (lactate/glucose, lactate/glutamine, glutamate/glutamine) as upper and lower bounds on exchange reactions in constraint-based metabolic models to improve prediction of cell-line-specific feasible flux distributions. This skill refines the flux prediction landscape by anchoring the model to observed substrate consumption and product secretion patterns.

## When to use

You have constraint-based metabolic models of multiple cell lines, experimental measurements of extracellular metabolite concentrations at two timepoints (e.g., fresh and spent media after 48 hours), and you need to reduce the size of the feasible flux region to improve segregation of metabolic phenotypes. Apply this skill when nutrient availability constraints alone produce insufficient inter-cell-line separation or when you want to capture cell-line-specific differences in catabolism and anabolism rates reflected in exometabolomic ratios.

## When NOT to use

- Extracellular metabolite time-course data is missing or covers only a single timepoint; flux ratios cannot be reliably computed without at least two timepoints.
- The metabolic model lacks exchange reactions for the metabolites being constrained (e.g., no lactate or glutamate exchange reaction in the model).
- Cell culture conditions differ substantially from those used to generate the model (e.g., different media composition, oxygen availability, or cell density); constraint values may not be transferable.
- You are studying a single cell line; extracellular flux ratio constraints are most valuable when comparing multiple phenotypes and require replication to estimate cell-line-specific ratios.

## Inputs

- Constraint-based metabolic model (SBML or MAT format, e.g., ENGRO2)
- Extracellular metabolite concentrations at t=0 and t=48h per cell line and replicate (YSI or UHPLC-MS; CSV with columns: Ratio, cell_line_A, cell_line_A_replica2, ...)
- Cell-line identifiers and replicate labels (e.g., MCF102A_A, MCF102A_B)
- Biomass reaction ID and exchange reaction IDs for lactate, glucose, glutamine, glutamate (string)

## Outputs

- Cell-line-specific SBML or MAT metabolic models with integrated Type 1+2 (nutrient + extracellular flux ratio) constraints
- Feasible flux distributions (FFD) dataset: CSV files with rows=steady-state solutions, columns=reaction fluxes for each constrained model
- t-SNE projection of FFD (2D coordinates per sampled solution, colored by cell line)
- Concordance metrics: Spearman correlation between predicted and experimental growth yield per cell line with p-values

## How to apply

First, compute extracellular flux ratios from time-course metabolomics data (e.g., lactate secretion / glucose consumption) for each cell line and replicate, typically from YSI bioanalyzer or UHPLC-MS measurement of media at t=0 and t=48h. Convert these ratios into exchange reaction flux constraints: set the upper bound of the lactate exchange reaction to the measured lactate/glucose ratio times the glucose uptake rate, and similarly for glutamate/glutamine and lactate/glutamine. Integrate these ratio constraints simultaneously with nutrient availability constraints (Type 1) and transcriptomics-derived RAS constraints (Type 3) into each cell-relative model. The key rationale is that extracellular flux ratios encode metabolic strategy (e.g., Warburg phenotype vs. oxidative metabolism) and are more stable and cell-line-specific than individual flux magnitudes, which depend on growth rate and biomass composition. Validate constraint integration by checking that the constrained model's predicted growth yield on glucose correlates with experimental yield (Spearman correlation with p-value < 0.05) and that t-SNE visualization of sampled feasible flux distributions shows improved inter-cell-line separation compared to Type 1 or Type 1+3 constraints alone.

## Related tools

- **COBRApy** (Python library to load, modify, and integrate constraints into SBML metabolic models; set bounds on exchange reactions) — https://github.com/opencobra/cobrapy
- **YSI bioanalyzer (YSI2950)** (Enzymatic measurement instrument for quantifying glucose, lactate, glutamine, and glutamate in culture media)
- **Agilent 1290 Infinity UHPLC + 6550 iFunnel Q-TOF MS** (High-resolution liquid chromatography–mass spectrometry for targeted quantification of extracellular metabolites with mass accuracy and isotopic natural abundance correction via MassHunter ProFinder)
- **optGpSampler** (Uniform sampling algorithm for feasible flux distributions from constrained null space of stoichiometric matrix; generates steady-state solutions for visualization and statistical analysis)
- **t-SNE** (Dimensionality reduction for visualization of high-dimensional feasible flux distributions to assess inter-cell-line segregation quality under different constraint conditions)
- **rasIntegration.py** (Pipeline script (from qLSLab/integrate) that integrates RAS, nutrient availability, and extracellular flux ratio constraints into cell-relative models; parameters: imposeYSI='Y', ysiFileName, imposeMedium='Y', mediumFileName) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/rasIntegration.py --imposeYSI Y --imposeRasConstraints Y --imposeMedium Y --ysiFileName ysi_ratio.csv --rasNormFileName ENGRO2_wNormalizedRAS.csv --mediumFileName medium.csv --modelId ENGRO2
```

## Evaluation signals

- Spearman correlation between in silico predicted growth yield on glucose and experimental yield is statistically significant (p < 0.05) for all cell lines under Type 1+2+3 constraints, indicating constraints are physiologically consistent.
- t-SNE visualization of feasible flux distributions shows improved inter-cell-line separation (visually distinct clusters) under Type 1+2+3 constraints compared to Type 1 or Type 1+2 alone, quantifiable by silhouette coefficient or manual cluster inspection.
- Each constrained model is non-infeasible (has a non-empty feasible region with ≥1000 sampled steady-state solutions) and the constrained null space volume is smaller than the unconstrained null space, confirming that extracellular flux ratio constraints reduce the feasible region.
- Extracellular flux ratio values are consistent across replicates within a cell line (coefficient of variation < 20% for lactate/glucose, lactate/glutamine, glutamate/glutamine ratios).
- Constraint check: verify that predicted exchange fluxes for lactate, glucose, glutamine, and glutamate from FFD samples fall within the specified bounds (lower_bound ≤ flux ≤ upper_bound) for ≥99% of sampled solutions.

## Limitations

- Extracellular flux ratio constraints assume quasi-steady-state metabolism and linear accumulation of metabolites over the 48h culture window; violations occur if cell culture reaches stationary phase or if metabolite accumulation becomes nonlinear.
- Limited metabolite coverage in exometabolomics datasets constrains the number of exchange reactions that can be bounded; unmeasured extracellular metabolites remain unconstrained and may inflate the feasible flux region.
- Enzymatic activity, allosteric regulation, product inhibition, and cofactor/prosthetic group effects are not captured by flux ratio constraints alone; reactions may violate predicted bounds due to post-translational regulation.
- Extracellular flux ratios are computed as mean across replicates; biological or technical variability within a cell line is not propagated into constraint uncertainty, potentially leading to overly narrow or overly wide feasible regions.
- Constraint integration assumes that metabolite exchange follows mass action kinetics and that substrate availability is the primary driver of flux differences; cell-line-specific differences in enzyme expression or allosteric regulation will not be fully captured.

## Evidence

- [intro] Set constraints on selected extracellular fluxes according to exo-metabolomics data: "to improve model predictions, INTEGRATE sets constraints also on selected extracellular fluxes, according to"
- [results] Extracellular flux ratio measurement via YSI bioanalyzer: "Absolute quantification of glucose, lactate, glutamine, and glutamate in fresh medium at t = 0 and in spent media after 48 hours of growth was determined enzymatically using YSI2950 bioanalyzer"
- [other] Type 1+2+3 constraints achieve superior segregation compared to subsets: "Type 1+2+3 constraints together achieve superior segregation of the five cell line flux distributions compared to individual or paired constraint applications, as demonstrated by t-SNE visualization"
- [readme] Constraint integration into cell-relative models via rasIntegration pipeline: "imposeYSI: 'Y' (yes) or 'N' (no) according to whether extracellular flux ratio constraints have to be integrated"
- [other] Extracellular flux ratios include lactate/glucose, lactate/glutamine, glutamate/glutamine: "nutrient availability plus extracellular flux ratios: lactate/glucose, lactate/glutamine, glutamate/glutamine"
