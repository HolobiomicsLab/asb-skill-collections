---
name: statistical-simulation-execution
description: Use when you have access to a published repository containing simulation scripts (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3315
  - http://edamontology.org/topic_3674
  tools:
  - R (or language used by PaIRKAT scripts)
  - R
  - PaIRKAT
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# statistical-simulation-execution

## Summary

Execute pre-built statistical simulation scripts to generate and validate Type I error rates and power estimates across tested scenarios. This skill reproduces computational results from a methodological repository by systematically running validated simulation code and collecting summary statistics.

## When to use

You have access to a published repository containing simulation scripts (e.g., PaIRKAT) and need to: (1) verify that published Type I error and power claims can be regenerated, (2) obtain simulation-based summary statistics for methodological validation, or (3) serve as a reference execution before adapting simulations for new parameters or study designs.

## When NOT to use

- The simulation scripts are not executable or dependencies are unavailable and cannot be resolved.
- You need to modify simulation parameters (effect sizes, sample sizes, test designs) — use script adaptation skills instead.
- The repository has no documented simulation scripts or the README does not clearly identify which files contain Type I error or power code.

## Inputs

- Repository clone or downloaded source code (e.g., github.com/CharlieCarpenter/PaIRKAT)
- Type I error simulation script (R or language-native)
- Power simulation script (R or language-native)
- Study design parameters embedded in or read by scripts (e.g., sample size, effect size, significance threshold)

## Outputs

- Type I error rate summary statistics (point estimates and confidence intervals)
- Statistical power estimates across tested scenarios
- Validation comparison table (generated vs. reported values)
- Simulation logs or diagnostic plots documenting convergence and coverage

## How to apply

Clone or download the target repository (e.g., github.com/CharlieCarpenter/PaIRKAT) and locate the designated simulation scripts (e.g., SimulationFunctions). Load and execute the Type I error simulation script to compute error rates and generate summary statistics across the predefined test scenarios. Then execute the power simulation script to compute statistical power under the same or related tested scenarios. Collect all generated outputs (numerical summaries, plots, or tables) and validate them against the reported values in the source article or repository documentation. Any discrepancies in summary statistics should be investigated for script modifications, dependency version changes, or random seed drift.

## Related tools

- **R** (Execution environment for Type I error and power simulation scripts)
- **PaIRKAT** (Repository containing validated simulation functions and workflows) — https://github.com/CharlieCarpenter/PaIRKAT

## Examples

```
# Source and execute Type I error simulation
source('PaIRKAT/SimulationFunctions/TypeISimulation.R')
run_typeI_simulation(n_replicates=10000, alpha=0.05)

# Source and execute power simulation
source('PaIRKAT/SimulationFunctions/PowerSimulation.R')
run_power_simulation(n_replicates=10000, effect_sizes=c(0.2, 0.5, 0.8))
```

## Evaluation signals

- Generated Type I error rates match reported values within expected Monte Carlo standard error (typically ±0.005–0.010 for 10,000+ replicates).
- Power estimates are monotonically increasing or stable across effect size and sample size scenarios as expected by statistical theory.
- All simulation output files are generated and contain non-null, numeric summary statistics with expected dimensionality.
- Random seed reproducibility check: re-running with the same seed produces identical summary statistics.
- No warnings or errors logged during script execution; any numerical edge cases (e.g., Inf, NaN) are documented and explained.

## Limitations

- Simulation results depend on random seed and number of replicates; minor numerical drift across runs and systems is expected.
- The repository README does not document a changelog, so changes or corrections to simulation code may not be tracked in version history.
- Validation against reported values requires access to the original article and reported summary statistics; missing or ambiguous reporting makes validation difficult.
- Execution environment (R version, package versions) can affect numerical results; reproducibility may require pinning dependencies.

## Evidence

- [intro] The task focuses on reproducing Type I error and power simulation results from the SimulationFunctions scripts.: "TypeI and Power simulation scripts"
- [other] The workflow explicitly includes executing both error and power simulations and collecting summary outputs.: "Execute the Type I error simulation script to compute error rates and generate summary statistics. 4. Execute the power simulation script to compute statistical power across tested scenarios and"
- [readme] The repository is identified as the authoritative source for PaIRKAT simulation functions.: "Scripts for PaIRKAT functions with example work flow"
