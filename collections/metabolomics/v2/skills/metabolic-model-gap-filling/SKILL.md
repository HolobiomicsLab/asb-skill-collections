---
name: metabolic-model-gap-filling
description: Use when you have consensus metabolic reconstructions in SBML or JSON format for community members and need to resolve incomplete reactions, missing cofactor availability, or blocked pathways that prevent feasibility of biomass production.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0621
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

# metabolic-model-gap-filling

## Summary

Gap-filling identifies and resolves metabolic dead-ends in genome-scale reconstructions by leveraging community-level constraints and cross-member dependencies. This skill is essential when individual member models contain metabolic gaps that prevent biomass production or violate stoichiometric balance—conditions common in consensus models derived from annotation pipelines.

## When to use

Apply this skill when you have consensus metabolic reconstructions in SBML or JSON format for community members and need to resolve incomplete reactions, missing cofactor availability, or blocked pathways that prevent feasibility of biomass production. Community-dependent gap-filling is particularly valuable when single-member gap-filling fails because metabolic capacity is distributed across community members.

## When NOT to use

- Input reconstructions already contain complete pathways for all essential nutrients and cofactors (no gaps to fill).
- Metabolic gaps are due to sequencing errors or annotation artifacts rather than genuine missing reactions in the reference genome.
- Analysis goal is purely comparative genomics rather than quantitative flux prediction.

## Inputs

- consensus metabolic reconstructions (SBML or JSON format) for individual community members
- community metadata defining member relationships and exchange metabolites

## Outputs

- gap-filled metabolic models for each community member (SBML or JSON)
- complete gap-filled community model (SBML or JSON)
- validation report on reaction balancing and biomass production feasibility

## How to apply

Load consensus metabolic reconstructions for all community members into COMMIT. Apply the community-dependent gap-filling algorithm, which identifies metabolic gaps in each member by checking reaction balancing and biomass production feasibility while leveraging community-level constraints and cross-member metabolic dependencies. The algorithm fills gaps by exploiting metabolic exchange and synthesis capacities present in other community members. After gap-filling, validate all reactions for stoichiometric balance and re-test biomass production feasibility. Export the complete gap-filled community model in standard format (SBML or JSON) for downstream flux balance analysis or dynamic simulations.

## Related tools

- **COMMIT** (implements community-dependent gap-filling algorithm; processes consensus reconstructions and fills metabolic gaps using community-level constraints) — https://zenodo.org/badge/latestdoi/363932874

## Evaluation signals

- All reactions in gap-filled models are stoichiometrically balanced (mass and charge conservation across all metabolites).
- Biomass production is feasible in all gap-filled member models under defined community exchange conditions.
- No orphan metabolites remain (all consumed metabolites are produced either internally or supplied via community exchange).
- Gap-filled reactions are traceable to community members' metabolic capacities; no reactions added ex nihilo.
- Export validates against SBML schema (if SBML format) or JSON schema (if JSON format) with no constraint violations.

## Limitations

- Gap-filling accuracy depends on completeness of reference genome annotations and quality of community member definitions.
- Algorithm may fail if metabolic gaps cannot be resolved through cross-member exchange due to distributed essential biosynthetic capacities.
- Community-dependent gap-filling assumes defined community membership; results are specific to the sampled community and may not generalize to different ecological contexts or growth conditions.

## Evidence

- [other] COMMIT implements community-dependent gap-filling for communities sampled from Arabidopsis thaliana by processing consensus metabolic reconstructions.: "COMMIT implements community-dependent gap-filling for communities sampled from Arabidopsis thaliana by processing consensus metabolic reconstructions."
- [other] Workflow: Load consensus metabolic reconstructions, apply COMMIT's community-dependent gap-filling algorithm to identify and fill metabolic gaps by leveraging community-level constraints and cross-member dependencies, then validate gap-filled models for consistency (reaction balancing, biomass production feasibility) and export in standard format.: "Apply COMMIT's community-dependent gap-filling algorithm to identify and fill metabolic gaps in each member reconstruction by leveraging community-level constraints and cross-member dependencies."
- [other] Output validation includes reaction balancing and biomass production feasibility checks.: "Validate the gap-filled models for consistency (reaction balancing, biomass production feasibility) and export the complete gap-filled community model"
- [other] Gap-filling output format is SBML or JSON.: "export the complete gap-filled community model in standard format (SBML or JSON)."
