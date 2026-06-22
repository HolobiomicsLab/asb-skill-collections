---
name: statistical-power-analysis
description: Use when you have implemented or obtained a statistical method (e.g., PaIRKAT) and need to quantify its statistical power—the probability of correctly rejecting a false null hypothesis—across a range of realistic experimental scenarios before applying it to real data or publishing results.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_2269
  - http://edamontology.org/topic_0634
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
---

# statistical-power-analysis

## Summary

Execute power simulation scripts to compute statistical power across tested scenarios and generate summary statistics for a statistical method. This skill validates whether a method achieves adequate power under varying sample sizes, effect sizes, or other experimental conditions.

## When to use

You have implemented or obtained a statistical method (e.g., PaIRKAT) and need to quantify its statistical power—the probability of correctly rejecting a false null hypothesis—across a range of realistic experimental scenarios before applying it to real data or publishing results.

## When NOT to use

- The statistical method has not yet been implemented or is not executable in your environment.
- You only need Type I error rates (false positive rates) rather than power; use Type I error simulation instead.
- You are analyzing empirical data directly and do not need pre-study power planning.

## Inputs

- Power simulation script (e.g., R script from SimulationFunctions)
- Method implementation or package (e.g., PaIRKAT functions)
- Simulation parameters: sample sizes, effect sizes, significance level (alpha)
- Number of simulation replicates

## Outputs

- Power estimates (probability of rejection) by scenario
- Summary statistics table (power by condition)
- Validation report comparing simulated power to expected or published values

## How to apply

Locate and load the power simulation script from the method's repository (e.g., SimulationFunctions in PaIRKAT). Execute the script in the appropriate runtime environment (R for PaIRKAT) with specified parameters for sample sizes, effect sizes, significance levels, and other experimental configurations. The simulation generates power estimates by repeatedly sampling from the null and alternative hypotheses and recording rejection rates across conditions. Collect all generated power summary statistics and validate them against published or expected values to confirm correct implementation.

## Related tools

- **PaIRKAT** (Statistical method package containing the power simulation script) — https://github.com/CharlieCarpenter/PaIRKAT
- **R** (Execution environment for the power simulation scripts)

## Examples

```
source('SimulationFunctions.R'); power_results <- run_power_simulation(n_samples=c(50,100,200), effect_size=0.5, alpha=0.05, n_replicates=1000)
```

## Evaluation signals

- Power summary statistics (e.g., power table by sample size and effect size) are successfully generated without runtime errors.
- Generated power values fall within plausible ranges (0–1) and show monotonic increase with sample size for fixed effect size.
- Simulated power estimates match or closely approximate published or expected power values for the method.
- Sensitivity to input parameters is as documented: power increases with sample size, effect size, and decreases with stringency (alpha).
- Replicate simulations produce consistent results (low variance in point estimates across multiple runs with identical parameters).

## Limitations

- Power simulation is computationally intensive and may require substantial runtime for large numbers of replicates or many parameter combinations.
- Results depend critically on correct specification of the data generation model and parameter distributions; misspecification of effect size or design can yield misleading power estimates.
- No changelog is documented in the repository, making it difficult to track changes to simulation algorithms across versions.
- Power estimates are specific to the assumed data-generating process and may not generalize to real data with different distributional properties or departures from assumptions.

## Evidence

- [other] Execute the power simulation script to compute statistical power across tested scenarios and generate summary statistics.: "Execute the power simulation script to compute statistical power across tested scenarios and generate summary statistics."
- [readme] Type I error and power simulation scripts are available in the repository: "TypeI and Power simulation scripts"
- [other] Collect and validate all generated simulation summary outputs against reported values: "Collect and validate all generated simulation summary outputs against reported values."
- [readme] Scripts for PaIRKAT functions with example work flow are provided: "Scripts for PaIRKAT functions with example work flow"
