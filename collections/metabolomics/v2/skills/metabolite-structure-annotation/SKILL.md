---
name: metabolite-structure-annotation
description: Use when you have chemical structures (as SMILES or molecular structure
  formats) of environmental compounds and need to predict their microbial metabolites
  and degradation pathways.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
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
  provenance_tier: literature
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

# metabolite-structure-annotation

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Predict biotransformation products and their parent-product relationships for environmental microbial degradation pathways using rule-based databases. This skill is essential when you need to annotate metabolite structures with likely degradation reactions and transformations derived from curated biodegradation knowledge bases.

## When to use

Apply this skill when you have chemical structures (as SMILES or molecular structure formats) of environmental compounds and need to predict their microbial metabolites and degradation pathways. Use it specifically when the analysis goal requires linking predicted products to known biotransformation reactions from curated databases like EAWAG's Biodegradation and Biocatalysis Database.

## When NOT to use

- Input compounds lack standardized chemical structure representation (SMILES or recognized molecular formats)
- Analysis goal requires human metabolite predictions rather than environmental microbial degradation pathways
- You need real-time or experimental metabolite validation; EAWAG predictions are database-derived, not experimentally verified for your specific compounds

## Inputs

- Chemical structures in SMILES format
- Chemical structures in molecular structure format
- Parent compound identifiers

## Outputs

- Predicted biotransformation product structures
- Parent-product relationship pairs
- Reaction type annotations
- Biotransformation product metadata

## How to apply

Load your input compounds in SMILES or structure format into BioTransformer 3.0's jar executable. Execute the environmental microbial degradation module, specifying the EAWAG Biodegradation and Biocatalysis Database rule set as the biotransformation prediction engine. Parse the module's output to extract predicted metabolite structures and associated reaction metadata, organizing results as parent-product relationship pairs with annotated reaction types. Validate that each predicted product is traceable to a specific reaction rule in the EAWAG database, ensuring predictions are grounded in experimental or curated biodegradation evidence rather than purely computational inference.

## Related tools

- **BioTransformer** (Executable prediction engine for environmental microbial degradation module; applies EAWAG database rules to input compounds to predict biotransformation products and reactions) — bitbucket.org/wishartlab/biotransformer3.0jar
- **EnviPath** (Licensor and steward of the EAWAG's Biodegradation and Biocatalysis Database; provides the rule set for biotransformation predictions under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license)

## Examples

```
java -jar BioTransformer3.0jar -i input.smi -o output.tsv -c EAWAG-BBD
```

## Evaluation signals

- All predicted metabolites are returned as structured chemical objects with valid molecular representations (SMILES or structure format)
- Each predicted product can be traced to a specific reaction type in the EAWAG database output; no orphaned metabolites without reaction annotation
- Parent-product relationship graph is acyclic and traces degradation from input compound to terminal products
- Reaction type annotations match EAWAG's controlled vocabulary; no undefined or malformed reaction identifiers
- Module execution completes without errors and returns non-empty metabolite sets for known degradable compounds

## Limitations

- Predictions are database-derived and reflect only biotransformations documented in EAWAG; novel or understudied degradation pathways will not be predicted
- BioTransformer's environmental module is specific to microbial degradation; predictions do not apply to human or other mammalian metabolism
- EAWAG data is licensed under Creative Commons Attribution-NonCommercial-ShareAlike; commercial use requires explicit permission
- No changelog available for tracking EAWAG database version updates or rule set changes over time

## Evidence

- [intro] The environmental microbial degradation module relies on the EAWAG's Biodegradation and Biocatalysis Database, which is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license by EnviPath.: "The environmental microbial degradation module relies on the EAWAG's Biodegradation and Biocatalysis Database, which is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0"
- [other] 1. Load input compounds (SMILES or structure format) into BioTransformer 3.0 jar executable. 2. Execute the environmental microbial degradation module specifying the EAWAG Biodegradation and Biocatalysis Database rule set. 3. Collect predicted biotransformation products and associated reaction information from module output. 4. Parse and structure predicted metabolites with parent-product relationships and reaction types.: "Load input compounds (SMILES or structure format) into BioTransformer 3.0 jar executable. Execute the environmental microbial degradation module specifying the EAWAG Biodegradation and Biocatalysis"
- [intro] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database"
