---
name: flux-distribution-interpretation-across-cell-lines
description: Use when you have sampled 10,000+ steady-state flux solutions for each of multiple cell lines from a constraint-based model; computed Reaction Propensity Scores (RPS) from substrate abundance (metabolomics) and Reaction Activity Scores (RAS) from gene expression (transcriptomics);
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3678
  tools:
  - Flux Variability Analysis
  - constraint-based stoichiometric metabolic models
  - Flux Variability Analysis (FVA)
  - randomSampling (INTEGRATE pipeline Step 6)
  - getRASscore (INTEGRATE pipeline Step 2)
  - concordanceAnalysis (INTEGRATE pipeline Step 10)
  - createMetabolicDataset (INTEGRATE pipeline Step 9)
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA
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
---

# Flux-distribution interpretation across cell lines

## Summary

Interpret feasible flux distributions (FFD) sampled from constraint-based metabolic models across multiple cell lines to distinguish metabolically controlled reactions (high RPSvsFFD concordance) from transcriptionally controlled ones (high RASvsFFD concordance). This skill enables classification of metabolic reactions by their regulatory mode using Cohen's kappa concordance coefficients.

## When to use

You have sampled 10,000+ steady-state flux solutions for each of multiple cell lines from a constraint-based model; computed Reaction Propensity Scores (RPS) from substrate abundance (metabolomics) and Reaction Activity Scores (RAS) from gene expression (transcriptomics); and need to determine which reactions are controlled by substrate availability versus transcriptional regulation. Apply this skill when substrate quantification is complete for reaction inputs and you wish to segregate metabolic reactions into regulatory classes.

## When NOT to use

- Substrate quantification is incomplete for reaction inputs — filtering will exclude reactions with missing metabolomics data, reducing analytical power below utility
- FFD samples are not generated from the same constraint-based model parametrization used to compute RPS and RAS scores — inconsistent model versions will invalidate concordance assumptions
- Only transcriptomics data is available without corresponding metabolomics measurements — RPS cannot be computed, defeating the dual-threshold regulatory discrimination

## Inputs

- Feasible Flux Distribution (FFD) samples (10,000 steady-state solutions per cell line from constraint-based model sampling)
- Reaction Propensity Score (RPS) matrix (reactions × cell lines, computed from intracellular metabolomics substrate abundances)
- Reaction Activity Score (RAS) matrix (reactions × cell lines, computed from transcriptomics gene expression via GPR rules)
- Metabolomics dataset with quantified substrate abundances (required for reactions included in analysis)
- Constraint-based metabolic model (SBML format, e.g., ENGRO2) with GPR associations

## Outputs

- Table of metabolically controlled reactions (13 in original ENGRO2 analysis) with RPSvsFFD and RPSvsRAS Cohen's kappa scores
- Filtered reaction set (RPSvsFFD kappa ≥ 0.2 AND RPSvsRAS kappa < 0.2)
- Cell-line-specific RPS and FFD distributions for retained reactions
- Heatmap or tabular representation of concordance scores across reactions and cell-line pairs

## How to apply

Load precomputed RPS, FFD distributions, and RAS scores for all reactions. Restrict analysis to reactions where all substrates have been quantified in metabolomics (filter: 81 reactions in ENGRO2 with complete substrate coverage). Compute Cohen's kappa concordance coefficient between RPS and FFD variation signs across cell line pairs; separately compute Cohen's kappa between RAS and RPS variation signs. Apply dual thresholds: retain reactions with RPSvsFFD Cohen's kappa ≥ 0.2 (indicating substrate-driven flux variation) AND RPSvsRAS Cohen's kappa < 0.2 (indicating weak transcriptional coupling). Tabulate final metabolically controlled reaction set with their concordance scores and cell-line-specific RPS and FFD distributions. This dual-threshold filtering distinguishes metabolic control independent of transcriptional regulation.

## Related tools

