---
name: constraint-based-flux-sampling-and-analysis
description: Use when when you have constraint-based metabolic models for multiple samples or cell lines, and you want to determine whether integrating multiple omics constraint types (nutrient availability, extracellular metabolite ratios, gene expression) produces distinct and biologically meaningful.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3391
  tools:
  - constraint-based stoichiometric metabolic models
  - Flux Variability Analysis
  - optGpSampler
  - COBRApy
  - Flux Variability Analysis (FVA)
  - t-SNE
  - YSI bioanalyzer (YSI2950)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- using constraint-based stoichiometric metabolic models as a scaffold
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions
- In this work, we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72]
- the implementation of optGpSampler algorithm [71] available in COBRApy [72]
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# constraint-based-flux-sampling-and-analysis

## Summary

Sample steady-state flux distributions from the feasible metabolic space of constraint-based stoichiometric models under different regulatory scenarios (nutrient availability, extracellular flux ratios, transcriptomics-derived constraints), then apply dimensionality reduction and statistical tests to evaluate how constraint combinations segregate metabolic phenotypes across biological samples.

## When to use

When you have constraint-based metabolic models for multiple samples or cell lines, and you want to determine whether integrating multiple omics constraint types (nutrient availability, extracellular metabolite ratios, gene expression) produces distinct and biologically meaningful segregation of their feasible flux distributions, or when you need to visualize and compare the geometry of the solution space under different regulatory assumptions.

## When NOT to use

- The metabolic model does not support stoichiometric constraint formulation or does not contain a biomass reaction.
- Experimental measurements (nutrient availability, extracellular flux ratios, transcriptomics, phenotype data) are absent or too sparse to construct or validate the constraint sets.
- The number of samples is very small (< 3 cell lines) such that inter-sample segregation metrics are uninformative or statistical tests lack power.

## Inputs

- constraint-based stoichiometric metabolic model (SBML or mat format)
- sample-specific nutrient availability bounds (lower and upper limits for uptake reactions)
- extracellular metabolite ratio measurements (e.g., lactate/glucose, lactate/glutamine ratios from YSI or UHPLC-MS)
- transcriptomics data (gene expression values, e.g., FPKM)
- experimental phenotype measurements (growth yield, biomass accumulation)

## Outputs

- Sampled steady-state flux distribution matrix (nSamples × nReactions) for each sample and constraint scenario
- t-SNE 2D projection coordinates for flux distribution visualization
- Visual segregation plots (t-SNE scatter) comparing intra- and inter-sample clustering across constraint scenarios
- Spearman correlation coefficients and p-values between experimental and predicted growth yield for each constraint scenario
- Concordance analysis results identifying which constraint combination achieves superior segregation and predictive accuracy

## How to apply

Load the constraint-based stoichiometric metabolic model and generate sample-specific models by applying type 1 constraints (nutrient availability bounds) separately for each cell line. Use uniform sampling (optGpSampler or equivalent) to draw 10,000 steady-state flux distributions from the null space of the stoichiometric matrix for each sample, subject to the constraint set. Apply t-SNE dimensionality reduction to project the high-dimensional flux vectors into 2D for visual segregation assessment. Repeat sampling for type 1+2 constraints (adding extracellular flux ratios such as lactate/glucose, lactate/glutamine, glutamate/glutamine), type 3 constraints (Reaction Activity Scores scaled by maximum gene expression), and all type 1+2+3 constraints combined. For each scenario, visually compare intra-sample clustering compactness and inter-sample separation. Compute Spearman correlation between experimental growth yield on glucose and in silico predictions for each constraint scenario, reporting p-values to validate that constraint integration improves predictive accuracy. Identify the constraint combination that yields the best inter-sample segregation and strongest experimental correlation as the optimal regulatory model.

## Related tools

