---
name: metabolic-model-constraint-application
description: Use when when you have a generic constraint-based metabolic model, RNA-seq expression data with GPR associations for reactions, experimentally measured nutrient uptake/secretion rates (from YSI bioanalyzer or similar), and intracellular/extracellular metabolomics data, and you need to generate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3674
  tools:
  - eFlux
  - TRFBA
  - scFBA
  - GX-FBA
  - constraint-based stoichiometric metabolic models
  - optGpSampler
  - COBRApy
  - Flux Variability Analysis (FVA)
  - GLPK solver
  - YSI bioanalyzer (YSI2950)
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we set flux boundaries as a function of gene expression as done, among others, by eFlux [36] and TRFBA
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA
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

# metabolic-model-constraint-application

## Summary

Integration of transcriptomics-derived Reaction Activity Scores (RAS), nutrient availability bounds, and exo-metabolomics flux ratio constraints into cell-relative constraint-based metabolic models to narrow the feasible solution space and enable prediction of cell-line-specific metabolic flux distributions.

## When to use

When you have a generic constraint-based metabolic model, RNA-seq expression data with GPR associations for reactions, experimentally measured nutrient uptake/secretion rates (from YSI bioanalyzer or similar), and intracellular/extracellular metabolomics data, and you need to generate cell-line-specific flux predictions that account for differential enzyme expression and substrate availability rather than relying on a single generic solution.

## When NOT to use

- Input model lacks GPR rules or the expression data genes do not map to the model — RAS computation will fail or assign RAS=1 to most reactions, negating the transcriptional control layer.
- No exo-metabolomics or nutrient flux measurements are available — nutrient availability constraints cannot be properly set, and the model will remain under-constrained relative to the biological system.
- Expression data is not normalized to the same scale across cell lines (e.g., raw counts instead of FPKM) — RAS normalization by maximum value will be biased and relative expression differences will not be preserved.

## Inputs

- Generic reversible constraint-based metabolic model (SBML or JSON format)
- RNA-seq FPKM abundance table with gene identifiers matching GPR rules
- Metabolic model with embedded Gene-Protein-Reaction (GPR) logical rules
- Nutrient availability constraints (uptake/secretion rate bounds from YSI bioanalyzer measurements, format: reaction ID, lower bound, upper bound per cell line)
- Exo-metabolomics flux ratio constraints (e.g., lactate-to-glucose, glutamine-to-glucose ratios from culture media measurements)
- List of cell line identifiers and biological replicate labels

## Outputs

- Cell-relative constraint-based metabolic models in SBML format (one per cell line), each with RAS-scaled bounds, nutrient constraints, and extracellular flux ratio constraints integrated
- Irreversible versions of constrained cell-relative models (reversible reactions split into forward and backward variants)
- Normalized RAS table (CSV): reaction ID, mean RAS per cell line, normalized RAS per cell line, and biological replicate averages

## How to apply

First, compute normalized Reaction Activity Scores (RAS) for each reaction in each cell line by resolving GPR logical expressions (minimum for AND-linked genes, sum for OR-linked genes) from RNA-seq FPKM data, then normalize by dividing by the maximum RAS across all cell lines. Second, perform Flux Variability Analysis (FVA) on the generic model with nutrient constraints to establish the baseline flux range (v_L, v_U) for each internal reaction. Third, apply three sequential constraint layers: (1) set nutrient availability bounds from exo-metabolomics measurements, (2) apply extracellular flux ratio constraints derived from YSI bioanalyzer data (e.g., lactate-to-glucose ratio), and (3) scale internal reaction bounds by RAS: lower bound = RAS × v_L, upper bound = RAS × v_U. Fourth, convert the constrained model to irreversible form (split reversible reactions into forward/backward pairs) and verify that the constrained feasible region is non-empty. The rationale is that RAS reflects transcriptional control, nutrient bounds reflect substrate availability control, and their combination captures both regulatory layers; reactions without GPRs retain symmetric FVA bounds (RAS = 1) as they are not transcriptionally regulated.

## Related tools

- **Flux Variability Analysis (FVA)** (Establish baseline lower and upper flux bounds for each internal reaction in the generic model before RAS scaling; essential first step to define the range that will be multiplied by RAS scores) — https://github.com/opencobra/cobrapy
- **COBRApy** (Python framework for loading, manipulating, and solving constraint-based metabolic models; used to perform FVA, set bounds, and validate model feasibility after constraint integration) — https://github.com/opencobra/cobrapy
- **GLPK solver** (Linear programming backend for solving flux balance optimization and FVA problems within COBRApy workflows) — https://www.gnu.org/software/glpk/
- **optGpSampler** (Uniform sampling of the constrained null space to generate feasible flux distributions after all constraints are applied; used downstream to validate that constrained models produce diverse steady-state solutions)
- **YSI bioanalyzer (YSI2950)** (Instrumental measurement of glucose, lactate, glutamine, and glutamate in fresh and spent culture media; provides exo-metabolomics data used to set extracellular flux ratio constraints)

