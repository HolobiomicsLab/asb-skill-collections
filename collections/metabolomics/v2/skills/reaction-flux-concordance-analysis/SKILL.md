---
name: reaction-flux-concordance-analysis
description: Use when you have computed RAS (Reaction Activity Scores) from transcriptomics and GPR rules, RPS (Reaction Propensity Scores) from intracellular metabolomics via mass-action kinetics, and flux distribution differences (FFD) from constraint-based sampling across multiple biological samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3418
  tools:
  - COBRApy
  - optGpSampler
  - Mann-Whitney U test
  - Mann–Whitney U test (SciPy)
  - Cohen's kappa metric (scikit-learn or manual implementation)
  - Benjamini–Hochberg FDR correction
  - concordanceAnalysis.py (INTEGRATE pipeline Step 10)
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72]
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions
- we first performed the Mann-Whitney U test [73] (p-value < 0.05) between the FFD distributions of each pair of the five cell lines
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

# Reaction-Flux Concordance Analysis

## Summary

Quantify agreement between transcriptional (RAS) and metabolic (RPS) regulation signals for metabolic reactions using Cohen's kappa concordance across pairwise cell-line comparisons. This skill discriminates whether flux changes arise from gene expression differences, substrate availability differences, or both regulatory layers combined.

## When to use

Apply this skill when you have computed RAS (Reaction Activity Scores) from transcriptomics and GPR rules, RPS (Reaction Propensity Scores) from intracellular metabolomics via mass-action kinetics, and flux distribution differences (FFD) from constraint-based sampling across multiple biological samples. Use it to classify which metabolic reactions are controlled at the transcriptional level, metabolic level (substrate-driven), or both simultaneously—essential for identifying intervention targets in cancer or metabolic engineering.

## When NOT to use

- Reactions lacking complete substrate quantification in the metabolomics dataset—these are filtered out and cannot be assigned RPS scores or FFD comparisons.
- Reactions without GPR (Gene-Protein-Reaction) associations—RAS computation requires enzyme gene expression data linked via valid GPR rules; reactions missing GPRs have undefined RASvsRAS concordance.
- When only transcriptomics or metabolomics is available, not both—the concordance skill requires parallel predictions from both regulatory layers to compute meaningful kappa coefficients and identify control mode.

## Inputs

- RAS (Reaction Activity Score) matrix: reactions × cell lines, computed from RNA-seq counts and GPR rules
- RPS (Reaction Propensity Score) matrix: reactions × cell lines, computed as product of substrate concentrations raised to stoichiometric coefficients
- FFD (Flux Distribution Difference) sampled solutions: sets of flux vectors for each cell line from optGpSampler uniform sampling
- Reaction metadata: reaction IDs, stoichiometric coefficients, substrate identifiers, GPR associations
- Metabolomics quantification matrix: intracellular metabolite abundances (LC-MS intensity) for substrates across cell lines and replicates

## Outputs

- Concordance classification table: reaction ID, RASvsFFD kappa, RPSvsFFD kappa, RASvsRPS kappa, adjusted p-value (FDR < 5%), regulatory class assignment (transcriptional/metabolic/combined/unclassified)
- Scatter plot: RPSvsRAS kappa (y-axis) vs. RPSvsFFD kappa (x-axis), colored by RASvsFFD concordance score, labeled by reaction ID for kappa ≥ 0.2
- Heatmap: RASvsFFD and RPSvsFFD kappa values for all reactions (rows), ordered by RPSvsFFD score (columns: 10 pairwise comparisons or aggregated)

## How to apply

For each of the C(n,2) pairwise comparisons among n cell lines, compute directional change signs (up +1, down −1, no-change 0) for RAS and RPS using Mann–Whitney U test (p < 0.05) with fold-change threshold ≥20%. In parallel, compute FFD variation signs from Mann–Whitney U testing on sampled flux distributions. For each reaction, calculate two Cohen's kappa coefficients—RASvsFFD and RPSvsFFD—to quantify concordance of directional signs across all pairwise comparisons. Classify reactions into four regulatory categories: (1) positive kappa for both RASvsFFD and RPSvsFFD indicates combined transcriptional and metabolic control; (2) positive RPSvsFFD with negative RASvsFFD indicates metabolic control only; (3) negative both with high RASvsFFD indicates transcriptional control only; (4) other sign patterns indicate unclassified regulation. Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR < 5%. Retain only reactions with concordance score ≥ 0.2 for visualization and downstream interpretation.

## Related tools

