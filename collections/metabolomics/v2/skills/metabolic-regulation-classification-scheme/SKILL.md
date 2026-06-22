---
name: metabolic-regulation-classification-scheme
description: Use when when you have computed Reaction Activity Scores (RAS) from transcriptomics and GPR rules, Reaction Presence Scores (RPS) from RAS normalized flux predictions, and Flux Fold-change Distributions (FFD) from metabolomic data and mass-action constraints across multiple sample pairs, and you.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - constraint-based stoichiometric metabolic models
  - COBRApy
  - mannWhitneyUTest.py
  - rasTtest.py
  - concordanceAnalysis.py
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

# metabolic-regulation-classification-scheme

## Summary

A concordance-based classification method that assigns metabolic reactions into four regulatory categories (combined transcriptional and metabolic, metabolic-only, transcriptional-only, or unclassified) by measuring Cohen's kappa agreement between RAS-vs-FFD and RPS-vs-FFD variation signs across pairwise cell-line comparisons. This skill discriminates whether differences in metabolic flux originate from transcriptional control of enzyme abundance or from metabolic control via substrate availability.

## When to use

When you have computed Reaction Activity Scores (RAS) from transcriptomics and GPR rules, Reaction Presence Scores (RPS) from RAS normalized flux predictions, and Flux Fold-change Distributions (FFD) from metabolomic data and mass-action constraints across multiple sample pairs, and you need to assign regulatory mechanism(s) to each reaction to guide therapeutic targeting or metabolic engineering design.

## When NOT to use

- When reactions lack GPR associations—these reactions cannot be included in RPS-RAS concordance analysis and will have missing RPSvsRAS values.
- When a single substrate for a reaction is missing from metabolomics measurements—the entire reaction must be omitted from FFD-based classification.
- When you have only cross-sectional (single timepoint) transcriptomics or metabolomics data and cannot form meaningful pairwise comparisons across ≥2 biological conditions.

## Inputs

- Reaction Activity Scores (RAS) computed from transcriptomics data and GPR rules for all reactions and sample pairs
- Reaction Presence Scores (RPS) from normalized RAS-derived flux constraints within constraint-based models
- Flux Fold-change Distributions (FFD) sampled from flux feasible regions using Mann–Whitney U test on metabolomics-constrained models
- Irreversible metabolic model in SBML or MAT format (reactions and GPRs split)
- Cell-line pair identifiers (10 pairwise comparisons minimum)

## Outputs

- Classification table with columns: reaction identifier, RASvsFFD Cohen's kappa, RPSvsRAS Cohen's kappa, empirical p-value, FDR-adjusted p-value, assigned regulatory class (combined/metabolic-only/transcriptional-only/unclassified)
- Concordance analysis dataset with Cohen coefficients and Pearson correlations for each pairwise comparison

## How to apply

For each of the 10 pairwise cell-line comparisons, compute the sign of variation (up +1, down −1, no-change 0) for RAS using t-test (p<0.05) with fold-change threshold ≥20%, and for RPS and FFD using Mann–Whitney U test (p<0.05). Then calculate two Cohen's kappa coefficients for each reaction: RASvsFFD and RPSvsRAS, which quantify concordance of variation signs across all 10 pairwise comparisons. Classify reactions based on kappa sign patterns: positive both scores → combined transcriptional and metabolic control; positive RPSvsFFD and negative RPSvsRAS → metabolic-only control; negative both scores with high RASvsFFD → transcriptional-only control; positive RPSvsRAS but negative RPSvsFFD → unclassified/other. Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling, setting significance threshold at FDR<5%. Compile final classification table with reaction identifiers, both kappa scores, adjusted p-values, and assigned regulatory class.

## Related tools

