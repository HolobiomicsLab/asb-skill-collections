---
name: environmental-degradation-pathway-analysis
description: Use when you have a target compound (in SMILES or structure format) and need to predict what metabolites will form via environmental microbial biotransformation, including the reaction types and parent–product relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_2814
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/nar/gkac408
  all_source_dois:
  - 10.1093/nar/gkac408
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# environmental-degradation-pathway-analysis

## Summary

Predict biotransformation products and degradation pathways for chemical compounds under environmental microbial conditions using BioTransformer's EAWAG-BBD-derived module. This skill reconstructs the sequence and types of reactions likely to occur when a pollutant or xenobiotic encounters soil, aquatic, or engineered microbial communities.

## When to use

Apply this skill when you have a target compound (in SMILES or structure format) and need to predict what metabolites will form via environmental microbial biotransformation, including the reaction types and parent–product relationships. Use it during environmental risk assessment, persistence prediction, or when designing remediation strategies and need to anticipate daughter products that may be toxic or persistent.

## When NOT to use

- Input compound is already a known metabolite and you need human metabolism (phase I/II) instead of environmental microbial pathways — use a mammalian metabolism module instead.
- Prediction must account for non-biological abiotic degradation (photolysis, hydrolysis) — this module predicts only microbial biotransformation.
- Rule base or licensing constraints forbid non-commercial use (Creative Commons BY-NC-SA license) — check your use-case permits non-commercial application.

## Inputs

- Chemical compound in SMILES notation
- Chemical compound in structure format (MOL, SDF, or compatible molecular descriptor)
- Single compound or batch of compounds for biotransformation prediction

## Outputs

- Predicted biotransformation products (metabolites) with SMILES or structure representations
- Parent–product relationship graph or table
- Reaction type annotations (e.g., oxidation, hydrolysis, conjugation) for each transformation step
- Biotransformation pathway tree or network

## How to apply

Load the input compound in SMILES or structure format into BioTransformer 3.0's jar executable. Execute the environmental microbial degradation module by specifying the EAWAG Biodegradation and Biocatalysis Database rule set as the prediction rule base. The module will apply curated biotransformation rules from the EAWAG-BBD to generate predicted metabolites. Parse and structure the module's output to extract predicted metabolites, parent–product relationships, and reaction type annotations. Validate that the rule set is EAWAG-BBD-derived (licensed CC-BY-NC-SA 4.0 by EnviPath) to ensure predictions are grounded in peer-reviewed biodegradation literature.

## Related tools

- **BioTransformer** (Executes the environmental microbial degradation module to predict biotransformation products using EAWAG-BBD-derived rule sets) — bitbucket.org/wishartlab/biotransformer3.0jar
- **EnviPath** (Curates and maintains the EAWAG Biodegradation and Biocatalysis Database; licensor of the rule set used by BioTransformer's environmental module)

## Examples

```
java -jar biotransformer3.0.jar -ismi input.smi -ibiomet eawag -omet json -o output_metabolites.json
```

## Evaluation signals

- All predicted metabolites have valid chemical structures (SMILES or MOL parseable without error)
- Parent–product relationships form a directed acyclic graph (DAG) with the input compound as root and no cycles
- Each transformation step has a reaction type label matching known microbial biotransformation classes (oxidation, hydrolysis, methylation, etc.)
- Predicted pathways are traceable to biotransformation rules in the EAWAG-BBD (can be verified against EAWAG-BBD documentation or EnviPath database)
- Reproducibility: identical compound input yields identical metabolite and pathway predictions across multiple runs

## Limitations

- Predictions depend on coverage and completeness of the EAWAG-BBD; novel or rare biotransformation reactions not in the database will not be predicted.
- Module assumes generic environmental microbial communities and cannot model organism-specific or site-specific microbial ecology; predictions may not reflect actual degradation rates or pathways in a particular environmental compartment.
- License (Creative Commons BY-NC-SA 4.0) restricts use to non-commercial applications; commercial environmental consulting or drug metabolism studies may require alternative tools or licensing.
- No changelog is available, making it difficult to track when rule sets are updated or to compare predictions between BioTransformer versions.

## Evidence

- [intro] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database: "The environmental microbial degradation module relies on the EAWAG's Biodegradation and Biocatalysis Database, which is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0"
- [other] Workflow steps for applying the skill: "1. Load input compounds (SMILES or structure format) into BioTransformer 3.0 jar executable. 2. Execute the environmental microbial degradation module specifying the EAWAG Biodegradation and"