- **COBRApy** (Constraint-based metabolic model representation and flux sampling via optGpSampler) — https://github.com/opencobra/cobrapy
- **Mann–Whitney U test (SciPy)** (Statistical test for directional change in RAS, RPS, and FFD distributions between cell-line pairs)
- **Cohen's kappa metric (scikit-learn or manual implementation)** (Quantification of concordance between RAS vs FFD and RPS vs FFD sign agreements across pairwise comparisons)
- **Benjamini–Hochberg FDR correction** (Multiple-testing correction on empirical p-values from randomized RPS sampling; sets significance threshold FDR < 5%)
- **concordanceAnalysis.py (INTEGRATE pipeline Step 10)** (Unified computation of Cohen's kappa, classification logic, and visualization (scatter and heatmap)) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/concordanceAnalysis.py --valLog 1.2 --weight linear --resultsMetabolomicFile resultsMetabolomic --metabolic_model ENGRO2_irrev.xml --lcellLines MCF102A MDAMB231 SKBR3 MCF7 MDAMB361
```

## Evaluation signals

- Kappa values range from −1 to +1; kappa > 0.2 indicates fair or better concordance. Verify that reported kappa distributions match published Fig 4A–B and that agreement between RAS and RPS variations exceeds that expected from two independent random datasets.
- FDR-corrected p-values for all classified reactions must be ≤ 0.05 after Benjamini–Hochberg correction; empirical p-values should be recomputable from randomized RPS sampling percentiles.
- Reaction counts by regulatory class (transcriptional, metabolic, combined, unclassified) must match published supplementary tables and be consistent with biological expectations for the cell-line pair (e.g., cancer lines show higher metabolic control than normal lines).
- Heatmap and scatter plot visual structure: reactions displayed must have kappa ≥ 0.2; color gradients and axes labels must correspond exactly to kappa values; only reactions with complete substrate metabolomics coverage appear in final output.
- Reproducibility: concordance results must be identical when recomputed using the same random seed for RPS sampling and the same fold-change threshold (≥20%) and statistical test parameters (p < 0.05).

## Limitations

- Reactions with missing substrate metabolomics coverage are excluded from concordance analysis, reducing the fraction of model reactions that can be classified—trade-off between model size and data completeness (81 fully covered reactions in the breast cancer case study).
- Cohen's kappa concordance assumes independence of RAS and RPS signals; if enzyme expression and substrate concentration are coupled (e.g., through feedback), kappa may underestimate true regulatory integration.
- FDR correction applied to empirical p-values derived from randomized RPS sampling; if RPS sampling is biased (e.g., insufficient sample size or poor constraint feasibility), p-value calibration may be unreliable.
- Directional change detection relies on fold-change threshold (≥20%) and statistical significance (p < 0.05); borderline reactions with small fold-changes or marginal p-values may be misclassified as 'no-change' and artificially inflate kappa values.
- The method assumes steady-state metabolic behavior and linear mass-action kinetics; transient dynamics, allosteric regulation, or post-translational modification are not explicitly modeled and may be misattributed to transcriptional or metabolic control.

## Evidence

- [other] For each of the 10 pairwise cell-line comparisons, compute the sign of variation (up +1, down −1, no-change 0) for RAS and RPS using t-test and Mann–Whitney U test (p<0.05) with fold-change threshold ≥20%.: "For each of the 10 pairwise cell-line comparisons, compute the sign of variation (up +1, down −1, no-change 0) for RAS and RPS using t-test and Mann–Whitney U test (p<0.05) with fold-change threshold"
- [other] For each reaction, calculate two Cohen's kappa coefficients: RASvsFFD and RPSvsRAS, quantifying concordance of variation signs across the 10 pairwise comparisons.: "For each reaction, calculate two Cohen's kappa coefficients: RASvsFFD and RPSvsRAS, quantifying concordance of variation signs across the 10 pairwise comparisons"
- [other] Classify reactions into four categories: positive RASvsFFD and RPSvsRAS (combined transcriptional and metabolic), positive RPSvsFFD and negative RPSvsRAS (metabolic only), negative both scores with high RASvsFFD (transcriptional only), or positive RPSvsRAS but negative RPSvsFFD (unclassified/other).: "Classify reactions into four categories: positive RASvsFFD and RPSvsRAS (combined transcriptional and metabolic), positive RPSvsFFD and negative RPSvsRAS (metabolic only), negative both scores with"
- [other] Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR<5%.: "Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR<5%"
- [other] Filter to retain only the 81 reactions for which all substrate abundances were quantified in the LC-MS metabolomics dataset.: "Filter to retain only the 81 reactions for which all substrate abundances were quantified in the LC-MS metabolomics dataset"
- [abstract] We discriminate fluxes regulated at the metabolic and/or gene expression level by intersecting these two outputs: "We discriminate fluxes regulated at the metabolic and/or gene expression level by intersecting these two outputs"
- [other] Concordance analysis of RAS and RPS directional variations across the 81 metabolic reactions with full substrate abundances yields Cohen's kappa values reported in a heatmap, with reactions ranked according to RPSvsFFD concordance scores and only those with scores greater than 0.2 displayed.: "Concordance analysis of RAS and RPS directional variations across the 81 metabolic reactions with full substrate abundances yields Cohen's kappa values reported in a heatmap, with reactions ranked"
