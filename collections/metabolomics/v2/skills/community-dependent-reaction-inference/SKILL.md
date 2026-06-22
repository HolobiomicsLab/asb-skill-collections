---
name: community-dependent-reaction-inference
description: Use when you have consensus metabolic reconstructions for multiple community members (e.g., plant-associated microbes or plant-microbial consortia) and those individual models contain incomplete or disconnected metabolic pathways.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3697
  tools:
  - COMMIT
derived_from:
- doi: 10.1371/journal.pcbi.1009906
  title: COMMIT
- doi: 10.5281/zenodo.363932874
  title: ''
evidence_spans:
- community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_commit
    doi: 10.1371/journal.pcbi.1009906
    title: COMMIT
  dedup_kept_from: coll_commit
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009906
  all_source_dois:
  - 10.1371/journal.pcbi.1009906
  - 10.5281/zenodo.363932874
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# community-dependent-reaction-inference

## Summary

Infer and fill metabolic gaps in individual organism models by leveraging shared metabolic context and dependencies across community members. This skill applies constraint-based reasoning to propose reactions that bridge gaps in consensus reconstructions using multi-organism metabolic overlap.

## When to use

Apply this skill when you have consensus metabolic reconstructions for multiple community members (e.g., plant-associated microbes or plant-microbial consortia) and those individual models contain incomplete or disconnected metabolic pathways. Use it specifically when metabolic gaps cannot be filled from single-organism databases alone, but the community context reveals shared substrates, products, or exchange requirements that suggest plausible gap-filling reactions.

## When NOT to use

- Input reconstructions already fully gap-filled or curated from complete enzymatic databases
- Single-organism models with no community context available; use organism-specific gap-filling instead
- Metabolic gaps that conflict with established biochemistry of the host organism or are inconsistent with known inter-member exchanges

## Inputs

- consensus metabolic reconstructions for community members (SBML or similar format)
- set of identified metabolic gaps per community member
- metabolic context specification (shared substrates, exchange requirements, host organism metabolic knowledge)

## Outputs

- gap-filled metabolic models for each community member with reaction annotations
- gap-filling report indicating source (community-context vs. external database) and confidence for each filled reaction

## How to apply

Load consensus metabolic reconstructions for all community members generated from prior annotation steps. Initialize the COMMIT gap-filling module with community context, specifying the set of metabolic gaps to address across the member set. Execute the community-dependent gap-filling algorithm, which leverages metabolic overlap and inter-member exchange dependencies to propose reactions that fill identified gaps. Validate proposed reactions by checking consistency with known metabolism of the host organism (e.g., Arabidopsis thaliana) and ensuring they preserve inter-member exchange requirements. Output gap-filled models with annotations indicating the source (community-derived vs. database-derived) and confidence of each filled reaction.

## Related tools

- **COMMIT** (Implements community-dependent gap-filling module that operates on consensus reconstructions and uses metabolic overlap to infer missing reactions across community members) — 10.5281/zenodo.363932874

## Evaluation signals

- Gap-filled reactions are annotated with community context as source and include confidence scores
- Filled reactions preserve metabolic connectivity—no orphan metabolites remain unbalanced in downstream analysis
- Proposed reactions are biochemically valid and consistent with curated plant (Arabidopsis thaliana) metabolism where applicable
- Inter-member exchange requirements remain satisfiable in the filled models (no blocked cross-feeding dependencies)
- Sensitivity check: removing a subset of community members and re-running gap-filling produces different (smaller) sets of filled reactions

## Limitations

- Gap-filling accuracy depends on the completeness and accuracy of the input consensus reconstructions; poor initial annotations propagate errors
- Community-dependent inference requires sufficient metabolic overlap; sparse or highly specialized communities may provide weak contextual signals
- Method cannot distinguish between multiple plausible gap-filling solutions; confidence rankings are heuristic and should be validated experimentally
- Host organism metabolic knowledge (e.g., Arabidopsis thaliana reference) must be available and reliable to validate inferred reactions

## Evidence

- [other] COMMIT implements community-dependent gap-filling as a module that operates on consensus metabolic reconstructions generated for community members, leveraging shared metabolic context across the community to identify and fill metabolic gaps.: "COMMIT implements community-dependent gap-filling as a module that operates on consensus metabolic reconstructions generated for community members, leveraging shared metabolic context across the"
- [other] Execute community-dependent gap-filling algorithm that leverages metabolic overlap and dependencies between community members to propose reactions filling identified gaps.: "Execute community-dependent gap-filling algorithm that leverages metabolic overlap and dependencies between community members to propose reactions filling identified gaps."
- [other] Validate filled gaps by checking consistency with known plant (Arabidopsis thaliana) metabolism and inter-member exchange requirements.: "Validate filled gaps by checking consistency with known plant (Arabidopsis thaliana) metabolism and inter-member exchange requirements."
- [other] Output gap-filled metabolic models for each community member with annotations indicating source and confidence of filled reactions.: "Output gap-filled metabolic models for each community member with annotations indicating source and confidence of filled reactions."
