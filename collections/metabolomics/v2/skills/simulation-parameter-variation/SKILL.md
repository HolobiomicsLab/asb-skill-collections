---
name: simulation-parameter-variation
description: Use when when you have a computational simulation framework (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Jupyter
  - metabolomics-ORA
derived_from:
- doi: 10.1371/journal.pcbi.1009105
  title: ORA
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ora
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  dedup_kept_from: coll_ora
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009105
  all_source_dois:
  - 10.1371/journal.pcbi.1009105
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Simulation Parameter Variation

## Summary

Systematically vary one or more input parameters across a defined range in a computational simulation to assess how changes in those parameters affect statistical outcomes and false-positive rates. This skill is essential for validating pathway analysis methods under realistic conditions of incomplete metabolite detection.

## When to use

When you have a computational simulation framework (e.g., for ORA p-value distributions) and need to understand how a key experimental constraint—such as metabolite detection coverage (10–100% of the pathway database)—influences statistical validity, false-positive rates, or effect size distributions. Use this skill to isolate the impact of a single variable while holding other conditions constant.

## When NOT to use

- You have only a single, fixed parameter configuration and no variation is needed (no sensitivity analysis question).
- The simulation framework is not reproducible or not parameterizable (e.g., closed-source tool with no exposed knobs).
- You are analyzing observed experimental data rather than running controlled simulations—use empirical statistical methods instead.

## Inputs

- Jupyter notebook or Python script with parameterizable simulation code
- Parameter range specification (e.g., coverage values: 10, 20, ..., 100%)
- Pathway database or simulated metabolite set definitions
- Statistical test implementation (e.g., ORA function)

## Outputs

- Summary statistics table (columns: parameter value, mean p-value, median p-value, false-positive rate, confidence intervals)
- Line or scatter plot: false-positive rate vs. parameter value with error bands
- Boxplots or violin plots: outcome (p-value) distributions across parameter levels
- Raw simulation results per parameter iteration (for reanalysis)

## How to apply

Load the simulation framework (typically a Jupyter notebook with reproducible code). Define a range for the parameter of interest (e.g., coverage fraction from 10% to 100% in 10% increments). For each parameter value, execute the full simulation workflow (e.g., run ORA on simulated metabolite sets), record the primary outcome metrics (p-value distributions, false-positive count at p < 0.05 threshold), and store results with associated parameter values. Aggregate results into a summary statistics table with columns for parameter value, mean/median outcome, false-positive rate, and confidence intervals. Visualize the relationship using line plots or scatter plots with error bands for the primary metric (e.g., false-positive rate) as a function of the varied parameter, and produce boxplots or violin plots for outcome distributions across parameter levels. Rationale: varying a single parameter reveals how realistic constraints affect method validity without confounding multiple factors.

## Related tools

- **Python** (Language for implementing and executing parameterized simulations with loops over parameter ranges)
- **Jupyter** (Interactive notebook environment for running, documenting, and visualizing simulation sweeps and aggregating results)
- **metabolomics-ORA** (Reference implementation of ORA simulation framework with reproducible code for varying metabolite coverage) — https://github.com/cwieder/metabolomics-ORA.git

## Examples

```
for coverage in range(10, 101, 10):
    results = run_ora_simulation(coverage_fraction=coverage/100, n_replicates=1000)
    summary.append({'coverage': coverage, 'fp_rate': sum(results['p'] < 0.05) / len(results), 'mean_p': results['p'].mean()})
df = pd.DataFrame(summary)
df.to_csv('coverage_sweep_results.csv', index=False)
```

## Evaluation signals

- The summary statistics table is complete with no missing parameter values in the specified range.
- False-positive rate (or other outcome metric) shows a monotonic or expected trend as the parameter varies, consistent with the biological/statistical hypothesis (e.g., false-positive rate decreases with increasing coverage).
- Error bands (confidence intervals) on visualizations are appropriately sized and do not contain contradictory or zero-width intervals.
- Boxplot or violin plot shows non-overlapping median/distribution shifts across parameter levels, confirming parameter effect is detectable.
- All simulation runs are recorded and reproducible from the same code and seed; re-running the workflow with identical parameters yields identical results.

## Limitations

- Parameter variation explores only one or two dimensions at a time; interactions between multiple parameters are not captured without factorial design.
- Simulation outcomes depend critically on the quality and realism of the underlying simulation model (e.g., how well the ORA null distribution is specified); parameter variation cannot compensate for model misspecification.
- Computational cost scales linearly or worse with the number of parameter values and simulation replicates; very fine-grained sweeps may be prohibitively expensive.
- False-positive rate estimates depend on the chosen threshold (e.g., p < 0.05); shifting the threshold alters conclusions and must be pre-specified or reported as a sensitivity analysis.

## Evidence

- [other] Execute the simulation workflow varying the fraction of detected metabolites across a range of coverage values (e.g., 10–100% of pathway database): "Execute the simulation workflow varying the fraction of detected metabolites across a range of coverage values (e.g., 10–100% of pathway database)"
- [other] For each coverage level, run ORA on simulated metabolite sets and record the distribution of p-values and count false positives (p < 0.05 threshold): "For each coverage level, run ORA on simulated metabolite sets and record the distribution of p-values and count false positives (p < 0.05 threshold)"
- [other] Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals: "Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals"
- [other] Generate a line or scatter plot showing false-positive rate as a function of coverage with error bands, and produce boxplots or violin plots of p-value distributions across coverage levels: "Generate a line or scatter plot showing false-positive rate as a function of coverage with error bands, and produce boxplots or violin plots of p-value distributions across coverage levels"
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
