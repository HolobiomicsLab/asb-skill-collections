---
name: metabolite-coverage-simulation
description: Use when designing or validating a metabolomics pathway analysis experiment,
  especially when you have uncertainty about how many metabolites your detection platform
  will reliably measure relative to a pathway database. Use it if you want to understand
  whether your expected metabolite coverage (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - Jupyter
  - metabolomics-ORA
  license_tier: open
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

# metabolite-coverage-simulation

## Summary

Simulate Over-representation Analysis (ORA) outcomes across varying fractions of detected metabolites to quantify how metabolite detection coverage affects p-value distributions and false-positive rates in pathway analysis. This skill reveals coverage-dependent statistical artifacts that can inflate false discovery.

## When to use

Apply this skill when designing or validating a metabolomics pathway analysis experiment, especially when you have uncertainty about how many metabolites your detection platform will reliably measure relative to a pathway database. Use it if you want to understand whether your expected metabolite coverage (e.g., 30% vs. 80% of database metabolites) will compromise ORA sensitivity or specificity before collecting data.

## When NOT to use

- Your metabolomics platform already has published, stable detection profiles for your target pathway database — use empirical benchmarking instead.
- You are performing ORA on a single real dataset with known coverage; this skill is for prospective design and validation, not post-hoc explanation of already-observed p-values.
- Your analysis does not use Over-representation Analysis; this skill is specific to ORA and does not apply to GSEA, SPIA, or other pathway enrichment methods.

## Inputs

- Metabolite pathway database (gene set / pathway membership annotations)
- Coverage range specification (e.g., list or array of fractional values from 0.1 to 1.0)
- ORA statistical threshold (e.g., α = 0.05 for significance cutoff)
- Simulation parameters (sample size, number of replicates per coverage level)

## Outputs

- Summary statistics table (coverage %, mean p-value, median p-value, false-positive rate, 95% CI)
- Line or scatter plot of false-positive rate vs. coverage with error bands
- Boxplots or violin plots of ORA p-value distributions stratified by coverage level
- Aggregated simulation results (raw p-value arrays per coverage condition)

## How to apply

Clone the metabolomics-ORA repository and load the provided Jupyter notebook simulation framework. Parameterize the simulation by specifying a range of metabolite detection coverage values (e.g., 10–100% of pathway database). For each coverage level, execute ORA on simulated metabolite sets and record the distribution of p-values and count false positives at the p < 0.05 threshold. Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals. Visualize false-positive rate as a function of coverage with error bands, and produce boxplots or violin plots of p-value distributions across coverage levels to identify the critical coverage threshold below which ORA reliability degrades.

## Related tools

- **Python** (Programming language for implementing the simulation logic and statistical calculations)
- **Jupyter** (Interactive notebook environment for running, documenting, and visualizing the coverage simulation workflow)
- **metabolomics-ORA** (Repository containing reproducible simulation code and the ORA framework used to evaluate p-value and false-positive behavior across coverage levels) — https://github.com/cwieder/metabolomics-ORA.git

## Examples

```
git clone https://github.com/cwieder/metabolomics-ORA.git && cd metabolomics-ORA && jupyter notebook # Open notebook, run simulation loop over coverage range [0.1, 0.2, ..., 1.0], aggregate results, and generate summary table and plots.
```

## Evaluation signals

- False-positive rate increases monotonically or in a predictable pattern as metabolite coverage decreases below a critical threshold (typically around 20–40% coverage).
- P-value distributions show increasing right-skew and wider variance at lower coverage levels, indicating inflated Type I error.
- Summary statistics table is complete with no missing values across all coverage conditions and matches the number of simulation replicates specified.
- Confidence intervals are appropriately narrow around point estimates of false-positive rate at high coverage, and widen as coverage decreases, reflecting increased variability.
- Visualization legend and axes are labeled with coverage percentage, p-value scale, and false-positive rate, and plots are reproducible from the same random seed.

## Limitations

- Simulation assumes metabolites are missing uniformly at random across all pathways; in practice, detection bias may be pathway- or metabolite-class-specific (e.g., lipids vs. amino acids).
- Results depend critically on the choice of pathway database and its annotation quality; switching databases may alter the coverage–performance relationship.
- The study does not address multiple-testing correction strategies (e.g., FDR control); reported false-positive rates use nominal p < 0.05 thresholds and may not reflect corrected significance levels.
- Simulation uses synthetic null metabolite sets; real pathway significance patterns may differ, and observed coverage effects in actual data may be confounded by biological signal.

## Evidence

- [other] How does the fraction of metabolites detected (coverage) relative to the pathway database affect the distribution of ORA p-values and false-positive rates in metabolomics pathway analysis?: "How does the fraction of metabolites detected (coverage) relative to the pathway database affect the distribution of ORA p-values and false-positive rates in metabolomics pathway analysis?"
- [other] The study provides reproducible simulation code in a Jupyter notebook that enables analysis of how metabolite detection coverage impacts ORA statistical outcomes.: "The study provides reproducible simulation code in a Jupyter notebook that enables analysis of how metabolite detection coverage impacts ORA statistical outcomes."
- [other] Execute the simulation workflow varying the fraction of detected metabolites across a range of coverage values (e.g., 10–100% of pathway database). For each coverage level, run ORA on simulated metabolite sets and record the distribution of p-values and count false positives (p < 0.05 threshold).: "Execute the simulation workflow varying the fraction of detected metabolites across a range of coverage values (e.g., 10–100% of pathway database). For each coverage level, run ORA on simulated"
- [other] Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals. Generate a line or scatter plot showing false-positive rate as a function of coverage with error bands, and produce boxplots or violin plots of p-value distributions across coverage levels.: "Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals. Generate a line or scatter plot showing"
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [intro] This repository contains the code to run the simulations presented in the study: "This repository contains the code to run the simulations presented in the study"
