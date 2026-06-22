---
name: type-i-error-computation
description: Use when when you need to verify that reported Type I error rates from a statistical method (here, PaIRKAT) can be independently reproduced, or when you require baseline false positive rate estimates across multiple simulation conditions (sample sizes, effect configurations, significance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3524
  - http://edamontology.org/topic_3307
  tools:
  - R (or language used by PaIRKAT scripts)
  - PaIRKAT
  - R
derived_from:
- doi: 10.1101/2021.04.23.440821v1
  title: PaIRKAT
evidence_spans:
- Scripts for PaIRKAT functions with example work flow
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairkat_cq
    doi: 10.1101/2021.04.23.440821v1
    title: PaIRKAT
  dedup_kept_from: coll_pairkat_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2021.04.23.440821v1
  all_source_dois:
  - 10.1101/2021.04.23.440821v1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# type-i-error-computation

## Summary

Execute Type I error simulation scripts from the PaIRKAT repository to compute false positive rates and generate summary statistics across tested statistical scenarios. This skill validates the reproducibility of reported Type I error rates by regenerating simulation outputs.

## When to use

When you need to verify that reported Type I error rates from a statistical method (here, PaIRKAT) can be independently reproduced, or when you require baseline false positive rate estimates across multiple simulation conditions (sample sizes, effect configurations, significance thresholds) to benchmark a new method or validate published claims.

## When NOT to use

- When you do not have access to the PaIRKAT repository or its simulation code.
- When your goal is to estimate power (statistical sensitivity), not Type I error; use the power simulation script instead.
- When you already have pre-computed Type I error summaries and only need to interpret or report them without regeneration.

## Inputs

- PaIRKAT repository clone (R scripts)
- Type I error simulation script (SimulationFunctions module)
- Simulation parameters (sample sizes, significance levels, number of replications)
- Published or reference Type I error rates (for validation)

## Outputs

- Type I error rate estimates (empirical rejection proportions under null)
- Summary statistics table (by scenario: sample size, alpha level, observed error rate, standard error, confidence interval)
- Validation report (comparison of computed vs. reference rates)

## How to apply

Clone the PaIRKAT repository and locate the SimulationFunctions scripts containing Type I error simulation code. Load and execute the Type I error simulation script in R, which will iterate through specified scenarios (varying sample sizes, parameter configurations, and nominal significance levels) and compute the empirical proportion of rejections under the null hypothesis. Collect all generated summary statistics (e.g., observed error rates, confidence intervals, scenario metadata) and validate them against reported values in the article or supplementary materials by computing absolute differences and checking whether observed rates fall within expected Monte Carlo confidence intervals.

## Related tools

- **PaIRKAT** (Source repository containing Type I error simulation scripts and example workflows) — github.com/CharlieCarpenter/PaIRKAT
- **R** (Execution environment for running Type I error simulation scripts)

## Examples

```
source('SimulationFunctions/TypeI_simulation.R'); results <- run_typeI_simulation(n_sims=10000, sample_sizes=c(50,100,200), alpha=0.05); summary_stats <- aggregate_results(results); write.csv(summary_stats, 'typeI_error_results.csv')
```

## Evaluation signals

- Simulation completes without errors and produces numeric output for all specified scenarios.
- Summary statistics (observed Type I error rates) fall within expected 95% Monte Carlo confidence intervals around published reference rates.
- Absolute difference between reproduced and published Type I error rates is ≤ 0.01 (or within stated tolerance in methods).
- All output tables include required metadata columns (sample size, alpha level, number of replications, observed error rate).
- No NaN, infinite, or out-of-range values (error rates should be in [0, 1]) in the summary output.

## Limitations

- Reproducibility depends on fixed random seed; results may differ slightly across runs or platforms without seed control.
- No changelog documented in the repository, so it is unclear whether the deposited scripts reflect the exact code used in the original publication.
- Simulation runtime may be substantial for large numbers of replications or scenarios, requiring adequate computational resources.
- The skill reproduces only the Type I error rates reported; it does not validate the underlying statistical method logic or assumptions.

## Evidence

- [intro] Type I error and power simulation scripts are available in SimulationFunctions: "TypeI and Power simulation scripts"
- [intro] The repository provides scripts for executing the PaIRKAT method workflow: "Scripts for PaIRKAT functions with example work flow"
- [other] The workflow involves cloning the repository, locating scripts, executing simulations, and collecting outputs: "Locate and load the SimulationFunctions scripts containing Type I error and power simulation code. 3. Execute the Type I error simulation script to compute error rates and generate summary"
- [other] R is the required tool for executing the PaIRKAT simulation scripts: "tools: R (or language used by PaIRKAT scripts)"
