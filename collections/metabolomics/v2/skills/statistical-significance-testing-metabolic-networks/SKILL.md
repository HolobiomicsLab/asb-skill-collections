---
name: statistical-significance-testing-metabolic-networks
description: Use when you have sampled flux distributions from two or more constraint-based
  metabolic models representing different biological conditions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_2259
  tools:
  - constraint-based stoichiometric metabolic models
  - COBRApy
  - optGpSampler
  - Mann-Whitney U test
  - Mann-Whitney U test (scipy.stats)
  - INTEGRATE pipeline
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- using constraint-based stoichiometric metabolic models as a scaffold
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72]
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72], and we sampled a million steady state solutions
- we first performed the Mann-Whitney U test [73] (p-value < 0.05) between the FFD
  distributions of each pair of the five cell lines
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009337
  all_source_dois:
  - 10.1371/journal.pcbi.1009337
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Statistical Significance Testing in Metabolic Networks

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply Mann-Whitney U tests and t-tests to determine whether directional changes in reaction activity scores (RAS) or metabolite abundances are statistically significant across pairwise sample comparisons in constraint-based metabolic models. This skill identifies which metabolic reactions exhibit genuine differential regulation between conditions.

## When to use

You have sampled flux distributions from two or more constraint-based metabolic models representing different biological conditions (e.g., cell lines, disease states) and need to test whether observed differences in reaction flux directions or RAS values are statistically significant rather than due to chance. Apply this when you have computed RAS scores from transcriptomics data or sampled flux distributions and want to assign directional signs (up, down, no-change) to individual reactions for downstream concordance analysis.

## When NOT to use

- Input samples are unpaired or from the same biological replicate; Mann-Whitney U requires independent samples.
- Reaction flux data are already discretized into binary or ternary categories; statistical testing is redundant.
- You have fewer than ~3–5 sampled solutions per condition; power to detect differences is too low.
- Metabolic model has no GPR associations; RAS cannot be computed and transcriptional regulation cannot be tested.

## Inputs

- Reaction flux distribution samples (CSV format, one row per sample solution, columns per reaction)
- RAS (Reaction Activity Score) vectors (CSV with reactions as rows, cell lines/samples as columns)
- Metadata identifying sample pairs for pairwise comparisons
- Irreversible metabolic model (SBML or .mat) for reaction splitting (optional, for t-test variant)

## Outputs

- Directional change assignments per reaction per pairwise comparison (up/down/no-change)
- Mann-Whitney U test p-values and adjusted p-values per reaction per comparison
- t-test results for RAS scores (if computed)
- Formatted dataset with sign assignments for downstream concordance analysis (kappa calculation)

## How to apply

For each reaction and each pairwise comparison between samples: (1) Extract reaction flux distributions from constraint-based model sampling output or RAS score vectors from GPR-based calculations. (2) Apply Mann-Whitney U test (p < 0.05) to determine if the distributions differ significantly between the two samples. (3) Assign directional change based on test result: record 'up' if the first sample's median is significantly higher, 'down' if lower, or 'no-change' if not significantly different. (4) For RAS scores specifically, you may also compute t-tests after splitting reversible reactions into forward/backward components. (5) Filter reactions to include only those with complete data (e.g., all substrates quantified in metabolomics if concordance analysis follows). The sign assignment from statistical testing becomes the ground truth for comparing predicted (RAS-based) versus observed (metabolomics-based) directional changes.

## Related tools

- **COBRApy** (Loads metabolic models, integrates constraints, and manages reaction/metabolite identifiers for statistical testing workflow) — https://github.com/opencobra/cobrapy
- **optGpSampler** (Samples the feasible flux region of constraint-based models to generate flux distributions for Mann-Whitney U testing)
- **Mann-Whitney U test (scipy.stats)** (Computes statistical significance of differences in reaction flux or RAS distributions between pairwise samples)
- **INTEGRATE pipeline** (Complete workflow that computes RAS from transcriptomics and metabolomic propensity scores, then applies Mann-Whitney U and t-tests for directional assignment) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/mannWhitneyUTest.py timeStampInput nSamples
```

## Evaluation signals

- Directional sign assignments (up/down/no-change) for all reactions in each pairwise comparison must be exhaustive and mutually exclusive; no missing values except for reactions excluded by filter criteria.
- Reported p-values must fall in [0, 1]; verify no numerical errors or unsigned comparisons led to invalid p-values.
- When Cohen's kappa is computed afterward using the directional signs from this test, kappa values should be interpretable (range [−1, 1]) and agreement frequencies should exceed chance expectations for concordant reaction pairs (empirical vs. random validation check).
- Reactions passing significance threshold (p < 0.05) should show larger effect sizes (e.g., greater separation of medians or means) than non-significant reactions; sanity-check rank order.
- If multiple testing correction is applied (e.g., Benjamini-Hochberg FDR), adjusted p-values should be ≥ raw p-values and no reaction should have adjusted p-value < raw p-value.

## Limitations

- Statistical power depends on the number of sampled solutions per model; the README recommends multiple batches and large nSamples, but with too few samples per condition the test may fail to detect genuine differences.
- Mann-Whitney U test is rank-based and non-parametric, so it is robust to non-normal distributions but loses power if sample sizes are very small (< 5 per group).
- When a single reaction substrate is missing from metabolomics measurements, the entire reaction is omitted from the dataset, reducing the pool of reactions available for concordance analysis post-testing.
- Reactions without GPR associations cannot have RAS computed, so t-test variant of this skill cannot be applied to them; they are excluded from RAS-RPS concordance analysis.
- The choice of significance threshold (p < 0.05) and log2 fold-change threshold (default 1.2 for metabolomics comparisons) are arbitrary; results are sensitive to these parameters and should be reported explicitly.

## Evidence

- [other] For each of the 10 pairwise cell-line comparisons, perform Mann-Whitney U testing (p < 0.05) on RAS and RPS distributions to determine the sign of directional change (up, down, or no-change) for each reaction.: "For each of the 10 pairwise cell-line comparisons, perform Mann-Whitney U testing (p < 0.05) on RAS and RPS distributions to determine the sign of directional change (up, down, or no-change) for each"
- [other] INTEGRATE first computes differential expression of reactions from transcriptomics data (transcriptional regulation only): "INTEGRATE first computes differential expression of reactions from transcriptomics data (transcriptional regulation only)"
- [readme] For each pair of input cell line c_1 and c_2, a file returning the output of Mann-Whitney U test. ... For each pair of input cell line c_1 and c_2, a file returning the output of t-test named 'ras_' + c_1 +'_vs_' + c_2 + '.csv': "For each pair of input cell line c_1 and c_2, a file returning the output of Mann-Whitney U test"
- [other] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [other] verify that the produced kappa values and agreement distributions match those displayed in the published Fig 4A–B and that the empirical probability of agreement between RAS and RPS variations exceeds that expected from two independent random datasets: "verify that the empirical probability of agreement between RAS and RPS variations exceeds that expected from two independent random datasets"
