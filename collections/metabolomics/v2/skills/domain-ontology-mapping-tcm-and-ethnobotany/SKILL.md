---
name: domain-ontology-mapping-tcm-and-ethnobotany
description: Use when when integrating structure-organism pairs from TCM databases, ethnobotanical collections, or alternative medicine sources that use domain-specific or transliterated terminology (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0089
  tools:
  - R
  - Python 3
  - Make
  - tcm.R
  - common.R
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

# Domain-ontology mapping for Traditional Chinese Medicine and ethnobotany

## Summary

Build controlled-vocabulary mappings for Traditional Chinese Medicine (TCM) and alternative medicine nomenclature, translating local database identifiers and substance names into standardized ontology terms. This ensures heterogeneous ethnobotanical and TCM data sources can be reconciled and queried using shared semantic frameworks.

## When to use

When integrating structure-organism pairs from TCM databases, ethnobotanical collections, or alternative medicine sources that use domain-specific or transliterated terminology (e.g., TCM plant names, indigenous preparation methods) that differs from chemical IUPAC nomenclature or standard taxonomic ranks. Use this skill when you need to harmonize multiple TCM or ethnobotanical vocabularies into a single queryable namespace before downstream curation or analysis.

## When NOT to use

- Input is a purely synthetic chemical library with no ethnobotanical or TCM provenance; no domain-specific terminology enrichment is possible or needed.
- Organism data is already standardized to a single monolithic taxonomy (e.g., NCBI only) with no alternative naming schemes to reconcile.
- The analysis goal requires only chemical structure comparison (e.g., scaffold analysis, descriptor calculation) and does not depend on semantic organism or preparation metadata.

## Inputs

- interim/db/*.tsv files (standardized structure-organism-reference triples with columns: structure_id, organism, reference, source_db, raw_data)
- interim/dictionaries/common/* lookup tables (existing InChI, SMILES, taxonomic mappings)
- TCM or ethnobotanical source databases in external/dbSource/ (heterogeneous formats: TSV, JSON, XML with TCM-specific fields)

## Outputs

- interim/dictionaries/tcm/* lookup tables (TCM and alternative medicine ontology mappings, e.g., pinyin-to-standard-name, preparation-type taxonomies, meridian associations)
- enriched interim/db/*.tsv files with tcm_ontology_id, preparation_method, and ethnobotanical_context columns appended

## How to apply

After standardizing and translating chemical structure and organism identifiers (InChI, SMILES, taxonomic ranks) via common.R, run the tcm.R translation script on the interim/db outputs to build domain-specific ontology mappings. Create lookup tables in interim/dictionaries/tcm/* that capture TCM-specific concepts (e.g., herbal preparation categories, meridian associations, traditional disease indications) and ethnobotanical metadata (indigenous names, preparation methods, cultural contexts). Map local identifiers from TCM sources (e.g., pinyin names, Chinese character variants) to standardized ontology terms or external identifiers (e.g., NCBI Taxonomy for organisms, ChEMBL or PubChem for structures). Validate that mappings are bijective or many-to-one (allowing synonymy but preventing ambiguous one-to-many collisions) and that no critical linking fields between structure, organism, and reference are null in >5% of rows after enrichment.

## Related tools

- **tcm.R** (Translates TCM and alternative medicine identifiers into standardized ontology mappings; generates interim/dictionaries/tcm/* lookup tables) — https://github.com/lotusnprod/lotus-processor
- **common.R** (Prerequisite translation script that maps local identifiers to controlled vocabularies (InChI, SMILES, taxonomic ranks); provides foundation for tcm.R enrichment) — https://github.com/lotusnprod/lotus-processor
- **R** (Execution environment for tcm.R and ontology mapping scripts)

## Examples

```
Rscript interim/tcm.R --input interim/db/organisms.tsv --common-dict interim/dictionaries/common/organism_mapping.tsv --output interim/dictionaries/tcm/tcm_ontology_mapping.tsv
```

## Evaluation signals

- Lookup tables in interim/dictionaries/tcm/* are non-empty and contain expected TCM and ethnobotanical fields (e.g., pinyin_name, preparation_type, meridian_association, source_ontology_uri).
- No row in the enriched interim/db/*.tsv file has null values in critical TCM-linking fields (tcm_ontology_id, organism_name, reference_doi) in >5% of rows.
- Mappings are internally consistent (e.g., all rows with the same pinyin_name map to a single standardized ontology term; no contradictory 1-to-many assignments).
- Cross-validation: sample enriched rows manually and verify that TCM ontology assignments align with domain expert expectations or published TCM classification schemes (e.g., Chinese Herbal Medicine Dictionary).
- Row counts in interim/db/*.tsv match source row counts after tcm.R enrichment (no data loss); any filtered rows are logged with reason codes.

## Limitations

- Mapping quality depends on the comprehensiveness and accuracy of the TCM and ethnobotanical reference ontologies used; rare or newly described TCM preparations may have no mapping and will be left null or require manual curation.
- Transliteration and character encoding inconsistencies (e.g., pinyin variant spellings, simplified vs. traditional Chinese characters) can cause false non-matches; preprocessing and fuzzy matching may be needed.
- Domain-specific terminology (e.g., meridian associations, energetic properties) may not have direct analogues in NCBI Taxonomy or ChEMBL, limiting interoperability with purely chemical databases.
- No changelog found — version history and updates to TCM ontology mappings are not documented, making it difficult to track which ontology versions were used for a given LOTUS release.

## Evidence

- [methods] Run tcm.R translation script to build Traditional Chinese Medicine and alternative medicine ontology mappings into interim/dictionaries/tcm/*: "Run tcm.R translation script to build Traditional Chinese Medicine and alternative medicine ontology mappings into interim/dictionaries/tcm/*."
- [methods] 1_gathering stage performs external database standardization and translation using R scripts (standardizing.R, common.R, tcm.R) to harmonize data from 31 initial open databases: "1_gathering stage performs external database standardization and translation using R scripts (standardizing.R, common.R, tcm.R) to harmonize data from 31 initial open databases into original tables."
- [methods] Validate output schemas and row counts match input database source counts; verify no critical fields (structure_id, organism_name, reference_doi) are null in >5% of rows: "Validate output schemas and row counts match input database source counts; verify no critical fields (structure_id, organism_name, reference_doi) are null in >5% of rows."
- [methods] Data originates from 31 initial open databases: "originating from 31 initial open databases"
- [readme] LOTUS is a comprehensive collection of documented structure-organism pairs that should allow more complete understanding of organisms and their chemistry within computational approaches: "*LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented"
