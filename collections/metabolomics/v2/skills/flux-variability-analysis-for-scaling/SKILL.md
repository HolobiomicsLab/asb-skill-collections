---
name: flux-variability-analysis-for-scaling
description: Use when you have a constraint-based metabolic model and need to establish per-reaction flux scaling factors derived from gene expression or other activity scores. Use FVA before integrating transcriptomics-derived constraints (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - Flux Variability Analysis
  - eFlux
  - TRFBA
  - scFBA
  - GX-FBA
  - optGpSampler
  - COBRApy
  - GLPK (GNU Linear Programming Kit)
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA
- we set flux boundaries as a function of gene expression as done, among others, by eFlux [36] and TRFBA
- We used relative gene-expression values as in GX-FBA
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions
- In this work, we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72]
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

# Flux Variability Analysis for Scaling

## Summary

FVA determines the minimum and maximum steady-state flux through each internal reaction in a constraint-based metabolic model under specified nutrient and extracellular constraints, providing the reference flux bounds needed to scale reaction-specific activity scores into feasible flux boundaries for downstream sampling.

## When to use

Apply this skill when you have a constraint-based metabolic model and need to establish per-reaction flux scaling factors derived from gene expression or other activity scores. Use FVA before integrating transcriptomics-derived constraints (e.g., RAS scores) so that activity-weighted bounds remain anchored to the stoichiometric feasible region. Essential when preparing cell-specific models for uniform null-space sampling to generate feasible flux distributions.

## When NOT to use

- When the model is already reaction-specific or tissue-specific and does not require cell-line-relative scaling (FVA results would be redundant with existing bounds).
- When no extracellular metabolomics or nutrient availability data are available; FVA bounds will be overly broad and scaling by expression alone may not improve predictive power.
- When the goal is to identify individual reaction knockout effects or sensitivity analysis; use single reaction deletion or sensitivity analysis tools instead.

## Inputs

- Generic constraint-based metabolic model (SBML or COBRApy format)
- Nutrient availability constraints (lower and upper bounds for exchange reactions)
- Extracellular flux ratio constraints (e.g., lactate/glucose, glutamine/glucose ratios from exo-metabolomics)

## Outputs

- Cell-line-specific FVA minimum and maximum flux bounds (v_L,r^c and v_U,r^c) per internal reaction
- Tabular file mapping reaction ID to min/max flux for each cell line, used as input to RAS-weighted bound scaling

## How to apply

Run Flux Variability Analysis on the generic metabolic model (e.g., ENGRO2) under type 1 and type 2 constraints (nutrient availability and extracellular flux ratios, respectively) for each cell line or sample condition. FVA solves two linear programming problems per reaction: one maximizing flux, one minimizing flux, to identify v_L,r^c (lower bound) and v_U,r^c (upper bound) for each internal reaction r in cell c. These FVA bounds then serve as the scaling reference: when an activity score (RAS_r^c) is computed from gene expression via GPR logic, the scaled bounds become RAS_r^c × v_L,r^c ≤ v_r^c ≤ RAS_r^c × v_U,r^c. Reactions without associated GPRs retain symmetric FVA bounds. This two-level constraint (FVA baseline + RAS multiplier) ensures that expression-based flux predictions remain within the stoichiometric and metabolic feasible space.

## Related tools

- **COBRApy** (Python constraint-based modeling toolkit used to load metabolic models and execute FVA via linear programming solvers (GLPK).) — https://github.com/opencobra/cobrapy
- **GLPK (GNU Linear Programming Kit)** (Solver backend for linear programming problems in FVA optimization.) — https://www.gnu.org/software/glpk/

## Examples

```
python pipeline/rasIntegration.py --imposeRasConstraints Y --rasNormFileName ENGRO2_wNormalizedRAS.csv --modelId ENGRO2
```

## Evaluation signals

- FVA bounds are finite (not unbounded ±∞) for all internal reactions, indicating valid stoichiometric constraints.
- Lower bounds ≤ 0 and upper bounds ≥ 0 for reversible reactions; lower bounds = 0 and upper bounds ≥ 0 for irreversible reactions (or vice versa); bounds follow reaction directionality.
- When RAS scores (0 to 1) are applied: scaled bounds RAS × v_L ≤ v_r^c ≤ RAS × v_U remain within the original FVA interval [v_L, v_U] for each reaction (verify no bound inversion).
- Subsequent uniform sampling of the constrained null space produces steady-state solutions (flux vectors) that satisfy all FVA and RAS-weighted bounds and mass-balance equations.
- Distribution of sampled fluxes across 1 million solutions shows continuous occupancy within FVA bounds, not clustering at artificial barriers.

## Limitations

- FVA assumes steady-state assumption and linear stoichiometry; does not account for enzyme kinetics, allosteric regulation, cofactor/prosthetic group availability, or product inhibition (acknowledged in the article).
- FVA bounds depend critically on the accuracy and completeness of the input model topology and the nutrient/extracellular constraints; missing or incorrectly specified constraints can propagate into spurious scaling factors.
- When metabolomics coverage is limited (few intracellular metabolites quantified), reactions with unmeasured substrates cannot be reliably constrained downstream, reducing the effective number of reactions that benefit from FVA-derived scaling.
- FVA is computationally expensive for large models; each reaction requires two LP solves, and scaling across cell lines multiplies this cost.

## Evidence

- [other] Perform Flux Variability Analysis (FVA) on ENGRO2 with type 1 and type 2 constraints (nutrient availability and extracellular flux ratios) to determine the maximum and minimum flux through each internal reaction for each cell line.: "Perform Flux Variability Analysis (FVA) on ENGRO2 with type 1 and type 2 constraints (nutrient availability and extracellular flux ratios) to determine the maximum and minimum flux through each"
- [other] For each reaction r in cell c, the lower and upper flux bounds are constrained as: RAS_r^c × v_L,r^c ≤ v_r^c ≤ RAS_r^c × v_U,r^c, where v_L,r^c and v_U,r^c are cell-specific FVA-determined bounds.: "the lower and upper flux bounds are constrained as: RAS_r^c × v_L,r^c ≤ v_r^c ≤ RAS_r^c × v_U,r^c, where v_L,r^c and v_U,r^c are cell-specific FVA-determined bounds."
- [intro] We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA.: "We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA"
- [other] ensuring reactions without GPRs use symmetric FVA bounds: "ensuring reactions without GPRs use symmetric FVA bounds"
- [readme] The Pipeline was tested using GLPK solver: "The Pipeline was tested using GLPK solver (https://www.gnu.org/software/glpk/)."
