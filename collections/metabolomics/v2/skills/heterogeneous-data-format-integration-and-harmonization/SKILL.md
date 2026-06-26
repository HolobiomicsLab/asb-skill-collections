---
name: heterogeneous-data-format-integration-and-harmonization
description: Use when your input consists of multiple external databases with different
  file formats, column names, identifier schemes, and taxonomic/chemical vocabularies
  (e.g., 31 open natural product databases with heterogeneous structure and organism
  metadata).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0637
  tools:
  - R
  - Python 3
  - Make
  - standardizing.R
  - common.R
  - tcm.R
  license_tier: restricted
  provenance_tier: literature
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

# heterogeneous-data-format-integration-and-harmonization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Standardize and ingest multiple heterogeneous source databases (TSV, JSON, XML, proprietary schemas) into a unified tabular format using format-specific parsing scripts and controlled-vocabulary mapping. This skill is essential when combining natural product data from 31+ independent sources with incompatible schemas into a single, queryable repository.

## When to use

Your input consists of multiple external databases with different file formats, column names, identifier schemes, and taxonomic/chemical vocabularies (e.g., 31 open natural product databases with heterogeneous structure and organism metadata). You need a canonical tabular representation with reconciled identifiers and standardized fields (structure_id, organism, reference, source_db) before downstream curation or analysis.

## When NOT to use

- Input data is already in a single, consistent tabular format with standardized identifiers and controlled vocabulary — apply this skill only to genuinely heterogeneous sources.
- The integration goal is exploratory join or entity linking only, not canonical harmonization; use a more lightweight mapping approach instead.
- Critical source-specific metadata or domain context would be lost by forcing all sources into a single common schema (consider a layered schema with source-specific extensions).

## Inputs

- Raw source databases in heterogeneous formats (TSV, JSON, XML, proprietary schemas) from external/dbSource/
- Format specification or sample records from each source database
- Target common schema specification (columns: structure_id, organism, reference, source_db, raw_data)

## Outputs

- Standardized interim/db/*.tsv files partitioned by data type (organism taxonomy, chemical structure metadata, bibliographic records)
- interim/dictionaries/common/* lookup tables mapping local identifiers to controlled vocabularies (InChI, SMILES, taxonomic ranks)
- interim/dictionaries/tcm/* ontology mapping files for Traditional Chinese Medicine and alternative medicine terms
- Validation report with schema conformance and null-field frequencies for each source

## How to apply

For each source database in external/dbSource/, execute a format-specific standardizing.R script that parses the native format (TSV, JSON, XML, or proprietary schema) and maps it to a common schema with required columns: structure_id, organism, reference, source_db, raw_data. Consolidate standardized outputs into interim/db/*.tsv files partitioned by data type (organism taxonomy, chemical structure metadata, bibliographic records). Next, run common.R translation script on interim/db outputs to map local identifiers to controlled vocabularies (InChI, SMILES, taxonomic ranks), producing interim/dictionaries/common/* lookup tables. Then apply tcm.R translation script to build Traditional Chinese Medicine and alternative medicine ontology mappings into interim/dictionaries/tcm/*. Finally, validate output schemas and row counts match input database source counts; flag any critical fields (structure_id, organism_name, reference_doi) with >5% null values as requiring manual review or exclusion.

## Related tools

- **standardizing.R** (Parse heterogeneous source database formats (TSV, JSON, XML, proprietary schemas) into a common schema with canonical columns (structure_id, organism, reference, source_db, raw_data)) — https://github.com/lotusnprod/lotus-processor
- **common.R** (Translate local identifiers in interim/db outputs to controlled vocabularies (InChI, SMILES, taxonomic ranks) and generate interim/dictionaries/common/* lookup tables) — https://github.com/lotusnprod/lotus-processor
- **tcm.R** (Build Traditional Chinese Medicine and alternative medicine ontology mappings into interim/dictionaries/tcm/* from standardized organism and structure data) — https://github.com/lotusnprod/lotus-processor
- **R** (Scripting language for parsing, standardization, translation, and validation)
- **Python 3** (Supplementary language for data sanitization and chemical structure utilities)
- **Make** (Build automation and workflow orchestration across standardizing, translating, and validation steps) — https://www.gnu.org/software/make

## Examples

```
cd lotus-processor && make MODE=test lotus-bloom
```

## Evaluation signals

- Output schema conforms to canonical columns (structure_id, organism, reference, source_db, raw_data) with no unexpected columns or data types.
- Row counts in standardized interim/db/*.tsv files match input source database counts (or documented reduction rationale if records were deduplicated or filtered).
- No critical fields (structure_id, organism_name, reference_doi) have >5% null values in the final consolidated output; null frequencies are ≤5% and documented.
- Lookup tables in interim/dictionaries/common/* and interim/dictionaries/tcm/* contain expected identifiers and mappings with no unmapped orphan records.
- A representative sample of standardized records can be spot-checked against original source records to verify format fidelity and correct identity preservation (e.g., structure IDs, organism names, reference DOIs).

## Limitations

- The common schema may lose source-specific metadata or nuances if forced into canonical columns; consider preserving raw_data JSON blobs or source-specific extensions.
- Controlled vocabulary mapping (InChI, SMILES, taxonomic ranks) depends on availability of reference resources and may produce unmapped or ambiguous identifiers for novel or rare organisms/structures.
- No automated changelog or version tracking documented for the standardization scripts themselves, making reproducibility and debugging of schema changes difficult across LOTUS releases.
- Null-field thresholds (>5%) are heuristic; sources with legitimate sparsity in certain fields (e.g., reference_doi) may be incorrectly flagged or excluded.

## Evidence

- [methods] standardizing.R script parse heterogeneous formats: "For each source database in external/dbSource/, run db/../standardizing.R to parse heterogeneous formats (TSV, JSON, XML, proprietary schemas) into a common schema (columns: structure_id, organism,"
- [methods] common.R and tcm.R translation scripts: "Run common.R translation script on interim/db outputs to map local identifiers to controlled vocabularies (InChI, SMILES, taxonomic ranks), writing interim/dictionaries/common/* lookup tables. 4. Run"
- [methods] validation schema and null-field thresholds: "Validate output schemas and row counts match input database source counts; verify no critical fields (structure_id, organism_name, reference_doi) are null in >5% of rows."
- [methods] 31 initial open databases: "Data originates from 31 initial open databases"
- [readme] LOTUS comprehensive collection rationale: "*LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented"
