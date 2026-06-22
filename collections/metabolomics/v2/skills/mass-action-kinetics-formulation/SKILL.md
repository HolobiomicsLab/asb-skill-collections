---
name: mass-action-kinetics-formulation
description: Use when you have intracellular metabolomics concentration measurements across multiple cell lines or conditions, a stoichiometric metabolic network model with reaction-metabolite associations, and you need to predict how differences in substrate availability (independent of enzyme expression).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2259
  tools:
  - ENGRO2
  - createMetabolicDataset.py
  - concordanceAnalysis.py
  - constraint-based stoichiometric metabolic models
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans: []
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
---

# mass-action-kinetics-formulation

## Summary

Computes Reaction Propensity Scores (RPS) from intracellular metabolomics abundance data using mass action law formulation, quantifying the expected relative metabolic flux changes across cell lines based on substrate availability alone. This provides a metabolic-regulation baseline independent of gene expression effects.

## When to use

Apply this skill when you have intracellular metabolomics concentration measurements across multiple cell lines or conditions, a stoichiometric metabolic network model with reaction-metabolite associations, and you need to predict how differences in substrate availability (independent of enzyme expression) translate into differences in metabolic flux propensity. Use it specifically to isolate the metabolic regulation layer (substrate-driven) from the transcriptional regulation layer (enzyme abundance-driven) for concordance analysis.

## When NOT to use

- When extracellular flux data or direct metabolic flux measurements (e.g., from labeled substrate tracing) are available and preferred; RPS is a proxy, not direct flux measurement.
- When substrate concentrations are not measured intracellularly or are only available in extracellular medium; model assumes intracellular substrate availability drives flux, not external concentration gradients.
- When the metabolic network lacks stoichiometric coefficients or reaction-metabolite associations; the mass action law formulation requires complete stoichiometric data.

## Inputs

- Intracellular metabolomics abundance dataset (metabolite concentrations per cell line, replicated measurements)
- Stoichiometric metabolic network model with reaction-metabolite associations and stoichiometric coefficients (e.g., ENGRO2 in SBML or similar format)
- Conversion mapping between metabolomics metabolite identifiers and model metabolite identifiers

## Outputs

- Normalized RPS dataset (table with reactions as rows, cell lines as columns, normalized RPS values ∈ [0,1] as entries)
- Pre-aggregation RPS scores (per-reaction, per-cell-line, per-replicate, before normalization)
- Metadata log of omitted reactions (those with unmeasured substrates, per cell line)

## How to apply

Load intracellular metabolomics abundance data (metabolite concentrations per cell line) and the stoichiometric metabolic network model (e.g., ENGRO2) with reaction-metabolite associations and stoichiometric coefficients. For each reaction and each cell line, retrieve all substrate metabolites from the model stoichiometry and their measured intracellular concentrations; omit any reaction missing one or more substrate measurements. Compute the RPS for each eligible reaction in each cell line as the product of substrate concentrations each raised to their stoichiometric coefficient power: RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q), where [X_q] is substrate q concentration and s_r,q is its stoichiometric coefficient. Aggregate RPS values across biological replicates within each cell line using median or mean as appropriate to produce a cell-line-level RPS score. Normalize RPS scores within each reaction across all cell lines by dividing by the maximum RPS value observed for that reaction, yielding dimensionless propensity scores bounded in [0,1] suitable for cross-reaction and cross-cell-line comparison.

## Related tools

- **ENGRO2** (Stoichiometric metabolic network model providing reaction-metabolite associations and stoichiometric coefficients for RPS computation)
- **createMetabolicDataset.py** (Preprocessing and preparation of metabolomics data for RPS calculation; quality filtering and mean computation across replicates) — https://github.com/qLSLab/integrate
- **concordanceAnalysis.py** (Post-processing integration and comparison of RPS output against RAS (transcription-derived scores) to identify metabolic vs. transcriptional regulation) — https://github.com/qLSLab/integrate
- **constraint-based stoichiometric metabolic models** (Formal scaffold providing stoichiometry, reaction definitions, and metabolite associations necessary for mass action law application)

## Evaluation signals

- All reactions in the output RPS table have at least one substrate measurement in at least one cell line; check that no reactions are missing that should have valid data.
- Normalized RPS scores fall within [0, 1] for all reactions and cell lines; the maximum RPS per reaction equals 1.0 (verification of normalization).
- RPS values correlate positively with intracellular substrate concentrations (mass action relationship: higher substrate → higher RPS); audit a sample of 5–10 reactions visually.
- Missing substrates cause consistent reaction omission across the pipeline; verify that reactions with unmeasured substrates are reported in the omission log and absent from the final RPS table.
- RPS concordance with RAS (Reaction Activity Scores from transcriptomics) is significantly less than perfect (Cohen κ and Pearson r < 0.8), confirming that substrate availability captures a distinct regulatory layer from gene expression.

## Limitations

- If any substrate is unmeasured, the entire reaction is omitted from the RPS dataset; this may remove important metabolic reactions and limits coverage to well-measured metabolites.
- RPS is a propensity score based on mass action law, not a direct measurement of metabolic flux; it does not account for enzyme kinetics (Km, Vmax), allosteric regulation, feedback inhibition, or post-translational modifications.
- Substrate concentrations are assumed to be at steady state within the 48-hour measurement window; dynamic changes or compartmentalization effects are not captured.
- RPS assumes all reactions are mass-action limited and does not distinguish reactions controlled by regulatory proteins, cofactor availability, or other non-concentration-dependent mechanisms.
- Cross-cell-line normalization by maximum RPS may obscure absolute differences in metabolic propensity; normalized scores are relative and suitable only for concordance analysis, not absolute flux prediction.

## Evidence

- [other] For each reaction r and cell line c, the Reaction Propensity Score (RPS) is computed as the product of substrate concentrations each raised to their stoichiometric coefficients: RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q): "For each reaction r and cell line c, the Reaction Propensity Score (RPS) is computed as the product of substrate concentrations each raised to their stoichiometric coefficients: RPS_r^c = ∏(q=1 to N)"
- [other] If any substrate is unmeasured, the reaction is omitted from the RPS dataset.: "If any substrate is unmeasured, the reaction is omitted from the RPS dataset."
- [other] For each metabolic reaction and each cell line, identify all substrate metabolites from the model's stoichiometry and retrieve their measured intracellular concentrations; omit reactions missing one or more substrate abundance measurements.: "For each metabolic reaction and each cell line, identify all substrate metabolites from the model's stoichiometry and retrieve their measured intracellular concentrations; omit reactions missing one"
- [other] Aggregate RPS values across biological replicates within each cell line (using median or mean as appropriate) to produce a cell-line-level RPS score for each reaction.: "Aggregate RPS values across biological replicates within each cell line (using median or mean as appropriate) to produce a cell-line-level RPS score for each reaction."
- [other] Normalize RPS scores within each reaction across all cell lines by dividing by the maximum RPS value observed for that reaction.: "Normalize RPS scores within each reaction across all cell lines by dividing by the maximum RPS value observed for that reaction."
- [intro] INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes"
- [full_text] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
