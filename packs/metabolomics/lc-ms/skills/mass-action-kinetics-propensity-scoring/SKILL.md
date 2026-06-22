---
name: mass-action-kinetics-propensity-scoring
description: Use when you have intracellular metabolomics measurements (absolute metabolite abundances) for multiple biological samples and want to identify which metabolic reactions are controlled by substrate availability rather than gene expression.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - constraint-based stoichiometric metabolic models
  - Flux Variability Analysis
  - Agilent 1290 Infinity UHPLC + 6550 iFunnel Q-TOF mass spectrometer
  - MassHunter ProFinder
  - createMetabolicDataset.py (INTEGRATE pipeline Step 9)
  - concordanceAnalysis.py (INTEGRATE pipeline Step 10)
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Mass-Action Kinetics Propensity Scoring

## Summary

Compute Reaction Propensity Scores (RPS) from intracellular metabolomics data using mass action law to quantify how substrate availability constrains metabolic flux, enabling discrimination of metabolically controlled reactions from transcriptionally regulated ones.

## When to use

Apply this skill when you have intracellular metabolomics measurements (absolute metabolite abundances) for multiple biological samples and want to identify which metabolic reactions are controlled by substrate availability rather than gene expression. Specifically, use it when you need to distinguish reactions with high concordance between substrate availability variations and flux variations (indicating metabolic control) from those where gene expression drives flux.

## When NOT to use

- Input metabolomics dataset has incomplete substrate coverage (missing measurements for >5–10% of substrates in reactions of interest); RPS cannot be reliably computed for reactions with unmeasured substrates.
- Metabolic model lacks accurate stoichiometry or cofactor/prosthetic group definitions; mass action law kinetics require correct stoichiometric coefficients and substrate multiplicativity assumptions.
- Allosteric regulation, product inhibition, or enzyme activity modulation are known to dominate control in the biological system; mass action kinetics with substrate abundances alone will not capture these regulatory layers.
- Biological samples have been perturbed in ways that violate the steady-state assumption (e.g., acute starvation, rapid perturbation without equilibration); FFD sampling assumes quasi-steady-state metabolism.

## Inputs

- Intracellular metabolomics abundance dataset (LC-MS/MS quantified metabolite concentrations, molar units, across multiple cell lines)
- Metabolic model in SBML or MAT format with complete reaction stoichiometry and substrate/product mappings
- Metabolite ID conversion file mapping metabolomics identifiers to model metabolite IDs
- Feasible Flux Distribution (FFD) samples from constraint-based model (sampled steady-state solutions from randomSampling step)
- Gene expression data (RAS scores or normalized transcript abundances) for computing concordance baselines

## Outputs

