---
name: sbml-model-manipulation
description: Use when when you have consensus metabolic reconstructions in SBML format
  for individual community members and need to resolve metabolic gaps by leveraging
  cross-member dependencies and community-level constraints before phenotypic validation
  or flux analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - COMMIT
  license_tier: open
  provenance_tier: literature
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009906
  all_source_dois:
  - 10.1371/journal.pcbi.1009906
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sbml-model-manipulation

## Summary

Manipulate and validate consensus metabolic models in SBML format by applying community-dependent gap-filling algorithms to identify and resolve metabolic gaps while preserving reaction balancing and biomass production feasibility. This skill bridges upstream consensus reconstruction with downstream community-level constraint propagation.

## When to use

When you have consensus metabolic reconstructions in SBML format for individual community members and need to resolve metabolic gaps by leveraging cross-member dependencies and community-level constraints before phenotypic validation or flux analysis.

## When NOT to use

- Input reconstructions have not yet been validated for stoichiometric consistency or biomass production in isolation
- Community composition or member identities are not well-defined or validated
- You require organism-specific gap-filling rather than community-dependent constraints

## Inputs

- Consensus metabolic reconstructions (SBML format) for community members
- Community-level metabolic constraints or member interdependencies (implicit or explicit)

## Outputs

- Gap-filled community metabolic model (SBML or JSON format)
- Validation report documenting reaction balancing and biomass feasibility

## How to apply

Load the SBML-encoded consensus metabolic reconstructions for each community member from the upstream consensus-building step. Apply COMMIT's community-dependent gap-filling algorithm, which identifies metabolic gaps by analyzing member reconstructions in the context of community-level constraints and cross-member metabolic dependencies. Validate the gap-filled models by checking reaction balancing (stoichiometric consistency), confirming biomass production feasibility (non-zero flux through biomass pseudoreaction), and ensuring no orphan metabolites remain. Export the complete gap-filled community model in standard SBML or JSON format for downstream analysis.

## Related tools

- **COMMIT** (Performs community-dependent gap-filling on consensus metabolic reconstructions) — https://zenodo.org/badge/latestdoi/363932874

## Evaluation signals

- All reactions in the gap-filled model are stoichiometrically balanced (element counts conserved per reaction)
- Biomass pseudoreaction has non-zero flux under simulated growth conditions
- No orphan metabolites remain (all metabolites are consumed or produced by at least one reaction)
- Gap-filled model maintains compatibility with consensus reconstructions of individual members
- SBML schema validation passes; file parses without syntax errors

## Limitations

- Gap-filling relies on availability of high-quality consensus reconstructions and well-characterized community-level constraints; sparse or missing interdependencies may limit effectiveness
- Validation of biomass production feasibility is model-dependent and may not reflect in vivo growth behavior
- Method is demonstrated on Arabidopsis thaliana communities; applicability to other plant species or ecosystems not explicitly evaluated

## Evidence

- [other] Apply COMMIT's community-dependent gap-filling algorithm: "Apply COMMIT's community-dependent gap-filling algorithm to identify and fill metabolic gaps in each member reconstruction by leveraging community-level constraints and cross-member dependencies."
- [other] Validate for reaction balancing and biomass production: "Validate the gap-filled models for consistency (reaction balancing, biomass production feasibility) and export the complete gap-filled community model in standard format (SBML or JSON)."
- [intro] COMMIT for communities sampled from Arabidopsis thaliana: "community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana"
- [other] Load consensus metabolic reconstructions: "Load consensus metabolic reconstructions for the community members from the upstream consensus-building step."
