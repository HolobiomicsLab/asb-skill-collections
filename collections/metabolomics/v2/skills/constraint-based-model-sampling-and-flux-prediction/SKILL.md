---
name: constraint-based-model-sampling-and-flux-prediction
description: Use when you have constraint-based metabolic models with integrated multi-omics constraints (transcriptomics via Reaction Activity Scores, extracellular flux ratios via YSI bioanalyzer or LC-MS, nutrient availability bounds), and you need to determine whether differential enzyme expression.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - COBRApy (optGpSampler algorithm)
  - Flux Variability Analysis (FVA)
  - constraint-based stoichiometric metabolic models
  - YSI2950 bioanalyzer
  - INTEGRATE pipeline (qLSLab/integrate)
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions of the ENGRO2 model
- We performed a Flux Variability Analysis (FVA). FVA [67, 68] is a constraint-based modelling technique aimed at determining the maximal (and minimal) possible flux through any reaction
- using constraint-based stoichiometric metabolic models as a scaffold
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate
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

# constraint-based-model-sampling-and-flux-prediction

## Summary

Uniformly sample the feasible flux distribution of constraint-based metabolic models under multiple constraint scenarios (transcriptomics-derived, metabolomics-derived, and nutrient availability), then compute median fluxes and compare predicted growth yield against experimental measurements to assess which regulatory layers best explain observed metabolic phenotypes.

## When to use

You have constraint-based metabolic models with integrated multi-omics constraints (transcriptomics via Reaction Activity Scores, extracellular flux ratios via YSI bioanalyzer or LC-MS, nutrient availability bounds), and you need to determine whether differential enzyme expression, substrate availability, or both explain differences in growth yield or other flux-dependent phenotypes across cell lines or conditions.

## When NOT to use

- Your constraint-based models do not have multi-omics constraints integrated (i.e., transcriptomics-derived reaction bounds, extracellular flux ratio constraints, and nutrient availability bounds must all be pre-computed and applied).
- You have only a single constraint scenario (e.g., only a generic model or only one cell line model); this skill requires comparison across ≥2 scenarios to identify which regulatory layer explains phenotype variation.
- Your experimental growth yield data are missing or do not span the same cell lines or conditions modeled; without experimental validation, you cannot assess which in silico scenario best predicts biology.
- You are modeling dynamic or time-dependent metabolic behavior; this skill applies only to steady-state flux balance analysis and does not capture transient regulation.

## Inputs

- constraint-based metabolic models in SBML or MAT format with integrated constraint scenarios (Type 1: nutrient availability bounds; Type 2: extracellular flux ratio constraints; Type 3: transcriptomics-derived reaction flux bounds via normalized Reaction Activity Scores)
- experimental growth yield data (grams protein produced / grams glucose consumed over 48 hours) from Bradford protein assay and YSI bioanalyzer glucose quantification
- model reaction parameters: biomass reaction name, glucose uptake reaction ID, protein fraction of biomass (e.g., 0.131972)

## Outputs

- CSV files containing sampled flux solutions (1 million steady-state solutions per model per constraint scenario) with columns for each reaction flux
- in silico growth yield values (median protein synthesis flux / median glucose uptake flux, in grams/hour) for each cell line and constraint scenario
- Spearman rank correlation coefficients and two-tailed p-values comparing predicted vs. experimental growth yield for each constraint scenario
- correlation plot annotating Spearman ρ and p-value for all four scenarios, highlighting which constraint type (Type 1, 2, 3, or 1+2+3) best separates cell lines

## How to apply

Load constraint-based models with each constraint scenario applied separately and in combination (e.g., Type 1: nutrient availability only; Type 2: extracellular flux only; Type 3: transcriptomics-derived constraints only; Type 1+2+3: all combined). Use optGpSampler to uniformly sample the feasible flux region with 10 batches of 100,000 samples each (1 million total steady-state solutions per model per scenario), enforcing the biomass growth constraint (e.g., 0.001 · 0.131972 · v_Biomass ≤ v_ExGlc · mw_Glc). For each sample and scenario, compute the median protein synthesis flux divided by median glucose uptake flux, converting the flux ratio to grams/hour using the biomass protein fraction. Load experimental growth yield (protein produced / glucose consumed in grams/hour from Bradford assay and YSI analysis). Calculate Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico growth yield for each constraint scenario. Rank scenarios by Spearman ρ to identify which constraint layer best separates cell lines and best predicts experimental phenotype.

## Related tools

