---
name: mass-action-law-flux-prediction
description: Use when when you have quantified intracellular metabolite abundances (LC-MS normalized values) from multiple samples and need to predict how differences in substrate availability translate into differences in metabolic flux for specific reactions in a constraint-based metabolic model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3929
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_2650
  - http://edamontology.org/topic_3407
  tools:
  - MassHunter ProFinder
  - constraint-based stoichiometric metabolic models
  - COBRApy (implied by workflow)
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
---

# Reconstruct the RPS computation from intracellular metabolomics via the mass action law

## Summary

Compute Reaction Propensity Scores (RPS) from intracellular metabolite abundances by applying the mass action law principle—where reaction rate is proportional to the product of substrate concentrations each raised to their stoichiometric coefficient. This provides a metabolomics-based prediction of metabolic flux differences driven by substrate availability alone, independent of enzymatic activity or transcriptional regulation.

## When to use

When you have quantified intracellular metabolite abundances (LC-MS normalized values) from multiple samples and need to predict how differences in substrate availability translate into differences in metabolic flux for specific reactions in a constraint-based metabolic model. Use this skill to decompose metabolic regulation into transcriptional vs. metabolic (substrate-driven) control layers by comparing RPS predictions against transcriptomics-derived (RAS) and flux-sampling (FFD) estimates.

## When NOT to use

- Reactions with missing substrate measurements in the metabolomics dataset—exclude these reactions from RPS calculation rather than imputing or using proxy substrates.
- When enzymatic activity, allosteric regulation, product inhibition, or cofactor/prosthetic group availability are known to drive flux changes; mass action law alone cannot discriminate these mechanisms.
- When metabolomics coverage is too sparse (e.g., <50% of reaction substrates quantified), rendering concordance analysis with flux predictions unreliable.

## Inputs

- Intracellular metabolite abundance data (LC-MS normalized concentration values, e.g., from MetaboLights MTBLS3597 format)
- Constraint-based stoichiometric metabolic model (SBML or COBRApy format, e.g., ENGRO2) with reaction definitions and stoichiometry
- Reaction-metabolite stoichiometric matrix (mapping reactions to their substrates and stoichiometric coefficients)
- Sample/cell line identifiers for organization

## Outputs

- RPS dataset: structured table with columns for reaction ID, stoichiometry details, and RPS values for each sample/cell line
- Filtered reaction list: 81 reactions (or equivalent) with complete substrate quantification across all samples
- RPS-indexed matrix compatible with downstream concordance analysis (rows=reactions, columns=samples)

## How to apply

For each reaction in the metabolic network with all substrates quantified in the metabolomics dataset, compute RPS as the product of substrate concentrations raised to their stoichiometric coefficients: RPS_r^c = ∏(q=1 to N) [X_q]^s_{r,q}, where [X_q] is the intracellular concentration of substrate q and s_{r,q} is its stoichiometric coefficient. Exclude any reaction with missing substrate measurements. Organize RPS values by reaction ID and sample/cell line, maintaining the same dimensionality as the parallel Feasible Flux Distribution (FFD) and Reaction Activity Score (RAS) datasets. This assumes that metabolic flux depends only on substrate mass action (neglecting enzymatic activity, allosteric regulation, and cofactor effects), allowing concordance analysis against transcriptomics and constraint-based flux predictions to identify which reactions are controlled primarily by substrate availability vs. gene expression.

## Related tools

- **constraint-based stoichiometric metabolic models** (Provides reaction definitions, stoichiometry, and metabolite-reaction mappings required to identify substrates and coefficients for each reaction in RPS calculation)
- **MassHunter ProFinder** (Performs LC-MS data analysis and isotopic natural abundance correction to generate normalized intracellular metabolite abundance values used as inputs to RPS computation)
- **COBRApy (implied by workflow)** (Loads and manipulates SBML metabolic models to extract reaction-metabolite associations and stoichiometric coefficients for RPS formula application) — https://github.com/opencobra/cobrapy

## Examples

```
# Step 10 in the README orchestrates concordance analysis including RPS computation:
# python pipeline/concordanceAnalysis.py
# with inputs: metabolomics_LM.csv, ENGRO2_irrev.xml, metsEngroVsMetabolomics.csv conversion file
# Internally computes RPS as product([X_q]^s_r,q) for all eligible reactions
```

