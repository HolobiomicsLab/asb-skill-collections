---
name: simulation-result-validation
description: Use when you have obtained a repository containing simulation scripts (e.g., Type I error or power analysis scripts) and need to verify that executing those scripts produces the same summary statistics and findings reported in the associated publication or documentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3677
  edam_topics:
  - http://edamontology.org/topic_3316
  tools:
  - R (or language used by PaIRKAT scripts)
  - R
  - PaIRKAT SimulationFunctions
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

# simulation-result-validation

## Summary

Validate that computational simulation scripts correctly reproduce published Type I error and power statistics by executing them end-to-end and comparing generated outputs against reported values. This skill ensures fidelity of simulation implementations and identifies discrepancies in statistical methodology.

## When to use

You have obtained a repository containing simulation scripts (e.g., Type I error or power analysis scripts) and need to verify that executing those scripts produces the same summary statistics and findings reported in the associated publication or documentation. Use this skill when reproducibility of simulation results is a prerequisite for trust in downstream methodological claims or reuse of the codebase.

## When NOT to use

- The simulation scripts are not available or cannot be executed in your computational environment.
- No reference values or published results exist against which to validate; use exploratory simulation instead.
- The repository README or documentation does not specify expected outputs or parameter ranges.

## Inputs

- Cloned or downloaded repository containing simulation scripts
- Type I error simulation script code
- Power simulation script code
- Published or documented reference values (summary statistics, tables, confidence intervals)
- Specification of simulation parameters (sample sizes, effect sizes, scenarios tested)

## Outputs

- Type I error summary statistics (error rates per scenario)
- Power summary statistics (power per scenario and parameter combination)
- Validation report comparing generated outputs to reference values
- Log of any discrepancies and their magnitude
- Reconciliation notes explaining acceptable deviations

## How to apply

Clone or obtain the simulation repository, then locate and load the simulation scripts (e.g., SimulationFunctions modules). Execute the Type I error simulation script to compute error rates and generate summary statistics across all tested parameter scenarios. Next, execute the power simulation script to compute statistical power and generate summary outputs. Collect all generated outputs (numeric summaries, tables, confidence intervals) and systematically compare them against the reported values in the publication, README, or supplementary materials. Document any deviations, their magnitude, and whether they fall within acceptable numerical tolerance (e.g., floating-point rounding). Validation succeeds when outputs match or discrepancies are explained by documented parameter choices or computational precision limits.

## Related tools

- **R** (Execution environment for PaIRKAT simulation scripts and summary statistic computation)
- **PaIRKAT SimulationFunctions** (Source module containing Type I error and power simulation implementations to be validated) — https://github.com/CharlieCarpenter/PaIRKAT

## Examples

```
# In R, after cloning github.com/CharlieCarpenter/PaIRKAT:
source('SimulationFunctions/TypeI_simulation.R')
TypeI_results <- run_TypeI_simulation(scenarios_config)
source('SimulationFunctions/Power_simulation.R')
Power_results <- run_power_simulation(scenarios_config)
validation <- compare_outputs(TypeI_results, published_TypeI_stats)
```

## Evaluation signals

- Generated Type I error rates match published/documented values within numerical tolerance (e.g., ±0.001 or floating-point precision limits).
- Generated power estimates match published values across all tested parameter scenarios and effect sizes.
- No script execution errors or warnings that would indicate broken dependencies, missing data, or undefined parameters.
- Summary statistics tables have correct dimensions, column names, and data types matching the published format.
- Validation log documents all comparisons performed and confirms no unexplained systematic deviations between runs.

## Limitations

- Validation depends on availability of complete reference values in the publication or supplementary materials; if only partial results are reported, comprehensive validation may not be possible.
- Floating-point arithmetic and random number generation can introduce minor numerical differences across platforms and R versions; acceptable tolerance thresholds must be pre-defined.
- The README provides no changelog or versioning information, so it may be unclear whether the current repository reflects the exact code used to generate published results.
- If simulation parameters (sample sizes, number of replicates, random seed strategy) are not fully documented, reproduction may yield different outputs even if the code is correct.

## Evidence

- [other] Can the Type I error and power simulation outputs from the PaIRKAT repository be successfully regenerated by executing the deposited simulation scripts?: "Can the Type I error and power simulation outputs from the PaIRKAT repository be successfully regenerated by executing the deposited simulation scripts?"
- [other] Execute the Type I error simulation script to compute error rates and generate summary statistics. Execute the power simulation script to compute statistical power across tested scenarios and generate summary statistics. Collect and validate all generated simulation summary outputs against reported values.: "Execute the Type I error simulation script to compute error rates and generate summary statistics. Execute the power simulation script to compute statistical power across tested scenarios and"
- [readme] Scripts for PaIRKAT functions with example work flow. TypeI and Power simulation scripts: "Scripts for PaIRKAT functions with example work flow. TypeI and Power simulation scripts"
