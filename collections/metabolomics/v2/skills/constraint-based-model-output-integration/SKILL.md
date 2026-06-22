---
name: constraint-based-model-output-integration
description: Use when when you have (1) transcriptomics data and a metabolic network model with GPR rules to compute RAS scores; (2) constraint-based model predictions (RPS from optGpSampler or similar) quantifying how gene expression differences translate to flux differences;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - constraint-based stoichiometric metabolic models
  - COBRApy
  - INTEGRATE pipeline (Steps 6–10)
  - Mass action kinetics (via INTEGRATE Step 9)
  - 'Statistical testing: t-test and Mann–Whitney U'
  - Cohen's kappa concordance statistic
  - Benjamini–Hochberg FDR correction
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- using constraint-based stoichiometric metabolic models as a scaffold
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

# constraint-based-model-output-integration

## Summary

Integrate constraint-based metabolic model predictions (RPS flux predictions and FFD flux distributions) with transcriptomics-derived reaction activity scores (RAS) to discriminate whether metabolic flux variation is driven by transcriptional regulation, metabolic (substrate/allosteric) regulation, or both. This multi-layer regulatory classification uses Cohen's kappa concordance between pairwise RAS-vs-FFD and RPS-vs-FFD variation sign comparisons across cell-line pairs.

## When to use

When you have (1) transcriptomics data and a metabolic network model with GPR rules to compute RAS scores; (2) constraint-based model predictions (RPS from optGpSampler or similar) quantifying how gene expression differences translate to flux differences; (3) intracellular metabolomics data enabling FFD predictions of how substrate availability changes translate to flux differences; and (4) you need to attribute observed flux changes to their regulatory origin (transcriptional vs. metabolic control) across multiple sample pairs.

## When NOT to use

- Input model lacks GPR associations for >50% of reactions, as RAS computation and GPR-dependent filtering will substantially reduce the analyzable reaction set
- Metabolomics dataset has incomplete substrate coverage (i.e., >10% of reaction substrates are missing from measurements), because FFD predictions require known metabolite concentrations for mass action kinetics
- Only single-timepoint or cross-sectional data are available without biological replicates, preventing reliable computation of p-values and variation sign determination for t-tests and Mann–Whitney U tests

## Inputs

- Constraint-based metabolic network model in SBML format with associated GPR (gene-protein-reaction) rules
- Transcriptomics dataset (RNA-seq read counts or FPKM) with multiple samples/cell-lines
- Intracellular metabolomics dataset (absolute or relative metabolite concentrations) for the same samples
- Pre-computed or newly generated RPS (Reaction Predicted Score) from optGpSampler flux sampling with transcriptomics constraints
- RAS (Reaction Activity Score) table computed from transcriptomics and GPR rules
- Pairwise cell-line comparison labels (e.g., 10 pairs from 5 cell lines)

## Outputs