## Examples

```
python pipeline/rasIntegration.py --imposeRasConstraints Y --imposeMedium Y --imposeYSI Y --rasNormFileName ENGRO2_wNormalizedRAS.csv --mediumFileName medium.csv --ysiFileName ysi_ratio.csv --modelId ENGRO2
```

## Evaluation signals

- All RAS values for GPR-associated reactions fall in [0, 1] after normalization; reactions without GPRs have RAS = 1.0 exactly.
- Constrained model feasible region is non-empty: at least one feasible steady-state solution exists that satisfies all three constraint layers (nutrient, extracellular ratio, RAS-scaled internal bounds).
- RAS-scaled bounds are tighter than baseline FVA bounds: for each reaction, lower_RAS ≥ lower_FVA and upper_RAS ≤ upper_FVA (because 0 ≤ RAS ≤ 1), except reactions with RAS=1 which retain FVA bounds.
- Biological replicate consistency: normalized RAS values computed from replicate samples within a cell line correlate (Pearson r > 0.8) when averaged; high variance across replicates signals measurement or computational error.
- Irreversible model validation: reversible reactions are correctly split; total reaction count increases; the irreversible model produces feasible solutions when sampled with optGpSampler (e.g., 10,000 steady-state samples per cell line with no convergence failures).

## Limitations

- RAS computation assumes GPR logic is accurately represented in the model; errors in GPR annotation (missing subunits, incorrectly modeled isoforms) propagate directly into RAS and biased flux predictions.
- Limited metabolite coverage in metabolomics data constrains the number of reactions for which intracellular substrate abundance can be used for post-hoc validation; reactions with missing substrate measurements must be excluded from concordance analysis.
- Enzymatic activity (allosteric regulation, product inhibition, cofactor effects) is not captured by RAS or substrate abundance alone; predicted fluxes may diverge from experimental fluxes when these mechanisms dominate.
- RAS normalization by maximum value across cell lines can mask absolute expression changes; if all cell lines have very low expression of a reaction, normalized RAS will appear to confer strong constraint when absolute control is weak.
- Extracellular flux ratio constraints assume steady state and linear relationship between uptake and secretion rates; time-dependent or nonlinear metabolic dynamics are not captured.

## Evidence

- [other] For each reaction r and each cell line c, resolve the GPR logical expression: for AND-linked genes, take the minimum transcript abundance value; for OR-linked genes, take the sum of transcript abundances; handle mixed AND/OR using standard precedence rules.: "For each reaction r and each cell line c, resolve the GPR logical expression: for AND-linked genes, take the minimum transcript abundance value; for OR-linked genes, take the sum of transcript"
- [other] RAS-dependent flux boundaries for each reaction in each cell line as: lower bound = RAS × FVA_min, upper bound = RAS × FVA_max, ensuring reactions without GPRs use symmetric FVA bounds.: "Set RAS-dependent flux boundaries for each reaction in each cell line as: lower bound = RAS × FVA_min, upper bound = RAS × FVA_max, ensuring reactions without GPRs use symmetric FVA bounds"
- [other] Apply all three constraint types (nutrient availability, extracellular flux ratios, and transcriptomics-derived flux boundaries) to each of the five cell-relative metabolic models.: "Apply all three constraint types (nutrient availability, extracellular flux ratios, and transcriptomics-derived flux boundaries) to each of the five cell-relative metabolic models"
- [results] Absolute quantification of glucose, lactate, glutamine, and glutamate in fresh medium at t = 0 and in spent media after 48 hours of growth was determined enzymatically using YSI2950 bioanalyzer: "Absolute quantification of glucose, lactate, glutamine, and glutamate in fresh medium at t = 0 and in spent media after 48 hours of growth was determined enzymatically using YSI2950 bioanalyzer"
- [intro] We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA: "We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA"
- [other] Uniformly sample the constrained null space of the stoichiometric matrix for each cell line using optGpSampler with thinning value 10, generating 1 million total steady-state solutions: "Uniformly sample the constrained null space of the stoichiometric matrix for each cell line using optGpSampler with thinning value 10, generating 1 million total steady-state solutions"
- [readme] imposeRasConstraints: 'Y' (yes) or 'N' (no) according to whether transcriptomics derived constraints have to be integrated.: "imposeRasConstraints: 'Y' (yes) or 'N' (no) according to whether transcriptomics derived constraints have to be integrated"
- [other] Convert each constrained model to irreversible form by splitting reversible reactions into forward and backward variants.: "Convert each constrained model to irreversible form by splitting reversible reactions into forward and backward variants"
