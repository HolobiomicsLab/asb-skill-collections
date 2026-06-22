---
name: taxonomic-nomenclature-normalization-and-validation
description: Use when you have organism names originating from 31+ heterogeneous natural product databases that use different taxonomic authorities, nomenclature versions, or rank assignments, and you need to harmonize them into a single organism subgraph with validated ranks before linking to chemical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_0621
  tools:
  - R
  - Python 3
  - Make
  - 2_translating_organism
  - 4_cleaningTaxonomy.R
  - 5_addingOTL.R
  - Kotlin
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- db/../standardizing.R, common.R
- 1_integrating.R
- Python scripts for data parsing and transformation
- 221[[smiles.py]]
- Please make sure to have [Make](https://www.gnu.org/software/make) installed.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus_cq
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.7554/eLife.70780
  all_source_dois:
  - 10.7554/eLife.70780
  - 10.1007/s00044-016-1764-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# taxonomic-nomenclature-normalization-and-validation

## Summary

Standardizes organism names from heterogeneous source databases into controlled taxonomic vocabularies and validates ranks, resolving nomenclatural conflicts and ensuring consistent organism identity across a structure-organism pair collection. This skill is essential when ingesting natural product data from multiple curated databases with divergent taxonomic authority standards.

## When to use

Apply this skill when you have organism names originating from 31+ heterogeneous natural product databases that use different taxonomic authorities, nomenclature versions, or rank assignments, and you need to harmonize them into a single organism subgraph with validated ranks before linking to chemical structures and references.

## When NOT to use

- Input organism names are already validated against a single authoritative taxonomy and do not require reconciliation across heterogeneous sources.
- The analysis goal is purely chemical (e.g., structure similarity, molecular property prediction) and organism identity is not required for downstream computations.
- Taxonomic rank information is not available or not critical for the research question.

## Inputs

- heterogeneous organism names from external/dbSource/* files (TSV, JSON, XML formats)
- local organism identifiers with associated raw taxonomic metadata
- interim/db/*.tsv files containing organism taxonomy data partitioned by source

## Outputs

- standardized organism subgraph with mapped controlled vocabulary identifiers (NCBI Taxonomy, taxonomic ranks)
- interim/dictionaries/common/* lookup tables for organism name-to-rank mappings
- interim/dictionaries/tcm/* ontology-enriched organism identifiers for Traditional Chinese Medicine and alternative medicine
- validated organism records with enforced rank consistency and null-check validation (≤5% nulls in organism_name, taxonomic_rank)

## How to apply

First, run the translating_organism filter (2_translating_organism/../main.kt) to map local organism identifiers from each source database to controlled taxonomic vocabularies (e.g., NCBI Taxonomy, taxonomic ranks). Then apply cleaningTaxonomy (4_cleaningTaxonomy.R) to validate and standardize rank assignments, resolve synonyms, and flag nomenclatural conflicts. Finally, run addingOTL (5_addingOTL.R) to enrich the standardized taxonomy with additional ontology mappings. Validation passes when no critical organism_name fields are null in >5% of rows and rank consistency is enforced across the organism subgraph.

## Related tools

- **2_translating_organism** (Maps local organism identifiers from source databases to controlled taxonomic vocabularies (NCBI Taxonomy, taxonomic ranks)) — https://github.com/lotusnprod/lotus-processor
- **4_cleaningTaxonomy.R** (Validates and standardizes taxonomic rank assignments, resolves nomenclatural synonyms and conflicts) — https://github.com/lotusnprod/lotus-processor
- **5_addingOTL.R** (Enriches standardized taxonomy with additional ontology mappings for Traditional Chinese Medicine and alternative medicine) — https://github.com/lotusnprod/lotus-processor
- **Kotlin** (Implementation language for 2_translating_organism organism identifier mapping script)
- **R** (Implementation language for cleaningTaxonomy and addingOTL validation and enrichment scripts)

## Examples

```
Rscript 4_cleaningTaxonomy.R < interim/db/organism_taxonomy.tsv > interim/dictionaries/common/organism_rank_validated.tsv
```

## Evaluation signals

- No organism_name field is null in >5% of rows in the standardized organism subgraph output.
- All organism records successfully map to at least one controlled vocabulary identifier (NCBI Taxonomy rank or equivalent).
- Organism rank consistency is enforced: child-parent taxonomic relationships in the organism subgraph conform to expected hierarchy (e.g., species nests under genus, genus under family).
- Row count in standardized organism output matches the input source database row count (accounting for deduplicated synonyms documented in mapping tables).
- Lookup tables in interim/dictionaries/common/* and interim/dictionaries/tcm/* contain no circular references and all mappings are bidirectionally resolvable.

## Limitations

- Nomenclatural conflicts arising from outdated or colloquial organism names in legacy databases may not be fully resolvable against a single authority; manual curation may be required for >5% of records.
- The skill assumes controlled taxonomic vocabularies (e.g., NCBI Taxonomy) are available and up-to-date; gaps or lags in authority maintenance can propagate into the standardized output.
- Traditional Chinese Medicine and alternative medicine ontologies (interim/dictionaries/tcm/*) may have limited coverage for rare or underrepresented organisms, resulting in partial enrichment.
- No changelog is documented for version updates to the translation and cleaning scripts, making it difficult to track nomenclatural standard changes across processor releases.

## Evidence

- [methods] standardizing.R translation script to build Traditional Chinese Medicine and alternative medicine ontology mappings: "Run tcm.R translation script to build Traditional Chinese Medicine and alternative medicine ontology mappings into interim/dictionaries/tcm/*."
- [methods] organism rank validation thresholds: "verify no critical fields (structure_id, organism_name, reference_doi) are null in >5% of rows."
- [methods] organism subgraph as a curating stage component: "2_curating: 1_integrating.R, organism subgraph, structure subgraph, reference subgraph"
- [methods] translating_organism as a filter step in the pipeline: "translating_organism  [section=methods; evidence='2_translating_organism/../main.kt']"
- [methods] cleaningTaxonomy filter step for rank standardization: "cleaningTaxonomy  [section=methods; evidence='4_cleaningTaxonomy.R']"
- [methods] origin from 31 initial open databases requiring harmonization: "Data originates from 31 initial open databases"
- [methods] controlled vocabulary mapping in common.R script: "Run common.R translation script on interim/db outputs to map local identifiers to controlled vocabularies (InChI, SMILES, taxonomic ranks), writing interim/dictionaries/common/* lookup tables."
- [readme] README description of structure-organism pair standardization objective: "*LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented"
