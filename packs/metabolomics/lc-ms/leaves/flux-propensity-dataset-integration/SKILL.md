---
name: flux-propensity-dataset-integration
description: Use when when you have (1) LC-MS normalized intracellular metabolite
  abundance data across multiple cell lines or samples, (2) a constraint-based metabolic
  model with stoichiometric coefficients, and (3) a need to quantify metabolic control
  through substrate availability independently of enzymatic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0625
  tools:
  - MassHunter ProFinder
  - constraint-based stoichiometric metabolic models
  - 'INTEGRATE pipeline (Step 10: concordanceAnalysis.py)'
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# Reconstruct the RPS computation from intracellular metabolomics via the mass action law

## Summary

Computes Reaction Propensity Scores (RPS) from LC-MS intracellular metabolite abundances using the mass action law, expressing each reaction's propensity as the product of substrate concentrations raised to their stoichiometric coefficients. This dataset enables downstream concordance analysis between metabolomic regulation (RPS), transcriptomic regulation (RAS), and constraint-based flux predictions (FFD).

## When to use

When you have (1) LC-MS normalized intracellular metabolite abundance data across multiple cell lines or samples, (2) a constraint-based metabolic model with stoichiometric coefficients, and (3) a need to quantify metabolic control through substrate availability independently of enzymatic expression levels. Apply this skill to generate a metabolomics-derived flux proxy for comparison with transcriptomics-derived (RAS) and model-predicted (FFD) flux signals.

## When NOT to use

- When enzymatic activity or allosteric regulation is the dominant control mechanism; mass action law neglects enzyme kinetics and allosteric effects.
- When substrate metabolite coverage in the metabolomics dataset is too sparse (majority of reactions have missing substrates); data quality will be severely compromised.
- When the goal is to predict absolute metabolic flux; RPS is a propensity proxy under mass action assumption, not a direct flux estimate.

## Inputs

- LC-MS normalized intracellular metabolite abundance table (e.g., MetaboLights MTBLS3597 format)
- Constraint-based stoichiometric metabolic model (SBML or equivalent, e.g., ENGRO2)
- Mapping file linking metabolomics metabolite IDs to model metabolite IDs

## Outputs

- RPS dataset table with columns: reaction ID, stoichiometry details, RPS values indexed by sample/cell line
- Exclusion log listing reactions omitted due to missing substrate abundances

## How to apply

Load intracellular metabolite abundance data (LC-MS normalized values, e.g., from MetaboLights) and a stoichiometric metabolic model (e.g., ENGRO2). Identify reactions for which all substrate abundances are quantified in the metabolomics dataset; exclude any reaction with a missing substrate measurement. For each eligible reaction and each sample/cell line, compute RPS as the product ∏([X_q]^s_{r,q}), where [X_q] is substrate concentration and s_{r,q} is the stoichiometric coefficient from the model. Organize RPS values into a structured table (columns: reaction ID, stoichiometry details, RPS for each sample) matching the indices and dimensions of parallel FFD and RAS datasets. This ensures downstream concordance analysis can align RPS (metabolomic control), RAS (transcriptomic control), and FFD (model flux envelope) signals across the same reaction set.

## Related tools

- **constraint-based stoichiometric metabolic models** (Provides reaction stoichiometry and metabolite identifiers; serves as the scaffold for mapping metabolomics measurements to model reactions.)
- **MassHunter ProFinder** (Performs data analysis and isotopic natural abundance correction on LC-MS raw data prior to RPS computation.)
- **INTEGRATE pipeline (Step 10: concordanceAnalysis.py)** (Executes concordance analysis comparing RPS, RAS, and FFD datasets to discriminate transcriptional vs. metabolic regulation.) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/concordanceAnalysis.py --metabolic_model ENGRO2_irrev.xml --metabolic_data metabolomics_LM.csv --dict_to_convert_metnames metsEngroVsMetabolomics.csv --valLog 1.2
```

## Evaluation signals

- RPS dataset contains exactly 81 reactions (or the correct count for your model subset) with all substrate concentrations available and no NaN or missing values.
- RPS values are positive and finite; verify no computational underflow or overflow occurred during product calculation (check log-space intermediate values if needed).
- RPS sample indices and reaction IDs match exactly with parallel FFD and RAS datasets to ensure downstream concordance analysis alignment.
- Visual inspection: RPS values vary monotonically with substrate abundance variation across samples; verify by plotting RPS vs. mean substrate concentration per reaction.
- Exclusion log documents the count and identity of reactions dropped due to missing substrates; this count should be consistent across runs and scientifically justifiable.

## Limitations

- Enzymatic activity is neglected; the mass action law assumption does not account for enzyme expression, cofactor availability, or catalytic efficiency, leading to incomplete metabolic control prediction.
- Allosteric regulation, product inhibition, and cofactor/prosthetic group effects cannot be discriminated from the RPS output without additional kinetic data; RPS reflects only substrate availability effects.
- Limited metabolite coverage in the metabolomics dataset constrains the number of analyzable reactions; reactions with unmeasured substrates must be excluded, reducing model scope.
- RPS is a steady-state propensity proxy derived from mass action kinetics; it does not model transient dynamics, feedback loops, or compartmentalization effects.
- Metabolomics measurement uncertainty (e.g., absolute quantification errors, batch effects) directly propagates to RPS values; normalization and quality filtering are prerequisites.

## Evidence

- [other] RPS computation formula and mass action law application: "The RPS for a reaction r in cell line c is computed as the product of substrate concentrations each raised to their stoichiometric coefficient (RPSc_r = ∏[X_q]^s_r,q), implementing the mass action"
- [other] Workflow steps for RPS dataset construction: "For each of the 81 eligible reactions and each cell line, compute the Reaction Propensity Score (RPS) as the product of substrate concentrations raised to their stoichiometric coefficients: RPS_r^c ="
- [readme] Data input sources and model details: "Load intracellular metabolite abundance data (LC-MS normalized values) for the five cell lines from MetaboLights MTBLS3597. Load the ENGRO2 metabolic network model with reaction stoichiometry and"
- [results] Exclusion criterion for missing substrates: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset."
- [intro] Mass action law rationale: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes (metabolic"
- [intro] Enzymatic activity neglect limitation: "Enzymatic activity is neglected in metabolic regulation prediction; only substrate availability is considered."
- [results] Allosteric and kinetic regulation not discriminated: "The phenomenon according to which gene expression and substrate availability agree with one another, but the flux does not agree with any of the two, might be imputed to model inaccuracy, as well as"