- **optGpSampler** (Uniform sampling algorithm for generating steady-state flux distributions from the null space of the stoichiometric matrix under constraints)
- **COBRApy** (Python package for loading, manipulating, and solving constraint-based metabolic models; used to set bounds, execute FVA, and prepare models for sampling) — https://github.com/opencobra/cobrapy
- **Flux Variability Analysis (FVA)** (Identifies minimum and maximum flux ranges for each reaction under constraints; used to normalize flux scales relative to maximum identified flux)
- **t-SNE** (Dimensionality reduction algorithm for projecting high-dimensional flux distribution matrices into 2D for visual segregation assessment)
- **YSI bioanalyzer (YSI2950)** (Enzymatic quantification of extracellular metabolites (glucose, lactate, glutamine, glutamate) for constraint derivation)

## Examples

```
python pipeline/randomSampling.py 10000 1 --biomassRxn Biomass --lcellLines MCF102A MDAMB231 SKBR3 MCF7 MDAMB361 --modelId ENGRO2
```

## Evaluation signals

- t-SNE plots show clear, visually distinct clusters for each sample within the type 1+2+3 constraint scenario, with minimal overlap between clusters.
- Spearman correlation coefficient between experimental growth yield and in silico predictions is statistically significant (p < 0.05) and higher for the combined constraint scenario than for individual or paired constraint subsets.
- Intra-sample flux distribution variance (within-cluster spread in t-SNE space) decreases monotonically as constraint types are added sequentially (type 1 → type 1+2 → type 1+2+3), indicating tighter solution space confinement.
- Inter-sample flux distribution distances (between-cluster separation in t-SNE space) increase monotonically with cumulative constraint addition, demonstrating enhanced phenotypic discrimination.
- The number of steady-state solutions (feasible flux distributions) decreases and remains computationally tractable (≤10,000 sampled) as constraints accumulate, confirming that the constraint system progressively narrows the solution space without over-constraining.

## Limitations

- Enzymatic activity regulation and cofactor/prosthetic group effects are not captured; only substrate availability is considered via mass action law formulation, which may miss allosteric regulation or product inhibition.
- Limited metabolite coverage in metabolomics datasets constrains the number of reactions that can be analyzed in concordance studies; reactions with missing substrate quantification must be excluded.
- Computational visualization and statistical power limit sampling to 10,000 steady-state solutions per sample; larger sample sets may be needed for high-dimensional flux spaces or very constrained models.
- Uncertainty in experimental measurements (transcriptomics, metabolomics, phenotype data) and model inaccuracies can obscure agreement between predicted and observed regulatory mechanisms.

## Evidence

- [other] Type 1+2+3 constraints together achieve superior segregation of the five cell line flux distributions compared to individual or paired constraint applications, as demonstrated by t-SNE visualization showing decreased intra-model and increased inter-model separation of steady-state solutions.: "Type 1+2+3 constraints together achieve superior segregation of the five cell line flux distributions compared to individual or paired constraint applications, as demonstrated by t-SNE visualization"
- [other] Sample 10,000 steady-state flux distributions from the null space of the stoichiometric matrix for each cell line using uniform sampling: "Sample 10,000 steady-state flux distributions from the null space of the stoichiometric matrix for each cell line using uniform sampling (optGpSampler)"
- [other] Apply t-SNE dimensionality reduction to the sampled flux distributions to produce a two-dimensional map and visualize the segregation of the five cell lines.: "Apply t-SNE dimensionality reduction to the sampled flux distributions to produce a two-dimensional map and visualize the segregation of the five cell lines."
- [other] Compute the Spearman correlation coefficient between experimental and in silico growth yield on glucose for each constraint scenario and report p-values.: "Compute the Spearman correlation coefficient between experimental and in silico growth yield on glucose for each constraint scenario and report p-values."
- [results] For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted: "For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted"
- [intro] We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA: "We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA"
- [readme] nSamples: number of solutions to sample for each batch. Users may decided to leave the following inputs associated to their default values or set them as preferred: "nSamples: number of solutions to sample for each batch. Users may decided to leave the following inputs associated to their default values or set them as preferred"
- [readme] imposeYSI: 'Y' (yes) or 'N' (no) according to whether extracellular flux ratio constraints have to be integrated. Default value: 'Y'.: "imposeYSI: 'Y' (yes) or 'N' (no) according to whether extracellular flux ratio constraints have to be integrated. Default value: 'Y'."