- Reaction classification table (CSV) with columns: reaction ID, RASvsFFD Cohen's kappa, RPSvsRAS Cohen's kappa, p-values, FDR-adjusted p-values, regulatory class assignment (combined/metabolic-only/transcriptional-only/unclassified)
- Sign concordance matrices showing variation sign (+1/0/−1) for RAS, RPS, and FFD across each pairwise comparison
- Statistical test results (t-test and Mann–Whitney U p-values) for RAS and RPS variation detection per cell-line pair
- FFD variation dataset with log₂ fold-change ratios for flux predictions derived from metabolomics across pairs
- Visualization of regulatory landscape (e.g., scatterplots or heatmaps of Cohen's kappa scores by regulatory class)

## How to apply

First, compute RAS (Reaction Activity Score) for each reaction from transcriptomics data and GPR rules, representing enzyme abundance-driven regulation. Second, generate RPS (Reaction Predicted Score) by sampling the feasible flux regions of constraint-based models using optGpSampler with transcriptomics-constrained bounds, capturing how gene expression changes alone would alter fluxes. Third, compute FFD (Flux From Different metabolite concentrations) predictions using metabolomics data and mass action kinetics, capturing how substrate/product availability changes would alter fluxes. Fourth, for each reaction and each of the N pairwise cell-line comparisons, determine the sign of variation (up +1, down −1, no-change 0) for RAS using t-test and Mann–Whitney U test (p<0.05, fold-change ≥20%), for RPS using Mann–Whitney U on sampled flux distributions, and for FFD using log₂ fold-change ratios of metabolite concentrations. Fifth, calculate two Cohen's kappa coefficients per reaction: RASvsFFD and RPSvsRAS, each measuring concordance of variation signs across all N pairwise comparisons—positive kappa indicates consistent co-direction. Sixth, apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS resampling (significance threshold FDR<5%). Finally, classify each reaction into four categories: (a) positive RASvsFFD AND positive RPSvsRAS = combined transcriptional and metabolic control; (b) positive RPSvsFFD AND negative RPSvsRAS = metabolic control only; (c) negative both with high RASvsFFD = transcriptional control only; (d) positive RPSvsRAS but negative RPSvsFFD = unclassified. Output a comprehensive classification table with reaction identifiers, both Cohen's kappa scores, adjusted p-values, and assigned regulatory class.

## Related tools

- **COBRApy** (Constraint-based metabolic model construction, optGpSampler uniform sampling of flux distributions, and flux variability analysis)
- **INTEGRATE pipeline (Steps 6–10)** (Automated randomSampling of feasible flux regions, mannWhitneyUTest on sampled RPS distributions, rasTtest on RAS scores, createMetabolicDataset for FFD preparation, and concordanceAnalysis for Cohen's kappa calculation and regulatory classification) — https://github.com/qLSLab/integrate
- **Mass action kinetics (via INTEGRATE Step 9)** (Compute predicted flux changes from intracellular metabolomics (FFD) by applying mass action law to metabolite concentration ratios)
- **Statistical testing: t-test and Mann–Whitney U** (Determine statistical significance and direction of variation in RAS scores and RPS flux samples across cell-line pairs (p<0.05 threshold))
- **Cohen's kappa concordance statistic** (Measure agreement between variation signs (up/down/no-change) of RAS-vs-FFD and RPS-vs-RAS across pairwise comparisons; linear weighting applied)
- **Benjamini–Hochberg FDR correction** (Control false discovery rate on empirical p-values derived from randomized RPS resampling; threshold FDR<5%)

## Examples

```
python pipeline/concordanceAnalysis.py --valLog 1.2 --weight linear --resultsMetabolomicFile resultsMetabolomic --metabolic_model ENGRO2_irrev.xml --lcellLines MCF102A SKBR3 MCF7 MDAMB231 MDAMB361 --meansFile medie_Met.csv
```

## Evaluation signals

- Cohen's kappa coefficients fall within valid range (−1 to +1); positive values indicate concordant variation signs, negative values indicate discordant directions
- FDR-adjusted p-values derived from randomized resampling are correctly applied; all reported kappa values meet FDR<5% significance threshold
- All four regulatory classes (combined, metabolic-only, transcriptional-only, unclassified) are represented; class assignments are logically consistent with sign patterns (e.g., positive RASvsFFD AND positive RPSvsRAS → combined, not metabolic-only)
- Reactions with missing GPR associations or incomplete metabolomics substrate coverage are excluded from the concordance analysis; the final table documents filtering steps and justifies reaction losses
- Variation signs (−1, 0, +1) are consistent across RAS t-test/Mann–Whitney, RPS Mann–Whitney on flux samples, and FFD log₂ fold-change thresholds (fold-change ≥1.2 or ≥20% for p<0.05)

## Limitations

- Reactions without GPR associations are excluded from RAS-RPS concordance analysis, potentially missing metabolically important reactions not tied to measured gene expression
- If any single reaction substrate is absent from the intracellular metabolomics dataset, the entire reaction is omitted from FFD analysis, reducing coverage when metabolite measurement is incomplete
- Direct determination of metabolic fluxes through labeled substrate tracers is not performed; RPS and FFD predictions are model-based and assume the constraint-based model accurately captures stoichiometry, reversibility, and flux constraints
- Cohen's kappa concordance requires consistent variation signs across multiple pairwise comparisons; transient or condition-specific regulation may be missed if sign direction changes between pairs
- FFD predictions depend on the validity of mass action kinetics and absolute metabolite concentration measurements; relative abundance data without absolute quantification may not accurately reflect flux changes

## Evidence

- [other] For each of the 10 pairwise cell-line comparisons, compute the sign of variation (up +1, down −1, no-change 0) for RAS and RPS using t-test and Mann–Whitney U test (p<0.05) with fold-change threshold ≥20%. Compute the sign of FFD variation for each pair using Mann–Whitney U test on sampled flux distributions with log₂ fold-change ratio.: "compute the sign of variation (up +1, down −1, no-change 0) for RAS and RPS using t-test and Mann–Whitney U test (p<0.05) with fold-change threshold ≥20%. Compute the sign of FFD variation for each"
- [other] For each reaction, calculate two Cohen's kappa coefficients: RASvsFFD and RPSvsRAS, quantifying concordance of variation signs across the 10 pairwise comparisons.: "For each reaction, calculate two Cohen's kappa coefficients: RASvsFFD and RPSvsRAS, quantifying concordance of variation signs across the 10 pairwise comparisons."
- [other] Classify reactions into four categories: positive RASvsFFD and RPSvsRAS (combined transcriptional and metabolic), positive RPSvsFFD and negative RPSvsRAS (metabolic only), negative both scores with high RASvsFFD (transcriptional only), or positive RPSvsRAS but negative RPSvsFFD (unclassified/other).: "Classify reactions into four categories: positive RASvsFFD and RPSvsRAS (combined transcriptional and metabolic), positive RPSvsFFD and negative RPSvsRAS (metabolic only), negative both scores with"
- [other] Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR<5%.: "Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR<5%."
- [other] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [other] Missing RPSvsRAS values occur when a reaction is not associated with a GPR: "Missing RPSvsRAS values occur when a reaction is not associated with a GPR"
- [abstract] We discriminate fluxes regulated at the metabolic and/or gene expression level by intersecting these two outputs: "We discriminate fluxes regulated at the metabolic and/or gene expression level by intersecting these two outputs"
- [intro] Each metabolic flux depends on at least two intertwined regulatory layers [8–10]: "Each metabolic flux depends on at least two intertwined regulatory layers"