- **COBRApy** (Constraint-based modeling library used to construct cell-line-specific models and sample flux distributions with optGpSampler for FFD computation) — https://github.com/opencobra/cobrapy
- **constraint-based stoichiometric metabolic models** (Scaffold for integrating transcriptomics (via RAS) and metabolomics (via FFD) to predict reaction-level flux changes)
- **mannWhitneyUTest.py** (Computes Mann–Whitney U test to determine FFD and RPS variation signs (up/down/no-change) across pairwise comparisons) — https://github.com/qLSLab/integrate
- **rasTtest.py** (Computes t-test on RAS scores to determine transcriptional variation signs across pairwise comparisons) — https://github.com/qLSLab/integrate
- **concordanceAnalysis.py** (Orchestrates Cohen's kappa concordance calculation, FDR correction, and final regulatory classification of reactions) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/concordanceAnalysis.py --valLog 1.2 --weight linear --resultsMetabolomicFile resultsMetabolomic --metabolic_model ENGRO2_irrev.xml --lcellLines MCF102A SKBR3 MCF7 MDAMB231 MDAMB361 --meansFile medie_Met.csv
```

## Evaluation signals

- All 10 pairwise cell-line comparisons yield valid variation sign matrices (up/down/no-change) for RAS, RPS, and FFD with no missing values for included reactions.
- Cohen's kappa values fall within the expected range [−1, +1] and satisfy FDR<5% threshold after Benjamini–Hochberg correction; kappa>0.41 typically indicates moderate to substantial concordance.
- Reactions are distributed across all four regulatory classes with counts that reflect known biology (e.g., more combined regulation in central metabolism, more transcriptional-only in anabolic pathways).
- When visualizing a sample reaction (e.g., ACONT as in the README), variation signs are consistent across both RASvsFFD and RPSvsRAS comparisons, matching the assigned regulatory class.
- Final classification table contains no reactions with both RASvsFFD and RPSvsRAS = NaN unless they lack GPR associations or have missing metabolomics substrates—these omissions are documented.

## Limitations

- Reactions without GPR associations cannot be classified because RPS cannot be computed; these must be pre-filtered before concordance analysis.
- When any single reaction substrate is missing from metabolomics measurements, the entire reaction is omitted from FFD computation and concordance analysis, reducing coverage of metabolic network.
- Direct metabolic flux determination through labeled substrates is not employed; FFD is inferred via mass-action law on metabolomics data and flux sampling, which may not capture non-steady-state dynamics or allosteric effects not encoded in the model.
- Classification robustness depends on statistical power of pairwise comparisons; sparse or noisy transcriptomics or metabolomics data may increase false-positive or false-negative regulatory assignments.
- The scheme assumes that variation sign concordance reflects causal regulation; bidirectional feedback loops or indirect metabolic control may be misclassified as transcriptional-only or metabolic-only.

## Evidence

- [other] Reactions are classified by measuring Cohen's kappa concordance between RAS-vs-FFD and RPS-vs-FFD variation signs: positive concordance for both indicates combined regulation, positive RPSvsFFD with negative RASvsFFD indicates metabolic control only, and positive values for both RASvsFFD and RASvsRPS indicates transcriptional and metabolic regulation.: "Reactions are classified by measuring Cohen's kappa concordance between RAS-vs-FFD and RPS-vs-FFD variation signs: positive concordance for both indicates combined regulation, positive RPSvsFFD with"
- [other] For each reaction, calculate two Cohen's kappa coefficients: RASvsFFD and RPSvsRAS, quantifying concordance of variation signs across the 10 pairwise comparisons.: "For each reaction, calculate two Cohen's kappa coefficients: RASvsFFD and RPSvsRAS, quantifying concordance of variation signs across the 10 pairwise comparisons."
- [other] Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR<5%.: "Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR<5%."
- [intro] The intersection of the two output datasets discriminates fluxes regulated at the metabolic and/or gene expression level: "The intersection of the two output datasets discriminates fluxes regulated at the metabolic and/or gene expression level"
- [abstract] We discriminate fluxes regulated at the metabolic and/or transcriptional level. This information is valuable to better inform targeted action planning in different fields, including personalized prescriptions in multifactorial diseases, such as cancer: "knowing the regulatory level at which a given metabolic reaction is controlled will be valuable to inform targeted, truly personalized therapies in cancer"
- [results] Missing RPSvsRAS values occur when a reaction is not associated with a GPR: "Missing RPSvsRAS values occur when a reaction is not associated with a GPR"
- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [readme] Aim: create the results (dataset and figures) for concordance analysis. A dataset of concordance analysis (Cohen coefficient and pearson correlation) of RPS vs RAS, RPS vs FFD, RPS vs FFD, the pvalues and the adjusted pvalues: "A dataset of concordance analysis (Cohen coefficient and pearson correlation) of RPS vs RAS, RPS vs FFD, the pvalues and the adjusted pvalues"
