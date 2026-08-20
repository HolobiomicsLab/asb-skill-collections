---
name: microbial-biotransformation-prediction
description: Use when when you have chemical structures (SMILES or molecular structure
  format) and need to forecast what metabolites environmental microbes would produce;
  particularly when assessing pollutant persistence, environmental fate, or xenobiotic
  degradation pathways in aquatic and terrestrial settings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2814
  tools:
  - BioTransformer
  - EnviPath
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab). Env. module data CC-BY-NC-SA (enviPath/EAWAG).
    url: https://bitbucket.org/wishartlab/biotransformer3.0jar.git
  license_tier: noncommercial
derived_from:
- doi: 10.1093/nar/gkac408
  title: BioTransformer 3.0
evidence_spans:
- BioTransformer's environmental microbial degradation module uses data from the EAWAG's
  Biodegradation and Biocatalysis Database
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biotransformer_3_0_2_cq
    doi: 10.1093/nar/gkac408
    title: BioTransformer 3.0
  dedup_kept_from: coll_biotransformer_3_0_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/nar/gkac408
  all_source_dois:
  - 10.1093/nar/gkac408
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# microbial-biotransformation-prediction

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Predict environmental biotransformation products of chemical compounds using rule-based microbial degradation modules. This skill applies curated biodegradation pathway databases to generate parent-product relationships and reaction types for compounds in SMILES or structure format.

## When to use

When you have chemical structures (SMILES or molecular structure format) and need to forecast what metabolites environmental microbes would produce; particularly when assessing pollutant persistence, environmental fate, or xenobiotic degradation pathways in aquatic and terrestrial settings.

## When NOT to use

- Input compounds lack sufficient structural diversity or known biochemical pathways in EAWAG-BBD; predictions will be sparse or absent.
- Analysis goal requires human/mammalian pharmacokinetic metabolism rather than environmental microbial degradation pathways.
- Compounds are proprietary or restricted under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 licensing constraints.

## Inputs

- Chemical compound structures in SMILES format
- Molecular structure files (mol, sdf, or equivalent format)
- Chemical structure objects loaded in BioTransformer

## Outputs

- Predicted biotransformation product structures
- Parent-product relationship pairs
- Reaction type classifications
- Biotransformation reaction information and metadata

## How to apply

Load compound structures (SMILES or structure format) into BioTransformer 3.0 jar executable and execute the environmental microbial degradation module, specifying the EAWAG Biodegradation and Biocatalysis Database rule set as the biotransformation rule source. The module applies curated microbial transformation rules derived from EAWAG-BBD to generate predicted metabolite structures and associated reaction metadata. Parse the output to extract predicted biotransformation products with parent-product relationships and reaction type classifications. Validate predictions by cross-referencing reaction types against documented microbial enzymatic pathways in the source database.

## Related tools

- **BioTransformer** (Executes rule-based biotransformation prediction; encapsulates the environmental microbial degradation module and EAWAG rule set integration) — bitbucket.org/wishartlab/biotransformer3.0jar
- **EnviPath** (Licenses and maintains the EAWAG Biodegradation and Biocatalysis Database rule set underlying the environmental microbial degradation module)

## Evaluation signals

- Predicted metabolites form a connected parent-product graph with documented reaction types (e.g., hydroxylation, dehydrogenation, cleavage).
- All predicted products are valid chemical structures with consistent SMILES or structure encoding and no malformed molecules.
- Reaction types and metabolite structures are traceable to EAWAG-BBD rule entries; manual spot-checking of 5–10 predictions against published biodegradation literature shows ≥70% agreement with known pathways.
- No output metabolites are identical to the input parent compound (except in null/no-degradation cases, which should be explicitly flagged).
- Predicted pathway depth (number of sequential biotransformation steps) aligns with known microbial catabolic potential for the compound class.

## Limitations

- Predictions are constrained to biotransformations documented in EAWAG-BBD; novel or newly discovered microbial pathways will not be captured.
- Environmental conditions (pH, temperature, oxygen availability, microbial consortium composition) are abstracted away; rule-based predictions do not account for kinetics or bioavailability.
- EAWAG-BBD focuses on aerobic and anaerobic bacterial pathways; fungi and other eukaryotic microbes may follow different metabolic logic not fully represented.
- Outputs are structure predictions only; no experimental validation or biodegradation rate constants are provided.

## Evidence

- [intro] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database: "The environmental microbial degradation module relies on the EAWAG's Biodegradation and Biocatalysis Database"
- [other] Load input compounds, execute module with EAWAG rule set, collect output, and parse metabolites: "1. Load input compounds (SMILES or structure format) into BioTransformer 3.0 jar executable. 2. Execute the environmental microbial degradation module specifying the EAWAG Biodegradation and"
- [intro] EAWAG-BBD is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International: "licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license by EnviPath"
