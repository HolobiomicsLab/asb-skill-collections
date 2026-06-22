---
name: community-metabolic-reconstruction-synthesis
description: Use when you have draft metabolic reconstructions (in SBML or equivalent format) for multiple organisms sampled from a single ecological community (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_2259
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
---

# community-metabolic-reconstruction-synthesis

## Summary

Synthesize a single consensus metabolic model from multiple draft genome-scale reconstructions of organisms in a microbial community by identifying and retaining only reactions and metabolites conserved across all input models. This approach enables faithful representation of community metabolism while reducing redundancy and improving model interpretability.

## When to use

You have draft metabolic reconstructions (in SBML or equivalent format) for multiple organisms sampled from a single ecological community (e.g., plant-associated microbiota) and want to generate a unified, agreement-based metabolic model that captures only the metabolic capabilities shared across all community members, particularly before performing community-dependent gap-filling.

## When NOT to use

- Input reconstructions are from unrelated organisms not sampled from a single ecological community; consensus approach requires shared evolutionary or ecological context.
- You require a comprehensive model that captures all metabolic potential of individual organisms; consensus models are deliberately conservative and exclude organism-specific capabilities.
- Your input models are already highly curated and manually validated; consensus generation may remove important but rare pathway variants.

## Inputs

- Draft metabolic reconstructions in SBML format for all community member organisms
- Specification of consensus criteria (e.g., reaction presence threshold across models)

## Outputs

- Consensus metabolic reconstructions for each organism in the community
- List of conserved reactions and metabolites agreed upon by consensus criteria

## How to apply

Load all draft metabolic reconstructions for community member organisms in a standard format (SBML). Execute the COMMIT consensus generation algorithm to integrate the draft models and identify conserved metabolic reactions across all input reconstructions for each organism. The algorithm retains only reactions and metabolites that meet consensus criteria (i.e., present in all or a specified threshold of input models). Output the consensus metabolic reconstruction for each organism, which serves as the curated input for downstream community-dependent gap-filling and metabolic modeling. Verify that the consensus model contains a union of metabolites and a conservative subset of reactions compared to individual drafts.

## Related tools

- **COMMIT** (Performs consensus generation and community-dependent gap-filling for metabolic model integration from multiple draft reconstructions) — 10.5281/zenodo.363932874

## Evaluation signals

- Consensus model reaction count is less than or equal to the union of all input models and greater than the intersection of any single pair, reflecting conservative agreement-based filtering.
- All reactions in the consensus model are present in 100% (or specified threshold) of input reconstructions; verify by cross-checking against source models.
- Metabolite coverage in the consensus model is complete for all reactions present; no orphaned metabolites or incomplete stoichiometry.
- Community-dependent gap-filling downstream successfully adds organism-specific reactions while preserving consensus backbone, indicating the consensus model is a suitable foundation.
- Output metabolic model validates syntactically in SBML schema and contains non-zero gene-protein-reaction associations (GPRs) where applicable.

## Limitations

- Consensus approach assumes that metabolic reactions conserved across all community members represent the 'true' shared metabolism; rare or unique pathways are discarded, which may omit important niche-specific metabolism.
- No changelog or version history documentation was found for COMMIT, limiting reproducibility tracking and validation of algorithm changes.
- Consensus generation requires input models to be in compatible formats and with consistent metabolite and reaction identifier namespaces; heterogeneous annotation across inputs may lead to false negatives in consensus detection.
- The method is designed for plant-associated microbial communities sampled from Arabidopsis thaliana; generalization to other ecological contexts (e.g., human microbiota, soil) is untested.

## Evidence

- [intro] COMMIT generates consensus metabolic reconstructions and performs community-dependent gap-filling for microbial communities sampled from Arabidopsis thaliana.: "COMMIT generates consensus metabolic reconstructions and performs community-dependent gap-filling for microbial communities sampled from Arabidopsis thaliana."
- [other] Execute COMMIT consensus generation algorithm to integrate draft models and identify conserved metabolic reactions across all input reconstructions for each organism.: "Execute COMMIT consensus generation algorithm to integrate draft models and identify conserved metabolic reactions across all input reconstructions for each organism."
- [other] Output the consensus metabolic reconstruction for each organism, containing only reactions and metabolites agreed upon by the consensus criteria.: "Output the consensus metabolic reconstruction for each organism, containing only reactions and metabolites agreed upon by the consensus criteria."
- [other] Load draft metabolic reconstructions for all community member organisms in standard format (e.g., SBML).: "Load draft metabolic reconstructions for all community member organisms in standard format (e.g., SBML)."
