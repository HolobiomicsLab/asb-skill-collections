---
name: smarts-pattern-design-for-microbial-degradation
description: Use when you need to predict small molecule metabolism in soil or aquatic
  microbiota and must translate published biotransformation rules (reaction types,
  enzyme families, substrate patterns) from EAWAG or similar biodegradation databases
  into executable chemical pattern-matching rules compatible.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0370
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0621
  tools:
  - BioTransformer
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab). Env. module data CC-BY-NC-SA (enviPath/EAWAG).
    url: https://bitbucket.org/wishartlab/biotransformer.git
  license_tier: noncommercial
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-019-0375-2
  title: BioTransformer 1.0
evidence_spans:
- This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that
  predicts small molecule metabolism
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biotransformer_1_0_cq
    doi: 10.1186/s13321-019-0375-2
    title: BioTransformer 1.0
  dedup_kept_from: coll_biotransformer_1_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-019-0375-2
  all_source_dois:
  - 10.1186/s13321-019-0375-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMARTS pattern design for microbial degradation

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Design and normalize biotransformation rules from the EAWAG Biodegradation and Biocatalysis Database into structured SMARTS patterns and reaction templates for predicting soil and aquatic microbial metabolites. This skill enables systematic encoding of enzyme-catalyzed degradation reactions into computable chemical substructure patterns.

## When to use

Apply this skill when you need to predict small molecule metabolism in soil or aquatic microbiota and must translate published biotransformation rules (reaction types, enzyme families, substrate patterns) from EAWAG or similar biodegradation databases into executable chemical pattern-matching rules compatible with cheminformatics libraries.

## When NOT to use

- Input is mammalian or human Phase I/II metabolism (use cyp450 or phaseII biotransformer options instead).
- Biotransformation rules are already encoded in SMARTS format and loaded in BioTransformer (skip to rule application step).
- Prediction task requires commercial use of EAWAG BBD data without explicit EnviPath commercial license.

## Inputs

- EAWAG Biodegradation and Biocatalysis Database records (biotransformation rules with reaction type, enzyme family, substrate pattern, product template)
- Small molecule substrate (SMILES or MOL format)
- Biotransformation rule set documentation (reaction metadata, condition thresholds)

## Outputs

- Structured SMARTS pattern library (reaction templates with condition metadata)
- Normalized biotransformation rule set (enzyme classification, substrate patterns, product templates)
- Predicted metabolite structures (intermediate and final products from applied rules)
- Biotransformation pathway documentation (reaction sequence, enzyme assignments)

## How to apply

Extract biotransformation records from EAWAG BBD that document microbial degradation pathways, including reaction type, enzyme family, substrate specificity, and product structure. Convert each rule into a SMARTS pattern representing the reactive substructure and transformation logic, incorporating condition thresholds (e.g., pH, oxygen availability for aerobic/anaerobic pathways). Normalize the rules into a structured rule set with metadata tags (enzyme EC number, reaction classification, organism scope) to enable systematic lookup and prioritization. Validate each SMARTS pattern by confirming it matches known substrates from EAWAG and generates correct product templates. Store the compiled rule set in a format compatible with BioTransformer's rule application engine, which will apply substructure matching to predict metabolites.

## Related tools

- **BioTransformer** (Rule application engine that executes the compiled SMARTS biotransformation rules against input substrates using substructure matching and reaction template expansion to predict metabolites) — https://github.com/Wishartlab-openscience/Biotransformer

## Examples

```
java -jar biotransformer-3.0.0.jar -k pred -b envimicro -ismi "CC(C)C1=CC=C(C)C=C1O" -osdf thymol_microbial_metabolites.sdf -s 2
```

## Evaluation signals

- SMARTS patterns correctly match known EAWAG substrate examples and generate expected product structures without false positives.
- Normalized rule set contains all required metadata fields (enzyme family, reaction type, condition thresholds, organism scope) and is parseable by BioTransformer.
- Predicted metabolite structures from applied rules match reference biotransformations documented in EAWAG BBD literature with correct molecular mass, formula, and logP properties.
- Biotransformation pathway traces are chemically plausible and show correct enzyme classification and intermediate products at each step.
- Rule coverage includes both aerobic and anaerobic reactions applicable to soil and aquatic microbiota, as per EAWAG BBD scope.

## Limitations

- SMARTS pattern design requires expert curation; automated conversion from EAWAG records may miss context-specific reaction conditions (pH, electron acceptor).
- EAWAG BBD data is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0; commercial use requires explicit EnviPath commercial license.
- SMARTS pattern expressiveness is limited for complex multi-step or cofactor-dependent reactions; rules may need manual refinement for edge cases.
- Prediction accuracy depends on completeness of EAWAG BBD coverage; degradation pathways not in the database will not be predicted.

## Evidence

- [other] Retrieve the EAWAG Biodegradation and Biocatalysis Database records and extract biotransformation rules (reaction types, enzyme families, substrate patterns, product templates) applicable to soil and aquatic microbial degradation pathways.: "Retrieve the EAWAG Biodegradation and Biocatalysis Database records and extract biotransformation rules (reaction types, enzyme families, substrate patterns, product templates) applicable to soil and"
- [other] Parse and normalize the biotransformation rules into a structured rule set (SMARTS patterns, condition thresholds, reaction metadata) compatible with cheminformatics libraries.: "Parse and normalize the biotransformation rules into a structured rule set (SMARTS patterns, condition thresholds, reaction metadata) compatible with cheminformatics libraries."
- [readme] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database, which is licensed by EnviPath under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database, which is licensed by EnviPath under the Creative Commons"
- [other] Implement the rule application engine in BioTransformer that applies the extracted biotransformation rules to input substrate molecules using substructure matching and reaction template expansion.: "Implement the rule application engine in BioTransformer that applies the extracted biotransformation rules to input substrate molecules using substructure matching and reaction template expansion."
- [readme] For the environmental microbial biodegradation, all reactions (aerobic and anaerobic) are reported, and not only the aerobic biotransformations (as per default in the EAWAG BBD/PPS system).: "For the environmental microbial biodegradation, all reactions (aerobic and anaerobic) are reported, and not only the aerobic biotransformations (as per default in the EAWAG BBD/PPS system)."
