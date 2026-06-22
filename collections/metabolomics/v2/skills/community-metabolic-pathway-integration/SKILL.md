---
name: community-metabolic-pathway-integration
description: Use when you have multiple draft metabolic models (in JSON, XML, or SBML format) representing individual members or assembly variants of a community—such as Arabidopsis thaliana-associated microbiota—and need a single integrated model that captures the consensus metabolic potential while resolving.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_3697
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

# community-metabolic-pathway-integration

## Summary

Merge multiple draft genome-scale metabolic reconstructions into a single consensus model for microbial communities by resolving pathway conflicts and gaps using community-dependent logic. This skill is essential when analyzing metabolic capacity of natural or engineered communities where individual member reconstructions must be unified to model community-level phenotypes.

## When to use

Apply this skill when you have multiple draft metabolic models (in JSON, XML, or SBML format) representing individual members or assembly variants of a community—such as Arabidopsis thaliana-associated microbiota—and need a single integrated model that captures the consensus metabolic potential while resolving pathway conflicts and redundancies across members.

## When NOT to use

- Input models are already manually curated, literature-validated consensus reconstructions—merging may introduce noise.
- Community has < 2 member models—consensus logic requires multiple sources to identify common and divergent pathways.
- Models are from phylogenetically distant organisms where pathway conservation assumptions break down.

## Inputs

- Multiple draft genome-scale metabolic models (JSON, XML, or SBML format)
- Community member annotations or assembly variant metadata

## Outputs

- Consensus genome-scale metabolic reconstruction (SBML format)
- Merged reaction, metabolite, and gene association inventory
- Gap-filling resolution log (pathway selection rationale)

## How to apply

Load and validate all input draft metabolic models using COMMIT to ensure structural integrity and annotation consistency. Execute COMMIT's consensus-merging algorithm to identify common reactions, metabolites, and gene associations across all models. Apply community-dependent gap-filling logic to resolve conflicts by selecting the most supported metabolic pathways based on representation frequency or annotation confidence across the member models. This prioritizes pathways present in multiple reconstructions over singleton variants. Export the final consensus reconstruction in standard systems biology markup language (SBML) format suitable for downstream flux balance analysis or community phenotype prediction.

## Related tools

- **COMMIT** (Executes consensus-merging algorithm, community-dependent gap-filling, model validation, and standardized export of merged metabolic reconstructions.) — https://zenodo.org/badge/latestdoi/363932874

## Evaluation signals

- All input draft models parse without structural errors after COMMIT validation; annotation consistency check reports no fatal inconsistencies.
- Consensus model contains the union of all reactions present in ≥2 input models plus community-supported gap-filled reactions; singleton reactions are tracked separately.
- Gap-filling resolution log documents which input models supported each conflict-resolved pathway; selected pathways should align with frequency or annotation coverage thresholds.
- Final SBML output conforms to standard systems biology markup schema; stoichiometry and gene-protein-reaction rules are syntactically valid.
- Consensus model metabolic capacity (e.g., predicted biomass production under community growth conditions) is equal to or greater than any single input model when simulated in isolation.

## Limitations

- Consensus merging assumes that draft input models are sufficiently complete and accurate; poor-quality reconstructions can bias the consensus toward erroneous pathways.
- Community-dependent gap-filling relies on pathway frequency across members; rare but functionally critical pathways may be discarded if present in only one model.
- Method is most validated for Arabidopsis thaliana-associated communities; applicability to other host-associated or environmental consortia may require parameter re-tuning.
- Resolving annotation conflicts (e.g., alternative gene symbols, pathway nomenclature) depends on input model standardization; highly heterogeneous annotations may require pre-processing.

## Evidence

- [other] Multiple draft metabolic models as input: "Load multiple draft metabolic models (in standard format such as JSON or XML) representing individual community members or assembly variants."
- [other] Consensus-merging algorithm identifies common pathways: "Execute COMMIT's consensus-merging algorithm to identify common reactions, metabolites, and gene associations across all input models."
- [other] Community-dependent gap-filling to resolve conflicts: "Resolve conflicts and gaps by applying COMMIT's community-dependent gap-filling logic to select the most supported metabolic pathways."
- [other] SBML export as final output: "Generate and export the final consensus metabolic reconstruction in standard systems biology format (e.g., SBML)."
- [intro] Application context: Arabidopsis thaliana communities: "Generation of consensus metabolic reconstructions and community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana"