- **COBRApy (optGpSampler algorithm)** (Uniform sampling of the feasible flux region of constraint-based models; core algorithm for generating steady-state flux distributions under multiple constraint scenarios) — https://github.com/opencobra/cobrapy
- **Flux Variability Analysis (FVA)** (Determines minimum and maximum flux bounds for each reaction under defined constraints, used to support sampling and interpretation of flux variability across cell lines)
- **YSI2950 bioanalyzer** (Experimental quantification of glucose, lactate, glutamine, and glutamate in culture media; provides absolute extracellular flux measurements for model constraints and growth yield validation)
- **INTEGRATE pipeline (qLSLab/integrate)** (Upstream constraint generation: computes Reaction Activity Scores (RAS) from transcriptomics, normalizes RAS, integrates transcriptomics/metabolomics/extracellular flux constraints into models to generate cell-line-specific models for sampling) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/randomSampling.py 100000 10
```

## Evaluation signals

- Spearman ρ increases monotonically (or nearly so) as constraints are added cumulatively (Type 1 < Type 1+2 < Type 1+2+3), confirming that multi-layer constraint integration improves prediction accuracy.
- The constraint scenario with the highest Spearman ρ and lowest two-tailed p-value (typically p < 0.05) is the one that best explains growth yield variation across cell lines; verify this matches biological expectations (e.g., if transcriptomics-derived constraints alone best separate lines, gene expression dominates regulation).
- In silico growth yield values computed from sampled flux distributions show mean±SD ranges consistent with experimental yield estimates (e.g., experimental yield ≈ in silico median ± IQR), indicating model feasibility.
- Sampled flux distributions contain ≥1 million steady-state solutions per model per scenario, and the 1 million solutions converge to stable median flux values (verify by checking that subsamples of 500k and 1M yield nearly identical medians).
- Each constraint scenario produces distinct feasible flux regions (e.g., FVA bounds differ detectably between Type 1, Type 3, and Type 1+2+3), confirming that constraints are non-redundant and shape the solution space.

## Limitations

- Uniform sampling assumes all feasible flux distributions are equally probable; in reality, flux distributions may be weighted by thermodynamic or kinetic constraints not captured in the steady-state model.
- Transcriptomics-derived constraint integration via Reaction Activity Scores (RAS) requires complete GPR (gene-protein-reaction) rules in the model; reactions without GPR associations are omitted from RAS-based constraint application and cannot be assessed for transcriptional regulation.
- When a single intracellular metabolite is missing from metabolomics measurements, the entire reaction is omitted from metabolomics-derived constraint datasets, potentially biasing flux predictions for affected pathways.
- Direct determination of metabolic fluxes through labeled isotope tracing lags behind omic technologies and is not integrated into this pipeline; extracellular flux measurements (YSI bioanalyzer, LC-MS) are proxies for intracellular flux and may not fully capture intracellular regulation.
- Steady-state assumption may not hold during early exponential growth or transition phases; the skill applies only when cell culture has reached quasi-steady state (e.g., constant cell size and balanced protein/cell number correlation over 48 hours, as confirmed in the validation data).

## Evidence

- [other] For each of the four constraint scenarios, uniformly sample the feasible flux region of each model using optGpSampler with 10 batches of 100,000 samples each (1 million total steady-state solutions per model per scenario): "uniformly sample the feasible flux region of each model using optGpSampler with 10 batches of 100,000 samples each (1 million total steady-state solutions per model per scenario)"
- [other] Compute the median protein synthesis flux divided by median glucose uptake flux (in silico growth yield) for each cell line under each scenario, converting flux ratio to grams/hour using the biomass protein fraction (0.131972): "Compute the median protein synthesis flux divided by median glucose uptake flux (in silico growth yield) for each cell line under each scenario, converting flux ratio to grams/hour using the biomass"
- [other] Calculate Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico growth yield for each constraint scenario: "Calculate Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico growth yield for each constraint scenario"
- [other] Transcriptomics-derived constraints alone (Type 3) result in good separation of feasible flux distributions and better discrimination of growth rates across five cell lines, with further improvement when extracellular flux constraints (Type 1+2) are simultaneously applied: "Transcriptomics-derived constraints alone (Type 3) result in good separation of feasible flux distributions and better discrimination of growth rates across five cell lines"
- [intro] we set flux boundaries as a function of gene expression as done, among others, by eFlux [36] and TRFBA: "we set flux boundaries as a function of gene expression as done, among others, by eFlux"
- [intro] INTEGRATE exploits constraint-based modeling to predict how the global relative differences in expression are expected to translate into consistent differences in metabolic fluxes: "INTEGRATE exploits constraint-based modeling to predict how the global relative differences in expression are expected to translate into consistent differences in metabolic fluxes"
- [results] When a single reaction substrate is missing from metabolomics measurements, the reaction is omitted from the dataset: "When a single reaction substrate is missing from metabolomics measurements, the reaction is omitted from the dataset"
- [results] Between 0 and 48 hours, the protein content linearly correlates with the number of cells: "Between 0 and 48 hours, the protein content linearly correlates with the number of cells"
