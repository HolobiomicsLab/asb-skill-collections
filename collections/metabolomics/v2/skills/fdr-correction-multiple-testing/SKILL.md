---
name: fdr-correction-multiple-testing
description: Use when you have computed empirical p-values from randomized sampling
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3318
  - http://edamontology.org/topic_2269
  tools:
  - COBRApy
  - scipy.stats
  - 'INTEGRATE pipeline (Step 10: concordanceAnalysis.py)'
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans: []
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

# FDR correction for multiple testing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply Benjamini–Hochberg false discovery rate correction to empirical p-values derived from randomized sampling to control Type I error across reaction-level regulatory classifications. This ensures that significance thresholds account for the multiple hypothesis tests performed on thousands of metabolic reactions.

## When to use

You have computed empirical p-values from randomized sampling (e.g., via resampling of RPS scores or Mann–Whitney U tests across multiple reaction-level comparisons) and need to set a single, multiple-testing-corrected significance threshold that applies uniformly across all reactions in a metabolic network. Use this when the number of reactions tested is large (>100) and you want to control genome-scale false discovery rather than per-reaction type I error.

## When NOT to use

- Input is a small number of reactions (< 20 total tested) where Benjamini–Hochberg correction may be overly conservative and Bonferroni or no correction is more appropriate.
- P-values are not empirically derived or do not have a clear null distribution (e.g., analytical p-values without resampling support).
- You are testing a single reaction in isolation or performing post-hoc hypothesis testing on a pre-selected subset of reactions, where FDR correction designed for genome-scale testing is inappropriate.

## Inputs

- empirical p-values (one per metabolic reaction, derived from randomized sampling or Mann–Whitney U tests)
- reaction identifiers (SBML reaction IDs, e.g. 'ACONT', 'PFK')
- Cohen's kappa concordance coefficients (RASvsFFD, RPSvsFFD, RPSvsRAS)

## Outputs

- FDR-adjusted p-values (one per reaction)
- significance assignment (binary: pass/fail at FDR < 0.05)
- filtered reaction classification table (only reactions meeting FDR threshold)
- summary statistics (number and fraction of reactions retained after correction)

## How to apply

After computing empirical p-values for each reaction (e.g., from randomized RPS sampling or Mann–Whitney U tests on flux distributions), apply the Benjamini–Hochberg procedure: rank p-values in ascending order, compute adjusted p-values using the formula p_adj = p × (m / rank), where m is the total number of reactions tested, then filter to retain only reactions with FDR-adjusted p-value < 0.05 (or your chosen alpha). This correction is applied before classifying reactions into regulatory categories (combined, metabolic-only, transcriptional-only, or unclassified) to ensure that only statistically robust concordance signatures are assigned a regulatory class. Document the number of reactions passing the FDR threshold and compare to unadjusted counts to assess the stringency of the correction.

## Related tools

- **COBRApy** (constraint-based sampling and reaction enumeration for multi-hypothesis testing context) — https://github.com/opencobra/cobrapy
- **scipy.stats** (empirical p-value computation and statistical testing (Mann–Whitney U, t-test)) — https://scipy.org/
- **INTEGRATE pipeline (Step 10: concordanceAnalysis.py)** (implementation of FDR correction on Cohen's kappa p-values and regulatory classification) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/concordanceAnalysis.py --valLog 1.2 --weight linear --resultsMetabolomicFile resultsMetabolomic --meansFile medie_Met.csv
```

## Evaluation signals

- Adjusted p-values are monotonically increasing with rank (no inversions); all adjusted p-values ≥ corresponding unadjusted p-values.
- Number of reactions passing FDR < 0.05 threshold is smaller than number passing unadjusted p < 0.05; document fold-change in stringency.
- Comparison of regulatory classifications before and after FDR correction shows removal of low-concordance reactions; check that concordance metrics (Cohen's kappa) for passing reactions are elevated compared to rejected ones.
- Sanity check: for very large m (thousands of reactions), adjusted p-values inflate by factor ≈ m / rank for top hits; verify this relationship holds in output.
- Reproducibility check: re-run with identical input p-values and confirm adjusted p-values are identical and in same order.

## Limitations

- Benjamini–Hochberg assumes independence or positive correlation among tests; violations (e.g., correlated fluxes in tightly coupled reactions) may reduce power or inflate FDR.
- Empirical p-values derived from randomized sampling are subject to Monte Carlo error; use sufficient sample size (typically >1000 samples per cell-line pair) to stabilize adjusted p-values.
- Single global FDR threshold (α = 0.05) may be overly stringent or permissive for reactions with low prior biological plausibility; consider sensitivity analysis or reaction-class-specific thresholds.
- When a reaction substrate is missing from metabolomics measurements, the reaction is omitted from the dataset before FDR correction, potentially biasing results toward metabolically complete pathways.

## Evidence

- [other] Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR<5%.: "Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR<5%"
- [other] Compile final classification table with reaction identifiers, Cohen's kappa scores, adjusted p-values, and assigned regulatory class.: "Compile final classification table with reaction identifiers, Cohen's kappa scores, adjusted p-values, and assigned regulatory class"
- [readme] A dataset of concordance analysis (Cohen coefficient and pearson correlation) of RPS vs RAS, RPS vs FFD, RPS vs FFD, the pvalues and the adjusted pvalues: "A dataset of concordance analysis (Cohen coefficient and pearson correlation) of RPS vs RAS, RPS vs FFD, RPS vs FFD, the pvalues and the adjusted pvalues"
- [other] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
