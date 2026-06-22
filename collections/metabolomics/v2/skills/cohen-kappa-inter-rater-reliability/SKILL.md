---
name: cohen-kappa-inter-rater-reliability
description: Use when when you have two independent predictions of categorical outcomes (up/down/no-change variation signs) across multiple sample pairs and need to measure agreement beyond what would be expected by chance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  tools:
  - COBRApy
  - optGpSampler
  - Mann-Whitney U test
  - Cohen's kappa metric
  - scipy.stats or statsmodels Cohen's kappa implementation
  - COBRApy optGpSampler
  - Pandas/NumPy
  - Matplotlib/Seaborn
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72]
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions
- we first performed the Mann-Whitney U test [73] (p-value < 0.05) between the FFD distributions of each pair of the five cell lines
- We quantified the level of concordance of the 10 variation signs (1 for each pair of cell lines) for a given pair of datasets by means of the Cohen's kappa metric, which has been commonly used to
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Cohen's Kappa Agreement Analysis for Categorical Variation Signs

## Summary

Compute Cohen's kappa coefficient to quantify concordance between two categorical classifiers (e.g., RAS and RPS directional changes) across multiple pairwise comparisons, accounting for chance agreement. Essential for validating whether two independent computational predictions of reaction flux direction agree better than random.

## When to use

When you have two independent predictions of categorical outcomes (up/down/no-change variation signs) across multiple sample pairs and need to measure agreement beyond what would be expected by chance. Specifically, use this when comparing RAS directional variations derived from gene expression against RPS directional variations derived from substrate concentrations, to discriminate transcriptional from metabolic regulation.

## When NOT to use

- Input variation signs are continuous (not categorical): use Pearson or Spearman correlation instead of kappa
- More than two raters/classifiers need agreement assessment: use Fleiss' kappa or Krippendorff's alpha instead
- Reactions lack complete substrate metabolomics coverage: these are filtered out before kappa computation per the protocol

## Inputs

- RAS variation signs (up/down/no-change) per reaction and cell-line pair from t-test on normalized transcriptomics scores
- RPS variation signs (up/down/no-change) per reaction and cell-line pair from Mann–Whitney U test on sampled flux distributions
- FFD (flux distribution) variation signs per reaction and cell-line pair
- List of reactions with complete substrate metabolomics coverage (81 reactions in INTEGRATE study)
- 10 pairwise cell-line comparisons

## Outputs

- Cohen's kappa coefficient table with values for each reaction and pairwise comparison (RPSvsRAS, RPSvsFFD, RASvsFFD columns)
- Scatter plot (RPSvsRAS kappa vs RPSvsFFD kappa, colored by RASvsFFD score, labeled for kappa ≥ 0.2)
- Heatmap of Cohen's kappa values for all 81 fully-covered reactions, ordered by RPSvsFFD score
- Validation statistics comparing empirical agreement distribution to random baseline

## How to apply

For each reaction and each of the 10 pairwise cell-line comparisons, extract the sign of directional change (up=+1, down=−1, no-change=0) from both RAS (computed via t-test on normalized transcriptomics scores) and RPS (computed via Mann–Whitney U test on flux distribution samples). Compute Cohen's kappa as κ = (p_o − p_e) / (1 − p_e), where p_o is the empirical proportion of agreement and p_e is the expected proportion under random assignment. Generate scatter plots with kappa values on axes (e.g., RPSvsRAS kappa vs RPSvsFFD kappa), label points for reactions with fair or better concordance (kappa ≥ 0.2), and produce heatmaps ordered by concordance score. Validate that empirical agreement probabilities exceed those from randomized datasets and that results match published figures (e.g., Fig 4A–B).

## Related tools

- **scipy.stats or statsmodels Cohen's kappa implementation** (Direct computation of κ from contingency tables of variation signs)
- **COBRApy optGpSampler** (Generates sampled flux distributions for FFD variation sign computation via Mann–Whitney U test) — https://github.com/opencobra/cobrapy
- **Pandas/NumPy** (Data wrangling and sign extraction from RAS and RPS vectors; contingency table construction)
- **Matplotlib/Seaborn** (Scatter plot and heatmap visualization of Cohen's kappa concordance scores)

## Examples

```
python pipeline/concordanceAnalysis.py --valLog 1.2 --weight linear --resultsMetabolomicFile resultsMetabolomic --metabolic_model ENGRO2_irrev.xml --lcellLines ['MCF102A','SKBR3','MCF7','MDAMB231','MDAMB361']
```

## Evaluation signals

- Kappa values for all 81 fully-covered reactions are produced with no missing entries for reactions with complete GPR associations
- Kappa ≥ 0.2 reactions (fair agreement or better) are correctly labeled and visible in scatter and heatmap plots, matching published Fig 4A–B
- Empirical agreement proportions (p_o) exceed expected random agreement (p_e) for majority of reactions, confirming non-chance concordance
- Heatmap is properly ordered by RPSvsFFD kappa scores in descending order
- Scatter plot axis labels (RPSvsRAS, RPSvsFFD) and color scale (RASvsFFD) are internally consistent and match paper notation

## Limitations

- Cohen's kappa requires both classifiers to yield valid categorical outcomes; reactions without GPR associations produce missing RAS values and are excluded from concordance analysis
- Kappa is undefined or poorly-behaved when one category is extremely rare (e.g., all reactions classified as 'no-change'); the protocol filters to the 81 reactions with full metabolomics coverage to mitigate this
- Kappa depends on the choice of sign threshold (fold-change ≥20%, p<0.05); different thresholds for RAS and RPS tests can inflate disagreement unrelated to biological regulation
- With 10 pairwise comparisons, multiple-testing correction (Benjamini–Hochberg FDR) must be applied to empirical p-values derived from randomized baseline sampling to set significance at FDR<5%

## Evidence

- [other] compute the Cohen's kappa coefficient quantifying agreement between RAS variation sign and RPS variation sign, accounting for chance agreement: "For each reaction and each pairwise comparison, compute the Cohen's kappa coefficient quantifying agreement between RAS variation sign and RPS variation sign, accounting for chance agreement."
- [other] kappa values reported in a heatmap, with reactions ranked according to RPSvsFFD concordance scores and only those with scores greater than 0.2 displayed: "Cohen's kappa values reported in a heatmap, with reactions ranked according to RPSvsFFD concordance scores and only those with scores greater than 0.2 displayed."
- [other] empirical probability of agreement between RAS and RPS variations exceeds that expected from two independent random datasets: "Validation: verify that the produced kappa values and agreement distributions match those displayed in the published Fig 4A–B and that the empirical probability of agreement between RAS and RPS"
- [other] Filter to retain only the 81 reactions for which all substrate abundances were quantified: "Filter to retain only the 81 reactions for which all substrate abundances were quantified in the LC-MS metabolomics dataset."
- [other] Missing RPSvsRAS values occur when a reaction is not associated with a GPR: "Missing RPSvsRAS values occur when a reaction is not associated with a GPR"
