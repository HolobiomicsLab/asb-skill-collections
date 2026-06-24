---
name: substrate-concentration-normalization
description: Use when you have LC-MS normalized intracellular metabolite abundance
  data from multiple cell lines (or samples) and need to compute reaction-level propensity
  scores that account for substrate availability as a predictor of metabolic flux.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0821
  - http://edamontology.org/topic_2259
  tools:
  - MassHunter ProFinder
  - Agilent 1290 Infinity UHPLC system
  - Agilent 6550 iFunnel Q-TOF mass spectrometer
  - constraint-based stoichiometric metabolic models
  - INTEGRATE pipeline (qLSLab/integrate)
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

# Substrate Concentration Normalization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Normalize intracellular metabolite abundances from LC-MS measurements to enable stoichiometry-aware computation of Reaction Propensity Scores (RPS) across multiple cell lines. This skill ensures that substrate concentrations are comparable and correctly weighted by their stoichiometric coefficients in mass action law calculations.

## When to use

Apply this skill when you have LC-MS normalized intracellular metabolite abundance data from multiple cell lines (or samples) and need to compute reaction-level propensity scores that account for substrate availability as a predictor of metabolic flux. Specifically, use this when you are preparing substrate concentrations for mass action law calculations to distinguish between transcriptional and metabolic control of reactions.

## When NOT to use

- Do not use this skill if your metabolomics data is already aggregated at the pathway or flux level (i.e., not individual metabolite abundances).
- Do not apply this skill if you are working with gene expression data (RNA-seq) instead of or without metabolomics; substrate normalization requires measured intracellular concentrations, not transcript counts.
- Do not use this skill if your goal is to normalize enzyme activity or protein abundance; this skill normalizes substrate concentrations specifically for mass action law-based flux prediction.

## Inputs

- LC-MS normalized intracellular metabolite abundance data (e.g., from MetaboLights MTBLS3597)
- Metabolic network model with reaction stoichiometry (e.g., ENGRO2 in SBML format)
- Metabolite ID conversion dictionary mapping metabolomics IDs to model metabolite IDs

## Outputs

- Normalized substrate concentration table indexed by metabolite ID, cell line, and replicate
- Quality-filtered dataset with reactions retained only if all substrate abundances are quantified
- Structured CSV with columns for metabolite ID, stoichiometry details, and normalized concentrations per cell line

## How to apply

Load LC-MS normalized metabolite abundance data (e.g., from MetaboLights or similar repositories) for all samples of interest. Match metabolite IDs between the metabolomics dataset and the metabolic network model using a conversion dictionary (e.g., 'metsEngroVsMetabolomics.csv'). For each reaction in the model, verify that all substrate metabolites have quantified abundance values; if any substrate is missing from the metabolomics measurements, exclude that reaction from downstream RPS computation. Retain the normalized abundance values as-is for each metabolite in each cell line, since these will be raised to their respective stoichiometric coefficients during RPS calculation. Organize the normalized substrate concentrations into a structured table indexed by metabolite ID, cell line, and replicate, matching the format used for parallel transcriptomics-derived (RAS) and constraint-based flux (FFD) datasets to enable downstream concordance analysis.

## Related tools

- **MassHunter ProFinder** (LC-MS data acquisition and isotopic natural abundance correction for metabolite abundance quantification)
- **Agilent 1290 Infinity UHPLC system** (LC separation of metabolites prior to MS detection)
- **Agilent 6550 iFunnel Q-TOF mass spectrometer** (MS detection and mass measurement of metabolites (m/z 60–1050))
- **constraint-based stoichiometric metabolic models** (Provides reaction stoichiometry and metabolite definitions for substrate filtering and normalization context)
- **INTEGRATE pipeline (qLSLab/integrate)** (Step 9 (createMetabolicDataset.py) and downstream concordance analysis integrate normalized substrate concentrations with RAS and FFD outputs) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/createMetabolicDataset.py --metabolic_data metabolomics_LM.csv --dict_to_convert_metnames metsEngroVsMetabolomics.csv --metabolic_model ENGRO2_irrev.xml --data_quality_filter 1 --namefile resultsMetabolomic
```

## Evaluation signals

- All substrate metabolites for each retained reaction have non-null, quantified LC-MS abundance values across all cell lines and replicates.
- Reactions with any missing substrate measurement are excluded from the dataset; verify row count matches the expected number of reactions with complete substrate coverage (e.g., 81 reactions for ENGRO2 in the article).
- Normalized concentration values are positive real numbers in the expected physiological range (e.g., micromolar to millimolar for intracellular metabolites); outliers or extreme values trigger review of LC-MS quality or conversion dictionary accuracy.
- Metabolite ID conversion is bidirectional and complete; all model metabolite IDs referenced in reaction stoichiometry can be mapped to metabolomics dataset columns, and vice versa.
- Organized substrate concentration table can be directly indexed by (reaction_id, cell_line, replicate) and passed to RPS calculation without missing or malformed entries; schema matches the structure of parallel RAS and FFD datasets for downstream concordance analysis.

## Limitations

- Limited metabolite coverage in the metabolomics dataset constrains the number of reactions that can be analyzed; reactions with unmeasured substrates must be excluded, potentially reducing the scope of flux prediction.
- Normalization assumes that LC-MS measurements are directly proportional to intracellular concentration; recovery bias, ionization efficiency variation, or matrix effects may introduce systematic errors not captured by normalization alone.
- This skill captures substrate availability only and neglects enzymatic activity, allosteric regulation, product inhibition, and cofactor/prosthetic group effects; differences in metabolic flux may not be fully explained by substrate concentration alone.
- Cross-cell-line or cross-sample comparisons depend on consistent LC-MS protocol and instrument tuning; differences in metabolite abundances may reflect technical variation rather than biological differences if normalization does not account for batch effects or instrumental drift.
- The conversion dictionary between metabolomics IDs and model metabolite IDs must be manually curated and verified; errors in mapping will lead to loss of reactions or incorrect stoichiometric calculations in downstream RPS computation.

## Evidence

- [other] Load intracellular metabolite abundance data (LC-MS normalized values) for the five cell lines from MetaboLights MTBLS3597.: "Load intracellular metabolite abundance data (LC-MS normalized values) for the five cell lines from MetaboLights MTBLS3597"
- [other] identify 81 reactions with quantified substrate abundances in all five cell lines; exclude any reaction with a missing substrate measurement.: "identify 81 reactions with quantified substrate abundances in all five cell lines; exclude any reaction with a missing substrate measurement"
- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [results] Data were acquired from m/z 60–1050. Data analysis and isotopic natural abundance correction were performed with MassHunter ProFinder: "Data were acquired from m/z 60–1050. Data analysis and isotopic natural abundance correction were performed with MassHunter ProFinder"
- [other] Organize RPS values into a dataset indexed by reaction and cell line, matching the structure of the parallel Feasible Flux Distribution (FFD) and Reaction Activity Score (RAS) datasets for downstream concordance analysis.: "Organize RPS values into a dataset indexed by reaction and cell line, matching the structure of the parallel Feasible Flux Distribution (FFD) and Reaction Activity Score (RAS) datasets for downstream"
- [readme] dict_to_convert_metnames: Conversion file between ID of metabolites in metabolomics dataset and ID of metabolites in the input model.: "dict_to_convert_metnames: Conversion file between ID of metabolites in metabolomics dataset and ID of metabolites in the input model"
