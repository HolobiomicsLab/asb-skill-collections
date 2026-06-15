---
name: statistical-distribution-visualization
description: Use when when you have run a computational analysis (e.g., Over-representation Analysis, pathway enrichment, statistical hypothesis test) repeatedly under varying conditions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_2269
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Jupyter
  - matplotlib / seaborn
  - pandas
derived_from:
- doi: 10.1371/journal.pcbi.1009105
  title: ORA
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ora
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  dedup_kept_from: coll_ora
schema_version: 0.2.0
---

# statistical-distribution-visualization

## Summary

Visualize and compare distributions of statistical test outcomes (p-values, effect sizes, false-positive rates) across experimental conditions or parameter sweeps to identify systematic biases and validate assumptions in computational workflows. This skill surfaces how changes in input coverage, detection thresholds, or methodological choices alter the distributional properties of test statistics.

## When to use

When you have run a computational analysis (e.g., Over-representation Analysis, pathway enrichment, statistical hypothesis test) repeatedly under varying conditions (e.g., different metabolite detection coverage levels, sample sizes, or input filtering criteria) and need to assess whether the p-value distribution, false-positive rate, or effect-size distribution behaves as expected under the null hypothesis or shows systematic distortion across conditions.

## When NOT to use

- When analyzing a single dataset with a fixed set of parameters—distribution visualization is most informative when comparing across multiple conditions or sensitivity analyses.
- When the focus is on point estimation or hypothesis testing of a single effect, rather than understanding how a method's statistical properties vary across input conditions.
- When sample sizes per condition are extremely small (< 5 replicates), making confidence intervals and distributional properties unreliable.

## Inputs

- Multiple sets of p-values from repeated statistical tests (e.g., ORA runs at different metabolite coverage levels)
- False-positive counts (number of significant results at chosen threshold per condition)
- Parameter values or condition labels (e.g., coverage percentages, detection thresholds)
- Confidence interval bounds or bootstrap replicates for each condition

## Outputs

- Boxplot or violin plot showing p-value distribution across parameter levels
- Line or scatter plot of false-positive rate vs. parameter value with error bands
- Summary statistics table (coverage, mean/median p-value, FPR, 95% CI)
- Annotated interpretation of distributional changes and parameter-dependent statistical behavior

## How to apply

Execute the analysis workflow across a defined parameter range (e.g., metabolite detection coverage from 10–100% of pathway database). For each parameter level, collect the full distribution of test statistics (e.g., ORA p-values, false-positive counts at p < 0.05 threshold). Aggregate results into a summary table with columns for parameter level, mean/median p-value, false-positive rate, and confidence intervals. Generate side-by-side boxplots or violin plots to compare p-value distributions across parameter levels, and produce a line or scatter plot with error bands showing how false-positive rate changes monotonically or non-monotonically with the parameter. Use these visualizations to identify parameter ranges where statistical assumptions are violated (e.g., inflated false positives under low coverage) and document the rationale for selecting optimal parameter values in downstream analyses.

## Related tools

- **Python** (Primary language for running simulations and executing ORA workflows across parameter ranges) — https://github.com/cwieder/metabolomics-ORA
- **Jupyter** (Interactive notebook environment for executing reproducible simulation code and generating inline visualizations) — https://github.com/cwieder/metabolomics-ORA
- **matplotlib / seaborn** (Plotting libraries for generating boxplots, violin plots, and line plots with error bands)
- **pandas** (Data aggregation and summary statistics computation (mean, median, confidence intervals))

## Evaluation signals

- Confidence intervals for false-positive rate at each parameter level do not overlap zero and scale monotonically or show clear directional trend with the parameter (e.g., higher coverage → lower FPR).
- P-value distributions under low metabolite coverage show evidence of right-skew or uniform-like behavior (violations of null assumption), while high-coverage distributions approximate exponential or uniform under the null.
- False-positive rate remains at or near the nominal significance threshold (e.g., ~5% at p < 0.05) across all parameter values; systematic inflation indicates a methodological pitfall requiring mitigation.
- Summary statistics table includes all conditions without missing values; error bands in plots span the full 95% confidence interval and are visually distinguishable across conditions.
- Visualization directly annotates or narratively explains which parameter ranges are safe for downstream use and which introduce unacceptable statistical bias.

## Limitations

- Coverage bias in metabolomics ORA is parameter-dependent and contingent on the pathway database composition; results may not generalize to databases with different pathway definitions or metabolite annotations.
- False-positive rate and p-value distribution depend critically on the choice of null model and statistical test (ORA assumes hypergeometric null); alternative enrichment methods (e.g., GSEA, network-based methods) may show different coverage sensitivity.
- Visualization of distributional properties requires sufficient replicates per condition (typically ≥ 50–100 test runs) to estimate robust confidence intervals; simulated data may not capture real-world metabolomics noise, missing data patterns, or batch effects.
- The skill assumes a continuous or discrete parameter sweep is feasible; computational cost scales linearly with number of conditions and test replicates, and may become prohibitive for very large metabolite databases or complex pathway networks.

## Evidence

- [other] Execute the simulation workflow varying the fraction of detected metabolites across a range of coverage values (e.g., 10–100% of pathway database). For each coverage level, run ORA on simulated metabolite sets and record the distribution of p-values and count false positives (p < 0.05 threshold).: "Execute the simulation workflow varying the fraction of detected metabolites across a range of coverage values (e.g., 10–100% of pathway database). For each coverage level, run ORA on simulated"
- [other] Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals. Generate a line or scatter plot showing false-positive rate as a function of coverage with error bands, and produce boxplots or violin plots of p-value distributions across coverage levels.: "Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals. Generate a line or scatter plot showing"
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [intro] This repository contains the code to run the simulations presented in the study: "This repository contains the code to run the simulations presented in the study"
- [other] How does the fraction of metabolites detected (coverage) relative to the pathway database affect the distribution of ORA p-values and false-positive rates in metabolomics pathway analysis?: "How does the fraction of metabolites detected (coverage) relative to the pathway database affect the distribution of ORA p-values and false-positive rates in metabolomics pathway analysis?"
