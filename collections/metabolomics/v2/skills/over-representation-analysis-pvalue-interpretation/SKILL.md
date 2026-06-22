---
name: over-representation-analysis-pvalue-interpretation
description: Use when when you have run ORA on a metabolomics dataset and obtained p-values for pathway enrichment, but you need to assess whether observed significance is genuine or an artifact of incomplete metabolite coverage.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0622
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

# over-representation-analysis-pvalue-interpretation

## Summary

Interpret Over-representation Analysis (ORA) p-values in metabolomics pathway analysis by quantifying how detection coverage (fraction of pathway metabolites actually measured) affects false-positive rates and statistical significance distributions. This skill guards against inflated significance claims arising from incomplete metabolite detection.

## When to use

When you have run ORA on a metabolomics dataset and obtained p-values for pathway enrichment, but you need to assess whether observed significance is genuine or an artifact of incomplete metabolite coverage. Specifically: when the fraction of detected metabolites relative to the pathway database is known or estimable (e.g., 30–80% coverage is common), and you want to understand how p-value distributions and false-positive rates shift across different coverage scenarios.

## When NOT to use

- Your metabolomics dataset has near-complete or genome-wide coverage (>95%) of the pathway database, in which case coverage bias is negligible and ORA p-values are more trustworthy.
- You are working with a method other than Over-representation Analysis (e.g., Gene Set Enrichment Analysis, topology-based pathway methods, or quantitative enrichment approaches) — those methods handle incomplete coverage differently.
- You do not have or cannot estimate the detection coverage for your measured metabolites relative to the pathway database.

## Inputs

- ORA p-value vector (one p-value per tested pathway)
- Metabolite detection coverage metric (fraction of pathway database detected; scalar or per-pathway value)
- Pathway membership database (metabolite-to-pathway mapping)

## Outputs

- False-positive rate summary table (coverage % vs. FPR, mean/median p-value, confidence intervals)
- Line or scatter plot of false-positive rate as a function of coverage with error bands
- Boxplots or violin plots of p-value distributions stratified by coverage level
- Adjusted p-value threshold or multiple-testing correction recommendation based on observed coverage

## How to apply

Obtain or simulate ORA results across a range of metabolite detection coverage levels (e.g., 10–100% of pathway database membership). For each coverage level, record the distribution of ORA p-values and calculate the empirical false-positive rate (proportion of p-values < 0.05 under the null hypothesis of no enrichment). Aggregate these into a summary table with columns for coverage percentage, mean/median p-value, false-positive rate, and confidence intervals. Plot false-positive rate as a function of coverage with error bands to visualize the relationship. Compare your observed p-values and coverage level against this benchmark: if your dataset has low coverage and your p-values fall in a regime where false-positive rates are inflated (e.g., >10–15% instead of the nominal 5%), apply multiple-testing correction or increase your p-value threshold. The rationale is that sparse detection systematically biases ORA statistics because the algorithm cannot fairly represent the 'universe' of metabolites in each pathway.

## Related tools

- **Python** (Language for executing simulation workflows, aggregating coverage-stratified ORA results, and generating summary statistics and plots.)
- **Jupyter** (Interactive notebook environment for iterating through simulation framework, varying coverage parameters, and visualizing p-value distributions and false-positive rate trends.)
- **metabolomics-ORA** (Reference repository containing reproducible simulation code and framework for analyzing ORA p-value behavior across metabolite detection coverage levels.) — https://github.com/cwieder/metabolomics-ORA.git

## Examples

```
# Load the metabolomics-ORA notebook; execute the simulation workflow varying coverage from 10% to 100% in 10% increments, then aggregate results: for coverage in range(10, 101, 10): run ORA on simulated sets; record p-values and FPR at p<0.05; store in summary_table. Finally, plot FPR vs. coverage with error bands.
```

## Evaluation signals

- False-positive rate increases monotonically or near-monotonically as metabolite detection coverage decreases; a plot of FPR vs. coverage should show a clear trend.
- Summary statistics table contains all expected columns (coverage %, mean/median p-value, FPR, confidence intervals) with no missing values and plausible numeric ranges (FPR between 0 and 1; p-values between 0 and 1).
- Boxplots or violin plots visually confirm that p-value distributions are more dispersed and skewed toward smaller values at lower coverage levels, consistent with increased false-positive inflation.
- When coverage is systematically varied in simulation, the observed empirical false-positive rate at a nominal threshold (p < 0.05) significantly exceeds 5% at low coverage (<50%) and approaches 5% only at high coverage (>80%), validating the pitfall.
- Any adjusted p-value threshold or multiple-testing correction recommendation is justified by the observed FPR inflation relative to the nominal rate in your specific coverage regime.

## Limitations

- The skill assumes that the pathway database is comprehensive and accurately annotated; errors in pathway membership will confound coverage estimates and bias conclusions.
- Coverage estimation is sensitive to the definition of 'detected': different detection thresholds (e.g., signal-to-noise ratio, peak intensity minimum, or statistical significance cutoff) will yield different coverage metrics and thus different false-positive rate estimates.
- The relationship between coverage and ORA p-value inflation may vary by pathway size, metabolite abundance distribution, and the underlying pathway database (KEGG, MetaCyc, Reactome, etc.); results from one database may not transfer directly to another.
- This skill addresses coverage bias in ORA but does not fully resolve other known pitfalls of ORA in metabolomics, such as correlation structure among metabolites, compound identifier ambiguity, or pathway size bias.

## Evidence

- [other] How does the fraction of metabolites detected (coverage) relative to the pathway database affect the distribution of ORA p-values and false-positive rates in metabolomics pathway analysis?: "research_question: How does the fraction of metabolites detected (coverage) relative to the pathway database affect the distribution of ORA p-values and false-positive rates in metabolomics pathway"
- [other] The study provides reproducible simulation code in a Jupyter notebook that enables analysis of how metabolite detection coverage impacts ORA statistical outcomes.: "finding: The study provides reproducible simulation code in a Jupyter notebook that enables analysis of how metabolite detection coverage impacts ORA statistical outcomes."
- [other] For each coverage level, run ORA on simulated metabolite sets and record the distribution of p-values and count false positives (p < 0.05 threshold).: "For each coverage level, run ORA on simulated metabolite sets and record the distribution of p-values and count false positives (p < 0.05 threshold)."
- [other] Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals.: "Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals."
- [intro] Over-representation Analysis (ORA) is a pathway analysis method used in metabolomics with identifiable pitfalls and best practices: "Over-representation Analysis (ORA) is a pathway analysis method used in metabolomics with identifiable pitfalls and best practices"
