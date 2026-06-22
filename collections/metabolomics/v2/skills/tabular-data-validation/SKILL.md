---
name: tabular-data-validation
description: Use when after curating and integrating structure-organism pairs from multiple sources when you need to produce a high-confidence subset suitable for publication or computational validation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3957
  - http://edamontology.org/topic_0621
  tools:
  - R
  - Make
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- db/../standardizing.R, common.R
- 1_integrating.R
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

# tabular-data-validation

## Summary

Cross-reference curated structure-organism pairs against reference dictionaries (organism, structure, reference) and validate metadata completeness to filter a curated collection down to high-confidence, platinum-tier pairs. This skill ensures that only pairs with verified dictionary entries, complete metadata, and no conflicting assertions advance to downstream analysis.

## When to use

Apply this skill after curating and integrating structure-organism pairs from multiple sources when you need to produce a high-confidence subset suitable for publication or computational validation. Specifically, use it when your input is a merged table of structure-organism pairs with associated literature references and you have authority dictionary files (organism, structure, reference) that define the canonical valid entries for your domain.

## When NOT to use

- Input table is already validated or pre-filtered to high-confidence pairs — re-validation wastes computational resources and risks false rejection.
- Reference dictionaries are incomplete, out-of-date, or not authoritative for your domain — validation results will be unreliable.
- You need to include all curated pairs regardless of metadata completeness or conflicts — use the full curated table instead.

## Inputs

- curated structure-organism pairs table (TSV/GZ format, e.g., interim/tables/3_curated/table.tsv.gz)
- organism reference dictionary (TSV/GZ format, e.g., interim/dictionary/organism/dictionary.tsv.gz)
- structure reference dictionary (TSV/GZ format, e.g., interim/dictionary/structure/dictionary.tsv.gz)
- reference metadata tables (TSV/GZ format, e.g., dictionaryOrganism.tsv.gz, metadata.tsv.gz)

## Outputs

- platinum.tsv.gz — high-confidence structure-organism pairs with validation flags and complete metadata

## How to apply

Load the curated table (e.g., interim/tables/3_curated/table.tsv.gz) alongside reference dictionaries (organism/dictionary.tsv.gz, structure/dictionary.tsv.gz, and reference metadata files). For each structure-organism pair in the curated table, perform three sequential validations: (1) verify that the organism identifier exists in the organism dictionary and that the structure identifier exists in the structure dictionary; (2) check that all associated reference identifiers and their metadata (e.g., literature citations from dictionaryOrganism.tsv.gz and metadata.tsv.gz) are present and non-null; (3) apply quality filters to flag and exclude pairs with conflicting or incomplete assertions. Retain only pairs meeting platinum-tier standards and write them to a new table (platinum.tsv.gz) with all validation flags and metadata columns preserved for traceability.

## Related tools

- **R** (Primary execution environment for loading, cross-referencing, and filtering tabular data using vectorized operations and file I/O (2_validating.R)) — https://github.com/lotusnprod/lotus-processor
- **Make** (Orchestrates the 3_analyzing stage pipeline, including validation workflow invocation) — https://github.com/lotusnprod/lotus-processor

## Examples

```
Rscript 2_validating.R --input interim/tables/3_curated/table.tsv.gz --organism interim/dictionary/organism/dictionary.tsv.gz --structure interim/dictionary/structure/dictionary.tsv.gz --reference interim/dictionary/reference/ --output platinum.tsv.gz
```

## Evaluation signals

- Platinum table row count is strictly ≤ curated table row count (no rows added, only filtered).
- Every structure identifier in platinum.tsv.gz has a matching entry in structure/dictionary.tsv.gz with no null values.
- Every organism identifier in platinum.tsv.gz has a matching entry in organism/dictionary.tsv.gz with no null values.
- All reference metadata columns (e.g., literature citations, dictionaryOrganism entries) are non-null for every platinum row.
- Validation flags and conflict indicators are logged and preserved as columns in platinum.tsv.gz for audit traceability.

## Limitations

- Validation accuracy depends entirely on the completeness and currency of reference dictionaries — stale or sparse dictionaries will over-filter or miss real conflicts.
- The skill does not resolve conflicts or ambiguities; it only flags and excludes pairs with inconsistencies — manual curation may still be needed for borderline cases.
- Performance scales with the size of the curated table and reference dictionaries; very large datasets may require indexed lookups or database queries for efficiency.

## Evidence

- [other] Cross-reference each structure-organism pair against organism and structure dictionaries: "Cross-reference each structure-organism pair against organism dictionary (interim/dictionary/organism/dictionary.tsv.gz) and structure dictionary (interim/dictionary/structure/dictionary.tsv.gz) to"
- [other] Validate reference metadata for literature citations: "Validate reference metadata (interim/dictionary/reference/dictionaryOrganism.tsv.gz and metadata.tsv.gz) for each pair's associated literature citations."
- [other] Apply quality filters to retain platinum-tier pairs: "Apply quality filters to retain only pairs meeting platinum-tier standards (e.g., high-confidence mappings, complete metadata, no conflicting assertions)."
- [other] Write passing pairs with validation flags preserved: "Write passing pairs to platinum.tsv.gz with all validation flags and metadata columns preserved."
- [methods] 3_analyzing stage produces platinum collection: "3_analyzing: 1_sampling.R, 2_validating.R producing platinum.tsv.gz"
