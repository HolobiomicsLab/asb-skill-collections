---
name: metabolic-reaction-classification-by-regulatory-layer
description: Use when you have integrated transcriptomics, intracellular metabolomics, and extracellular flux ratio data from multiple cell lines or conditions, and need to determine whether observed differences in metabolic fluxes originate from gene expression changes, substrate availability changes, or both.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  tools:
  - constraint-based stoichiometric metabolic models
  - COBRApy or similar constraint-based modeling library
  - INTEGRATE pipeline (Steps 1–10)
  - getRASscore.py
  - createMetabolicDataset.py
  - concordanceAnalysis.py
  - randomSampling.py
  - YSI2950 bioanalyzer
  - Agilent 6550 iFunnel Q-TOF mass spectrometer with MassHunter ProFinder
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

# Metabolic Reaction Classification by Regulatory Layer

## Summary

Distinguish between transcriptionally and metabolically controlled metabolic reactions by computing concordance between reaction propensity scores (RPS, derived from gene expression) and feasible flux distributions (FFD, derived from constraint-based modeling), then comparing against reaction activity scores (RAS). Reactions with high RPSvsFFD concordance but low RPSvsRAS concordance are classified as metabolically regulated (substrate availability–driven) rather than transcriptionally regulated.

## When to use

You have integrated transcriptomics, intracellular metabolomics, and extracellular flux ratio data from multiple cell lines or conditions, and need to determine whether observed differences in metabolic fluxes originate from gene expression changes, substrate availability changes, or both. Use this skill when you want to identify which reactions in your metabolic model are controlled by metabolic factors (substrate availability via mass action kinetics) independently of transcriptional regulation.

## When NOT to use

- Metabolomics dataset has <50% substrate coverage for the metabolic reactions of interest; the filter step requires 'complete substrate quantification,' and incomplete data will cause reactions to be excluded from analysis.
- Only transcriptomics data is available without metabolomics measurements; the skill requires intracellular metabolite abundances to compute RPS and thus cannot distinguish metabolic from transcriptional control.
- The input metabolic model lacks GPR rules or has poor gene-annotation coverage; RAS computation depends on GPR rules, and sparse annotations will result in incomplete reaction scoring.

## Inputs

- Transcriptomics dataset (FPKM or equivalent gene expression values across cell lines)
- Constraint-based metabolic model in SBML format (e.g., ENGRO2)
- GPR (gene-protein-reaction) rules extracted from the model
- Intracellular metabolomics dataset (absolute or relative metabolite abundances with complete substrate quantification for target reactions)
- Extracellular flux measurements (YSI bioanalyzer or equivalent: glucose, lactate, glutamine, glutamate uptake/secretion rates across cell lines and replicates)
- Medium composition file (nutrient availability constraints per cell line)
- Metabolite ID mapping file (conversion between metabolomics dataset IDs and model metabolite IDs)

## Outputs

