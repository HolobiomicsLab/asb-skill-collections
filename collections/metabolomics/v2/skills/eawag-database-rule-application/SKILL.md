---
name: eawag-database-rule-application
description: Use when when you have small-molecule structures (SMILES or structure format) and need to predict their environmental biotransformation pathways under microbial degradation conditions, particularly when the degradation rules must be drawn from curated, experimentally-validated biodegradation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0199
  tools:
  - BioTransformer
  - EnviPath
derived_from:
- doi: 10.1093/nar/gkac408
  title: BioTransformer 3.0
evidence_spans:
- BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database
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
---

# eawag-database-rule-application

## Summary

Apply the EAWAG Biodegradation and Biocatalysis Database rule set within BioTransformer to predict microbial biotransformation products for input compounds. This skill bridges curated environmental biodegradation knowledge with computational prediction to generate parent–product relationships and reaction types.

## When to use

When you have small-molecule structures (SMILES or structure format) and need to predict their environmental biotransformation pathways under microbial degradation conditions, particularly when the degradation rules must be drawn from curated, experimentally-validated biodegradation literature rather than mammalian metabolism or Phase I/II enzymatic rules.

## When NOT to use

- Input compounds are already known metabolites or degradation products (no parent structure available).
- Analysis goal is mammalian Phase I/II metabolism prediction; use BioTransformer's Phase I or Phase II modules instead.
- Compounds are proteins, nucleic acids, or macromolecules outside the scope of small-molecule biodegradation rules.

## Inputs

- Chemical structures in SMILES format or structure file format
- Compound identifier (e.g., IUPAC name, InChI, or CAS number)

## Outputs

- Predicted biotransformation products (metabolite structures)
- Parent–product relationship graph
- Reaction types and transformations applied
- Metabolite identifiers and SMILES strings

## How to apply

Load input compounds in SMILES or structure format into the BioTransformer 3.0 jar executable. Execute the environmental microbial degradation module by explicitly specifying the EAWAG Biodegradation and Biocatalysis Database rule set as the target rule engine (not the Phase I, Phase II, or gut microbial modules). The module will apply transformation rules mined from the EAWAG database to generate a reaction tree. Parse the output to extract predicted metabolites, parent–product linkages, and associated reaction types. Validate that the output contains structured biotransformation products with traceable rule provenance, confirming that rules originated from the EAWAG database rather than other BioTransformer modules.

## Related tools

- **BioTransformer** (Executable jar that hosts the environmental microbial degradation module and applies EAWAG-derived biotransformation rules to input compounds.) — bitbucket.org/wishartlab/biotransformer3.0jar
- **EnviPath** (Curator and licensor of the EAWAG Biodegradation and Biocatalysis Database underlying the rule set.)

## Examples

```
java -jar biotransformer3.0.jar -ismi compound.smi -oformat json -bicestype EAWAG_BBD > predictions.json
```

## Evaluation signals

- Output metabolites are valid chemical structures (parseable SMILES with correct valence and connectivity).
- Parent–product relationships form a coherent biotransformation tree (no orphaned or circular edges).
- All reaction transformations are traceable to EAWAG database rules (metadata or rule identifiers are present in output).
- Predicted metabolites are chemically plausible degradation intermediates (e.g., hydroxylation, decarboxylation, deamination) consistent with environmental microbial pathways.
- Output does not duplicate reaction rules or generate identical metabolites from multiple pathways unless multi-route degradation is documented in the EAWAG database.

## Limitations

- EAWAG database rule set is limited to biodegradation pathways documented in literature; novel or undocumented transformations will not be predicted.
- Predictions assume environmental microbial consortia with generic catabolic capabilities; organism-specific or site-specific degradation cannot be modeled.
- License (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International) restricts commercial use of predictions without attribution and reciprocal licensing.
- No changelog available for the EAWAG database rule set; version tracking and rule update history are not documented.

## Evidence

- [intro] EAWAG database dependency: "The environmental microbial degradation module relies on the EAWAG's Biodegradation and Biocatalysis Database"
- [intro] Licensing constraint: "licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license by EnviPath"
- [other] Workflow: input format and execution: "Load input compounds (SMILES or structure format) into BioTransformer 3.0 jar executable"
- [other] Workflow: module specification: "Execute the environmental microbial degradation module specifying the EAWAG Biodegradation and Biocatalysis Database rule set"
- [other] Workflow: output parsing: "Parse and structure predicted metabolites with parent-product relationships and reaction types"
