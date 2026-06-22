---
name: steady-state-solution-uniform-sampling
description: Use when when you have a constraint-based metabolic model with cell-specific flux boundaries (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - eFlux
  - TRFBA
  - scFBA
  - GX-FBA
  - optGpSampler
  - COBRApy
  - GLPK solver
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we set flux boundaries as a function of gene expression as done, among others, by eFlux [36] and TRFBA
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA
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
---

# Steady-state solution uniform sampling

## Summary

Uniformly sample the feasible flux region of a constraint-based metabolic model to generate a large ensemble of steady-state flux distributions. This produces a probabilistic representation of all metabolically feasible solutions under the given constraints, enabling statistical characterization of flux variability across reactions and biological conditions.

## When to use

When you have a constraint-based metabolic model with cell-specific flux boundaries (e.g., from RAS-scaled FVA bounds, exo-metabolomics constraints, and nutrient availability data) and need to move beyond point predictions (single optimizations) to capture the full landscape of feasible flux distributions for downstream concordance analysis or flux variability characterization across multiple cell lines or conditions.

## When NOT to use

- Model has no or very few active constraints—sampling from an unconstrained or poorly constrained null space will produce uninformative, highly dispersed flux distributions that do not reflect biological reality.
- Input model is already in irreversible form and reversible reactions have been pre-split—re-splitting will create duplicate and contradictory reaction pairs.
- Only a single optimal flux solution is needed (e.g., for stoichiometric balance checking or flux balance analysis); sampling is unnecessary overhead in this case.

## Inputs

- Irreversible-format constraint-based metabolic model (SBML or MAT file) with RAS-dependent flux boundaries applied
- Nutrient availability constraints (lower and upper bounds per cell line)
- Extracellular flux ratio constraints (YSI or equivalent exo-metabolomics data)
- Biomass reaction name and minimum viable biomass threshold (epsilon)

## Outputs

- Feasible flux distribution (FFD) dataset: CSV files containing nSamples × nReactions matrix of sampled flux values per cell line and batch
- Steady-state solution ensemble: 1 million feasible flux vectors per cell line satisfying all stoichiometric, thermodynamic, and biological constraints

## How to apply

Convert the constrained stoichiometric metabolic model to irreversible form by splitting reversible reactions into forward and backward variants. Then apply uniform sampling to the constrained null space using optGpSampler with a thinning value of 10 to generate steady-state solutions while maintaining the growth yield constraint (biomass ≥ epsilon, typically 1e-4). Generate samples in batches (e.g., 10 batches of 100,000 solutions each for 1 million total) to balance computational tractability with ensemble representativeness. Export the resulting flux distributions (flux values across all reactions for each sampled solution per cell line) as CSV datasets for subsequent statistical tests (e.g., Mann-Whitney U) and concordance analysis comparing predicted flux variation (FFD) against substrate-availability-driven flux prediction (RPS) and transcriptionally regulated flux prediction (RAS).

## Related tools

- **optGpSampler** (Uniformly samples the constrained null space of the stoichiometric matrix; core algorithm for generating steady-state flux distributions while respecting all imposed constraints and maintaining growth yield.)
- **COBRApy** (Python toolkit for constraint-based model manipulation, format conversion (reversible to irreversible), and integration with optGpSampler sampling routines.)
- **GLPK solver** (Linear programming backend used during model constraint enforcement and sampling validation.) — https://www.gnu.org/software/glpk/

## Examples

```
python pipeline/randomSampling.py 100000 10
```

## Evaluation signals

- Sampled flux vectors satisfy stoichiometric constraints (S × v = 0 within numerical tolerance) and all imposed flux bounds for each reaction and cell line.
- All sampled solutions maintain non-negative biomass production (biomass flux ≥ epsilon) as specified in the growth yield constraint.
- Ensemble statistics (mean, variance, percentiles) of flux distributions show clear cell-line-specific patterns consistent with their transcriptomics and metabolomics profiles (e.g., cancer lines with higher lactate production rates than normal lines).
- Concordance analysis between FFD and independent predictions (RPS from mass action, RAS from transcriptomics) yields reasonable Cohen's kappa and Pearson correlation coefficients; reactions with concordance > 0.2 are retained for interpretation.
- Sample size is sufficient: visualization and statistical tests are computationally tractable; 10,000 subsampled solutions represent the full 1 million-solution ensemble without significant loss of distribution shape (confirmed by KS test or Jensen-Shannon divergence).

## Limitations

- Uniform sampling assumes all feasible solutions are equally likely metabolically, but does not account for enzyme kinetics, allosteric regulation, or product inhibition—these regulatory mechanisms are not discriminable from sampling alone without additional experimental constraints.
- Limited metabolite coverage in the metabolomics dataset constrains which reactions can be meaningfully evaluated; reactions with missing substrate abundances are excluded from concordance analysis, reducing the effective size of the analyzable reaction set.
- Sampling is computationally intensive (1 million solutions × 5 cell lines × multiple statistical replicates); for visualization and exploratory analysis, only a 10,000-solution subsample is typically plotted, which may obscure rare tail distributions or low-frequency modes.
- Thinning value (default 10) is fixed empirically; suboptimal thinning can lead to correlated samples that artificially inflate ensemble concordance or underestimate variance.

## Evidence

- [other] Uniformly sample the constrained null space of the stoichiometric matrix for each cell line using optGpSampler with thinning value 10, generating 1 million total steady-state solutions (10 batches of 100,000 each) while maintaining the growth yield constraint.: "Uniformly sample the constrained null space of the stoichiometric matrix for each cell line using optGpSampler with thinning value 10, generating 1 million total steady-state solutions (10 batches of"
- [other] Convert each constrained model to irreversible form by splitting reversible reactions into forward and backward variants.: "Convert each constrained model to irreversible form by splitting reversible reactions into forward and backward variants."
- [results] For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted: "For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted"
- [other] RAS-dependent flux boundaries for each reaction in each cell line as: lower bound = RAS × FVA_min, upper bound = RAS × FVA_max, ensuring reactions without GPRs use symmetric FVA bounds: "Set RAS-dependent flux boundaries for each reaction in each cell line as: lower bound = RAS × FVA_min, upper bound = RAS × FVA_max, ensuring reactions without GPRs use symmetric FVA bounds"
- [other] Export the FFD datasets (flux distributions across all sampled solutions for each cell line) for downstream concordance analysis.: "Export the FFD datasets (flux distributions across all sampled solutions for each cell line) for downstream concordance analysis."
- [readme] python pipeline/randomSampling.py nSamples nBatches: "python pipeline/randomSampling.py nSamples nBatches"
