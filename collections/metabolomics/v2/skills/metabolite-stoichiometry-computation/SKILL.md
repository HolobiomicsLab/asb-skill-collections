---
name: metabolite-stoichiometry-computation
description: Use when when you have quantified intracellular metabolite abundances (LC-MS normalized values) for multiple cell lines or samples, a metabolic network model with reaction stoichiometry, and you need to predict how substrate availability translates into metabolic flux differences.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_2259
  tools:
  - MassHunter ProFinder
  - constraint-based stoichiometric metabolic models
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- Data analysis and isotopic natural abundance correction were performed with MassHunter ProFinder (Agilent)
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

# Reaction Propensity Score (RPS) computation from intracellular metabolomics via mass action law

## Summary

Computes a Reaction Propensity Score (RPS) for each metabolic reaction in a cell line by applying the mass action law to measured intracellular metabolite abundances, multiplying substrate concentrations each raised to their stoichiometric coefficients. This score estimates reaction rate potential based purely on substrate availability, excluding enzymatic activity.

## When to use

When you have quantified intracellular metabolite abundances (LC-MS normalized values) for multiple cell lines or samples, a metabolic network model with reaction stoichiometry, and you need to predict how substrate availability translates into metabolic flux differences. RPS is particularly useful when substrate concentration variations are the primary regulatory layer of interest and you want to assess metabolic control independent of transcriptional regulation.

## When NOT to use

- Enzymatic activity, allosteric regulation, product inhibition, or cofactor/prosthetic group effects are known to dominate the regulation of target reactions — RPS neglects all of these layers.
- Metabolomics dataset has poor coverage of substrates; if >20% of reaction substrates are unmeasured, the eligible reaction pool becomes too sparse for meaningful concordance analysis.
- Input concentrations are relative abundance values (e.g., peak intensity ratios) rather than absolute quantified concentrations — mass action law derivation assumes true molar concentrations.

## Inputs

- Intracellular metabolite abundance data (LC-MS normalized values) indexed by metabolite ID and cell line
- Stoichiometric metabolic network model (SBML or equivalent format) with reaction-substrate mappings and stoichiometric coefficients
- List of reactions with complete substrate quantification across all samples

## Outputs

- Reaction Propensity Score (RPS) table: rows=reaction IDs, columns=RPS values per cell line
- Metadata table linking each RPS computation to substrate concentrations and stoichiometric coefficients used

## How to apply

First, load the intracellular metabolite abundance data (LC-MS normalized concentrations) and the stoichiometric metabolic model; identify all reactions with quantified substrate abundances present in all samples, excluding any reaction with a missing substrate measurement. For each eligible reaction and each cell line, compute RPS as the product formula: RPS_r^c = ∏(q=1 to N) [X_q]^s_{r,q}, where [X_q] is the measured concentration of substrate q and s_{r,q} is the stoichiometric coefficient of that substrate in reaction r. Organize the resulting RPS values into a structured table indexed by reaction ID and cell line, matching the structure of parallel datasets (Feasible Flux Distribution, Reaction Activity Score) to enable downstream concordance analysis. Export as a CSV with columns for reaction ID, stoichiometry details, and RPS values for each sample.

## Related tools

- **MassHunter ProFinder** (Data analysis and isotopic natural abundance correction for LC-MS metabolomics to generate normalized intracellular metabolite abundance values input to RPS computation)
- **constraint-based stoichiometric metabolic models** (Source of reaction stoichiometry and substrate-product relationships required to retrieve stoichiometric coefficients (s_{r,q}) for RPS formula)

## Evaluation signals

- All eligible reactions (those with complete substrate quantification) have RPS values computed; reactions with any missing substrate are absent from output, confirming filter was applied.
- RPS values are positive and scale monotonically with substrate concentration changes (higher substrate abundance → higher RPS) within each reaction, validating the product formula.
- RPS dataset dimensions match expected structure: number of rows = number of eligible reactions (typically 81 in ENGRO2 model with full substrate coverage), number of columns = number of cell lines plus metadata columns.
- RPS values can be successfully merged with Feasible Flux Distribution (FFD) and Reaction Activity Score (RAS) tables by reaction ID, enabling downstream concordance analysis (e.g., correlation coefficient computation).
- Spot-check RPS computation for 2–3 reactions: manually verify product calculation matches reported value (e.g., for a reaction with 2 substrates at concentrations 5 mM and 2 mM with stoichiometric coefficients 1 and 2, RPS should equal 5^1 × 2^2 = 20).

## Limitations

- Enzymatic activity is completely neglected; RPS reflects substrate availability only and cannot capture allosteric activation/inhibition or product feedback inhibition without additional experimental data.
- Limited metabolite coverage in metabolomics dataset constrains the number of analyzable reactions; reactions with even a single unmeasured substrate are excluded, reducing statistical power.
- Mass action law assumes dilute, well-mixed solution and elementary reaction kinetics, which may not hold in crowded cellular environments or for multi-step enzymatic reactions.
- Absolute concentration determination by LC-MS is technically challenging; if reported values are relative abundances or log-fold changes rather than true molar concentrations, the RPS formula becomes invalid.
- Assumes stoichiometric coefficients are accurately defined in the input metabolic model; errors in the model's reaction definitions will propagate to RPS calculations.

## Evidence

- [other] The RPS for a reaction r in cell line c is computed as the product of substrate concentrations each raised to their stoichiometric coefficient (RPSc_r = ∏[X_q]^s_r,q), implementing the mass action law assumption that reaction rate is proportional to this product: "The RPS for a reaction r in cell line c is computed as the product of substrate concentrations each raised to their stoichiometric coefficient (RPSc_r = ∏[X_q]^s_r,q), implementing the mass action"
- [other] Load intracellular metabolite abundance data (LC-MS normalized values) for the five cell lines from MetaboLights MTBLS3597. Load the ENGRO2 metabolic network model with reaction stoichiometry and identify 81 reactions with quantified substrate abundances in all five cell lines; exclude any reaction with a missing substrate measurement.: "Load intracellular metabolite abundance data (LC-MS normalized values) for the five cell lines from MetaboLights MTBLS3597. Load the ENGRO2 metabolic network model with reaction stoichiometry and"
- [other] For each of the 81 eligible reactions and each cell line, compute the Reaction Propensity Score (RPS) as the product of substrate concentrations raised to their stoichiometric coefficients: RPS_r^c = ∏(q=1 to N) [X_q]^s_{r,q}, where [X_q] is substrate concentration and s_{r,q} is stoichiometric coefficient.: "For each of the 81 eligible reactions and each cell line, compute the Reaction Propensity Score (RPS) as the product of substrate concentrations raised to their stoichiometric coefficients: RPS_r^c ="
- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [intro] INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes"
- [intro] Enzymatic activity is neglected in metabolic regulation prediction; only substrate availability is considered: "Enzymatic activity is neglected in metabolic regulation prediction; only substrate availability is considered"
