---
name: enzyme-family-classification-and-mapping
description: Use when you have biotransformation reaction data from a curated source like EAWAG's Biodegradation and Biocatalysis Database and need to map enzyme families, reaction types, and substrate specificities into machine-readable rule formats (SMARTS patterns, condition thresholds) for automated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  tools:
  - BioTransformer
  - EAWAG's Biodegradation and Biocatalysis Database (EnviPath)
derived_from:
- doi: 10.1186/s13321-019-0375-2
  title: BioTransformer 1.0
evidence_spans:
- This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that predicts small molecule metabolism
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
---

# enzyme-family-classification-and-mapping

## Summary

Extract and normalize enzyme family classifications and biotransformation rules from curated biodegradation databases (e.g., EAWAG BBD) into structured rule sets compatible with cheminformatics libraries. This skill enables substrate pattern matching and reaction template expansion for metabolite prediction across microbial degradation pathways.

## When to use

You have biotransformation reaction data from a curated source like EAWAG's Biodegradation and Biocatalysis Database and need to map enzyme families, reaction types, and substrate specificities into machine-readable rule formats (SMARTS patterns, condition thresholds) for automated small-molecule metabolism prediction. Use this when building or extending a metabolite prediction module that must apply rules to novel substrates via substructure matching.

## When NOT to use

- The input database lacks explicit enzyme family or reaction type annotations—rules cannot be reliably classified.
- Substrate patterns are already in a proprietary or tool-specific format incompatible with standard cheminformatics libraries.
- You only need to identify a single known metabolite; full rule set extraction and normalization is unnecessary overhead.

## Inputs

- Biotransformation reaction records from EAWAG or equivalent database (XML, CSV, or tabular format)
- Enzyme family and reaction type annotations
- Substrate chemical structures and product templates

## Outputs

- Structured biotransformation rule set (SMARTS patterns with condition metadata)
- Enzyme family–reaction type mapping index
- Validated rule compatibility report against reference metabolites

## How to apply

Retrieve biotransformation records from the reference database and extract metadata including reaction types, enzyme families, substrate patterns, and product templates. Parse and normalize these rules into a structured format: convert chemical patterns to SMARTS notation, encode enzyme family assignments, and specify applicability conditions (e.g., pH, oxygen requirement). Load the normalized rule set into the cheminformatics engine (e.g., BioTransformer's rule application module) and validate by comparing predicted metabolites and pathways against known reference biotransformations. The enzyme family classification guides rule prioritization and specificity thresholds during reaction template matching.

## Related tools

- **BioTransformer** (Rule application engine that executes normalized biotransformation rules via substructure matching and reaction template expansion to predict metabolite structures) — https://github.com/Wishartlab-openscience/Biotransformer
- **EAWAG's Biodegradation and Biocatalysis Database (EnviPath)** (Reference source of curated biotransformation rules, enzyme family classifications, and substrate–product mappings for soil and aquatic microbial degradation) — https://envipath.org/

## Examples

```
java -jar biotransformer-3.0.0.jar -k pred -b envimicro -ismi "CC(C)C1=CC=C(C)C=C1O" -osdf metabolites.sdf -s 2
```

## Evaluation signals

- Biotransformation rule set successfully loads into BioTransformer without parsing errors; all SMARTS patterns are valid and interpretable by the cheminformatics library.
- Predicted metabolites match reference structures and biotransformation pathways documented in EAWAG or peer-reviewed literature with ≥80% overlap in major products.
- Enzyme family classifications correctly filter applicable rules for test substrates (e.g., CYP450-dependent oxidations are not applied to anaerobic degradation pathways).
- Molecular properties of predicted metabolites (mass, logP, formula) fall within expected ranges relative to parent compounds and documented intermediates.
- Rule set supports multi-step prediction chains without rule conflicts; sequential application of rules produces chemically plausible metabolite trees.

## Limitations

- Environmental microbial degradation module predictions represent both aerobic and anaerobic biotransformations; users must manually filter for their specific environmental context (e.g., oxic vs. anoxic soil).
- Rule set is tied to the EAWAG database version and currency; rare or newly discovered enzyme families or reaction types may not be represented.
- Commercial use of rules derived from EAWAG data requires separate explicit license from EnviPath; non-commercial academic use is permitted under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.

## Evidence

- [other] Extract biotransformation rules and normalization: "Retrieve the EAWAG Biodegradation and Biocatalysis Database records and extract biotransformation rules (reaction types, enzyme families, substrate patterns, product templates)"
- [other] SMARTS and rule format specification: "Parse and normalize the biotransformation rules into a structured rule set (SMARTS patterns, condition thresholds, reaction metadata) compatible with cheminformatics libraries"
- [other] Rule application and metabolite prediction: "Implement the rule application engine in BioTransformer that applies the extracted biotransformation rules to input substrate molecules using substructure matching and reaction template expansion"
- [other] Validation against reference data: "Validate the predicted metabolite set by comparing output structures, biotransformation pathways, and molecular properties (mass, logP, etc.) against reference biotransformations documented in EAWAG"
- [readme] License and commercial restriction: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database, which is licensed by EnviPath under the Creative Commons"
- [readme] Enzyme family role in rule application: "The type of biotransformer - EC-based (ecbased), CYP450 (cyp450), Phase II (phaseII), Human gut microbial (hgut), human super transformer** (superbio, or allHuman), Environmental microbial"
