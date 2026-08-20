---
name: pathway-database-filtering-by-detection
description: Use when you have run a metabolomics experiment with incomplete coverage
  of a reference pathway database (e.g., 10–100% of database metabolites detected),
  and you plan to use ORA for pathway enrichment. The skill is essential if your detection
  method has known sensitivity limits (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Jupyter
  - cwieder/metabolomics-ORA
  techniques:
  - mass-spectrometry
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

# pathway-database-filtering-by-detection

## Summary

Filter pathway databases to include only metabolites detected in an experiment before running Over-representation Analysis (ORA), reducing false positives driven by coverage bias. This skill addresses a critical pitfall in metabolomics pathway analysis where undetected metabolites in the reference database inflate null distributions and distort p-value calibration.

## When to use

Apply this skill when you have run a metabolomics experiment with incomplete coverage of a reference pathway database (e.g., 10–100% of database metabolites detected), and you plan to use ORA for pathway enrichment. The skill is essential if your detection method has known sensitivity limits (e.g., mass spectrometry ionization bias, LC retention time windows) that cause systematic metabolite dropout, as unfiltered databases will artificially inflate false-positive rates at low coverage levels.

## When NOT to use

- Your metabolomics platform has near-complete coverage (>95%) of the reference database, making filtering negligible and unlikely to materially change ORA outcomes.
- You are performing exploratory pathway discovery where you intentionally want to leverage all available database knowledge, including pathways with sparse detection, to generate hypotheses rather than control error rates.
- The input pathway database is already pre-filtered or curated to detected metabolites by the database provider or a prior analysis step.

## Inputs

- metabolite detection set (list of detected metabolite identifiers from experiment)
- reference pathway database (mappings of metabolite IDs to pathway annotations)
- metadata on detection coverage and sensitivity thresholds

## Outputs

- filtered pathway database (database subset to detected metabolites only)
- coverage statistics table (coverage percentage, detected/total counts per pathway)
- ORA p-value distributions and false-positive rate summary (before/after filtering comparison)
- calibration plots (p-value histograms, QQ plots, or empirical null distributions)

## How to apply

Before executing ORA, subset the pathway database to retain only metabolites actually detected in your sample set. Record the coverage fraction (detected metabolites / total database metabolites) at each filtering stage. Run ORA on the filtered database and compare the resulting p-value distribution and false-positive rate (FPR, proportion of tests with p < 0.05 under the null) against the unfiltered database. The filtering step should be documented with coverage statistics so that downstream interpretation accounts for the reduced effective pathway size. Validate that the p-value distribution is well-calibrated (uniform under the null) after filtering; persistent deviations suggest additional confounders beyond coverage.

## Related tools

- **Python** (primary language for implementing the filtering logic, ORA simulations, and p-value aggregation)
- **Jupyter** (interactive notebook environment for running reproducible simulations that vary coverage fractions and compute ORA statistics) — https://github.com/cwieder/metabolomics-ORA.git
- **cwieder/metabolomics-ORA** (reference repository containing simulation framework and code to execute coverage-dependent ORA analysis) — https://github.com/cwieder/metabolomics-ORA.git

## Examples

```
# Clone repository and load simulation notebook
git clone https://github.com/cwieder/metabolomics-ORA.git
# In Jupyter: vary coverage from 10–100%, run ORA, aggregate p-value distributions and false-positive rates by coverage level
```

## Evaluation signals

- Coverage percentage is correctly computed and recorded for each filtering step (detected metabolites / total database metabolites before filtering).
- ORA p-value distribution becomes closer to uniform (well-calibrated) after filtering, with false-positive rate at p < 0.05 threshold approaching the nominal significance level under null simulation.
- Mean and median ORA p-values, confidence intervals, and false-positive rate values are aggregated in a summary table with coverage as a stratification variable; trend should show decreasing FPR or improved calibration with increasing coverage.
- Boxplots or violin plots of p-value distributions across coverage levels show visually distinct separation, with lower coverage producing more inflated p-values.
- Comparison plots (before/after filtering) demonstrate that unfiltered databases show spuriously low p-values at low coverage, while filtered databases show corrected (higher) p-values and improved null calibration.

## Limitations

- Filtering based on detected metabolites assumes detection patterns are random or systematic but independent of pathway membership; if detection is pathway-biased (e.g., lipids detected preferentially), filtering may introduce new selection bias.
- The filtered database reflects only a single experiment's detection footprint; replicability depends on consistent detection across runs and platforms.
- Filtering does not address other ORA pitfalls such as pathway database overlap, redundancy, or multiple-testing correction; it is a necessary but not sufficient fix for robust pathway analysis.
- Coverage filtering is most informative when paired with empirical null simulations; a single filtered analysis without null calibration may mask residual statistical issues.

## Evidence

- [other] How does the fraction of metabolites detected (coverage) relative to the pathway database affect the distribution of ORA p-values and false-positive rates in metabolomics pathway analysis?: "How does the fraction of metabolites detected (coverage) relative to the pathway database affect the distribution of ORA p-values and false-positive rates"
- [other] Execute the simulation workflow varying the fraction of detected metabolites across a range of coverage values (e.g., 10–100% of pathway database). For each coverage level, run ORA on simulated metabolite sets and record the distribution of p-values and count false positives (p < 0.05 threshold).: "Execute the simulation workflow varying the fraction of detected metabolites across a range of coverage values (e.g., 10–100% of pathway database). For each coverage level, run ORA on simulated"
- [other] Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals.: "Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals."
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [intro] Pathway analysis in metabolomics: Pitfalls and best practice for the use of Over-representation Analysis: "Over-representation Analysis (ORA) is a pathway analysis method used in metabolomics with identifiable pitfalls and best practices"
