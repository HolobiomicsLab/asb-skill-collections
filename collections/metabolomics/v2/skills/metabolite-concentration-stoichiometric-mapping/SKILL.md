---
name: metabolite-concentration-stoichiometric-mapping
description: Use when you have intracellular metabolomics abundance data (absolute or relative concentrations) for multiple cell lines or conditions, a constraint-based stoichiometric metabolic model with reaction-metabolite associations, and you need to disentangle how differences in substrate concentration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0599
  tools:
  - constraint-based stoichiometric metabolic models
  - INTEGRATE pipeline
  - constraint-based stoichiometric metabolic models (ENGRO2)
  - Python (v3.0+)
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
---

# metabolite-concentration-stoichiometric-mapping

## Summary

Map measured intracellular metabolite concentrations to stoichiometric coefficients in a constraint-based metabolic model to compute Reaction Propensity Scores (RPS) that quantify expected metabolic flux differences driven by substrate availability alone, independent of gene expression regulation.

## When to use

Apply this skill when you have intracellular metabolomics abundance data (absolute or relative concentrations) for multiple cell lines or conditions, a constraint-based stoichiometric metabolic model with reaction-metabolite associations, and you need to disentangle how differences in substrate concentration translate into metabolic flux differences—distinct from transcriptional regulation of enzyme abundance.

## When NOT to use

- When intracellular metabolite concentrations are not measured or available—RPS requires actual concentration values, not just relative expression or presence/absence.
- When the goal is to assess transcriptional regulation of metabolic enzymes; use this skill for substrate-driven (metabolic-level) regulation only; pair it with transcriptomics-based Reaction Activity Scores (RAS) to discriminate between the two layers.
- When the stoichiometric model lacks reaction-metabolite associations or GPR (gene-protein-reaction) rules are needed for cross-validation with transcriptomics.

## Inputs

- Intracellular metabolomics abundance data (metabolite concentrations per cell line; CSV or TSV format with metabolite IDs and numeric abundance columns)
- Constraint-based stoichiometric metabolic model in SBML format (e.g., ENGRO2) with reaction-metabolite associations and stoichiometric coefficients
- Metabolite identifier mapping/conversion file (linking metabolomics dataset IDs to model metabolite IDs, if nomenclature differs)

## Outputs

- Normalized RPS dataset (CSV table with reactions as rows, cell lines/samples as columns, normalized RPS values [0–1] as entries)
- Reaction omission report (log of reactions excluded due to missing substrate measurements)

## How to apply

For each reaction in the metabolic model and each cell line or sample: (1) retrieve all substrate metabolites and their stoichiometric coefficients from the model's stoichiometry; (2) check whether each substrate has a measured concentration in the metabolomics dataset; if any substrate is unmeasured, exclude that reaction from analysis; (3) compute the Reaction Propensity Score (RPS) as the product of substrate concentrations each raised to their stoichiometric coefficient: RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q); (4) aggregate RPS values across biological replicates within each cell line (using median or mean); (5) normalize RPS scores within each reaction by dividing by the maximum RPS value observed for that reaction across all cell lines. This mass action law formulation assumes reaction rates depend solely on substrate availability and stoichiometry, making it suitable for detecting substrate-driven (metabolic-level) regulation independent of enzyme abundance.

## Related tools

- **INTEGRATE pipeline** (Integrates RPS computation (metabolite-stoichiometry mapping) with transcriptomics-derived RAS scores and constraint-based modeling to discriminate substrate-driven from transcriptionally controlled metabolic fluxes) — https://github.com/qLSLab/integrate
- **constraint-based stoichiometric metabolic models (ENGRO2)** (Provides reaction-metabolite associations, stoichiometric coefficients, and metabolite IDs required to map concentrations to reaction propensity)
- **Python (v3.0+)** (Implementation language for metabolomics data loading, stoichiometric lookup, RPS computation, and aggregation/normalization steps in the INTEGRATE workflow) — https://github.com/qLSLab/integrate

## Examples

```
# Pseudocode/conceptual invocation (from INTEGRATE workflow Step 3)
# Load metabolomics data, retrieve stoichiometry from ENGRO2 model, compute RPS:
for reaction_r in model.reactions:
    for cell_line_c in cell_lines:
        substrates = model.get_stoichiometry(reaction_r)  # dict of {metabolite_id: coeff}
        if all(met in metabolomics_data[cell_line_c] for met in substrates):
            rps = 1.0
            for met, coeff in substrates.items():
                rps *= (metabolomics_data[cell_line_c][met] ** coeff)
            rps_matrix[reaction_r][cell_line_c] = rps
        # else: omit reaction_r from rps_matrix[cell_line_c]
# Normalize per reaction: rps_matrix[r, :] /= rps_matrix[r, :].max()
```

## Evaluation signals

- All reactions with complete substrate measurements (no missing concentration values) have a computed RPS value; reactions with ≥1 unmeasured substrate are recorded in the exclusion log.
- Normalized RPS values fall in the range [0, 1] per reaction (max RPS = 1.0), with cell-line-specific variation; reactions with no flux difference across cell lines should have uniform normalized scores.
- RPS values correlate positively with substrate concentration patterns: cell lines with higher substrate availability for a given reaction should have higher RPS scores for that reaction.
- Concordance analysis (e.g., Cohen's kappa, Pearson correlation) between RPS and RAS (transcriptomics-derived scores) reveals which reactions are regulated at the metabolic (substrate) vs. transcriptional (enzyme abundance) level; high RPS–RAS concordance indicates coordinated regulation.
- Output table schema is consistent: exactly one RPS column per cell line/sample replicate, one row per reaction, numeric entries only.

## Limitations

- If any substrate metabolite for a reaction is unmeasured in the metabolomics dataset, the entire reaction is omitted from RPS computation and analysis, potentially biasing results toward well-measured metabolic modules and away from pathways with sparse coverage.
- RPS assumes steady-state kinetics governed by mass action law; it does not account for allosteric regulation, enzyme kinetic parameters (Km, Vmax), product inhibition, or cofactor availability, potentially overestimating flux differences driven by substrate concentration alone.
- RPS is computed from intracellular metabolite concentrations at a single time point (or aggregated across replicates); it does not capture dynamic flux changes or temporal regulation, limiting applicability to steady-state or cross-sectional study designs.
- Metabolomics measurement error (e.g., low abundance species, technical variability, instrumental drift) propagates directly into RPS values; normalization by maximum does not correct for systematic bias or batch effects in concentration measurements.

## Evidence

- [other] RPS computation formula: "RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q), where [X_q] is substrate q concentration and s_r,q is its stoichiometric coefficient"
- [other] Handling of unmeasured substrates: "If any substrate is unmeasured, the reaction is omitted from the RPS dataset"
- [other] Workflow steps for RPS computation: "For each metabolic reaction and each cell line, identify all substrate metabolites from the model's stoichiometry and retrieve their measured intracellular concentrations; omit reactions missing one"
- [other] Aggregation and normalization: "Aggregate RPS values across biological replicates within each cell line (using median or mean as appropriate) to produce a cell-line-level RPS score for each reaction. Normalize RPS scores within"
- [intro] Integration with mass action law: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes"
- [abstract] Discriminating regulatory layers: "The pipeline discriminates whether differential expression of metabolic enzymes originates differences in metabolic fluxes versus whether differences in substrate availability translate into"
