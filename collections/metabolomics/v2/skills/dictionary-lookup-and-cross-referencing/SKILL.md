---
name: dictionary-lookup-and-cross-referencing
description: Use when after integrating and curating raw structure-organism pairs from multiple heterogeneous databases, use this skill when you need to verify that each pair and its associated metadata (literature citations, organism taxonomy, chemical identifiers) exist in your authoritative reference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - R
  - 2_validating.R
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dictionary-lookup-and-cross-referencing

## Summary

Validate structure-organism pairs and their metadata by cross-referencing each pair against curated dictionary records (organism, structure, reference) to identify and flag inconsistencies, missing entries, or conflicting assertions. This skill filters curated data to high-confidence platinum-tier collections suitable for computational natural products research.

## When to use

After integrating and curating raw structure-organism pairs from multiple heterogeneous databases, use this skill when you need to verify that each pair and its associated metadata (literature citations, organism taxonomy, chemical identifiers) exist in your authoritative reference dictionaries and meet quality standards for downstream analysis. Specifically apply when transitioning from the 2_curating stage to the 3_analyzing stage to produce a validated subset (platinum collection).

## When NOT to use

- Input is already a validated platinum or gold-tier collection — re-validation is redundant unless dictionaries have been updated.
- Reference dictionaries are incomplete, unmaintained, or significantly out of date relative to the curated input — cross-referencing will produce spurious rejections.
- The use case prioritizes comprehensiveness over quality — if downstream analysis tolerates noise and missing metadata, this filtering step may be overly restrictive.

## Inputs

- curated structure-organism pair table (TSV.GZ format, e.g., interim/tables/3_curated/table.tsv.gz)
- organism reference dictionary (TSV.GZ, e.g., interim/dictionary/organism/dictionary.tsv.gz)
- structure reference dictionary (TSV.GZ, e.g., interim/dictionary/structure/dictionary.tsv.gz)
- organism reference metadata (TSV.GZ, e.g., interim/dictionary/reference/dictionaryOrganism.tsv.gz)
- reference metadata file (metadata.tsv.gz)

## Outputs

- platinum collection (TSV.GZ, e.g., platinum.tsv.gz)
- validation flags and metadata columns for each retained pair
- audit trail of filtering decisions

## How to apply

Load the curated table (e.g., interim/tables/3_curated/table.tsv.gz) and corresponding reference dictionaries (organism.tsv.gz, structure.tsv.gz) with their metadata files. For each structure-organism pair, perform exact-match or normalized lookups in the organism dictionary to verify presence and consistency of taxonomic identifiers. Cross-check the structure dictionary for valid chemical identifiers and format consistency. Validate associated reference metadata (literature citations via dictionaryOrganism.tsv.gz and metadata.tsv.gz) to ensure cited sources exist and are non-conflicting. Apply tiered quality filters retaining only pairs meeting platinum-tier standards such as high-confidence mappings with complete metadata and no assertion conflicts. Write passing pairs to the output file (platinum.tsv.gz) with all validation flags and metadata columns preserved for audit traceability.

## Related tools

- **R** (primary language for implementing dictionary lookups, cross-referencing logic, validation filters, and output serialization within the 2_validating.R script) — https://github.com/lotusnprod/lotus-processor
- **2_validating.R** (script that orchestrates the validation filter within the 3_analyzing stage, loading curated pairs and dictionaries, performing cross-reference checks, and writing platinum.tsv.gz) — https://github.com/lotusnprod/lotus-processor

## Examples

```
Rscript 2_validating.R --input interim/tables/3_curated/table.tsv.gz --organism_dict interim/dictionary/organism/dictionary.tsv.gz --structure_dict interim/dictionary/structure/dictionary.tsv.gz --reference_meta interim/dictionary/reference/metadata.tsv.gz --output platinum.tsv.gz
```

## Evaluation signals

- Output platinum.tsv.gz row count is ≤ input curated table row count (filtering is restrictive, not expansive).
- All retained pairs have non-null entries in organism, structure, and reference metadata columns.
- Spot-check: randomly sample 50–100 platinum pairs and verify each organism ID exists in organism dictionary and each structure ID exists in structure dictionary via direct lookup.
- Validation flag columns in platinum.tsv.gz are consistently populated (no silent NULL values where flags should exist) and reflect the filtering logic applied.
- No pair in platinum.tsv.gz has conflicting assertions in metadata (e.g., same pair linked to contradictory literature citations or organism taxonomies).

## Limitations

- Dictionary lookups assume exact or pre-normalized string matching; typos, encoding errors, or legacy aliases in curated pairs may cause false rejections if not harmonized before lookup.
- Cross-referencing is only as rigorous as the completeness and accuracy of the reference dictionaries; if dictionaries omit valid pairs or contain stale entries, filtering will produce biased results.
- Platinum-tier thresholds (e.g., 'high-confidence mappings', 'complete metadata') are not quantified in the source material; operationalization requires domain expertise and iterative tuning.
- Validation performance may degrade on very large tables (>500k pairs) if dictionaries are not indexed; naive nested lookups can become a bottleneck.

## Evidence

- [methods] Cross-reference each structure-organism pair against dictionaries: "Cross-reference each structure-organism pair against organism dictionary (interim/dictionary/organism/dictionary.tsv.gz) and structure dictionary (interim/dictionary/structure/dictionary.tsv.gz) to"
- [methods] Validate reference metadata for literature citations: "Validate reference metadata (interim/dictionary/reference/dictionaryOrganism.tsv.gz and metadata.tsv.gz) for each pair's associated literature citations."
- [methods] Apply quality filters to retain platinum-tier standards: "Apply quality filters to retain only pairs meeting platinum-tier standards (e.g., high-confidence mappings, complete metadata, no conflicting assertions)."
- [methods] Output platinum collection with validation flags preserved: "Write passing pairs to platinum.tsv.gz with all validation flags and metadata columns preserved."
- [other] 2_validating.R operates as validation filter in 3_analyzing stage: "The 2_validating.R step operates within the 3_analyzing stage as a validation filter that processes curated pairs and produces platinum.tsv.gz as its output."
