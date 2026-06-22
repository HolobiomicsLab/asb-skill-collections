---
name: controlled-vocabulary-lookup-table-construction
description: 'Use when after ingesting and parsing multiple external databases with diverse identifier schemes and nomenclatures. Trigger conditions: (1) you have interim standardized tables with local identifiers (structure_id, organism_name, reference_doi) that lack semantic normalization;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0219
  - http://edamontology.org/topic_0637
  tools:
  - R
  - Python 3
  - Make
  - common.R
  - tcm.R
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# controlled-vocabulary-lookup-table-construction

## Summary

Build standardized lookup tables that map local identifiers (structure IDs, organism names, reference DOIs) to controlled vocabularies (InChI, SMILES, taxonomic ranks) and domain ontologies (e.g., Traditional Chinese Medicine). This skill is essential for harmonizing heterogeneous source data into a unified semantic space before integration and validation.

## When to use

Apply this skill after ingesting and parsing multiple external databases with diverse identifier schemes and nomenclatures. Trigger conditions: (1) you have interim standardized tables with local identifiers (structure_id, organism_name, reference_doi) that lack semantic normalization; (2) you need to map these identifiers to widely adopted controlled vocabularies (InChI, SMILES, taxonomic ranks) or domain-specific ontologies; (3) downstream analysis or integration requires consistent, machine-readable identifiers across all source databases.

## When NOT to use

- Input identifiers are already harmonized to a single controlled vocabulary (e.g., all structures already in InChI format, all organisms already in NCBI Taxonomy). In this case, skip to validation.
- No external controlled vocabularies or ontologies are available for the domain or data type.
- The source databases use proprietary or non-reversible identifier schemes with no public mapping documentation.

## Inputs

- interim/db/*.tsv files (standardized tables with columns: structure_id, organism, reference, source_db, raw_data)
- external database source records in heterogeneous formats (TSV, JSON, XML, proprietary schemas)

## Outputs

- interim/dictionaries/common/* lookup tables (mapping local identifiers to InChI, SMILES, taxonomic ranks)
- interim/dictionaries/tcm/* lookup tables (domain-specific ontology mappings, e.g., Traditional Chinese Medicine)
- validated lookup tables with bidirectional traceability and null-field inventory

## How to apply

Execute translation scripts sequentially on interim standardized outputs to build and populate lookup tables. First, run a common.R translation script on interim/db/ TSV files to map local structure and organism identifiers to standard vocabularies (InChI, SMILES, taxonomic ranks), writing results to interim/dictionaries/common/* lookup tables. Second, run a domain-specific translation script (e.g., tcm.R for Traditional Chinese Medicine) to enrich organism and structure records with ontology mappings, writing to interim/dictionaries/tcm/*. Each lookup table should preserve bidirectional traceability: local identifier → standard identifier, and standard identifier → source_db + original local ID. Validate that no critical fields remain null in >5% of rows and that row counts match input database records.

## Related tools

- **common.R** (Translation script that maps local identifiers to controlled vocabularies (InChI, SMILES, taxonomic ranks) and writes lookup tables to interim/dictionaries/common/*) — https://github.com/lotusnprod/lotus-processor
- **tcm.R** (Domain-specific translation script that builds Traditional Chinese Medicine and alternative medicine ontology mappings into interim/dictionaries/tcm/*) — https://github.com/lotusnprod/lotus-processor
- **R** (Language used to implement translation and mapping scripts)

## Examples

```
Rscript common.R --input interim/db/ --output interim/dictionaries/common/ --vocabulary InChI,SMILES,NCBI_Taxonomy && Rscript tcm.R --input interim/db/ --output interim/dictionaries/tcm/
```

## Evaluation signals

- All rows in output lookup tables have non-null values in critical fields (local_id, standard_id, source_db, mapping_date); null-field inventory shows ≤ 5% nulls in any column.
- Row counts in lookup tables match or exceed row counts in corresponding interim/db/*.tsv source files (accounting for deduplicated IDs).
- Bidirectional traceability is preserved: for a random sample of 10–20 entries, local_id → standard_id and reverse lookup standard_id → source_db + original local_id both succeed with no orphaned IDs.
- Domain-specific lookup tables (e.g., tcm/*) contain expected ontology mappings with documented provenance (e.g., source vocabulary version, mapping date, reference URI).
- No collisions: distinct local identifiers map to distinct standard identifiers (1:1 mapping enforced at validation step); if many-to-1 or 1-to-many mappings exist, they are explicitly documented and flagged.

## Limitations

- Translation accuracy depends on the quality and coverage of external controlled vocabularies; gaps in vocabulary coverage will result in unmapped or null entries.
- Bidirectional mapping may not always be possible if local identifiers include ambiguous or non-standard nomenclature not present in the target vocabulary.
- Domain-specific ontologies (e.g., TCM) may have overlapping or conflicting definitions; conflicts must be manually curated or resolved using explicit priority rules.
- The 5% null-field threshold is a heuristic; some use cases may require stricter thresholds (e.g., 0% nulls in critical fields).
- No changelog is documented; version history and updates to vocabulary mappings are not tracked, potentially complicating reproducibility and lineage tracing across LOTUS processor releases.

## Evidence

- [methods] Run common.R translation script on interim/db outputs to map local identifiers to controlled vocabularies: "Run common.R translation script on interim/db outputs to map local identifiers to controlled vocabularies (InChI, SMILES, taxonomic ranks), writing interim/dictionaries/common/* lookup tables."
- [methods] Run tcm.R translation script to build Traditional Chinese Medicine and alternative medicine ontology mappings: "Run tcm.R translation script to build Traditional Chinese Medicine and alternative medicine ontology mappings into interim/dictionaries/tcm/*."
- [methods] Validate output schemas and ensure no critical fields are null in >5% of rows: "Validate output schemas and row counts match input database source counts; verify no critical fields (structure_id, organism_name, reference_doi) are null in >5% of rows."
- [methods] Standardized outputs into interim/db/*.tsv files partitioned by data type: "Consolidate standardized outputs into interim/db/*.tsv files partitioned by data type (organism taxonomy, chemical structure metadata, bibliographic records)."
- [other] No changelog found — version history and updates not documented: "No changelog found — version history and updates not documented"