- RPS score table (reactions × cell lines) with computed propensity scores quantifying substrate-driven flux potential
- Normalized RPS values (mean and normalized RPS per reaction per cell line)
- RPSvsFFD concordance matrix (Cohen's kappa, Pearson correlation, p-values) indicating degree of metabolic control
- RPSvsRAS concordance matrix for comparison to transcriptional control
- Filtered set of metabolically controlled reactions (RPSvsFFD kappa ≥0.2 and RPSvsRAS kappa <0.2) with cell-line-specific RPS and FFD distributions

## How to apply

First, load intracellular metabolomics data and filter to reactions with complete substrate quantification—exclude any reaction if even one substrate is missing from the measurements. For each reaction in each cell line, apply the mass action law formulation to compute a Reaction Propensity Score (RPS) reflecting the multiplicative effect of substrate abundances on reaction flux potential. Normalize RPS values across cell lines to enable cross-sample comparison. Then compute Cohen's kappa concordance coefficient between RPS variation signs and Flux Feasibility Distribution (FFD) variation signs across cell line pairs. Reactions with RPSvsFFD Cohen's kappa ≥0.2 (fair concordance) indicate substrate availability drives flux changes; contrast these against RPSvsRAS concordance (< 0.2) to confirm metabolic rather than transcriptional control. The monotonic relationship between RPS and FFD variations, coupled with non-monotonic FFD-to-RAS relationship, signals metabolic regulation.

## Related tools

- **constraint-based stoichiometric metabolic models** (Provides reaction stoichiometry and substrate/product definitions needed to apply mass action law formulation; model is the scaffold upon which RPS is computed and concordance is assessed.) — https://github.com/qLSLab/integrate
- **Flux Variability Analysis** (Generates feasible flux distributions (FFD) by sampling the null space of the constraint-based model; FFD samples are used to compare against RPS variation patterns to assess metabolic control.) — https://github.com/qLSLab/integrate
- **Agilent 1290 Infinity UHPLC + 6550 iFunnel Q-TOF mass spectrometer** (Instrumentation for high-resolution LC-MS/MS quantification of intracellular metabolite abundances; provides absolute metabolite concentrations required for mass action law calculations.)
- **MassHunter ProFinder** (Post-acquisition data analysis software for metabolomics; performs isotopic natural abundance correction on LC-MS raw data before RPS input preparation.)
- **createMetabolicDataset.py (INTEGRATE pipeline Step 9)** (Prepares metabolomics data for concordance analysis; handles metabolite ID conversion, quality filtering, and statistical test dataset creation prior to RPS computation.) — https://github.com/qLSLab/integrate
- **concordanceAnalysis.py (INTEGRATE pipeline Step 10)** (Computes Cohen's kappa concordance coefficients between RPS and FFD, and between RPS and RAS; produces concordance matrices and visualizations for metabolic control classification.) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/concordanceAnalysis.py --valLog 1.2 --weight linear --resultsMetabolomicFile resultsMetabolomic --metabolic_model ENGRO2_irrev.xml --meansFile medie_Met.csv --lcellLines ['MCF102A','MDAMB231','SKBR3','MCF7','MDAMB361']
```

## Evaluation signals

- RPS values are computed for exactly the 81 reactions (or the subset) with complete substrate quantification; no reactions with missing substrate measurements appear in output RPS table.
- RPS variation signs (increase/decrease/no-change) across cell line pairs show monotonic concordance with FFD variation signs, reflected as Cohen's kappa ≥0.2 for metabolically controlled reactions.
- RPSvsRAS concordance is substantially lower (<0.2) than RPSvsFFD concordance for identified metabolically controlled reactions, confirming that substrate availability, not gene expression, drives flux.
- Cohen's kappa and Pearson correlation values are in expected ranges (−1 to +1 for kappa, −1 to +1 for Pearson); p-values and FDR-adjusted p-values are computed and reported for statistical significance.
- Tabulated metabolically controlled reactions display cell-line-specific RPS and FFD distributions with consistent directional agreement (e.g., high RPS in cell line A paired with high FFD in cell line A), indicating predictive validity of the propensity model.

## Limitations

- Enzymatic activity and allosteric regulation are neglected; only substrate availability is modeled via mass action law. Reactions controlled by product inhibition, cofactor depletion, or allosteric effectors will show poor concordance even if substrate-driven.
- Limited metabolite coverage in metabolomics constrains the number of reactions analyzable; reactions with unmeasured or rare substrates are excluded entirely from RPS calculation, biasing the analyzed reaction set toward central metabolism.
- Mass action law formulation assumes kinetic homogeneity (uniform enzyme kinetics, Michaelis constants, catalytic efficiencies) across cell lines; cell-line-specific differences in enzyme expression or post-translational modification can violate this assumption.
- Steady-state assumption may not hold during dynamic metabolic transitions or in cell lines with unstable growth; FFD sampling presumes quasi-equilibrium between substrate availability and flux.
- Cohen's kappa threshold (0.2) and dichotomy (metabolic vs. transcriptional control) are heuristic; reactions with moderate or mixed control will be misclassified at boundary thresholds.

## Evidence

- [intro] INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes (metabolic control): "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes"
- [other] Reactions with RPSvsFFD concordance ≥0.2 and RPSvsRAS concordance <0.2 indicate metabolic control: "13 reactions in ENGRO2 were identified as metabolically regulated, characterized by RPSvsFFD concordance scores above 0.2 paired with RPSvsRAS scores below this threshold or missing, indicating their"
- [results] Filter to reactions with complete substrate quantification before RPS computation: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [intro] Monotonic relationship between flux and substrate variations indicates metabolic control: "evidence for a monotonic relationship between variations in fluxes and variations in substrate abundances, and for a concurrent non-monotonic relationship between flux"
- [abstract] Differences in metabolic fluxes depend on substrate availability, not just gene expression: "use metabolomics to predict how differences in substrate availability translate into differences in metabolic fluxes"
- [readme] Concordance analysis workflow computes Cohen's kappa between RPS and FFD: "Compute Cohen's kappa concordance coefficient between RPS and FFD variations for each reaction pair across cell lines"
- [readme] Metabolomics data preparation filters by quality and requires metabolite ID conversion: "create the metabolomic dataset to perform concordance analysis... dict_to_convert_metnames: Conversion file between ID of metabolites in metabolomics dataset and ID of metabolites in the input model"
