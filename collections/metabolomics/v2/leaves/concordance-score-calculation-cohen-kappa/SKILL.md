---
name: concordance-score-calculation-cohen-kappa
description: Use when you have paired quantitative variation patterns for the same
  set of reactions across multiple biological samples (cell lines) and need to discriminate
  whether flux variations correlate monotonically with substrate abundance changes
  (metabolic control) versus gene expression changes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0208
  - http://edamontology.org/topic_3407
  tools:
  - constraint-based stoichiometric metabolic models
  - Flux Variability Analysis (FVA)
  - Cohen's kappa coefficient (statistical test)
  - concordanceAnalysis.py
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate_cq
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate_cq
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

# concordance-score-calculation-cohen-kappa

## Summary

Compute Cohen's kappa concordance coefficients between paired reaction metrics (e.g., RPS vs FFD, RAS vs RPS) to quantify agreement in variation patterns across cell lines, enabling discrimination of metabolic control mechanisms (substrate-driven vs. transcriptionally-driven).

## When to use

Apply this skill when you have paired quantitative variation patterns for the same set of reactions across multiple biological samples (cell lines) and need to discriminate whether flux variations correlate monotonically with substrate abundance changes (metabolic control) versus gene expression changes (transcriptional control). Specifically, use it after computing RPS (Reaction Propensity Score) and FFD (Feasible Flux Distribution) concordance values, and RAS (Reaction Activity Score) variation signs, to identify reactions with RPSvsFFD kappa ≥ 0.2 paired with RPSvsRAS kappa < 0.2.

## When NOT to use

- When substrate abundances are incompletely measured in metabolomics (missing metabolites will exclude the corresponding reactions from analysis).
- When only transcriptomics or only metabolomics data are available; this skill requires both gene expression and intracellular metabolite quantification to compute paired variation metrics.
- When cell line sample size is very small (< 3 pairs); Cohen's kappa stability and statistical power degrade with few comparison units.

## Inputs

- RPS (Reaction Propensity Score) matrix: reactions × cell lines with substrate propensity values
- FFD (Feasible Flux Distribution) samples: reactions × steady-state solutions across cell-line models
- RAS (Reaction Activity Score) variation signs: reactions × cell lines with transcriptional activity indicators
- Metabolomics measurements: reaction substrates with complete quantification across cell lines
- Irreversible metabolic model (SBML or MAT format) with GPR rules and reaction definitions

## Outputs

- Concordance score matrix: reactions × metric pairs (RPSvsFFD, RPSvsRAS) with Cohen's kappa coefficients
- Filtered reaction set: 13 (or sample-size appropriate count) metabolically controlled reactions meeting RPSvsFFD ≥ 0.2 and RPSvsRAS < 0.2 thresholds
- Tabulated results: reaction IDs, concordance scores, cell-line-specific RPS distributions, FFD distributions (10,000 sampled steady-state solutions per cell line)
- Heatmap visualization: RPSvsRAS and RPSvsFFD concordance scores for reactions with RPSvsFFD > 0.2

## How to apply

For each reaction with complete substrate quantification (all substrates measured in metabolomics), compute Cohen's kappa coefficient between pairs of variation metrics across all cell-line comparisons. Apply a two-threshold filtering strategy: retain reactions where RPSvsFFD Cohen's kappa ≥ 0.2 (indicating fair concordance between substrate propensity and feasible flux) AND RPSvsRAS Cohen's kappa < 0.2 (indicating poor concordance with transcriptional activity). This dual-threshold logic identifies reactions whose flux variations are determined by substrate availability rather than transcriptional regulation. Use linear weighting on the kappa statistic when computing concordance. Tabulate the final set with their concordance scores and cell-line-specific RPS and FFD distributions for downstream interpretation.

## Related tools

