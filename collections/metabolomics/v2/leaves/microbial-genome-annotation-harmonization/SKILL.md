---
name: microbial-genome-annotation-harmonization
description: Use when you have draft metabolic reconstructions (in SBML or standard
  format) for multiple organisms sampled from the same microbial community and need
  to produce a single consensus model per organism that reflects only metabolic capabilities
  agreed upon across the input reconstructions, or when.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_0623
  - http://edamontology.org/topic_3697
  tools:
  - COMMIT
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009906
  title: COMMIT
- doi: 10.5281/zenodo.363932874
  title: ''
evidence_spans:
- community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis
  thaliana
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

# microbial-genome-annotation-harmonization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate consensus metabolic reconstructions from multiple draft genome annotations of community member organisms by identifying and integrating conserved metabolic reactions across all input models. This skill is essential when working with microbial communities where individual genome annotations exist but need unified, community-aware metabolic representations.

## When to use

You have draft metabolic reconstructions (in SBML or standard format) for multiple organisms sampled from the same microbial community and need to produce a single consensus model per organism that reflects only metabolic capabilities agreed upon across the input reconstructions, or when preparing models for community-dependent gap-filling.

## When NOT to use

- Input is a single organism reconstruction rather than multiple draft reconstructions for the same organism from different sources.
- Community membership or organism identity is unknown or poorly defined.
- Reconstructions are already manually curated and do not require consensus filtering across multiple sources.

## Inputs

- Draft metabolic reconstructions in SBML format (one per community member organism)
- List of organism identifiers or reconstruction file paths

## Outputs

- Consensus metabolic reconstruction per organism (SBML format)
- Consensus metabolic model containing only conserved reactions and metabolites

## How to apply

Load all draft metabolic reconstructions for community member organisms in standard format (e.g., SBML). Execute the COMMIT consensus generation algorithm to integrate the draft models and identify conserved metabolic reactions across all input reconstructions for each organism. The algorithm filters to retain only reactions and metabolites that meet consensus criteria, producing a harmonized reconstruction per organism. The rationale is that consensus-based integration reduces annotation artifacts and model redundancy while preserving metabolic functions conserved across independently annotated genomes, preparing the models for reliable community-level analysis and downstream gap-filling.

## Related tools

- **COMMIT** (Consensus generation algorithm that integrates draft metabolic reconstructions and identifies conserved metabolic reactions across all input models) — 10.5281/zenodo.363932874

## Evaluation signals

- Each output consensus reconstruction contains only reactions and metabolites present in input reconstructions that meet the consensus criteria.
- The number of retained reactions per organism should be ≤ the minimum number across all input draft reconstructions for that organism.
- Output SBML files are valid and parseable by standard metabolic modeling tools.
- Consensus reconstructions can be successfully used as input for downstream community-dependent gap-filling without errors.
- Metabolic coverage (e.g., number of pathways represented) is consistent across consensus reconstructions for organisms in the same community.

## Limitations

- Consensus approach may remove organism-specific metabolic reactions that are genuinely present but annotated inconsistently across draft reconstructions.
- Quality of consensus reconstructions is dependent on the accuracy and completeness of the input draft reconstructions.
- Method assumes that input reconstructions use compatible reaction nomenclature and metabolite identifiers; significant format heterogeneity may degrade consensus quality.

## Evidence

- [other] Load draft metabolic reconstructions in standard format (SBML): "Load draft metabolic reconstructions for all community member organisms in standard format (e.g., SBML)."
- [other] COMMIT consensus algorithm integrates models and identifies conserved reactions: "Execute COMMIT consensus generation algorithm to integrate draft models and identify conserved metabolic reactions across all input reconstructions for each organism."
- [other] Output contains only reactions and metabolites meeting consensus criteria: "Output the consensus metabolic reconstruction for each organism, containing only reactions and metabolites agreed upon by the consensus criteria."
- [intro] Applied to Arabidopsis thaliana plant-associated communities: "Generation of consensus metabolic reconstructions and community-dependent gap-filling using COMMIT for communites sampled from _Arabidopsis thaliana_"
