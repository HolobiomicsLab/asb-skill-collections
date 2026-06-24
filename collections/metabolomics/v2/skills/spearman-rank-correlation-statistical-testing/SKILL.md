---
name: spearman-rank-correlation-statistical-testing
description: Use when you have paired in silico and experimental measurements from
  multiple biological samples (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_2269
  tools:
  - COBRApy (optGpSampler algorithm)
  - COBRApy
  - scipy.stats.spearmanr
  - matplotlib/seaborn
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72], and we sampled a million steady state solutions of the ENGRO2 model
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

# spearman-rank-correlation-statistical-testing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute Spearman rank correlation coefficient and two-tailed p-value to quantify monotonic association between two ranked variables (e.g., predicted vs. experimental phenotypes). Used to validate whether constraint-based model predictions discriminate biological samples and correlate with experimental measurements.

## When to use

Apply this skill when you have paired in silico and experimental measurements from multiple biological samples (e.g., five cell lines) and need to assess whether a constraint scenario (transcriptomics-derived, metabolomics-derived, or combined) produces predicted values that rank-correlate with experimental ground truth. Appropriate when data may violate normality assumptions or contain outliers, and when you want to test whether one constraint scenario achieves better separation and discrimination of sample phenotypes than another.

## When NOT to use

- Input data contain fewer than 5 samples (Spearman ρ becomes unstable with n < 5).
- Predicted and experimental values are already known to be from normally distributed populations with homogeneous variance and no outliers; Pearson correlation may be more powerful in that case.
- Data contain tied ranks in both variables that dominate the sample set; consider reporting Kendall's τ as a sensitivity check.

## Inputs

- Predicted phenotype values (median or aggregated per sample from constraint-based model sampling)
- Experimental phenotype measurements (e.g., growth yield in grams/hour, from Bradford protein assay and YSI glucose/lactate analysis)
- Sample identifiers (e.g., cell line names: MCF102A, MDAMB231, SKBR3, MCF7, MDAMB361)

## Outputs

- Spearman rank correlation coefficient (ρ) per constraint scenario
- Two-tailed p-value per constraint scenario
- Correlation plot with ρ and p-value annotations for all constraint scenarios
- Comparative assessment of which constraint scenario achieves highest correlation and best phenotypic discrimination

## How to apply

Compute the median of a predicted metric (e.g., in silico growth yield derived from 1 million sampled steady-state flux distributions per model per constraint scenario) for each sample. Load experimental measurements of the same metric (e.g., growth yield from Bradford assay and YSI analysis over 48 h). For each constraint scenario, calculate the Spearman rank correlation coefficient ρ between the experimental and predicted values across all samples, along with the two-tailed p-value. Generate a correlation plot annotating both ρ and p-value for all constraint scenarios to highlight which scenario achieves the highest overall correlation while best separating the samples. The workflow requires paired sample-level data (not replicate-level): use median or mean aggregated values to represent each sample's in silico prediction and corresponding experimental measurement.

## Related tools

- **COBRApy** (Flux sampling and constraint-based metabolic modeling to generate in silico predictions that serve as input to correlation analysis) — https://github.com/opencobra/cobrapy
- **scipy.stats.spearmanr** (Python function to compute Spearman rank correlation coefficient and two-tailed p-value) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html
- **matplotlib/seaborn** (Plotting library to generate correlation scatter plots with ρ and p-value annotations)

## Examples

```
from scipy.stats import spearmanr; rho, p_value = spearmanr(experimental_growth_yield, in_silico_growth_yield); print(f'Spearman ρ={rho:.3f}, p={p_value:.4e}')
```

## Evaluation signals

- Spearman ρ increases monotonically across constraint scenarios (Type 3 alone > Type 1+2 alone; Type 1+2+3 combined ≥ all individual scenarios).
- Two-tailed p-value is < 0.05 for the best-performing constraint scenario, indicating statistically significant rank correlation.
- Scatter plot of predicted vs. experimental values shows clear monotonic trend with no severe outlier leverage; residuals show no systematic pattern.
- Number of samples in each constraint scenario matches input sample count (e.g., 5 for breast cell lines); no missing or duplicate entries.
- Median in silico values are derived from ≥ 1 million sampled steady-state flux solutions per model per scenario to ensure robust central tendency estimate.

## Limitations

- Spearman correlation requires at least 5 samples to be statistically meaningful; with fewer samples, confidence intervals widen and p-values lose power.
- The metric used (e.g., growth yield) must be directly comparable between in silico (flux-derived) and experimental (assay-derived) measurements; unit conversion and biomass protein fraction (0.131972 in ENGRO2) must be applied consistently.
- Correlation does not imply causality: a high ρ means predictions rank-order samples consistently with experiments, but does not validate the biochemical mechanisms or constraint logic.
- If experimental measurements contain large systematic errors or missing replicates, correlation quality depends on data quality; averaging biological replicates before correlation improves robustness.
- Tied ranks (identical values in predicted or experimental data) reduce effective sample size for correlation; report the number of tied pairs in the output.

## Evidence

- [other] Calculate Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico growth yield for each constraint scenario.: "Calculate Spearman rank correlation coefficient and two-tailed p-value between experimental and in silico growth yield for each constraint scenario."
- [other] Compute the median protein synthesis flux divided by median glucose uptake flux (in silico growth yield) for each cell line under each scenario, converting flux ratio to grams/hour using the biomass protein fraction (0.131972).: "Compute the median protein synthesis flux divided by median glucose uptake flux (in silico growth yield) for each cell line under each scenario, converting flux ratio to grams/hour using the biomass"
- [other] Load experimental growth yield data (protein produced over 48h / glucose consumed over 48h, in grams/hour from Bradford assay and YSI analysis in S1 File).: "Load experimental growth yield data (protein produced over 48h / glucose consumed over 48h, in grams/hour from Bradford assay and YSI analysis in S1 File)."
- [other] Generate a correlation plot (matching Fig 3E) with Spearman ρ and p-value annotations for all four scenarios, highlighting that Type 3 constraints alone best separate the five cell lines while Type 1+2+3 yields the highest overall correlation.: "Generate a correlation plot (matching Fig 3E) with Spearman ρ and p-value annotations for all four scenarios, highlighting that Type 3 constraints alone best separate the five cell lines while Type"
- [other] uniformly sample the feasible flux region of each model using optGpSampler with 10 batches of 100,000 samples each (1 million total steady-state solutions per model per scenario): "uniformly sample the feasible flux region of each model using optGpSampler with 10 batches of 100,000 samples each (1 million total steady-state solutions per model per scenario)"
