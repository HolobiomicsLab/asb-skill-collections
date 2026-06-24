---
name: parent-product-relationship-mapping
description: Use when you have predicted biotransformation products from BioTransformer's
  environmental microbial degradation module (or similar rule-based prediction engines)
  and need to construct traceable lineages showing which parent compound(s) produced
  which metabolite(s) and what reaction type(s).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3407
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

# parent-product-relationship-mapping

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Map predicted biotransformation products to their parent compounds and classify the reaction types connecting them. This skill structures raw predicted metabolites from computational biotransformation modules into queryable parent-product networks with annotated reaction relationships.

## When to use

You have predicted biotransformation products from BioTransformer's environmental microbial degradation module (or similar rule-based prediction engines) and need to construct traceable lineages showing which parent compound(s) produced which metabolite(s) and what reaction type(s) mediated the transformation.

## When NOT to use

- Input is already a pre-constructed metabolite network or knowledge graph (skip to downstream analysis)
- Biotransformation products are from non-rule-based methods (e.g. machine learning models without explicit reaction classification) lacking reaction type annotations
- Output scope is limited to single-generation direct metabolites only (parent-product mapping adds overhead if downstream analysis does not require multi-generational tracing)

## Inputs

- Predicted biotransformation products (structures in SMILES or molfile format)
- Reaction metadata from BioTransformer module output (reaction type, enzyme/rule identifiers)
- Parent compound identifiers (SMILES or structure format)

## Outputs

- Parent-product relationship graph (nodes = compounds, edges = biotransformation reactions with type labels)
- Structured metabolite lineages (flat or hierarchical table/JSON with parent ID, product ID, reaction type)
- Annotated reaction metadata (reaction classification, enzymatic rule, predicted confidence if available)

## How to apply

After executing BioTransformer's environmental microbial degradation module on input compounds and collecting predicted biotransformation products and reaction information, parse the output to extract parent compound identifiers (SMILES or structure format), predicted product structures, and associated reaction type labels. Structure these three components into a relational mapping where each parent-product edge is annotated with its reaction classification. Validate that all parent identifiers match input compounds and all products have valid chemical representations. Store the mapping in a format that preserves hierarchical depth (first-generation vs. multi-generational metabolites) and reaction type diversity.

## Related tools

- **BioTransformer** (Rule-based biotransformation prediction engine that generates predicted products and reaction metadata for input compounds; executed as 3.0 jar executable with EAWAG module specified) — bitbucket.org/wishartlab/biotransformer3.0jar
- **EnviPath** (Licensor and curator of EAWAG's Biodegradation and Biocatalysis Database, which defines the biotransformation rules and reaction types used by BioTransformer's environmental microbial degradation module)

## Evaluation signals

- All parent compound identifiers in the mapping correspond to input compounds loaded into BioTransformer; no orphaned or synthetic parents
- All predicted products have valid chemical structures (valid SMILES, non-empty molfiles); structures are chemically distinct from parents
- Each parent-product edge is labeled with a reaction type from the EAWAG rule set; no edges lack reaction metadata
- Multi-generational lineages (if present) preserve parent-child relationships across generations without cycles
- Mapping schema is consistent (e.g., all edges use the same reaction type vocabulary; all identifiers use the same format)

## Limitations

- Reaction types are constrained to those present in the EAWAG's Biodegradation and Biocatalysis Database; biotransformations not covered by EAWAG rules will not be predicted
- Predicted products are computational predictions; experimental validation is required to confirm biological plausibility
- The mapping reflects only direct biotransformation pathways; secondary metabolism, abiotic degradation, or non-microbial transformations are out of scope
- Parent-product relationships depend entirely on BioTransformer's rule matching; ambiguous or novel chemical transformations may be missed or misclassified

## Evidence

- [intro] The environmental microbial degradation module relies on the EAWAG's Biodegradation and Biocatalysis Database: "The environmental microbial degradation module relies on the EAWAG's Biodegradation and Biocatalysis Database"
- [other] Collect predicted biotransformation products and associated reaction information from module output: "Collect predicted biotransformation products and associated reaction information from module output"
- [other] Parse and structure predicted metabolites with parent-product relationships and reaction types: "Parse and structure predicted metabolites with parent-product relationships and reaction types"
- [other] Load input compounds (SMILES or structure format) into BioTransformer 3.0 jar executable: "Load input compounds (SMILES or structure format) into BioTransformer 3.0 jar executable"