- **constraint-based stoichiometric metabolic models** (Scaffold for Flux Variability Analysis; provides reaction stoichiometry and GPR rules for concordance analysis)
- **Flux Variability Analysis (FVA)** (Computes flux boundaries for each reaction; enables sampling of feasible flux region and computation of FFD)
- **randomSampling (INTEGRATE pipeline Step 6)** (Samples 10,000+ steady-state flux solutions from the feasible region of each cell-line model to generate FFD distributions) — https://github.com/qLSLab/integrate
- **getRASscore (INTEGRATE pipeline Step 2)** (Computes RAS from GPR rules and transcriptomics (FPKM) data; generates reaction-level activity scores across cell lines) — https://github.com/qLSLab/integrate
- **concordanceAnalysis (INTEGRATE pipeline Step 10)** (Computes Cohen's kappa concordance coefficients between RPS vs FFD and RPS vs RAS; applies thresholds to identify metabolically controlled reactions) — https://github.com/qLSLab/integrate
- **createMetabolicDataset (INTEGRATE pipeline Step 9)** (Prepares metabolomic statistical test dataset with quality filtering and maps metabolite IDs to model metabolites) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/concordanceAnalysis.py --valLog 1.2 --weight linear --resultsMetabolomicFile resultsMetabolomic --metabolic_model ENGRO2_irrev.xml --lcellLines MCF102A SKBR3 MCF7 MDAMB231 MDAMB361 --meansFile medie_Met.csv
```

## Evaluation signals

- Cohen's kappa scores are computed for all reaction pairs (RPSvsFFD and RPSvsRAS) and fall in the range [-1, 1]; verify that mean values align with reported concordance levels in concordance analysis output
- Filtered set of reactions meets dual thresholds: all retained reactions have RPSvsFFD kappa ≥ 0.2; none have RPSvsRAS kappa ≥ 0.2; verify through threshold-violation audit before final reporting
- Only reactions with complete substrate quantification (no missing metabolomics values) are included in the final table; audit row count against filter criteria (original: 81/reactions passed substrate filter, 13 passed dual concordance thresholds)
- FFD and RPS distributions per cell line show interpretable variation (e.g., monotonic trends in log-ratio metabolite abundances correlate with flux variation direction); non-degenerate distributions (std > 0) indicate adequate sampling
- Heatmap or table of concordance scores is consistent with narrative: reactions with high RPSvsFFD kappa and low RPSvsRAS kappa appear in metabolic control category; reactions with high RASvsFFD kappa appear in transcriptional control category (if applicable)

## Limitations

- Analysis assumes mass-action kinetics for metabolic control prediction; enzymatic activity, allosteric regulation, product inhibition, and cofactor/prosthetic group effects cannot be discriminated without additional experimental data (enzyme activity assays, phosphoproteomics)
- Limited metabolite coverage in metabolomics dataset constrains the number of analyzable reactions: reactions with even one unmeasured substrate are excluded, reducing reaction coverage
- Concordance analysis depends on sufficient statistical power across cell-line pairs; small sample sizes (5 cell lines in ENGRO2 study) introduce uncertainty in kappa estimation and may inflate false negatives
- Model inaccuracy, substrate transport kinetics not captured by mass action law, and incomplete GPR coverage can produce reactions where gene expression and substrate availability agree but flux does not; these are difficult to disambiguate post-hoc
- FFD sampling computational cost is high (10,000 solutions per model); results may be limited to subsampled steady-state space for visualization, potentially underrepresenting rare flux states

## Evidence

- [other] 13 reactions in ENGRO2 were identified as metabolically regulated, characterized by RPSvsFFD concordance scores above 0.2 paired with RPSvsRAS scores below this threshold: "13 reactions in ENGRO2 were identified as metabolically regulated, characterized by RPSvsFFD concordance scores above 0.2 paired with RPSvsRAS scores below this threshold or missing, indicating their"
- [other] Fig 4A reports the concordance level variations for the 81 metabolic reactions of ENGRO2 for which quantification of all substrate abundances was available: "Fig 4A reports the concordance level variations for the 81 metabolic reactions of ENGRO2 for which quantification of all substrate abundances was available"
- [other] The heatmap in Fig 4B reports the RPSvsRAS and the RPSvsFFD concordance scores for reactions having a level of concordance between RPS and FFD greater than 0.2: "The heatmap in Fig 4B reports the RPSvsRAS and the RPSvsFFD concordance scores for reactions having a level of concordance between RPS and FFD greater than 0.2"
- [other] Compute Cohen's kappa concordance coefficient between RPS and FFD variations for each reaction pair across cell lines: "Compute Cohen's kappa concordance coefficient between RPS and FFD variations for each reaction pair across cell lines"
- [other] Apply concordance threshold: retain reactions with RPSvsFFD Cohen's kappa ≥ 0.2 (fair concordance) and RPSvsRAS Cohen's kappa < 0.2 (poor concordance): "Apply concordance threshold: retain reactions with RPSvsFFD Cohen's kappa ≥ 0.2 (fair concordance) and RPSvsRAS Cohen's kappa < 0.2 (poor concordance), indicating metabolic control independent of"
- [results] For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted: "For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted"
- [intro] INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes"
- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
