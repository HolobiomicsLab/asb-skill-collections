---
name: false-positive-rate-assessment
description: Use when you have run ORA on simulated metabolite sets with known null
  conditions (no true pathway enrichment) and need to measure how detection coverage,
  pathway database size, or other experimental parameters inflate Type I error rates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Jupyter
  license_tier: restricted
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

# false-positive-rate-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantify the proportion of statistically significant results (p < 0.05) that are false positives across a range of controlled simulation conditions in pathway analysis. This skill is essential for validating the robustness of Over-representation Analysis (ORA) under varying metabolite detection coverage and identifying conditions where statistical thresholds become unreliable.

## When to use

Apply this skill when you have run ORA on simulated metabolite sets with known null conditions (no true pathway enrichment) and need to measure how detection coverage, pathway database size, or other experimental parameters inflate Type I error rates. Use it to validate that a pathway analysis pipeline maintains false-positive rate control (typically ≤ 5%) across realistic metabolomics scenarios.

## When NOT to use

- Input contains real metabolomics data with unknown ground truth; FPR assessment requires null simulations where no true enrichment exists.
- ORA has not yet been executed on the simulated sets; this skill quantifies results post-analysis, not the analysis itself.
- Coverage is uniform across all metabolites in the pathway database; FPR assessment is most informative when coverage varies systematically.

## Inputs

- Simulated metabolite sets with null condition (no true pathway enrichment)
- ORA p-value results indexed by metabolite detection coverage level (10–100%)
- Pathway database with known metabolite membership
- Coverage fraction values (e.g., [0.1, 0.2, …, 1.0])

## Outputs

- Summary statistics table: coverage percentage, false-positive rate, mean/median p-value, confidence intervals
- Line or scatter plot: false-positive rate vs. coverage with error bands
- Count of p < 0.05 results per coverage level (numerator for FPR calculation)

## How to apply

Execute ORA on simulated metabolite sets drawn from null distributions (where no true enrichment exists) across a range of metabolite detection coverage levels (e.g., 10–100% of pathway database). For each coverage level, count the number of tests with p < 0.05 and divide by the total number of simulations to obtain the false-positive rate. Aggregate results into a summary table with columns for coverage percentage and false-positive rate with confidence intervals. Generate line or scatter plots showing false-positive rate as a function of coverage with error bands to visualize how coverage bias affects Type I error inflation. Compare observed false-positive rates against the nominal 5% threshold to identify coverage ranges where ORA becomes unreliable.

## Related tools

- **Python** (Statistical computation and data aggregation for FPR calculation and table generation)
- **Jupyter** (Reproducible notebook environment for running simulations, executing FPR calculations, and generating plots) — https://github.com/cwieder/metabolomics-ORA.git

## Examples

```
# After running ORA on simulated sets at each coverage level, aggregate FPR:
fpr_by_coverage = []; coverage_levels = [0.1, 0.2, ..., 1.0]
for cov in coverage_levels:
    p_vals = [results from ORA at this coverage]
    fpr = sum(1 for p in p_vals if p < 0.05) / len(p_vals)
    fpr_by_coverage.append(fpr)
# Plot FPR vs coverage with error bands using matplotlib or seaborn
```

## Evaluation signals

- False-positive rate at nominal p < 0.05 threshold should remain ≤ 5% (or match the expected α level) across all coverage levels in null simulations, or show clear inflation patterns if ORA is miscalibrated.
- Confidence intervals around FPR estimates should not be excessively wide (CI width should decrease with increasing number of simulations); check that total simulations per coverage level is sufficient (n ≥ 1000 recommended).
- Plot of FPR vs. coverage should be monotonic or show expected trend (e.g., FPR increases as coverage decreases if coverage bias is a confounder); aberrant jumps or non-monotonicity suggest simulation or aggregation error.
- Summary table should have consistent row counts and matching coverage fractions; all p-values used in the calculation should be from null simulations (verified by checking simulation code and random seed).
- Numerical FPR values should fall within [0, 1] range; confidence intervals should be symmetric around the FPR point estimate (e.g., using binomial Wilson score intervals) and not extend beyond [0, 1].

## Limitations

- FPR assessment assumes that the null simulations correctly represent the null distribution under the tested metabolite detection regime; bias in null data generation will propagate to FPR estimates.
- The choice of p-value threshold (e.g., p < 0.05) is arbitrary; FPR is sensitive to this choice, and a single threshold may not capture power or calibration across the full p-value distribution.
- Coverage is treated as a discrete or binned variable in aggregation; if coverage varies continuously within a bin, FPR may be confounded with other unmeasured parameters.
- Results are specific to the pathway database, metabolite set size, and ORA implementation used in simulations; generalization to other databases or ORA variants requires separate assessment.
- No changelog or versioning information was found for the metabolomics-ORA repository; reproducibility may be affected if the code or pathway databases are updated without tracking changes.

## Evidence

- [other] For each coverage level, run ORA on simulated metabolite sets and record the distribution of p-values and count false positives (p < 0.05 threshold).: "For each coverage level, run ORA on simulated metabolite sets and record the distribution of p-values and count false positives (p < 0.05 threshold)."
- [other] Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals.: "Aggregate results into a summary statistics table with columns for coverage percentage, mean/median ORA p-value, false-positive rate, and confidence intervals."
- [other] Generate a line or scatter plot showing false-positive rate as a function of coverage with error bands, and produce boxplots or violin plots of p-value distributions across coverage levels.: "Generate a line or scatter plot showing false-positive rate as a function of coverage with error bands, and produce boxplots or violin plots of p-value distributions across coverage levels."
- [other] The study provides reproducible simulation code in a Jupyter notebook that enables analysis of how metabolite detection coverage impacts ORA statistical outcomes.: "The study provides reproducible simulation code in a Jupyter notebook that enables analysis of how metabolite detection coverage impacts ORA statistical outcomes."
- [other] How does the fraction of metabolites detected (coverage) relative to the pathway database affect the distribution of ORA p-values and false-positive rates in metabolomics pathway analysis?: "How does the fraction of metabolites detected (coverage) relative to the pathway database affect the distribution of ORA p-values and false-positive rates in metabolomics pathway analysis?"
