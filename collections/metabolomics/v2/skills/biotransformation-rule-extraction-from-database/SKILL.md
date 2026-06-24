---
name: biotransformation-rule-extraction-from-database
description: Use when you need to populate or reconstruct a biotransformation prediction
  module and have access to a curated biotransformation database (such as EAWAG BBD)
  that documents empirically validated microbial degradation pathways, enzyme-substrate
  relationships, and reaction outcomes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_2258
  tools:
  - BioTransformer
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab). Env. module data CC-BY-NC-SA (enviPath/EAWAG).
    url: https://bitbucket.org/wishartlab/biotransformer.git
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

# biotransformation-rule-extraction-from-database

## Summary

Extract and normalize biotransformation rules from curated databases (e.g., EAWAG's Biodegradation and Biocatalysis Database) into structured, machine-actionable rule sets for predicting small molecule metabolism in environmental microbiota. This skill enables systematic capture of reaction types, enzyme families, substrate patterns, and product templates to populate rule-based metabolism prediction engines.

## When to use

Use this skill when you need to populate or reconstruct a biotransformation prediction module and have access to a curated biotransformation database (such as EAWAG BBD) that documents empirically validated microbial degradation pathways, enzyme-substrate relationships, and reaction outcomes. Apply it when your goal is to operationalize published biodegradation knowledge into a predictive computational tool rather than inferring rules de novo from literature or sequence data.

## When NOT to use

- Input database is not curated or empirically validated (e.g., purely literature-mined, uncrossed claims); rule extraction from low-quality sources will propagate noise into predictions.
- Goal is rapid ad-hoc metabolite prediction for a single compound; use pre-packaged biotransformer tools (e.g., BioTransformer executable) instead of extracting rules de novo.
- Biotransformation scope differs from your target organism or environment (e.g., rules for mammalian Phase I metabolism will not accurately predict soil microbial pathways); verify database scope and organism/environment tags before extraction.

## Inputs

- Biotransformation database records (EAWAG Biodegradation and Biocatalysis Database or equivalent; typically XML, JSON, or relational format)
- Enzyme classification (EC) metadata linked to microbial degradation reactions
- Substrate structures and product structures (as SMILES, SMARTS, or MOL records)
- Reaction condition annotations (aerobic/anaerobic, pH, temperature, cofactor requirements)

## Outputs

- Structured biotransformation rule set (SMARTS patterns, reaction templates, and metadata)
- Normalized rule objects compatible with cheminformatics rule engines (e.g., BioTransformer's internal rule format)
- Rule validation report comparing predicted vs. reference metabolites with property concordance metrics

## How to apply

Begin by retrieving records from the target biotransformation database (e.g., EAWAG Biodegradation and Biocatalysis Database) and systematically extract biotransformation rules that capture reaction types (oxidation, reduction, conjugation, deconjugation), enzyme families (EC classifications), substrate patterns (substructural motifs), and product templates (expected outputs). Normalize these heterogeneous rule descriptions into a structured format compatible with cheminformatics libraries—primarily SMARTS patterns for substructure matching, reaction condition thresholds (pH ranges, oxygen requirements, cofactor dependencies), and machine-readable reaction metadata (bidirectionality, reversibility flags, organism/environment contexts). Validate the normalized rules by comparing predicted metabolites against reference biotransformations documented in the same database or peer-reviewed literature, checking consistency of product structures, molecular properties (mass, logP, formal charge), and pathway topology. Configure rule application precedence and specificity thresholds to minimize false-positive metabolite predictions while maintaining sensitivity to rare or context-dependent biotransformations.

## Related tools

- **BioTransformer** (Executes extracted and normalized biotransformation rules against input substrate molecules to generate predicted metabolite structures and pathways; integrates rule sets from EAWAG BBD for environmental microbial degradation prediction.) — https://github.com/Wishartlab-openscience/Biotransformer

## Examples

```
java -jar biotransformer-3.0.0.jar -k pred -b envimicro -ismi "CCNC1=NC(=NC(=N1)Cl)NC(C)C" -osdf ~/atrazine-metabolites.sdf -s 2
```

## Evaluation signals

- Rule coverage: All documented biotransformations in the source database for a given enzyme family or reaction type should be represented in the extracted rule set; audit by sampling 10–20 reference reactions and verifying their rule proxies are present.
- Substructure matching fidelity: Test extracted SMARTS patterns against known substrates from the database; false-positive (pattern matches non-substrates) and false-negative (pattern fails to match true substrates) rates should each be <5%.
- Metabolite structure validity: Predicted metabolites generated by applying rules should conform to chemical graph validity (valence, connectivity, stereochemistry preservation); compare output structures using cheminformatics libraries (RDKit canonical SMILES matching).
- Property concordance: Predicted metabolite mass, molecular formula, and logP should match reference products documented in the database within measurement tolerance (mass ±0.01 Da, logP ±0.5 units).
- Pathway topology consistency: Multi-step biotransformation sequences predicted by chained rule application should not create chemically unrealistic intermediates (e.g., radical fragments, hypervalent atoms, disconnected products).

## Limitations

- Rules extracted from EAWAG BBD represent empirically observed biodegradation pathways and may not exhaustively capture all thermodynamically feasible transformations; rare or environment-specific pathways may be underrepresented.
- Rule extraction assumes the source database provides sufficient metadata (substrate patterns, product structures, reaction conditions); incomplete or ambiguously documented reactions may yield low-quality rules.
- Environmental microbial degradation rules are organism-centric and context-dependent (aerobic vs. anaerobic, soil vs. aquatic); extracted rules may fail to predict accurate pathways when applied to environmental contexts not covered by the source database.
- EAWAG BBD data is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0); commercial use of extracted rules requires explicit license negotiation with EnviPath, which may restrict deployment of biotransformer tools in proprietary settings.

## Evidence

- [other] Retrieve the EAWAG Biodegradation and Biocatalysis Database records and extract biotransformation rules (reaction types, enzyme families, substrate patterns, product templates) applicable to soil and aquatic microbial degradation pathways.: "Retrieve the EAWAG Biodegradation and Biocatalysis Database records and extract biotransformation rules (reaction types, enzyme families, substrate patterns, product templates)"
- [other] Parse and normalize the biotransformation rules into a structured rule set (SMARTS patterns, condition thresholds, reaction metadata) compatible with cheminformatics libraries.: "Parse and normalize the biotransformation rules into a structured rule set (SMARTS patterns, condition thresholds, reaction metadata) compatible with cheminformatics libraries"
- [other] Validate the predicted metabolite set by comparing output structures, biotransformation pathways, and molecular properties (mass, logP, etc.) against reference biotransformations documented in EAWAG or literature.: "Validate the predicted metabolite set by comparing output structures, biotransformation pathways, and molecular properties (mass, logP, etc.) against reference biotransformations"
- [readme] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database, which is licensed by EnviPath under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International. Therefore users of the environmental microbial degradation module must cite the EnviPath paper below. To use the environmental microbial module for commercial purposes, users must request an appropriate commercial license from EnviPath.: "environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database, which is licensed by EnviPath under the Creative Commons"
- [readme] For the environmental microbial biodegradation, all reactions (aerobic and anaerobic) are reported, and not only the aerobic biotransformations (as per default in the EAWAG BBD/PPS system).: "For the environmental microbial biodegradation, all reactions (aerobic and anaerobic) are reported"
