---
name: community-constraint-propagation
description: Use when you have consensus metabolic reconstructions for multiple community members (e.g., from a plant microbiome or synthetic consortium) and need to gap-fill incomplete models while preserving community-level feasibility.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_3174
  tools:
  - COMMIT
derived_from:
- doi: 10.1371/journal.pcbi.1009906
  title: COMMIT
evidence_spans:
- community-dependent gap-filling using COMMIT for communites sampled from
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_commit_cq
    doi: 10.1371/journal.pcbi.1009906
    title: COMMIT
  dedup_kept_from: coll_commit_cq
schema_version: 0.2.0
---

# community-constraint-propagation

## Summary

Apply metabolic constraints derived from community-level dependencies to identify and resolve gaps in individual member reconstructions within a multi-organism system. This skill enables gap-filling that respects cross-member metabolic interactions rather than treating organisms in isolation.

## When to use

You have consensus metabolic reconstructions for multiple community members (e.g., from a plant microbiome or synthetic consortium) and need to gap-fill incomplete models while preserving community-level feasibility. Use this when individual member reconstructions contain metabolic gaps that cannot be resolved by single-organism logic alone, but can be inferred from interdependencies with other community members.

## When NOT to use

- Input reconstructions are already individually complete or were manually curated to high fidelity—community-constraint propagation adds minimal value if gaps are rare or well-characterized.
- The community is very loosely coupled or members are expected to be metabolically independent; single-organism gap-filling is more appropriate.
- You lack reliable consensus models for at least 2+ community members; the skill depends on meaningful cross-member dependencies to function.

## Inputs

- consensus metabolic reconstructions (SBML or JSON format) for community members
- community member metadata (taxonomy, growth requirements, or known metabolic capabilities)
- community-level constraints or phenotypic data (optional: growth rates, exchange fluxes, known metabolite dependencies)

## Outputs

- gap-filled metabolic reconstructions for each community member (SBML or JSON)
- community-level model with resolved cross-member dependencies
- validation report documenting gap-filling operations and consistency checks

## How to apply

Load consensus metabolic reconstructions (in SBML or JSON format) for all community members from an upstream consensus-building step. Apply COMMIT's community-dependent gap-filling algorithm, which identifies metabolic gaps in each member by leveraging cross-member dependencies and community-level constraints—e.g., by checking whether a missing reaction in one organism can be supplied by a neighbor or is required to maintain community-level biomass feasibility. Validate the gap-filled models for internal consistency (reaction balancing, mass balance, charge balance) and confirm that community-level constraints (e.g., biomass production feasibility for the consortium) are satisfied. Export the complete gap-filled community model in standard format (SBML or JSON).

## Related tools

- **COMMIT** (implements community-dependent gap-filling algorithm that identifies and fills metabolic gaps by leveraging community-level constraints and cross-member dependencies) — https://zenodo.org/badge/latestdoi/363932874

## Evaluation signals

- All reactions in gap-filled models pass stoichiometric balance checks (mass and charge balanced for each reaction).
- Community-level biomass production is feasible in the integrated model; no member is left without an essential metabolite that the community cannot provide.
- Gap-filled reactions correspond to known metabolic pathways or are supported by literature evidence for the organisms' taxonomy and known capabilities.
- Validation report confirms that gap-filled models satisfy the input community-level constraints (e.g., expected exchange metabolites, growth feasibility).
- Cross-member dependency justification is traceable—each gap-filled reaction should be annotated with the community member(s) or constraint(s) that justified its inclusion.

## Limitations

- Requires high-quality consensus metabolic reconstructions as input; garbage-in-garbage-out—poor consensus models will propagate and amplify gaps rather than resolve them.
- Community-constraint propagation assumes meaningful metabolic interdependencies exist; in loosely coupled or antagonistic communities, inferred gaps may be false positives.
- Validation of gap-filled models is indirect; the skill confirms internal consistency and community-level feasibility but does not experimentally verify whether inferred reactions actually occur in vivo.
- Performance and accuracy depend on the completeness and accuracy of the reference metabolic database and the fidelity of the consensus-building step.

## Evidence

- [intro] consensus-dependent-gap-filling: "community-dependent gap-filling using COMMIT for communites sampled from"
- [other] gap-filling-via-community-constraints: "Apply COMMIT's community-dependent gap-filling algorithm to identify and fill metabolic gaps in each member reconstruction by leveraging community-level constraints and cross-member dependencies."
- [other] validation-workflow: "Validate the gap-filled models for consistency (reaction balancing, biomass production feasibility) and export the complete gap-filled community model in standard format (SBML or JSON)."
- [other] input-format: "Load consensus metabolic reconstructions for the community members from the upstream consensus-building step."
