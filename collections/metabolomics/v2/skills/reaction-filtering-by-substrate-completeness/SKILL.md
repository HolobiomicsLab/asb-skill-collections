---
name: reaction-filtering-by-substrate-completeness
description: Use when you have loaded intracellular metabolomics data (LC-MS normalized abundances) and a stoichiometric metabolic model with multiple reactions, and you plan to compute reaction propensity scores or other flux-related metrics that depend on substrate concentrations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_2640
  - http://edamontology.org/topic_3407
  tools:
  - MassHunter ProFinder
  - constraint-based stoichiometric metabolic models
  - concordanceAnalysis.py
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

# reaction-filtering-by-substrate-completeness

## Summary

Filter metabolic reactions to retain only those with complete quantification of all substrate abundances in a metabolomics dataset, enabling reliable downstream computation of Reaction Propensity Scores (RPS) and concordance analysis. This is a quality-control step that prevents NaN/undefined computations when applying mass action law formulations.

## When to use

You have loaded intracellular metabolomics data (LC-MS normalized abundances) and a stoichiometric metabolic model with multiple reactions, and you plan to compute reaction propensity scores or other flux-related metrics that depend on substrate concentrations. Apply this filter before any reaction-level computation that assumes all substrates for a given reaction are quantified.

## When NOT to use

- Metabolomics data is already aggregated or normalized at the reaction level (substrate information is lost).
- You are performing pathway-level rather than reaction-level analysis where individual substrate coverage is irrelevant.
- Computational cost of screening all reactions is prohibitive and you need a sampling-based alternative.

## Inputs

- SBML or constraint-based metabolic model (e.g., ENGRO2) with reaction stoichiometry
- Intracellular metabolomics dataset with LC-MS normalized metabolite abundances indexed by sample/cell line
- Metabolite ID mapping table (if metabolomics IDs differ from model IDs)

## Outputs

- Filtered reaction list (reaction IDs) meeting substrate completeness criterion
- Structured table with columns: reaction ID, stoichiometry details, and eligibility flags per cell line
- Count of eligible vs. excluded reactions (quality metric)

## How to apply

Iterate over all reactions in the metabolic model (e.g., 81 reactions in ENGRO2). For each reaction, retrieve its stoichiometric substrate list. Check whether every substrate metabolite has a quantified abundance measurement in the metabolomics dataset for each cell line or sample. Exclude any reaction if even a single substrate is missing from the metabolomics measurements across any sample. Retain only reactions meeting this completeness criterion in a filtered dataset indexed by reaction ID and cell line. Document the number of reactions retained versus excluded to assess metabolite coverage constraints.

## Related tools

- **constraint-based stoichiometric metabolic models** (Source of reaction definitions and stoichiometric coefficients used to identify substrate requirements for filtering)
- **MassHunter ProFinder** (Generates and normalizes LC-MS metabolomics abundances that are checked for completeness during filtering)
- **concordanceAnalysis.py** (Downstream step that operates only on filtered reaction dataset to compute RPS vs. FFD and RAS concordance) — https://github.com/qLSLab/integrate

## Evaluation signals

- Filtered reaction dataset contains no reactions with NaN or missing substrate concentrations in any sample.
- Number of retained reactions (typically 81 out of a larger total in ENGRO2) is documented and consistent across replicate runs.
- Ratio of eligible reactions to total reactions in model reflects expected metabolite coverage limitations.
- Downstream RPS computation completes without undefined value errors when applied to the filtered reaction set.
- Cross-checking: for each retained reaction in each sample, verify that all stoichiometric substrates appear in the metabolomics abundance table with numeric values.

## Limitations

- Severely reduces the reaction set when metabolomics coverage is sparse; only reactions with ALL substrates quantified are retained, potentially losing mechanistic insight into reactions with partial data.
- Cannot infer or impute missing substrate abundances; filter is binary (keep/exclude) rather than probabilistic.
- Does not account for measurement uncertainty or detection limits; a substrate below LOD still fails the completeness test.
- Coverage depends on LC-MS method design (m/z range, polarity) and metabolite ionization efficiency; polar compounds and cofactors (e.g., ATP, NADH) are often underrepresented.

## Evidence

- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [results] Fig 4A reports the concordance level variations for the 81 metabolic reactions of ENGRO2 for which quantification of all substrate abundances was available: "Fig 4A reports the concordance level variations for the 81 metabolic reactions of ENGRO2 for which quantification of all substrate abundances was available"
- [other] Reactions included in concordance analysis only if quantification of all substrate abundances was available: "Reactions included in concordance analysis only if quantification of all substrate abundances was available"
- [other] Load the ENGRO2 metabolic network model with reaction stoichiometry and identify 81 reactions with quantified substrate abundances in all five cell lines; exclude any reaction with a missing substrate measurement.: "Load the ENGRO2 metabolic network model with reaction stoichiometry and identify 81 reactions with quantified substrate abundances in all five cell lines; exclude any reaction with a missing"
- [results] the uncertainty mainly depends on the limited number of cell lines for which we are assessing the agreement. Other possible sources of uncertainty are the uncertainty in the experimental data, the: "the limited number of cell lines for which we are assessing the agreement. Other possible sources of uncertainty are the uncertainty in the experimental data"
