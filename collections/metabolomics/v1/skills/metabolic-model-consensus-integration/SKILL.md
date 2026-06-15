---
name: metabolic-model-consensus-integration
description: Use when you have draft metabolic reconstructions in SBML or standard format for multiple organisms in a microbial community (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3837
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_3174
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_commit
    doi: 10.1371/journal.pcbi.1009906
    title: COMMIT
  dedup_kept_from: coll_commit
schema_version: 0.2.0
---

# metabolic-model-consensus-integration

## Summary

Integrates multiple draft metabolic reconstructions from community member organisms into a single consensus model by identifying conserved metabolic reactions across all input reconstructions. This skill is essential when studying microbial communities where individual organism models exist but must be unified for community-level metabolic analysis.

## When to use

Apply this skill when you have draft metabolic reconstructions in SBML or standard format for multiple organisms in a microbial community (e.g., sampled from plant microbiomes like Arabidopsis thaliana) and need to generate a unified consensus model that represents the metabolic core conserved across all community members.

## When NOT to use

- Input reconstructions are not in standard format (SBML, JSON-based model formats) or are incomplete draft models lacking sufficient coverage
- Single-organism metabolic modeling where consensus across multiple reconstructions is not required
- Community samples where organism membership and draft models are unavailable or highly incomplete

## Inputs

- Draft metabolic reconstructions in SBML format for multiple community organisms
- List of organism identifiers and model file paths

## Outputs

- Consensus metabolic reconstruction for each organism (SBML format)
- Set of conserved metabolic reactions across all input models
- Community-dependent gap-filled metabolic models

## How to apply

Load all draft metabolic reconstructions for community member organisms in standard format (SBML). Execute the COMMIT consensus generation algorithm to integrate the draft models and identify conserved metabolic reactions agreed upon by the consensus criteria across all input reconstructions. The algorithm outputs a consensus metabolic reconstruction for each organism, containing only reactions and metabolites that satisfy the consensus threshold. Validate that the consensus models are logically consistent and retain metabolic functionality relevant to the community context.

## Related tools

- **COMMIT** (Generates consensus metabolic reconstructions and performs community-dependent gap-filling by integrating multiple draft models and identifying conserved reactions) — 10.5281/zenodo.363932874

## Evaluation signals

- Consensus models contain only reactions and metabolites present in all (or majority of) input reconstructions, verified by intersection analysis
- Output models remain in valid SBML format and pass schema validation
- Consensus reconstructions retain core metabolic functions (central carbon metabolism, biosynthesis pathways) expected in the organism and community context
- Gap-filled reactions are documented and traceable to community-dependent inference rules applied by COMMIT
- Comparison of input vs. output model sizes and reaction counts shows expected reduction due to consensus filtering

## Limitations

- Consensus approach may be overly restrictive if input draft reconstructions have high heterogeneity or quality variation; reactions present in only some (not all) organisms are discarded
- Requires high-quality, well-curated draft metabolic models as input; GIGO (garbage in, garbage out) principle applies
- Community-dependent gap-filling relies on accurate organism co-occurrence and functional interdependencies; misspecified community membership will degrade consensus quality
- No explicit versioning or changelog documented in the article; reproducibility across COMMIT versions may require careful dependency specification

## Evidence

- [other] COMMIT generates consensus metabolic reconstructions and performs community-dependent gap-filling for microbial communities sampled from Arabidopsis thaliana.: "COMMIT generates consensus metabolic reconstructions and performs community-dependent gap-filling for microbial communities sampled from Arabidopsis thaliana."
- [other] Execute COMMIT consensus generation algorithm to integrate draft models and identify conserved metabolic reactions across all input reconstructions for each organism.: "Execute COMMIT consensus generation algorithm to integrate draft models and identify conserved metabolic reactions across all input reconstructions for each organism."
- [other] Output the consensus metabolic reconstruction for each organism, containing only reactions and metabolites agreed upon by the consensus criteria.: "Output the consensus metabolic reconstruction for each organism, containing only reactions and metabolites agreed upon by the consensus criteria."
- [other] Load draft metabolic reconstructions for all community member organisms in standard format (e.g., SBML).: "Load draft metabolic reconstructions for all community member organisms in standard format (e.g., SBML)."
- [intro] Generation of consensus metabolic reconstructions and community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana: "Generation of consensus metabolic reconstructions and community-dependent gap-filling using COMMIT for communites sampled from _Arabidopsis thaliana_"