- **constraint-based stoichiometric metabolic models** (scaffold for defining reaction stoichiometry, GPR associations, and steady-state feasible flux space; enables FFD sampling across cell-line-specific constraints) — https://github.com/qLSLab/integrate
- **Flux Variability Analysis (FVA)** (compute maximum feasible flux for each reaction to normalize RPS and FFD values before concordance calculation) — https://github.com/qLSLab/integrate
- **Cohen's kappa coefficient (statistical test)** (quantify agreement between two categorical or ordinal variation patterns (e.g., RPS vs FFD sign concordance); weight='linear' in INTEGRATE implementation) — https://github.com/qLSLab/integrate
- **concordanceAnalysis.py** (main pipeline script; computes Cohen's kappa concordance and Pearson correlation for RPS vs RAS and RPS vs FFD, applies thresholds, generates heatmap and tabulated concordance results) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/concordanceAnalysis.py --valLog 1.2 --weight linear --resultsMetabolomicFile resultsMetabolomic --metabolic_model ENGRO2_irrev.xml --lcellLines MCF102A SKBR3 MCF7 MDAMB231 MDAMB361 --meansFile medie_Met.csv
```

## Evaluation signals

- Output concordance scores fall within the valid range [-1, 1] for Cohen's kappa, with expected mean near 0 for uncorrelated metric pairs and ≥ 0.2 for metabolically controlled reactions.
- Filtered reaction count and RPSvsFFD score distribution match reported findings (e.g., 13 reactions with RPSvsFFD kappa ≥ 0.2 and RPSvsRAS kappa < 0.2 in the ENGRO2 breast cancer model).
- Heatmap visualization shows clear separation: metabolically controlled reactions cluster in the upper-left quadrant (high RPSvsFFD, low RPSvsRAS); transcriptionally controlled reactions cluster in the upper-right (high both).
- Reactions excluded due to missing substrate measurements are documented; total reactions in concordance analysis ≤ total reactions in model, with completeness documented in metadata.
- Cell-line-specific RPS and FFD distributions are non-empty and display expected variance (e.g., 10,000 sampled solutions per model per cell line); no NaN or infinity values in reported scores.

## Limitations

- Limited metabolite coverage in metabolomics dataset constrains the number of reactions analyzable; reactions with any missing substrate are excluded entirely, reducing statistical power.
- Cohen's kappa concordance alone cannot discriminate allosteric regulation, product inhibition, or cofactor/prosthetic group effects; these regulatory mechanisms require additional enzymatic activity data.
- Enzymatic activity is neglected in metabolic regulation prediction; only substrate availability is considered via the mass action law formulation, potentially missing kinetic bottlenecks.
- FFD distributions are limited to 10,000 sampled steady-state solutions per cell line for computational visualization; very rare feasible regions may be undersampled.
- Agreement between gene expression and substrate availability but disagreement with actual flux suggests model inaccuracy or missing regulatory layers; cannot be fully resolved without additional experimental data (e.g., enzyme activity assays, post-translational modifications).

## Evidence

- [other] 13 reactions in ENGRO2 were identified as metabolically regulated, characterized by RPSvsFFD concordance scores above 0.2 paired with RPSvsRAS scores below this threshold: "13 reactions in ENGRO2 were identified as metabolically regulated, characterized by RPSvsFFD concordance scores above 0.2 paired with RPSvsRAS scores below this threshold or missing"
- [other] Compute Cohen's kappa concordance coefficient between RPS and FFD variations for each reaction pair across cell lines. Compute Cohen's kappa concordance coefficient between RAS and RPS variations for each reaction pair across cell lines.: "Compute Cohen's kappa concordance coefficient between RPS and FFD variations for each reaction pair across cell lines. 4. Compute Cohen's kappa concordance coefficient between RAS and RPS variations"
- [other] Apply concordance threshold: retain reactions with RPSvsFFD Cohen's kappa ≥ 0.2 (fair concordance) and RPSvsRAS Cohen's kappa < 0.2 (poor concordance), indicating metabolic control independent of transcriptional regulation.: "Apply concordance threshold: retain reactions with RPSvsFFD Cohen's kappa ≥ 0.2 (fair concordance) and RPSvsRAS Cohen's kappa < 0.2 (poor concordance), indicating metabolic control"
- [results] Reactions included in concordance analysis only if quantification of all substrate abundances was available: "Fig 4A reports the concordance level variations for the 81 metabolic reactions of ENGRO2 for which quantification of all substrate abundances was available"
- [readme] weight: weight on the Kappa Cohen. Default value: 'linear': "weight: weight on the Kappa Cohen. Default value: 'linear'"
- [results] For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted: "For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted"
- [intro] evidence for a monotonic relationship between variations in fluxes and variations in substrate abundances, and for a concurrent non-monotonic relationship between flux and gene expression: "evidence for a monotonic relationship between variations in fluxes and variations in substrate abundances, and for a concurrent non-monotonic relationship between flux"
- [results] Allosteric regulation, product inhibition, and cofactor/prosthetic group effects cannot be discriminated from the current analysis without additional data: "Allosteric regulation, product inhibition, and cofactor/prosthetic group effects cannot be discriminated from the current analysis without additional data"
