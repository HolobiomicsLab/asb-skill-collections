---
name: chemical-identifier-standardization-and-mapping
description: Use when you have structure-organism pairs originating from multiple open databases (e.g., ChEMBL, PubChem, Wikidata) with disparate identifier schemes, file formats (TSV, JSON, XML, proprietary schemas), and taxonomic rank naming conventions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3071
  tools:
  - R
  - Python 3
  - Make
  - standardizing.R
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-identifier-standardization-and-mapping

## Summary

Standardize and map heterogeneous chemical identifiers (InChI, SMILES, structure IDs) and organism taxonomy across multiple source databases into unified controlled vocabularies. This skill is essential when ingesting multi-source natural product datasets where chemical nomenclature and taxonomic rank representations vary by source.

## When to use

Apply this skill when you have structure-organism pairs originating from multiple open databases (e.g., ChEMBL, PubChem, Wikidata) with disparate identifier schemes, file formats (TSV, JSON, XML, proprietary schemas), and taxonomic rank naming conventions. Trigger conditions: >1 source database, >5% of rows with null or inconsistent structure_id, organism_name, or reference_doi fields, or need to cross-reference structures and organisms across sources.

## When NOT to use

- Input is already a single, internally consistent table with a fixed identifier scheme and no cross-source reconciliation needed.
- Chemical structures are represented only as 2D images or spectra with no encoded molecular graphs; InChI/SMILES mapping is not applicable.
- Organism taxonomy is not available or is out of scope for the analysis.

## Inputs

- raw structure-organism pair tables from external databases (TSV, JSON, XML, proprietary formats)
- source database metadata (schema documentation, identifier systems)
- local and external controlled vocabulary resources (InChI, SMILES, taxonomic databases)

## Outputs

- standardized interim/db/*.tsv tables with unified schema (structure_id, organism, reference, source_db, raw_data)
- interim/dictionaries/common/* lookup tables mapping to InChI and SMILES
- interim/dictionaries/tcm/* Traditional Chinese Medicine and alternative medicine ontology mappings
- validated consolidation with schema conformance and completeness metrics

## How to apply

First, run source-database-specific standardizing.R scripts to parse heterogeneous input formats into a common relational schema (columns: structure_id, organism, reference, source_db, raw_data). Next, consolidate standardized outputs into interim/db/*.tsv files partitioned by data type (organism taxonomy, chemical structure metadata, bibliographic records). Then apply common.R translation scripts to map local structure identifiers to InChI and SMILES canonical forms using controlled vocabulary lookup tables. Finally, apply tcm.R translation to build Traditional Chinese Medicine and alternative medicine ontology mappings. Validate output schemas and ensure no critical fields have >5% null rate; verify row counts match input source counts to confirm lossless integration.

## Related tools

- **standardizing.R** (Parse heterogeneous database formats (TSV, JSON, XML, proprietary schemas) into common relational schema) — https://github.com/lotusnprod/lotus-processor
- **common.R** (Translate local structure identifiers to InChI, SMILES, and taxonomic rank controlled vocabularies) — https://github.com/lotusnprod/lotus-processor
- **tcm.R** (Build Traditional Chinese Medicine and alternative medicine ontology mappings for structure-organism pairs) — https://github.com/lotusnprod/lotus-processor
- **R** (Execute standardizing, translation, and validation scripts)
- **Python 3** (Support data sanitization, SMILES validation, and related cheminformatics tasks)

## Examples

```
cd lotus-processor && Rscript external/dbSource/db_name/standardizing.R && Rscript common.R && Rscript tcm.R
```

## Evaluation signals

- Output schema matches input schema requirement; all rows contain non-null values for structure_id, organism_name, reference_doi (or documented exceptions <5% per field).
- Row count of each interim/db/*.tsv file matches input source count; no records lost during standardization.
- All structure identifiers are successfully mapped to canonical InChI or SMILES in interim/dictionaries/common/* lookup tables; mapping coverage documented.
- Organism taxonomy is reconciled to controlled rank vocabularies; cross-source conflicts logged and resolved entries verified against reference sources (NCBI Taxonomy, etc.).
- TCM ontology mappings exist and are non-empty for traditional medicine sources; alternative medicine terms are consistently applied across records.

## Limitations

- Standardization is source-specific: each database requires a custom standardizing.R script; novel or proprietary schemas may require new script development.
- Identifier mapping relies on external controlled vocabularies (InChI, SMILES, taxonomic databases); incomplete or outdated reference data will reduce mapping coverage.
- Organism taxonomy reconciliation assumes taxonomic names are available and reasonably standardized within source databases; highly colloquial or misspelled organism names may fail to map.
- No changelog or version history is documented in the repository, making it difficult to track backwards-compatible changes to identifier schemes or ontology mappings.
- Large-scale data with many-to-many structure-organism relationships may produce memory-intensive lookup tables; partitioning and incremental processing strategy not detailed in provided materials.

## Evidence

- [methods] 1. For each source database in external/dbSource/, run db/../standardizing.R to parse heterogeneous formats (TSV, JSON, XML, proprietary schemas) into a common schema (columns: structure_id, organism, reference, source_db, raw_data).: "For each source database in external/dbSource/, run db/../standardizing.R to parse heterogeneous formats (TSV, JSON, XML, proprietary schemas) into a common schema"
- [methods] 2. Consolidate standardized outputs into interim/db/*.tsv files partitioned by data type (organism taxonomy, chemical structure metadata, bibliographic records).: "Consolidate standardized outputs into interim/db/*.tsv files partitioned by data type (organism taxonomy, chemical structure metadata, bibliographic records)"
- [methods] 3. Run common.R translation script on interim/db outputs to map local identifiers to controlled vocabularies (InChI, SMILES, taxonomic ranks), writing interim/dictionaries/common/* lookup tables.: "Run common.R translation script on interim/db outputs to map local identifiers to controlled vocabularies (InChI, SMILES, taxonomic ranks)"
- [methods] 4. Run tcm.R translation script to build Traditional Chinese Medicine and alternative medicine ontology mappings into interim/dictionaries/tcm/*.: "Run tcm.R translation script to build Traditional Chinese Medicine and alternative medicine ontology mappings into interim/dictionaries/tcm/*"
- [methods] 5. Validate output schemas and row counts match input database source counts; verify no critical fields (structure_id, organism_name, reference_doi) are null in >5% of rows.: "Validate output schemas and row counts match input database source counts; verify no critical fields (structure_id, organism_name, reference_doi) are null in >5%"
- [methods] Data originates from 31 initial open databases: "originating from 31 initial open databases"
- [intro] *LOTUS* is a comprehensive collection of documented structure-organism pairs.: "*LOTUS* is a comprehensive collection of documented structure-organism pairs"
