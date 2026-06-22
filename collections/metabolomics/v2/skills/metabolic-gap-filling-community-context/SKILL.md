---
name: metabolic-gap-filling-community-context
description: Use when you have consensus metabolic reconstructions for all members of a microbial or plant community (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0621
  tools:
  - COMMIT
derived_from:
- doi: 10.1371/journal.pcbi.1009906
  title: COMMIT
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolic-gap-filling-community-context

## Summary

Community-dependent gap-filling leverages shared metabolic context across multiple microbial or plant community members to identify and fill metabolic gaps in individual consensus reconstructions. This skill is essential when working with multi-member community models where interdependencies and metabolic overlap can resolve gaps that cannot be addressed by single-organism reconstruction alone.

## When to use

Apply this skill when you have consensus metabolic reconstructions for all members of a microbial or plant community (e.g., Arabidopsis thaliana-associated microbiota) and need to resolve metabolic gaps by exploiting cross-member metabolic context, inter-member exchange requirements, and shared pathway dependencies rather than filling gaps in isolation.

## When NOT to use

- When you have only a single organism's metabolic reconstruction (no community context available)
- When metabolic gaps are due to incomplete annotation of a single organism's known biochemistry and can be resolved by organism-specific literature or database curation
- When input reconstructions are already genome-annotated and gap-filling should prioritize sequence homology or genomic evidence over community inference

## Inputs

- Consensus metabolic reconstructions for all community members (e.g., SBML or JSON format)
- Specification of metabolic gaps to be addressed
- Community context metadata (membership, growth conditions, host organism)

## Outputs

- Gap-filled metabolic models for each community member
- Reaction-level annotations indicating source (community context, inter-member transfer) and confidence
- Exchange reaction specifications between community members

## How to apply

Load consensus metabolic reconstructions for all community members into the COMMIT gap-filling module, specifying the metabolic context and gaps to be addressed across the member set. Execute the community-dependent gap-filling algorithm, which analyzes metabolic overlap and dependencies between community members to propose reactions that fill identified gaps. Validate filled reactions against known organism-specific metabolism (e.g., plant primary metabolism for Arabidopsis) and verify consistency with inter-member exchange requirements. Annotate the final gap-filled models to indicate the source of each filled reaction and confidence level, enabling downstream curation and validation.

## Related tools

- **COMMIT** (Implements community-dependent gap-filling module that operates on consensus reconstructions, leveraging shared metabolic context across community members to identify and fill metabolic gaps) — https://zenodo.org/record/363932874

## Evaluation signals

- Filled gaps are annotated with source (community member, metabolic overlap type) and confidence metadata
- Gap-filled models maintain consistency with known organism-specific metabolism (e.g., primary/secondary metabolism pathways for plant hosts)
- Exchange reactions between community members are chemically and metabolically feasible (e.g., known cross-feeding or co-metabolite dependencies)
- Filled reactions do not create implausible metabolic shortcuts or violate stoichiometric constraints across the community
- Comparison of single-organism vs. community-context gap-filling shows that community-dependent fills resolve gaps unresolvable in isolation

## Limitations

- Community-dependent gap-filling assumes reliable consensus reconstructions for all members; errors in upstream reconstructions propagate and can lead to incorrect gap-filling proposals
- Validation is constrained by incomplete knowledge of inter-member metabolic exchange, especially for uncultured or undercharacterized community members
- The method requires all community members to be represented; absence of key community members may leave gaps unresolved or lead to biased fill proposals
- Confidence in filled reactions depends on the degree of metabolic overlap and known interdependencies in the community; highly specialized or host-specific metabolisms may not be reliably filled from community context alone

## Evidence

- [other] COMMIT implements community-dependent gap-filling as a module that operates on consensus metabolic reconstructions generated for community members, leveraging shared metabolic context across the community to identify and fill metabolic gaps.: "COMMIT implements community-dependent gap-filling as a module that operates on consensus metabolic reconstructions generated for community members, leveraging shared metabolic context across the"
- [other] Execute community-dependent gap-filling algorithm that leverages metabolic overlap and dependencies between community members to propose reactions filling identified gaps.: "Execute community-dependent gap-filling algorithm that leverages metabolic overlap and dependencies between community members to propose reactions filling identified gaps."
- [other] Validate filled gaps by checking consistency with known plant (Arabidopsis thaliana) metabolism and inter-member exchange requirements.: "Validate filled gaps by checking consistency with known plant (Arabidopsis thaliana) metabolism and inter-member exchange requirements."
- [other] Output gap-filled metabolic models for each community member with annotations indicating source and confidence of filled reactions.: "Output gap-filled metabolic models for each community member with annotations indicating source and confidence of filled reactions."
- [intro] community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana: "community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana"
