---
name: correlation-analysis-between-experimental-computational-data
description: Use when you have paired experimental and computational predictions for
  the same biological property (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_2258
  tools:
  - COBRApy (optGpSampler algorithm)
  - Flux Variability Analysis (FVA)
  - Spearman rank correlation test (scipy.stats or equivalent)
  - Matplotlib or equivalent visualization library
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72], and we sampled a million steady state solutions of the ENGRO2 model
- We performed a Flux Variability Analysis (FVA). FVA [67, 68] is a constraint-based
  modelling technique aimed at determining the maximal (and minimal) possible flux
  through any reaction
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# correlation-analysis-between-experimental-computational-data

## Summary

Quantify agreement between experimental measurements and in silico predictions by computing rank-based correlation coefficients and statistical significance tests, then visualize results to assess how well computational constraints discriminate biological samples. This validates whether integrating transcriptomics, metabolomics, or flux constraints improves model predictive power.

## When to use

You have paired experimental and computational predictions for the same biological property (e.g., growth yield, metabolic flux ratios) across multiple samples or conditions, and you want to assess whether adding constraint types (transcriptomics-derived, extracellular flux, nutrient availability) meaningfully improves the model's ability to discriminate between samples or predict absolute values.

## When NOT to use

- Input data contain only a single sample or fewer than three samples per group (correlation requires sufficient variance and N for statistical power).
- Experimental and computational predictions are already on different scales with no known stoichiometric or measurement conversion factor (e.g., flux in mmol/gDW/h vs. protein in mg — conversion via biomass protein fraction or similar must be available or manually determined).
- You are comparing qualitative categories (e.g., 'upregulated' vs. 'downregulated') rather than continuous or rank-orderable numerical values.

## Inputs

- Experimental measurement table (rows = samples, columns = biological properties; e.g., growth yield in grams/hour from Bradford + YSI assay over 48 hours)
- In silico prediction table (rows = samples, columns = same properties; e.g., median in silico growth yield from optGpSampler results, in grams/hour)
- Constraint scenario labels (e.g., 'Type 1 only', 'Type 2 only', 'Type 3 only', 'Type 1+2+3')

## Outputs

- Spearman rank correlation coefficient (ρ) per constraint scenario
- Two-tailed p-value per constraint scenario
- Correlation scatter plot with all scenarios overlaid or paneled, annotated with ρ and p-value per scenario
- Ranked comparison of constraint scenarios by correlation strength

## How to apply

Load experimental data (e.g., protein produced over time / glucose consumed, measured via Bradford assay and YSI bioanalyzer) and in silico predictions (e.g., median protein synthesis flux / median glucose uptake flux from 1 million sampled steady-state solutions per model per constraint scenario). Convert in silico flux ratios to the same units as experimental data using stoichiometric coefficients (e.g., biomass protein fraction = 0.131972). Compute Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico values for each constraint scenario separately. Generate a correlation scatter plot annotated with ρ and p-value for all scenarios, highlighting which constraint combination achieves both best sample discrimination (separation of points) and highest overall correlation.

## Related tools

- **COBRApy (optGpSampler algorithm)** (Generate large ensembles of steady-state flux distributions (1 million samples per model per scenario) to compute median in silico predictions for correlation against experimental data) — https://github.com/opencobra/cobrapy
- **Spearman rank correlation test (scipy.stats or equivalent)** (Compute rank-based correlation coefficient and p-value between paired experimental and in silico data, robust to non-linear relationships and outliers)
- **Matplotlib or equivalent visualization library** (Generate scatter plots of experimental vs. in silico predictions, annotated with ρ and p-value for each constraint scenario)

## Examples

```
from scipy.stats import spearmanr; rho, pval = spearmanr(experimental_growth_yield, in_silico_growth_yield); print(f'Spearman ρ={rho:.3f}, p={pval:.4f}')
```

## Evaluation signals

- Spearman ρ increases monotonically or plateaus as constraint types are added (Type 3 alone > Type 1+2 alone; Type 1+2+3 ≥ any subset), indicating that constraints are not redundant and do improve discrimination.
- Two-tailed p-value is < 0.05 for at least the highest-ρ scenario, confirming statistical significance of the correlation.
- Scatter plot shows clear visual separation of samples along the experimental–in silico diagonal for the best-performing constraint scenario, with minimal off-diagonal scatter (residuals).
- Median in silico values fall within the biological range of experimental values (no systematic bias toward extreme high or low predictions).
- Correlation is computed only on samples where all measurements (experimental and in silico) are present; missing or NaN values are excluded or reported.

## Limitations

- Spearman correlation assumes monotonic but not necessarily linear relationship; it may mask systematic bias (e.g., systematic over- or under-prediction) even if ranks match well.
- Median flux from sampling may obscure multi-modal or highly variable feasible regions; if the feasible region is very large, median may not be representative of the true steady state.
- Correlation is sensitive to outlier samples or measurement errors; robust estimation (e.g., percentile-based or trimmed correlation) is not discussed.
- Direct determination of metabolic fluxes through labeled substrates remains the gold standard but lags behind omic technologies; experimental data here are indirect proxies (protein accumulation, nutrient depletion) rather than true flux measurements.
- When a single reaction substrate is missing from metabolomics measurements, the reaction is omitted from the dataset, potentially biasing the constraint set and downstream correlations.

## Evidence

- [other] Calculate Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico growth yield for each constraint scenario.: "Calculate Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico growth yield for each constraint scenario"
- [other] Compute the median protein synthesis flux divided by median glucose uptake flux (in silico growth yield) for each cell line under each scenario, converting flux ratio to grams/hour using the biomass protein fraction (0.131972).: "Compute the median protein synthesis flux divided by median glucose uptake flux (in silico growth yield) for each cell line under each scenario, converting flux ratio to grams/hour using the biomass"
- [other] Load experimental growth yield data (protein produced over 48h / glucose consumed over 48h, in grams/hour from Bradford assay and YSI analysis in S1 File).: "Load experimental growth yield data (protein produced over 48h / glucose consumed over 48h, in grams/hour from Bradford assay and YSI analysis in S1 File)"
- [other] Generate a correlation plot (matching Fig 3E) with Spearman ρ and p-value annotations for all four scenarios, highlighting that Type 3 constraints alone best separate the five cell lines while Type 1+2+3 yields the highest overall correlation.: "Generate a correlation plot (matching Fig 3E) with Spearman ρ and p-value annotations for all four scenarios, highlighting that Type 3 constraints alone best separate the five cell lines while Type"
- [other] uniformly sample the feasible flux region of each model using optGpSampler with 10 batches of 100,000 samples each (1 million total steady-state solutions per model per scenario): "uniformly sample the feasible flux region of each model using optGpSampler with 10 batches of 100,000 samples each (1 million total steady-state solutions per model per scenario)"
