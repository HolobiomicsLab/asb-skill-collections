---
name: metabolic-model-merging-consensus-building
description: Use when you have multiple draft metabolic reconstructions (in JSON, XML, or SBML format) representing individual members or assembly variants of a community and need a single, non-redundant consensus model that captures shared and community-supported metabolic capacity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3810
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

# metabolic-model-merging-consensus-building

## Summary

Merge multiple draft genome-scale metabolic models into a single consensus reconstruction by resolving conflicts and gaps using community-dependent logic. This skill is essential when integrating metabolic diversity from multi-member microbial or plant-associated communities into a unified, systems-level representation.

## When to use

Apply this skill when you have multiple draft metabolic reconstructions (in JSON, XML, or SBML format) representing individual members or assembly variants of a community and need a single, non-redundant consensus model that captures shared and community-supported metabolic capacity. Typical trigger: presence of >1 validated genome-scale metabolic model for the same community context.

## When NOT to use

- Input models are already manually curated and validated by domain experts; consensus merging may introduce errors if expert curation is overridden by majority voting.
- Only a single metabolic model is available; consensus merging requires >1 input model to be meaningful.
- Models represent distinct ecological niches or taxa with fundamentally incompatible metabolic strategies; forced consensus may obscure important functional diversity.

## Inputs

- Multiple draft genome-scale metabolic models (JSON, XML, or SBML format)
- Model annotation metadata (gene associations, reaction evidence)
- Community context or sample metadata (optional, for gap-filling weighting)

## Outputs

- Single consensus metabolic reconstruction (SBML format)
- Merged reaction and metabolite inventory
- Gap-filling log documenting conflict resolution decisions

## How to apply

Load all draft metabolic models in standard format (JSON, XML, SBML) and validate each using COMMIT to check structural integrity and annotation consistency. Execute COMMIT's consensus-merging algorithm to identify common reactions, metabolites, and gene associations across all input models. Resolve conflicts and gaps by applying community-dependent gap-filling logic to select the most supported metabolic pathways—prioritizing reactions present in multiple drafts or supported by community context. Export the final consensus model in SBML or equivalent systems biology format. Validation: cross-check that the consensus model contains the union of essential reactions and is smaller than the sum of individual models, indicating successful deduplication.

## Related tools

- **COMMIT** (Merges multiple draft metabolic models and implements community-dependent gap-filling to resolve conflicts and generate consensus reconstruction) — https://zenodo.org/badge/latestdoi/363932874

## Evaluation signals

- Consensus model passes structural validation (SBML schema compliance, no orphaned reactions or metabolites).
- Reaction overlap: verify that shared reactions across input models are present in the consensus, and strain-specific reactions are reconciled or noted.
- Model size: consensus reaction/metabolite count falls between the minimum and maximum of input models (not the sum, indicating deduplication).
- Gap-filling completeness: consensus model has no unresolved metabolic gaps for core pathways relevant to the community context.
- Reproducibility: re-running the merge with the same inputs produces identical consensus output.

## Limitations

- COMMIT requires input models to be in parseable standard format (JSON, XML, SBML); poorly annotated or non-standard models may fail validation.
- Community-dependent gap-filling relies on contextual metadata; absence of community sampling or growth condition information may reduce accuracy of gap-filling decisions.
- Consensus merging assumes draft models represent genuine biological diversity; contamination or artifacts in individual models can propagate into consensus.
- The method does not prioritize rare or strain-specific metabolic functions; minority pathways may be lost if present in only one or few input models.

## Evidence

- [other] COMMIT implements community-dependent gap-filling to generate consensus metabolic reconstructions from multiple draft reconstructions: "COMMIT implements community-dependent gap-filling to generate consensus metabolic reconstructions from multiple draft reconstructions of Arabidopsis thaliana-associated communities."
- [other] Execute COMMIT's consensus-merging algorithm to identify common reactions and resolve conflicts: "Execute COMMIT's consensus-merging algorithm to identify common reactions, metabolites, and gene associations across all input models. 4. Resolve conflicts and gaps by applying COMMIT's"
- [other] Load multiple draft metabolic models in standard format and validate each input model: "Load multiple draft metabolic models (in standard format such as JSON or XML) representing individual community members or assembly variants. 2. Parse and validate each input model using COMMIT to"
- [other] Generate and export the final consensus metabolic reconstruction in standard systems biology format: "Generate and export the final consensus metabolic reconstruction in standard systems biology format (e.g., SBML)."
- [intro] Development of consensus metabolic reconstructions from Arabidopsis thaliana communities: "Generation of consensus metabolic reconstructions and community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana"
