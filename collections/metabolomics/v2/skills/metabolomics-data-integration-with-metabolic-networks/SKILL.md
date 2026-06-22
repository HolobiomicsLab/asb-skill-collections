---
name: metabolomics-data-integration-with-metabolic-networks
description: Use when you have measured intracellular metabolite concentrations (e.g., via LC–MS/MS) across multiple cell lines or samples and want to predict which metabolic reactions are substrate-limited versus transcriptionally regulated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3805
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0092
  tools:
  - constraint-based stoichiometric metabolic models
  - INTEGRATE pipeline (qLSLab/integrate)
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-integration-with-metabolic-networks

## Summary

Integrate intracellular metabolomics abundance data with constraint-based stoichiometric metabolic network models to compute Reaction Propensity Scores (RPS) that quantify expected metabolic flux changes across biological samples based on substrate availability alone. This enables discrimination of metabolically-controlled from transcriptionally-controlled metabolic fluxes when intersected with transcriptomic predictions.

## When to use

You have measured intracellular metabolite concentrations (e.g., via LC–MS/MS) across multiple cell lines or samples and want to predict which metabolic reactions are substrate-limited versus transcriptionally regulated. Use this skill when you need to isolate the contribution of metabolite availability to flux differences from the contribution of enzyme expression, or when direct flux measurement via isotope labeling is infeasible.

## When NOT to use

- Input metabolomics data is already aggregated at the pathway or functional module level rather than individual metabolite abundances.
- You require direct flux measurements or flux inference that accounts for allosteric regulation, cofactor availability, or enzyme kinetics beyond mass action (use 13C-MFA or flux sampling instead).
- The metabolic model lacks stoichiometric coefficients or reaction–metabolite associations (e.g., reactions without defined substrates).

## Inputs

- intracellular metabolomics abundance dataset (e.g., CSV with metabolite IDs as rows, samples/cell lines as columns, concentration values)
- constraint-based stoichiometric metabolic network model in SBML or JSON format (e.g., ENGRO2) with reaction–metabolite associations and stoichiometric coefficients
- mapping file between metabolomics dataset metabolite identifiers and model metabolite identifiers (e.g., 'metsEngroVsMetabolomics.csv')

## Outputs

- normalized Reaction Propensity Score (RPS) table: CSV with reactions as rows (column 'Rxn'), sample-level mean and normalized RPS columns (e.g., 'mean_MCF102A', 'norm_MCF102A')
- reactions excluded from RPS computation (those with unmeasured substrates) and their stoichiometric requirements

## How to apply

Load intracellular metabolomics abundance data (metabolite concentrations per sample) and a stoichiometric metabolic model (e.g., ENGRO2 with reaction–metabolite associations). For each reaction and each sample, identify all substrate metabolites from the model's stoichiometry and retrieve their measured intracellular concentrations; omit reactions missing one or more substrate measurements. Compute the Reaction Propensity Score (RPS) for each eligible reaction in each sample as the product of substrate concentrations each raised to their stoichiometric coefficient power: RPS_r^c = ∏[X_q]^(s_r,q), following mass action law formulation. Aggregate RPS values across biological replicates within each sample (median or mean) to produce sample-level RPS scores. Normalize RPS scores within each reaction across all samples by dividing by the maximum RPS observed for that reaction. Output a normalized RPS table with reactions as rows, samples as columns, and normalized RPS entries (range [0,1]).

## Related tools

- **constraint-based stoichiometric metabolic models** (scaffold for reaction–metabolite associations and stoichiometric coefficients; provides GPR rules for integration with transcriptomics)
- **INTEGRATE pipeline (qLSLab/integrate)** (complete computational workflow that wraps RPS computation, normalization, and concordance analysis with RAS (transcriptomics) output) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/createMetabolicDataset.py --metabolic_model ENGRO2_irrev.xml --metabolic_data metabolomics_LM.csv --dict_to_convert_metnames metsEngroVsMetabolomics.csv --output_means medie_Met.csv
```

## Evaluation signals

- All reactions in the output table have valid, non-zero normalized RPS values in the range [0, 1] across samples; reactions with unmeasured substrates are consistently excluded.
- RPS values for a given reaction across samples scale monotonically with the product of substrate concentrations, with maximum RPS = 1.0 for the sample with highest predicted substrate availability.
- Concordance with Reaction Activity Scores (RAS) derived from transcriptomics (via Cohen's kappa or Pearson correlation) identifies reactions where substrate availability and gene expression regulation align or diverge.
- Replicates within a sample have similar mean RPS values (low coefficient of variation), indicating reproducible metabolite quantification.
- RPS values for substrate-limited reactions (those showing flux changes despite constant enzyme expression) are significantly different across samples; RPS values for transcriptionally-controlled reactions are similar despite transcript differences.

## Limitations

- If any substrate for a reaction is absent from the metabolomics dataset, the entire reaction is omitted from RPS computation, potentially excluding important hub reactions with multiple substrates.
- RPS assumes mass action law kinetics (proportional to substrate concentration raised to stoichiometric power) and does not account for allosteric inhibition, cofactor depletion, pH-dependent activity, or enzyme kinetic saturation.
- RPS does not capture product inhibition or feedback regulation; a reaction with high RPS may still have low flux if product concentration is inhibitory.
- Intracellular metabolite concentrations are often measured in a single metabolic state (e.g., steady-state culture at 48 h); RPS may not reflect flux control in dynamic or heterogeneous cellular conditions.
- Stoichiometric coefficients must be accurate in the metabolic model; errors in stoichiometry or missing reactions propagate directly to RPS values.

## Evidence

- [other] For each reaction r and cell line c, the Reaction Propensity Score (RPS) is computed as the product of substrate concentrations each raised to their stoichiometric coefficients: RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q), where [X_q] is substrate concentration and s_r,q is the stoichiometric coefficient.: "RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q), where [X_q] is substrate concentration and s_r,q is the stoichiometric coefficient."
- [other] If any substrate is unmeasured, the reaction is omitted from the RPS dataset.: "If any substrate is unmeasured, the reaction is omitted from the RPS dataset."
- [intro] INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes"
- [other] Aggregate RPS values across biological replicates within each cell line (using median or mean as appropriate) to produce a cell-line-level RPS score for each reaction. Normalize RPS scores within each reaction across all cell lines by dividing by the maximum RPS value observed for that reaction.: "Aggregate RPS values across biological replicates within each cell line (using median or mean as appropriate) to produce a cell-line-level RPS score for each reaction. Normalize RPS scores within"
- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [intro] The intersection of the two output datasets discriminates fluxes regulated at the metabolic and/or gene expression level: "The intersection of the two output datasets discriminates fluxes regulated at the metabolic and/or gene expression level"
