---
name: multi-cell-line-rps-calculation
description: Use when when you have LC-MS normalized intracellular metabolite abundance
  measurements for multiple cell lines and need to estimate reaction activity driven
  by substrate availability rather than enzyme expression alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - MassHunter ProFinder
  - constraint-based stoichiometric metabolic models
  - concordanceAnalysis.py
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- Data analysis and isotopic natural abundance correction were performed with MassHunter
  ProFinder (Agilent)
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

# multi-cell-line-rps-calculation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute Reaction Propensity Scores (RPS) across multiple cell lines by applying the mass action law to LC-MS intracellular metabolomics data, yielding substrate-availability-based reaction activity estimates for downstream concordance analysis with transcriptomics and flux predictions.

## When to use

When you have LC-MS normalized intracellular metabolite abundance measurements for multiple cell lines and need to estimate reaction activity driven by substrate availability rather than enzyme expression alone. Use this skill when preparing inputs for concordance analysis to distinguish metabolically controlled reactions (monotonic RPS–flux relationship) from transcriptionally controlled ones.

## When NOT to use

- If intracellular metabolite measurements are missing for one or more substrates of a reaction—that reaction must be excluded from RPS calculation.
- If the metabolic model lacks stoichiometric coefficients or precise substrate definitions, making mass action law formulation impossible.
- If only extracellular (exo-metabolomics) flux data is available; RPS requires intracellular substrate abundances.

## Inputs

- constraint-based stoichiometric metabolic model with reaction stoichiometry (SBML or equivalent)
- LC-MS normalized intracellular metabolite abundances (multiple cell lines)
- reaction-to-metabolite stoichiometric mapping

## Outputs

- RPS dataset: structured table indexed by reaction ID and cell line
- CSV file with columns for reaction ID, stoichiometry details, and RPS values per cell line

## How to apply

Load the constraint-based metabolic model (e.g. ENGRO2) and identify all reactions with complete stoichiometric coefficients and quantified substrate measurements across all cell lines; exclude any reaction with a missing substrate. For each eligible reaction r in each cell line c, compute RPS as the product of substrate concentrations raised to their stoichiometric coefficients: RPS_r^c = ∏(q=1 to N) [X_q]^s_{r,q}, where [X_q] is the substrate concentration (from LC-MS data) and s_{r,q} is the stoichiometric coefficient from the model. Organize the resulting RPS matrix by reaction ID and cell line to match the structure of parallel Feasible Flux Distribution (FFD) and Reaction Activity Score (RAS) datasets, ensuring dimensional alignment for subsequent Kappa Cohen and Pearson correlation concordance tests.

## Related tools

- **MassHunter ProFinder** (LC-MS data processing and natural abundance correction to generate normalized intracellular metabolite abundances)
- **constraint-based stoichiometric metabolic models** (Provide reaction stoichiometry and substrate definitions for RPS computation)
- **concordanceAnalysis.py** (Compute Cohen's Kappa and Pearson correlation between RPS, RAS, and FFD datasets) — https://github.com/qLSLab/integrate

## Examples

```
for rxn in reactions_with_all_substrates: rps_value = prod([metabolite_conc[s] ** stoich_coeff[rxn][s] for s in substrates[rxn]]); rps_dataset[rxn][cellline] = rps_value
```

## Evaluation signals

- Reaction count matches expected eligible set (e.g. 81 out of full model) after filtering for missing substrates.
- RPS values are positive and non-zero for all reactions; any zero or negative values indicate formula or data error.
- RPS matrix has no missing cells; all cell lines × reactions grid is complete.
- RPS values scale monotonically with metabolite concentration increases; doubling all substrate concentrations should raise RPS predictably.
- Concordance scores (Cohen's Kappa, Pearson r) between RPS and FFD/RAS are interpretable (−1 to 1 range); monotonic relationships expected for metabolically controlled reactions.

## Limitations

- Enzymatic activity is completely neglected; RPS predicts only substrate-availability-driven reaction rates, ignoring allosteric regulation, product inhibition, and cofactor effects.
- Limited metabolite coverage in LC-MS data constrains the number of analyzable reactions; if a substrate is absent from measurements, the entire reaction is omitted.
- Mass action law assumes no enzyme saturation kinetics or cooperative binding; validity depends on substrate concentrations remaining far from enzyme K_m values.
- RPS cannot discriminate between product inhibition and other non-enzymatic regulatory mechanisms; additional experimental data (e.g. labeled flux, protein abundance) is required.

## Evidence

- [other] The RPS for a reaction r in cell line c is computed as the product of substrate concentrations each raised to their stoichiometric coefficient (RPSc_r = ∏[X_q]^s_r,q), implementing the mass action law assumption: "The RPS for a reaction r in cell line c is computed as the product of substrate concentrations each raised to their stoichiometric coefficient (RPSc_r = ∏[X_q]^s_r,q), implementing the mass action"
- [other] Load intracellular metabolite abundance data (LC-MS normalized values) for the five cell lines from MetaboLights MTBLS3597. Load the ENGRO2 metabolic network model with reaction stoichiometry and identify 81 reactions with quantified substrate abundances in all five cell lines: "Load intracellular metabolite abundance data (LC-MS normalized values) for the five cell lines from MetaboLights MTBLS3597. Load the ENGRO2 metabolic network model with reaction stoichiometry and"
- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [other] Organize RPS values into a dataset indexed by reaction and cell line, matching the structure of the parallel Feasible Flux Distribution (FFD) and Reaction Activity Score (RAS) datasets for downstream concordance analysis.: "Organize RPS values into a dataset indexed by reaction and cell line, matching the structure of the parallel Feasible Flux Distribution (FFD) and Reaction Activity Score (RAS) datasets for downstream"
- [intro] Evidence for a monotonic relationship between variations in fluxes and variations in substrate abundances indicates metabolic control of a reaction: "evidence for a monotonic relationship between variations in fluxes and variations in substrate abundances, and for a concurrent non-monotonic relationship between flux"
- [results] Data analysis and isotopic natural abundance correction were performed with MassHunter ProFinder: "Data analysis and isotopic natural abundance correction were performed with MassHunter ProFinder"