- Classified reaction set: list of metabolically controlled reactions with reaction IDs, RPSvsFFD and RPSvsRAS concordance scores, and Cohen's kappa values
- Cell-line-specific RPS distributions (per-reaction substrate availability propensity scores for each cell line)
- Cell-line-specific FFD distributions (sampled feasible flux ranges for each reaction in each cell-line model)
- Concordance analysis table (Cohen's kappa, Pearson correlation, p-values, and adjusted p-values for all reaction pairs)
- Heatmap visualization of RPSvsRAS and RPSvsFFD concordance scores for reactions meeting the concordance threshold

## How to apply

First, compute RAS (Reaction Activity Score) from transcriptomics data and GPR rules for all reactions, then generate cell-line-specific metabolic models by integrating RAS constraints and extracellular flux measurements (YSI ratios, uptake/secretion rates). Next, sample the feasible flux region of each model using random sampling constrained by metabolomics-derived bounds on extracellular fluxes to generate FFD distributions. In parallel, compute RPS (Reaction Propensity Score) using intracellular metabolomics and mass action kinetics on reactions with complete substrate quantification. Then compute Cohen's kappa concordance coefficients for RPSvsFFD and RPSvsRAS pairs across all cell-line comparisons. Apply filtering: retain only reactions with RPSvsFFD Cohen's kappa ≥ 0.2 (indicating fair concordance between substrate-based and flux predictions) AND RPSvsRAS Cohen's kappa < 0.2 (indicating poor concordance with transcriptional activity), thereby isolating reactions whose flux variations are determined by substrate availability rather than gene expression differences.

## Related tools

- **COBRApy or similar constraint-based modeling library** (Constraint-based model integration, flux variability analysis, and random sampling of feasible flux regions)
- **INTEGRATE pipeline (Steps 1–10)** (Full implementation: GPR extraction, RAS computation, model integration, random sampling, concordance analysis) — https://github.com/qLSLab/integrate
- **getRASscore.py** (Generate RAS (Reaction Activity Score) from GPR rules and transcriptomics data) — https://github.com/qLSLab/integrate
- **createMetabolicDataset.py** (Prepare metabolomics data for RPS calculation and concordance analysis; perform substrate-level statistical filtering) — https://github.com/qLSLab/integrate
- **concordanceAnalysis.py** (Compute Cohen's kappa concordance coefficients between RPS–FFD and RPS–RAS pairs; generate heatmaps and concordance tables) — https://github.com/qLSLab/integrate
- **randomSampling.py** (Sample feasible flux distributions (FFD) from each cell-line–constrained metabolic model) — https://github.com/qLSLab/integrate
- **YSI2950 bioanalyzer** (Enzymatic quantification of glucose, lactate, glutamine, and glutamate in spent media for extracellular flux constraint derivation)
- **Agilent 6550 iFunnel Q-TOF mass spectrometer with MassHunter ProFinder** (Untargeted LC-MS/MS analysis and isotopic abundance correction for intracellular metabolomics quantification)

## Examples

```
python pipeline/concordanceAnalysis.py --valLog 1.2 --weight linear --resultsMetabolomicFile resultsMetabolomic --metabolic_model ENGRO2_irrev.xml --lcellLines MCF102A MDAMB231 SKBR3 MCF7 MDAMB361 --meansFile medie_Met.csv
```

## Evaluation signals

- Verify that the 81 reactions with complete substrate quantification form the analysis set and that reactions with any missing substrate measurements are excluded (filter enforcement).
- Check that RPSvsFFD concordance scores range from 0 to 1 (Cohen's kappa bounds) and that the threshold cutoff (≥0.2) partitions the reaction set into two interpretable groups: metabolically vs. non-metabolically controlled.
- Confirm that metabolically controlled reactions (RPSvsFFD ≥ 0.2 AND RPSvsRAS < 0.2) have monotonic agreement between RPS and FFD variation directions across cell-line pairs, whereas non-metabolically controlled reactions show non-monotonic or absent relationships.
- Cross-validate that reactions meeting the metabolic control criteria show strong correlation between substrate abundance changes (from metabolomics) and flux changes (from FFD sampling) across cell lines, with R² or Spearman correlation consistent with the Cohen's kappa ≥ 0.2 threshold.
- Assess that the classified reaction set is biologically coherent (e.g., reactions involving highly abundant substrates like glucose, lactate, and glutamine metabolism are enriched in the metabolically controlled set, reflecting known cancer cell metabolic dependencies).

## Limitations

- Limited metabolite coverage in metabolomics datasets constrains the number of reactions that can be analyzed; only reactions with all substrates quantified are included, potentially excluding important peripheral or cofactor-dependent reactions.
- Enzymatic activity, allosteric regulation, product inhibition, and cofactor/prosthetic group availability are not modeled; the method infers metabolic control only from substrate availability via mass action kinetics and thus cannot discriminate these regulatory mechanisms without additional data.
- The method assumes that the mass action kinetics approximation (RPS based on product of substrate concentrations) is valid; violations (e.g., strongly allosteric reactions, complex multi-substrate kinetics) will confound RPS and bias concordance scores.
- Model inaccuracy, constraint redundancy, or poor integration of extracellular flux measurements can cause reactions to show poor concordance with both RPS and RAS; such reactions cannot be reliably classified.
- The analysis is limited to the cell lines and conditions represented in the study; results may not generalize to other biological contexts, cancer subtypes, or growth media compositions.
- Computational cost of random sampling limits the number of steady-state solutions sampled (typically 10,000 per model); large feasible flux regions may be undersampled, leading to incomplete FFD distributions.

## Evidence

- [other] 13 reactions in ENGRO2 were identified as metabolically regulated, characterized by RPSvsFFD concordance scores above 0.2 paired with RPSvsRAS scores below this threshold or missing: "13 reactions in ENGRO2 were identified as metabolically regulated, characterized by RPSvsFFD concordance scores above 0.2 paired with RPSvsRAS scores below this threshold or missing, indicating their"
- [other] Filter to reactions with complete substrate quantification (81 reactions with all substrates measured in metabolomics): "Filter to reactions with complete substrate quantification (81 reactions with all substrates measured in metabolomics)."
- [other] Apply concordance threshold: retain reactions with RPSvsFFD Cohen's kappa ≥ 0.2 (fair concordance) and RPSvsRAS Cohen's kappa < 0.2 (poor concordance): "Apply concordance threshold: retain reactions with RPSvsFFD Cohen's kappa ≥ 0.2 (fair concordance) and RPSvsRAS Cohen's kappa < 0.2 (poor concordance), indicating metabolic control independent of"
- [intro] INTEGRATE first computes differential expression of reactions from transcriptomics data (transcriptional regulation only). Then, INTEGRATE exploits constraint-based modeling to predict how the global relative differences in expression are expected to translate into consistent differences in metabolic fluxes: "INTEGRATE first computes differential expression of reactions from transcriptomics data (transcriptional regulation only). Then, INTEGRATE exploits constraint-based modeling to predict how the global"
- [intro] INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes (metabolic"
- [results] Fig 4A reports the concordance level variations for the 81 metabolic reactions of ENGRO2 for which quantification of all substrate abundances was available: "Fig 4A reports the concordance level variations for the 81 metabolic reactions of ENGRO2 for which quantification of all substrate abundances was available"
- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [results] The heatmap in Fig 4B reports the RPSvsRAS and the RPSvsFFD concordance scores for reactions having a level of concordance between RPS and FFD greater than 0.2: "The heatmap in Fig 4B reports the RPSvsRAS and the RPSvsFFD concordance scores for reactions having a level of concordance between RPS and FFD greater than 0.2"
- [intro] Monotonic relationship between flux variation and substrate abundance variation indicates metabolic control of a reaction: "Our novel hypothesis is that evidence for a monotonic relationship between variations in fluxes and variations in substrate abundances, and for a concurrent non-monotonic relationship between flux"
- [readme] python pipeline/concordanceAnalysis.py: "**Step 10: Concordance data analysis**
* Aim: create the results (dataset and figures) for concordance analysis
* Usage: `python pipeline/concordanceAnalysis.py`"