## Evaluation signals

- All 81 eligible reactions in the model have complete substrate quantification; no NaN or missing values in the RPS dataset for reactions included in concordance analysis.
- RPS values are positive and finite for all reactions and samples; stoichiometric coefficients are correctly applied (e.g., A + 2B → C produces RPS = [A]^1 × [B]^2, not [A]×[B]).
- RPS dataset dimensionality matches FFD and RAS datasets (same reaction set, same sample/cell line set) enabling direct pairwise concordance comparison.
- RPS vs. FFD concordance scores and RPS vs. RAS concordance scores can be computed and ranked; reactions with concordance > 0.2 are plotted in downstream heatmaps as expected.
- Exclusion filters applied correctly: reactions with any missing substrate are not present in the final RPS table; only cell lines with complete metabolomics coverage are included.

## Limitations

- Enzymatic activity is entirely neglected; reactions cannot be distinguished by enzyme abundance, Vmax, or Km differences—only by substrate availability. This leads to underprediction of flux when enzyme abundance is rate-limiting.
- Allosteric regulation, product inhibition, and cofactor/prosthetic group availability cannot be discriminated from this analysis without additional experimental data (e.g., enzyme kinetics, redox measurements).
- Limited metabolite coverage in metabolomics datasets constrains the number of reactions that can be analyzed; reactions whose substrates are not quantified must be excluded, reducing statistical power and leaving gaps in pathway coverage.
- The mass action law formulation assumes linear kinetics and does not account for substrate saturation (Michaelis-Menten kinetics) or cooperative binding, which may mispredict flux when substrates are near saturation or when allosteric cooperativity is present.
- Compartmentalization and metabolite pool heterogeneity are not explicitly modeled; the analysis assumes a single uniform concentration per metabolite across the cell.

## Evidence

- [other] The RPS for a reaction r in cell line c is computed as the product of substrate concentrations each raised to their stoichiometric coefficient (RPSc_r = ∏[X_q]^s_r,q), implementing the mass action law assumption that reaction rate is proportional to this product: "The RPS for a reaction r in cell line c is computed as the product of substrate concentrations each raised to their stoichiometric coefficient (RPSc_r = ∏[X_q]^s_r,q), implementing the mass action"
- [other] For each of the 81 eligible reactions and each cell line, compute the Reaction Propensity Score (RPS) as the product of substrate concentrations raised to their stoichiometric coefficients: RPS_r^c = ∏(q=1 to N) [X_q]^s_{r,q}, where [X_q] is substrate concentration and s_{r,q} is stoichiometric coefficient.: "For each of the 81 eligible reactions and each cell line, compute the Reaction Propensity Score (RPS) as the product of substrate concentrations raised to their stoichiometric coefficients: RPS_r^c ="
- [other] Load intracellular metabolite abundance data (LC-MS normalized values) for the five cell lines from MetaboLights MTBLS3597.: "Load intracellular metabolite abundance data (LC-MS normalized values) for the five cell lines from MetaboLights MTBLS3597"
- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset.: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [intro] INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes"
- [intro] Enzymatic activity is neglected in metabolic regulation prediction; only substrate availability is considered.: "Enzymatic activity is neglected in metabolic regulation prediction; only substrate availability is considered"
- [results] The phenomenon according to which gene expression and substrate availability agree with one another, but the flux does not agree with any of the two, might be imputed to model inaccuracy, as well as allosteric regulation, product inhibition, and cofactor/prosthetic group effects: "allosteric regulation, product inhibition, and cofactor/prosthetic group effects cannot be discriminated from the current analysis without additional data"
- [results] Fig 4A reports the concordance level variations for the 81 metabolic reactions of ENGRO2 for which quantification of all substrate abundances was available: "Fig 4A reports the concordance level variations for the 81 metabolic reactions of ENGRO2 for which quantification of all substrate abundances was available"
- [other] Organize RPS values into a dataset indexed by reaction and cell line, matching the structure of the parallel Feasible Flux Distribution (FFD) and Reaction Activity Score (RAS) datasets for downstream concordance analysis.: "Organize RPS values into a dataset indexed by reaction and cell line, matching the structure of the parallel Feasible Flux Distribution (FFD) and Reaction Activity Score (RAS) datasets for downstream"
